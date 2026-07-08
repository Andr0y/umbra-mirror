using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace ReIDEval
{
    class ReIDEvaluation
    {
        // === CONFIG ===
        const int IMG_WIDTH = 224;
        const int IMG_HEIGHT = 224;

        // Preprocess image (System.Drawing) -> CHW normalized floats
        static float[] PreprocessImage(string imagePath)
        {
            using var src = new Bitmap(imagePath);
            var resized = new Bitmap(IMG_WIDTH, IMG_HEIGHT, PixelFormat.Format24bppRgb);
            using (var g = Graphics.FromImage(resized))
            {
                g.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;
                g.DrawImage(src, 0, 0, IMG_WIDTH, IMG_HEIGHT);
            }

            var rect = new Rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT);
            var bmpData = resized.LockBits(rect, ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
            try
            {
                int stride = Math.Abs(bmpData.Stride);
                int bytes = stride * IMG_HEIGHT;
                byte[] buffer = new byte[bytes];
                Marshal.Copy(bmpData.Scan0, buffer, 0, bytes);

                float[] chw = new float[3 * IMG_HEIGHT * IMG_WIDTH];
                int channelStride = IMG_HEIGHT * IMG_WIDTH;

                for (int y = 0; y < IMG_HEIGHT; y++)
                {
                    int row = y * stride;
                    for (int x = 0; x < IMG_WIDTH; x++)
                    {
                        int idx = row + x * 3;
                        float b = buffer[idx + 0] / 255f;
                        float g = buffer[idx + 1] / 255f;
                        float r = buffer[idx + 2] / 255f;

                        // ImageNet normalization (same as torchvision used in Python)
                        r = (r - 0.485f) / 0.229f;
                        g = (g - 0.456f) / 0.224f;
                        b = (b - 0.406f) / 0.225f;

                        int pos = y * IMG_WIDTH + x;
                        chw[0 * channelStride + pos] = r;
                        chw[1 * channelStride + pos] = g;
                        chw[2 * channelStride + pos] = b;
                    }
                }

                return chw;
            }
            finally
            {
                resized.UnlockBits(bmpData);
            }
        }

        // Extract single-image feature using ONNX session
        static float[] ExtractFeatures(InferenceSession session, string inputName, string outputName, string imagePath)
        {
            float[] chw = PreprocessImage(imagePath);

            // Build [1,3,H,W] tensor
            var tensor = new DenseTensor<float>(new[] { 1, 3, IMG_HEIGHT, IMG_WIDTH });
            // copy CHW into tensor buffer
            for (int i = 0; i < chw.Length; i++)
                tensor.Buffer.Span[i] = chw[i];

            // Create inputs list (note: list itself is not disposable)
            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor(inputName, tensor)
            };

            try
            {
                // Run inference (results is disposable)
                using IDisposableReadOnlyCollection<DisposableNamedOnnxValue> results = session.Run(inputs);
                var output = results.First(x => x.Name == outputName).AsEnumerable<float>().ToArray();

                // L2 normalize
                float norm = (float)Math.Sqrt(output.Select(v => v * v).Sum());
                if (norm == 0f) norm = 1e-12f;
                for (int i = 0; i < output.Length; i++) output[i] /= norm;

                return output;
            }
            finally
            {
                // Dispose inputs individually (they implement IDisposable)
                foreach (var n in inputs);
            }
        }

        static double EuclideanDistance(float[] a, float[] b)
        {
            double sum = 0;
            for (int i = 0; i < a.Length; i++)
            {
                double d = a[i] - b[i];
                sum += d * d;
            }
            return Math.Sqrt(sum);
        }

        // Entry point for evaluation
        public static void Main(string[] args)
        {
            // Expecting: <modelPath> <inputName> <outputName> <inferenceSortedDir> <groundTruthDir>
            if (args.Length < 5)
            {
                Console.WriteLine("Usage: dotnet run --project ReIDeval/ReIDeval.csproj -- <model.onnx> <inputName> <outputName> <inference_sorted_dir> <ground_truth_dir>");
                Console.WriteLine("Example: dotnet run --project ReIDeval/ReIDeval.csproj -- swin_model.onnx input output ./sorted ./ground_truth");
                return;
            }

            string modelPath = args[0];
            string inputName = args[1];
            string outputName = args[2];
            string inferenceSortedDir = args[3];
            string groundTruthDir = args[4];

            if (!File.Exists(modelPath))
            {
                Console.WriteLine($"Model file not found: {modelPath}");
                return;
            }

            if (!Directory.Exists(inferenceSortedDir))
            {
                Console.WriteLine($"Inference sorted dir not found: {inferenceSortedDir}");
                return;
            }

            if (!Directory.Exists(groundTruthDir))
            {
                Console.WriteLine($"Ground truth dir not found: {groundTruthDir}");
                return;
            }

            using var session = new InferenceSession(modelPath);

            // Build filename -> GT id map
            var filenameToGT = new Dictionary<string, string>();
            foreach (var gtFolder in Directory.GetDirectories(groundTruthDir))
            {
                string gtId = Path.GetFileName(gtFolder);
                foreach (var file in Directory.GetFiles(gtFolder))
                {
                    string fname = Path.GetFileName(file);
                    filenameToGT[fname] = gtId;
                }
            }

            int totalImages = 0;
            int correctlyClustered = 0;
            var clusterStats = new Dictionary<string, (string majority, int correct, int total)>();
            var wronglyClustered = new List<(string fname, string cluster, string gt, string predicted, double dist)>();

            Console.WriteLine("\nEvaluating clusters...");
            foreach (var clusterFolder in Directory.GetDirectories(inferenceSortedDir))
            {
                string clusterId = Path.GetFileName(clusterFolder);
                var imgFiles = Directory.GetFiles(clusterFolder)
                                        .Where(f => f.EndsWith(".jpg", StringComparison.OrdinalIgnoreCase)
                                                 || f.EndsWith(".jpeg", StringComparison.OrdinalIgnoreCase)
                                                 || f.EndsWith(".png", StringComparison.OrdinalIgnoreCase))
                                        .OrderBy(f => f)
                                        .ToArray();
                if (imgFiles.Length == 0) continue;

                var feats = new List<float[]>();
                var gtIds = new List<string>();
                var validFiles = new List<string>();

                // Extract features for all images in this cluster
                foreach (var fullPath in imgFiles)
                {
                    try
                    {
                        var feat = ExtractFeatures(session, inputName, outputName, fullPath);
                        feats.Add(feat);

                        string fname = Path.GetFileName(fullPath);
                        string originalName = fname.Contains("_code") ? fname.Split(new[] { "_code" }, StringSplitOptions.None).Last() : fname;
                        if (filenameToGT.TryGetValue(originalName, out string gt))
                        {
                            gtIds.Add(gt);
                            validFiles.Add(fname);
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Failed to process {fullPath}: {ex.Message}");
                    }
                }

                if (gtIds.Count == 0) continue; // nothing to evaluate in this cluster

                totalImages += gtIds.Count;

                // majority GT
                var majorityGroup = gtIds.GroupBy(x => x).OrderByDescending(g => g.Count()).First();
                string majorityGT = majorityGroup.Key;
                int correct = majorityGroup.Count();

                // loner cluster special rule
                if (imgFiles.Length == 1) correct = 0;

                correctlyClustered += correct;
                clusterStats[clusterId] = (majorityGT, correct, gtIds.Count);

                // compute center (mean of feats)
                float[] center = new float[feats[0].Length];
                foreach (var f in feats)
                    for (int i = 0; i < center.Length; i++)
                        center[i] += f[i];
                for (int i = 0; i < center.Length; i++) center[i] /= feats.Count;

                // misclassified
                for (int i = 0; i < validFiles.Count; i++)
                {
                    if (imgFiles.Length == 1 || gtIds[i] != majorityGT)
                    {
                        double dist = EuclideanDistance(feats[i], center);
                        wronglyClustered.Add((validFiles[i], clusterId, gtIds[i], majorityGT, dist));
                    }
                }
            }

            double precision = totalImages > 0 ? (double)correctlyClustered / totalImages : 0.0;

            Console.WriteLine("\nEvaluation complete.");
            Console.WriteLine($"Total images evaluated: {totalImages}");
            Console.WriteLine($"Correctly clustered images: {correctlyClustered}");
            Console.WriteLine($"Model precision: {precision:F4}\n");

            Console.WriteLine("Per-cluster breakdown:");
            foreach (var kv in clusterStats.OrderBy(k => k.Key))
            {
                var s = kv.Value;
                double acc = s.total > 0 ? (double)s.correct / s.total : 0.0;
                Console.WriteLine($"- Cluster {kv.Key}: {s.correct}/{s.total} correct ({acc:P2}) → Majority GT ID: {s.majority}");
            }

            if (wronglyClustered.Count > 0)
            {
                Console.WriteLine("\nWrongly clustered images:");
                foreach (var w in wronglyClustered)
                    Console.WriteLine($"  {w.fname} → cluster: {w.cluster}, GT: {w.gt}, Pred: {w.predicted}, dist: {w.dist:F4}");
            }
            else
            {
                Console.WriteLine("\nNo wrongly clustered images found.");
            }
        }
    }
}

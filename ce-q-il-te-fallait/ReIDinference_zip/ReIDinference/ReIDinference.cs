using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using System.Linq;
using System.Collections.Generic;
using System;


class ReIDInference
{
    // === IMAGE PREPROCESSING ===
    static float[] PreprocessImage_SystemDrawing(string imagePath, int targetWidth, int targetHeight)
    {
        using var src = new Bitmap(imagePath);

        // Resize to target
        var resized = new Bitmap(targetWidth, targetHeight, PixelFormat.Format24bppRgb);
        using (var g = Graphics.FromImage(resized))
        {
            g.InterpolationMode = InterpolationMode.HighQualityBicubic;
            g.CompositingQuality = CompositingQuality.HighQuality;
            g.SmoothingMode = SmoothingMode.HighQuality;
            g.DrawImage(src, 0, 0, targetWidth, targetHeight);
        }

        // Lock bits (24bpp = BGR order in memory)
        var rect = new Rectangle(0, 0, targetWidth, targetHeight);
        var bmpData = resized.LockBits(rect, ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
        try
        {
            int stride = Math.Abs(bmpData.Stride);
            int bytes = stride * targetHeight;
            byte[] raw = new byte[bytes];
            Marshal.Copy(bmpData.Scan0, raw, 0, bytes);

            // Prepare CHW array: [R_channel, G_channel, B_channel] each channel is H*W
            float[] chw = new float[3 * targetHeight * targetWidth];
            int channelStride = targetHeight * targetWidth;

            for (int y = 0; y < targetHeight; y++)
            {
                int rowStart = y * stride;
                for (int x = 0; x < targetWidth; x++)
                {
                    int idx = rowStart + x * 3; // B, G, R
                    byte b = raw[idx + 0];
                    byte g = raw[idx + 1];
                    byte r = raw[idx + 2];

                    int pos = y * targetWidth + x; // H*W index
                    // Normalize using ImageNet mean/std
                    float rf = (r / 255f - 0.485f) / 0.229f;
                    float gf = (g / 255f - 0.456f) / 0.224f;
                    float bf = (b / 255f - 0.406f) / 0.225f;

                    chw[0 * channelStride + pos] = rf; // R channel
                    chw[1 * channelStride + pos] = gf; // G channel
                    chw[2 * channelStride + pos] = bf; // B channel
                }
            }

            return chw;
        }
        finally
        {
            resized.UnlockBits(bmpData);
            resized.Dispose();
        }
    }

    // === FEATURE EXTRACTION ===
    static float[] ExtractFeatures_Onnx(InferenceSession session, string inputName, string outputName, string imagePath, int width, int height)
    {
        float[] chw = PreprocessImage_SystemDrawing(imagePath, width, height);

        var tensor = new DenseTensor<float>(new[] { 1, 3, height, width });
        int channelSize = height * width;
        for (int c = 0; c < 3; c++)
        {
            int baseIdx = c * channelSize;
            for (int i = 0; i < channelSize; i++)
                tensor.Buffer.Span[c * channelSize + i] = chw[baseIdx + i];
        }

        var inputs = new List<NamedOnnxValue>
        {
            NamedOnnxValue.CreateFromTensor(inputName, tensor)
        };

        using var results = session.Run(inputs);
        var raw = results.First(r => r.Name == outputName).AsEnumerable<float>().ToArray();

        // L2 normalize
        float norm = (float)Math.Sqrt(raw.Select(v => v * v).Sum());
        if (norm == 0f) norm = 1e-12f;
        for (int i = 0; i < raw.Length; i++) raw[i] /= norm;

        return raw;
    }

    static double EuclideanDistance(float[] a, float[] b)
    {
        double sum = 0;
        for (int i = 0; i < a.Length; i++)
        {
            double diff = a[i] - b[i];
            sum += diff * diff;
        }
        return Math.Sqrt(sum);
    }

    // === MAIN ===
    static void Main(string[] args)
    {
        // === CONFIG ===
        string modelPath = "ReIDinference/swin_model.onnx";
        string inputName = "input";     // replace with actual input node name if needed
        string outputName = "output";   // replace with actual output node name
        string unsortedDir = "ReIDinference/unsorted";
        string sortedDir = "ReIDinference/sorted";
        float similarityThreshold = 0.65f;
        int imgSize = 224;
        double maxLonerDistance = 0.75;

        Directory.CreateDirectory(sortedDir);

        // === MODEL ===
        using var session = new InferenceSession(modelPath);

        // === PHASE 0: Feature Extraction ===
        var imagePaths = Directory.GetFiles(unsortedDir, "*.jpg");
        var features = new List<float[]>();
        var paths = new List<string>();

        Console.WriteLine("\nExtracting embeddings...");
        foreach (var path in imagePaths)
        {
            var vec = ExtractFeatures_Onnx(session, inputName, outputName, path, imgSize, imgSize);
            features.Add(vec);
            paths.Add(path);
        }

        // === Continue with clustering ===
        var seedFeatures = new List<float[]>();
        var seedIds = new List<string>();
        var clusterFeatureBank = new List<List<float[]>>();
        var assignedIndices = new HashSet<int>();

        int identityCounter = 1;

        Console.WriteLine("\nPhase 1: Discovering initial identities...");
        for (int i = 0; i < features.Count; i++)
        {
            var feat = features[i];
            var path = paths[i];

            if (seedFeatures.Count > 0)
            {
                var dists = seedFeatures.Select(sf => EuclideanDistance(feat, sf)).ToArray();
                double bestDist = dists.Min();
                int bestIdx = Array.IndexOf(dists, bestDist);

                if (bestDist <= similarityThreshold)
                {
                    string identityName = seedIds[bestIdx];
                    clusterFeatureBank[bestIdx].Add(feat);
                    Directory.CreateDirectory(Path.Combine(sortedDir, identityName));
                    File.Copy(path, Path.Combine(sortedDir, identityName, Path.GetFileName(path)), true);
                    Console.WriteLine($"Assigned {Path.GetFileName(path)} → {identityName} (dist={bestDist:F3})");
                }
                else
                {
                    string identityName = identityCounter.ToString("D4");
                    identityCounter++;
                    seedFeatures.Add(feat);
                    seedIds.Add(identityName);
                    clusterFeatureBank.Add(new List<float[]> { feat });
                    Directory.CreateDirectory(Path.Combine(sortedDir, identityName));
                    File.Copy(path, Path.Combine(sortedDir, identityName, Path.GetFileName(path)), true);
                    Console.WriteLine($"Created new ID {identityName} for {Path.GetFileName(path)} (dist={bestDist:F3})");
                }
            }
            else
            {
                string identityName = identityCounter.ToString("D4");
                identityCounter++;
                seedFeatures.Add(feat);
                seedIds.Add(identityName);
                clusterFeatureBank.Add(new List<float[]> { feat });
                Directory.CreateDirectory(Path.Combine(sortedDir, identityName));
                File.Copy(path, Path.Combine(sortedDir, identityName, Path.GetFileName(path)), true);
                Console.WriteLine($"Created first ID {identityName} for {Path.GetFileName(path)}");
            }
            assignedIndices.Add(i);
        }


        // === PHASE 2: Assign remaining ===
        Console.WriteLine("\nPhase 2: Assigning remaining images...");
        for (int i = 0; i < features.Count; i++)
        {
            if (assignedIndices.Contains(i)) continue;
            var feat = features[i];
            var path = paths[i];

            double bestSim = double.NegativeInfinity;
            int bestIdx = -1;

            for (int j = 0; j < clusterFeatureBank.Count; j++)
            {
                if (clusterFeatureBank[j].Count == 0) continue;
                var clusterCenter = clusterFeatureBank[j][0]; // use first feature
                double dist = EuclideanDistance(feat, clusterCenter);
                double sim = -dist;
                if (sim > bestSim)
                {
                    bestSim = sim;
                    bestIdx = j;
                }
            }

            if (bestIdx == -1)
            {
                string identityName = identityCounter.ToString("D4");
                identityCounter++;
                Directory.CreateDirectory(Path.Combine(sortedDir, identityName));
                File.Copy(path, Path.Combine(sortedDir, identityName, Path.GetFileName(path)), true);
                seedIds.Add(identityName);
                seedFeatures.Add(feat);
                clusterFeatureBank.Add(new List<float[]> { feat });
                assignedIndices.Add(i);
                Console.WriteLine($"Fallback new ID {identityName} for {Path.GetFileName(path)} (no valid match)");
            }
            else
            {
                string assignedId = seedIds[bestIdx];
                Directory.CreateDirectory(Path.Combine(sortedDir, assignedId));
                File.Copy(path, Path.Combine(sortedDir, assignedId, Path.GetFileName(path)), true);
                clusterFeatureBank[bestIdx].Add(feat);
                assignedIndices.Add(i);
                Console.WriteLine($"Assigned {Path.GetFileName(path)} → {assignedId} (sim={-bestSim:F3})");
            }
        }

        // === PHASE 3: Merge loners ===
        Console.WriteLine("\nPhase 3: Merging loners...");
        string unknownDir = Path.Combine(sortedDir, "unknown");
        Directory.CreateDirectory(unknownDir);

        while (true)
        {
            var lonerDirs = new List<(int idx, string filename)>();
            for (int idx = 0; idx < clusterFeatureBank.Count; idx++)
            {
                string idPath = Path.Combine(sortedDir, seedIds[idx]);
                if (!Directory.Exists(idPath)) continue;
                var files = Directory.GetFiles(idPath, "*.jpg");
                if (files.Length == 1)
                    lonerDirs.Add((idx, Path.GetFileName(files[0])));
            }

            if (!lonerDirs.Any())
            {
                Console.WriteLine("No more loners found.");
                break;
            }

            bool movedAny = false;
            foreach (var (idx, filename) in lonerDirs)
            {
                string sourceDir = Path.Combine(sortedDir, seedIds[idx]);
                string sourcePath = Path.Combine(sourceDir, filename);
                if (!File.Exists(sourcePath)) continue;

                var sourceFeat = clusterFeatureBank[idx].First();
                double bestDist = double.MaxValue;
                int bestIdx = -1;

                for (int j = 0; j < clusterFeatureBank.Count; j++)
                {
                    if (j == idx || clusterFeatureBank[j].Count == 0) continue;
                    var clusterCenter = clusterFeatureBank[j].Aggregate(new float[sourceFeat.Length],
                        (acc, vec) => { for (int k = 0; k < acc.Length; k++) acc[k] += vec[k]; return acc; });
                    for (int k = 0; k < clusterCenter.Length; k++) clusterCenter[k] /= clusterFeatureBank[j].Count;
                    double dist = EuclideanDistance(sourceFeat, clusterCenter);
                    if (dist < bestDist)
                    {
                        bestDist = dist;
                        bestIdx = j;
                    }
                }

                if (bestIdx != -1 && bestDist <= maxLonerDistance)
                {
                    string targetDir = Path.Combine(sortedDir, seedIds[bestIdx]);
                    Directory.CreateDirectory(targetDir);
                    File.Move(sourcePath, Path.Combine(targetDir, filename), true);
                    clusterFeatureBank[bestIdx].Add(sourceFeat);
                    Directory.Delete(sourceDir, true);
                    clusterFeatureBank[idx].Clear();
                    movedAny = true;
                    Console.WriteLine($"Merged loner {filename} → {seedIds[bestIdx]} (dist={bestDist:F3})");
                }
                else
                {
                    File.Move(sourcePath, Path.Combine(unknownDir, filename), true);
                    Directory.Delete(sourceDir, true);
                    clusterFeatureBank[idx].Clear();
                    Console.WriteLine($"Skipped merging {filename} → unknown (dist={bestDist:F3})");
                }
            }

            if (!movedAny)
            {
                Console.WriteLine("No more loner merges possible.");
                break;
            }
        }

        // === PHASE 4: Missing images ===
        Console.WriteLine("\nPhase 4: Saving unassigned images to 'unknown'...");
        var originalPaths = new HashSet<string>(imagePaths.Select(Path.GetFullPath));
        var clusteredPaths = new HashSet<string>(
            Directory.GetFiles(sortedDir, "*.jpg", SearchOption.AllDirectories).Select(Path.GetFullPath));

        var missingPaths = originalPaths.Where(p => !clusteredPaths.Any(cp => Path.GetFileName(cp) == Path.GetFileName(p))).ToList();

        foreach (var missing in missingPaths)
        {
            File.Copy(missing, Path.Combine(unknownDir, Path.GetFileName(missing)), true);
        }

        // === SUMMARY ===
        Console.WriteLine($"\n- Summary:");
        Console.WriteLine($"Original images found: {originalPaths.Count}");
        Console.WriteLine($"Images placed in clusters: {clusteredPaths.Count}");
        Console.WriteLine($"Images copied to unknown: {missingPaths.Count}");
    }
}

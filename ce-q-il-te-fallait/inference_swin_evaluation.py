import os
import glob
import argparse
import torch
import numpy as np
from PIL import Image
from collections import Counter
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import euclidean_distances
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, Dataset
import sys
sys.path.append("../Person_reID_baseline_pytorch/model/swin_p0.5_circle_w5_b16_lr0.01")
from tools.model import ft_net_swin

# === CONFIG ===
IMG_SIZE = (224, 224)
USE_GPU = torch.cuda.is_available()
MODEL_PATH = 'C:/Users/c.erades/OneDrive - STACKR/Bureau/Re-id project/reid-implementation-main/reid_official/R-D IA/savedModels/net_last.pth'
TRAIN_DIR = '../../Market-1501-v15.09.15 (2)/pytorch'  # Used only to get num_classes

# === TRANSFORMS ===
transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# === DATASET CLASS ===
class ImagePathDataset(Dataset):
    def __init__(self, paths):
        self.paths = paths
        self.transform = transform

    def __getitem__(self, idx):
        path = self.paths[idx]
        img = Image.open(path).convert('RGB')
        return self.transform(img), path

    def __len__(self):
        return len(self.paths)

def extract_features(model, image_paths):
    dataset = ImagePathDataset(image_paths)
    loader = DataLoader(dataset, batch_size=64, shuffle=False)
    features = []
    paths = []

    with torch.no_grad():
        for imgs, batch_paths in loader:
            if USE_GPU:
                imgs = imgs.cuda()
            feats = model(imgs).cpu().numpy()
            feats = normalize(feats, axis=1)
            features.append(feats)
            paths.extend(batch_paths)

    return np.vstack(features), paths

def evaluate_clustering(inference_sorted_dir, ground_truth_sorted_dir, verbose=False):
    # === Load model ===
    print("🔧 Loading model...")
    train_data = ImageFolder(os.path.join(TRAIN_DIR, 'train'), transform)
    model = ft_net_swin(len(train_data.classes))
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    model.eval()
    if USE_GPU:
        model = model.cuda()

    # === Build filename to GT ID mapping ===
    filename_to_gt_id = {}
    for gt_folder in os.listdir(ground_truth_sorted_dir):
        gt_folder_path = os.path.join(ground_truth_sorted_dir, gt_folder)
        if not os.path.isdir(gt_folder_path):
            continue
        for img_path in glob.glob(os.path.join(gt_folder_path, '*.jpg')):
            filename = os.path.basename(img_path)
            filename_to_gt_id[filename] = gt_folder

    total_images = 0
    correctly_clustered = 0
    wrongly_clustered_files = []
    cluster_stats = {}

    print("\n🔍 Evaluating clusters...")
    for cluster_id in os.listdir(inference_sorted_dir):
        cluster_path = os.path.join(inference_sorted_dir, cluster_id)
        if not os.path.isdir(cluster_path):
            continue

        img_files = sorted([
            f for f in os.listdir(cluster_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])
        if len(img_files) == 0:
            continue

        img_paths = [os.path.join(cluster_path, f) for f in img_files]
        feats, _ = extract_features(model, img_paths)

        cluster_center = np.mean(feats, axis=0, keepdims=True)

        gt_ids = []
        valid_filenames = []

        for f in img_files:
            original_name = f.split('_code')[-1] if '_code' in f else f
            gt_id = filename_to_gt_id.get(original_name)
            if gt_id:
                gt_ids.append(gt_id)
                valid_filenames.append(f)

        if not gt_ids:
            continue  # skip clusters with no known GT matches

        total_images += len(gt_ids)
        majority_gt_id, correct_count = Counter(gt_ids).most_common(1)[0]

        # Count loner clusters as invalid (0% correct)
        if len(img_files) == 1:
            correct_count = 0

        correctly_clustered += correct_count
        cluster_stats[cluster_id] = {
            'majority_gt_id': majority_gt_id,
            'correct': correct_count,
            'total': len(gt_ids),
            'accuracy': correct_count / len(gt_ids) if len(gt_ids) > 0 else 0
        }

        # Compute misclassified filenames + distances
        for i, (feat, fname, gt_id) in enumerate(zip(feats, valid_filenames, gt_ids)):
            if len(img_files) == 1 or gt_id != majority_gt_id:
                dist = euclidean_distances([feat], cluster_center)[0][0]
                wrongly_clustered_files.append((fname, cluster_id, gt_id, majority_gt_id, dist))

    # === Final stats ===
    precision = correctly_clustered / total_images if total_images > 0 else 0.0
    print(f"\n✅ Evaluation complete.")
    print(f"Total images evaluated: {total_images}")
    print(f"Correctly clustered images: {correctly_clustered}")
    print(f"Model precision: {precision:.4f}")

    if verbose:
        print("\n📊 Per-cluster breakdown:")
        for cluster, stats in sorted(cluster_stats.items()):
            print(f"- Cluster {cluster}: {stats['correct']}/{stats['total']} correct "
                  f"({stats['accuracy']:.2%}) → Majority GT ID: {stats['majority_gt_id']}")

    if wrongly_clustered_files:
        print("\n❌ Wrongly clustered images (filename | cluster | GT | predicted | distance):")
        for fname, cluster, true_id, pred_id, dist in wrongly_clustered_files:
            print(f"  {fname} → cluster: {cluster}, GT: {true_id}, Pred: {pred_id}, dist: {dist:.4f}")
    else:
        print("\n✅ No wrongly clustered images found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate clustering accuracy using ground truth.")
    parser.add_argument("inference_sorted_dir", type=str, help="Path to the directory with predicted clusters.")
    parser.add_argument("ground_truth_sorted_dir", type=str, help="Path to the ground truth image folders.")
    parser.add_argument("--verbose", action="store_true", help="Print per-cluster breakdown.")

    args = parser.parse_args()

    evaluate_clustering(
        inference_sorted_dir=args.inference_sorted_dir,
        ground_truth_sorted_dir=args.ground_truth_sorted_dir,
        verbose=args.verbose
    )

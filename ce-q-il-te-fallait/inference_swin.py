#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import torch
import shutil
import glob
import numpy as np
from PIL import Image
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import euclidean_distances
from torchvision import transforms, datasets
from torch.utils.data import Dataset, DataLoader
import argparse
import sys
sys.path.append("../Person_reID_baseline_pytorch/model/swin_p0.5_circle_w5_b16_lr0.01")
from tools.model import ft_net_swin

# === DATASET CLASS ===
class ImagePathDataset(Dataset):
    def __init__(self, paths, transform):
        self.paths = paths
        self.transform = transform

    def __getitem__(self, idx):
        path = self.paths[idx]
        img = Image.open(path).convert('RGB')
        return self.transform(img), path

    def __len__(self):
        return len(self.paths)

# === MAIN PIPELINE ===
def main(args):
    # === CONFIG ===
    UNSORTED_DIR = args.unsorted_dir
    SORTED_DIR = args.sorted_dir
    SIMILARITY_THRESHOLD = args.similarity_threshold
    USE_GPU = torch.cuda.is_available() and not args.no_cuda
    IMG_SIZE = tuple(args.img_size)
    MODEL_PATH = args.model_path
    TRAIN_DIR = args.train_dir

    # === TRANSFORMS ===
    transform = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # === MODEL LOADING ===
    image_datasets = {}
    image_datasets['train'] = datasets.ImageFolder(os.path.join(TRAIN_DIR, 'train'), transform)
    class_names = image_datasets['train'].classes
    num_classes = len(class_names)
    model = ft_net_swin(class_num=num_classes)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()
    if USE_GPU:
        model = model.cuda()

    os.makedirs(SORTED_DIR, exist_ok=True)
    all_image_paths = sorted(glob.glob(os.path.join(UNSORTED_DIR, '*.jpg')))

    # === PHASE 0: Pre-extract features ===
    dataset = ImagePathDataset(all_image_paths, transform)
    loader = DataLoader(dataset, batch_size=64, shuffle=False)

    features = []
    paths = []
    with torch.no_grad():
        for imgs, batch_paths in loader:
            if USE_GPU:
                imgs = imgs.cuda()
            feats = model(imgs).cpu().numpy()
            feats = normalize(feats, axis=1)  # L2-normalize
            features.append(feats)
            paths.extend(batch_paths)

    features = np.vstack(features)  # [N, D]

    # === CLUSTERING ===
    seed_features = []
    seed_ids = []
    cluster_feature_bank = []
    assigned_indices = set()

    print("\n🔍 Phase 1: Discovering initial identities...")
    identity_counter = 1
    for i, (feat, path) in enumerate(zip(features, paths)):
        if len(seed_features) > 0:
            dists = euclidean_distances([feat], seed_features)[0]
            best_dist = dists.min()
            best_idx = dists.argmin()

            if best_dist <= SIMILARITY_THRESHOLD:
                identity_name = seed_ids[best_idx]
                cluster_feature_bank[best_idx].append(feat)
                os.makedirs(os.path.join(SORTED_DIR, identity_name), exist_ok=True)
                shutil.copy2(path, os.path.join(SORTED_DIR, identity_name, os.path.basename(path)))
                print(f"✅ Assigned {os.path.basename(path)} → {identity_name} (dist={best_dist:.3f})")
            else:
                identity_name = f"{identity_counter:04d}"
                identity_counter += 1
                seed_features.append(feat)
                seed_ids.append(identity_name)
                cluster_feature_bank.append([feat])
                os.makedirs(os.path.join(SORTED_DIR, identity_name), exist_ok=True)
                shutil.copy2(path, os.path.join(SORTED_DIR, identity_name, os.path.basename(path)))
                print(f"🆕 Created new ID {identity_name} for {os.path.basename(path)} (dist={best_dist:.3f})")
        else:
            identity_name = f"{identity_counter:04d}"
            identity_counter += 1
            seed_features.append(feat)
            seed_ids.append(identity_name)
            cluster_feature_bank.append([feat])
            os.makedirs(os.path.join(SORTED_DIR, identity_name), exist_ok=True)
            shutil.copy2(path, os.path.join(SORTED_DIR, identity_name, os.path.basename(path)))
            print(f"🆕 Created first ID {identity_name} for {os.path.basename(path)}")

        assigned_indices.add(i)

    print("\n🔁 Phase 2: Assigning remaining images...")
    for i, (feat, path) in enumerate(zip(features, paths)):
        if i in assigned_indices:
            continue

        best_sim = -1e9
        best_idx = -1
        for j, feats in enumerate(cluster_feature_bank):
            cluster_center = np.mean(feats, axis=0, keepdims=True)
            dist = euclidean_distances([feat], cluster_center)[0][0]
            sim = -dist
            if sim > best_sim:
                best_sim = sim
                best_idx = j

        if best_idx == -1 or not seed_ids:
            identity_name = f"{identity_counter:04d}"
            identity_counter += 1
            os.makedirs(os.path.join(SORTED_DIR, identity_name), exist_ok=True)
            shutil.copy2(path, os.path.join(SORTED_DIR, identity_name, os.path.basename(path)))
            seed_ids.append(identity_name)
            seed_features.append(feat)
            cluster_feature_bank.append([feat])
            assigned_indices.add(i)
            print(f"🆕 Fallback new ID {identity_name} for {os.path.basename(path)} (no valid match)")
        else:
            assigned_id = seed_ids[best_idx]
            os.makedirs(os.path.join(SORTED_DIR, assigned_id), exist_ok=True)
            shutil.copy2(path, os.path.join(SORTED_DIR, assigned_id, os.path.basename(path)))
            cluster_feature_bank[best_idx].append(feat)
            assigned_indices.add(i)
            print(f"✅ Assigned {os.path.basename(path)} → {assigned_id} (sim={-best_sim:.3f})")

    print("\n🎉 Clustering complete.")

    print("\n🧹 Phase 3: Iteratively merging loner clusters or moving them to 'unknown'...")
    MAX_LONER_DISTANCE = 0.75
    unknown_dir = os.path.join(SORTED_DIR, 'unknown')
    os.makedirs(unknown_dir, exist_ok=True)

    while True:
        loner_dirs = []
        for idx, feats in enumerate(cluster_feature_bank):
            id_path = os.path.join(SORTED_DIR, seed_ids[idx])
            if not os.path.exists(id_path):
                continue
            files = [f for f in os.listdir(id_path) if not f.startswith('.')]
            if len(files) == 1:
                loner_dirs.append((idx, files[0]))

        if not loner_dirs:
            print("✅ No more loners found.")
            break

        moved_any = False
        for idx, filename in loner_dirs:
            source_dir = os.path.join(SORTED_DIR, seed_ids[idx])
            source_path = os.path.join(source_dir, filename)

            if not os.path.exists(source_path):
                print(f"⚠️ Skipping missing file: {source_path}")
                continue

            source_feat = cluster_feature_bank[idx][0]
            best_idx = -1
            best_dist = float('inf')

            for j, feats in enumerate(cluster_feature_bank):
                if j == idx or len(feats) == 0:
                    continue
                cluster_center = np.mean(feats, axis=0, keepdims=True)
                dist = euclidean_distances([source_feat], cluster_center)[0][0]
                if dist < best_dist:
                    best_dist = dist
                    best_idx = j

            if best_idx != -1 and best_dist <= MAX_LONER_DISTANCE:
                # Merge
                target_dir = os.path.join(SORTED_DIR, seed_ids[best_idx])
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(source_path, os.path.join(target_dir, filename))
                cluster_feature_bank[best_idx].append(source_feat)
                shutil.rmtree(source_dir, ignore_errors=True)
                cluster_feature_bank[idx] = []
                moved_any = True
                print(f"🔁 Merged loner {filename} → {seed_ids[best_idx]} (dist={best_dist:.3f})")
            else:
                # Too far → move directly to 'unknown'
                try:
                    shutil.move(source_path, os.path.join(unknown_dir, filename))
                    shutil.rmtree(source_dir, ignore_errors=True)
                    cluster_feature_bank[idx] = []
                    print(f"📥 Skipped merging {filename} → unknown (dist={best_dist:.3f})")
                except Exception as e:
                    print(f"⚠️ Failed to move loner {filename} to unknown: {e}")

        if not moved_any:
            print("⚠️ No more loner merges possible.")
            break


    print("\n📦 Phase 4: Saving unassigned images to 'unknown'...")

    original_paths = set(os.path.abspath(p) for p in glob.glob(os.path.join(UNSORTED_DIR, '*.jpg')))

    clustered_paths = set()
    for root, dirs, files in os.walk(SORTED_DIR):
        for file in files:
            if file.lower().endswith('.jpg'):
                clustered_paths.add(os.path.abspath(os.path.join(root, file)))

    missing_paths = []
    for orig_path in original_paths:
        if not any(os.path.basename(orig_path) == os.path.basename(clustered_path) for clustered_path in clustered_paths):
            missing_paths.append(orig_path)

    unknown_dir = os.path.join(SORTED_DIR, 'unknown')
    os.makedirs(unknown_dir, exist_ok=True)
    for missing in missing_paths:
        try:
            shutil.copy2(missing, os.path.join(unknown_dir, os.path.basename(missing)))
        except Exception as e:
            print(f"⚠️ Could not copy {missing} to unknown: {e}")


    print(f"\n📊 Summary:")
    print(f"Original images found: {len(original_paths)}")
    print(f"Images placed in clusters: {len(clustered_paths)}")
    print(f"Images copied to unknown: {len(missing_paths)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Greedy clustering-based ReID inference with Swin.")
    parser.add_argument('--unsorted_dir', type=str, required=True, help="Directory of input unsorted images")
    parser.add_argument('--sorted_dir', type=str, required=True, help="Directory to save clustered images")
    parser.add_argument('--train_dir', type=str, required=True, help="Directory used to determine number of classes for model")
    parser.add_argument('--model_path', type=str, required=True, help="Path to .pth model checkpoint")
    parser.add_argument('--similarity_threshold', type=float, default=0.65, help="Similarity threshold (default: 0.65)")
    parser.add_argument('--img_size', type=int, nargs=2, default=[224, 224], help="Image resize dimensions (default: 224 224)")
    parser.add_argument('--no_cuda', action='store_true', help="Disable CUDA even if available")
    args = parser.parse_args()

    main(args)

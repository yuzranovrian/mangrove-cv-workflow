import os
import shutil
import random

# ==========================================
# KONFIGURASI PATH & RATIO SPLIT
# ==========================================
# Folder tempat kamu meletakkan hasil uncompress/export dari CVAT
SOURCE_DIR = r"dataset/raw_cvat_NamaMitra"

# Folder tujuan struktur YOLO (gunakan nama mitra/program agar tidak tertukar)
OUTPUT_DIR = r"dataset/yolo_NamaMitra"

# Rasio pembagian data training (0.8 = 80% train, 20% validation)
TRAIN_RATIO = 0.8
SEED = 42  # Agar acaknya konsisten jika dijalankan ulang


def setup_yolo_folders(base_dir):
    """Membuat struktur folder standar YOLO."""
    folders = [
        os.path.join(base_dir, "images", "train"),
        os.path.join(base_dir, "images", "val"),
        os.path.join(base_dir, "labels", "train"),
        os.path.join(base_dir, "labels", "val"),
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def split_dataset():
    random.seed(SEED)
    setup_yolo_folders(OUTPUT_DIR)

    images_dir = os.path.join(SOURCE_DIR, "images")
    labels_dir = os.path.join(SOURCE_DIR, "labels")

    if not os.path.exists(images_dir):
        print(
            f"Error: Folder '{images_dir}' tidak ditemukan! Pastikan hasil export CVAT sudah diekstrak ke '{SOURCE_DIR}'.")
        return

    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print(f"Error: Tidak ada gambar ditemukan di '{images_dir}'.")
        return

    random.shuffle(image_files)

    num_train = int(len(image_files) * TRAIN_RATIO)
    train_images = image_files[:num_train]
    val_images = image_files[num_train:]

    print(f"Total data ditemukan: {len(image_files)}")
    print(f"Membagi data -> Train: {len(train_images)} | Val: {len(val_images)}")

    def copy_files(file_list, split_type):
        for img_name in file_list:
            base_name = os.path.splitext(img_name)[0]
            label_name = f"{base_name}.txt"

            src_img = os.path.join(images_dir, img_name)
            src_lbl = os.path.join(labels_dir, label_name)

            dst_img = os.path.join(OUTPUT_DIR, "images", split_type, img_name)
            dst_lbl = os.path.join(OUTPUT_DIR, "labels", split_type, label_name)

            # Copy gambar
            if os.path.exists(src_img):
                shutil.copy(src_img, dst_img)

            # Copy label .txt jika ada (jika background murni, label tidak ada)
            if os.path.exists(src_lbl):
                shutil.copy(src_lbl, dst_lbl)

    print("Memulai proses penyalinan file...")
    copy_files(train_images, "train")
    copy_files(val_images, "val")
    print(f"Selesai! Dataset YOLO sudah tersusun di '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    split_dataset()
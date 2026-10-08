import os
import subprocess
import sys

# Auto-install ultralytics jika belum terpasang
try:
    from ultralytics import YOLO
except ImportError:
    print("Pustaka 'ultralytics' belum ditemukan. Memulai instalasi otomatis...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
    from ultralytics import YOLO

# ==========================================
# KONFIGURASI TRAINING & DATASET
# ==========================================
# Folder dataset hasil dari Script 2
DATASET_DIR = "dataset/yolo_BenihBaik"
DATA_YAML_PATH = os.path.join(DATASET_DIR, "data.yaml")

MODEL_VARIANT = "yolov8m.pt"  # Pilihan base model: yolov8n.pt, yolov8s.pt, yolov8m.pt
EPOCHS = 100  # Jumlah iterasi training (default: 100)
IMAGE_SIZE = 640  # Resolusi input gambar (640x640)
BATCH_SIZE = 16  # Ukuran batch (sesuaikan dengan RAM/GPU, misal 8 atau 16)

# Output folder untuk menyimpan file bobot (weights)
PROJECT_NAME = "runs/detect"
EXP_NAME = "mangrove_counter_v1"


def create_data_yaml():
    """Membuat file data.yaml secara otomatis di dalam folder dataset."""
    abs_dataset_path = os.path.abspath(DATASET_DIR)

    # Gunakan forward slash untuk kompatibilitas path di YAML
    abs_dataset_path_formatted = abs_dataset_path.replace("\\", "/")

    yaml_content = f"""path: {abs_dataset_path_formatted}
train: images/train
val: images/val

names:
  0: mangrove
"""
    with open(DATA_YAML_PATH, "w") as f:
        f.write(yaml_content)
    print(f"File konfigurasi '{DATA_YAML_PATH}' berhasil disiapkan.")


def train_model():
    # 1. Pastikan file data.yaml tersedia
    create_data_yaml()

    # 2. Load base model YOLO
    print(f"Memuat base model: {MODEL_VARIANT}...")
    model = YOLO(MODEL_VARIANT)

    # 3. Jalankan proses training
    print("Memulai proses training model YOLO...")
    model.train(
        data=DATA_YAML_PATH,
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        project=PROJECT_NAME,
        name=EXP_NAME,
        device="cpu",  # Ubah ke '0' atau 'cuda' jika komputer menggunakan GPU Nvidia / M-Series Apple
        save=True,
        plots=True
    )

    print("\n==========================================")
    print("TRAINING SELESAI!")
    print(f"File bobot terbaik (best.pt) tersimpan di: {PROJECT_NAME}/{EXP_NAME}/weights/best.pt")
    print("==========================================")


if __name__ == "__main__":
    train_model()
import os
import subprocess
import sys

# Auto-install SAHI & Ultralytics jika belum terpasang
try:
    from sahi import AutoDetectionModel
    from sahi.predict import get_sliced_prediction
except ImportError:
    print("Pustaka 'sahi' belum ditemukan. Memulai instalasi otomatis...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sahi", "ultralytics"])
    from sahi import AutoDetectionModel
    from sahi.predict import get_sliced_prediction

# ==========================================
# KONFIGURASI PATH & PARAMETER SAHI
# ==========================================
# File GeoTIFF peta udara yang ingin dideteksi
GEOTIFF_PATH = r"dataset/raw/BenihBaik.tif"

# Path file bobot (weights) terbaik hasil Script 3
MODEL_PATH = r"runs/detect/mangrove_BenihBaik_v1/weights/best.pt"

# Folder output tempat menyimpan gambar hasil deteksi
OUTPUT_DIR = r"runs/detect/webodm_sahi_BenihBaik/"

CONF_THRESHOLD = 0.35  # Batas minimum tingkat keyakinan model (35%)
SLICE_SIZE = 640       # Ukuran window slicing SAHI
OVERLAP_RATIO = 0.25   # Overlap 25% agar pohon di perbatasan irisan tidak terlewat

os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_sahi_counter():
    if not os.path.exists(GEOTIFF_PATH):
        print(f"Error: File GeoTIFF '{GEOTIFF_PATH}' tidak ditemukan!")
        return

    if not os.path.exists(MODEL_PATH):
        print(f"Error: File model '{MODEL_PATH}' tidak ditemukan. Jalankan Script 3 terlebih dahulu!")
        return

    print("Memuat model YOLO ke dalam SAHI Engine...")
    detection_model = AutoDetectionModel.from_pretrained(
        model_type="yolov8",
        model_path=MODEL_PATH,
        confidence_threshold=CONF_THRESHOLD,
        device="cpu",  # Ubah ke 'cuda' atau '0' jika menggunakan GPU
    )

    print(f"Menjalankan proses deteksi pada GeoTIFF: {GEOTIFF_PATH}")
    result = get_sliced_prediction(
        image=GEOTIFF_PATH,
        detection_model=detection_model,
        slice_height=SLICE_SIZE,
        slice_width=SLICE_SIZE,
        overlap_height_ratio=OVERLAP_RATIO,
        overlap_width_ratio=OVERLAP_RATIO,
        postprocess_type="NMS",
        postprocess_match_threshold=0.5
    )

    # Export gambar hasil visualisasi deteksi
    result.export_visuals(
        export_dir=OUTPUT_DIR,
        rect_th=1,          # Ketebalan garis bounding box (1px)
        text_size=0.3,       # Ukuran teks
        hide_labels=True,   # Sembunyikan label teks agar tidak menutupi peta
        hide_conf=True      # Sembunyikan persentase confidence
    )

    total_mangroves = len(result.object_prediction_list)
    print("\n==========================================")
    print(f"HASIL DETEKSI OTOMATIS (SAHI):")
    print(f"Total Mangrove Terdeteksi: {total_mangroves} individu")
    print(f"Hasil gambar visualisasi disimpan di: {OUTPUT_DIR}")
    print("==========================================")

if __name__ == "__main__":
    run_sahi_counter()
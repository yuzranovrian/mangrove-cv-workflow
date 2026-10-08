import os
import subprocess
import sys

# Auto-install SAHI & Shapely/GeoPandas jika belum terpasang
try:
    from sahi import AutoDetectionModel
    from sahi.predict import get_sliced_prediction
except ImportError:
    print("Pustaka yang dibutuhkan belum ada. Memulai instalasi otomatis...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sahi", "ultralytics", "shapely", "geopandas"])
    from sahi import AutoDetectionModel
    from sahi.predict import get_sliced_prediction

# ==========================================
# KONFIGURASI PATH EXPORT GIS
# ==========================================
# File GeoTIFF peta udara yang dideteksi
GEOTIFF_PATH = r"dataset/raw/NamaMitra.tif"

# Path file bobot (weights) terbaik hasil Script 3
MODEL_PATH = r"runs/detect/mangrove_NamaMitra_v1/weights/best.pt"

# Folder output untuk menyimpan file GeoJSON
OUTPUT_GIS_DIR = r"runs/detect/webodm_gis_export_NamaMitra/"

CONF_THRESHOLD = 0.35  # Batas minimum tingkat keyakinan model (35%)
SLICE_SIZE = 640
OVERLAP_RATIO = 0.25

os.makedirs(OUTPUT_GIS_DIR, exist_ok=True)


def export_to_geojson():
    if not os.path.exists(GEOTIFF_PATH):
        print(f"Error: File GeoTIFF '{GEOTIFF_PATH}' tidak ditemukan!")
        return

    if not os.path.exists(MODEL_PATH):
        print(f"Error: File model '{MODEL_PATH}' tidak ditemukan. Jalankan Script 3 terlebih dahulu!")
        return

    print("Memuat model YOLO untuk ekspor format GIS...")
    detection_model = AutoDetectionModel.from_pretrained(
        model_type="yolov8",
        model_path=MODEL_PATH,
        confidence_threshold=CONF_THRESHOLD,
        device="cpu",  # Ubah ke 'cuda' atau '0' jika menggunakan GPU
    )

    print(f"Memproses koordinat spasial dari GeoTIFF: {GEOTIFF_PATH}")
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

    geojson_output_path = os.path.join(OUTPUT_GIS_DIR, "mangrove_detections_BenihBaik.json")

    # Ekspor hasil deteksi ke format GeoJSON
    result.export_as_json(file_path=geojson_output_path)

    print("\n==========================================")
    print("EKSPOR FILE VEKTOR SPASIAL BERHASIL!")
    print(f"Path File: {geojson_output_path}")
    print("Petunjuk: Silakan drag & drop file GeoJSON ini ke QGIS / ArcGIS Pro untuk QC & digitasi manual.")
    print("==========================================")


if __name__ == "__main__":
    export_to_geojson()
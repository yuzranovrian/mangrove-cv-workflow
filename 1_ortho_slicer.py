import subprocess
import sys

# Auto-install rasterio & opencv jika belum terpasang
try:
    import rasterio
    import cv2
except ImportError:
    print("Pustaka yang dibutuhkan belum ada. Memulai instalasi otomatis...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rasterio", "opencv-python"])
    import rasterio
    import cv2

import os
import numpy as np

# ==========================================
# KONFIGURASI PATH & PARAMETER
# ==========================================
INPUT_GEOTIFF = "C:\Users\NamaUser\Downloads\Nama File.tif"  # Ubah sesuai lokasi GeoTIFF
OUTPUT_DIR = "dataset/tiles_NamaMitra_640"  # Folder output hasil slicing, ganti "NamaMitra" ke nama mitra atau program
TILE_SIZE = 640  # Ukuran tile (640x640)
OVERLAP = 0.20  # Overlap 20% antar tile agar objek di pinggir tidak terpotong

os.makedirs(OUTPUT_DIR, exist_ok=True)


def slice_geotiff(input_path, output_dir, tile_size=640, overlap=0.20):
    print(f"Membuka file GeoTIFF: {input_path}")

    with rasterio.open(input_path) as src:
        # Membaca 3 band pertama (RGB)
        image = src.read([1, 2, 3])
        # Transpose dari (Band, Height, Width) ke (Height, Width, Band) standar OpenCV
        image = np.transpose(image, (1, 2, 0))

        # Konversi RGB ke BGR untuk OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    height, width, _ = image.shape
    print(f"Dimensi Gambar Asli: {width} x {height} piksel")

    step = int(tile_size * (1 - overlap))
    count = 0

    # Iterasi sliding window
    for y in range(0, height - tile_size + 1, step):
        for x in range(0, width - tile_size + 1, step):
            tile = image[y:y + tile_size, x:x + tile_size]

            # Filter tile kosong (hitam/transparan di luar area peta)
            if np.mean(tile) > 10:  # Hanya simpan tile yang berisi data gambar
                tile_filename = os.path.join(output_dir, f"tile_{y}_{x}.png")
                cv2.imwrite(tile_filename, tile)
                count += 1

    print(f"Selesai! Berhasil mengekspor {count} tile ke '{output_dir}'.")


if __name__ == "__main__":
    slice_geotiff(INPUT_GEOTIFF, OUTPUT_DIR, TILE_SIZE, OVERLAP)
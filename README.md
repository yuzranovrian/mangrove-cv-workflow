# Mangrove CV Workflow (YOLO + SAHI)

Workflow otomatisasi deteksi dan perhitungan populasi benih/pohon mangrove dari citra udara WebODM menggunakan YOLOv8/v11 dan SAHI Engine.

## 📋 Struktur Script
1. `1_ortho_slicer.py` : Pemotongan GeoTIFF raksasa menjadi tile 640x640 untuk bahan labeling di CVAT.
2. `2_split_val.py` : Pembagian dataset export CVAT menjadi struktur YOLO (`train` & `val`).
3. `3_yolo_trainer.py` : Pelatihan model YOLO untuk menghasilkan file bobot `best.pt`.
4. `4_mangrove_counter.py` : Deteksi dan perhitungan populasi otomatis menggunakan SAHI.
5. `5_gis_exporter.py` : Ekspor hasil deteksi ke format GeoJSON untuk integrasi QGIS/ArcGIS Pro.

## 🚀 Panduan Memulai
1. Clone repository ini:
   git clone <URL_REPOSITORY_GITHUB>

2. Install seluruh dependency:
   pip install -r requirements.txt

---
## ⚙️ Persiapan Environment & Tools

Sebelum menjalankan skrip Python, pastikan seluruh infrastruktur (Git, Docker, CVAT, WebODM) sudah terinstal dan terkonfigurasi dengan benar. 

Langkah-langkah instalasi lengkap dapat dilihat pada dokumen berikut:
👉 [Panduan Setup Environment & Tools](ENVIRONMENT_SETUP.md)
---

## 📖 Panduan Penggunaan Lengkap (Step-by-Step)

### Langkah 1: Slicing Citra Udara (1_ortho_slicer.py)
Memotong file GeoTIFF raksasa menjadi potongan gambar kecil (640x640 piksel) agar ringan di-upload ke CVAT.

1. Siapkan file GeoTIFF (misal: BenihBaik.tif) di dalam folder project.
2. Buka 1_ortho_slicer.py dan sesuaikan path-nya:
   - INPUT_GEOTIFF = r"dataset/raw/BenihBaik.tif"
   - OUTPUT_DIR = r"dataset/tiles_BenihBaik_640/"
3. Klik kanan 1_ortho_slicer.py -> pilih Run '1_ortho_slicer'.
4. Hasil pemotongan tersimpan di folder dataset/tiles_BenihBaik_640/.

---

### Langkah 2: Labeling Manual di CVAT (Proses Luar)
1. Buka platform CVAT (Computer Vision Annotation Tool).
2. Buat Task baru, upload seluruh gambar dari folder dataset/tiles_BenihBaik_640/.
3. Buat label mangrove, lalu lakukan annotasi/labeling pada benih atau pohon mangrove.
4. Setelah selesai, export dataset dengan format YOLO 1.1.
5. Ekstrak file zip hasil export CVAT tersebut ke folder dataset/raw_cvat_BenihBaik/.

---

### Langkah 3: Split Dataset Train & Val (2_split_val.py)
Membagi hasil anotasi CVAT menjadi folder train (80%) dan val (20%) standar YOLO.

1. Buka 2_split_val.py dan sesuaikan path folder:
   - SOURCE_DIR = r"dataset/raw_cvat_BenihBaik"
   - OUTPUT_DIR = r"dataset/yolo_BenihBaik"
2. Klik kanan 2_split_val.py -> pilih Run '2_split_val'.
3. Struktur dataset YOLO akan terbentuk di dataset/yolo_BenihBaik/.

---

### Langkah 4: Training Model YOLO (3_yolo_trainer.py)
Melatih model AI untuk mengenali pola mangrove dari dataset yang telah disiapkan.

1. Buka 3_yolo_trainer.py dan atur parameter training:
   - DATASET_DIR = "dataset/yolo_BenihBaik"
   - MODEL_VARIANT = "yolov8m.pt"
   - EPOCHS = 100
2. Klik kanan 3_yolo_trainer.py -> pilih Run '3_yolo_trainer'.
3. File bobot terbaik tersimpan di runs/detect/mangrove_BenihBaik_v1/weights/best.pt.

---

### Langkah 5: Deteksi & Hitung Populasi (4_mangrove_counter.py)
Menjalankan SAHI Engine pada GeoTIFF utuh untuk menghitung populasi mangrove secara otomatis.

1. Buka 4_mangrove_counter.py dan arahkan ke file model:
   - GEOTIFF_PATH = r"dataset/raw/BenihBaik.tif"
   - MODEL_PATH = r"runs/detect/mangrove_BenihBaik_v1/weights/best.pt"
   - OUTPUT_DIR = r"runs/detect/webodm_sahi_BenihBaik/"
2. Klik kanan 4_mangrove_counter.py -> pilih Run '4_mangrove_counter'.
3. Total populasi akan muncul di konsol, dan gambar visualisasi tersimpan di folder output.

---

### Langkah 6: Export ke Format GIS (5_gis_exporter.py)
Mengonversi hasil deteksi menjadi file vektor spasial GeoJSON untuk diolah di QGIS / ArcGIS Pro.

1. Buka 5_gis_exporter.py dan atur path-nya:
   - GEOTIFF_PATH = r"dataset/raw/BenihBaik.tif"
   - MODEL_PATH = r"runs/detect/mangrove_BenihBaik_v1/weights/best.pt"
   - OUTPUT_GIS_DIR = r"runs/detect/webodm_gis_export_BenihBaik/"
2. Klik kanan 5_gis_exporter.py -> pilih Run '5_gis_exporter'.
3. Drag & drop file mangrove_detections_BenihBaik.json dari folder output langsung ke QGIS atau ArcGIS Pro.
# Panduan Lengkap Setup Environment & Tools (Git, Docker, CVAT, WebODM, PyCharm)

Dokumen ini berisi panduan komprehensif instalasi dan konfigurasi seluruh infrastruktur perangkat lunak yang dibutuhkan untuk workflow Computer Vision & Mapping.

---

## 📋 Urutan Instalasi Ringkas
1. Git for Windows
2. PyCharm Community / Professional
3. Docker Desktop & WSL 2
4. WebODM (Instalasi di Drive D & Run Detached)
5. CVAT (Instalasi di Drive D & Host Jaringan LAN)

---

## 🛠️ Langkah 1: Instalasi Git for Windows

1. Unduh installer Git resmi di: `https://git-scm.com/download/win`
2. Jalankan file `.exe` yang telah diunduh.
3. Pada opsi instalasi, pilih **Use Git from the Windows Command Prompt** dan biarkan opsi default lainnya.
4. Selesaikan instalasi hingga tombol **Finish**.
5. Verifikasi instalasi melalui PowerShell atau Command Prompt:
   git --version

---

## 🐍 Langkah 2: Instalasi PyCharm IDE

1. Unduh installer PyCharm di: `https://www.jetbrains.com/pycharm/download/`
2. Jalankan installer dan centang opsi berikut saat proses setup:
   - Create Desktop Shortcut
   - Add "Open Folder as Project"
   - Add .py to association
3. Selesaikan instalasi lalu restart komputer jika diminta.

---

## 🐳 Langkah 3: Instalasi Docker Desktop & WSL 2

1. Buka PowerShell sebagai **Administrator**, lalu jalankan perintah berikut untuk mengaktifkan WSL 2:
   wsl --install
2. Restart komputer setelah proses setup WSL selesai.
3. Unduh Docker Desktop di: `https://www.docker.com/products/docker-desktop/`
4. Jalankan installer Docker Desktop, pastikan opsi **Use WSL 2 instead of Hyper-V** tercentang.
5. Selesaikan instalasi dan jalankan Docker Desktop.

---

## ⚙️ Cara Mengubah Alokasi RAM Docker via File Konfigurasi (.wslconfig)

Secara default, WSL 2 / Docker Desktop dapat mengambil hingga 50% - 80% RAM komputer. Untuk membatasi/mengatur alokasi RAM agar komputer tidak lag:

1. Buka File Explorer, lalu masuk ke folder User Windows:
   C:\Users\<NamaUser>\
2. Buat file baru bernama `.wslconfig` (pastikan ada titik di depan nama file).
3. Buka file `.wslconfig` menggunakan Notepad, lalu masukkan konfigurasi berikut (contoh membatasi RAM 16 GB dan Swap 4 GB):

```
[wsl2]
memory=16GB
processors=4
swap=4GB
localhostForwarding=true
```

4. Simpan file tersebut.
5. Buka PowerShell/Command Prompt dan restart WSL agar konfigurasi baru aktif:
   wsl --shutdown

---

## 🛸 Langkah 4: Instalasi WebODM di Drive D & Cara Run Detached

### A. Pindah Direktori & Clone ke Drive D
1. Buka **Git Bash**.
2. Berpindah dari drive C: ke drive D: menggunakan perintah `cd`:
   cd /d/
3. Buat folder baru (opsional) atau langsung jalankan perintah clone WebODM:
   git clone https://github.com/OpenDroneMap/WebODM.git --depth 1
4. Masuk ke dalam direktori folder WebODM yang baru dibuat:
   cd WebODM

### B. Menjalankan WebODM Tanpa Mengunci Terminal (Bisa Di-close)
1. Jalankan script WebODM dalam mode *detached* (background):
   ./webodm.sh start -d
2. Setelah proses pengunduhan container selesai dan muncul pesan sukses, kamu bisa **menutup terminal Git Bash** secara aman.
3. Buka peramban (browser) dan akses WebODM di:
   http://localhost:8000

*Catatan Navigasi Git Bash:*
- Cek lokasi direktori kamu saat ini: `pwd`
- Menghentikan WebODM di kemudian hari: `cd /d/WebODM` lalu `./webodm.sh stop`

---

## 🏷️ Langkah 5: Instalasi CVAT di Drive D & Konfigurasi Host LAN

Agar PC kamu berfungsi sebagai **server/host CVAT** sehingga tim di kantor dapat mengakses platform CVAT melalui IP komputer kamu:

### A. Clone CVAT ke Drive D
1. Buka **Git Bash**.
2. Masuk ke Drive D:
   ```
   cd /d/
   ```
3. Clone repository CVAT:

   ```
   git clone https://github.com/cvat-ai/cvat.git
   ```
4. Masuk ke direktori folder CVAT:
   ```
   cd cvat
   ```

### B. Cek IP Address Komputer Host (Windows)
1. Buka Command Prompt (CMD) atau PowerShell di Windows.
2. Ketik perintah berikut dan tekan Enter:
   ```
   ipconfig
   ```
3. Catat alamat **IPv4 Address** lokal kamu (contoh: `192.168.1.50`).

### C. Konfigurasi Environment Host CVAT & Menjalankan Container
1. Di Git Bash (masih di dalam folder `/d/cvat`), atur variabel lingkungan `CVAT_HOST` menggunakan IP komputer kamu:
   export CVAT_HOST=192.168.1.50
2. Jalankan container CVAT dalam mode *detached* (background):
   docker compose up -d
3. Buat akun Administrator (Superuser) CVAT:
   docker exec -it cvat_server python3 manage.py createsuperuser
   (Masukkan username, email, dan password sesuai petunjuk di layar).

### D. Cara Akses CVAT
- **Di Komputer Kamu (Host):**
  Dapat diakses via browser melalui `http://localhost:8080` atau `http://192.168.1.50:8080`
- **Di Komputer Tim Lain (Satu Jaringan Wi-Fi/LAN Kantor):**
  Anggota tim cukup membuka browser di perangkat mereka dan mengetik alamat IP host kamu:
  `http://192.168.1.50:8080`

*Catatan Penting Host LAN:*
- Pastikan opsi **Private Network** pada Windows Firewall diizinkan (*allow access*) untuk Docker Desktop saat ada pop-up konfirmasi.
- Jika IP komputer kamu berubah (*Dynamic IP*), kamu tinggal menjalankan ulang perintah `export CVAT_HOST=<IP_Baru>` dan `docker compose up -d`.
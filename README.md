
# ZenMode

ZenMode adalah skrip Python sederhana yang memblokir situs-situs distraksi seperti media sosial dengan memodifikasi file **hosts** pada sistem operasi Anda. Skrip ini cocok digunakan ketika Anda ingin fokus bekerja atau belajar tanpa gangguan.

---

## 🚀 Fitur

- Memblokir daftar situs distraksi secara otomatis
- Dukungan Windows, macOS, dan Linux
- Flush DNS otomatis agar perubahan hosts langsung aktif
- Dapat menghentikan blokir kapan saja
- Dijalankan melalui command line dengan argument

---

## 📌 Daftar Situs yang Diblokir

Secara default, ZenMode memblokir situs-situs berikut:

- Facebook  
- Twitter  
- YouTube  
- Instagram  
- TikTok  
- Reddit  
- Snapchat  
- LinkedIn  

Anda bisa menambah atau mengurangi situs pada daftar `WEBSITES_TO_BLOCK` di dalam file `zen2.0.py`.

---

## 🛠️ Cara Menggunakan

### 1. Jalankan Script dengan Hak Administrator

Karena ZenMode memodifikasi file **hosts**, skrip harus dijalankan sebagai **Administrator** (Windows) atau menggunakan **sudo** (macOS/Linux).

### 2. Menyalakan ZenMode

Format perintah:

```sh
python zen2.0.py start <durasi_dalam_menit>
```

Contoh:

```sh
python zen2.0.py start 30
```

ZenMode akan aktif selama 30 menit.

### 3. Mematikan ZenMode Secara Manual

Jika ingin menonaktifkan sebelum durasi berakhir:

```sh
python zen2.0.py stop
```

---

## ⚠️ Peringatan

- Pastikan Anda tahu apa yang Anda lakukan karena file **hosts** adalah file sistem yang penting.
- Jangan memodifikasi daftar situs atau file hosts jika tidak yakin.
- Jika terjadi error, script akan mencoba mengembalikan kondisi file hosts seperti semula.

---

## 📄 Lisensi

Proyek ini bebas digunakan dan dimodifikasi sesuai kebutuhan Anda.

---

## ✨ Kontribusi

Silakan modifikasi kode dan tambahkan fitur sesuai kebutuhan Anda. Jika ingin berbagi perbaikan atau fitur baru, jangan ragu untuk mengirimkan file atau patch.

---

Selamat fokus dan semoga produktivitas meningkat dengan ZenMode!

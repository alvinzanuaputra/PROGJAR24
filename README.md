# Identitas

| Nama | NRP | Kelas | Tahun |
|------|-----|-------|-------|
| Alvin Zanua Putra | 5025231064 | Pemrograman Jaringan D | 2024-2025 |

---

# TUGAS 1

## SOAL:

1. Jalankan socket_info.py di mesin-1 dan mesin-2, capturelah hasilnya, lakukan analysis menggunakan wireshark, capture hasilnya
2. Jalankan server.py di mesin-1 dan client.py di mesin-2, sesuaikan isi program, pastikan komunikasi dapat dilakukan, capturelah hasilnya, lakukan analysis menggunakan wireshark, capture hasilnya
3. Jalankan kembali soal nomor 2, namun kali ini rubahlah komunikasi agar berjalan di port 32444, kirimkan isi sebuah file, dan capturelahh hasilnya, lakukan analysis menggunakan wireshark, capture hasilnya
4. Jalankan client di mesin-2 dan mesin-3 dengan server berada di mesin-1, jalankan client secara bersamaan, apakah yang terjadi? capturelah hasilnya, lakukan analysis menggunakan wireshark, capture hasilnya

---

# TUGAS 2

## SOAL:

1. Buatlah sebuah program time server dengan ketentuan sebagai berikut:
   - Membuka port di port 45000 dengan transport TCP
   - Server harus dapat melayani request yang concurrent, gunakan contoh multithreading pada ini
   - Ketentuan request yang dilayani:
     - Diawali dengan string "TIME" dan diakhiri dengan karakter 13 dan karakter 10
     - Setiap request dapat diakhiri dengan string "QUIT" yang diakhiri dengan karakter 13 dan 10
   - Server akan merespon dengan jam dengan ketentuan:
     - Dalam bentuk string (UTF-8)
     - Diawali dengan "JAM<spasi><jam>"
     - <jam> berisikan info jam dalam format "hh:mm:ss" dan diakhiri dengan karakter 13 dan karakter 10

   **CATATAN:** Untuk mendapatkan waktu sekarang dapat menggunakan contoh berikut:
   ```python
   from datetime import datetime
   now = datetime.now()
   waktu = now.strftime("%d %m %Y %H:%M:%S")
   ```

2. Jalankan di lab environment:
   - Tuliskan dalam satu file PDF dengan nama TUGAS2.PDF:
     - Link menuju source code anda di github (masing-masing harus punya repository di github)
     - Capturelah hasil eksekusi program server anda
   - Semua poin, harus dilengkapi dengan deskripsi dan penjelasan minimum 50 kata

---

# TUGAS 3

## SOAL:

1. Pada file server protocol (https://github.com/rm77/progjar/tree/master/progjar4a), Tambahkan kemampuan:
   - Upload file
     - Content file yang diupload harus diencode dulu dengan format base64 
   - Hapus file

2. Update-lah spesifikasi protokol (PROTOKOL.txt) yang telah ada pada contoh dengan kemampuan yang baru ditambahkan tersebut, berikan penjelasan tambahan dalam satu paragraf

3. Buatlah client implementation dari operasi tambahan tersebut. Jalankan operasi client server untuk kemampuan tersebut, berikanlah screenshot seperlunya, dan penjelasan dalam paragraf

---

# TUGAS 4

## SOAL:

1. Dari hasil modifikasi program (https://github.com/rm77/progjar/tree/master/progjar4a) pada TUGAS 3

2. Rubahlah model pemrosesan concurrency yang ada, dari multithreading menjadi:
   - Multihreading menggunakan pool
   - Multiprocessing menggunakan pool

3. Modifikasilah program client untuk melakukan:
   - Download file
   - Upload file
   - List file

4. Lakukan stress test pada program server tersebut dengan cara membuat client agar melakukan proses pada nomor 3 secara concurrent dengan menggunakan multithreading pool dan multiprocessing pool

   **Kombinasi stress test:**
   - Operasi download, upload
   - Volume file 10 MB, 50 MB, 100 MB 
   - Jumlah client worker pool 1, 5, 50 
   - Jumlah server worker pool 1, 5, 50

   **Untuk setiap kombinasi tersebut catatlah:**
   - Waktu total per client melakukan proses upload/download (dalam seconds)
   - Throughput per client (dalam bytes per second, total bytes yang sukses diproses per second)
   - Jumlah worker client yang sukses dan gagal (jika sukses semua, maka gagal = 0)
   - Jumlah worker server yang sukses dan gagal (jika sukses semua, maka gagal = 0)

5. Hasil stress test, harus direkap ke sebuah tabel yang barisnya adalah total kombinasi dari nomor 4. Total baris kombinasi = 2x3x3x3 = 54 baris, dengan kolom:
   - Nomor
   - Operasi
   - Volume
   - Jumlah client worker pool
   - Jumlah server worker pool
   - Waktu total per client
   - Throughput per client
   - Jumlah worker client yang sukses dan gagal
   - Jumlah worker server yang sukses dan gagal
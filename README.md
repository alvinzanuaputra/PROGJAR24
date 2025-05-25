# Pemrograman Jaringan D - 2024

## Identitas
| Nama | NRP | Kelas | Tahun |
|------|-----|-------|-------|
| Alvin Zanua Putra | 5025231064 | Pemrograman Jaringan D | 2024-2025 |

## Daftar Tugas
- [Tugas 1](#tugas-1) - Socket Programming Dasar
- [Tugas 2](#tugas-2) - Time Server
- [Tugas 3](#tugas-3) - File Protocol Server
- [Tugas 4](#tugas-4) - Concurrent File Server

## Tugas 1
### Soal
1. Jalankan socket_info.py di mesin-1 dan mesin-2, capturelah hasilnya, lakukan analysis menggunakan wireshark
2. Jalankan server.py di mesin-1 dan client.py di mesin-2, sesuaikan isi program dan pastikan komunikasi dapat dilakukan
3. Jalankan kembali soal nomor 2 dengan komunikasi di port 32444 dan kirimkan isi sebuah file
4. Jalankan client di mesin-2 dan mesin-3 dengan server di mesin-1 secara bersamaan

## Tugas 2
### Soal
Membuat time server dengan spesifikasi:
- Port 45000 dengan transport TCP
- Mendukung request concurrent dengan multithreading
- Format request: "TIME" diakhiri CR+LF
- Format quit: "QUIT" diakhiri CR+LF
- Format response: "JAM hh:mm:ss" diakhiri CR+LF

### Contoh Kode Waktu
```python
from datetime import datetime
now = datetime.now()
waktu = now.strftime("%d %m %Y %H:%M:%S")
```

## Tugas 3
### Soal
Menambahkan fitur pada file server protocol:
1. Upload file (dengan encoding base64)
2. Hapus file
3. Update spesifikasi protokol
4. Implementasi client untuk fitur baru

## Tugas 4
### Soal
Pengembangan file server dengan concurrent processing:

1. Modifikasi server untuk mendukung:
   - Multithreading pool
   - Multiprocessing pool

2. Modifikasi client untuk operasi:
   - Download file
   - Upload file
   - List file

3. Stress testing dengan kombinasi:
   - Operasi: download, upload
   - Volume: 10MB, 50MB, 100MB
   - Client worker pool: 1, 5, 50
   - Server worker pool: 1, 5, 50

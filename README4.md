Nama	: Alvin Zanua Putra
NRP		: 5025231064
Kelas	: Pemrograman Jaringan – D

# TUGAS 4

## SOAL :

1. Dari hasil modifikasi program (https://github.com/rm77/progjar/tree/master/progjar4a) pada TUGAS 3
2. Rubahlah model pemrosesan concurrency yang ada, dari multithreading menjadi
   a. Multihreading menggunakan pool
   b. Multiprocessing menggunakan pool
3. Modifikasilah program client untuk melakukan
   a. Download file
   b. Upload file
   c. List file
4. Lakukan stress test pada program server tersebut dengan cara membuat client agar melakukan proses pada nomor 3 secara concurrent dengan menggunakan multithreading pool dan multiprocessing pool
   Kombinasi stress test:
   - Operasi download, upload
   - Volume file 10 MB, 50 MB, 100 MB 
   - Jumlah client worker pool 1, 5, 50 
   - Jumlah server worker pool 1, 5, 50
   Untuk setiap kombinasi tersebut catatlah:
   A. Waktu total per client melakukan proses upload/download (dalam seconds)
   B. Throughput per client (dalam bytes per second, total bytes yang sukses diproses per second)
   C. Jumlah worker client yang sukses dan gagal (jika sukses semua, maka gagal = 0)
   D. Jumlah worker server yang sukses dan gagal (jika sukses semua, maka gagal = 0)
5. Hasil stress test, harus direkap ke sebuah tabel yang barisnya adalah total kombinasi dari nomor 4. Total baris kombinasi = 2x3x3x3 = 54 baris, dengan kolom:
   a. Nomor
   b. Operasi
   c. Volume
   d. Jumlah client worker pool
   e. Jumlah server worker pool
   f. Waktu total per client
   g. Throughput per client
   h. Jumlah worker client yang sukses dan gagal
   i. Jumlah worker server yang sukses dan gagal

---

## JAWABAN
# File Server Stress Test Suite

Implementasi lengkap file server dengan dukungan thread pool dan multiprocessing pool, serta comprehensive stress testing sesuai dengan requirements yang diminta.

## Struktur File

- `file_interface.py` - Enhanced file interface dengan dukungan UPLOAD dan DELETE
- `file_protocol.py` - Protocol handler (tidak berubah)
- `file_server.py` - Enhanced server dengan pool support
- `thread_pool.py` - Thread pool server implementation
- `file_client_cli.py` - Client CLI (existing)
- `file_client_stress_test.py` - Comprehensive stress test implementation
- `run_tests.py` - Test runner script untuk menjalankan semua kombinasi test

## Prerequisites

Install dependencies yang diperlukan:

```bash
pip install pandas
```

## Cara Menjalankan :

### 1. Menjalankan Server

#### Server dengan Thread Pool:
```bash
# Threading pool dengan 5 workers
python file_server.py --workers 5

# Multiprocessing pool dengan 10 workers  
python file_server.py --workers 10 --multiprocessing

# Custom port
python file_server.py --port 9999 --workers 5
```

#### Server dengan Thread Pool (alternatif):
```bash
# Threading pool
python thread_pool.py --workers 5

# Multiprocessing pool
python thread_pool.py --workers 5 --multiprocessing
```

### 2. Menjalankan Stress Test

#### Comprehensive Test (Semua 81 kombinasi):
```bash
# Jalankan semua kombinasi test
python run_tests.py --mode comprehensive

# Dengan client multiprocessing
python run_tests.py --mode comprehensive --client-multiprocessing
```

#### Single Configuration Test:
```bash
# Test dengan konfigurasi tertentu
python run_tests.py --mode single --server-workers 5 --server-multiprocessing

# Manual stress test
python file_client_stress_test.py --server-workers 1 5 50 --output results.csv
```

### 3. Manual Testing

#### Test individual operations:
```bash
# Test basic functionality
python file_client_cli.py
```

## Kombinasi Stress Test

Sesuai requirements, sistem akan menjalankan test dengan kombinasi:

### Parameter Test:
- **Operasi**: Upload, Download (2 operasi)
- **Volume file**: 10 MB, 50 MB, 100 MB (3 ukuran)
- **Client worker pool**: 1, 5, 50 (3 konfigurasi)
- **Server worker pool**: 1, 5, 50 (3 konfigurasi)

**Total kombinasi**: 2 × 3 × 3 × 3 = **81 test cases**

### Metrics yang Dicatat:

Untuk setiap kombinasi test, sistem akan mencatat:

1. **Nomor** - Urutan test (1-81)
2. **Operasi** - Upload/Download
3. **Volume** - Ukuran file dalam MB
4. **Jumlah client worker pool** - Jumlah client workers
5. **Jumlah server worker pool** - Jumlah server workers
6. **Waktu total per client** - Rata-rata waktu per client (seconds)
7. **Throughput per client** - Rata-rata throughput (bytes/second)
8. **Client worker sukses/gagal** - Statistik keberhasilan client
9. **Server worker sukses/gagal** - Statistik keberhasilan server

## Output

### CSV Report
Hasil test akan disimpan dalam file CSV dengan format:
```
Nomor,Operasi,Volume (MB),Jumlah Client Worker Pool,Jumlah Server Worker Pool,Waktu Total per Client (s),Throughput per Client (bytes/s),Client Worker Sukses,Client Worker Gagal,Server Worker Sukses,Server Worker Gagal
1,upload,10,1,1,2.5678,4194304.56,1,0,1,0
2,upload,10,1,5,2.1234,4857830.12,1,0,5,0
...
```

### Console Output
Selama test berjalan, akan ditampilkan progress real-time:
```
Starting comprehensive stress test...
Total combinations: 81
Operations: ['upload', 'download']
Volumes: [10, 50, 100] MB
Client workers: [1, 5, 50]
Server workers: [1, 5, 50]
=====================================
Test 1/81: upload 10MB (C:1, S:1)
Test 2/81: upload 10MB (C:1, S:5)
...
```

## Fitur-Fitur

### Server Features:
- ✅ Multithreading dengan pool
- ✅ Multiprocessing dengan pool  
- ✅ Configurable worker count
- ✅ Connection statistics
- ✅ Graceful shutdown
- ✅ Error handling dan logging

### Client Features:
- ✅ Upload file support
- ✅ Download file support
- ✅ List files support
- ✅ Concurrent operations
- ✅ Thread dan process pool support
- ✅ Performance metrics
- ✅ Error tracking

### Stress Test Features:
- ✅ 81 kombinasi test lengkap
- ✅ Automatic file generation
- ✅ Real-time progress monitoring
- ✅ Comprehensive statistics
- ✅ CSV export
- ✅ Error handling
- ✅ Timeout protection

## Troubleshooting

### Common Issues:

1. **"Address already in use"**
   ```bash
   # Ganti port
   python file_server.py --port 9999
   ```

2. **"Permission denied" saat membuat file**
   ```bash
   # Pastikan directory files/ ada dan writable
   mkdir files
   chmod 755 files
   ```

3. **Memory error dengan file besar**
   ```bash
   # Kurangi jumlah concurrent workers
   python run_tests.py --mode single --server-workers 1
   ```

4. **Timeout errors**
   - Increase timeout values dalam stress test
   - Reduce file sizes untuk testing
   - Check network connectivity

### Monitoring:

Check log files untuk debugging:
```bash
tail -f server_8889.log
```

## Advanced Usage

### Custom Test Scenarios:

Untuk membuat test scenario custom, modify file `file_client_stress_test.py`:

```python
# Custom volume sizes
volumes = [1, 5, 10]  # MB

# Custom worker counts  
client_worker_counts = [1, 2, 4]
server_worker_counts = [1, 3, 5]

# Custom operations
operations = ['upload', 'download', 'list']
```

### Performance Tuning:

1. **Server optimization**:
   - Increase worker count untuk high concurrency
   - Use multiprocessing untuk CPU-intensive tasks
   - Adjust socket buffer sizes

2. **Client optimization**:
   - Use appropriate pool size
   - Implement connection pooling
   - Add retry mechanisms

3. **System optimization**:
   - Increase file descriptor limits
   - Optimize network buffers
   - Monitor CPU dan memory usage

## Results Analysis

Setelah test selesai, analisis hasil dengan:

1. **Throughput Analysis**: Bandingkan throughput across different configurations
2. **Scalability Analysis**: Lihat bagaimana performance scale dengan worker count
3. **Error Analysis**: Identifikasi patterns dalam failed requests
4. **Resource Usage**: Monitor CPU dan memory usage selama test

File CSV hasil test dapat dianalisis lebih lanjut dengan tools seperti Excel, Pandas, atau visualization tools lainnya.
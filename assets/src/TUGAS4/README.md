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


### Format Hasil Stress Test
Hasil akan disimpan dalam file CSV dengan kolom:
1. Nomor
2. Operasi
3. Volume
4. Jumlah client worker pool
5. Jumlah server worker pool
6. Waktu total per client
7. Throughput per client
8. Jumlah worker client yang sukses dan gagal
9. Jumlah worker server yang sukses dan gagal

Total kombinasi test: 2 x 3 x 3 x 3 = 54 baris

----

# INI ADALAH TESTING MANUAL SATU PER-SATU

**CATATAN SPLIT TERMINAL 2 KALI**

## MODE MULTI THREADING
  
```bash
# 1 worker
python3 file_server.py --mode thread --workers 1
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv

python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
```

```bash
# 5 worker
python3 file_server.py --mode thread --workers 5
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv

python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
```

```bash
# 50 worker
python3 file_server.py --mode thread --workers 50
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv

python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
```

## MODE MULTIPROCESS
  
```bash
# 1 worker
python3 file_server.py --mode process --workers 1
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv

python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 1 --output files.csv
```

```bash
# 5 worker
python3 file_server.py --mode process --workers 5
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv

python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 5 --output files.csv
```

```bash
# 50 worker
python3 file_server.py --mode process --workers 50
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode upload --server 172.16.16.101 --port 5666 --file files/100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv

python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 10MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 50MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
python3 file_client_cli_test.py --mode download --server 172.16.16.101 --port 5666 --file 100MB-TESTFILE.ORG.pdf --pool_mode thread --pool_size 50 --output files.csv
```

## Stress Semua testing

### Bagian Multithreading 

```bash
# Mode Thread (54 kombinasi pertama)
python3 file_client_cli_test.py --mode stress_all --server 172.16.16.101 --port 5666 \
    --pool_mode thread --output laporan_thread.csv
```

### Bagian Multiprocess

```bash
# Mode Process (54 kombinasi kedua)
python3 file_client_cli_test.py --mode stress_all --server 172.16.16.101 --port 5666 \
    --pool_mode process --output laporan_process.csv
```


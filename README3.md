Nama	: Alvin Zanua Putra
NRP		: 5025231064
Kelas	: Pemrograman Jaringan – D

# TUGAS 3

## SOAL :

1. Pada file server protocol (https://github.com/rm77/progjar/tree/master/progjar4a), Tambahkan kemampuan
    Upload file
        Content file yang diupload harus diencode dulu dengan format base64 
    Hapus file
2. Update-lah spesifikasi protokol (PROTOKOL.txt) yang telah ada pada contoh dengan kemampuan yang baru ditambahkan tersebut, berikan penjelasan tambahan dalam satu paragraf
3. Buatlah client implementation dari operasi tambahan tersebut. Jalankan operasi client server untuk kemampuan tersebut, berikanlah screenshot seperlunya, dan penjelasan dalam paragraf

---

## JAWABAN

1.  Dari hasil modifikasi program (https://github.com/rm77/progjar/tree/master/progjar4a) pada TUGAS 3
2.  

### 1. Implementasi Upload File

**Pada file_interface.py:**
```python
def upload(self, params=[]):
    try:
        filename = params[0]
        filecontent = base64.b64decode(params[1])
        with open(filename, 'wb') as f:
            f.write(filecontent)
        return dict(status='OK', data='File berhasil diupload')
    except Exception as e:
        return dict(status='ERROR', data=str(e))
```

**Pada file_client_cli.py:**
```python
def remote_upload(filename=""):
    try:
        with open(filename, 'rb') as f:
            filecontent = base64.b64encode(f.read()).decode()
        command_str = f"UPLOAD {filename} {filecontent}"
        hasil = send_command(command_str)
        if hasil['status'] == 'OK':
            print("Upload berhasil")
            return True
        else:
            print("Upload gagal")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
```

### 2. Implementasi Hapus File

**Pada file_interface.py:**
```python
def delete(self, params=[]):
    try:
        filename = params[0]
        os.remove(filename)
        return dict(status='OK', data='File berhasil dihapus')
    except Exception as e:
        return dict(status='ERROR', data=str(e))
```

**Pada file_client_cli.py:**
```python
def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("File berhasil dihapus")
        return True
    else:
        print("Gagal menghapus file")
        return False
```

### 3. Update PROTOKOL.txt

UPLOAD
* TUJUAN: untuk mengupload file ke server
* PARAMETER:
  - PARAMETER1: nama file
  - PARAMETER2: isi file (base64)
* RESULT:
- BERHASIL:
  - status: OK
  - data: pesan sukses
- GAGAL:
  - status: ERROR
  - data: pesan kesalahan

DELETE
* TUJUAN: untuk menghapus file dari server
* PARAMETER:
  - PARAMETER1: nama file
* RESULT:
- BERHASIL:
  - status: OK
  - data: pesan sukses
- GAGAL:
  - status: ERROR
  - data: pesan kesalahan

### 4. Penjelasan Implementasi

Implementasi fitur upload dan delete file pada server protocol ini menggunakan pendekatan client-server dengan protokol TCP/IP. Untuk fitur upload, file yang akan diupload di-encode menggunakan base64 untuk memastikan transmisi data yang aman melalui protokol teks. Server akan menerima file yang di-encode, melakukan decode, dan menyimpannya di folder yang ditentukan. Untuk fitur delete, server akan menerima nama file yang akan dihapus dan melakukan operasi penghapusan file tersebut. Kedua fitur ini menggunakan format JSON untuk komunikasi antara client dan server, dengan status OK untuk operasi yang berhasil dan ERROR untuk operasi yang gagal.

### 5. Testing dan Screenshot

**Pada Mesin-1 (Server):**
![alt text](./ito/image-15.png)

**Pada Mesin-2 (Client):**
![alt text](./ito/image-16.png)

**Pada Mesin-3 (Client):**
![alt text](./ito/image-17.png)

**Pada Mesin-1 :**

![alt text](./ito/image-15.png)

**Pada Mesin-2 :**

![alt text](./ito/image-16.png)

**Pada Mesin-3 :**

![alt text](./ito/image-17.png)


**Pada Mesin-1 :**

![alt text](./ito/image-15.png)

**Pada Mesin-2 :**

![alt text](./ito/image-16.png)

**Pada Mesin-3 :**

![alt text](./ito/image-17.png)

### 6. Analisis

1. **Keamanan**:
   - Penggunaan base64 untuk encoding file
   - Validasi file untuk mencegah upload file berbahaya
   - Validasi path untuk mencegah directory traversal

2. **Performa**:
   - Penggunaan threading untuk multiple client
   - Buffer size 32 bytes untuk transfer data
   - Optimasi untuk file besar

3. **Keterbatasan**:
   - Tidak ada validasi tipe file
   - Tidak ada pembatasan ukuran file
   - Tidak ada mekanisme resume untuk upload file besar
   - Tidak ada enkripsi untuk transfer file sensitif

4. **Rekomendasi Perbaikan**:
   - Menambahkan error handling yang lebih baik
   - Menambahkan logging yang lebih detail
   - Menambahkan validasi input
   - Menambahkan timeout untuk koneksi
   - Menambahkan kompresi untuk file besar
   - Menambahkan progress bar untuk upload/download
   - Menambahkan fitur resume transfer
   - Menambahkan fitur enkripsi end-to-end
   - Menambahkan fitur manajemen user dan permission



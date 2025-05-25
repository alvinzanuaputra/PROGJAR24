import os
import socket
import json
import base64
import logging
import argparse
import time
import csv
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def kirim_perintah(server_ip, server_port, perintah_str=""):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_ip, server_port))
        sock.sendall((perintah_str + "\r\n\r\n").encode())
        data_diterima = ""
        while True:
            data = sock.recv(524288)
            if data:
                data_diterima += data.decode()
                if "\r\n\r\n" in data_diterima:
                    break
            else:
                break
        return json.loads(data_diterima.strip())
    except Exception as e:
        return {"status": "ERROR", "data": str(e)}
    finally:
        sock.close()

def tulis_csv_operasi(operasi, filepath, waktu_mulai, waktu_selesai, status, output_file):
    """Fungsi untuk menulis hasil operasi ke file CSV"""
    waktu_total = waktu_selesai - waktu_mulai
    ukuran_file = os.path.getsize(filepath) if os.path.exists(filepath) else 0
    throughput = ukuran_file / waktu_total if waktu_total > 0 else 0
    
    # Konversi ukuran file ke format MB/KB
    if ukuran_file >= 1024*1024:
        volume_file_str = f"{round(ukuran_file / 1024 / 1024)}MB"
    else:
        volume_file_str = f"{round(ukuran_file / 1024)}KB"
    
    # Header CSV
    header = [
        "Nomor",
        "Operasi",
        "Volume",
        "Jumlah client worker pool",
        "Jumlah server worker pool",
        "Waktu total per client (detik)",
        "Throughput per client (bytes/detik)",
        "Jumlah worker client yang sukses dan gagal",
        "Jumlah worker server yang sukses dan gagal"
    ]
    
    # Data yang akan ditulis
    data = [
        1,  # Nomor (default 1 untuk operasi tunggal)
        operasi,
        volume_file_str,
        1,  # Jumlah client worker (1 untuk operasi tunggal)
        1,  # Jumlah server worker (1 untuk operasi tunggal)
        round(waktu_total, 3),
        round(throughput, 3),
        "1 sukses, 0 gagal" if status == "OK" else "0 sukses, 1 gagal",
        "1 sukses, 0 gagal" if status == "OK" else "0 sukses, 1 gagal"
    ]
    
    # Tulis ke CSV
    tulis_header = not os.path.exists(output_file)
    with open(output_file, mode="a", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if tulis_header:
            writer.writerow(header)
        writer.writerow(data)
    
    logging.info(f"Data operasi {operasi} telah dicatat ke {output_file}")

def upload_remote(server_ip, server_port, filepath="", output_csv=None):
    waktu_mulai = time.time()
    
    # Cek apakah file ada
    if not os.path.exists(filepath):
        error_msg = f"File tidak ditemukan: {filepath}"
        logging.error(error_msg)
        if output_csv:
            waktu_selesai = time.time()
            tulis_csv_operasi("upload", filepath, waktu_mulai, waktu_selesai, "ERROR", output_csv)
        return {"status": "ERROR", "data": error_msg}
    
    try:
        with open(filepath, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        filename = os.path.basename(filepath)
        perintah_str = f"UPLOAD {filename} {encoded}"
        hasil = kirim_perintah(server_ip, server_port, perintah_str)
        waktu_selesai = time.time()
        
        if output_csv:
            tulis_csv_operasi("upload", filepath, waktu_mulai, waktu_selesai, 
                            hasil.get('status', 'ERROR'), output_csv)
        
        return hasil
    except Exception as e:
        error_msg = f"Error saat upload file: {str(e)}"
        logging.error(error_msg)
        waktu_selesai = time.time()
        if output_csv:
            tulis_csv_operasi("upload", filepath, waktu_mulai, waktu_selesai, 
                            "ERROR", output_csv)
        return {"status": "ERROR", "data": error_msg}

def download_remote(server_ip, server_port, filename="", output_csv=None):
    waktu_mulai = time.time()
    perintah_str = f"GET {filename}"
    result = kirim_perintah(server_ip, server_port, perintah_str)
    
    if result.get('status') == 'OK':
        namafile = result.get('data_namafile')
        isifile = base64.b64decode(result.get('data_file'))
        save_path = f"unduh_{namafile}"
        with open(save_path, 'wb') as fp:
            fp.write(isifile)
        waktu_selesai = time.time()
        
        if output_csv:
            tulis_csv_operasi("download", save_path, waktu_mulai, waktu_selesai, 
                            "OK", output_csv)
            
        logging.info(f"File {namafile} berhasil diunduh ke {save_path}")
    else:
        waktu_selesai = time.time()
        if output_csv:
            tulis_csv_operasi("download", f"unduh_{filename}", waktu_mulai, 
                            waktu_selesai, "ERROR", output_csv)
    
    return result

def list_remote(server_ip, server_port):
    perintah_str = "LIST"
    return kirim_perintah(server_ip, server_port, perintah_str)

def tugas_worker(server_ip, server_port, operasi, filepath):
    waktu_mulai = time.time()
    if operasi == "upload":
        hasil = upload_remote(server_ip, server_port, filepath)
        ukuran_byte = os.path.getsize(filepath) if hasil.get('status') == 'OK' else 0
    elif operasi == "download":
        hasil = download_remote(server_ip, server_port, filepath)
        try:
            ukuran_byte = os.path.getsize(f"unduh_{filepath}") if hasil.get('status') == 'OK' else 0
        except:
            ukuran_byte = 0
    elif operasi == "list":
        hasil = list_remote(server_ip, server_port)
        ukuran_byte = len(str(hasil)) if hasil.get('status') == 'OK' else 0
    else:
        hasil = {"status": "ERROR", "data": "Operasi tidak dikenal"}
        ukuran_byte = 0
    
    durasi = time.time() - waktu_mulai
    return (hasil.get('status') == 'OK', durasi, ukuran_byte)

def stress_test(server_ip, server_port, operasi, filepath, mode_pool, ukuran_pool, worker_server, nomor, output_csv):
    if mode_pool == "thread":
        executor_cls = ThreadPoolExecutor
    else:
        executor_cls = ProcessPoolExecutor
    
    hasil_list = []
    waktu_mulai_semua = time.time()
    
    logging.info(f"Memulai stress test #{nomor}: {operasi} dengan {ukuran_pool} {mode_pool} worker")

    with executor_cls(max_workers=ukuran_pool) as executor:
        futures = [executor.submit(tugas_worker, server_ip, server_port, operasi, filepath) for _ in range(ukuran_pool)]
        for f in futures:
            hasil_list.append(f.result())

    waktu_total = time.time() - waktu_mulai_semua
    jumlah_sukses = sum(1 for r in hasil_list if r[0])
    jumlah_gagal = ukuran_pool - jumlah_sukses
    total_bytes = sum(r[2] for r in hasil_list)
    throughput = total_bytes / waktu_total if waktu_total > 0 else 0
    waktu_rata = waktu_total / ukuran_pool if ukuran_pool > 0 else 0

    # Menentukan volume file
    if os.path.exists(filepath):
        volume_file = os.path.getsize(filepath)
    else:
        volume_file = 0
        
    if volume_file >= 1024*1024:
        volume_file_str = f"{round(volume_file / 1024 / 1024)}MB"
    else:
        volume_file_str = f"{round(volume_file / 1024)}KB"

    # Header CSV
    header = [
        "Nomor", "Operasi", "Volume", "Jumlah client worker pool", "Jumlah server worker pool",
        "Waktu total per client (detik)", "Throughput per client (bytes/detik)",
        "Jumlah worker client yang sukses dan gagal", "Jumlah worker server yang sukses dan gagal"
    ]
    
    baris = [
        nomor, operasi, volume_file_str, ukuran_pool, worker_server,
        round(waktu_rata, 3), round(throughput / ukuran_pool if ukuran_pool > 0 else 0, 3),
        f"{jumlah_sukses} sukses, {jumlah_gagal} gagal",
        f"{worker_server} sukses, {jumlah_gagal} gagal"
    ]
    
    # Tulis ke CSV
    tulis_header = not os.path.exists(output_csv)
    
    with open(output_csv, mode="a", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if tulis_header:
            writer.writerow(header)
        writer.writerow(baris)

    print(f"Hasil stress test #{nomor} disimpan ke {output_csv}")
    print("Data:", baris)
    
    return {
        'waktu_total': waktu_total,
        'sukses': jumlah_sukses,
        'gagal': jumlah_gagal,
        'throughput': throughput
    }

def jalankan_semua_stress_test(server_ip, server_port, pool_mode, output_csv):
    """Menjalankan semua kombinasi stress test"""
    operasi_list = ['upload', 'download']
    volume_list = {
        10: "10MB-TESTFILE.ORG.pdf",
        50: "50MB-TESTFILE.ORG.pdf",
        100: "100MB-TESTFILE.ORG.pdf"
    }
    client_worker_list = [1, 5, 50]
    server_worker_list = [1, 5, 50]
    
    nomor = 1
    if pool_mode == "process":
        # Jika mode process, mulai dari nomor 55
        nomor = 55
    
    print(f"Memulai stress test lengkap dengan mode {pool_mode}...")
    print(f"Total kombinasi: {len(operasi_list)} x {len(volume_list)} x {len(client_worker_list)} x {len(server_worker_list)} = 54 test")
    
    for operasi in operasi_list:
        for volume, nama_file in volume_list.items():
            if operasi == 'upload':
                file_path = f"files/{nama_file}"
            else:
                file_path = nama_file
            
            for client_workers in client_worker_list:
                for server_workers in server_worker_list:
                    print(f"\n--- Test #{nomor} ---")
                    print(f"Mode: {pool_mode}, Operasi: {operasi}, File: {nama_file}, Client Workers: {client_workers}, Server Workers: {server_workers}")
                    
                    try:
                        hasil = stress_test(
                            server_ip, server_port, operasi, file_path,
                            pool_mode, client_workers, server_workers,
                            nomor, output_csv
                        )
                        print(f"Hasil: {hasil['sukses']} sukses, {hasil['gagal']} gagal, Throughput: {hasil['throughput']:.2f} bytes/detik")
                    except Exception as e:
                        print(f"Error pada test #{nomor}: {e}")
                    
                    nomor += 1
                    time.sleep(1)  # Jeda singkat antar test

    print(f"\nStress test mode {pool_mode} selesai! Hasil disimpan di {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="File client CLI test dan stress test")
    parser.add_argument("--server", default="172.16.16.101", help="Alamat IP server")
    parser.add_argument("--port", type=int, default=5666, help="Port server")
    parser.add_argument("--mode", choices=["upload", "download", "list", "stress", "stress_all"], required=True, help="Mode operasi")
    parser.add_argument("--file", help="Path file untuk upload atau nama file untuk download")
    parser.add_argument("--pool_mode", choices=["thread", "process"], default="thread", help="Mode pool untuk stress test")
    parser.add_argument("--pool_size", type=int, default=1, help="Jumlah concurrent worker")
    parser.add_argument("--server_workers", type=int, default=1, help="Jumlah server worker (hanya untuk logging)")
    parser.add_argument("--nomor", type=int, default=1, help="Nomor test case untuk laporan")
    parser.add_argument("--output", default="laporan_stress_test.csv", help="Nama file output CSV")
    args = parser.parse_args()

    if args.mode == "upload":
        if not args.file:
            print("Mode upload memerlukan argumen --file")
            return
            
        # Cek keberadaan file sebelum upload
        if not os.path.exists(args.file):
            print(f"ERROR: File tidak ditemukan: {args.file}")
            print("Pastikan file yang akan diupload berada di direktori yang benar")
            print(f"Direktori saat ini: {os.getcwd()}")
            print("Daftar file di direktori saat ini:")
            print("\n".join(os.listdir(".")))
            return
            
        res = upload_remote(args.server, args.port, args.file, args.output)
        print("Hasil upload:", res)
        
    elif args.mode == "download":
        if not args.file:
            print("Mode download memerlukan argumen --file")
            return
        res = download_remote(args.server, args.port, args.file, args.output)
        print("Hasil download:", res)
        
    elif args.mode == "list":
        res = list_remote(args.server, args.port)
        print("Daftar file di server:", res)
        
    elif args.mode == "stress":
        if not args.file:
            print("Stress test memerlukan argumen --file")
            return
        stress_test(
            args.server, args.port, "download", args.file,
            args.pool_mode, args.pool_size, args.server_workers,
            args.nomor, args.output
        )
        
    elif args.mode == "stress_all":
        jalankan_semua_stress_test(args.server, args.port, args.pool_mode, args.output)

if __name__ == "__main__":
    main()
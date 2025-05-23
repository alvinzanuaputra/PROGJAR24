from socket import *
import socket
import threading
import logging
import time
import sys

from file_protocol import FileProtocol

fp = FileProtocol()

class ProcessTheClient(threading.Thread):
    """Kelas untuk menangani setiap client yang terhubung"""
    def _init_(self, connection, address):
        self.connection = connection  # Menyimpan koneksi socket
        self.address = address       # Menyimpan alamat client
        threading.Thread._init_(self)
   
    def run(self):
        """Method yang dijalankan saat thread dimulai"""
        while True:
            # Menerima data dari client (maksimal 32 bytes)
            data = self.connection.recv(8096)
            if data:
                # Decode data yang diterima
                d = data.decode()
                # Proses string menggunakan protokol file
                hasil = fp.proses_string(d)
                
                # Jika hasil adalah dictionary dan merupakan request download
                if isinstance(hasil, dict) and hasil.get('is_download'):
                    # Kirim response untuk download
                    response = f"DOWNLOAD {hasil['data_namafile']}\r\n"
                    self.connection.sendall(response.encode())
                    # Kirim file yang diminta
                    self.connection.sendall(hasil['data_file'])
                    self.connection.sendall(b"\r\n\r\n")
                else:
                    # Kirim response normal
                    hasil=hasil+"\r\n\r\n"
                    self.connection.sendall(hasil.encode())
            else:
                # Jika tidak ada data, keluar dari loop
                break
        # Tutup koneksi
        self.connection.close()

class Server(threading.Thread):
    """Kelas utama server yang menangani koneksi masuk"""
    def _init_(self,ipaddress='0.0.0.0',port=8889):
        self.ipinfo=(ipaddress,port)  # Menyimpan info IP dan port
        self.the_clients = []         # List untuk menyimpan client yang terhubung
        # Buat socket TCP
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set opsi socket untuk reuse address
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread._init_(self)

    def run(self):
        """Method yang dijalankan saat thread server dimulai"""
        # Log informasi server
        logging.warning(f"server berjalan di ip address {self.ipinfo}")
        # Bind socket ke IP dan port
        self.my_socket.bind(self.ipinfo)
        # Mulai listening untuk koneksi masuk
        self.my_socket.listen(1)
        while True:
            # Terima koneksi baru
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")

            # Buat thread baru untuk menangani client
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            # Tambahkan client ke list
            self.the_clients.append(clt)

def main():
    """Fungsi utama untuk menjalankan server"""
    # Buat instance server dengan IP 0.0.0.0 dan port 46666
    svr = Server(ipaddress='0.0.0.0',port=46666)
    # Mulai server
    svr.start()

# Jalankan main() jika file dijalankan langsung
if __name__ == "_main_":
    main()
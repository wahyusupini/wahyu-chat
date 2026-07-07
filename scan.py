import requests
import time
import os
import platform


# Fungsi untuk membersihkan layar terminal
def clean():
    # Jika sistem operasi adalah Windows (NT), gunakan 'cls', jika Linux/macOS gunakan 'clear'
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")


# Fungsi utama untuk melakukan pemindaian path
def pt_scan(target, wordlist):
    print(f"[*] Memulai scanning pada target: {target}...")
    print("-" * 40)

    # Mencoba membaca file wordlist
    try:
        with open(wordlist, "r") as file:
            # Membaca file baris demi baris dan menghapus karakter enter (\n)
            files = file.read().splitlines()
    except FileNotFoundError:
        print("[!] File wordlist tidak ditemukan!")
        return

    # Melakukan perulangan untuk setiap kata di dalam wordlist
    for data in files:
        # Menyusun URL target, pastikan input target tidak diakhiri dengan '/'
        url = f"https://{target}/{data}"

        try:
            # Mengirimkan permintaan HTTP GET ke URL
            respon = requests.get(url, timeout=5)
            hasil = respon.status_code

            # Jika status code di bawah 400 (misal 200 OK atau 301/302 Redirect), dianggap valid
            if hasil < 400:
                print(f"[+] {url:<40} : {hasil}")

            # Memberikan jeda waktu antar request agar tidak membebani server
            time.sleep(0.5)

        except requests.exceptions.RequestException:
            print("[!] Request error / Tidak bisa terhubung")
            pass


if __name__ == "__main__":
    clean()
    print("=" * 10 + " PATH SCANNER " + "=" * 10)
    print("\n")

    # Meminta input dari pengguna
    target = input("[?] Masukkan target (contoh: google.com) : ")
    wordlist = input("[?] Masukkan lokasi file wordlist (.txt) : ")

    # Menjalankan fungsi scanner
    pt_scan(target, wordlist)
import sys
import os
import platform
import time
import argparse
import ctypes
import subprocess   

# --- Variabel Konfigurasi ---

WEBSITES_TO_BLOCK = [
    "www.facebook.com", "facebook.com",
    "www.twitter.com", "twitter.com",
    "www.youtube.com", "youtube.com",
    "www.instagram.com", "instagram.com",
    "www.tiktok.com", "tiktok.com",
    "www.reddit.com", "reddit.com",
    "www.snapchat.com", "snapchat.com",
    "www.linkedin.com", "linkedin.com",
]

REDIRECT_IP = "127.0.0.1"


# --- Fungsi Sistem ---

def get_hosts_path():
    system = platform.system()
    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    return "/etc/hosts"


def is_admin():
    system = platform.system()
    try:
        if system == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def flush_dns():
    """Melakukan flush DNS sesuai OS."""
    system = platform.system()
    print("Melakukan flush DNS...")

    try:
        if system == "Windows": 
            subprocess.run(["ipconfig", "/flushdns"], check=True)

        elif system == "Darwin":  # macOS
            subprocess.run(["dscacheutil", "-flushcache"], check=True)
            subprocess.run(["killall", "-HUP", "mDNSResponder"], check=True)

        elif system == "Linux": 
            # Tidak semua Linux punya service DNS yang sama
            # Coba beberapa opsi yang umum
            commands = [
                ["systemctl", "restart", "systemd-resolved"],
                ["systemctl", "restart", "NetworkManager"],
                ["resolvectl", "flush-caches"],
            ]
            for cmd in commands:
                try:
                    subprocess.run(cmd, check=True)
                    break
                except Exception:
                    continue
        print("Flush DNS berhasil.\n")

    except Exception as e:
        print(f"Gagal flush DNS otomatis: {e}")
        print("Anda mungkin perlu flush DNS secara manual.\n")


# --- Fungsi Inti ZenMode ---

def block_sites(hosts_path):
    print("ZenMode AKTIF. Memblokir situs...")
    try:
        with open(hosts_path, 'r+') as file:
            content = file.read()
            for site in WEBSITES_TO_BLOCK:
                if site not in content:
                    file.write(f"{REDIRECT_IP} {site}\n")
        print(f"Berhasil memblokir {len(WEBSITES_TO_BLOCK)} situs.")
    except Exception as e:
        print(f"GAGAL menulis ke file hosts: {e}")
        sys.exit(1)


def unblock_sites(hosts_path):
    print("ZenMode NONAKTIF. Mengembalikan akses situs...")
    try:
        with open(hosts_path, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not any(site in line for site in WEBSITES_TO_BLOCK):
                    file.write(line)
            file.truncate()
        print("File hosts telah dibersihkan.")
    except Exception as e:
        print(f"GAGAL membersihkan file hosts: {e}")


# --- Program Utama ---

if __name__ == "__main__":
    if not is_admin():
        print("Kesalahan: Skrip ini perlu hak akses Administrator/sudo.")
        sys.exit(1)

    HOSTS_PATH = get_hosts_path()

    parser = argparse.ArgumentParser(description="ZenMode: Pemblokir situs distraksi via file hosts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Mulai mode Zen dan blokir situs.")
    start_parser.add_argument("duration", type=int, help="Durasi blokir dalam MENIT.")

    stop_parser = subparsers.add_parser("stop", help="Hentikan mode Zen dan buka blokir.")

    try:
        args = parser.parse_args()

        if args.command == "start":
            # FLUSH DNS SEBELUM BLOKIR
            flush_dns()

            block_sites(HOSTS_PATH)
            duration_seconds = args.duration * 60

            print(f"ZenMode berjalan selama {args.duration} menit.")
            print("Tekan Ctrl+C untuk berhenti lebih awal.\n")

            try:
                time.sleep(duration_seconds)
            except KeyboardInterrupt:
                print("\nZenMode dihentikan manual...")
            finally:
                unblock_sites(HOSTS_PATH)
                flush_dns()

        elif args.command == "stop":
            unblock_sites(HOSTS_PATH)
            flush_dns()
            print("Mode Zen dihentikan.")

    except Exception as e:
        print(f"Terjadi error: {e}")
        unblock_sites(HOSTS_PATH)
        flush_dns()

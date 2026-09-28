import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME")	

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads/sampul")
    ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_EXCEL_EXT = {"xlsx"}

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5")) * 1024 * 1024

    # Batas hari peminjaman default
    LAMA_PINJAM_HARI = 7

    # Batas maksimal buku yang boleh dipinjam/diajukan sekaligus per mahasiswa
    # (pengajuan yang menunggu persetujuan ikut dihitung).
    MAKS_PINJAM_PER_USER = 2

    # Panjang NISN (Nomor Induk Siswa Nasional = 10 digit angka)
    NISN_PANJANG = 10

    # Lama masa berlaku kartu perpustakaan (hari) saat diterbitkan / diperpanjang
    MASA_BERLAKU_KARTU_HARI = 365

    # Jumlah hari sebelum jatuh tempo untuk mulai menampilkan peringatan
    # "akan jatuh tempo" ke mahasiswa & staf/kepala perpustakaan (menggantikan sistem denda).
    PERINGATAN_JATUH_TEMPO_HARI = 3

    # Daftar domain email yang dianggap valid saat registrasi/tambah pengguna
    # (tanpa perlu sistem verifikasi OTP). Silakan tambahkan domain kampus
    # resmi di sini jika sudah tersedia, mis. "stikomkendari.ac.id".
    ALLOWED_EMAIL_DOMAINS = [
        "gmail.com",
        "yahoo.com",
        "yahoo.co.id",
        "outlook.com",
        "hotmail.com",
        "live.com",
        "icloud.com",
        "proton.me",
        "protonmail.com",
    ]

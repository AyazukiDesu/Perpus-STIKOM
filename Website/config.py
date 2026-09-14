import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "perpustakaan_db")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-jangan-dipakai-produksi")

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads/sampul")
    ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_EXCEL_EXT = {"xlsx"}

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5")) * 1024 * 1024

    # Batas hari peminjaman default
    LAMA_PINJAM_HARI = 7

    # Jumlah hari sebelum jatuh tempo untuk mulai menampilkan peringatan
    # "akan jatuh tempo" ke anggota & staf/operator (menggantikan sistem denda).
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

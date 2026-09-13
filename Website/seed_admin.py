import getpass
from app import create_app
from extensions import db
from models import User

app = create_app()

with app.app_context():
    print("=== Buat Akun Operator Pertama ===")
    if User.query.filter_by(role="operator").first():
        print("Sudah ada akun operator di database. Tidak perlu membuat lagi.")
    else:
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        nama_lengkap = input("Nama Lengkap: ").strip()
        password = getpass.getpass("Password: ")

        if User.query.filter_by(username=username).first():
            print("Username sudah dipakai. Batal.")
        else:
            user = User(username=username, email=email, nama_lengkap=nama_lengkap, role="operator")
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Akun operator '{username}' berhasil dibuat. Silakan login lewat halaman /auth/login.")

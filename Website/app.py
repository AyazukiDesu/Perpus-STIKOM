import os
from datetime import date
from flask import Flask
from config import Config
from extensions import db, login_manager
from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Jadikan UPLOAD_FOLDER path absolut (relatif terhadap lokasi project),
    # bukan relatif terhadap folder tempat perintah dijalankan — supaya file
    # yang disimpan selalu berada di folder yang sama dengan yang disajikan
    # oleh endpoint /static, di komputer/OS manapun.
    if not os.path.isabs(app.config["UPLOAD_FOLDER"]):
        app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])

    # pastikan folder upload ada
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ---- Pengaturan dari database + helper tampilan denda ----
    from utils.pengaturan import terapkan_pengaturan
    from utils.denda import denda_peminjaman, format_rupiah
    from flask import request

    @app.before_request
    def muat_pengaturan():
        # Salin pengaturan (lama pinjam, tarif denda, dst.) dari DB ke app.config.
        if request.endpoint != "static":
            terapkan_pengaturan(app)

    app.jinja_env.filters["rupiah"] = format_rupiah
    app.jinja_env.globals["denda_sekarang"] = denda_peminjaman

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_jumlah_pending_akun():
        # Dipakai navbar untuk menampilkan badge jumlah akun yang menunggu
        # persetujuan. Hanya dihitung untuk kepala perpustakaan yang sedang login agar
        # tidak membebani query di halaman lain / role lain.
        from flask_login import current_user
        if current_user.is_authenticated and current_user.is_kepala:
            jumlah = User.query.filter_by(role="mahasiswa", status_akun="pending").count()
        else:
            jumlah = 0
        return {"jumlah_pending_akun": jumlah}

    @app.context_processor
    def inject_jumlah_pengajuan_peminjaman():
        # Dipakai navbar/sidebar untuk menampilkan badge jumlah pengajuan
        # peminjaman yang menunggu ditinjau. Hanya dihitung untuk staf/kepala perpustakaan.
        from flask_login import current_user
        from models import Peminjaman
        if current_user.is_authenticated and (current_user.is_staf or current_user.is_kepala):
            jumlah = Peminjaman.query.filter_by(status="diajukan").count()
        else:
            jumlah = 0
        return {"jumlah_pengajuan_peminjaman": jumlah}

    @app.context_processor
    def inject_tahun_sekarang():
        # Dipakai footer untuk tahun copyright, dihitung otomatis
        # (sebelumnya ditulis angka tetap "2026" di template).
        return {"tahun_sekarang": date.today().year}

    # ---- registrasi blueprint ----
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.buku import buku_bp
    from routes.peminjaman import peminjaman_bp
    from routes.laporan import laporan_bp
    from routes.kartu import kartu_bp
    from routes.denda import denda_bp
    from routes.pengaturan import pengaturan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(buku_bp)
    app.register_blueprint(peminjaman_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(kartu_bp)
    app.register_blueprint(denda_bp)
    app.register_blueprint(pengaturan_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="20.20.20.254", port=5000)

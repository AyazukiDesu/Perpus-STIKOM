import os
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

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_jumlah_pending_akun():
        # Dipakai navbar untuk menampilkan badge jumlah akun yang menunggu
        # persetujuan. Hanya dihitung untuk operator yang sedang login agar
        # tidak membebani query di halaman lain / role lain.
        from flask_login import current_user
        if current_user.is_authenticated and current_user.is_operator:
            jumlah = User.query.filter_by(role="user", status_akun="pending").count()
        else:
            jumlah = 0
        return {"jumlah_pending_akun": jumlah}

    @app.context_processor
    def inject_jumlah_pengajuan_peminjaman():
        # Dipakai navbar/sidebar untuk menampilkan badge jumlah pengajuan
        # peminjaman yang menunggu ditinjau. Hanya dihitung untuk staf/operator.
        from flask_login import current_user
        from models import Peminjaman
        if current_user.is_authenticated and (current_user.is_staf or current_user.is_operator):
            jumlah = Peminjaman.query.filter_by(status="diajukan").count()
        else:
            jumlah = 0
        return {"jumlah_pengajuan_peminjaman": jumlah}

    # ---- registrasi blueprint ----
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.buku import buku_bp
    from routes.peminjaman import peminjaman_bp
    from routes.laporan import laporan_bp
    from routes.kartu import kartu_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(buku_bp)
    app.register_blueprint(peminjaman_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(kartu_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)

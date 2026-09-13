import random
import string
from datetime import date, timedelta

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User, KartuAnggota
from utils.decorators import role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _generate_nomor_kartu():
    """Buat nomor kartu unik format ANG-XXXXXX"""
    while True:
        kode = "ANG-" + "".join(random.choices(string.digits, k=6))
        if not KartuAnggota.query.filter_by(nomor_kartu=kode).first():
            return kode


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Registrasi publik HANYA untuk role 'user' (anggota), dan HARUS lewat
    # persetujuan operator dulu sebelum bisa login (status_akun='pending').
    # Akun staf/operator dibuat oleh operator lewat menu manajemen pengguna,
    # dan otomatis langsung 'disetujui' (lihat tambah_pengguna()).
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")

        if not all([username, email, nama_lengkap, password]):
            flash("Semua field wajib diisi.", "danger")
            return redirect(url_for("auth.register"))

        if password != password2:
            flash("Konfirmasi password tidak cocok.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            nama_lengkap=nama_lengkap,
            role="user",
            status_akun="pending",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Catatan: kartu anggota digital SENGAJA belum dibuat di sini.
        # Kartu baru diterbitkan otomatis saat operator menyetujui akun
        # (lihat setujui_pengguna()), supaya masa berlaku kartu dihitung
        # sejak tanggal disetujui, bukan sejak tanggal daftar.

        flash(
            "Registrasi berhasil! Akun Anda akan aktif setelah disetujui "
            "oleh operator perpustakaan. Silakan cek kembali nanti.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if user.menunggu_persetujuan:
                flash(
                    "Akun Anda masih menunggu persetujuan operator perpustakaan. "
                    "Silakan coba login lagi nanti.",
                    "warning",
                )
                return redirect(url_for("auth.login"))
            if user.ditolak_operator:
                flash(
                    "Registrasi akun Anda ditolak oleh operator. "
                    "Hubungi operator perpustakaan untuk informasi lebih lanjut.",
                    "danger",
                )
                return redirect(url_for("auth.login"))
            if not user.is_active_db:
                flash("Akun Anda dinonaktifkan. Hubungi operator perpustakaan.", "danger")
                return redirect(url_for("auth.login"))
            login_user(user)
            flash(f"Selamat datang, {user.nama_lengkap}!", "success")
            return redirect(url_for("dashboard.index"))
        flash("Username atau password salah.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("auth.login"))


# ------------------------------------------------------------------
# Manajemen pengguna (khusus operator) - membuat akun staf/operator
# ------------------------------------------------------------------
@auth_bp.route("/pengguna")
@login_required
@role_required("operator")
def daftar_pengguna():
    pengguna = User.query.order_by(User.created_at.desc()).all()
    return render_template("auth/daftar_pengguna.html", pengguna=pengguna)


@auth_bp.route("/pengguna/tambah", methods=["GET", "POST"])
@login_required
@role_required("operator")
def tambah_pengguna():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "staf")

        if role not in ("user", "staf", "operator"):
            flash("Role tidak valid.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        # Dibuat langsung oleh operator -> otomatis dianggap terverifikasi,
        # tidak perlu melalui alur persetujuan seperti registrasi mandiri.
        user = User(
            username=username, email=email, nama_lengkap=nama_lengkap,
            role=role, status_akun="disetujui",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        if role == "user":
            kartu = KartuAnggota(
                user_id=user.id,
                nomor_kartu=_generate_nomor_kartu(),
                tanggal_terbit=date.today(),
                tanggal_kadaluarsa=date.today() + timedelta(days=365),
                status="aktif",
            )
            db.session.add(kartu)

        db.session.commit()
        flash(f"Pengguna '{username}' ({role}) berhasil dibuat.", "success")
        return redirect(url_for("auth.daftar_pengguna"))

    return render_template("auth/tambah_pengguna.html")


@auth_bp.route("/pengguna/<int:user_id>/toggle-aktif", methods=["POST"])
@login_required
@role_required("operator")
def toggle_aktif_pengguna(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Anda tidak bisa menonaktifkan akun sendiri.", "warning")
        return redirect(url_for("auth.daftar_pengguna"))
    user.is_active_db = not user.is_active_db
    db.session.commit()
    status = "diaktifkan" if user.is_active_db else "dinonaktifkan"
    flash(f"Akun '{user.username}' berhasil {status}.", "success")
    return redirect(url_for("auth.daftar_pengguna"))


# ------------------------------------------------------------------
# PERSETUJUAN AKUN ANGGOTA BARU (khusus operator)
# Registrasi mandiri lewat /auth/register masuk sini dulu sebelum
# bisa login. Tidak mengubah/menyentuh proses tambah_pengguna() di atas.
# ------------------------------------------------------------------
@auth_bp.route("/pengguna/persetujuan")
@login_required
@role_required("operator")
def daftar_persetujuan():
    pending = (
        User.query.filter_by(role="user", status_akun="pending")
        .order_by(User.created_at.asc())
        .all()
    )
    return render_template("auth/persetujuan.html", pending=pending)


@auth_bp.route("/pengguna/<int:user_id>/setujui", methods=["POST"])
@login_required
@role_required("operator")
def setujui_pengguna(user_id):
    user = User.query.get_or_404(user_id)

    if user.status_akun != "pending":
        flash("Akun ini sudah pernah diproses sebelumnya.", "warning")
        return redirect(url_for("auth.daftar_persetujuan"))

    user.status_akun = "disetujui"

    # terbitkan kartu anggota digital sekarang (masa berlaku dihitung
    # sejak tanggal disetujui, bukan sejak tanggal daftar)
    if not user.kartu:
        kartu = KartuAnggota(
            user_id=user.id,
            nomor_kartu=_generate_nomor_kartu(),
            tanggal_terbit=date.today(),
            tanggal_kadaluarsa=date.today() + timedelta(days=365),
            status="aktif",
        )
        db.session.add(kartu)

    db.session.commit()
    flash(f"Akun '{user.username}' disetujui dan kartu anggota diterbitkan.", "success")
    return redirect(url_for("auth.daftar_persetujuan"))


@auth_bp.route("/pengguna/<int:user_id>/tolak", methods=["POST"])
@login_required
@role_required("operator")
def tolak_pengguna(user_id):
    user = User.query.get_or_404(user_id)

    if user.status_akun != "pending":
        flash("Akun ini sudah pernah diproses sebelumnya.", "warning")
        return redirect(url_for("auth.daftar_persetujuan"))

    user.status_akun = "ditolak"
    user.is_active_db = False
    db.session.commit()
    flash(f"Registrasi '{user.username}' ditolak.", "info")
    return redirect(url_for("auth.daftar_persetujuan"))

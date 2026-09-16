import random
import string
from datetime import date, timedelta

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User, KartuAnggota, Peminjaman
from utils.decorators import role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


_PREFIX_KARTU = {"user": "ANG", "staf": "STF", "operator": "OPR"}


def _email_domain_valid(email):
    """Cek domain email terhadap Config.ALLOWED_EMAIL_DOMAINS.
    (Sebelumnya daftar ini ada di config.py tapi tidak pernah dipakai/divalidasi.)"""
    from flask import current_app
    domain = email.rsplit("@", 1)[-1].lower() if "@" in email else ""
    allowed = current_app.config.get("ALLOWED_EMAIL_DOMAINS") or []
    return domain in allowed


def _generate_nomor_kartu(role="user"):
    """Buat nomor kartu unik, format <PREFIX>-XXXXXX.
    Prefix mengikuti role pemilik kartu: ANG (anggota), STF (staf), OPR (operator)."""
    prefix = _PREFIX_KARTU.get(role, "ANG")
    while True:
        kode = f"{prefix}-" + "".join(random.choices(string.digits, k=6))
        if not KartuAnggota.query.filter_by(nomor_kartu=kode).first():
            return kode


def _terbitkan_kartu_jika_belum_ada(user):
    """Terbitkan kartu perpustakaan digital untuk user manapun (semua role)
    jika dia belum punya. Dipakai saat akun dibuat/disetujui, dan sebagai
    fallback 'lazy create' saat akun lama (dibuat sebelum fitur ini ada)
    membuka halaman kartunya sendiri."""
    if user.kartu:
        return user.kartu
    kartu = KartuAnggota(
        user_id=user.id,
        nomor_kartu=_generate_nomor_kartu(user.role),
        tanggal_terbit=date.today(),
        tanggal_kadaluarsa=date.today() + timedelta(days=365),
        status="aktif",
    )
    db.session.add(kartu)
    db.session.commit()
    return kartu


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

        if len(password) < 6:
            flash("Password minimal 6 karakter.", "danger")
            return redirect(url_for("auth.register"))

        if not _email_domain_valid(email):
            flash("Domain email tidak diizinkan. Gunakan email pribadi yang umum (gmail, yahoo, outlook, dsb).", "danger")
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

        if len(password) < 6:
            flash("Password minimal 6 karakter.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        if not _email_domain_valid(email):
            flash("Domain email tidak diizinkan. Gunakan email pribadi yang umum (gmail, yahoo, outlook, dsb).", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        # BUG LAMA: dulu hanya username yang dicek duplikatnya di sini, email
        # tidak dicek sama sekali -> submit email yang sudah dipakai bikin
        # server error 500 (UNIQUE constraint gagal di database).
        if User.query.filter_by(email=email).first():
            flash("Email sudah digunakan pengguna lain.", "danger")
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

        # Kartu perpustakaan digital sekarang diterbitkan untuk SEMUA role
        # (anggota, staf, maupun operator), bukan cuma anggota.
        kartu = KartuAnggota(
            user_id=user.id,
            nomor_kartu=_generate_nomor_kartu(role),
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


@auth_bp.route("/pengguna/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("operator")
def edit_pengguna(user_id):
    # Edit akun sendiri diarahkan ke halaman "Profil Saya" (self-service),
    # supaya operator tidak bisa tanpa sadar mengubah role/status akunnya sendiri
    # lewat form manajemen pengguna ini.
    if user_id == current_user.id:
        flash("Gunakan halaman 'Profil Saya' untuk mengedit akun Anda sendiri.", "info")
        return redirect(url_for("auth.profil"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        no_telepon = request.form.get("no_telepon", "").strip()
        alamat = request.form.get("alamat", "").strip()
        role = request.form.get("role", user.role)
        password_baru = request.form.get("password", "")

        if not all([username, email, nama_lengkap]):
            flash("Nama, username, dan email wajib diisi.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        if role not in ("user", "staf", "operator"):
            flash("Role tidak valid.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        duplikat_username = User.query.filter(User.username == username, User.id != user.id).first()
        if duplikat_username:
            flash("Username sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        duplikat_email = User.query.filter(User.email == email, User.id != user.id).first()
        if duplikat_email:
            flash("Email sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        # Jika akun ini satu-satunya operator, jangan biarkan diturunkan rolenya
        # dari sini (mencegah sistem kehilangan seluruh akses operator).
        if user.is_operator and role != "operator":
            jumlah_operator = User.query.filter_by(role="operator").count()
            if jumlah_operator <= 1:
                flash("Tidak bisa mengubah role: ini adalah satu-satunya akun operator yang tersisa.", "warning")
                return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        user.username = username
        user.email = email
        user.nama_lengkap = nama_lengkap
        user.no_telepon = no_telepon or None
        user.alamat = alamat or None
        user.role = role

        if password_baru:
            user.set_password(password_baru)

        # kalau kartu belum pernah terbit (mis. akun lama sebelum fitur ini ada), terbitkan sekarang
        _terbitkan_kartu_jika_belum_ada(user)

        db.session.commit()
        flash(f"Akun '{user.username}' berhasil diperbarui.", "success")
        return redirect(url_for("auth.daftar_pengguna"))

    return render_template("auth/edit_pengguna.html", u=user)


@auth_bp.route("/pengguna/<int:user_id>/hapus", methods=["POST"])
@login_required
@role_required("operator")
def hapus_pengguna(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Anda tidak bisa menghapus akun sendiri.", "warning")
        return redirect(url_for("auth.daftar_pengguna"))

    if user.is_operator:
        jumlah_operator = User.query.filter_by(role="operator").count()
        if jumlah_operator <= 1:
            flash("Tidak bisa menghapus: ini adalah satu-satunya akun operator yang tersisa.", "warning")
            return redirect(url_for("auth.daftar_pengguna"))

    # Cegah hapus akun yang masih punya pengajuan/peminjaman AKTIF —
    # harus diselesaikan (dikembalikan/ditolak) dulu supaya stok buku &
    # data sirkulasi tetap konsisten.
    ada_aktif = Peminjaman.query.filter(
        Peminjaman.user_id == user.id,
        Peminjaman.status.in_(["diajukan", "dipinjam"]),
    ).first()
    if ada_aktif:
        flash(
            f"Tidak bisa menghapus '{user.username}': masih ada pengajuan/peminjaman aktif. "
            "Selesaikan (kembalikan/tolak) dulu, atau nonaktifkan saja akunnya.",
            "warning",
        )
        return redirect(url_for("auth.daftar_pengguna"))

    username = user.username
    riwayat_lama = Peminjaman.query.filter_by(user_id=user.id).count()
    db.session.delete(user)
    db.session.commit()

    pesan = f"Akun '{username}' berhasil dihapus."
    if riwayat_lama:
        pesan += f" ({riwayat_lama} riwayat peminjaman lama miliknya ikut terhapus.)"
    flash(pesan, "success")
    return redirect(url_for("auth.daftar_pengguna"))


# ------------------------------------------------------------------
# PROFIL SAYA (self-service, khusus staf & operator) - edit data diri
# sendiri & ganti password. Tidak boleh mengubah role/status akun sendiri
# lewat sini (itu tetap lewat menu manajemen pengguna, oleh operator lain).
# ------------------------------------------------------------------
@auth_bp.route("/profil", methods=["GET", "POST"])
@login_required
@role_required("staf", "operator")
def profil():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        no_telepon = request.form.get("no_telepon", "").strip()
        alamat = request.form.get("alamat", "").strip()
        password_lama = request.form.get("password_lama", "")
        password_baru = request.form.get("password_baru", "")
        password_baru2 = request.form.get("password_baru2", "")

        if not all([email, nama_lengkap]):
            flash("Nama dan email wajib diisi.", "danger")
            return redirect(url_for("auth.profil"))

        duplikat_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if duplikat_email:
            flash("Email sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.profil"))

        # ganti password bersifat opsional, tapi kalau diisi harus lengkap & valid
        if password_baru or password_baru2 or password_lama:
            if not current_user.check_password(password_lama):
                flash("Password lama yang dimasukkan salah.", "danger")
                return redirect(url_for("auth.profil"))
            if password_baru != password_baru2:
                flash("Konfirmasi password baru tidak cocok.", "danger")
                return redirect(url_for("auth.profil"))
            if len(password_baru) < 6:
                flash("Password baru minimal 6 karakter.", "danger")
                return redirect(url_for("auth.profil"))
            current_user.set_password(password_baru)

        current_user.email = email
        current_user.nama_lengkap = nama_lengkap
        current_user.no_telepon = no_telepon or None
        current_user.alamat = alamat or None

        _terbitkan_kartu_jika_belum_ada(current_user)

        db.session.commit()
        flash("Profil berhasil diperbarui.", "success")
        return redirect(url_for("auth.profil"))

    return render_template("auth/profil.html")


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
            nomor_kartu=_generate_nomor_kartu(user.role),
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

from datetime import date, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user

from extensions import db
from models import Peminjaman, Buku, User
from utils.decorators import role_required

peminjaman_bp = Blueprint("peminjaman", __name__, url_prefix="/peminjaman")


# ------------------------------------------------------------------
# PROSES PEMINJAMAN BARU (dilakukan oleh staf/operator saat anggota datang)
# ------------------------------------------------------------------
@peminjaman_bp.route("/pinjam/<int:buku_id>", methods=["GET", "POST"])
@login_required
@role_required("staf", "operator")
def pinjam_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)

    if request.method == "POST":
        user_id = request.form.get("user_id", type=int)
        anggota = User.query.filter_by(id=user_id, role="user").first()

        if not anggota:
            flash("Anggota tidak ditemukan.", "danger")
            return redirect(url_for("peminjaman.pinjam_buku", buku_id=buku_id))

        if buku.stok <= 0:
            flash("Stok buku habis, tidak bisa dipinjam.", "danger")
            return redirect(url_for("buku.detail_buku", buku_id=buku_id))

        # cek apakah anggota masih meminjam buku yang sama & belum kembali
        sudah_pinjam = Peminjaman.query.filter_by(
            user_id=anggota.id, buku_id=buku.id, status="dipinjam"
        ).first()
        if sudah_pinjam:
            flash(f"{anggota.nama_lengkap} masih meminjam buku ini dan belum mengembalikannya.", "warning")
            return redirect(url_for("peminjaman.pinjam_buku", buku_id=buku_id))

        lama_hari = current_app.config["LAMA_PINJAM_HARI"]
        peminjaman = Peminjaman(
            user_id=anggota.id,
            buku_id=buku.id,
            diproses_oleh=current_user.id,
            tanggal_pinjam=date.today(),
            tanggal_jatuh_tempo=date.today() + timedelta(days=lama_hari),
            status="dipinjam",
        )
        buku.stok -= 1
        db.session.add(peminjaman)
        db.session.commit()

        flash(
            f"Buku '{buku.judul}' berhasil dipinjamkan ke {anggota.nama_lengkap}. "
            f"Jatuh tempo: {peminjaman.tanggal_jatuh_tempo.strftime('%d-%m-%Y')}.",
            "success",
        )
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    anggota_list = User.query.filter_by(role="user", is_active_db=True).order_by(User.nama_lengkap).all()
    return render_template("peminjaman/pinjam.html", buku=buku, anggota_list=anggota_list)


# ------------------------------------------------------------------
# DAFTAR PEMINJAMAN AKTIF (staf/operator) - dengan indikator terlambat
# ------------------------------------------------------------------
@peminjaman_bp.route("/")
@login_required
@role_required("staf", "operator")
def daftar_peminjaman():
    status_filter = request.args.get("status", "dipinjam")
    query = Peminjaman.query
    if status_filter != "semua":
        query = query.filter_by(status=status_filter)
    daftar = query.order_by(Peminjaman.tanggal_pinjam.desc()).all()
    return render_template("peminjaman/daftar.html", daftar=daftar, status_filter=status_filter, today=date.today())


# ------------------------------------------------------------------
# PROSES PENGEMBALIAN
# ------------------------------------------------------------------
@peminjaman_bp.route("/<int:peminjaman_id>/kembalikan", methods=["POST"])
@login_required
@role_required("staf", "operator")
def kembalikan_buku(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status == "dikembalikan":
        flash("Buku ini sudah dikembalikan sebelumnya.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    p.tanggal_kembali = date.today()
    p.status = "dikembalikan"

    if p.tanggal_kembali > p.tanggal_jatuh_tempo:
        hari_telat = (p.tanggal_kembali - p.tanggal_jatuh_tempo).days
        p.denda = hari_telat * current_app.config["DENDA_PER_HARI"]
        flash(f"Buku dikembalikan TERLAMBAT {hari_telat} hari. Denda: Rp{p.denda:,}", "warning")
    else:
        flash("Buku berhasil dikembalikan tepat waktu.", "success")

    p.buku.stok += 1
    db.session.commit()
    return redirect(url_for("peminjaman.daftar_peminjaman"))


# ------------------------------------------------------------------
# RIWAYAT PEMINJAMAN PER PESERTA (anggota lihat riwayat sendiri;
# staf/operator bisa lihat riwayat anggota manapun)
# ------------------------------------------------------------------
@peminjaman_bp.route("/riwayat/saya")
@login_required
@role_required("user")
def riwayat_saya():
    daftar = (
        Peminjaman.query.filter_by(user_id=current_user.id)
        .order_by(Peminjaman.tanggal_pinjam.desc())
        .all()
    )
    return render_template("peminjaman/riwayat_anggota.html", daftar=daftar, anggota=current_user, today=date.today())


@peminjaman_bp.route("/riwayat/anggota/<int:user_id>")
@login_required
@role_required("staf", "operator")
def riwayat_anggota(user_id):
    anggota = User.query.get_or_404(user_id)
    daftar = (
        Peminjaman.query.filter_by(user_id=user_id)
        .order_by(Peminjaman.tanggal_pinjam.desc())
        .all()
    )
    return render_template("peminjaman/riwayat_anggota.html", daftar=daftar, anggota=anggota, today=date.today())


# ------------------------------------------------------------------
# RIWAYAT PEMINJAMAN PER BUKU
# ------------------------------------------------------------------
@peminjaman_bp.route("/riwayat/buku/<int:buku_id>")
@login_required
@role_required("staf", "operator")
def riwayat_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    daftar = (
        Peminjaman.query.filter_by(buku_id=buku_id)
        .order_by(Peminjaman.tanggal_pinjam.desc())
        .all()
    )
    return render_template("peminjaman/riwayat_buku.html", daftar=daftar, buku=buku, today=date.today())

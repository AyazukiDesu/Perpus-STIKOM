from datetime import date, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from extensions import db
from models import User, KartuAnggota
from utils.decorators import role_required
from utils.kartu import validasi_nisn, terbitkan_kartu_jika_belum_ada as _terbitkan_kartu_jika_belum_ada

kartu_bp = Blueprint("kartu", __name__, url_prefix="/kartu")


# Kartu perpustakaan digital berlaku untuk SEMUA role (mahasiswa, staf, kepala
# perpustakaan). Kalau akun lama belum pernah punya kartu (dibuat sebelum fitur
# ini ada), kartunya diterbitkan otomatis saat pertama kali dibuka ("lazy create").
# ID kartu = NISN pemilik.
@kartu_bp.route("/saya")
@login_required
def kartu_saya():
    kartu = _terbitkan_kartu_jika_belum_ada(current_user)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=current_user)


@kartu_bp.route("/saya/cetak")
@login_required
def kartu_saya_cetak():
    kartu = _terbitkan_kartu_jika_belum_ada(current_user)
    return render_template("kartu/cetak.html", kartu=kartu, anggota=current_user)


@kartu_bp.route("/anggota/<int:user_id>")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kartu_anggota_lain(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = _terbitkan_kartu_jika_belum_ada(anggota)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=anggota)


@kartu_bp.route("/anggota/<int:user_id>/cetak")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kartu_anggota_lain_cetak(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = _terbitkan_kartu_jika_belum_ada(anggota)
    return render_template("kartu/cetak.html", kartu=kartu, anggota=anggota)


# ------------------------------------------------------------------
# PENGATURAN KARTU PERPUSTAKAAN (staf & kepala perpustakaan)
# Daftar semua kartu, ubah NISN / masa berlaku / status, perpanjang,
# aktifkan-nonaktifkan. Kartu nonaktif atau kadaluarsa tidak bisa
# dipakai meminjam buku.
# ------------------------------------------------------------------
@kartu_bp.route("/kelola")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kelola_kartu():
    q = request.args.get("q", "").strip()
    filter_status = request.args.get("status", "semua")

    query = KartuAnggota.query.join(User, KartuAnggota.user_id == User.id)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like), User.nisn.ilike(like))
        )
    if filter_status == "aktif":
        query = query.filter(KartuAnggota.status == "aktif", KartuAnggota.tanggal_kadaluarsa >= date.today())
    elif filter_status == "nonaktif":
        query = query.filter(KartuAnggota.status == "nonaktif")
    elif filter_status == "kadaluarsa":
        query = query.filter(KartuAnggota.tanggal_kadaluarsa < date.today())

    daftar = query.order_by(User.nama_lengkap.asc()).all()

    # akun yang belum punya kartu (mis. akun lama / masih pending) ditampilkan terpisah
    tanpa_kartu = (
        User.query.outerjoin(KartuAnggota, KartuAnggota.user_id == User.id)
        .filter(KartuAnggota.id.is_(None), User.status_akun == "disetujui")
        .order_by(User.nama_lengkap.asc())
        .all()
    )
    return render_template(
        "kartu/kelola.html", daftar=daftar, tanpa_kartu=tanpa_kartu,
        q=q, filter_status=filter_status, today=date.today(),
    )


@kartu_bp.route("/kelola/terbitkan/<int:user_id>", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def terbitkan_kartu(user_id):
    user = User.query.get_or_404(user_id)
    if user.kartu:
        flash("Pengguna ini sudah memiliki kartu.", "warning")
    else:
        _terbitkan_kartu_jika_belum_ada(user)
        flash(f"Kartu untuk '{user.nama_lengkap}' berhasil diterbitkan.", "success")
    return redirect(url_for("kartu.kelola_kartu"))


@kartu_bp.route("/kelola/<int:kartu_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def edit_kartu(kartu_id):
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    pemilik = kartu.pemilik

    if request.method == "POST":
        nisn, err = validasi_nisn(
            request.form.get("nisn", ""), wajib=pemilik.is_mahasiswa, abaikan_user_id=pemilik.id
        )
        if err:
            flash(err, "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))

        try:
            terbit = date.fromisoformat(request.form.get("tanggal_terbit", ""))
            kadaluarsa = date.fromisoformat(request.form.get("tanggal_kadaluarsa", ""))
        except ValueError:
            flash("Format tanggal tidak valid.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))
        if kadaluarsa < terbit:
            flash("Tanggal kadaluarsa tidak boleh lebih awal dari tanggal terbit.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))

        status = request.form.get("status", kartu.status)
        if status not in ("aktif", "nonaktif"):
            flash("Status kartu tidak valid.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))

        pemilik.nisn = nisn
        kartu.tanggal_terbit = terbit
        kartu.tanggal_kadaluarsa = kadaluarsa
        kartu.status = status
        db.session.commit()
        flash(f"Kartu '{pemilik.nama_lengkap}' berhasil diperbarui.", "success")
        return redirect(url_for("kartu.kelola_kartu"))

    return render_template("kartu/edit.html", kartu=kartu, pemilik=pemilik)


@kartu_bp.route("/kelola/<int:kartu_id>/toggle", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def toggle_kartu(kartu_id):
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    kartu.status = "nonaktif" if kartu.status == "aktif" else "aktif"
    db.session.commit()
    flash(f"Kartu '{kartu.pemilik.nama_lengkap}' sekarang {kartu.status}.", "success")
    return redirect(request.referrer or url_for("kartu.kelola_kartu"))


@kartu_bp.route("/kelola/<int:kartu_id>/perpanjang", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def perpanjang_kartu(kartu_id):
    """Perpanjang masa berlaku. Dihitung dari tanggal kadaluarsa saat ini kalau
    kartu masih berlaku, atau dari hari ini kalau sudah kadaluarsa."""
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    hari = current_app.config["MASA_BERLAKU_KARTU_HARI"]
    dasar = max(kartu.tanggal_kadaluarsa, date.today())
    kartu.tanggal_kadaluarsa = dasar + timedelta(days=hari)
    kartu.status = "aktif"
    db.session.commit()
    flash(
        f"Kartu '{kartu.pemilik.nama_lengkap}' diperpanjang sampai "
        f"{kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y')}.",
        "success",
    )
    return redirect(url_for("kartu.kelola_kartu"))

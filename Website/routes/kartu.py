from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import User
from utils.decorators import role_required
from routes.auth import _terbitkan_kartu_jika_belum_ada

kartu_bp = Blueprint("kartu", __name__, url_prefix="/kartu")


# Kartu perpustakaan digital sekarang berlaku untuk SEMUA role (anggota, staf,
# operator). Kalau akun lama belum pernah punya kartu (dibuat sebelum fitur
# ini ada), kartunya diterbitkan otomatis saat pertama kali dibuka ("lazy create").
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
@role_required("staf", "operator")
def kartu_anggota_lain(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = _terbitkan_kartu_jika_belum_ada(anggota)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=anggota)


@kartu_bp.route("/anggota/<int:user_id>/cetak")
@login_required
@role_required("staf", "operator")
def kartu_anggota_lain_cetak(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = _terbitkan_kartu_jika_belum_ada(anggota)
    return render_template("kartu/cetak.html", kartu=kartu, anggota=anggota)

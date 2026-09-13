from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from models import User, KartuAnggota
from utils.decorators import role_required

kartu_bp = Blueprint("kartu", __name__, url_prefix="/kartu")


@kartu_bp.route("/saya")
@login_required
@role_required("user")
def kartu_saya():
    kartu = KartuAnggota.query.filter_by(user_id=current_user.id).first()
    if not kartu:
        abort(404)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=current_user)


@kartu_bp.route("/anggota/<int:user_id>")
@login_required
@role_required("staf", "operator")
def kartu_anggota_lain(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = KartuAnggota.query.filter_by(user_id=user_id).first_or_404()
    return render_template("kartu/kartu.html", kartu=kartu, anggota=anggota)

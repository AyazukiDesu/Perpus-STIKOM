from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required

from utils.decorators import role_required
from utils.pengaturan import DAFTAR, nilai_saat_ini, simpan_pengaturan

pengaturan_bp = Blueprint("pengaturan", __name__, url_prefix="/pengaturan")


@pengaturan_bp.route("/", methods=["GET", "POST"])
@login_required
@role_required("kepala_perpustakaan")
def halaman():
    if request.method == "POST":
        baru, galat = {}, []
        for kunci, _cfg, minimum, maksimum, label, satuan, _bantuan in DAFTAR:
            mentah = request.form.get(kunci, "").strip().replace(".", "")
            try:
                nilai = int(mentah)
            except ValueError:
                galat.append(f"{label}: isi dengan angka bulat.")
                continue
            if not (minimum <= nilai <= maksimum):
                galat.append(f"{label}: harus antara {minimum} dan {maksimum}.")
                continue
            baru[kunci] = nilai

        if galat:
            for g in galat:
                flash(g, "danger")
        else:
            simpan_pengaturan(baru)
            flash("Pengaturan disimpan. Berlaku untuk peminjaman berikutnya; "
                  "peminjaman yang sudah berjalan tidak berubah jatuh temponya.", "success")
        return redirect(url_for("pengaturan.halaman"))

    nilai = nilai_saat_ini(current_app)
    kolom = [
        {"kunci": k, "label": label, "satuan": satuan, "bantuan": bantuan,
         "min": mn, "maks": mx, "nilai": nilai[k]}
        for k, _c, mn, mx, label, satuan, bantuan in DAFTAR
    ]
    return render_template("pengaturan/halaman.html", kolom=kolom)

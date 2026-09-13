import os
import uuid
from collections import OrderedDict
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash,
    current_app, send_file, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from models import Buku, Kategori
from utils.decorators import role_required
from utils.excel_import import buat_template_excel, import_buku_dari_excel

buku_bp = Blueprint("buku", __name__, url_prefix="/buku")


def _allowed_image(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXT"]


def _simpan_sampul(file_storage):
    """Simpan file gambar ke folder upload, kembalikan path relatif terhadap
    folder 'static/' (selalu pakai forward-slash, aman di Windows/Linux/Mac)."""
    if not file_storage or file_storage.filename == "":
        return None
    if not _allowed_image(file_storage.filename):
        flash("Format gambar tidak didukung (gunakan png/jpg/jpeg/webp).", "warning")
        return None

    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    nama_unik = f"{uuid.uuid4().hex}.{ext}"
    nama_aman = secure_filename(nama_unik)
    path_lengkap = os.path.join(current_app.config["UPLOAD_FOLDER"], nama_aman)
    file_storage.save(path_lengkap)

    # Path disimpan ke DB relatif terhadap folder static, dengan '/' selalu
    # (bukan os.path.join) agar konsisten dipakai ulang oleh url_for('static', ...)
    # di semua template, terlepas dari OS server-nya.
    return f"uploads/sampul/{nama_aman}"  # contoh: uploads/sampul/xxxx.jpg


# ------------------------------------------------------------------
# DAFTAR & PENCARIAN BUKU (semua role bisa lihat)
# ------------------------------------------------------------------
@buku_bp.route("/")
@login_required
def daftar_buku():
    q = request.args.get("q", "").strip()
    kategori_id = request.args.get("kategori_id", type=int)

    query = Buku.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Buku.judul.ilike(like), Buku.penulis.ilike(like), Buku.isbn.ilike(like))
        )
    if kategori_id:
        query = query.filter(Buku.kategori_id == kategori_id)

    daftar = query.order_by(Buku.judul.asc()).all()
    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()

    # Kelompokkan buku per kategori agar tampilannya seperti rak perpustakaan
    # sungguhan: tiap rak (kategori) berisi buku-bukunya sendiri, rapi dan mudah dipahami.
    kelompok = OrderedDict()
    for kat in kategori_list:
        buku_kat = [b for b in daftar if b.kategori_id == kat.id]
        if buku_kat:
            kelompok[kat.nama_kategori] = buku_kat
    tanpa_kategori = [b for b in daftar if not b.kategori_id]
    if tanpa_kategori:
        kelompok["Tanpa Kategori"] = tanpa_kategori

    return render_template(
        "buku/daftar.html", daftar=daftar, kelompok=kelompok,
        kategori_list=kategori_list, q=q, kategori_id=kategori_id
    )


@buku_bp.route("/<int:buku_id>")
@login_required
def detail_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    return render_template("buku/detail.html", buku=buku)


# ------------------------------------------------------------------
# TAMBAH / EDIT / HAPUS BUKU (khusus staf & operator)
# ------------------------------------------------------------------
@buku_bp.route("/tambah", methods=["GET", "POST"])
@login_required
@role_required("staf", "operator")
def tambah_buku():
    if request.method == "POST":
        judul = request.form.get("judul", "").strip()
        penulis = request.form.get("penulis", "").strip()
        penerbit = request.form.get("penerbit", "").strip()
        tahun_terbit = request.form.get("tahun_terbit", type=int)
        isbn = request.form.get("isbn", "").strip()
        kategori_id = request.form.get("kategori_id", type=int)
        deskripsi = request.form.get("deskripsi", "").strip()
        stok = request.form.get("stok", type=int, default=0)

        if not judul or not penulis:
            flash("Judul dan penulis wajib diisi.", "danger")
            return redirect(url_for("buku.tambah_buku"))

        sampul_path = _simpan_sampul(request.files.get("sampul"))

        buku = Buku(
            judul=judul, penulis=penulis, penerbit=penerbit or None,
            tahun_terbit=tahun_terbit, isbn=isbn or None, kategori_id=kategori_id or None,
            deskripsi=deskripsi or None, stok=stok or 0, sampul_path=sampul_path,
        )
        db.session.add(buku)
        db.session.commit()
        flash(f"Buku '{judul}' berhasil ditambahkan.", "success")
        return redirect(url_for("buku.daftar_buku"))

    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()
    return render_template("buku/form.html", buku=None, kategori_list=kategori_list)


@buku_bp.route("/<int:buku_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("staf", "operator")
def edit_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)

    if request.method == "POST":
        buku.judul = request.form.get("judul", "").strip()
        buku.penulis = request.form.get("penulis", "").strip()
        buku.penerbit = request.form.get("penerbit", "").strip() or None
        buku.tahun_terbit = request.form.get("tahun_terbit", type=int)
        buku.isbn = request.form.get("isbn", "").strip() or None
        buku.kategori_id = request.form.get("kategori_id", type=int) or None
        buku.deskripsi = request.form.get("deskripsi", "").strip() or None
        buku.stok = request.form.get("stok", type=int, default=0)

        sampul_baru = _simpan_sampul(request.files.get("sampul"))
        if sampul_baru:
            buku.sampul_path = sampul_baru

        db.session.commit()
        flash(f"Buku '{buku.judul}' berhasil diperbarui.", "success")
        return redirect(url_for("buku.daftar_buku"))

    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()
    return render_template("buku/form.html", buku=buku, kategori_list=kategori_list)


@buku_bp.route("/<int:buku_id>/hapus", methods=["POST"])
@login_required
@role_required("operator")
def hapus_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    judul = buku.judul
    db.session.delete(buku)
    db.session.commit()
    flash(f"Buku '{judul}' berhasil dihapus.", "success")
    return redirect(url_for("buku.daftar_buku"))


# ------------------------------------------------------------------
# KATEGORI
# ------------------------------------------------------------------
@buku_bp.route("/kategori", methods=["GET", "POST"])
@login_required
@role_required("staf", "operator")
def kategori():
    if request.method == "POST":
        nama = request.form.get("nama_kategori", "").strip()
        if nama and not Kategori.query.filter_by(nama_kategori=nama).first():
            db.session.add(Kategori(nama_kategori=nama))
            db.session.commit()
            flash(f"Kategori '{nama}' ditambahkan.", "success")
        else:
            flash("Kategori kosong atau sudah ada.", "warning")
        return redirect(url_for("buku.kategori"))

    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()
    return render_template("buku/kategori.html", kategori_list=kategori_list)


# ------------------------------------------------------------------
# IMPORT / EXPORT EXCEL (khusus staf & operator)
# ------------------------------------------------------------------
@buku_bp.route("/template-excel")
@login_required
@role_required("staf", "operator")
def download_template_excel():
    buffer = buat_template_excel()
    return send_file(
        buffer,
        as_attachment=True,
        download_name="template_import_buku.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@buku_bp.route("/import-excel", methods=["GET", "POST"])
@login_required
@role_required("staf", "operator")
def import_excel():
    if request.method == "POST":
        file = request.files.get("file_excel")
        if not file or file.filename == "":
            flash("Pilih file Excel (.xlsx) terlebih dahulu.", "danger")
            return redirect(url_for("buku.import_excel"))

        if not file.filename.lower().endswith(".xlsx"):
            flash("File harus berformat .xlsx", "danger")
            return redirect(url_for("buku.import_excel"))

        sukses, errors = import_buku_dari_excel(file.stream)
        flash(f"{sukses} buku berhasil diimport.", "success" if sukses else "warning")
        for err in errors[:20]:
            flash(err, "warning")
        return redirect(url_for("buku.daftar_buku"))

    return render_template("buku/import_excel.html")

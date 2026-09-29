from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from sqlalchemy import func

from extensions import db
from models import Peminjaman, User, Buku
from utils.decorators import role_required
from utils.denda import denda_peminjaman, denda_berjalan_semua, format_rupiah
from utils.excel_export import buat_excel

denda_bp = Blueprint("denda", __name__, url_prefix="/denda")

STATUS_LABEL = {
    "belum_lunas": "Belum Lunas",
    "lunas": "Lunas",
    "dibebaskan": "Dibebaskan",
    "tidak_ada": "-",
}


def _query_denda(status, q):
    """Peminjaman yang memiliki denda (sudah dibekukan) sesuai filter status & pencarian."""
    query = Peminjaman.query.filter(Peminjaman.denda > 0)
    if status in ("belum_lunas", "lunas", "dibebaskan"):
        query = query.filter(Peminjaman.status_denda == status)
    if q:
        like = f"%{q}%"
        query = (
            query.join(User, Peminjaman.user_id == User.id)
            .join(Buku, Peminjaman.buku_id == Buku.id)
            .filter(db.or_(
                User.nama_lengkap.ilike(like), User.username.ilike(like),
                User.nim.ilike(like), Buku.judul.ilike(like),
            ))
        )
    return query


@denda_bp.route("/")
@login_required
@role_required("staf", "kepala_perpustakaan")
def daftar_denda():
    status = request.args.get("status", "belum_lunas")
    q = request.args.get("q", "").strip()

    if status == "berjalan":
        # buku yang masih dipinjam dan sudah telat: denda masih terus bertambah
        semua = Peminjaman.query.filter_by(status="dipinjam").order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all()
        daftar = [p for p in semua if denda_peminjaman(p) > 0 or p.hari_telat > 0]
        if q:
            k = q.lower()
            daftar = [p for p in daftar if k in p.anggota.nama_lengkap.lower()
                      or k in p.anggota.username.lower() or k in p.buku.judul.lower()]
    else:
        daftar = _query_denda(status, q).order_by(Peminjaman.tanggal_kembali.desc()).all()

    awal_bulan = date.today().replace(day=1)
    total_belum_lunas = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "belum_lunas").scalar() or 0
    terkumpul_bulan_ini = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "lunas", Peminjaman.tanggal_denda_selesai >= awal_bulan).scalar() or 0
    terkumpul_total = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "lunas").scalar() or 0

    return render_template(
        "denda/daftar.html", daftar=daftar, status=status, q=q,
        total_belum_lunas=int(total_belum_lunas),
        terkumpul_bulan_ini=int(terkumpul_bulan_ini),
        terkumpul_total=int(terkumpul_total),
        total_berjalan=denda_berjalan_semua(),
        total_daftar=sum(denda_peminjaman(p) for p in daftar),
        status_label=STATUS_LABEL,
    )


@denda_bp.route("/<int:peminjaman_id>/lunas", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def lunasi(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status_denda != "belum_lunas":
        flash("Denda ini tidak berstatus belum lunas.", "warning")
        return redirect(request.referrer or url_for("denda.daftar_denda"))

    p.status_denda = "lunas"
    p.tanggal_denda_selesai = date.today()
    p.denda_diproses_oleh = current_user.id
    db.session.commit()
    flash(f"Denda {format_rupiah(p.denda)} dari {p.anggota.nama_lengkap} dicatat LUNAS.", "success")
    return redirect(request.referrer or url_for("denda.daftar_denda"))


@denda_bp.route("/<int:peminjaman_id>/bebaskan", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def bebaskan(peminjaman_id):
    """Hapus denda tanpa pembayaran (mis. alasan khusus). Khusus kepala perpustakaan."""
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status_denda != "belum_lunas":
        flash("Denda ini tidak berstatus belum lunas.", "warning")
        return redirect(request.referrer or url_for("denda.daftar_denda"))

    p.status_denda = "dibebaskan"
    p.tanggal_denda_selesai = date.today()
    p.denda_diproses_oleh = current_user.id
    p.catatan_denda = request.form.get("catatan", "").strip()[:255] or None
    db.session.commit()
    flash(f"Denda {format_rupiah(p.denda)} dari {p.anggota.nama_lengkap} dibebaskan.", "success")
    return redirect(request.referrer or url_for("denda.daftar_denda"))


@denda_bp.route("/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_denda():
    status = request.args.get("status", "semua")
    daftar = _query_denda(status, "").order_by(Peminjaman.tanggal_kembali.desc()).all()
    baris = [
        [p.anggota.nama_lengkap, p.anggota.nim or p.anggota.username, p.buku.judul,
         p.tanggal_pinjam.strftime("%d-%m-%Y"), p.tanggal_jatuh_tempo.strftime("%d-%m-%Y"),
         p.tanggal_kembali.strftime("%d-%m-%Y") if p.tanggal_kembali else "-",
         p.hari_telat, p.denda, STATUS_LABEL.get(p.status_denda, p.status_denda),
         p.tanggal_denda_selesai.strftime("%d-%m-%Y") if p.tanggal_denda_selesai else "-"]
        for p in daftar
    ]
    buffer = buat_excel(
        "Denda",
        ["Mahasiswa", "NIM/Username", "Buku", "Tgl Pinjam", "Jatuh Tempo", "Tgl Kembali",
         "Hari Telat", "Denda (Rp)", "Status", "Tgl Lunas/Bebas"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True, download_name=f"laporan_denda_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

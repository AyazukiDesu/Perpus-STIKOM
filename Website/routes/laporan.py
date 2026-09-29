from datetime import date, timedelta

from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from sqlalchemy import and_, case, func

from extensions import db
from models import Buku, Peminjaman, User
from utils.decorators import role_required
from utils.denda import denda_peminjaman
from utils.excel_export import buat_excel

laporan_bp = Blueprint("laporan", __name__, url_prefix="/laporan")


@laporan_bp.route("/populer")
@login_required
@role_required("staf", "kepala_perpustakaan")
def buku_populer():
    hasil = (
        db.session.query(Buku, db.func.count(Peminjaman.id).label("jumlah_pinjam"))
        .join(Peminjaman, Peminjaman.buku_id == Buku.id)
        .group_by(Buku.id)
        .order_by(db.func.count(Peminjaman.id).desc())
        .limit(20)
        .all()
    )
    return render_template("laporan/populer.html", hasil=hasil)


@laporan_bp.route("/tidak-populer")
@login_required
@role_required("staf", "kepala_perpustakaan")
def buku_tidak_populer():
    # Buku yang tidak pernah dipinjam sama sekali
    subq = db.session.query(Peminjaman.buku_id).distinct().subquery()
    tidak_pernah = Buku.query.filter(~Buku.id.in_(subq)).order_by(Buku.judul).all()

    # Buku yang jarang dipinjam (dipinjam <= 2 kali), diurutkan paling jarang dulu
    jarang = (
        db.session.query(Buku, db.func.count(Peminjaman.id).label("jumlah_pinjam"))
        .join(Peminjaman, Peminjaman.buku_id == Buku.id)
        .group_by(Buku.id)
        .having(db.func.count(Peminjaman.id) <= 2)
        .order_by(db.func.count(Peminjaman.id).asc())
        .all()
    )
    return render_template("laporan/tidak_populer.html", tidak_pernah=tidak_pernah, jarang=jarang)


# ------------------------------------------------------------------
# STATISTIK MAHASISWA PALING SERING MEMINJAM
# ------------------------------------------------------------------
# Kunci -> (label tampilan, jumlah hari ke belakang; None = seluruh riwayat)
PERIODE_STATISTIK = {
    "semua": ("Semua waktu", None),
    "30": ("30 hari terakhir", 30),
    "90": ("90 hari terakhir", 90),
    "365": ("1 tahun terakhir", 365),
}

# Hanya peminjaman yang benar-benar terjadi. 'diajukan' (belum disetujui) dan
# 'ditolak' tidak dihitung sebagai aktivitas meminjam.
STATUS_DIHITUNG = ("dipinjam", "dikembalikan", "terlambat")


def statistik_mahasiswa_peminjam(kunci_periode="semua", limit=None):
    """Peringkat mahasiswa berdasarkan jumlah buku yang dipinjam.

    Kembalikan list dict berurut dari yang paling sering meminjam:
    user, total, judul_unik, sedang_dipinjam, terlambat, terakhir, peringkat.
    Urutan seri: yang lebih baru meminjam dulu, lalu nama A-Z.
    """
    if kunci_periode not in PERIODE_STATISTIK:
        kunci_periode = "semua"
    hari = PERIODE_STATISTIK[kunci_periode][1]

    hari_ini = date.today()
    # Padanan SQL dari Peminjaman.is_telat: sudah kembali tapi lewat tempo,
    # atau belum kembali dan hari ini sudah lewat tempo.
    telat = case(
        (and_(Peminjaman.status == "dikembalikan",
              Peminjaman.tanggal_kembali > Peminjaman.tanggal_jatuh_tempo), 1),
        (and_(Peminjaman.status == "dipinjam",
              Peminjaman.tanggal_jatuh_tempo < hari_ini), 1),
        else_=0,
    )
    sedang = case((Peminjaman.status == "dipinjam", 1), else_=0)

    q = (
        db.session.query(
            User,
            func.count(Peminjaman.id).label("total"),
            func.count(Peminjaman.buku_id.distinct()).label("judul_unik"),
            func.sum(sedang).label("sedang"),
            func.sum(telat).label("telat"),
            func.max(Peminjaman.tanggal_pinjam).label("terakhir"),
        )
        .join(Peminjaman, Peminjaman.user_id == User.id)
        .filter(User.role == "mahasiswa", Peminjaman.status.in_(STATUS_DIHITUNG))
    )
    if hari:
        q = q.filter(Peminjaman.tanggal_pinjam >= hari_ini - timedelta(days=hari))

    q = q.group_by(User.id).order_by(
        func.count(Peminjaman.id).desc(),
        func.max(Peminjaman.tanggal_pinjam).desc(),
        User.nama_lengkap.asc(),
    )
    if limit:
        q = q.limit(limit)

    hasil = []
    for user, total, judul_unik, sedang_n, telat_n, terakhir in q.all():
        hasil.append({
            "user": user,
            "total": int(total),
            "judul_unik": int(judul_unik),
            "sedang_dipinjam": int(sedang_n or 0),
            "terlambat": int(telat_n or 0),
            "terakhir": terakhir,
        })
    # Peringkat kompetisi: total yang sama -> peringkat sama (1, 2, 2, 4, ...).
    for i, baris in enumerate(hasil):
        if i > 0 and baris["total"] == hasil[i - 1]["total"]:
            baris["peringkat"] = hasil[i - 1]["peringkat"]
        else:
            baris["peringkat"] = i + 1
    return hasil


def _periode_dari_request():
    kunci = request.args.get("periode", "semua")
    return kunci if kunci in PERIODE_STATISTIK else "semua"


@laporan_bp.route("/mahasiswa-aktif")
@login_required
@role_required("staf", "kepala_perpustakaan")
def mahasiswa_aktif():
    """Mahasiswa yang paling sering meminjam buku (top 50)."""
    kunci = _periode_dari_request()
    hasil = statistik_mahasiswa_peminjam(kunci, limit=50)
    return render_template(
        "laporan/mahasiswa_aktif.html",
        hasil=hasil,
        periode=kunci,
        periode_opsi=PERIODE_STATISTIK,
        total_terbanyak=hasil[0]["total"] if hasil else 0,
    )


@laporan_bp.route("/mahasiswa-aktif/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_mahasiswa_aktif():
    kunci = _periode_dari_request()
    baris = [
        [b["peringkat"], b["user"].nama_lengkap, b["user"].nim or b["user"].username,
         b["total"], b["judul_unik"], b["sedang_dipinjam"], b["terlambat"],
         b["terakhir"].strftime("%d-%m-%Y") if b["terakhir"] else "-"]
        for b in statistik_mahasiswa_peminjam(kunci)
    ]
    buffer = buat_excel(
        "Mahasiswa Aktif",
        ["Peringkat", "Mahasiswa", "NIM/Username", "Total Dipinjam", "Judul Berbeda",
         "Sedang Dipinjam", "Kali Terlambat", "Terakhir Meminjam"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True,
        download_name=f"mahasiswa_aktif_{kunci}_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def _daftar_terlambat():
    semua = (
        Peminjaman.query.filter_by(status="dipinjam")
        .order_by(Peminjaman.tanggal_jatuh_tempo.asc())
        .all()
    )
    return sorted((p for p in semua if p.hari_telat > 0), key=lambda p: p.hari_telat, reverse=True)


@laporan_bp.route("/terlambat")
@login_required
@role_required("staf", "kepala_perpustakaan")
def buku_terlambat():
    """Semua buku yang sudah lewat jatuh tempo dan belum kembali, terlama di atas."""
    daftar = _daftar_terlambat()
    total_denda = sum(denda_peminjaman(p) for p in daftar)
    return render_template("laporan/terlambat.html", daftar=daftar, total_denda=total_denda)


@laporan_bp.route("/terlambat/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_terlambat():
    baris = [
        [p.anggota.nama_lengkap, p.anggota.nim or p.anggota.username, p.anggota.no_telepon or "-",
         p.buku.judul, p.tanggal_jatuh_tempo.strftime("%d-%m-%Y"), p.hari_telat, denda_peminjaman(p)]
        for p in _daftar_terlambat()
    ]
    buffer = buat_excel(
        "Terlambat",
        ["Mahasiswa", "NIM/Username", "No. Telepon", "Buku", "Jatuh Tempo", "Hari Telat", "Denda Berjalan (Rp)"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True, download_name=f"buku_terlambat_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

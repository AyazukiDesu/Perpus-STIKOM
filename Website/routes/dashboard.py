from datetime import date, timedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from extensions import db
from models import Buku, Peminjaman, User, Kategori

dashboard_bp = Blueprint("dashboard", __name__)

BULAN_ID = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def _enam_bulan_terakhir():
    """Kembalikan list (tahun, bulan) untuk 6 bulan terakhir, urut menaik, termasuk bulan ini."""
    awal_bulan_ini = date.today().replace(day=1)
    hasil = []
    for mundur in range(5, -1, -1):
        bulan = awal_bulan_ini.month - mundur
        tahun = awal_bulan_ini.year
        while bulan <= 0:
            bulan += 12
            tahun -= 1
        hasil.append((tahun, bulan))
    return hasil


def _data_grafik_peminjaman_bulanan():
    """Jumlah peminjaman per bulan, 6 bulan terakhir (untuk grafik garis/batang)."""
    bulan_list = _enam_bulan_terakhir()
    tahun_awal, bulan_awal = bulan_list[0]
    mulai = date(tahun_awal, bulan_awal, 1)

    baris = (
        db.session.query(
            func.date_format(Peminjaman.tanggal_pinjam, "%Y-%m").label("bulan_kunci"),
            func.count(Peminjaman.id),
        )
        .filter(Peminjaman.tanggal_pinjam >= mulai)
        .group_by("bulan_kunci")
        .all()
    )
    peta_jumlah = {kunci: jumlah for kunci, jumlah in baris}

    labels, data = [], []
    for tahun, bulan in bulan_list:
        kunci = f"{tahun:04d}-{bulan:02d}"
        labels.append(f"{BULAN_ID[bulan - 1]} {tahun}")
        data.append(peta_jumlah.get(kunci, 0))
    return labels, data


def _data_grafik_buku_terpopuler(limit=5):
    """Top N buku paling sering dipinjam (untuk grafik batang)."""
    hasil = (
        db.session.query(Buku.judul, func.count(Peminjaman.id).label("jumlah"))
        .join(Peminjaman, Peminjaman.buku_id == Buku.id)
        .group_by(Buku.id)
        .order_by(func.count(Peminjaman.id).desc())
        .limit(limit)
        .all()
    )
    labels = [judul for judul, _ in hasil]
    data = [jumlah for _, jumlah in hasil]
    return labels, data


def _data_grafik_distribusi_kategori():
    """Jumlah judul buku per kategori (untuk grafik donat)."""
    hasil = (
        db.session.query(Kategori.nama_kategori, func.count(Buku.id))
        .outerjoin(Buku, Buku.kategori_id == Kategori.id)
        .group_by(Kategori.id)
        .having(func.count(Buku.id) > 0)
        .order_by(func.count(Buku.id).desc())
        .all()
    )
    labels = [nama for nama, _ in hasil]
    data = [jumlah for _, jumlah in hasil]
    return labels, data


@dashboard_bp.route("/")
@login_required
def index():
    context = {}
    if current_user.is_anggota:
        pinjaman_aktif = Peminjaman.query.filter_by(
            user_id=current_user.id, status="dipinjam"
        ).all()
        context["pinjaman_aktif"] = pinjaman_aktif
        context["jumlah_terlambat_saya"] = sum(1 for p in pinjaman_aktif if p.is_telat)
    else:
        # staf & operator melihat ringkasan umum + grafik
        context["total_buku"] = Buku.query.count()
        context["total_stok"] = sum(b.stok for b in Buku.query.all())
        context["sedang_dipinjam"] = Peminjaman.query.filter_by(status="dipinjam").count()
        context["terlambat"] = sum(
            1 for p in Peminjaman.query.filter_by(status="dipinjam").all() if p.is_telat
        )

        # grafik: tren peminjaman 6 bulan terakhir
        labels_bulanan, data_bulanan = _data_grafik_peminjaman_bulanan()
        context["labels_grafik_bulanan"] = labels_bulanan
        context["data_grafik_bulanan"] = data_bulanan

        # grafik: buku paling sering dipinjam
        labels_top, data_top = _data_grafik_buku_terpopuler()
        context["labels_grafik_top_buku"] = labels_top
        context["data_grafik_top_buku"] = data_top

        # grafik: distribusi buku per kategori
        labels_kat, data_kat = _data_grafik_distribusi_kategori()
        context["labels_grafik_kategori"] = labels_kat
        context["data_grafik_kategori"] = data_kat

        # daftar penting: akan jatuh tempo dalam 3 hari ke depan
        batas_tempo = date.today() + timedelta(days=3)
        context["akan_jatuh_tempo"] = (
            Peminjaman.query.filter(
                Peminjaman.status == "dipinjam",
                Peminjaman.tanggal_jatuh_tempo >= date.today(),
                Peminjaman.tanggal_jatuh_tempo <= batas_tempo,
            )
            .order_by(Peminjaman.tanggal_jatuh_tempo.asc())
            .all()
        )

        # aktivitas terbaru
        context["peminjaman_terbaru"] = (
            Peminjaman.query.order_by(Peminjaman.id.desc()).limit(6).all()
        )

        if current_user.is_operator:
            context["total_anggota"] = User.query.filter_by(role="user").count()
            context["menunggu_persetujuan"] = User.query.filter_by(
                role="user", status_akun="pending"
            ).count()

    return render_template("dashboard.html", today=date.today(), **context)

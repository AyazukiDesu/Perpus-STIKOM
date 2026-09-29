"""Perhitungan denda keterlambatan."""
from datetime import date

from flask import current_app
from sqlalchemy import func

from extensions import db
from models import Peminjaman


def hitung_denda(jatuh_tempo, sampai, tarif, maks=0, tenggang=0):
    """Fungsi murni (mudah diuji).

    jatuh_tempo, sampai : date  -> 'sampai' = hari ini (masih dipinjam) atau tanggal kembali
    tarif               : Rp per hari
    maks                : batas atas denda (0 = tanpa batas)
    tenggang            : hari gratis setelah jatuh tempo
    """
    hari_kena_denda = (sampai - jatuh_tempo).days - tenggang
    if hari_kena_denda <= 0 or tarif <= 0:
        return 0
    total = hari_kena_denda * tarif
    if maks and total > maks:
        total = maks
    return total


def denda_dari_config(jatuh_tempo, sampai):
    c = current_app.config
    return hitung_denda(jatuh_tempo, sampai, c["DENDA_PER_HARI"], c["DENDA_MAKS"], c["MASA_TENGGANG_HARI"])


def denda_peminjaman(p):
    """Denda sebuah peminjaman saat ini.
    - dikembalikan : nilai yang sudah dibekukan saat pengembalian
    - dipinjam     : denda berjalan sampai hari ini
    - lainnya      : 0"""
    if p.status == "dikembalikan":
        return p.denda or 0
    if p.status == "dipinjam":
        return denda_dari_config(p.tanggal_jatuh_tempo, date.today())
    return 0


def total_denda_belum_lunas(user_id=None):
    """Jumlah denda yang sudah dibekukan tapi belum dibayar (semua anggota atau satu anggota)."""
    q = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "belum_lunas"
    )
    if user_id:
        q = q.filter(Peminjaman.user_id == user_id)
    return int(q.scalar() or 0)


def denda_berjalan_semua(user_id=None):
    """Total denda dari buku yang MASIH dipinjam dan sudah telat."""
    q = Peminjaman.query.filter_by(status="dipinjam")
    if user_id:
        q = q.filter_by(user_id=user_id)
    return sum(denda_peminjaman(p) for p in q.all())


def format_rupiah(angka):
    return "Rp " + f"{int(angka or 0):,}".replace(",", ".")

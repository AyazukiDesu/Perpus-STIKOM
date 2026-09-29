from datetime import timedelta

from flask import current_app

from models import Peminjaman
from utils.denda import denda_peminjaman, format_rupiah, total_denda_belum_lunas
from utils.kartu import terbitkan_kartu_jika_belum_ada


def lama_pinjam_untuk(buku, lama_hari=None):
    """Tentukan lama pinjam (hari): isian petugas > pengaturan khusus buku > pengaturan umum."""
    if lama_hari and lama_hari > 0:
        return lama_hari
    if buku is not None and buku.lama_pinjam_hari:
        return buku.lama_pinjam_hari
    return current_app.config["LAMA_PINJAM_HARI"]


def hitung_jatuh_tempo(buku, mulai, lama_hari=None):
    return mulai + timedelta(days=lama_pinjam_untuk(buku, lama_hari))


def cek_tunggakan(mahasiswa):
    """Jika pengaturan 'blokir jika ada denda' aktif: mahasiswa dengan buku terlambat
    atau denda belum lunas tidak boleh meminjam lagi."""
    if not current_app.config["BLOKIR_JIKA_DENDA"]:
        return True, None

    telat = [
        p for p in Peminjaman.query.filter_by(user_id=mahasiswa.id, status="dipinjam").all()
        if p.hari_telat > 0
    ]
    if telat:
        return False, (
            f"Masih ada {len(telat)} buku yang terlambat dikembalikan "
            f"(denda berjalan {format_rupiah(sum(denda_peminjaman(p) for p in telat))}). "
            "Kembalikan buku tersebut terlebih dahulu."
        )

    belum_lunas = total_denda_belum_lunas(mahasiswa.id)
    if belum_lunas > 0:
        return False, (
            f"Ada denda belum lunas sebesar {format_rupiah(belum_lunas)}. "
            "Lunasi denda di perpustakaan terlebih dahulu."
        )
    return True, None


def cek_kartu_valid(mahasiswa):
    """Kartu perpustakaan harus aktif dan belum kadaluarsa untuk bisa meminjam.
    Kembalikan (True, None) atau (False, pesan)."""
    kartu = terbitkan_kartu_jika_belum_ada(mahasiswa)
    if kartu.status != "aktif":
        return False, "Kartu perpustakaan tidak aktif. Hubungi staf/kepala perpustakaan."
    if kartu.is_kadaluarsa:
        return False, (
            f"Kartu perpustakaan sudah kadaluarsa pada {kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y')}. "
            "Minta staf/kepala perpustakaan untuk memperpanjang."
        )
    return True, None


def cek_kuota_pinjam(mahasiswa):
    """Maksimal Config.MAKS_PINJAM_PER_USER buku (diajukan + dipinjam) per mahasiswa."""
    maks = current_app.config["MAKS_PINJAM_PER_USER"]
    if mahasiswa.jumlah_pinjaman_aktif >= maks:
        return False, (
            f"Batas peminjaman tercapai: maksimal {maks} buku per mahasiswa "
            "(termasuk pengajuan yang masih menunggu). Kembalikan salah satu buku terlebih dahulu."
        )
    return True, None


def cek_bisa_meminjam(mahasiswa):
    """Gabungan validasi kartu + tunggakan denda + kuota. Kembalikan (True, None) atau (False, pesan)."""
    for cek in (cek_kartu_valid, cek_tunggakan, cek_kuota_pinjam):
        ok, pesan = cek(mahasiswa)
        if not ok:
            return False, pesan
    return True, None

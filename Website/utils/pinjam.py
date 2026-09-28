from flask import current_app

from utils.kartu import terbitkan_kartu_jika_belum_ada


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
    """Gabungan validasi kartu + kuota. Kembalikan (True, None) atau (False, pesan)."""
    for cek in (cek_kartu_valid, cek_kuota_pinjam):
        ok, pesan = cek(mahasiswa)
        if not ok:
            return False, pesan
    return True, None

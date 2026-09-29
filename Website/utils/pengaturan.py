"""Pengaturan perpustakaan yang bisa diubah kepala perpustakaan.

Nilai disimpan di tabel `pengaturan`. Sebelum tiap request diproses,
`terapkan_pengaturan()` menyalinnya ke app.config, sehingga seluruh kode lama
(mis. current_app.config["LAMA_PINJAM_HARI"]) otomatis memakai nilai terbaru.
Jika tabel belum ada / kosong, nilai awal dari config.py dipakai.
"""
from extensions import db
from models import Pengaturan

# kunci di DB -> (kunci di app.config, minimum, maksimum, label, satuan, bantuan)
DAFTAR = [
    ("lama_pinjam_hari", "LAMA_PINJAM_HARI", 1, 365, "Lama peminjaman standar", "hari",
     "Jatuh tempo otomatis = tanggal pinjam + angka ini. Bisa diganti per buku atau per transaksi."),
    ("maks_pinjam", "MAKS_PINJAM_PER_USER", 1, 50, "Maksimal buku per mahasiswa", "buku",
     "Pengajuan yang menunggu persetujuan ikut dihitung."),
    ("peringatan_hari", "PERINGATAN_JATUH_TEMPO_HARI", 0, 30, "Peringatan sebelum jatuh tempo", "hari",
     "Mulai menampilkan peringatan \"segera jatuh tempo\" sekian hari sebelumnya."),
    ("denda_per_hari", "DENDA_PER_HARI", 0, 1000000, "Denda per hari keterlambatan", "Rp",
     "Isi 0 untuk menonaktifkan denda."),
    ("denda_maks", "DENDA_MAKS", 0, 100000000, "Batas maksimal denda per buku", "Rp",
     "Isi 0 jika denda tidak dibatasi."),
    ("masa_tenggang_hari", "MASA_TENGGANG_HARI", 0, 30, "Masa tenggang tanpa denda", "hari",
     "Denda baru dihitung setelah lewat sekian hari dari jatuh tempo."),
    ("maks_perpanjang", "MAKS_PERPANJANG", 0, 20, "Maksimal perpanjangan per peminjaman", "kali",
     "Isi 0 untuk melarang perpanjangan."),
    ("blokir_jika_denda", "BLOKIR_JIKA_DENDA", 0, 1, "Blokir peminjaman jika ada denda", "0/1",
     "1 = mahasiswa yang punya denda belum lunas atau buku terlambat tidak bisa meminjam lagi. 0 = tidak diblokir."),
]


def terapkan_pengaturan(app):
    """Salin pengaturan dari DB ke app.config. Aman dipanggil sebelum tabel dibuat."""
    try:
        baris = {r.kunci: r.nilai for r in Pengaturan.query.all()}
    except Exception:
        db.session.rollback()
        return
    for kunci, kunci_config, *_ in DAFTAR:
        if kunci in baris:
            try:
                app.config[kunci_config] = int(baris[kunci])
            except ValueError:
                pass


def nilai_saat_ini(app):
    """Dict {kunci_db: nilai} yang sedang berlaku, untuk mengisi form Pengaturan."""
    return {kunci: app.config[kunci_config] for kunci, kunci_config, *_ in DAFTAR}


def simpan_pengaturan(data):
    """Simpan dict {kunci_db: int} ke tabel pengaturan (insert atau update)."""
    for kunci, nilai in data.items():
        baris = db.session.get(Pengaturan, kunci)
        if baris:
            baris.nilai = str(nilai)
        else:
            db.session.add(Pengaturan(kunci=kunci, nilai=str(nilai)))
    db.session.commit()

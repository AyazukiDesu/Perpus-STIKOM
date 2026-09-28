from datetime import date, timedelta

from flask import current_app

from extensions import db
from models import KartuAnggota, User


def validasi_nisn(nisn, wajib=True, abaikan_user_id=None):
    """Validasi NISN. Kembalikan (nisn_bersih_atau_None, pesan_error_atau_None).

    - wajib=True  : NISN harus diisi (dipakai untuk mahasiswa).
    - wajib=False : boleh kosong (staf / kepala perpustakaan) -> dikembalikan None.
    - Harus berupa angka dengan panjang Config.NISN_PANJANG (default 10 digit).
    - Harus unik di seluruh pengguna (abaikan_user_id dipakai saat edit).
    """
    nisn = (nisn or "").strip()
    if not nisn:
        if wajib:
            return None, "NISN wajib diisi."
        return None, None

    panjang = current_app.config["NISN_PANJANG"]
    if not nisn.isdigit() or len(nisn) != panjang:
        return None, f"NISN harus berupa {panjang} digit angka."

    q = User.query.filter(User.nisn == nisn)
    if abaikan_user_id:
        q = q.filter(User.id != abaikan_user_id)
    if q.first():
        return None, "NISN sudah terdaftar pada pengguna lain."
    return nisn, None


def terbitkan_kartu_jika_belum_ada(user):
    """Terbitkan kartu perpustakaan digital untuk user manapun (semua role)
    jika belum punya. ID kartu = NISN milik user (users.nisn)."""
    if user.kartu:
        return user.kartu
    kartu = KartuAnggota(
        user_id=user.id,
        tanggal_terbit=date.today(),
        tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config["MASA_BERLAKU_KARTU_HARI"]),
        status="aktif",
    )
    db.session.add(kartu)
    db.session.commit()
    return kartu

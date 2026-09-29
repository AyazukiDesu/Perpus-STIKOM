from datetime import date, timedelta

from flask import current_app

from extensions import db
from models import KartuAnggota, User


def validasi_nim(nim, wajib=True, abaikan_user_id=None):
    """Validasi NIM. Kembalikan (nim_bersih_atau_None, pesan_error_atau_None).

    - wajib=True  : NIM harus diisi (dipakai untuk mahasiswa).
    - wajib=False : boleh kosong (staf / kepala perpustakaan) -> dikembalikan None.
    - Harus berupa angka dengan panjang antara Config.NIM_PANJANG_MIN dan
      Config.NIM_PANJANG_MAKS (default 8-12 digit).
    - Harus unik di seluruh pengguna (abaikan_user_id dipakai saat edit).
    """
    nim = (nim or "").strip()
    if not nim:
        if wajib:
            return None, "NIM wajib diisi."
        return None, None

    p_min = current_app.config["NIM_PANJANG_MIN"]
    p_maks = current_app.config["NIM_PANJANG_MAKS"]
    if not nim.isdigit() or not (p_min <= len(nim) <= p_maks):
        rentang = f"{p_min}" if p_min == p_maks else f"{p_min}-{p_maks}"
        return None, f"NIM harus berupa {rentang} digit angka."

    q = User.query.filter(User.nim == nim)
    if abaikan_user_id:
        q = q.filter(User.id != abaikan_user_id)
    if q.first():
        return None, "NIM sudah terdaftar pada pengguna lain."
    return nim, None


def terbitkan_kartu_jika_belum_ada(user):
    """Terbitkan kartu perpustakaan digital untuk user manapun (semua role)
    jika belum punya. ID kartu = NIM milik user (users.nim)."""
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

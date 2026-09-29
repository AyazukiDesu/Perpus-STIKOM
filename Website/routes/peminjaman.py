from datetime import date, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user

from extensions import db
from models import Peminjaman, Buku, User
from utils.decorators import role_required
from utils.denda import denda_dari_config, format_rupiah
from utils.pinjam import cek_bisa_meminjam, cek_kartu_valid, hitung_jatuh_tempo, lama_pinjam_untuk

peminjaman_bp = Blueprint("peminjaman", __name__, url_prefix="/peminjaman")


# ------------------------------------------------------------------
# PENGAJUAN PEMINJAMAN OLEH ANGGOTA (role user, mandiri lewat sistem)
# ------------------------------------------------------------------
@peminjaman_bp.route("/ajukan/<int:buku_id>", methods=["POST"])
@login_required
@role_required("mahasiswa")
def ajukan_peminjaman(buku_id):
    buku = Buku.query.get_or_404(buku_id)

    if buku.stok <= 0:
        flash("Stok buku habis, pengajuan tidak dapat dibuat.", "danger")
        return redirect(url_for("buku.detail_buku", buku_id=buku_id))

    # cegah pengajuan ganda: anggota tidak boleh punya pengajuan/pinjaman aktif
    # untuk buku yang sama sebelum yang sebelumnya selesai (disetujui->dikembalikan, atau ditolak)
    aktif = Peminjaman.query.filter(
        Peminjaman.user_id == current_user.id,
        Peminjaman.buku_id == buku.id,
        Peminjaman.status.in_(["diajukan", "dipinjam"]),
    ).first()
    if aktif:
        flash("Anda sudah memiliki pengajuan/peminjaman aktif untuk buku ini.", "warning")
        return redirect(url_for("buku.detail_buku", buku_id=buku_id))

    # batas maksimal 2 buku per mahasiswa + kartu harus aktif/belum kadaluarsa
    ok, pesan = cek_bisa_meminjam(current_user)
    if not ok:
        flash(pesan, "danger")
        return redirect(url_for("buku.detail_buku", buku_id=buku_id))

    pengajuan = Peminjaman(
        user_id=current_user.id,
        buku_id=buku.id,
        tanggal_pinjam=date.today(),
        tanggal_jatuh_tempo=hitung_jatuh_tempo(buku, date.today()),
        status="diajukan",
    )
    db.session.add(pengajuan)
    db.session.commit()

    flash(f"Pengajuan peminjaman buku '{buku.judul}' berhasil dikirim, menunggu persetujuan staf/kepala perpustakaan.", "success")
    return redirect(url_for("buku.detail_buku", buku_id=buku_id))


@peminjaman_bp.route("/<int:peminjaman_id>/batalkan", methods=["POST"])
@login_required
@role_required("mahasiswa")
def batalkan_pengajuan(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.user_id != current_user.id:
        abort(403)
    if p.status != "diajukan":
        flash("Hanya pengajuan yang masih menunggu persetujuan yang dapat dibatalkan.", "warning")
        return redirect(url_for("peminjaman.riwayat_saya"))

    db.session.delete(p)
    db.session.commit()
    flash("Pengajuan peminjaman berhasil dibatalkan.", "success")
    return redirect(url_for("peminjaman.riwayat_saya"))


# ------------------------------------------------------------------
# TINJAU PENGAJUAN PEMINJAMAN (staf/kepala perpustakaan): setujui / tolak
# ------------------------------------------------------------------
@peminjaman_bp.route("/pengajuan")
@login_required
@role_required("staf", "kepala_perpustakaan")
def daftar_pengajuan():
    daftar = (
        Peminjaman.query.filter_by(status="diajukan")
        .order_by(Peminjaman.id.asc())
        .all()
    )
    return render_template(
        "peminjaman/pengajuan.html", daftar=daftar, today=date.today(),
        lama_pinjam_untuk=lama_pinjam_untuk,
    )


@peminjaman_bp.route("/<int:peminjaman_id>/setujui", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def setujui_pengajuan(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status != "diajukan":
        flash("Pengajuan ini sudah diproses sebelumnya.", "warning")
        return redirect(url_for("peminjaman.daftar_pengajuan"))

    if p.buku.stok <= 0:
        flash(f"Stok buku '{p.buku.judul}' habis, tidak bisa disetujui.", "danger")
        return redirect(url_for("peminjaman.daftar_pengajuan"))

    # kartu bisa saja dinonaktifkan/kadaluarsa sejak pengajuan dibuat
    # (kuota tidak dicek ulang: pengajuan ini sendiri sudah dihitung di kuota)
    ok, pesan = cek_kartu_valid(p.anggota)
    if not ok:
        flash(f"Tidak bisa disetujui untuk {p.anggota.nama_lengkap}: {pesan}", "danger")
        return redirect(url_for("peminjaman.daftar_pengajuan"))

    # petugas boleh mengisi lama pinjam sendiri; kosong = ikut pengaturan buku/umum
    lama_hari = request.form.get("lama_hari", type=int)
    p.status = "dipinjam"
    p.diproses_oleh = current_user.id
    p.tanggal_pinjam = date.today()
    p.tanggal_jatuh_tempo = hitung_jatuh_tempo(p.buku, date.today(), lama_hari)
    p.buku.stok -= 1
    db.session.commit()

    flash(
        f"Pengajuan '{p.buku.judul}' oleh {p.anggota.nama_lengkap} disetujui. "
        f"Jatuh tempo: {p.tanggal_jatuh_tempo.strftime('%d-%m-%Y')}.",
        "success",
    )
    return redirect(url_for("peminjaman.daftar_pengajuan"))


@peminjaman_bp.route("/<int:peminjaman_id>/tolak", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def tolak_pengajuan(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status != "diajukan":
        flash("Pengajuan ini sudah diproses sebelumnya.", "warning")
        return redirect(url_for("peminjaman.daftar_pengajuan"))

    p.status = "ditolak"
    p.diproses_oleh = current_user.id
    p.catatan = request.form.get("catatan", "").strip() or None
    db.session.commit()

    flash(f"Pengajuan '{p.buku.judul}' oleh {p.anggota.nama_lengkap} ditolak.", "success")
    return redirect(url_for("peminjaman.daftar_pengajuan"))


# ------------------------------------------------------------------
# PROSES PEMINJAMAN BARU (dilakukan oleh staf/kepala perpustakaan saat anggota datang)
# ------------------------------------------------------------------
@peminjaman_bp.route("/pinjam/<int:buku_id>", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def pinjam_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)

    if request.method == "POST":
        user_id = request.form.get("user_id", type=int)
        anggota = User.query.filter_by(id=user_id, role="mahasiswa").first()

        if not anggota:
            flash("Anggota tidak ditemukan.", "danger")
            return redirect(url_for("peminjaman.pinjam_buku", buku_id=buku_id))

        if buku.stok <= 0:
            flash("Stok buku habis, tidak bisa dipinjam.", "danger")
            return redirect(url_for("buku.detail_buku", buku_id=buku_id))

        # cek apakah anggota masih meminjam buku yang sama & belum kembali
        sudah_pinjam = Peminjaman.query.filter_by(
            user_id=anggota.id, buku_id=buku.id, status="dipinjam"
        ).first()
        if sudah_pinjam:
            flash(f"{anggota.nama_lengkap} masih meminjam buku ini dan belum mengembalikannya.", "warning")
            return redirect(url_for("peminjaman.pinjam_buku", buku_id=buku_id))

        ok, pesan = cek_bisa_meminjam(anggota)
        if not ok:
            flash(f"{anggota.nama_lengkap}: {pesan}", "danger")
            return redirect(url_for("peminjaman.pinjam_buku", buku_id=buku_id))

        lama_hari = request.form.get("lama_hari", type=int)
        peminjaman = Peminjaman(
            user_id=anggota.id,
            buku_id=buku.id,
            diproses_oleh=current_user.id,
            tanggal_pinjam=date.today(),
            tanggal_jatuh_tempo=hitung_jatuh_tempo(buku, date.today(), lama_hari),
            status="dipinjam",
        )
        buku.stok -= 1
        db.session.add(peminjaman)
        db.session.commit()

        flash(
            f"Buku '{buku.judul}' berhasil dipinjamkan ke {anggota.nama_lengkap}. "
            f"Jatuh tempo: {peminjaman.tanggal_jatuh_tempo.strftime('%d-%m-%Y')}.",
            "success",
        )
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    anggota_list = User.query.filter_by(role="mahasiswa", is_active_db=True).order_by(User.nama_lengkap).all()
    return render_template(
        "peminjaman/pinjam.html", buku=buku, anggota_list=anggota_list,
        lama_default=lama_pinjam_untuk(buku),
    )


# ------------------------------------------------------------------
# DAFTAR PEMINJAMAN AKTIF (staf/kepala perpustakaan) - dengan indikator terlambat
# ------------------------------------------------------------------
@peminjaman_bp.route("/")
@login_required
@role_required("staf", "kepala_perpustakaan")
def daftar_peminjaman():
    status_filter = request.args.get("status", "dipinjam")
    q = request.args.get("q", "").strip()

    query = Peminjaman.query
    if status_filter != "semua":
        query = query.filter_by(status=status_filter)
    if q:
        like = f"%{q}%"
        query = (
            query.join(User, Peminjaman.user_id == User.id)
            .join(Buku, Peminjaman.buku_id == Buku.id)
            .filter(
                db.or_(
                    User.nama_lengkap.ilike(like),
                    User.username.ilike(like),
                    Buku.judul.ilike(like),
                )
            )
        )
    daftar = query.order_by(Peminjaman.tanggal_pinjam.desc()).all()
    return render_template(
        "peminjaman/daftar.html", daftar=daftar, status_filter=status_filter, q=q, today=date.today()
    )


# ------------------------------------------------------------------
# PROSES PENGEMBALIAN
# ------------------------------------------------------------------
@peminjaman_bp.route("/<int:peminjaman_id>/kembalikan", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def kembalikan_buku(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status == "dikembalikan":
        flash("Buku ini sudah dikembalikan sebelumnya.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    if p.status != "dipinjam":
        flash("Hanya buku yang sedang dipinjam yang bisa dikembalikan.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    p.tanggal_kembali = date.today()
    p.status = "dikembalikan"

    # Denda dibekukan pada saat pengembalian (tarif yang berlaku hari ini).
    p.denda = denda_dari_config(p.tanggal_jatuh_tempo, p.tanggal_kembali)
    p.status_denda = "belum_lunas" if p.denda > 0 else "tidak_ada"
    p.buku.stok += 1

    if p.tanggal_kembali > p.tanggal_jatuh_tempo:
        hari_telat = (p.tanggal_kembali - p.tanggal_jatuh_tempo).days
        if p.denda > 0 and request.form.get("bayar") == "1":
            p.status_denda = "lunas"
            p.tanggal_denda_selesai = date.today()
            p.denda_diproses_oleh = current_user.id
            flash(
                f"Buku dikembalikan terlambat {hari_telat} hari. "
                f"Denda {format_rupiah(p.denda)} sudah dibayar lunas.", "success",
            )
        elif p.denda > 0:
            flash(
                f"Buku dikembalikan TERLAMBAT {hari_telat} hari. Denda {format_rupiah(p.denda)} "
                "belum dibayar — catat pembayarannya di menu Denda.", "warning",
            )
        else:
            flash(f"Buku dikembalikan terlambat {hari_telat} hari (masih dalam masa tenggang, tanpa denda).", "info")
    else:
        flash("Buku berhasil dikembalikan tepat waktu.", "success")

    db.session.commit()
    return redirect(url_for("peminjaman.daftar_peminjaman"))


# ------------------------------------------------------------------
# PERPANJANG & ATUR JATUH TEMPO
# ------------------------------------------------------------------
@peminjaman_bp.route("/<int:peminjaman_id>/perpanjang", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def perpanjang(peminjaman_id):
    """Perpanjang jatuh tempo dari tanggal jatuh tempo saat ini (bukan dari hari ini)."""
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status != "dipinjam":
        flash("Hanya peminjaman yang sedang berjalan yang bisa diperpanjang.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))
    if p.hari_telat > 0:
        flash("Buku sudah lewat jatuh tempo dan tidak bisa diperpanjang. Proses pengembalian terlebih dahulu.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    maks = current_app.config["MAKS_PERPANJANG"]
    if p.jumlah_perpanjang >= maks:
        flash(f"Batas perpanjangan tercapai (maksimal {maks} kali untuk satu peminjaman).", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    hari = request.form.get("hari", type=int) or lama_pinjam_untuk(p.buku)
    hari = max(1, min(hari, 365))
    p.tanggal_jatuh_tempo = p.tanggal_jatuh_tempo + timedelta(days=hari)
    p.jumlah_perpanjang += 1
    db.session.commit()

    flash(
        f"Jatuh tempo '{p.buku.judul}' diperpanjang {hari} hari menjadi "
        f"{p.tanggal_jatuh_tempo.strftime('%d-%m-%Y')} (perpanjangan ke-{p.jumlah_perpanjang}).",
        "success",
    )
    return redirect(request.referrer or url_for("peminjaman.daftar_peminjaman"))


@peminjaman_bp.route("/<int:peminjaman_id>/atur-jatuh-tempo", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def atur_jatuh_tempo(peminjaman_id):
    """Koreksi tanggal jatuh tempo secara langsung. Khusus kepala perpustakaan
    karena bisa mengubah besar denda."""
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status != "dipinjam":
        flash("Jatuh tempo hanya bisa diatur untuk peminjaman yang sedang berjalan.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    try:
        baru = date.fromisoformat(request.form.get("tanggal", ""))
    except ValueError:
        flash("Format tanggal tidak valid.", "danger")
        return redirect(url_for("peminjaman.daftar_peminjaman"))
    if baru < p.tanggal_pinjam:
        flash("Jatuh tempo tidak boleh lebih awal dari tanggal pinjam.", "danger")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    p.tanggal_jatuh_tempo = baru
    db.session.commit()
    flash(f"Jatuh tempo '{p.buku.judul}' diatur ke {baru.strftime('%d-%m-%Y')}.", "success")
    return redirect(request.referrer or url_for("peminjaman.daftar_peminjaman"))


# ------------------------------------------------------------------
# RIWAYAT PEMINJAMAN PER PESERTA (anggota lihat riwayat sendiri;
# staf/kepala perpustakaan bisa lihat riwayat anggota manapun)
# ------------------------------------------------------------------
@peminjaman_bp.route("/riwayat/saya")
@login_required
@role_required("mahasiswa")
def riwayat_saya():
    q = request.args.get("q", "").strip()
    query = Peminjaman.query.filter_by(user_id=current_user.id)
    if q:
        like = f"%{q}%"
        query = query.join(Buku, Peminjaman.buku_id == Buku.id).filter(Buku.judul.ilike(like))
    daftar = query.order_by(Peminjaman.id.desc()).all()
    return render_template(
        "peminjaman/riwayat_anggota.html", daftar=daftar, anggota=current_user,
        today=date.today(), bisa_batalkan=True, q=q,
    )


@peminjaman_bp.route("/riwayat/anggota/<int:user_id>")
@login_required
@role_required("staf", "kepala_perpustakaan")
def riwayat_anggota(user_id):
    anggota = User.query.get_or_404(user_id)
    q = request.args.get("q", "").strip()
    query = Peminjaman.query.filter_by(user_id=user_id)
    if q:
        like = f"%{q}%"
        query = query.join(Buku, Peminjaman.buku_id == Buku.id).filter(Buku.judul.ilike(like))
    daftar = query.order_by(Peminjaman.id.desc()).all()
    return render_template(
        "peminjaman/riwayat_anggota.html", daftar=daftar, anggota=anggota,
        today=date.today(), bisa_batalkan=False, q=q,
    )


# ------------------------------------------------------------------
# RIWAYAT PEMINJAMAN PER BUKU
# ------------------------------------------------------------------
@peminjaman_bp.route("/riwayat/buku/<int:buku_id>")
@login_required
@role_required("staf", "kepala_perpustakaan")
def riwayat_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    q = request.args.get("q", "").strip()
    query = Peminjaman.query.filter_by(buku_id=buku_id)
    if q:
        like = f"%{q}%"
        query = query.join(User, Peminjaman.user_id == User.id).filter(
            db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like))
        )
    daftar = query.order_by(Peminjaman.tanggal_pinjam.desc()).all()
    return render_template("peminjaman/riwayat_buku.html", daftar=daftar, buku=buku, today=date.today(), q=q)

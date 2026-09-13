from flask import Blueprint, render_template
from flask_login import login_required

from extensions import db
from models import Buku, Peminjaman
from utils.decorators import role_required

laporan_bp = Blueprint("laporan", __name__, url_prefix="/laporan")


@laporan_bp.route("/populer")
@login_required
@role_required("staf", "operator")
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
@role_required("staf", "operator")
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

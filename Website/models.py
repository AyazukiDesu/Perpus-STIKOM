from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db

# Label tampilan untuk tiap role (nilai di database tetap snake_case).
ROLE_LABEL = {
    "mahasiswa": "Mahasiswa",
    "staf": "Staf",
    "kepala_perpustakaan": "Kepala Perpustakaan",
}

# Status peminjaman yang dihitung sebagai "memakai kuota" pinjam.
STATUS_PINJAMAN_AKTIF = ("diajukan", "dipinjam")


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nama_lengkap = db.Column(db.String(150), nullable=False)
    # NISN (10 digit). Wajib untuk mahasiswa; opsional untuk staf/kepala perpustakaan.
    # NISN inilah yang dipakai sebagai nomor/ID kartu perpustakaan.
    nisn = db.Column(db.String(20), unique=True, nullable=True)
    role = db.Column(
        db.Enum("mahasiswa", "staf", "kepala_perpustakaan", name="role_enum"),
        nullable=False,
        default="mahasiswa",
    )
    no_telepon = db.Column(db.String(20))
    alamat = db.Column(db.String(255))
    is_active_db = db.Column("is_active", db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Status persetujuan akun oleh kepala perpustakaan.
    # - 'pending'   : baru daftar sendiri lewat form publik, menunggu ditinjau operator, BELUM bisa login.
    # - 'disetujui' : sudah diverifikasi operator (atau dibuat langsung oleh kepala perpustakaan/staf), bisa login normal.
    # - 'ditolak'   : ditolak operator, tidak bisa login.
    # Default 'disetujui' agar akun lama (sebelum fitur ini ada) & akun yang dibuat operator tidak terpengaruh/ter-blok.
    status_akun = db.Column(
        db.Enum("pending", "disetujui", "ditolak", name="status_akun_enum"),
        nullable=False,
        default="disetujui",
    )

    kartu = db.relationship("KartuAnggota", backref="pemilik", uselist=False, cascade="all, delete-orphan")
    peminjaman_list = db.relationship(
        "Peminjaman", foreign_keys="Peminjaman.user_id", backref="anggota", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # helper role
    @property
    def is_kepala(self):
        return self.role == "kepala_perpustakaan"

    @property
    def is_staf(self):
        return self.role == "staf"

    @property
    def is_mahasiswa(self):
        return self.role == "mahasiswa"

    @property
    def role_label(self):
        return ROLE_LABEL.get(self.role, self.role)

    # ---- kuota peminjaman ----
    @property
    def jumlah_pinjaman_aktif(self):
        """Jumlah buku yang sedang diajukan atau dipinjam (belum dikembalikan)."""
        return Peminjaman.query.filter(
            Peminjaman.user_id == self.id,
            Peminjaman.status.in_(STATUS_PINJAMAN_AKTIF),
        ).count()

    # helper status persetujuan
    @property
    def menunggu_persetujuan(self):
        return self.status_akun == "pending"

    @property
    def ditolak_operator(self):  # ditolak oleh kepala perpustakaan
        return self.status_akun == "ditolak"


class KartuAnggota(db.Model):
    __tablename__ = "kartu_anggota"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    tanggal_terbit = db.Column(db.Date, default=date.today)
    tanggal_kadaluarsa = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum("aktif", "nonaktif", name="status_kartu_enum"), default="aktif")

    @property
    def nisn(self):
        """ID kartu = NISN pemilik kartu (satu sumber data: users.nisn)."""
        return self.pemilik.nisn

    @property
    def is_kadaluarsa(self):
        return date.today() > self.tanggal_kadaluarsa

    @property
    def bisa_dipakai(self):
        """Kartu boleh dipakai meminjam jika berstatus aktif & belum kadaluarsa."""
        return self.status == "aktif" and not self.is_kadaluarsa


class Kategori(db.Model):
    __tablename__ = "kategori"

    id = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100), unique=True, nullable=False)

    buku_list = db.relationship("Buku", backref="kategori", lazy=True)


class Buku(db.Model):
    __tablename__ = "buku"

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    penulis = db.Column(db.String(150), nullable=False)
    penerbit = db.Column(db.String(150))
    tahun_terbit = db.Column(db.Integer)
    isbn = db.Column(db.String(30))
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))
    deskripsi = db.Column(db.Text)
    stok = db.Column(db.Integer, default=0)
    sampul_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    peminjaman_list = db.relationship("Peminjaman", backref="buku", cascade="all, delete-orphan")

    @property
    def total_dipinjam(self):
        return sum(1 for p in self.peminjaman_list)


class Peminjaman(db.Model):
    __tablename__ = "peminjaman"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    buku_id = db.Column(db.Integer, db.ForeignKey("buku.id"), nullable=False)
    diproses_oleh = db.Column(db.Integer, db.ForeignKey("users.id"))
    tanggal_pinjam = db.Column(db.Date, default=date.today)
    tanggal_jatuh_tempo = db.Column(db.Date, nullable=False)
    tanggal_kembali = db.Column(db.Date)
    # Alur status:
    #   'diajukan'     -> anggota mengajukan peminjaman sendiri, menunggu ditinjau staf/kepala perpustakaan.
    #   'dipinjam'     -> pengajuan disetujui (atau dipinjamkan langsung oleh staf/kepala perpustakaan di meja).
    #   'dikembalikan' -> buku sudah dikembalikan.
    #   'ditolak'      -> pengajuan ditolak staf/kepala perpustakaan.
    #   'terlambat'    -> (dihitung dinamis lewat is_telat, bukan disimpan sebagai status baris)
    status = db.Column(
        db.Enum("diajukan", "dipinjam", "dikembalikan", "terlambat", "ditolak", name="status_pinjam_enum"),
        default="dipinjam",
    )
    # Catatan opsional dari staf/kepala perpustakaan, biasanya diisi saat menolak pengajuan
    # agar anggota tahu alasannya.
    catatan = db.Column(db.String(255))

    @property
    def is_telat(self):
        if self.status in ("dikembalikan", "diajukan", "ditolak"):
            if self.status == "dikembalikan":
                return self.tanggal_kembali and self.tanggal_kembali > self.tanggal_jatuh_tempo
            return False
        return date.today() > self.tanggal_jatuh_tempo

    @property
    def is_diajukan(self):
        return self.status == "diajukan"

    @property
    def hari_menuju_jatuh_tempo(self):
        """Jumlah hari tersisa menuju jatuh tempo (negatif jika sudah lewat).
        Hanya relevan untuk peminjaman yang sedang berjalan ('dipinjam')."""
        if self.status != "dipinjam":
            return None
        return (self.tanggal_jatuh_tempo - date.today()).days

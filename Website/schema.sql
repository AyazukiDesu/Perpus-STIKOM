-- =====================================================================
-- SCHEMA DATABASE - APLIKASI PERPUSTAKAAN
-- Jalankan file ini setelah membuat database (lihat README.md)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS perpustakaan_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE perpustakaan_db;

-- ---------------------------------------------------------------------
-- TABEL USERS (menyimpan semua role: mahasiswa, staf, kepala_perpustakaan)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    -- NIM (Nomor Induk Mahasiswa) = ID kartu perpustakaan. Wajib untuk mahasiswa (divalidasi di aplikasi),
    -- boleh NULL untuk staf/kepala perpustakaan.
    nim VARCHAR(20) DEFAULT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(150) NOT NULL,
    role ENUM('mahasiswa', 'staf', 'kepala_perpustakaan') NOT NULL DEFAULT 'mahasiswa',
    no_telepon VARCHAR(20) DEFAULT NULL,
    alamat VARCHAR(255) DEFAULT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    -- status persetujuan akun oleh operator: 'pending' (baru daftar sendiri, belum bisa login),
    -- 'disetujui' (bisa login normal), 'ditolak' (ditolak operator).
    -- Default 'disetujui' supaya tidak mengganggu akun yang sudah ada / dibuat langsung oleh operator.
    status_akun ENUM('pending', 'disetujui', 'ditolak') NOT NULL DEFAULT 'disetujui',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABEL KARTU ANGGOTA (kartu perpus digital, 1-1 dengan user; ID kartu = users.nim)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kartu_anggota (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    tanggal_terbit DATE NOT NULL,
    tanggal_kadaluarsa DATE NOT NULL,
    status ENUM('aktif', 'nonaktif') NOT NULL DEFAULT 'aktif',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABEL KATEGORI BUKU
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kategori (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_kategori VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABEL BUKU
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS buku (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    penulis VARCHAR(150) NOT NULL,
    penerbit VARCHAR(150) DEFAULT NULL,
    tahun_terbit YEAR DEFAULT NULL,
    isbn VARCHAR(30) DEFAULT NULL,
    kategori_id INT DEFAULT NULL,
    deskripsi TEXT DEFAULT NULL,
    stok INT NOT NULL DEFAULT 0,
    sampul_path VARCHAR(255) DEFAULT NULL,
    lokasi_rak VARCHAR(50) DEFAULT NULL,          -- mis. "Rak A-3"
    lama_pinjam_hari INT DEFAULT NULL,            -- lama pinjam khusus buku ini; NULL = ikut pengaturan umum
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kategori_id) REFERENCES kategori(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABEL PEMINJAMAN (sekaligus jadi riwayat peminjaman)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS peminjaman (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    buku_id INT NOT NULL,
    diproses_oleh INT DEFAULT NULL, -- staf/kepala perpustakaan yang memproses
    tanggal_pinjam DATE NOT NULL,
    tanggal_jatuh_tempo DATE NOT NULL,
    tanggal_kembali DATE DEFAULT NULL,
    -- 'diajukan'  : anggota mengajukan sendiri lewat sistem pengajuan peminjaman, menunggu ditinjau.
    -- 'dipinjam'  : pengajuan disetujui / dipinjamkan langsung oleh staf-operator.
    -- 'ditolak'   : pengajuan ditolak staf/kepala perpustakaan.
    status ENUM('diajukan', 'dipinjam', 'dikembalikan', 'terlambat', 'ditolak') NOT NULL DEFAULT 'dipinjam',
    catatan VARCHAR(255) DEFAULT NULL, -- catatan staf/kepala perpustakaan, biasanya alasan penolakan
    -- Denda keterlambatan: diisi (dibekukan) saat buku dikembalikan.
    denda INT NOT NULL DEFAULT 0,
    status_denda ENUM('tidak_ada', 'belum_lunas', 'lunas', 'dibebaskan') NOT NULL DEFAULT 'tidak_ada',
    tanggal_denda_selesai DATE DEFAULT NULL,      -- tanggal dibayar / dibebaskan
    denda_diproses_oleh INT DEFAULT NULL,
    catatan_denda VARCHAR(255) DEFAULT NULL,
    jumlah_perpanjang INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (buku_id) REFERENCES buku(id) ON DELETE CASCADE,
    FOREIGN KEY (diproses_oleh) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (denda_diproses_oleh) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABEL PENGATURAN (diubah kepala perpustakaan lewat menu Pengaturan)
-- Kosong pun tidak apa-apa: nilai awal diambil dari config.py.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pengaturan (
    kunci VARCHAR(50) PRIMARY KEY,
    nilai VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABEL LOG STOK (riwayat perubahan stok manual)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS log_stok (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buku_id INT NOT NULL,
    user_id INT DEFAULT NULL,
    perubahan INT NOT NULL,
    stok_sesudah INT NOT NULL,
    alasan VARCHAR(100) NOT NULL,
    waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buku_id) REFERENCES buku(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- DATA AWAL (opsional) - akun kepala perpustakaan default
-- Password default: "operator123" (WAJIB diganti setelah login pertama)
-- Hash di bawah dibuat dengan werkzeug.security.generate_password_hash
-- ---------------------------------------------------------------------
-- Catatan: hash contoh TIDAK disertakan di sini karena hash berbeda tiap
-- generate. Gunakan script `python seed_admin.py` (disertakan dalam paket)
-- untuk membuat akun kepala perpustakaan pertama secara otomatis & aman.

-- ---------------------------------------------------------------------
-- INDEX TAMBAHAN untuk pencarian & laporan lebih cepat
-- ---------------------------------------------------------------------
CREATE INDEX idx_buku_judul ON buku(judul);
CREATE INDEX idx_buku_penulis ON buku(penulis);
CREATE INDEX idx_peminjaman_status ON peminjaman(status);
CREATE INDEX idx_peminjaman_user ON peminjaman(user_id);
CREATE INDEX idx_peminjaman_buku ON peminjaman(buku_id);
CREATE INDEX idx_peminjaman_status_denda ON peminjaman(status_denda);
CREATE INDEX idx_log_stok_buku ON log_stok(buku_id);

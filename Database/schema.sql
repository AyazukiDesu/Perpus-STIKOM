-- =====================================================================
-- SCHEMA DATABASE - APLIKASI PERPUSTAKAAN
-- Jalankan file ini setelah membuat database (lihat README.md)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS perpustakaan_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE perpustakaan_db;

-- ---------------------------------------------------------------------
-- TABEL USERS (menyimpan semua role: user/anggota, staf, operator)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(150) NOT NULL,
    role ENUM('user', 'staf', 'operator') NOT NULL DEFAULT 'user',
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
-- TABEL KARTU ANGGOTA (kartu perpus digital, 1-1 dengan user role 'user')
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kartu_anggota (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    nomor_kartu VARCHAR(30) NOT NULL UNIQUE,
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
    diproses_oleh INT DEFAULT NULL, -- staf/operator yang memproses
    tanggal_pinjam DATE NOT NULL,
    tanggal_jatuh_tempo DATE NOT NULL,
    tanggal_kembali DATE DEFAULT NULL,
    -- 'diajukan'  : anggota mengajukan sendiri lewat sistem pengajuan peminjaman, menunggu ditinjau.
    -- 'dipinjam'  : pengajuan disetujui / dipinjamkan langsung oleh staf-operator.
    -- 'ditolak'   : pengajuan ditolak staf/operator.
    status ENUM('diajukan', 'dipinjam', 'dikembalikan', 'terlambat', 'ditolak') NOT NULL DEFAULT 'dipinjam',
    catatan VARCHAR(255) DEFAULT NULL, -- catatan staf/operator, biasanya alasan penolakan
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (buku_id) REFERENCES buku(id) ON DELETE CASCADE,
    FOREIGN KEY (diproses_oleh) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- DATA AWAL (opsional) - akun operator default
-- Password default: "operator123" (WAJIB diganti setelah login pertama)
-- Hash di bawah dibuat dengan werkzeug.security.generate_password_hash
-- ---------------------------------------------------------------------
-- Catatan: hash contoh TIDAK disertakan di sini karena hash berbeda tiap
-- generate. Gunakan script `python seed_admin.py` (disertakan dalam paket)
-- untuk membuat akun operator pertama secara otomatis & aman.

-- ---------------------------------------------------------------------
-- INDEX TAMBAHAN untuk pencarian & laporan lebih cepat
-- ---------------------------------------------------------------------
CREATE INDEX idx_buku_judul ON buku(judul);
CREATE INDEX idx_buku_penulis ON buku(penulis);
CREATE INDEX idx_peminjaman_status ON peminjaman(status);
CREATE INDEX idx_peminjaman_user ON peminjaman(user_id);
CREATE INDEX idx_peminjaman_buku ON peminjaman(buku_id);

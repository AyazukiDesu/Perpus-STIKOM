# Aplikasi Perpustakaan (Flask + MySQL)

Aplikasi web manajemen perpustakaan yang berjalan di komputer lokal (local server),
dengan 3 role: **user (anggota)**, **staf**, **operator**.

## 1. Persiapan Database MySQL

1. Pastikan MySQL Server sudah terinstall dan berjalan di komputer Anda.
2. Buka MySQL client (bisa lewat terminal `mysql -u root -p`, atau tools seperti
   phpMyAdmin/HeidiSQL/MySQL Workbench).
3. Jalankan file `schema.sql` yang sudah disediakan:

   ```bash
   mysql -u root -p < schema.sql
   ```

   Perintah ini akan otomatis membuat database `perpustakaan_db` beserta seluruh
   tabel yang dibutuhkan (users, kartu_anggota, kategori, buku, peminjaman).

4. (Opsional) Jika ingin memverifikasi tabel sudah terbuat:
   ```sql
   USE perpustakaan_db;
   SHOW TABLES;
   ```

## 2. Persiapan Environment Python

1. Buat virtual environment (disarankan):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

2. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```

3. Salin file konfigurasi environment:
   ```bash
   cp .env.example .env      # Mac/Linux
   copy .env.example .env    # Windows
   ```
   Lalu buka `.env` dan sesuaikan `DB_USER`, `DB_PASSWORD`, dan `DB_NAME` dengan
   konfigurasi MySQL lokal Anda.

## 3. Membuat Akun Operator Pertama

Karena registrasi publik hanya untuk role "user", akun **operator** pertama harus
dibuat lewat script berikut:

```bash
python seed_admin.py
```

Ikuti instruksi di terminal (username, email, nama, password).

## 4. Menjalankan Aplikasi

```bash
python app.py
```

Buka browser ke: **http://127.0.0.1:5000**

## 5. Alur Testing Bertahap (sesuai urutan pembangunan fitur)

### Tahap 1 — Login, Registrasi & Role
1. Buka `/auth/register` → daftar sebagai anggota baru → cek berhasil login.
2. Login sebagai operator (akun dari `seed_admin.py`) → masuk menu
   **Manajemen Pengguna** → tambah akun staf.
3. Logout, login sebagai staf → perhatikan menu yang muncul berbeda dari operator
   dan dari anggota (role-based menu).
4. Sebagai anggota, buka menu **Kartu Anggota** → kartu digital otomatis
   muncul (dibuat otomatis saat registrasi).

### Tahap 2 — Manajemen Buku
1. Login sebagai staf/operator → menu **Buku** → **+ Tambah Buku** → isi data
   + upload gambar sampul → simpan → cek sampul tampil di daftar buku.
2. Coba **Kategori** → tambah beberapa kategori (misal: Fiksi, Sains, Sejarah).
3. Coba **Import Excel**:
   - Klik "Unduh Template Excel" → isi beberapa baris data buku.
   - Upload kembali file tersebut → cek buku baru otomatis masuk ke database.

### Tahap 3 — Peminjaman & Pengembalian
1. Sebagai staf/operator, dari daftar buku klik **Pinjamkan** pada buku yang
   stoknya > 0 → pilih anggota → proses.
2. Cek menu **Peminjaman** → buku yang baru dipinjam muncul dengan tanggal
   jatuh tempo (default 7 hari, bisa diubah di `config.py` -> `LAMA_PINJAM_HARI`).
3. Klik **Kembalikan** → jika tanggal hari ini sudah melewati jatuh tempo,
   sistem otomatis menghitung denda keterlambatan.
4. Sebagai anggota, cek menu **Riwayat Peminjaman** → riwayat pribadi muncul.
5. Sebagai staf/operator, dari halaman detail buku klik **Riwayat Peminjaman**
   → riwayat per buku muncul.

### Tahap 4 — Pencarian & Laporan
1. Menu **Buku** → gunakan kolom pencarian (judul/penulis/ISBN) dan filter
   kategori.
2. Menu **Buku Populer** → menampilkan buku dengan jumlah peminjaman terbanyak.
3. Menu **Buku Tidak Populer** → menampilkan buku yang belum pernah dipinjam,
   dan buku yang jarang dipinjam (≤2 kali).

## 6. Struktur Proyek

```
perpustakaan_app/
├── app.py                  # entry point Flask (application factory)
├── config.py                # konfigurasi (baca dari .env)
├── extensions.py             # inisialisasi db & login_manager
├── models.py                  # model SQLAlchemy (User, Buku, dll)
├── schema.sql                  # skema database MySQL
├── seed_admin.py                # script buat akun operator pertama
├── requirements.txt
├── .env.example
├── routes/
│   ├── auth.py               # login, registrasi, manajemen pengguna
│   ├── dashboard.py          # dashboard sesuai role
│   ├── buku.py               # manajemen buku, kategori, import excel
│   ├── peminjaman.py         # pinjam, kembalikan, riwayat
│   ├── laporan.py            # statistik buku populer/tidak populer
│   └── kartu.py              # kartu anggota digital
├── templates/                # Jinja2 templates
├── static/
│   ├── css/style.css
│   └── uploads/sampul/       # tempat penyimpanan sampul buku yang diupload
└── utils/
    ├── decorators.py         # role_required decorator
    └── excel_import.py       # generate template & proses import excel
```

## 7. Catatan Keamanan (untuk penggunaan lokal)

- Password disimpan ter-hash (werkzeug `generate_password_hash`), tidak plain text.
- `SECRET_KEY` di `.env` sebaiknya diganti string acak yang panjang.
- Aplikasi ini didesain untuk dijalankan di jaringan lokal/komputer pribadi,
  bukan untuk dipublikasikan langsung ke internet tanpa pengamanan tambahan
  (HTTPS, rate limiting, dsb).

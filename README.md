**DOKUMENTASI TEKNIS**

**Perpus STIKOM --- Aplikasi Perpustakaan Berbasis Flask dan MySQL**

*Panduan setup, pemakaian, dan penjelasan kode untuk pemula* · Versi 6 — Panduan Rekonstruksi ·
22 Oktober 2026

------------------------------------------------------------------------

## Daftar Isi

**BAGIAN I --- PENGANTAR**

-   BAB 1 --- Gambaran Umum Proyek
-   BAB 2 --- Konsep Dasar untuk Pemula

**BAGIAN II --- INSTALASI DAN PENGGUNAAN**

-   BAB 3 --- Instalasi dan Setup
-   BAB 4 --- Panduan Pemakaian per Role
-   BAB 5 --- Peta URL Aplikasi

**BAGIAN III --- DATABASE**

-   BAB 6 --- Struktur Database (schema.sql)

**BAGIAN IV --- PENJELASAN KODE**

-   BAB 7 --- Alur Kerja Satu Request
-   BAB 8 --- Inti Aplikasi (app.py)
-   BAB 9 --- Konfigurasi, Ekstensi, dan Model
-   BAB 10 --- Autentikasi dan Manajemen Pengguna
-   BAB 11 --- Manajemen Data Buku
-   BAB 12 --- Alur Peminjaman Buku
-   BAB 13 --- Dashboard
-   BAB 14 --- Laporan
-   BAB 15 --- Kartu Anggota
-   BAB 16 --- Denda dan Pengaturan
-   BAB 17 --- Fungsi Bantu (utils)
-   BAB 18 --- Skrip Akun Awal (seed_admin.py)

**BAGIAN V --- LAMPIRAN**

-   BAB 19 --- Template, CSS, dan Front-End
-   BAB 20 --- Troubleshooting
-   BAB 21 --- Catatan Konsistensi Dokumen Lama
-   LAMPIRAN A --- Catatan Temuan dan Keamanan
-   LAMPIRAN B --- Glosarium

------------------------------------------------------------------------

**Tentang Dokumen Ini**

> **Pembaruan versi 6:** dokumentasi ini ditambah katalog bedah kode
> untuk setiap fungsi/metode Python yang ditemukan dalam ZIP. Penjelasan
> baris-per-baris merujuk pada nomor baris file asli; kode tidak diubah
> oleh proses dokumentasi ini.

Dokumen ini menjelaskan aplikasi web **Perpus STIKOM** secara bertahap:
mulai dari gambaran umum, cara memasang dan memakai, struktur database,
sampai penjelasan fungsi secara menyeluruh dan panduan membangun ulang aplikasi. Disusun agar pemula bisa
belajar dari atas ke bawah tanpa melompat-lompat.

**Cocok untuk:** mahasiswa/pemula yang baru belajar Flask, calon
pengelola sistem, dan pengembang yang akan melanjutkan proyek. **Yang
sebaiknya sudah diketahui:** dasar Python (fungsi, class, dictionary)
dan HTML sederhana. SQL dijelaskan di Bab 6.

### Cara Membaca

-   Nomor `baris X–Y` merujuk ke nomor baris pada file kode aslinya.
-   Kotak kutipan di awal bab berisi **Tujuan belajar**, **Prasyarat**,
    dan di akhir bab **Ringkasan bab**.
-   `Teks berformat kode` adalah nama file, fungsi, variabel, atau
    perintah.
-   Tabel dipakai untuk perbandingan atau daftar; poin berurutan dipakai
    untuk langkah.
-   Buka file kodenya di editor di samping dokumen ini agar mudah
    mencocokkan nomor baris.

### Jalur Belajar yang Disarankan

  Langkah   Kegiatan                                              Bab
  --------- ----------------------------------------------------- ------------------
  1         Kenali proyek dan istilah dasar                       1--2
  2         Pasang, jalankan, dan coba tiap role                  3--5
  3         Pahami struktur database                              6
  4         Pelajari alur request, lalu inti aplikasi dan model   7--9
  5         Baca route per fitur sesuai minat                     10--16
  6         Pelajari fungsi bantu dan akun awal                   17--18
  7         Rujuk template, troubleshooting, dan glosarium        19--20, Lampiran

------------------------------------------------------------------------

# BAGIAN I --- PENGANTAR

## BAB 1 --- Gambaran Umum Proyek

> **Tujuan belajar:** Mengenal apa itu Perpus STIKOM, siapa penggunanya,
> fitur, dan strukturnya.\
> **Prasyarat:** -

**Perpus STIKOM** adalah aplikasi web perpustakaan berbasis **Flask +
MySQL** yang berjalan di server lokal (`http://127.0.0.1:5000`,
dijalankan lewat `run.bat`). Pola yang dipakai: *application factory* +
*blueprint* + SQLAlchemy ORM + Flask-Login.

### 1.1 Role Pengguna

  ---------------------------------------------------------------------
  Role                               Kemampuan utama
  ---------------------------------- ----------------------------------
  `mahasiswa`                        Daftar mandiri (menunggu
                                     persetujuan), cari buku, ajukan
                                     peminjaman, lihat riwayat & kartu
                                     sendiri

  `staf`                             Kelola buku, setujui/tolak
                                     pengajuan, pinjamkan langsung,
                                     proses pengembalian, kelola kartu
                                     & denda, laporan

  `kepala_perpustakaan`              Semua kemampuan staf + kelola
                                     pengguna, setujui akun baru, ubah
                                     pengaturan sistem
  ---------------------------------------------------------------------

### 1.2 Fitur

Login/registrasi + persetujuan akun · manajemen buku (stok, kategori,
sampul, import/ekspor Excel) · peminjaman (pengajuan → persetujuan →
dipinjam → kembali) · perpanjangan & jatuh tempo · denda otomatis ·
kartu anggota digital + cetak · laporan (populer, tidak populer,
mahasiswa aktif, terlambat) · dashboard grafik · pengaturan dinamis dari
database.

### 1.3 Struktur Folder

    Perpus-STIKOM/
    ├── run.bat                 # buka browser + jalankan app
    ├── README.md               # daftar kebutuhan & fitur
    ├── Database/               # schema.sql + data_dummy_buku_1000.xlsx
    ├── Informasi/Teknis.md     # panduan instalasi & testing
    └── Website/
        ├── app.py              # inti aplikasi (Bab 8)
        ├── config.py, extensions.py, models.py   (Bab 9)
        ├── routes/             # auth, buku, peminjaman, dashboard, laporan, kartu, denda, pengaturan (Bab 10–16)
        ├── utils/              # decorators, pengaturan, denda, pinjam, kartu, excel_* (Bab 17)
        ├── seed_admin.py       # buat akun kepala pertama (Bab 18)
        ├── templates/          # 30 file HTML Jinja2 (Bab 19)
        ├── requirements.txt, schema.sql, .env

### 1.4 Database (7 tabel)

`users`, `kartu_anggota`, `kategori`, `buku`, `peminjaman`,
`pengaturan`, `log_stok`.

### 1.5 Teknologi

Flask 3.0.3 · Flask-SQLAlchemy 3.1.1 · Flask-Login 0.6.3 ·
mysql-connector-python 8.4.0 · python-dotenv · openpyxl 3.1.5 · Werkzeug
3.0.3.

### 1.6 Alur Utama Peminjaman

1.  Mahasiswa mengajukan buku (status `diajukan`) → 2. Staf menyetujui
    (`dipinjam`, jatuh tempo dihitung) atau menolak → 3. Bisa
    diperpanjang (maks. sesuai pengaturan) → 4. Dikembalikan
    (`dikembalikan`, denda dibekukan jika telat) → 5. Denda
    dilunasi/dibebaskan. Validasi sebelum meminjam: kartu aktif & belum
    kadaluarsa, tidak ada tunggakan denda, kuota belum penuh.

> **Ringkasan bab:** Aplikasi Flask+MySQL dengan 3 role, 7 tabel, dan
> alur peminjaman dari pengajuan sampai denda.

## BAB 2 --- Konsep Dasar untuk Pemula

> **Tujuan belajar:** Memahami istilah dasar (Flask, ORM, blueprint,
> session, dll.) agar bab kode mudah diikuti.\
> **Prasyarat:** Bab 1

### 2.1 Daftar Konsep

-   **Flask**: kerangka web Python ringan. Setiap alamat URL dipetakan
    ke sebuah fungsi (*route*).
-   **Application factory** (`create_app`): aplikasi dibuat di dalam
    fungsi, sehingga mudah diuji dan terhindar dari impor melingkar.
-   **Blueprint**: modul route per fitur (auth, buku, dst.) yang
    didaftarkan ke aplikasi utama.
-   **ORM / SQLAlchemy**: tabel database ditulis sebagai *class* Python
    (`models.py`); query memakai `User.query.filter_by(...)` alih-alih
    SQL mentah.
-   **Session & Flask-Login**: setelah login, ID user disimpan di cookie
    ter-tanda-tangan (memakai `SECRET_KEY`). `current_user` memberi
    akses ke user aktif di setiap request.
-   **Hash password**: password tidak disimpan asli; `set_password`
    menyimpan hash Werkzeug, `check_password` membandingkan.
-   **Decorator** (`@login_required`, `@role_required(...)`):
    "pembungkus" yang memeriksa hak akses sebelum fungsi route berjalan.
-   **Jinja2**: mesin template HTML (`{{ variabel }}`, `{% if %}`,
    `{% for %}`, filter `|rupiah`).
-   **Context processor**: variabel yang otomatis tersedia di semua
    template (jumlah pending, tahun).
-   **Flash message**: pesan singkat (sukses/error) yang tampil sekali
    setelah redirect.
-   **PRG (Post/Redirect/Get)**: setelah form `POST` berhasil, server
    mengarahkan (`redirect`) ke halaman lain agar refresh tidak mengirim
    ulang form.
-   **Foreign key & CASCADE**: relasi antar tabel; mis. hapus user
    otomatis menghapus kartu & peminjamannya.
-   **`.env`**: berisi rahasia/konfigurasi yang dibaca `python-dotenv`
    supaya tidak ditulis di kode.

> **Ringkasan bab:** Istilah di bab ini akan terus muncul di penjelasan
> kode; kembali ke sini bila bingung.

# BAGIAN II --- INSTALASI DAN PENGGUNAAN

## BAB 3 --- Instalasi dan Setup

> **Tujuan belajar:** Memasang dan menjalankan aplikasi dari nol di
> Windows.\
> **Prasyarat:** Bab 1

### 3.1 Yang harus terpasang

-   **Python 3.10+** (centang "Add Python to PATH" saat instal).
-   **MySQL Server** (bisa lewat XAMPP/Laragon/MySQL Installer) + client
    seperti phpMyAdmin/HeidiSQL/Workbench.

### 3.2 Langkah demi langkah

1.  **Ekstrak** `Perpus-STIKOM.zip`.

2.  **Buat database.** Jalankan file **`Website/schema.sql`** (bukan
    `Database/schema.sql`, lihat Bab 6):

    -   lewat terminal: `mysql -u root -p < Website/schema.sql`
    -   atau lewat phpMyAdmin/HeidiSQL: tab SQL → tempel isi file →
        jalankan. Hasilnya: database `perpustakaan_db` + 7 tabel +
        index.

3.  **Virtual environment** (opsional tapi disarankan), di folder
    `Website`:

        python -m venv venv
        venv\Scripts\activate
        pip install -r requirements.txt

4.  **Isi file `.env`** di folder `Website/` (README menyebut
    `.env.example`, tetapi file itu tidak ada di zip, jadi buat/ubah
    `.env` langsung): \| Kunci \| Isi contoh \| Arti \|
    \|---\|---\|---\| \| `DB_HOST` \| `localhost` \| alamat server MySQL
    \| \| `DB_PORT` \| `3306` \| port MySQL \| \| `DB_USER` \| `root` \|
    user MySQL \| \| `DB_PASSWORD` \| (password Anda) \| boleh kosong
    jika MySQL tanpa password \| \| `DB_NAME` \| `perpustakaan_db` \|
    nama database dari schema \| \| `SECRET_KEY` \| teks acak panjang \|
    kunci penanda session login; **wajib diganti** \| \| `UPLOAD_FOLDER`
    *(opsional)* \| `static/uploads/sampul` \| folder sampul buku \| \|
    `MAX_CONTENT_LENGTH_MB` *(opsional)* \| `5` \| batas ukuran upload
    (MB) \|

5.  **Buat akun kepala perpustakaan pertama** (dari folder `Website`):
    `python seed_admin.py`, isi username, email, nama, password.

6.  **Jalankan**: klik dua kali `run.bat` (otomatis membuka browser),
    atau `python app.py` dari folder `Website`, lalu buka
    `http://127.0.0.1:5000`.

    -   Catatan: `run.bat` memakai `python` bawaan sistem. Jika paket
        terpasang hanya di `venv`, aktifkan venv dulu atau ubah baris
        perintahnya menjadi
        `Website\venv\Scripts\python Website\app.py`.

7.  **(Opsional) Isi data contoh**: login sebagai kepala → menu Buku →
    Import Excel → unggah `Database/data_dummy_buku_1000.xlsx` (1000
    buku). Pastikan header kolomnya sama dengan template (judul,
    penulis, penerbit, tahun_terbit, isbn, kategori, deskripsi, stok);
    jika berbeda, unduh template lalu salin datanya.

### 3.3 Akses dari perangkat lain

Karena `host="0.0.0.0"`, komputer lain di jaringan yang sama bisa
membuka `http://<IP-komputer-server>:5000`. Izinkan port 5000 di Windows
Firewall jika diblokir.

> **Ringkasan bab:** Urutan: instal Python & MySQL → impor
> `Website/schema.sql` → isi `.env` → `seed_admin.py` → `run.bat`.

## BAB 4 --- Panduan Pemakaian per Role

> **Tujuan belajar:** Mengetahui apa yang bisa dilakukan tiap role dan
> urutan langkahnya.\
> **Prasyarat:** Bab 3

### 4.1 Mahasiswa

1.  **Daftar** di `/auth/register` (username, email dari domain yang
    diizinkan seperti gmail/yahoo/outlook, NIM 8--12 digit, nama,
    password).
2.  Akun berstatus **pending**: belum bisa login sampai kepala
    perpustakaan menyetujui.
3.  Setelah disetujui: login → cari buku di menu **Buku**
    (judul/penulis/ISBN + filter kategori) → buka detail → **Ajukan
    Peminjaman**.
4.  Pantau status di **Riwayat Saya** (`diajukan` → `dipinjam` /
    `ditolak`). Pengajuan yang belum diproses bisa **dibatalkan**.
5.  Lihat **Kartu Anggota** digital (otomatis terbit) dan boleh dicetak.
6.  Patuhi jatuh tempo; denda berjalan terlihat di riwayat. Jika
    **blokir denda** aktif, mahasiswa yang telat/berdenda tidak bisa
    meminjam lagi.

### 4.2 Staf

1.  **Kelola buku**: tambah/edit/hapus, unggah sampul, atur stok, lokasi
    rak, lama pinjam khusus buku, kelola kategori.
2.  **Import/Ekspor Excel**: unduh template → isi → unggah; atau ekspor
    daftar buku ke `.xlsx`.
3.  **Pengajuan**: menu Pengajuan → **Setujui** (stok berkurang, jatuh
    tempo dihitung) atau **Tolak** (isi alasan).
4.  **Pinjamkan langsung** dari daftar buku (pilih anggota, bisa atur
    lama pinjam).
5.  **Kembalikan**: tombol Kembalikan di daftar peminjaman → stok
    bertambah, denda otomatis dihitung dan dibekukan jika telat.
6.  **Perpanjang** (dibatasi `MAKS_PERPANJANG`) atau **atur ulang jatuh
    tempo** manual.
7.  **Denda**: tandai **Lunas** atau **Bebaskan** (dengan catatan);
    ekspor ke Excel.
8.  **Kartu**: terbitkan, edit, nonaktifkan/aktifkan, perpanjang masa
    berlaku.
9.  **Laporan**: buku populer, tidak populer, mahasiswa aktif, buku
    terlambat (sebagian bisa diekspor Excel).

### 4.3 Kepala Perpustakaan

Semua kemampuan staf, ditambah: - **Persetujuan akun** mahasiswa baru
(setujui/tolak). - **Manajemen pengguna**: tambah akun staf/kepala,
edit, aktif/nonaktifkan, hapus. - **Pengaturan sistem**: lama pinjam,
kuota, denda, masa tenggang, perpanjangan, blokir denda. Perubahan
langsung berlaku di request berikutnya (lihat `utils/pengaturan.py`).

> **Ringkasan bab:** Mahasiswa mengajukan, staf memproses, kepala
> mengatur akun dan pengaturan.

## BAB 5 --- Peta URL Aplikasi

> **Tujuan belajar:** Melihat daftar alamat (URL) dan fungsinya sebagai
> peta menuju kode.\
> **Prasyarat:** Bab 4

### 5.1 Tabel URL

  ------------------------------------------------------------------------
  Prefix                 Path penting               Fungsi
  ---------------------- -------------------------- ----------------------
  `/`                    `/`                        dashboard

  `/auth`                `/register`, `/login`,     akun sendiri
                         `/logout`, `/profil`       

  `/auth`                `/pengguna`,               kelola pengguna &
                         `/pengguna/tambah`,        persetujuan
                         `/pengguna/<id>/edit`,     
                         `/toggle-aktif`, `/hapus`, 
                         `/pengguna/persetujuan`,   
                         `/setujui`, `/tolak`       

  `/buku`                `/`, `/<id>`, `/tambah`,   data buku
                         `/<id>/edit`,              
                         `/<id>/hapus`, `/ekspor`,  
                         `/kategori`,               
                         `/template-excel`,         
                         `/import-excel`            

  `/peminjaman`          `/ajukan/<buku_id>`,       pengajuan
                         `/<id>/batalkan`,          
                         `/pengajuan`,              
                         `/<id>/setujui`,           
                         `/<id>/tolak`              

  `/peminjaman`          `/pinjam/<buku_id>`, `/`,  transaksi
                         `/<id>/kembalikan`,        
                         `/<id>/perpanjang`,        
                         `/<id>/atur-jatuh-tempo`   

  `/peminjaman`          `/riwayat/saya`,           riwayat
                         `/riwayat/anggota/<id>`,   
                         `/riwayat/buku/<id>`       

  `/denda`               `/`, `/<id>/lunas`,        denda
                         `/<id>/bebaskan`,          
                         `/ekspor`                  

  `/kartu`               `/saya`, `/saya/cetak`,    kartu anggota
                         `/anggota/<id>`,           
                         `/kelola`, `/kelola/...`   

  `/laporan`             `/populer`,                laporan
                         `/tidak-populer`,          
                         `/mahasiswa-aktif`,        
                         `/terlambat`; ekspor       
                         khusus mahasiswa aktif &   
                         terlambat                  

  `/pengaturan`          `/`                        pengaturan sistem
  ------------------------------------------------------------------------

Route berbasis `POST` (hapus, setujui, dll.) hanya dipanggil dari tombol
form, bukan dibuka lewat alamat browser.

> **Ringkasan bab:** Setiap fitur punya prefix URL sendiri sesuai
> blueprint-nya.

# BAGIAN III --- DATABASE

## BAB 6 --- Struktur Database (schema.sql)

> **File dibahas:** `Website/schema.sql`\
> **Tujuan belajar:** Memahami tabel, kolom, dan relasi database.\
> **Prasyarat:** Bab 2

> **Penting:** ada dua file, `Website/schema.sql` (terbaru, dipakai
> kode) dan `Database/schema.sql` (versi lama: kolom `nisn` bukan `nim`,
> tanpa tabel `pengaturan`/`log_stok`, tanpa kolom denda, `lokasi_rak`,
> `lama_pinjam_hari`, `jumlah_perpanjang`). Gunakan
> **`Website/schema.sql`**. Menjalankan versi lama membuat aplikasi
> error karena kolom tidak cocok dengan `models.py`.

### 6.1 Pembukaan (baris 6--9)

-   `CREATE DATABASE IF NOT EXISTS perpustakaan_db` --- buat database
    hanya jika belum ada.
-   `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci` --- mendukung
    semua karakter (termasuk emoji) dan pencarian tidak peka huruf
    besar/kecil.
-   `USE perpustakaan_db;` --- semua perintah berikutnya dijalankan di
    database ini.

### 6.2 Istilah SQL yang muncul

`AUTO_INCREMENT` nomor otomatis · `PRIMARY KEY` kunci unik utama ·
`UNIQUE` tidak boleh kembar · `NOT NULL` wajib diisi · `DEFAULT` nilai
awal · `ENUM` hanya boleh salah satu nilai daftar · `FOREIGN KEY`
penghubung ke tabel lain · `ENGINE=InnoDB` mesin yang mendukung relasi &
transaksi.

### 6.3 Tabel `users` (baris 14--32) --- semua akun

  ---------------------------------------------------------------------
  Kolom                              Penjelasan
  ---------------------------------- ----------------------------------
  `id`                               kunci utama

  `username`, `email`                unik, wajib

  `nim`                              unik, boleh `NULL` (staf/kepala
                                     tidak punya); sekaligus **ID
                                     kartu**

  `password_hash`                    hash password (255 karakter cukup
                                     untuk hash Werkzeug)

  `nama_lengkap`                     wajib

  `role`                             `mahasiswa` / `staf` /
                                     `kepala_perpustakaan`, default
                                     mahasiswa

  `no_telepon`, `alamat`             opsional

  `is_active`                        1 = boleh login, 0 = dinonaktifkan

  `status_akun`                      `pending` (baru daftar),
                                     `disetujui`, `ditolak`; default
                                     `disetujui` agar akun buatan admin
                                     langsung aktif

  `created_at`                       waktu dibuat otomatis
  ---------------------------------------------------------------------

### 6.4 Tabel `kartu_anggota` (baris 37--44)

Relasi **1-ke-1** dengan user (`user_id` UNIQUE). `tanggal_terbit`,
`tanggal_kadaluarsa` wajib, `status` aktif/nonaktif.
`ON DELETE CASCADE`: user dihapus → kartunya ikut terhapus.

### 6.5 Tabel `kategori` (baris 49--52)

Hanya `id` dan `nama_kategori` (unik).

### 6.6 Tabel `buku` (baris 57--72)

`judul`, `penulis` wajib; `penerbit`, `tahun_terbit` (tipe `YEAR`),
`isbn`, `deskripsi` opsional; `stok` default 0; `sampul_path` menyimpan
**alamat file** gambar (bukan gambarnya); `lokasi_rak` mis. "Rak A-3";
`lama_pinjam_hari` (NULL = ikut pengaturan umum); `kategori_id` →
`kategori` dengan `ON DELETE SET NULL` (kategori dihapus, buku tetap ada
tanpa kategori).

### 6.7 Tabel `peminjaman` (baris 77--101) --- transaksi sekaligus riwayat

-   Relasi: `user_id` (peminjam), `buku_id`, `diproses_oleh` (staf yang
    memproses), `denda_diproses_oleh` (staf yang mengurus denda). Hapus
    user/buku → riwayat terkait ikut terhapus (`CASCADE`); hapus staf →
    hanya kolom pemroses jadi `NULL`.
-   Tanggal: `tanggal_pinjam`, `tanggal_jatuh_tempo` (wajib),
    `tanggal_kembali` (NULL selama belum kembali).
-   `status`: `diajukan`, `dipinjam` (default), `dikembalikan`,
    `terlambat`, `ditolak`. (Keterlambatan umumnya dihitung dari
    tanggal, bukan dari status ini.)
-   `catatan`: alasan penolakan/catatan staf.
-   Denda: `denda` (rupiah, bulat), `status_denda` (`tidak_ada`,
    `belum_lunas`, `lunas`, `dibebaskan`), `tanggal_denda_selesai`,
    `catatan_denda`.
-   `jumlah_perpanjang`: berapa kali sudah diperpanjang (dibandingkan
    dengan `MAKS_PERPANJANG`).

### 6.8 Tabel `pengaturan` (baris 107--110)

Model *key-value*: `kunci` (kunci utama) + `nilai`. Boleh kosong; nilai
awal dari `config.py`. Dibaca/ditulis oleh `utils/pengaturan.py`.

### 6.9 Tabel `log_stok` (baris 115--125)

Tabel ini dirancang untuk menyimpan riwayat perubahan stok: `buku_id`,
`user_id` (pelaku), `perubahan` (+/−), `stok_sesudah`, `alasan`, dan
`waktu`. **Namun, pada kode route yang diperiksa di ZIP ini belum
ditemukan proses yang menulis ke `LogStok`**, sehingga riwayat tersebut
tidak otomatis terisi. Lihat temuan nomor 8 di Lampiran A.

### 6.10 Bagian "Data Awal" (baris 127--134)

Hanya komentar: tidak ada akun bawaan. Akun kepala pertama dibuat lewat
`python seed_admin.py`. (Teks "operator123" di komentar tidak dipakai di
mana pun.)

### 6.11 Index (baris 139--145)

Index membuat pencarian/pengurutan lebih cepat, dengan sedikit biaya
saat menulis data. Dibuat untuk: `buku.judul`, `buku.penulis`
(pencarian), `peminjaman.status`, `.user_id`, `.buku_id`,
`.status_denda` (laporan & filter), `log_stok.buku_id`.

### 6.12 Diagram relasi (teks)

    users 1──1 kartu_anggota
    users 1──* peminjaman *──1 buku *──1 kategori
    users 1──* log_stok *──1 buku
    pengaturan  (berdiri sendiri)

> **Ringkasan bab:** 7 tabel; `peminjaman` adalah pusat data transaksi
> dan riwayat. Gunakan `Website/schema.sql`.

# BAGIAN IV --- PENJELASAN KODE

## BAB 7 --- Alur Kerja Satu Request

> **Tujuan belajar:** Mengikuti perjalanan satu request dari browser
> sampai tampil kembali.\
> **Prasyarat:** Bab 2, 6

### 7.1 Contoh: Mahasiswa Mengajukan Pinjaman

1.  Browser mengirim `POST /peminjaman/ajukan/12`.
2.  Flask menjalankan `before_request` → `terapkan_pengaturan` menyalin
    pengaturan terbaru dari DB ke `app.config`.
3.  Flask-Login memuat user lewat `load_user` dari session.
4.  Dekorator memeriksa login dan role.
5.  Fungsi route memanggil `cek_bisa_meminjam` (`utils/pinjam.py`):
    kartu valid → tidak ada tunggakan → kuota cukup.
6.  Jika lolos, baris `Peminjaman` berstatus `diajukan` dibuat dan
    di-`commit`.
7.  Server `flash` pesan lalu `redirect`.
8.  Halaman tujuan dirender dengan Jinja2; `context_processor` menambah
    angka badge di navbar.
9.  Staf menyetujui → status `dipinjam`, stok berkurang, jatuh tempo =
    hari ini + lama pinjam (`hitung_jatuh_tempo`).
10. Saat dikembalikan → `hitung_denda` dijalankan; jika telat, `denda`
    dibekukan dan `status_denda = belum_lunas`.

**Siklus status `peminjaman.status`:** `diajukan` → (`ditolak`) atau
`dipinjam` → `dikembalikan`. **Siklus `status_denda`:** `tidak_ada` →
`belum_lunas` → `lunas` atau `dibebaskan`.

> **Ringkasan bab:** Urutan: before_request → login → cek role →
> validasi → simpan → flash → redirect → render.

## BAB 8 --- Inti Aplikasi (app.py)

> **File dibahas:** `app.py`\
> **Tujuan belajar:** Memahami cara aplikasi dirakit di `app.py`.\
> **Prasyarat:** Bab 2, 7

### 8.1 Inisialisasi Flask & Konfigurasi (baris 10--24)

``` python
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    if not os.path.isabs(app.config["UPLOAD_FOLDER"]):
        app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
```

-   `app = Flask(__name__)` --- membuat objek aplikasi Flask. `__name__`
    dipakai Flask untuk menentukan lokasi root project.
-   `app.config.from_object(Config)` --- memuat semua pengaturan
    (SECRET_KEY, URI database, dll) dari class `Config` di `config.py`.
-   `db.init_app(app)` --- menghubungkan objek SQLAlchemy (`db`) yang
    dibuat terpisah di `extensions.py` ke aplikasi ini (pola
    *application factory*).
-   `login_manager.init_app(app)` --- sama, tapi untuk Flask-Login
    (pengelola session login).
-   `if not os.path.isabs(...)` --- mengecek apakah path `UPLOAD_FOLDER`
    sudah absolut. Jika belum, digabung dengan `app.root_path` (lokasi
    folder project), supaya path selalu konsisten di komputer/OS
    manapun, tidak tergantung dari mana perintah dijalankan.
-   `os.makedirs(..., exist_ok=True)` --- membuat folder upload jika
    belum ada. `exist_ok=True` mencegah error kalau foldernya sudah ada.

### 8.2 `before_request`: Pengaturan Dinamis (baris 27--38)

``` python
    from utils.pengaturan import terapkan_pengaturan
    from utils.denda import denda_peminjaman, format_rupiah
    from flask import request

    @app.before_request
    def muat_pengaturan():
        if request.endpoint != "static":
            terapkan_pengaturan(app)

    app.jinja_env.filters["rupiah"] = format_rupiah
    app.jinja_env.globals["denda_sekarang"] = denda_peminjaman
```

-   Import dilakukan **di dalam** fungsi `create_app()` (bukan di atas
    file) --- ini disebut *local import*, biasa dipakai untuk
    menghindari *circular import* (dua file saling mengimpor satu sama
    lain).
-   `@app.before_request` --- dekorator yang membuat fungsi
    `muat_pengaturan` otomatis dijalankan **sebelum setiap request**
    masuk ke aplikasi.
-   `if request.endpoint != "static"` --- mencegah fungsi ini jalan saat
    request-nya hanya meminta file statis (CSS/JS/gambar), supaya tidak
    query database tanpa perlu di setiap load file statis.
-   `terapkan_pengaturan(app)` --- menyalin data pengaturan (lama
    pinjam, tarif denda, dst) dari tabel database ke `app.config`,
    supaya nilai-nilai itu bisa diubah dari database tanpa mengubah
    kode.
-   `app.jinja_env.filters["rupiah"] = format_rupiah` --- mendaftarkan
    fungsi `format_rupiah` sebagai filter Jinja, sehingga di template
    HTML bisa dipakai `{{ angka|rupiah }}`.
-   `app.jinja_env.globals["denda_sekarang"] = denda_peminjaman` ---
    mendaftarkan fungsi sebagai *global*, sehingga bisa dipanggil
    langsung di template: `{{ denda_sekarang(...) }}`.

### 8.3 `load_user` & `context_processor` (baris 40--72)

``` python
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_jumlah_pending_akun():
        from flask_login import current_user
        if current_user.is_authenticated and current_user.is_kepala:
            jumlah = User.query.filter_by(role="mahasiswa", status_akun="pending").count()
        else:
            jumlah = 0
        return {"jumlah_pending_akun": jumlah}

    @app.context_processor
    def inject_jumlah_pengajuan_peminjaman():
        from flask_login import current_user
        from models import Peminjaman
        if current_user.is_authenticated and (current_user.is_staf or current_user.is_kepala):
            jumlah = Peminjaman.query.filter_by(status="diajukan").count()
        else:
            jumlah = 0
        return {"jumlah_pengajuan_peminjaman": jumlah}

    @app.context_processor
    def inject_tahun_sekarang():
        return {"tahun_sekarang": date.today().year}
```

-   `@login_manager.user_loader` --- dekorator wajib dari Flask-Login.
    Fungsi `load_user` dipanggil otomatis untuk mengambil data user dari
    `user_id` yang tersimpan di session.
-   `User.query.get(int(user_id))` --- `user_id` dari session disimpan
    sebagai string, maka dikonversi `int()` dulu sebelum dicari di tabel
    `User`.
-   `@app.context_processor` --- dekorator yang membuat *dictionary*
    yang dikembalikan fungsi tersedia otomatis di **semua** template,
    tanpa perlu dikirim manual lewat `render_template(...)`.
-   `inject_jumlah_pending_akun` --- menghitung jumlah akun mahasiswa
    berstatus `"pending"`, tapi hanya dihitung kalau user yang login
    adalah kepala perpustakaan (`is_kepala`). Kalau bukan, nilainya 0
    --- ini untuk efisiensi, supaya tidak query database percuma di role
    lain.
-   `inject_jumlah_pengajuan_peminjaman` --- logika serupa, menghitung
    peminjaman berstatus `"diajukan"`, untuk role staf atau kepala.
-   `inject_tahun_sekarang` --- mengembalikan `date.today().year`,
    dipakai agar tahun di footer (copyright) otomatis mengikuti tahun
    berjalan, tidak perlu diubah manual tiap tahun di template.

### 8.4 Registrasi Blueprint (baris 74--93)

``` python
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.buku import buku_bp
    from routes.peminjaman import peminjaman_bp
    from routes.laporan import laporan_bp
    from routes.kartu import kartu_bp
    from routes.denda import denda_bp
    from routes.pengaturan import pengaturan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(buku_bp)
    app.register_blueprint(peminjaman_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(kartu_bp)
    app.register_blueprint(denda_bp)
    app.register_blueprint(pengaturan_bp)

    return app
```

-   **Blueprint** adalah cara Flask memecah kumpulan route (URL +
    fungsi) menjadi modul-modul terpisah per fitur, supaya satu file
    `app.py` tidak berisi ratusan route sekaligus.
-   Setiap baris import mengambil objek blueprint (`xxx_bp`) yang
    didefinisikan di masing-masing file dalam folder `routes/`.
-   `app.register_blueprint(...)` --- mendaftarkan blueprint tersebut ke
    aplikasi utama, sehingga semua route di dalamnya menjadi aktif.
-   Urutan pendaftaran tidak memengaruhi fungsi program, hanya soal
    kerapian pengelompokan kode.
-   `return app` --- mengakhiri fungsi `create_app()`, mengembalikan
    objek aplikasi Flask yang sudah lengkap dengan konfigurasi,
    ekstensi, dan semua route.

### 8.5 Menjalankan Aplikasi (baris 96--98)

``` python
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
```

-   `if __name__ == "__main__":` --- blok ini hanya dijalankan ketika
    file `app.py` dieksekusi langsung (`python app.py`), bukan ketika
    filenya diimpor dari file lain.
-   `app = create_app()` --- memanggil fungsi pabrik (*factory
    function*) yang sudah dibuat di atas untuk menghasilkan instance
    aplikasi.
-   `app.run(...)` --- menjalankan server pengembangan (development
    server) bawaan Flask.
    -   `debug=True` --- mengaktifkan mode debug: server otomatis
        restart saat kode berubah, dan menampilkan halaman error detail
        jika terjadi kesalahan.
    -   `host="0.0.0.0"` --- membuat server bisa diakses dari perangkat
        lain di jaringan yang sama, bukan hanya dari
        `localhost`/komputer itu sendiri.
    -   `port=5000` --- port default tempat server berjalan (akses lewat
        `http://alamat-ip:5000`).

> **Ringkasan bab:** `create_app()` menyiapkan konfigurasi, ekstensi,
> pengaturan dinamis, context processor, dan blueprint.

## BAB 9 --- Konfigurasi, Ekstensi, dan Model

> **File dibahas:** `config.py, extensions.py, models.py`\
> **Tujuan belajar:** Memahami konfigurasi dan model data (class Python
> untuk tabel).\
> **Prasyarat:** Bab 6, 8

### 9.1 `extensions.py` --- Objek Ekstensi Bersama

``` python
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Silakan login terlebih dahulu untuk mengakses halaman ini."
login_manager.login_message_category = "warning"
```

-   `db = SQLAlchemy()` --- membuat objek ORM (Object Relational Mapper)
    yang nantinya dipakai di seluruh file untuk mendefinisikan tabel
    (lewat `db.Model`) dan melakukan query.
-   `login_manager = LoginManager()` --- objek pengelola sesi login dari
    Flask-Login.
-   File ini **tidak langsung terhubung ke aplikasi** (`app`) saat
    dibuat --- baru dihubungkan belakangan lewat `db.init_app(app)` di
    `app.py`. Ini disebut pola *application factory*: ekstensi dibuat
    terpisah dari `app` supaya bisa diimpor oleh file manapun
    (`models.py`, `routes/`) tanpa risiko *circular import* (dua file
    saling mengimpor).
-   `login_manager.login_view = "auth.login"` --- jika user yang belum
    login mencoba akses halaman yang butuh login, Flask-Login otomatis
    mengarahkan ke endpoint `auth.login` (fungsi `login` di blueprint
    `auth`).
-   `login_manager.login_message` dan `login_message_category` --- pesan
    dan kategori (untuk styling, misalnya warna kuning untuk "warning")
    yang ditampilkan saat user diarahkan ke halaman login.

### 9.2 `config.py` --- Konfigurasi Aplikasi

``` python
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
```

-   `load_dotenv()` --- membaca file `.env` (file konfigurasi rahasia
    yang tidak ikut di-upload ke repo publik) dan memasukkan isinya
    sebagai *environment variable*.
-   `os.getenv("DB_HOST")` --- mengambil nilai variabel lingkungan
    `DB_HOST`. Jika tidak ada argumen kedua, hasilnya `None` saat
    variabel tidak ditemukan. Pada `DB_PASSWORD`, argumen kedua `""`
    dipakai sebagai nilai cadangan jika variabel kosong/tidak ada
    (misalnya saat password database memang dikosongkan).
-   `SQLALCHEMY_DATABASE_URI` --- string koneksi database MySQL, disusun
    dengan f-string dari lima variabel di atas. Formatnya:
    `mysql+mysqlconnector://user:password@host:port/nama_database`.
-   `SQLALCHEMY_TRACK_MODIFICATIONS = False` --- mematikan fitur
    pelacakan perubahan objek SQLAlchemy yang memakan memori dan tidak
    dipakai di sini.
-   `SECRET_KEY` --- kunci rahasia yang dipakai Flask untuk mengenkripsi
    session dan data sensitif lain (seperti cookie login). Wajib
    dirahasiakan, karenanya diambil dari `.env`, bukan ditulis langsung
    di kode.

``` python
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads/sampul")
    ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_EXCEL_EXT = {"xlsx"}
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5")) * 1024 * 1024
```

-   `UPLOAD_FOLDER` --- folder penyimpanan file upload (sampul buku),
    default `"static/uploads/sampul"` jika tidak diatur di `.env`.
-   `ALLOWED_IMAGE_EXT` / `ALLOWED_EXCEL_EXT` --- kumpulan (`set`)
    ekstensi file yang diizinkan, dipakai nanti untuk validasi saat
    upload sampul buku atau import data Excel.
-   `MAX_CONTENT_LENGTH` --- batas ukuran file upload dalam byte. Nilai
    diambil dalam MB dari `.env` (default 5), lalu dikonversi ke byte
    (`* 1024 * 1024`) karena Flask butuh satuan byte.

``` python
    LAMA_PINJAM_HARI = 7
    MAKS_PINJAM_PER_USER = 2
    NIM_PANJANG_MIN = 8
    NIM_PANJANG_MAKS = 12
    MASA_BERLAKU_KARTU_HARI = 365
    PERINGATAN_JATUH_TEMPO_HARI = 3

    DENDA_PER_HARI = 1000
    DENDA_MAKS = 0
    MASA_TENGGANG_HARI = 0
    BLOKIR_JIKA_DENDA = 1

    MAKS_PERPANJANG = 2

    ALLOWED_EMAIL_DOMAINS = [
        "gmail.com", "yahoo.com", "yahoo.co.id", "outlook.com",
        "hotmail.com", "live.com", "icloud.com", "proton.me", "protonmail.com",
    ]
```

-   Seluruh nilai ini adalah **nilai awal/cadangan** (nilai *hardcode*
    langsung di kode), bukan nilai tetap selamanya --- berdasarkan
    komentar di kode, kepala perpustakaan bisa mengubahnya nanti lewat
    menu Pengaturan, yang tersimpan di tabel database `pengaturan`
    (lihat class `Pengaturan` di `models.py`, dan fungsi
    `terapkan_pengaturan` di `utils/pengaturan.py` yang menyalin nilai
    dari tabel ke `app.config` setiap request).
-   `LAMA_PINJAM_HARI = 7` --- batas hari peminjaman default.
-   `MAKS_PINJAM_PER_USER = 2` --- maksimal buku yang boleh
    dipinjam/diajukan sekaligus per mahasiswa.
-   `NIM_PANJANG_MIN/MAKS` --- rentang panjang digit NIM yang diterima
    saat validasi, bisa disesuaikan per kampus.
-   `MASA_BERLAKU_KARTU_HARI = 365` --- lama masa berlaku kartu anggota
    (1 tahun) saat diterbitkan/diperpanjang.
-   `PERINGATAN_JATUH_TEMPO_HARI = 3` --- mulai berapa hari sebelum
    jatuh tempo, sistem menampilkan peringatan.
-   `DENDA_PER_HARI = 1000` --- tarif denda keterlambatan per hari (Rp).
-   `DENDA_MAKS = 0` --- batas atas denda; nilai 0 berarti tidak ada
    batas.
-   `MASA_TENGGANG_HARI = 0` --- jumlah hari gratis setelah jatuh tempo
    sebelum denda mulai dihitung.
-   `BLOKIR_JIKA_DENDA = 1` --- nilai 1 (dianggap *true*) berarti
    mahasiswa dengan denda/keterlambatan tidak bisa meminjam buku baru.
-   `MAKS_PERPANJANG = 2` --- berapa kali tanggal jatuh tempo boleh
    diperpanjang.
-   `ALLOWED_EMAIL_DOMAINS` --- daftar (`list`) domain email yang
    dianggap valid saat registrasi, tanpa perlu verifikasi OTP. Domain
    kampus resmi bisa ditambahkan di sini.

### 9.3 `models.py` --- Struktur Data (ORM)

``` python
from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

ROLE_LABEL = {
    "mahasiswa": "Mahasiswa",
    "staf": "Staf",
    "kepala_perpustakaan": "Kepala Perpustakaan",
}
STATUS_PINJAMAN_AKTIF = ("diajukan", "dipinjam")
```

-   `generate_password_hash` / `check_password_hash` --- fungsi dari
    Werkzeug untuk mengenkripsi password (hash) dan memverifikasinya,
    sehingga password asli tidak pernah disimpan di database.
-   `ROLE_LABEL` --- dictionary pemetaan nilai role di database
    (snake_case, mis. `"kepala_perpustakaan"`) ke label tampilan yang
    lebih enak dibaca (`"Kepala Perpustakaan"`).
-   `STATUS_PINJAMAN_AKTIF` --- tuple berisi status peminjaman yang
    dianggap "masih memakai kuota pinjam" (dipakai untuk menghitung
    berapa buku yang sedang dipinjam/diajukan seorang mahasiswa).

### Class `User`

``` python
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    ...
    role = db.Column(db.Enum("mahasiswa", "staf", "kepala_perpustakaan", name="role_enum"), nullable=False, default="mahasiswa")
```

-   `class User(UserMixin, db.Model):` --- class ini mewarisi dua class:
    `UserMixin` (dari Flask-Login, memberi method standar seperti
    `is_authenticated`, `is_active`, `get_id()`) dan `db.Model` (dari
    SQLAlchemy, menjadikan class ini sebuah tabel database).
-   `__tablename__ = "users"` --- nama tabel di database.
-   `db.Column(db.Integer, primary_key=True)` --- mendefinisikan kolom
    `id` sebagai kunci utama (primary key), tipe angka.
-   `unique=True, nullable=False` --- kolom `username` dan `email` wajib
    diisi dan tidak boleh ada nilai yang sama di baris lain.
-   `nim` --- `nullable=True` karena wajib untuk mahasiswa tapi opsional
    untuk staf/kepala; nomor ini juga dipakai sebagai nomor kartu
    perpustakaan.
-   `role` menggunakan `db.Enum(...)` --- artinya nilai kolom ini
    dibatasi hanya boleh salah satu dari tiga pilihan yang disebutkan,
    dijamin oleh database sendiri (bukan cuma validasi di kode Python).
-   `is_active_db = db.Column("is_active", db.Boolean, ...)` --- nama
    atribut Python (`is_active_db`) berbeda dari nama kolom asli di
    database (`"is_active"`), karena `UserMixin` sudah mendefinisikan
    properti `is_active` miliknya sendiri; penamaan ini menghindari
    bentrok.
-   `status_akun` --- Enum tiga nilai (`pending`, `disetujui`,
    `ditolak`) untuk alur persetujuan akun oleh kepala perpustakaan.
    Default `"disetujui"` supaya akun lama/akun buatan operator tidak
    otomatis terkunci.

``` python
    kartu = db.relationship("KartuAnggota", backref="pemilik", uselist=False, cascade="all, delete-orphan")
    peminjaman_list = db.relationship("Peminjaman", foreign_keys="Peminjaman.user_id", backref="anggota", cascade="all, delete-orphan")
```

-   `db.relationship(...)` --- mendefinisikan relasi antar tabel di
    level Python (tanpa perlu menulis `JOIN` manual).
-   `"KartuAnggota"` --- nama class tabel tujuan. `backref="pemilik"`
    membuat arah sebaliknya otomatis tersedia: dari objek `KartuAnggota`
    bisa akses `.pemilik` untuk mendapatkan `User`-nya.
-   `uselist=False` --- relasi ini **satu-ke-satu** (satu user hanya
    punya satu kartu), bukan daftar.
-   `cascade="all, delete-orphan"` --- jika user dihapus, data terkait
    (kartu, peminjaman) ikut terhapus otomatis, supaya tidak ada data
    "yatim" yang menunjuk ke user yang sudah tidak ada.
-   `peminjaman_list` menunjuk relasi satu-ke-banyak (satu user bisa
    punya banyak riwayat peminjaman).
    `foreign_keys="Peminjaman.user_id"` ditulis eksplisit karena tabel
    `Peminjaman` punya **dua** kolom yang sama-sama merujuk ke
    `users.id` (`user_id` dan `diproses_oleh`), sehingga SQLAlchemy
    perlu diberi tahu secara spesifik kolom mana yang dipakai untuk
    relasi ini.

``` python
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

-   `set_password` --- menyimpan **hash** dari password (bukan teks
    asli) ke kolom `password_hash`.
-   `check_password` --- membandingkan password yang dimasukkan user
    saat login dengan hash tersimpan, mengembalikan `True`/`False`.

``` python
    @property
    def is_kepala(self):
        return self.role == "kepala_perpustakaan"
```

-   `@property` --- dekorator yang membuat method bisa diakses seperti
    atribut biasa, tanpa tanda kurung (`user.is_kepala`, bukan
    `user.is_kepala()`).
-   `is_kepala`, `is_staf`, `is_mahasiswa` --- masing-masing hanya
    mengecek apakah `role` cocok dengan nilai tertentu; dipakai di
    banyak tempat (seperti di `app.py` bagian context_processor) untuk
    pengecekan hak akses yang mudah dibaca.
-   `role_label` --- mengambil label tampilan dari dictionary
    `ROLE_LABEL`, dengan nilai cadangan `self.role` sendiri jika tidak
    ditemukan di dictionary.

``` python
    @property
    def jumlah_pinjaman_aktif(self):
        """Jumlah buku yang sedang diajukan atau dipinjam (belum dikembalikan)."""
        return Peminjaman.query.filter(
            Peminjaman.user_id == self.id,
            Peminjaman.status.in_(STATUS_PINJAMAN_AKTIF),
        ).count()
```

-   `Peminjaman.query.filter(...)` --- query SQLAlchemy untuk menghitung
    baris di tabel `peminjaman` milik user ini (`user_id == self.id`)
    yang statusnya ada di dalam `STATUS_PINJAMAN_AKTIF` (yaitu
    `"diajukan"` atau `"dipinjam"`).
-   `.in_(...)` --- setara `WHERE status IN ('diajukan', 'dipinjam')` di
    SQL mentah.
-   `.count()` --- mengembalikan jumlah baris, dipakai untuk mengecek
    apakah mahasiswa sudah mencapai batas `MAKS_PINJAM_PER_USER`.
-   `menunggu_persetujuan` dan `ditolak_operator` --- property pendek
    untuk mengecek `status_akun`, mempermudah pengecekan di template
    (`{% if user.menunggu_persetujuan %}`) daripada menulis perbandingan
    string berulang kali.

### Class `KartuAnggota`

``` python
class KartuAnggota(db.Model):
    __tablename__ = "kartu_anggota"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    tanggal_terbit = db.Column(db.Date, default=date.today)
    tanggal_kadaluarsa = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum("aktif", "nonaktif", name="status_kartu_enum"), default="aktif")
```

-   `db.ForeignKey("users.id")` --- menandai kolom `user_id` sebagai
    kunci tamu (*foreign key*) yang merujuk ke kolom `id` di tabel
    `users`. `unique=True` memastikan relasi satu-ke-satu dijaga juga di
    level database, tidak hanya di Python.
-   `tanggal_terbit` --- default `date.today` (catatan: tanpa tanda
    kurung `()`, karena SQLAlchemy memanggil fungsi ini sendiri setiap
    kali baris baru dibuat, bukan dipanggil sekali saat class
    didefinisikan).

``` python
    @property
    def nim(self):
        """ID kartu = NIM pemilik kartu (satu sumber data: users.nim)."""
        return self.pemilik.nim

    @property
    def is_kadaluarsa(self):
        return date.today() > self.tanggal_kadaluarsa

    @property
    def bisa_dipakai(self):
        return self.status == "aktif" and not self.is_kadaluarsa
```

-   `nim` --- properti ini **tidak** punya kolom sendiri di database,
    melainkan mengambil nilai `nim` dari `self.pemilik` (yaitu objek
    `User` terkait, didapat lewat `backref="pemilik"` yang didefinisikan
    tadi). Ini sengaja dibuat begitu supaya data NIM hanya tersimpan di
    satu tempat (tabel `users`), tidak diduplikasi di tabel kartu.
-   `is_kadaluarsa` --- membandingkan tanggal hari ini dengan
    `tanggal_kadaluarsa`.
-   `bisa_dipakai` --- kartu valid dipakai hanya jika statusnya
    `"aktif"` **dan** belum kadaluarsa (dua syarat harus sama-sama
    terpenuhi, dihubungkan `and`).

### Class `Kategori`

``` python
class Kategori(db.Model):
    __tablename__ = "kategori"
    id = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100), unique=True, nullable=False)
    buku_list = db.relationship("Buku", backref="kategori", lazy=True)
```

-   Tabel paling sederhana: hanya `id` dan nama kategori.
-   `lazy=True` pada relationship --- data buku terkait **tidak**
    langsung diambil saat objek `Kategori` di-query, melainkan baru
    di-query ke database saat `.buku_list` benar-benar diakses
    (menghemat beban query jika tidak dibutuhkan).

### Class `Buku`

``` python
class Buku(db.Model):
    __tablename__ = "buku"
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    ...
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))
    stok = db.Column(db.Integer, default=0)
    sampul_path = db.Column(db.String(255))
    lokasi_rak = db.Column(db.String(50))
    lama_pinjam_hari = db.Column(db.Integer)
```

-   Kolom-kolom dasar data buku (judul, penulis, penerbit, dst).
    `kategori_id` adalah foreign key ke tabel `kategori`.
-   `stok` --- jumlah eksemplar buku yang tersedia, default 0.
-   `sampul_path` --- menyimpan path/nama file gambar sampul yang
    diupload (lokasi fisik file diatur lewat `UPLOAD_FOLDER` di
    `config.py`).
-   `lama_pinjam_hari` --- kolom nullable (boleh kosong): jika diisi,
    berarti buku ini punya aturan lama pinjam khusus, berbeda dari
    pengaturan umum `LAMA_PINJAM_HARI`.

``` python
    @property
    def total_dipinjam(self):
        return sum(1 for p in self.peminjaman_list)
```

-   Menghitung jumlah **seluruh** riwayat peminjaman buku ini (semua
    status, bukan hanya yang aktif) --- dipakai misalnya untuk laporan
    buku populer.
-   `sum(1 for p in self.peminjaman_list)` --- menjumlahkan angka 1
    untuk tiap item di `peminjaman_list`; cara ini setara dengan
    `len(self.peminjaman_list)`.

### Class `Peminjaman`

``` python
class Peminjaman(db.Model):
    __tablename__ = "peminjaman"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    buku_id = db.Column(db.Integer, db.ForeignKey("buku.id"), nullable=False)
    diproses_oleh = db.Column(db.Integer, db.ForeignKey("users.id"))
    tanggal_pinjam = db.Column(db.Date, default=date.today)
    tanggal_jatuh_tempo = db.Column(db.Date, nullable=False)
    tanggal_kembali = db.Column(db.Date)
    status = db.Column(db.Enum("diajukan", "dipinjam", "dikembalikan", "terlambat", "ditolak", name="status_pinjam_enum"), default="dipinjam")
    catatan = db.Column(db.String(255))
```

-   Ini tabel inti transaksi peminjaman, menghubungkan `User` (peminjam)
    dan `Buku`.
-   `diproses_oleh` --- foreign key **kedua** yang menunjuk ke
    `users.id`, mencatat staf/kepala mana yang memproses pengajuan ini
    (berbeda dari `user_id` yang merupakan peminjamnya).
-   `status` Enum lima nilai sesuai alur yang dijelaskan di komentar
    kode: `diajukan` → menunggu tinjauan, `dipinjam` →
    disetujui/dipinjamkan langsung, `dikembalikan` → selesai, `ditolak`
    → ditolak. Catatan: `"terlambat"` ada di daftar Enum tapi menurut
    komentar kode **tidak pernah disimpan langsung** --- keterlambatan
    dihitung secara dinamis lewat property `is_telat`, bukan disimpan
    sebagai nilai status baris.

``` python
    denda = db.Column(db.Integer, nullable=False, default=0)
    status_denda = db.Column(db.Enum("tidak_ada", "belum_lunas", "lunas", "dibebaskan", name="status_denda_enum"), nullable=False, default="tidak_ada")
    tanggal_denda_selesai = db.Column(db.Date)
    denda_diproses_oleh = db.Column(db.Integer, db.ForeignKey("users.id"))
    catatan_denda = db.Column(db.String(255))
    jumlah_perpanjang = db.Column(db.Integer, nullable=False, default=0)
```

-   `denda` --- nilai nominal denda (Rupiah), tapi menurut komentar kode
    nilai ini baru **dibekukan** (diisi tetap) saat buku benar-benar
    dikembalikan. Selama buku masih dipinjam, besaran denda dihitung
    berjalan (real-time) lewat fungsi di `utils/denda.py`, bukan dari
    kolom ini.
-   `status_denda` --- status pembayaran denda: belum ada, menunggu
    dibayar, lunas, atau dibebaskan (dihapuskan kepala perpustakaan).
-   `jumlah_perpanjang` --- penghitung berapa kali jatuh tempo
    peminjaman ini sudah diperpanjang, dibandingkan dengan batas
    `MAKS_PERPANJANG` di `config.py`.

``` python
    @property
    def hari_telat(self):
        """Jumlah hari melewati jatuh tempo (0 jika belum/tidak telat)."""
        if self.status == "dikembalikan" and self.tanggal_kembali:
            akhir = self.tanggal_kembali
        elif self.status == "dipinjam":
            akhir = date.today()
        else:
            return 0
        return max(0, (akhir - self.tanggal_jatuh_tempo).days)
```

-   Fungsi ini menentukan "tanggal akhir" yang dipakai untuk menghitung
    keterlambatan: jika sudah dikembalikan, pakai tanggal pengembalian;
    jika masih dipinjam, pakai hari ini; selain itu (diajukan/ditolak),
    langsung kembalikan 0 (belum relevan dihitung telat).
-   `(akhir - self.tanggal_jatuh_tempo).days` --- pengurangan dua objek
    `date` di Python menghasilkan objek `timedelta`, dan `.days`
    mengambil selisih dalam satuan hari.
-   `max(0, ...)` --- memastikan hasil tidak pernah negatif (jika belum
    jatuh tempo, selisihnya negatif, tapi ditampilkan sebagai 0 hari
    telat).

``` python
    @property
    def is_telat(self):
        if self.status in ("dikembalikan", "diajukan", "ditolak"):
            if self.status == "dikembalikan":
                return self.tanggal_kembali and self.tanggal_kembali > self.tanggal_jatuh_tempo
            return False
        return date.today() > self.tanggal_jatuh_tempo
```

-   Mengembalikan `True`/`False` apakah peminjaman ini terlambat.
-   Untuk status `diajukan`/`ditolak`, selalu `False` (belum/tidak
    relevan).
-   Untuk `dikembalikan`, dicek apakah tanggal kembali melewati jatuh
    tempo.
-   Untuk status lain (`dipinjam`), dicek apakah hari ini sudah melewati
    jatuh tempo --- artinya telat meski belum dikembalikan.

``` python
    @property
    def hari_menuju_jatuh_tempo(self):
        if self.status != "dipinjam":
            return None
        return (self.tanggal_jatuh_tempo - date.today()).days
```

-   Hanya dihitung untuk peminjaman berstatus `"dipinjam"` (sedang
    berjalan); status lain mengembalikan `None`.
-   Hasil bisa negatif jika sudah lewat jatuh tempo --- dipakai untuk
    menampilkan peringatan "akan jatuh tempo dalam X hari" sesuai
    `PERINGATAN_JATUH_TEMPO_HARI`.

### Class `Pengaturan` dan `LogStok`

``` python
class Pengaturan(db.Model):
    __tablename__ = "pengaturan"
    kunci = db.Column(db.String(50), primary_key=True)
    nilai = db.Column(db.String(100), nullable=False)
```

-   Tabel bertipe **key-value**: setiap baris adalah satu pasangan
    `kunci` (nama pengaturan, misalnya `"lama_pinjam_hari"`) dan `nilai`
    (nilainya, disimpan sebagai teks). Inilah tabel yang dibaca
    `terapkan_pengaturan()` untuk menimpa nilai default di `config.py`
    dengan nilai yang diatur kepala perpustakaan.
-   `kunci` dijadikan primary key langsung (bukan `id` angka terpisah),
    karena nilainya memang unik per jenis pengaturan.

``` python
class LogStok(db.Model):
    __tablename__ = "log_stok"
    id = db.Column(db.Integer, primary_key=True)
    buku_id = db.Column(db.Integer, db.ForeignKey("buku.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    perubahan = db.Column(db.Integer, nullable=False)
    stok_sesudah = db.Column(db.Integer, nullable=False)
    alasan = db.Column(db.String(100), nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)

    petugas = db.relationship("User", foreign_keys=[user_id])
```

-   Tabel pencatatan riwayat (*log*) setiap kali stok buku diubah manual
    (tambah stok baru, tandai rusak/hilang, dll).
-   `perubahan` --- angka perubahan stok, bisa positif (menambah) atau
    negatif (mengurangi).
-   `stok_sesudah` --- nilai stok setelah perubahan ini, disimpan agar
    riwayat tetap akurat meski stok berubah lagi di kemudian hari.
-   `waktu` --- default `datetime.now` memakai **waktu lokal komputer
    server** (berbeda dari kolom lain yang pakai `datetime.utcnow`,
    seperti di `User.created_at`) --- catatan ini penting karena
    mencampur dua zona waktu berbeda dalam satu aplikasi bisa
    membingungkan saat membaca log.
-   `petugas = db.relationship("User", foreign_keys=[user_id])` ---
    relasi langsung ke `User` yang melakukan perubahan stok, dipakai
    untuk menampilkan nama staf di halaman riwayat log.

> **Ringkasan bab:** Config membaca `.env`; tiap model mewakili satu
> tabel dan relasinya.

## BAB 10 --- Autentikasi dan Manajemen Pengguna

> **File dibahas:** `routes/auth.py`\
> **Tujuan belajar:** Memahami registrasi, login, manajemen pengguna,
> dan persetujuan akun.\
> **Prasyarat:** Bab 9

### 10.1 Import & Setup Blueprint (baris 1--11)

``` python
from datetime import date, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, KartuAnggota, Peminjaman
from utils.decorators import role_required
from utils.kartu import validasi_nim, terbitkan_kartu_jika_belum_ada as _terbitkan_kartu_jika_belum_ada

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
```

-   `Blueprint("auth", __name__, url_prefix="/auth")` --- membuat
    blueprint bernama `"auth"`. Semua route di file ini otomatis diawali
    `/auth/...` berkat `url_prefix`. Nama `"auth"` inilah yang dipakai
    saat memanggil `url_for("auth.login")` di tempat lain.
-   `from utils.kartu import ... as _terbitkan_kartu_jika_belum_ada` ---
    mengimpor fungsi dengan **alias** (nama lain). Garis bawah di depan
    (`_`) adalah konvensi Python untuk menandai "fungsi/variabel ini
    untuk pemakaian internal file ini saja".
-   `login_user`, `logout_user`, `login_required`, `current_user` ---
    semuanya dari Flask-Login: `login_user` menyimpan user ke session,
    `current_user` adalah objek user yang sedang login (atau anonim jika
    belum login), `login_required` adalah dekorator yang memaksa user
    harus login dulu sebelum mengakses route.

``` python
def _email_domain_valid(email):
    from flask import current_app
    domain = email.rsplit("@", 1)[-1].lower() if "@" in email else ""
    allowed = current_app.config.get("ALLOWED_EMAIL_DOMAINS") or []
    return domain in allowed
```

-   Fungsi bantu (helper) untuk validasi domain email.
-   `email.rsplit("@", 1)[-1]` --- `rsplit("@", 1)` memecah string dari
    **kanan**, maksimal 1 kali pemisahan. Contoh:
    `"a@b@gmail.com".rsplit("@", 1)` menghasilkan
    `["a@b", "gmail.com"]`. Ini dipakai supaya jika ada tanda `@` lebih
    dari satu (jarang, tapi tetap ditangani), yang diambil tetap bagian
    **setelah `@` terakhir** (domainnya), bukan ikut terpotong di `@`
    pertama.
-   `if "@" in email else ""` --- jika email tidak mengandung `@` sama
    sekali (input tidak valid), domain dianggap string kosong supaya
    tidak error.
-   `current_app.config.get("ALLOWED_EMAIL_DOMAINS") or []` ---
    mengambil daftar domain valid dari konfigurasi aplikasi; jika entah
    kenapa tidak ada (`None`), dipakai list kosong sebagai cadangan agar
    `in` tidak error.
-   `current_app` --- objek proxy Flask yang mewakili aplikasi yang
    sedang aktif menangani request ini, dipakai di dalam fungsi karena
    `app` tidak bisa diimpor langsung tanpa risiko circular import.

### 10.2 `register()` --- Registrasi Mandiri (baris 23--90)

``` python
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        ...
```

-   `@auth_bp.route("/register", methods=["GET", "POST"])` --- route ini
    menerima dua metode HTTP: `GET` (menampilkan halaman form) dan
    `POST` (mengirim data form).
-   `if request.method == "POST":` --- logika di dalam blok ini hanya
    jalan saat form dikirim; kalau `GET`, langsung lompat ke baris
    terakhir (`return render_template(...)`) untuk menampilkan halaman
    kosong.
-   `request.form.get("username", "").strip()` --- mengambil nilai input
    form bernama `username`. Argumen kedua `""` adalah nilai cadangan
    jika field tidak dikirim. `.strip()` membuang spasi di awal/akhir
    (misalnya user tidak sengaja mengetik spasi sebelum teks).

``` python
        if not all([username, email, nama_lengkap, password]):
            flash("Semua field wajib diisi.", "danger")
            return redirect(url_for("auth.register"))
```

-   `all([...])` --- mengembalikan `True` hanya jika **semua** elemen
    list bernilai *truthy* (tidak kosong). String kosong `""` dianggap
    *falsy*, jadi kondisi ini mendeteksi jika ada field wajib yang belum
    diisi.
-   `flash(pesan, kategori)` --- menyimpan pesan sementara (akan muncul
    sekali di halaman berikutnya, biasanya sebagai notifikasi). Kategori
    (`"danger"`, `"success"`, dll) dipakai untuk menentukan warna/style
    notifikasi.
-   `redirect(url_for("auth.register"))` --- mengarahkan ulang ke
    halaman registrasi (pola **Post/Redirect/Get**: setelah POST
    gagal/berhasil, selalu redirect, bukan langsung render, supaya kalau
    halaman di-refresh user tidak mengirim form yang sama dua kali).

``` python
        if password != password2:
            flash("Konfirmasi password tidak cocok.", "danger")
            return redirect(url_for("auth.register"))
        if len(password) < 6:
            flash("Password minimal 6 karakter.", "danger")
            return redirect(url_for("auth.register"))
        if not _email_domain_valid(email):
            flash("Domain email tidak diizinkan. ...", "danger")
            return redirect(url_for("auth.register"))
        nim, err = validasi_nim(nim_input, wajib=True)
        if err:
            flash(err, "danger")
            return redirect(url_for("auth.register"))
```

-   Serangkaian validasi berurutan, masing-masing langsung `return` jika
    gagal (disebut *early return* / *guard clause*) --- pola ini
    menghindari kode bersarang (`if` di dalam `if` di dalam `if`...)
    yang sulit dibaca.
-   `validasi_nim(nim_input, wajib=True)` --- fungsi dari
    `utils/kartu.py` yang mengembalikan **dua nilai sekaligus** (`nim`,
    `err`) lewat *tuple unpacking*. Jika valid, `err` adalah
    `None`/kosong; jika tidak, berisi pesan error yang langsung
    ditampilkan.

``` python
        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar.", "danger")
            return redirect(url_for("auth.register"))
```

-   `User.query.filter_by(username=username).first()` --- query
    SQLAlchemy: cari baris di tabel `users` dengan `username` yang
    cocok, ambil satu baris pertama saja (`.first()`), hasilnya objek
    `User` jika ketemu atau `None` jika tidak. Dipakai sebagai cek
    duplikat sebelum data baru disimpan --- mencegah error "unique
    constraint" di database.

``` python
        user = User(
            username=username, email=email, nama_lengkap=nama_lengkap,
            nim=nim, role="mahasiswa", status_akun="pending",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
```

-   `User(...)` --- membuat objek baru dari class `User` (belum
    tersimpan ke database, baru ada di memori Python).
-   `role="mahasiswa"` dan `status_akun="pending"` --- **dipaksa**
    (hardcode) di kode, bukan diambil dari form, memastikan registrasi
    publik ini hanya bisa membuat akun mahasiswa berstatus menunggu
    persetujuan, tidak bisa disalahgunakan untuk membuat akun
    staf/kepala lewat form publik.
-   `user.set_password(password)` --- memanggil method di `models.py`
    yang mengubah password mentah menjadi hash sebelum disimpan.
-   `db.session.add(user)` --- menandai objek ini untuk dimasukkan ke
    database (masih di level "staging", belum permanen).
-   `db.session.commit()` --- benar-benar menyimpan perubahan ke
    database (seperti `COMMIT` di SQL).
-   Komentar kode menjelaskan **kartu anggota sengaja belum dibuat di
    sini** --- baru diterbitkan saat akun disetujui (lihat
    `setujui_pengguna()`), supaya masa berlaku kartu dihitung dari
    tanggal disetujui, bukan tanggal daftar.

``` python
        flash("Registrasi berhasil! ...", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")
```

-   Setelah berhasil, user diarahkan ke halaman login (bukan langsung
    dashboard --- karena statusnya masih `"pending"`, belum bisa login).
-   `return render_template("auth/register.html")` --- baris paling
    akhir fungsi (di luar blok `if POST`), ini yang dijalankan jika
    request-nya `GET` (menampilkan form registrasi kosong).

### 10.3 `login()` (baris 93--130)

``` python
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
```

-   Jika user yang mengakses halaman ini **sudah login**, langsung
    diarahkan ke dashboard --- mencegah user yang sudah login melihat
    form login lagi.

``` python
        user = User.query.filter_by(username=username).first()
        if user is None and username:
            user = User.query.filter_by(nim=username).first()
```

-   Login bisa memakai **username ATAU NIM**, dicek lewat satu kolom
    input yang sama.
-   Dicoba dulu sebagai username; kalau tidak ketemu (`user is None`)
    **dan** inputnya tidak kosong, baru dicoba lagi sebagai NIM. Ini
    contoh *fallback logic* bertingkat.

``` python
        if user and user.check_password(password):
            if user.menunggu_persetujuan:
                flash("Akun Anda masih menunggu persetujuan ...", "warning")
                return redirect(url_for("auth.login"))
            if user.ditolak_operator:
                flash("Registrasi akun Anda ditolak ...", "danger")
                return redirect(url_for("auth.login"))
            if not user.is_active_db:
                flash("Akun Anda dinonaktifkan. ...", "danger")
                return redirect(url_for("auth.login"))
            login_user(user)
            flash(f"Selamat datang, {user.nama_lengkap}!", "success")
            return redirect(url_for("dashboard.index"))
        flash("Username/NIM atau password salah.", "danger")
```

-   `if user and user.check_password(password):` --- dua syarat: user
    ditemukan **dan** passwordnya cocok (hash dicocokkan lewat method di
    `models.py`). Python berhenti mengevaluasi `and` di `user` kalau
    `user` adalah `None`, jadi tidak akan error memanggil method pada
    `None`.
-   Tiga pengecekan berurutan setelah password cocok --- menolak login
    meski password benar, jika: akun masih `pending`, akun `ditolak`,
    atau akun dinonaktifkan staf (`is_active_db`). Urutan ini penting:
    password harus dicek dulu, supaya pesan error tidak membocorkan
    informasi status akun ke orang yang tidak tahu passwordnya.
-   `login_user(user)` --- fungsi Flask-Login yang benar-benar menyimpan
    identitas user ke session (membuat user "login").
-   Baris `flash(...)` terakhir **tidak** diikuti `return` langsung di
    dalamnya --- artinya setelah flash, kode jatuh ke baris
    `return render_template("auth/login.html")` di akhir fungsi,
    menampilkan ulang form login dengan pesan error.

### 10.4 `logout()` (baris 133--138)

``` python
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("auth.login"))
```

-   `@login_required` --- dekorator Flask-Login: jika user yang belum
    login mencoba akses route ini, otomatis diarahkan ke `login_view`
    yang sudah diatur di `extensions.py` (`"auth.login"`).
-   `logout_user()` --- menghapus data login dari session.

### 10.5 Manajemen Pengguna (khusus Kepala Perpustakaan) (baris 144--365)

``` python
@auth_bp.route("/pengguna")
@login_required
@role_required("kepala_perpustakaan")
def daftar_pengguna():
    pengguna = User.query.order_by(User.created_at.desc()).all()
    return render_template("auth/daftar_pengguna.html", pengguna=pengguna)
```

-   `@role_required("kepala_perpustakaan")` --- dekorator kustom
    (didefinisikan di `utils/decorators.py`) yang membatasi akses hanya
    untuk role tertentu. Dipasang **setelah** `@login_required`, karena
    harus login dulu baru bisa dicek role-nya.
-   `User.query.order_by(User.created_at.desc()).all()` --- mengambil
    **semua** user, diurutkan berdasarkan tanggal dibuat, `desc()`
    artinya dari yang terbaru ke terlama.

``` python
@auth_bp.route("/pengguna/tambah", methods=["GET", "POST"])
@login_required
@role_required("kepala_perpustakaan")
def tambah_pengguna():
    ...
        if role not in ("mahasiswa", "staf", "kepala_perpustakaan"):
            flash("Role tidak valid.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))
```

-   Fungsi ini mirip `register()`, bedanya: dipakai kepala perpustakaan
    untuk membuat akun **apa saja** (termasuk staf/kepala), dan **role
    diambil dari form** (bukan hardcode `"mahasiswa"`), sehingga perlu
    divalidasi dulu apakah nilainya salah satu dari tiga pilihan yang
    sah.

``` python
        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))
        # BUG LAMA: dulu hanya username yang dicek duplikatnya di sini, email
        # tidak dicek sama sekali -> submit email yang sudah dipakai bikin
        # server error 500 (UNIQUE constraint gagal di database).
        if User.query.filter_by(email=email).first():
            flash("Email sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))
```

-   Komentar di kode ini mencatat riwayat perbaikan bug: sebelumnya
    validasi email duplikat tidak ada, sehingga submit email yang sudah
    dipakai lolos sampai ke database dan baru gagal di sana (menyebabkan
    error server 500 yang tidak ramah untuk user), bukan pesan error
    yang jelas seperti sekarang.

``` python
        user = User(
            username=username, email=email, nama_lengkap=nama_lengkap,
            nim=nim, role=role, status_akun="disetujui",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        kartu = KartuAnggota(
            user_id=user.id,
            tanggal_terbit=date.today(),
            tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config["MASA_BERLAKU_KARTU_HARI"]),
            status="aktif",
        )
        db.session.add(kartu)
        db.session.commit()
```

-   `status_akun="disetujui"` --- berbeda dari `register()`, akun yang
    dibuat kepala perpustakaan langsung disetujui (tidak lewat antrean).
-   `db.session.flush()` --- **mengirim** perintah SQL `INSERT` ke
    database (sehingga `user.id` sudah terisi dengan id baru), tapi
    **belum** commit penuh (transaksi belum ditutup). Ini dipakai karena
    baris berikutnya butuh `user.id` untuk membuat `KartuAnggota`
    (foreign key), padahal id baru ada setelah data user benar-benar
    masuk ke database.
-   `date.today() + timedelta(days=...)` --- menghitung tanggal
    kadaluarsa kartu: hari ini ditambah sejumlah hari dari
    `MASA_BERLAKU_KARTU_HARI` (365 hari, dari `config.py`). `timedelta`
    adalah objek "rentang waktu" dari modul `datetime`, bisa dijumlahkan
    langsung ke objek `date`.
-   `db.session.commit()` di akhir --- baru benar-benar menyimpan
    **kedua** perubahan (user baru dan kartu baru) sekaligus sebagai
    satu transaksi.

``` python
@auth_bp.route("/pengguna/<int:user_id>/toggle-aktif", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def toggle_aktif_pengguna(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Anda tidak bisa menonaktifkan akun sendiri.", "warning")
        return redirect(url_for("auth.daftar_pengguna"))
    user.is_active_db = not user.is_active_db
    db.session.commit()
```

-   `<int:user_id>` di route --- bagian dinamis URL, Flask otomatis
    mengonversi segmen URL ini menjadi `int` dan mengirimkannya sebagai
    argumen fungsi `user_id`.
-   `User.query.get_or_404(user_id)` --- mencari user berdasarkan
    primary key; jika tidak ditemukan, otomatis menampilkan halaman
    error 404, tanpa perlu menulis pengecekan manual.
-   `user.id == current_user.id` --- mencegah kepala perpustakaan
    menonaktifkan akunnya sendiri (yang bisa mengakibatkan dia terkunci
    dari sistem).
-   `user.is_active_db = not user.is_active_db` --- membalik nilai
    boolean (dari `True` jadi `False` atau sebaliknya), cara singkat
    untuk fitur *toggle*.

``` python
@auth_bp.route("/pengguna/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("kepala_perpustakaan")
def edit_pengguna(user_id):
    if user_id == current_user.id:
        flash("Gunakan halaman 'Profil Saya' untuk mengedit akun Anda sendiri.", "info")
        return redirect(url_for("auth.profil"))
    user = User.query.get_or_404(user_id)
```

-   Mengedit akun sendiri **dialihkan** ke halaman "Profil Saya"
    (`profil()`), bukan diproses di sini --- mencegah kepala
    perpustakaan tanpa sadar mengubah role/status akunnya sendiri lewat
    form manajemen pengguna biasa.

``` python
        nim, err = validasi_nim(nim_input, wajib=(role == "mahasiswa"), abaikan_user_id=user.id)
        ...
        duplikat_username = User.query.filter(User.username == username, User.id != user.id).first()
        ...
        if user.is_kepala and role != "kepala_perpustakaan":
            jumlah_kepala = User.query.filter_by(role="kepala_perpustakaan").count()
            if jumlah_kepala <= 1:
                flash("Tidak bisa mengubah role: ini adalah satu-satunya akun kepala perpustakaan yang tersisa.", "warning")
                return redirect(url_for("auth.edit_pengguna", user_id=user.id))
```

-   `abaikan_user_id=user.id` --- saat validasi NIM untuk fitur
    **edit**, NIM milik user ini sendiri harus dikecualikan dari
    pengecekan "sudah dipakai orang lain", kalau tidak, NIM miliknya
    sendiri akan selalu dianggap duplikat.
-   `User.query.filter(User.username == username, User.id != user.id)`
    --- perhatikan ini pakai `.filter()` (bukan `.filter_by()`), yang
    menerima ekspresi perbandingan langsung (`User.id != user.id`) ---
    dipakai saat butuh kondisi lebih dari sekadar `kolom=nilai`, di sini
    untuk mengecualikan baris user itu sendiri.
-   Blok pengecekan jumlah kepala perpustakaan --- mencegah role
    satu-satunya akun kepala diturunkan, yang bisa membuat sistem
    **kehilangan seluruh akses admin tertinggi** (tidak ada yang bisa
    menyetujui akun baru atau mengatur sistem lagi).

``` python
        user.username = username
        ...
        if password_baru:
            user.set_password(password_baru)
        _terbitkan_kartu_jika_belum_ada(user)
        db.session.commit()
```

-   Baris-baris `user.xxx = yyy` **langsung mengubah atribut objek**
    yang sudah diambil dari database tadi
    (`user = User.query.get_or_404(...)`) --- SQLAlchemy otomatis
    melacak perubahan ini, cukup `db.session.commit()` di akhir tanpa
    perlu `db.session.add(user)` lagi (karena objeknya sudah "dikenal"
    sesi database).
-   `if password_baru:` --- reset password bersifat **opsional**; kalau
    field dikosongkan, password lama tetap dipakai.
-   `_terbitkan_kartu_jika_belum_ada(user)` --- dipanggil untuk
    jaga-jaga, kalau user ini adalah akun lama (dibuat sebelum fitur
    kartu digital ada) dan belum punya kartu sama sekali.

``` python
@auth_bp.route("/pengguna/<int:user_id>/hapus", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def hapus_pengguna(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Anda tidak bisa menghapus akun sendiri.", "warning")
        return redirect(url_for("auth.daftar_pengguna"))
    if user.is_kepala:
        jumlah_kepala = User.query.filter_by(role="kepala_perpustakaan").count()
        if jumlah_kepala <= 1:
            flash("Tidak bisa menghapus: ini adalah satu-satunya akun kepala perpustakaan yang tersisa.", "warning")
            return redirect(url_for("auth.daftar_pengguna"))
```

-   Dua pengamanan sebelum hapus: tidak bisa hapus diri sendiri, dan
    tidak bisa menghapus kepala perpustakaan terakhir --- melindungi
    sistem dari kehilangan akses admin sepenuhnya.

``` python
    ada_aktif = Peminjaman.query.filter(
        Peminjaman.user_id == user.id,
        Peminjaman.status.in_(["diajukan", "dipinjam"]),
    ).first()
    if ada_aktif:
        flash(f"Tidak bisa menghapus '{user.username}': masih ada pengajuan/peminjaman aktif. ...", "warning")
        return redirect(url_for("auth.daftar_pengguna"))
```

-   Pengamanan tambahan: user dengan peminjaman yang **masih aktif**
    (belum dikembalikan/ditolak) tidak boleh dihapus, supaya data buku
    yang sedang dipinjam tetap konsisten (tidak kehilangan jejak siapa
    yang sedang memegang buku apa).

``` python
    username = user.username
    riwayat_lama = Peminjaman.query.filter_by(user_id=user.id).count()
    db.session.delete(user)
    db.session.commit()
    pesan = f"Akun '{username}' berhasil dihapus."
    if riwayat_lama:
        pesan += f" ({riwayat_lama} riwayat peminjaman lama miliknya ikut terhapus.)"
    flash(pesan, "success")
```

-   `username = user.username` --- nilai disimpan dulu ke variabel
    **sebelum** objeknya dihapus, karena setelah
    `db.session.delete(user)` dan `commit()`, mengakses `user.username`
    berisiko error (objeknya sudah tidak valid di database).
-   `db.session.delete(user)` --- menghapus baris ini; karena
    `cascade="all, delete-orphan"` di relasi `models.py`, kartu dan
    riwayat peminjaman milik user ini ikut terhapus otomatis (ini
    konsisten dengan pengecekan "tidak ada peminjaman **aktif**" tadi
    --- yang ikut terhapus hanya riwayat yang **sudah selesai**, seperti
    `dikembalikan`/`ditolak`).
-   Pesan sukses dibuat dinamis, menyebutkan jumlah riwayat lama yang
    ikut terhapus jika ada.

### 10.6 `profil()` --- Edit Profil Sendiri (baris 372--420)

``` python
@auth_bp.route("/profil", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def profil():
```

-   `@role_required("staf", "kepala_perpustakaan")` --- dekorator ini
    menerima **lebih dari satu** role yang diizinkan (mahasiswa tidak
    termasuk, karena mahasiswa tidak punya menu profil staf semacam
    ini).

``` python
        if password_baru or password_baru2 or (password_lama and not current_user.is_kepala):
            if not current_user.is_kepala and not current_user.check_password(password_lama):
                flash("Password lama yang dimasukkan salah.", "danger")
                return redirect(url_for("auth.profil"))
            if password_baru != password_baru2:
                ...
            if len(password_baru) < 6:
                ...
            current_user.set_password(password_baru)
```

-   Logika ganti password di sini **opsional** --- hanya diproses jika
    salah satu field password diisi.
-   Catatan di komentar kode: kepala perpustakaan (role tertinggi)
    **tidak perlu** memasukkan password lama untuk mengganti password,
    sedangkan staf tetap wajib --- aturan ini tercermin di
    `not current_user.is_kepala` pada pengecekan password lama.

``` python
        current_user.email = email
        current_user.nama_lengkap = nama_lengkap
        current_user.no_telepon = no_telepon or None
        current_user.alamat = alamat or None
        _terbitkan_kartu_jika_belum_ada(current_user)
        db.session.commit()
```

-   `no_telepon or None` --- jika `no_telepon` adalah string kosong
    (*falsy*), disimpan sebagai `None` (NULL di database) daripada
    string kosong --- kebiasaan baik agar data kosong konsisten
    direpresentasikan sebagai NULL, bukan campuran NULL dan `""`.
-   Perhatikan di sini langsung memakai `current_user` (bukan mengambil
    ulang `User.query.get(...)`), karena `current_user` dari Flask-Login
    **adalah** objek user yang sedang login itu sendiri.

### 10.7 Persetujuan Akun Baru (baris 428--483)

``` python
@auth_bp.route("/pengguna/persetujuan")
@login_required
@role_required("kepala_perpustakaan")
def daftar_persetujuan():
    pending = (
        User.query.filter_by(role="mahasiswa", status_akun="pending")
        .order_by(User.created_at.asc())
        .all()
    )
    return render_template("auth/persetujuan.html", pending=pending)
```

-   Menampilkan daftar akun mahasiswa yang menunggu persetujuan,
    diurutkan `asc()` (dari yang paling lama mendaftar) --- supaya
    antrean diproses berurutan (yang mendaftar duluan, ditinjau duluan).

``` python
@auth_bp.route("/pengguna/<int:user_id>/setujui", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def setujui_pengguna(user_id):
    user = User.query.get_or_404(user_id)
    if user.status_akun != "pending":
        flash("Akun ini sudah pernah diproses sebelumnya.", "warning")
        return redirect(url_for("auth.daftar_persetujuan"))
    user.status_akun = "disetujui"
    if not user.kartu:
        kartu = KartuAnggota(
            user_id=user.id,
            tanggal_terbit=date.today(),
            tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config["MASA_BERLAKU_KARTU_HARI"]),
            status="aktif",
        )
        db.session.add(kartu)
    db.session.commit()
```

-   `if user.status_akun != "pending":` --- pengaman supaya akun yang
    sudah diproses (disetujui/ditolak sebelumnya) tidak bisa diproses
    ulang secara tidak sengaja (misalnya tombol di-klik dua kali, atau
    dua kepala perpustakaan membuka halaman yang sama bersamaan).
-   `if not user.kartu:` --- hanya membuat kartu baru jika user **belum
    punya** kartu (`user.kartu` memakai relationship yang didefinisikan
    di `models.py`, akan bernilai `None` jika belum ada kartu terkait).
-   Di sinilah tanggal kadaluarsa kartu dihitung dari **tanggal
    disetujui** (bukan tanggal daftar), sesuai catatan di `register()`
    sebelumnya.

``` python
@auth_bp.route("/pengguna/<int:user_id>/tolak", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def tolak_pengguna(user_id):
    user = User.query.get_or_404(user_id)
    if user.status_akun != "pending":
        flash("Akun ini sudah pernah diproses sebelumnya.", "warning")
        return redirect(url_for("auth.daftar_persetujuan"))
    user.status_akun = "ditolak"
    user.is_active_db = False
    db.session.commit()
```

-   Menolak pendaftaran: status diubah jadi `"ditolak"`, dan
    `is_active_db` juga dipaksa `False` sebagai lapis pengaman tambahan
    (meski status `ditolak` saja sebenarnya sudah diblok di fungsi
    `login()`).

> **Ringkasan bab:** Mahasiswa mendaftar → pending → disetujui kepala →
> bisa login.

## BAB 11 --- Manajemen Data Buku

> **File dibahas:** `routes/buku.py`\
> **Tujuan belajar:** Memahami pengelolaan buku, kategori, sampul, serta
> import/ekspor Excel.\
> **Prasyarat:** Bab 9

### 11.1 Import & Fungsi Bantu (baris 1--58)

``` python
import os
import uuid
from collections import OrderedDict
from werkzeug.utils import secure_filename
...
buku_bp = Blueprint("buku", __name__, url_prefix="/buku")
```

-   `uuid` --- modul untuk membuat ID unik acak, dipakai nanti untuk
    menamai file upload supaya tidak bentrok.
-   `OrderedDict` --- dictionary yang **mengingat urutan key**
    dimasukkan (di Python versi modern, dictionary biasa sebenarnya
    sudah begitu juga, tapi `OrderedDict` dipakai di sini untuk
    menegaskan maksud: urutan kategori harus sesuai urutan ditambahkan).
-   `secure_filename` --- fungsi dari Werkzeug yang "membersihkan" nama
    file dari karakter berbahaya (misalnya `../../etc/passwd`), penting
    untuk keamanan saat menyimpan file yang diunggah user.

``` python
def _allowed_image(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXT"]
```

-   `filename.rsplit(".", 1)[-1]` --- mengambil ekstensi file dengan
    memecah string dari kanan di tanda titik terakhir. Contoh:
    `"foto.sampul.jpg".rsplit(".", 1)` → `["foto.sampul", "jpg"]`,
    diambil elemen terakhir `"jpg"`.
-   Hasil dicocokkan dengan set `ALLOWED_IMAGE_EXT` dari `config.py`
    (`{"png", "jpg", "jpeg", "webp"}`).

``` python
def _simpan_sampul(file_storage):
    if not file_storage or file_storage.filename == "":
        return None
    if not _allowed_image(file_storage.filename):
        flash("Format gambar tidak didukung (gunakan png/jpg/jpeg/webp).", "warning")
        return None

    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    nama_unik = f"{uuid.uuid4().hex}.{ext}"
    nama_aman = secure_filename(nama_unik)
    path_lengkap = os.path.join(current_app.config["UPLOAD_FOLDER"], nama_aman)
    file_storage.save(path_lengkap)
    return f"uploads/sampul/{nama_aman}"
```

-   `if not file_storage or file_storage.filename == "":` --- jika user
    tidak memilih file sama sekali (field upload dikosongkan), fungsi
    berhenti dan mengembalikan `None` (artinya "tidak ada perubahan
    sampul").
-   `uuid.uuid4().hex` --- menghasilkan string acak unik (contoh:
    `"a1b2c3d4..."`). Dipakai sebagai nama file baru, **bukan** nama
    asli dari user, supaya: (1) tidak ada dua file bentrok nama, (2)
    nama file asli yang mungkin aneh/berbahaya tidak ikut dipakai.
-   `secure_filename(nama_unik)` --- tetap dipanggil sebagai lapis
    keamanan tambahan meski nama sudah dibuat sendiri dari UUID.
-   `os.path.join(...)` --- menggabungkan folder upload dengan nama
    file, otomatis memakai pemisah path yang benar sesuai OS (`\` di
    Windows, `/` di Linux/Mac) --- dipakai di sini karena ini operasi
    **sistem file** di server.
-   `file_storage.save(path_lengkap)` --- benar-benar menulis file ke
    disk.
-   `return f"uploads/sampul/{nama_aman}"` --- path yang **disimpan ke
    database** sengaja ditulis manual dengan `/` (bukan `os.path.join`),
    karena path ini nantinya dipakai di template HTML lewat
    `url_for('static', ...)` yang selalu mengharapkan format URL
    (forward-slash), bukan format path sistem operasi.

``` python
def _isbn_duplikat(isbn, kecuali_id=None):
    if not isbn:
        return None
    q = Buku.query.filter(Buku.isbn == isbn)
    if kecuali_id:
        q = q.filter(Buku.id != kecuali_id)
    return q.first()
```

-   Fungsi ini dipakai ulang oleh `tambah_buku()` dan `edit_buku()` ---
    contoh praktik **DRY** (*Don't Repeat Yourself*): logika pengecekan
    ISBN duplikat ditulis sekali, dipanggil di banyak tempat.
-   `kecuali_id` --- parameter opsional, dipakai saat **edit**: ISBN
    milik buku yang sedang diedit itu sendiri harus dikecualikan dari
    pengecekan duplikat (mirip pola `abaikan_user_id` di `auth.py`).
-   Query dibangun bertahap (`q = ...`, lalu `q = q.filter(...)` lagi
    jika perlu) --- menunjukkan query SQLAlchemy bisa dirangkai/ditambah
    secara kondisional sebelum dieksekusi dengan `.first()`.

``` python
def _lama_pinjam_form():
    nilai = request.form.get("lama_pinjam_hari", type=int)
    return nilai if nilai and 1 <= nilai <= 365 else None
```

-   `request.form.get(..., type=int)` --- parameter `type=int` otomatis
    mengonversi nilai form ke integer; jika gagal/kosong, hasilnya
    `None` (bukan error).
-   Ekspresi *conditional* (`x if kondisi else y`) --- mengembalikan
    nilai hanya jika valid (ada isinya **dan** dalam rentang wajar
    1--365 hari); di luar itu dianggap `None` (ikut pengaturan umum,
    bukan error).

### 11.2 `daftar_buku()` --- Daftar & Pencarian (baris 64--112)

``` python
@buku_bp.route("/")
@login_required
def daftar_buku():
    q = request.args.get("q", "").strip()
    kategori_id = request.args.get("kategori_id", type=int)

    query = Buku.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Buku.judul.ilike(like), Buku.penulis.ilike(like), Buku.isbn.ilike(like))
        )
    if kategori_id:
        query = query.filter(Buku.kategori_id == kategori_id)
```

-   `request.args.get(...)` --- berbeda dari `request.form` (data dari
    form POST), `request.args` mengambil data dari **query string URL**
    (contoh: `/buku/?q=python&kategori_id=2`), biasa dipakai untuk
    pencarian/filter lewat `GET`.
-   `query = Buku.query` lalu ditambah filter secara bertahap --- pola
    *query builder*: filter pencarian dan filter kategori masing-masing
    **opsional**, hanya ditambahkan ke query jika parameternya memang
    dikirim.
-   `like = f"%{q}%"` --- menyusun pola `LIKE` SQL: tanda `%` berarti
    "apa saja sebelum/sesudah teks ini", sehingga pencarian menemukan
    kecocokan di bagian mana pun teks, bukan hanya yang persis sama.
-   `db.or_(... , ... , ...)` --- menggabungkan tiga kondisi dengan
    logika **OR**: baris ditemukan jika judul **atau** penulis **atau**
    ISBN mengandung kata kunci pencarian.
-   `.ilike(like)` --- versi `LIKE` yang **tidak membedakan huruf
    besar/kecil** (*case-insensitive*), supaya pencarian "python" tetap
    menemukan "Python" atau "PYTHON".

``` python
    daftar = query.order_by(Buku.judul.asc()).all()
    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()

    buku_id_aktif = set()
    maks_pinjam = current_app.config["MAKS_PINJAM_PER_USER"]
    jumlah_aktif = 0
    if current_user.is_mahasiswa:
        aktif = Peminjaman.query.filter(
            Peminjaman.user_id == current_user.id,
            Peminjaman.status.in_(["diajukan", "dipinjam"]),
        ).all()
        buku_id_aktif = {p.buku_id for p in aktif}
        jumlah_aktif = len(aktif)
    kuota_penuh = jumlah_aktif >= maks_pinjam
```

-   Query baru benar-benar dieksekusi di sini lewat `.all()` (semua
    baris filter sebelumnya baru "rencana query" sampai
    `.all()`/`.first()`/`.count()` dipanggil).
-   `if current_user.is_mahasiswa:` --- blok ini **hanya** dijalankan
    untuk role mahasiswa, karena fitur kuota peminjaman hanya relevan
    untuk mereka (staf/kepala tidak "meminjam" lewat sistem ini).
-   `{p.buku_id for p in aktif}` --- ini **set comprehension**, membuat
    kumpulan `buku_id` dari semua peminjaman aktif milik user, dipakai
    nanti di template untuk menandai buku mana saja yang sudah
    diajukan/dipinjam user ini (misalnya menampilkan tombol berbeda).
-   Komentar kode menjelaskan ini **sengaja dihitung sekali di sini**
    (bukan per baris buku di template), supaya tidak melakukan query
    database berulang kali untuk tiap buku yang ditampilkan (praktik
    menghindari masalah performa "N+1 query").

``` python
    kelompok = OrderedDict()
    for kat in kategori_list:
        buku_kat = [b for b in daftar if b.kategori_id == kat.id]
        if buku_kat:
            kelompok[kat.nama_kategori] = buku_kat
    tanpa_kategori = [b for b in daftar if not b.kategori_id]
    if tanpa_kategori:
        kelompok["Tanpa Kategori"] = tanpa_kategori
```

-   Mengelompokkan daftar buku (yang sudah diambil dari database) **di
    level Python**, bukan lewat query terpisah per kategori --- karena
    data `daftar` sudah ada di memori, lebih efisien memfilternya
    langsung dengan *list comprehension* daripada query ulang ke
    database untuk tiap kategori.
-   `if buku_kat:` --- kategori yang **tidak punya buku** (sesuai filter
    pencarian saat ini) tidak dimasukkan ke `kelompok`, supaya tidak
    menampilkan rak kosong di halaman.
-   Buku tanpa kategori (`kategori_id` kosong) dikumpulkan terpisah di
    bawah label `"Tanpa Kategori"`.

### 11.3 `detail_buku()` (baris 115--133)

``` python
@buku_bp.route("/<int:buku_id>")
@login_required
def detail_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    pengajuan_aktif = None
    if current_user.is_mahasiswa:
        pengajuan_aktif = Peminjaman.query.filter(
            Peminjaman.user_id == current_user.id,
            Peminjaman.buku_id == buku.id,
            Peminjaman.status.in_(["diajukan", "dipinjam"]),
        ).first()

    maks_pinjam = current_app.config["MAKS_PINJAM_PER_USER"]
    jumlah_aktif = current_user.jumlah_pinjaman_aktif if current_user.is_mahasiswa else 0
```

-   Mirip `daftar_buku()` tapi untuk **satu buku spesifik**: mengecek
    apakah mahasiswa yang sedang login sudah punya pengajuan/pinjaman
    aktif untuk **buku ini saja** (tiga kondisi filter sekaligus: user,
    buku, status).
-   `jumlah_aktif = current_user.jumlah_pinjaman_aktif if ... else 0`
    --- di sini memakai **property** yang sudah didefinisikan di
    `models.py` (`User.jumlah_pinjaman_aktif`), berbeda dari
    `daftar_buku()` yang menghitungnya manual lewat query --- keduanya
    menghasilkan nilai yang sama, hanya beda cara (menunjukkan kode yang
    ditulis di waktu berbeda tidak selalu konsisten gaya penulisannya).

### 11.4 `tambah_buku()` & `edit_buku()` (baris 139--214)

``` python
@buku_bp.route("/tambah", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def tambah_buku():
    if request.method == "POST":
        ...
        stok = max(0, request.form.get("stok", type=int, default=0) or 0)
```

-   `request.form.get("stok", type=int, default=0)` --- jika field
    `stok` kosong/tidak valid sebagai angka, langsung dipakai
    `default=0` oleh Flask sendiri.
-   `... or 0` --- lapis pengaman tambahan jika hasilnya tetap `None`
    (misalnya pada versi Flask tertentu `default` dan `type`
    berinteraksi beda), memastikan nilainya tidak pernah `None` sebelum
    dibandingkan dengan `max()`.
-   `max(0, ...)` --- mencegah nilai stok negatif (jika user iseng
    memasukkan angka minus).

``` python
        ada = _isbn_duplikat(isbn)
        if ada:
            flash(f"ISBN {isbn} sudah terdaftar untuk buku '{ada.judul}'. "
                  "Jika ini eksemplar tambahan, tambahkan stok pada buku tersebut.", "warning")
            return redirect(url_for("buku.tambah_buku"))
        sampul_path = _simpan_sampul(request.files.get("sampul"))
```

-   Pesan error di sini cukup informatif: bukan sekadar "ISBN sudah
    ada", tapi juga memberi **saran tindakan** (tambah stok ke buku yang
    sudah ada, bukan buat entri baru) --- ini desain yang membantu
    pengguna, bukan sekadar validasi teknis.
-   `request.files.get("sampul")` --- berbeda dari `request.form`,
    `request.files` khusus untuk data file yang diunggah lewat form
    (`<input type="file">`).

``` python
        buku = Buku(
            judul=judul, penulis=penulis, penerbit=penerbit or None,
            tahun_terbit=tahun_terbit, isbn=isbn or None, kategori_id=kategori_id or None,
            deskripsi=deskripsi or None, stok=stok, sampul_path=sampul_path,
            lokasi_rak=lokasi_rak, lama_pinjam_hari=_lama_pinjam_form(),
        )
        db.session.add(buku)
        db.session.commit()
```

-   Pola `nilai or None` diulang untuk banyak field opsional ---
    mengubah string kosong jadi `None`/NULL secara konsisten (sama
    seperti di `profil()` pada `auth.py`).

``` python
@buku_bp.route("/<int:buku_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def edit_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    if request.method == "POST":
        isbn_baru = request.form.get("isbn", "").strip()
        ada = _isbn_duplikat(isbn_baru, kecuali_id=buku.id)
        ...
        buku.judul = request.form.get("judul", "").strip()
        ...
        sampul_baru = _simpan_sampul(request.files.get("sampul"))
        if sampul_baru:
            buku.sampul_path = sampul_baru
```

-   `if sampul_baru:` --- sampul **hanya** diganti jika user benar-benar
    mengunggah file baru (`_simpan_sampul` mengembalikan `None` jika
    field kosong). Jika tidak, `buku.sampul_path` lama tetap
    dipertahankan --- mencegah sampul lama "terhapus" tanpa sengaja
    kalau user cuma mau mengedit judul tanpa mengganti gambar.
-   Perhatikan: file sampul **lama** yang digantikan tidak dihapus dari
    disk di kode ini --- artinya file lama tetap tersimpan (jadi "file
    sampah") meski sudah tidak dipakai lagi; ini bukan bug yang fatal,
    tapi berarti folder upload bisa terus bertambah ukurannya seiring
    waktu.

### 11.5 `hapus_buku()` (baris 217--244)

``` python
@buku_bp.route("/<int:buku_id>/hapus", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def hapus_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    # BUG LAMA: buku bisa langsung dihapus meski masih ada pengajuan/peminjaman
    # aktif atasnya. ...
    ada_aktif = Peminjaman.query.filter(
        Peminjaman.buku_id == buku.id,
        Peminjaman.status.in_(["diajukan", "dipinjam"]),
    ).first()
    if ada_aktif:
        flash(f"Tidak bisa menghapus '{buku.judul}': masih ada pengajuan/peminjaman aktif atas buku ini. "
              "Selesaikan (kembalikan/tolak) dulu.", "warning")
        return redirect(url_for("buku.daftar_buku"))
```

-   Catatan: hanya `role_required("kepala_perpustakaan")` (tanpa
    `"staf"`) --- berbeda dari `tambah_buku()`/`edit_buku()` yang
    mengizinkan staf juga. Artinya menghapus buku adalah tindakan yang
    dianggap lebih sensitif, dibatasi hanya untuk kepala perpustakaan.
-   Komentar "BUG LAMA" di kode ini sama polanya dengan yang di
    `auth.py` --- mendokumentasikan riwayat perbaikan: sebelumnya
    penghapusan buku tidak mengecek peminjaman aktif, sehingga karena
    `cascade="all, delete-orphan"` di `models.py`, menghapus buku
    **otomatis ikut menghapus** seluruh riwayat peminjamannya ---
    termasuk yang sedang berjalan, membuat data sirkulasi jadi kacau
    (ada mahasiswa yang "sedang pinjam buku" tapi bukunya sudah tidak
    ada catatannya sama sekali).

### 11.6 `ekspor_buku()` --- Unduh Excel (baris 247--268)

``` python
@buku_bp.route("/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_buku():
    from datetime import date
    daftar = Buku.query.order_by(Buku.judul).all()
    baris = [
        [b.judul, b.penulis, b.penerbit or "", b.tahun_terbit or "", b.isbn or "",
         b.kategori.nama_kategori if b.kategori else "", b.stok, b.lokasi_rak or "",
         b.lama_pinjam_hari or ""]
        for b in daftar
    ]
    buffer = buat_excel(
        "Koleksi Buku",
        ["Judul", "Penulis", "Penerbit", "Tahun", "ISBN", "Kategori", "Stok", "Lokasi Rak", "Lama Pinjam (hari)"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True, download_name=f"koleksi_buku_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
```

-   `baris = [ [...] for b in daftar ]` --- *list comprehension* yang
    mengubah setiap objek `Buku` menjadi satu baris list data mentah,
    siap dipakai fungsi pembuat Excel (yang tidak perlu tahu apa-apa
    soal model `Buku`, hanya menerima list/list --- memisahkan tanggung
    jawab antara "logika data" dan "logika format file").
-   `b.kategori.nama_kategori if b.kategori else ""` --- memakai relasi
    `backref="kategori"` yang didefinisikan di `models.py` pada class
    `Kategori`; jika buku tidak punya kategori (`None`), ditampilkan
    string kosong, bukan error.
-   `buat_excel(...)` --- fungsi dari `utils/excel_export.py` yang
    menerima judul sheet, header kolom, dan data baris, mengembalikan
    **buffer** (data file di memori, bukan file fisik di disk).
-   `send_file(buffer, as_attachment=True, download_name=..., mimetype=...)`
    --- mengirim isi buffer sebagai **file download**, bukan ditampilkan
    sebagai halaman web. `as_attachment=True` memicu browser membuka
    dialog "Save As" alih-alih mencoba menampilkan isinya langsung.
-   `date.today().isoformat()` --- nama file dibuat dinamis menyertakan
    tanggal unduh (format ISO: `YYYY-MM-DD`), supaya file lama dan baru
    mudah dibedakan.

### 11.7 Kategori Buku (baris 274--311)

``` python
@buku_bp.route("/kategori", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def kategori():
    if request.method == "POST":
        nama = request.form.get("nama_kategori", "").strip()
        if nama and not Kategori.query.filter_by(nama_kategori=nama).first():
            db.session.add(Kategori(nama_kategori=nama))
            db.session.commit()
            flash(f"Kategori '{nama}' ditambahkan.", "success")
        else:
            flash("Kategori kosong atau sudah ada.", "warning")
        return redirect(url_for("buku.kategori"))
```

-   `if nama and not Kategori.query.filter_by(nama_kategori=nama).first():`
    --- satu kondisi gabungan: nama tidak boleh kosong **dan** belum ada
    kategori dengan nama yang sama. Jika salah satu gagal, masuk ke
    cabang `else` dengan satu pesan error umum untuk kedua kasus.

``` python
@buku_bp.route("/kategori/<int:kategori_id>/hapus", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def hapus_kategori(kategori_id):
    """Hapus kategori. Buku di dalamnya TIDAK ikut terhapus: buku tsb menjadi
    'Tanpa Kategori' (kategori_id di-set NULL)."""
    kat = Kategori.query.get_or_404(kategori_id)
    nama = kat.nama_kategori
    jumlah_buku = len(kat.buku_list)
    for b in list(kat.buku_list):
        b.kategori_id = None
    db.session.delete(kat)
    db.session.commit()
```

-   Berbeda dari relasi `User`→`KartuAnggota`/`Peminjaman` yang pakai
    `cascade="all, delete-orphan"`, relasi `Kategori`→`Buku` di
    `models.py` **tidak** memakai cascade --- artinya menghapus kategori
    **tidak** otomatis menghapus bukunya. Namun kode di sini tetap perlu
    menangani manual: tiap buku di kategori itu diputus relasinya
    (`kategori_id = None`) **sebelum** kategorinya dihapus.
-   `for b in list(kat.buku_list):` --- perhatikan `kat.buku_list`
    dibungkus `list(...)` saat diiterasi sambil **diubah isinya**
    (`b.kategori_id = None` menyebabkan relasi berubah). Ini kebiasaan
    aman: mengubah koleksi yang sedang di-looping bisa menyebabkan
    perilaku tak terduga, jadi dibuat salinan list-nya dulu sebelum
    diubah-ubah.

### 11.8 Import/Export Excel (baris 317--351)

``` python
@buku_bp.route("/template-excel")
@login_required
@role_required("staf", "kepala_perpustakaan")
def download_template_excel():
    buffer = buat_template_excel()
    return send_file(buffer, as_attachment=True, download_name="template_import_buku.xlsx", mimetype="...")
```

-   Menyediakan file template kosong (dibuat oleh
    `utils/excel_import.py`) yang bisa diisi staf secara offline, lalu
    diunggah lewat `import_excel()` di bawah --- pola umum fitur impor
    massal: sediakan format yang sudah pasti benar, supaya proses impor
    lebih sedikit gagal karena format salah.

``` python
@buku_bp.route("/import-excel", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def import_excel():
    if request.method == "POST":
        file = request.files.get("file_excel")
        if not file or file.filename == "":
            flash("Pilih file Excel (.xlsx) terlebih dahulu.", "danger")
            return redirect(url_for("buku.import_excel"))
        if not file.filename.lower().endswith(".xlsx"):
            flash("File harus berformat .xlsx", "danger")
            return redirect(url_for("buku.import_excel"))

        sukses, errors = import_buku_dari_excel(file.stream)
        flash(f"{sukses} buku berhasil diimport.", "success" if sukses else "warning")
        for err in errors[:20]:
            flash(err, "warning")
        return redirect(url_for("buku.daftar_buku"))
```

-   Dua pengecekan sebelum file diproses: file memang ada (tidak kosong)
    dan ekstensinya benar `.xlsx` --- validasi sederhana di level route
    sebelum file dibuka/dibaca sama sekali.
-   `import_buku_dari_excel(file.stream)` --- `file.stream` adalah data
    mentah file yang diunggah (belum disimpan ke disk), langsung
    diproses di memori oleh fungsi di `utils/excel_import.py`, yang
    mengembalikan **dua nilai**: jumlah baris sukses, dan list pesan
    error per baris yang gagal (misalnya format kolom salah, data tidak
    lengkap).
-   `flash(f"...", "success" if sukses else "warning")` --- kategori
    pesan dipilih secara dinamis: jika tidak ada satu pun baris yang
    berhasil, pesan ditampilkan sebagai peringatan (warning), bukan
    sukses.
-   `for err in errors[:20]:` --- hanya menampilkan **maksimal 20**
    pesan error pertama, meski mungkin ada ratusan baris gagal ---
    mencegah halaman dibanjiri ratusan notifikasi flash sekaligus jika
    file yang diunggah memang sangat bermasalah.

> **Ringkasan bab:** CRUD buku + pencarian + Excel, dengan hak akses
> staf/kepala.

## BAB 12 --- Alur Peminjaman Buku

> **File dibahas:** `routes/peminjaman.py`\
> **Tujuan belajar:** Memahami alur peminjaman: pengajuan, persetujuan,
> pengembalian, perpanjangan, riwayat.\
> **Prasyarat:** Bab 9, 17

### 12.1 Pengajuan Mandiri oleh Mahasiswa (baris 18--73)

``` python
@peminjaman_bp.route("/ajukan/<int:buku_id>", methods=["POST"])
@login_required
@role_required("mahasiswa")
def ajukan_peminjaman(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    if buku.stok <= 0:
        flash("Stok buku habis, pengajuan tidak dapat dibuat.", "danger")
        return redirect(url_for("buku.detail_buku", buku_id=buku_id))
```

-   Route ini hanya menerima `methods=["POST"]` (tanpa `"GET"`) ---
    artinya tidak ada halaman form terpisah untuk ini; aksinya langsung
    dipicu dari tombol di halaman detail buku (`buku/detail.html`),
    sesuai kerangka URL yang dikembalikan oleh
    `redirect(url_for("buku.detail_buku", ...))` di setiap jalur.
-   Pengecekan stok dilakukan **paling awal**, sebelum validasi lain ---
    jika stok 0, tidak perlu memeriksa hal lain sama sekali.

``` python
    aktif = Peminjaman.query.filter(
        Peminjaman.user_id == current_user.id,
        Peminjaman.buku_id == buku.id,
        Peminjaman.status.in_(["diajukan", "dipinjam"]),
    ).first()
    if aktif:
        flash("Anda sudah memiliki pengajuan/peminjaman aktif untuk buku ini.", "warning")
        return redirect(url_for("buku.detail_buku", buku_id=buku_id))

    ok, pesan = cek_bisa_meminjam(current_user)
    if not ok:
        flash(pesan, "danger")
        return redirect(url_for("buku.detail_buku", buku_id=buku_id))
```

-   Cek pengajuan ganda: mencegah satu mahasiswa mengajukan buku yang
    **sama** dua kali sebelum pengajuan pertamanya selesai diproses.
-   `ok, pesan = cek_bisa_meminjam(current_user)` --- memanggil fungsi
    dari `utils/pinjam.py` yang mengembalikan dua nilai sekaligus:
    boolean (boleh/tidak) dan pesan penjelasan jika tidak boleh
    (misalnya kuota penuh atau kartu kadaluarsa) --- pola yang sama
    seperti `validasi_nim()` di `auth.py`.

``` python
    pengajuan = Peminjaman(
        user_id=current_user.id,
        buku_id=buku.id,
        tanggal_pinjam=date.today(),
        tanggal_jatuh_tempo=hitung_jatuh_tempo(buku, date.today()),
        status="diajukan",
    )
    db.session.add(pengajuan)
    db.session.commit()
```

-   `hitung_jatuh_tempo(buku, date.today())` --- fungsi dari
    `utils/pinjam.py` yang menentukan tanggal jatuh tempo, kemungkinan
    mempertimbangkan `buku.lama_pinjam_hari` (lama pinjam khusus buku
    ini) atau nilai umum `LAMA_PINJAM_HARI` jika kosong.
-   Perhatikan: `tanggal_jatuh_tempo` **sudah dihitung dan disimpan**
    meski status masih `"diajukan"` (belum disetujui) --- supaya saat
    nanti disetujui staf, tanggal ini sudah ada (lalu dihitung ulang
    persis di `setujui_pengajuan()` memakai tanggal persetujuan
    sebenarnya).

``` python
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
```

-   `if p.user_id != current_user.id: abort(403)` --- pengecekan
    kepemilikan **penting untuk keamanan**: mencegah mahasiswa A
    membatalkan pengajuan milik mahasiswa B hanya dengan menebak-nebak
    `peminjaman_id` di URL (disebut *Insecure Direct Object Reference*,
    salah satu celah keamanan umum di web). `abort(403)` menampilkan
    halaman error "Forbidden".
-   Pembatalan memakai `db.session.delete(p)` --- menghapus barisnya
    sepenuhnya dari database (berbeda dari `tolak_pengajuan()` di bawah
    yang hanya **mengubah status** menjadi `"ditolak"`, tetap menyimpan
    riwayatnya). Ini masuk akal: pembatalan oleh mahasiswa sendiri
    dianggap "tidak jadi mengajukan", sementara penolakan staf adalah
    keputusan yang perlu dicatat sebagai riwayat.

### 12.2 Tinjauan Pengajuan oleh Staf/Kepala (baris 79--146)

``` python
@peminjaman_bp.route("/pengajuan")
@login_required
@role_required("staf", "kepala_perpustakaan")
def daftar_pengajuan():
    daftar = (
        Peminjaman.query.filter_by(status="diajukan")
        .order_by(Peminjaman.id.asc())
        .all()
    )
    return render_template("peminjaman/pengajuan.html", daftar=daftar, today=date.today(), lama_pinjam_untuk=lama_pinjam_untuk)
```

-   `lama_pinjam_untuk=lama_pinjam_untuk` --- perhatikan, **fungsi
    Python itu sendiri** dikirim ke template (bukan hasil
    pemanggilannya). Ini memungkinkan template Jinja memanggil fungsi
    ini langsung per baris data (`{{ lama_pinjam_untuk(buku) }}`),
    berguna saat lama pinjam berbeda-beda tiap buku dan perlu dihitung
    ulang untuk setiap baris yang ditampilkan.

``` python
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
```

-   Stok dicek **ulang** di sini, karena bisa saja berubah sejak
    pengajuan dibuat (misalnya ada eksemplar lain yang rusak dan stoknya
    dikurangi manual oleh staf melalui fitur lain sebelum pengajuan ini
    diproses).

``` python
    ok, pesan = cek_kartu_valid(p.anggota)
    if not ok:
        flash(f"Tidak bisa disetujui untuk {p.anggota.nama_lengkap}: {pesan}", "danger")
        return redirect(url_for("peminjaman.daftar_pengajuan"))
```

-   `p.anggota` --- memakai `backref="anggota"` yang didefinisikan di
    relasi `User.peminjaman_list` pada `models.py`, sehingga dari objek
    `Peminjaman` bisa langsung mengakses `User` pemiliknya tanpa query
    terpisah.
-   Komentar kode menjelaskan: kartu kadaluarsa dicek **ulang** di sini
    (kondisinya bisa berubah sejak pengajuan dibuat), tapi kuota
    maksimal pinjam **tidak** dicek ulang --- karena pengajuan ini
    sendiri sudah termasuk dalam hitungan kuota sejak dibuat (lihat
    `STATUS_PINJAMAN_AKTIF` di `models.py` yang mencakup status
    `"diajukan"`).

``` python
    lama_hari = request.form.get("lama_hari", type=int)
    p.status = "dipinjam"
    p.diproses_oleh = current_user.id
    p.tanggal_pinjam = date.today()
    p.tanggal_jatuh_tempo = hitung_jatuh_tempo(p.buku, date.today(), lama_hari)
    p.buku.stok -= 1
    db.session.commit()
```

-   `request.form.get("lama_hari", type=int)` --- staf/kepala boleh
    menentukan lama pinjam **khusus** saat menyetujui (misalnya memberi
    tambahan waktu), jika dikosongkan, nilainya `None` dan
    `hitung_jatuh_tempo` akan memakai aturan default (lama pinjam buku
    atau umum).
-   `p.tanggal_pinjam = date.today()` --- **ditimpa ulang** dengan
    tanggal hari ini (tanggal persetujuan), bukan tanggal saat mahasiswa
    mengajukan --- supaya masa pinjam dihitung sejak buku benar-benar
    mulai dipinjamkan, bukan sejak diajukan (yang mungkin sudah beberapa
    hari lalu).
-   `p.buku.stok -= 1` --- baru di sinilah stok benar-benar dikurangi
    (bukan saat pengajuan dibuat), karena pengajuan belum tentu
    disetujui.
-   `p.tanggal_jatuh_tempo.strftime('%d-%m-%Y')` --- `strftime`
    memformat objek tanggal menjadi string dengan pola tertentu;
    `%d-%m-%Y` menghasilkan format `31-12-2026` (format tanggal
    Indonesia, hari-bulan-tahun).

``` python
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
```

-   Berbeda dari `batalkan_pengajuan()` (dihapus), di sini baris **tetap
    disimpan** dengan status `"ditolak"` --- menjaga riwayat bahwa
    pengajuan ini pernah ada dan sudah diproses oleh staf tertentu,
    lengkap dengan alasan penolakan di `catatan`.

### 12.3 Dipinjamkan Langsung oleh Staf (baris 152--207)

``` python
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
```

-   Fitur ini untuk kasus mahasiswa datang langsung ke meja (bukan
    mengajukan lewat sistem) --- staf memilih anggota dan buku, lalu
    langsung diproses sebagai `"dipinjam"` tanpa melalui tahap
    `"diajukan"`.
-   `User.query.filter_by(id=user_id, role="mahasiswa").first()` --- dua
    kondisi sekaligus di `filter_by`: id harus cocok **dan** role-nya
    memang mahasiswa (mencegah staf salah pilih atau manipulasi ID untuk
    "meminjamkan buku" ke akun staf lain).

``` python
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
```

-   Pengecekan serupa dengan `ajukan_peminjaman()`, tapi di sini hanya
    mengecek status `"dipinjam"` (bukan termasuk `"diajukan"`) ---
    karena jalur ini **melewati** tahap pengajuan, tidak relevan
    mengecek pengajuan yang menunggu.

``` python
        lama_hari = request.form.get("lama_hari", type=int)
        peminjaman = Peminjaman(
            user_id=anggota.id, buku_id=buku.id, diproses_oleh=current_user.id,
            tanggal_pinjam=date.today(),
            tanggal_jatuh_tempo=hitung_jatuh_tempo(buku, date.today(), lama_hari),
            status="dipinjam",
        )
        buku.stok -= 1
        db.session.add(peminjaman)
        db.session.commit()
```

-   `status="dipinjam"` langsung diisi dari awal pembuatan objek, karena
    memang tidak perlu tahap "diajukan" untuk alur ini.

``` python
    anggota_list = User.query.filter_by(role="mahasiswa", is_active_db=True).order_by(User.nama_lengkap).all()
    return render_template("peminjaman/pinjam.html", buku=buku, anggota_list=anggota_list, lama_default=lama_pinjam_untuk(buku))
```

-   Saat menampilkan form (`GET`), hanya mahasiswa yang **aktif**
    (`is_active_db=True`) yang muncul di daftar pilihan --- mahasiswa
    yang akunnya dinonaktifkan tidak bisa dipilih untuk dipinjamkan buku
    baru.

### 12.4 `daftar_peminjaman()` --- Daftar & Pencarian (baris 213--239)

``` python
@peminjaman_bp.route("/")
@login_required
@role_required("staf", "kepala_perpustakaan")
def daftar_peminjaman():
    status_filter = request.args.get("status", "dipinjam")
    q = request.args.get("q", "").strip()
    query = Peminjaman.query
    if status_filter != "semua":
        query = query.filter_by(status=status_filter)
```

-   `status_filter` default `"dipinjam"` --- halaman ini **secara
    default** menampilkan peminjaman yang sedang berjalan saja, bukan
    semua riwayat; user harus eksplisit memilih `?status=semua` untuk
    melihat semuanya.

``` python
    if q:
        like = f"%{q}%"
        query = (
            query.join(User, Peminjaman.user_id == User.id)
            .join(Buku, Peminjaman.buku_id == Buku.id)
            .filter(
                db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like), Buku.judul.ilike(like))
            )
        )
```

-   `.join(User, Peminjaman.user_id == User.id)` --- **join eksplisit**:
    karena pencarian butuh data dari tabel `User` dan `Buku` (nama
    peminjam, judul buku), bukan cuma dari tabel `Peminjaman` itu
    sendiri, maka perlu digabung (`JOIN`) secara manual, berbeda dari
    query-query sebelumnya yang hanya menyentuh satu tabel.
-   Pencarian ini bisa menemukan hasil lewat tiga kemungkinan kolom
    berbeda (nama lengkap peminjam, username peminjam, atau judul buku)
    sekaligus.

### 12.5 `kembalikan_buku()` --- Proses Pengembalian (baris 245--287)

``` python
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
```

-   Dua pengecekan terpisah dengan pesan berbeda, meski secara logika
    bisa digabung jadi satu `if p.status != "dipinjam"` --- pemisahan
    ini sengaja dibuat agar pesan untuk kasus "sudah dikembalikan" lebih
    spesifik/jelas, berbeda dari kasus lain seperti status `"diajukan"`
    atau `"ditolak"` yang memang tidak relevan dikembalikan.

``` python
    p.tanggal_kembali = date.today()
    p.status = "dikembalikan"
    p.denda = denda_dari_config(p.tanggal_jatuh_tempo, p.tanggal_kembali)
    p.status_denda = "belum_lunas" if p.denda > 0 else "tidak_ada"
    p.buku.stok += 1
```

-   `denda_dari_config(p.tanggal_jatuh_tempo, p.tanggal_kembali)` ---
    fungsi dari `utils/denda.py` yang menghitung besaran denda
    berdasarkan tarif dan aturan yang **berlaku hari ini** (dari
    `app.config`, yang sudah disinkronkan dari tabel `pengaturan` lewat
    `before_request` di `app.py`). Inilah momen "pembekuan" denda yang
    disebut komentar di `models.py` --- setelah ini, nilai `p.denda`
    tidak berubah lagi meski tarif denda umum berubah di kemudian hari.
-   `p.buku.stok += 1` --- stok dikembalikan (ditambah 1) begitu buku
    diterima kembali.

``` python
    if p.tanggal_kembali > p.tanggal_jatuh_tempo:
        hari_telat = (p.tanggal_kembali - p.tanggal_jatuh_tempo).days
        if p.denda > 0 and request.form.get("bayar") == "1":
            p.status_denda = "lunas"
            p.tanggal_denda_selesai = date.today()
            p.denda_diproses_oleh = current_user.id
            flash(f"Buku dikembalikan terlambat {hari_telat} hari. Denda {format_rupiah(p.denda)} sudah dibayar lunas.", "success")
        elif p.denda > 0:
            flash(f"Buku dikembalikan TERLAMBAT {hari_telat} hari. Denda {format_rupiah(p.denda)} belum dibayar — catat pembayarannya di menu Denda.", "warning")
        else:
            flash(f"Buku dikembalikan terlambat {hari_telat} hari (masih dalam masa tenggang, tanpa denda).", "info")
    else:
        flash("Buku berhasil dikembalikan tepat waktu.", "success")
```

-   `request.form.get("bayar") == "1"` --- form pengembalian menyertakan
    checkbox/opsi "langsung bayar denda sekarang". Jika dicentang
    **dan** memang ada denda, status denda langsung diset `"lunas"` saat
    itu juga (one-step), tanpa perlu buka menu Denda terpisah.
-   Tiga kemungkinan pesan berbeda saat terlambat: denda dibayar
    langsung (sukses), denda belum dibayar (peringatan, dengan arahan ke
    menu Denda), atau terlambat tapi **masih dalam masa tenggang**
    (`MASA_TENGGANG_HARI` di `config.py`) sehingga belum ada denda sama
    sekali (info).
-   `format_rupiah(p.denda)` --- fungsi dari `utils/denda.py` yang sama
    dengan yang didaftarkan sebagai filter Jinja `|rupiah` di `app.py`,
    di sini dipanggil langsung di kode Python (bukan di template) untuk
    disisipkan ke teks pesan `flash`.

### 12.6 Perpanjang & Koreksi Jatuh Tempo (baris 293--348)

``` python
@peminjaman_bp.route("/<int:peminjaman_id>/perpanjang", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def perpanjang(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status != "dipinjam":
        flash("Hanya peminjaman yang sedang berjalan yang bisa diperpanjang.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))
    if p.hari_telat > 0:
        flash("Buku sudah lewat jatuh tempo dan tidak bisa diperpanjang. Proses pengembalian terlebih dahulu.", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))
```

-   `p.hari_telat` --- memakai **property** yang didefinisikan di
    `models.py` (bukan dihitung ulang manual di sini) --- buku yang
    sudah telat tidak boleh diperpanjang lagi; staf harus memproses
    pengembalian (dengan dendanya) dulu.

``` python
    maks = current_app.config["MAKS_PERPANJANG"]
    if p.jumlah_perpanjang >= maks:
        flash(f"Batas perpanjangan tercapai (maksimal {maks} kali untuk satu peminjaman).", "warning")
        return redirect(url_for("peminjaman.daftar_peminjaman"))

    hari = request.form.get("hari", type=int) or lama_pinjam_untuk(p.buku)
    hari = max(1, min(hari, 365))
    p.tanggal_jatuh_tempo = p.tanggal_jatuh_tempo + timedelta(days=hari)
    p.jumlah_perpanjang += 1
    db.session.commit()
```

-   `request.form.get("hari", type=int) or lama_pinjam_untuk(p.buku)`
    --- jika staf tidak mengisi jumlah hari perpanjangan secara manual,
    dipakai nilai lama pinjam normal buku ini sebagai default.
-   `hari = max(1, min(hari, 365))` --- kombinasi `min` dan `max` ini
    adalah pola umum untuk **membatasi nilai dalam rentang**
    (*clamping*): `min(hari, 365)` memastikan tidak lebih dari 365, lalu
    `max(1, ...)` memastikan hasilnya tidak kurang dari 1 --- jadi nilai
    akhir selalu antara 1 sampai 365, apa pun input yang dikirim
    (termasuk jika dikirim negatif atau sangat besar).
-   Docstring fungsi menegaskan: jatuh tempo baru dihitung dari
    **tanggal jatuh tempo saat ini**
    (`p.tanggal_jatuh_tempo + timedelta(...)`), bukan dari hari ini ---
    supaya perpanjangan selalu menambah durasi dari batas sebelumnya,
    bukan "reset" hitungan dari awal.

``` python
@peminjaman_bp.route("/<int:peminjaman_id>/atur-jatuh-tempo", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def atur_jatuh_tempo(peminjaman_id):
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
```

-   Hanya `role_required("kepala_perpustakaan")` (bukan staf juga) ---
    sesuai docstring, karena fitur ini bisa mengubah besar denda secara
    langsung (mengubah tanggal jatuh tempo berarti mengubah jumlah hari
    telat yang dihitung nanti), dianggap tindakan sensitif.
-   `date.fromisoformat(request.form.get("tanggal", ""))` ---
    mengonversi string tanggal format ISO (`"2026-12-31"`) menjadi objek
    `date`. Dibungkus `try/except ValueError` karena jika formatnya
    salah (misalnya kosong atau format lain), fungsi ini melempar error
    `ValueError`, yang di sini ditangkap dan diubah jadi pesan flash
    yang ramah, bukan membuat aplikasi crash.
-   `baru < p.tanggal_pinjam` --- validasi masuk akal: jatuh tempo tidak
    boleh lebih awal dari tanggal mulai pinjam (mencegah input yang
    tidak logis).

``` python
    return redirect(request.referrer or url_for("peminjaman.daftar_peminjaman"))
```

-   `request.referrer` --- URL halaman sebelumnya (tempat form ini
    dikirim). Dipakai di `perpanjang()` dan `atur_jatuh_tempo()` supaya
    staf diarahkan **kembali ke halaman asal** (misalnya halaman riwayat
    anggota tertentu), bukan selalu ke daftar peminjaman umum.
    `or url_for(...)` adalah cadangan jika `referrer` tidak tersedia
    (misalnya browser tidak mengirim header ini).

### 12.7 Riwayat Peminjaman (baris 355--405)

``` python
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
    return render_template("peminjaman/riwayat_anggota.html", daftar=daftar, anggota=current_user, today=date.today(), bisa_batalkan=True, q=q)
```

``` python
@peminjaman_bp.route("/riwayat/anggota/<int:user_id>")
@login_required
@role_required("staf", "kepala_perpustakaan")
def riwayat_anggota(user_id):
    anggota = User.query.get_or_404(user_id)
    ...
    return render_template("peminjaman/riwayat_anggota.html", daftar=daftar, anggota=anggota, today=date.today(), bisa_batalkan=False, q=q)
```

-   Kedua fungsi ini **merender template HTML yang sama**
    (`peminjaman/riwayat_anggota.html`), hanya beda sumber datanya:
    `riwayat_saya()` untuk mahasiswa melihat riwayatnya sendiri,
    `riwayat_anggota(user_id)` untuk staf/kepala melihat riwayat anggota
    manapun.
-   `bisa_batalkan=True` vs `bisa_batalkan=False` --- variabel ini
    dikirim ke template untuk **mengatur tampilan** secara kondisional
    (misalnya menyembunyikan tombol "Batalkan" saat staf yang melihat
    riwayat orang lain), sementara logika pembatalan sesungguhnya
    (otorisasi) tetap dijaga di fungsi `batalkan_pengajuan()` yang sudah
    mengecek kepemilikan data.

``` python
@peminjaman_bp.route("/riwayat/buku/<int:buku_id>")
@login_required
@role_required("staf", "kepala_perpustakaan")
def riwayat_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    ...
    query = query.join(User, Peminjaman.user_id == User.id).filter(
        db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like))
    )
    daftar = query.order_by(Peminjaman.tanggal_pinjam.desc()).all()
    return render_template("peminjaman/riwayat_buku.html", daftar=daftar, buku=buku, today=date.today(), q=q)
```

-   Kebalikan dari dua fungsi sebelumnya: di sini yang tetap (fixed)
    adalah **buku**-nya, lalu dicari/difilter berdasarkan siapa saja
    yang pernah meminjamnya --- berguna misalnya untuk melihat seberapa
    sering satu buku dipinjam dan oleh siapa saja (terkait juga dengan
    laporan buku populer di `routes/laporan.py`).

> **Ringkasan bab:** Pusat logika bisnis; validasinya berada di
> `utils/pinjam.py`.

## BAB 13 --- Dashboard

> **File dibahas:** `routes/dashboard.py`\
> **Tujuan belajar:** Memahami cara dashboard menyusun statistik dan
> data grafik.\
> **Prasyarat:** Bab 9

### 13.1 Fungsi Bantu Grafik (baris 1--82)

``` python
from sqlalchemy import func
BULAN_ID = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
```

-   `from sqlalchemy import func` --- `func` memberi akses ke fungsi
    agregat SQL (`COUNT`, `SUM`, `MAX`, format tanggal, dsb) langsung
    lewat Python, tanpa menulis SQL mentah.
-   `BULAN_ID` --- list nama bulan singkat berbahasa Indonesia, dipakai
    untuk label grafik (karena `date` Python tidak otomatis tahu nama
    bulan dalam Bahasa Indonesia).

``` python
def _enam_bulan_terakhir():
    awal_bulan_ini = date.today().replace(day=1)
    hasil = []
    for mundur in range(5, -1, -1):
        bulan = awal_bulan_ini.month - mundur
        tahun = awal_bulan_ini.year
        while bulan <= 0:
            bulan += 12
            tahun -= 1
        hasil.append((tahun, bulan))
    return hasil
```

-   `date.today().replace(day=1)` --- mengambil tanggal hari ini, tapi
    menukar nilai `day` menjadi 1, menghasilkan tanggal 1 di bulan
    berjalan (dipakai sebagai titik acuan, bukan tanggal spesifik hari
    ini).
-   `range(5, -1, -1)` --- menghasilkan urutan `5, 4, 3, 2, 1, 0`
    (mundur dari 5 ke 0), dipakai untuk menghitung 6 bulan ke belakang
    **termasuk bulan ini** (mundur 0 = bulan ini sendiri).
-   `while bulan <= 0: bulan += 12; tahun -= 1` --- penanganan manual
    pergantian tahun: jika pengurangan bulan menghasilkan angka 0 atau
    negatif (misalnya bulan sekarang Februari dikurangi 5 = -3), angka
    bulan ditambah 12 dan tahun dikurangi 1, diulang (`while`, bukan
    `if`) sampai nilai bulan valid (1--12) --- berguna jika mundur lebih
    dari satu tahun kalender sekaligus.
-   Hasil akhir: list berisi *tuple* `(tahun, bulan)` berurutan dari
    yang terlama ke terbaru.

``` python
def _data_grafik_peminjaman_bulanan():
    bulan_list = _enam_bulan_terakhir()
    tahun_awal, bulan_awal = bulan_list[0]
    mulai = date(tahun_awal, bulan_awal, 1)

    baris = (
        db.session.query(
            func.date_format(Peminjaman.tanggal_pinjam, "%Y-%m").label("bulan_kunci"),
            func.count(Peminjaman.id),
        )
        .filter(Peminjaman.tanggal_pinjam >= mulai)
        .group_by("bulan_kunci")
        .all()
    )
    peta_jumlah = {kunci: jumlah for kunci, jumlah in baris}
```

-   `func.date_format(..., "%Y-%m")` --- fungsi MySQL `DATE_FORMAT`
    dipanggil lewat `func`, mengubah tanggal menjadi string `"2026-10"`
    (tahun-bulan saja), dipakai sebagai kunci pengelompokan
    (`group_by`).
-   `.group_by("bulan_kunci")` --- mengelompokkan baris berdasarkan
    **alias** kolom hasil (`label("bulan_kunci")`) yang didefinisikan di
    baris query sebelumnya.
-   `{kunci: jumlah for kunci, jumlah in baris}` --- mengubah hasil
    query (list of tuple) menjadi dictionary, supaya pencarian jumlah
    per bulan lebih mudah dan cepat (`peta_jumlah["2026-10"]`) dibanding
    mencari di list satu-satu.

``` python
    labels, data = [], []
    for tahun, bulan in bulan_list:
        kunci = f"{tahun:04d}-{bulan:02d}"
        labels.append(f"{BULAN_ID[bulan - 1]} {tahun}")
        data.append(peta_jumlah.get(kunci, 0))
    return labels, data
```

-   `f"{tahun:04d}-{bulan:02d}"` --- format string dengan padding angka:
    `:04d` memastikan tahun selalu 4 digit (misal `"2026"`), `:02d`
    memastikan bulan selalu 2 digit dengan angka 0 di depan jika perlu
    (misal bulan 3 jadi `"03"`) --- harus cocok persis dengan format
    `"%Y-%m"` dari `date_format` SQL di atas supaya pencarian di
    dictionary berhasil.
-   `BULAN_ID[bulan - 1]` --- dikurangi 1 karena index list Python
    dimulai dari 0, sementara nomor bulan dimulai dari 1 (Januari =
    bulan 1 = index 0).
-   `peta_jumlah.get(kunci, 0)` --- jika bulan tertentu **tidak ada data
    peminjaman sama sekali**, hasil query tidak akan punya baris untuk
    bulan itu; `.get(kunci, 0)` memastikan grafik tetap menampilkan
    nilai 0 untuk bulan kosong, bukan melompati bulan itu.
-   Fungsi ini mengembalikan **dua list sejajar** (`labels` dan `data`)
    --- pola umum untuk menyuplai data ke library grafik JavaScript
    (Chart.js dan sejenisnya) di sisi template.

``` python
def _data_grafik_buku_terpopuler(limit=5):
    hasil = (
        db.session.query(Buku.judul, func.count(Peminjaman.id).label("jumlah"))
        .join(Peminjaman, Peminjaman.buku_id == Buku.id)
        .group_by(Buku.id)
        .order_by(func.count(Peminjaman.id).desc())
        .limit(limit)
        .all()
    )
    labels = [judul for judul, _ in hasil]
    data = [jumlah for _, jumlah in hasil]
    return labels, data
```

-   `.join(Peminjaman, ...)` --- **inner join**: hanya buku yang
    **pernah** punya baris di tabel `Peminjaman` yang muncul di hasil
    (buku yang belum pernah dipinjam otomatis tidak tampil di grafik
    ini, karena tidak ada baris untuk di-`JOIN`).
-   `[judul for judul, _ in hasil]` --- garis bawah `_` dipakai sebagai
    nama variabel untuk nilai yang **sengaja diabaikan** (konvensi
    Python: "saya tahu ada nilai kedua di sini, tapi saya tidak butuh
    dia untuk list ini").

``` python
def _data_grafik_distribusi_kategori():
    hasil = (
        db.session.query(Kategori.nama_kategori, func.count(Buku.id))
        .outerjoin(Buku, Buku.kategori_id == Kategori.id)
        .group_by(Kategori.id)
        .having(func.count(Buku.id) > 0)
        .order_by(func.count(Buku.id).desc())
        .all()
    )
```

-   `.outerjoin(...)` --- **left outer join**, berbeda dari `.join()`
    biasa: kategori tetap muncul di hasil query meski tidak punya buku
    sama sekali (`COUNT` akan bernilai 0 untuk kategori kosong).
-   `.having(func.count(Buku.id) > 0)` --- tapi kemudian **difilter
    lagi** untuk membuang kategori yang hasil hitungnya 0 --- jadi meski
    pakai outer join, kategori kosong tetap tidak ditampilkan di grafik
    distribusi ini. `.having()` dipakai (bukan `.filter()`) karena
    kondisinya melibatkan hasil fungsi agregat (`COUNT`), yang di SQL
    memang harus difilter pakai `HAVING`, bukan `WHERE`.

### 13.2 `index()` --- Isi Dashboard (baris 85--187)

``` python
@dashboard_bp.route("/")
@login_required
def index():
    context = {}
    if current_user.is_mahasiswa:
        pinjaman_aktif = Peminjaman.query.filter_by(user_id=current_user.id, status="dipinjam").all()
        context["pinjaman_aktif"] = pinjaman_aktif
        context["jumlah_terlambat_saya"] = sum(1 for p in pinjaman_aktif if p.is_telat)
        context["denda_berjalan_saya"] = denda_berjalan_semua(current_user.id)
        context["denda_belum_lunas_saya"] = total_denda_belum_lunas(current_user.id)
```

-   `context = {}` --- dictionary kosong yang **diisi secara bertahap**
    tergantung role user, lalu di akhir fungsi di-*unpack* semuanya ke
    `render_template` sekaligus (`**context`).
-   Dashboard ini **satu fungsi untuk dua tampilan berbeda** (mahasiswa
    vs staf/kepala) --- percabangan besar
    `if current_user.is_mahasiswa: ... else: ...` menentukan data mana
    yang disiapkan, tapi keduanya mengarah ke template HTML yang sama
    (`dashboard.html`), yang di dalamnya sendiri tentu punya logika
    kondisional untuk menampilkan bagian yang sesuai.
-   `sum(1 for p in pinjaman_aktif if p.is_telat)` --- menghitung berapa
    banyak item di `pinjaman_aktif` yang propertinya `is_telat` bernilai
    `True`, dengan menjumlahkan angka 1 untuk tiap kecocokan (pola yang
    sama seperti `Buku.total_dipinjam` di `models.py`).

``` python
        batas_peringatan = current_app.config["PERINGATAN_JATUH_TEMPO_HARI"]
        context["akan_jatuh_tempo_saya"] = [
            p for p in pinjaman_aktif
            if not p.is_telat and p.hari_menuju_jatuh_tempo is not None
            and p.hari_menuju_jatuh_tempo <= batas_peringatan
        ]
```

-   *List comprehension* dengan tiga kondisi sekaligus: belum telat,
    nilai hari-menuju-jatuh-tempo memang ada (bukan `None`), dan sisa
    harinya sudah masuk ambang peringatan --- menyaring tepat kasus
    "akan segera jatuh tempo, belum terlambat".

``` python
        buku_id_aktif = {p.buku_id for p in Peminjaman.query.filter(
            Peminjaman.user_id == current_user.id,
            Peminjaman.status.in_(["diajukan", "dipinjam"]),
        ).all()}
        rekomendasi = (
            db.session.query(Buku, func.count(Peminjaman.id).label("jumlah"))
            .join(Peminjaman, Peminjaman.buku_id == Buku.id)
            .filter(Buku.stok > 0)
            .group_by(Buku.id)
            .order_by(func.count(Peminjaman.id).desc())
            .limit(10)
            .all()
        )
        context["rekomendasi_buku"] = [
            (b, jumlah) for b, jumlah in rekomendasi if b.id not in buku_id_aktif
        ][:5]
```

-   Logika rekomendasi: ambil 10 buku paling sering dipinjam (secara
    keseluruhan) yang stoknya tersedia, lalu **buang** yang sudah sedang
    diajukan/dipinjam mahasiswa ini sendiri
    (`b.id not in buku_id_aktif`), baru ambil 5 teratas (`[:5]`).
-   Mengapa ambil 10 dulu baru dipotong jadi 5? Karena setelah buku yang
    sudah dipinjam user ini disaring keluar, sisa barisnya mungkin
    kurang dari 5 kalau dari awal cuma ambil 5 --- mengambil lebih
    banyak (10) dari database dulu sebagai "cadangan" sebelum
    penyaringan di level Python.

``` python
    else:
        context["total_buku"] = Buku.query.count()
        context["total_stok"] = sum(b.stok for b in Buku.query.all())
        context["sedang_dipinjam"] = Peminjaman.query.filter_by(status="dipinjam").count()
        context["terlambat"] = sum(1 for p in Peminjaman.query.filter_by(status="dipinjam").all() if p.is_telat)
```

-   `sum(b.stok for b in Buku.query.all())` --- menjumlahkan stok **di
    level Python** (ambil semua baris dulu, baru dijumlah), bukan lewat
    `func.sum()` di database. Ini kurang efisien dibanding query agregat
    SQL langsung, tapi untuk jumlah data buku yang wajar, perbedaannya
    tidak signifikan.
-   `context["terlambat"]` juga dihitung dengan mengambil semua baris
    `status="dipinjam"` dulu baru disaring `is_telat` di Python ---
    karena `is_telat` adalah **property Python** (bukan kolom database),
    sehingga tidak bisa langsung difilter lewat SQL `WHERE`, harus
    diambil semua lalu dicek satu-satu.

``` python
        labels_bulanan, data_bulanan = _data_grafik_peminjaman_bulanan()
        context["labels_grafik_bulanan"] = labels_bulanan
        context["data_grafik_bulanan"] = data_bulanan
        ...
        top_mhs = statistik_mahasiswa_peminjam("semua", limit=5)
        context["labels_grafik_top_mhs"] = [b["user"].nama_lengkap for b in top_mhs]
        context["data_grafik_top_mhs"] = [b["total"] for b in top_mhs]
```

-   `from routes.laporan import statistik_mahasiswa_peminjam` (lihat
    baris impor di atas) --- dashboard **memakai ulang** fungsi yang
    sama dengan yang dipakai di halaman laporan khusus mahasiswa aktif
    (`routes/laporan.py`), bukannya menulis ulang query serupa ---
    praktik *code reuse* lintas file.

``` python
        batas_tempo = date.today() + timedelta(days=current_app.config["PERINGATAN_JATUH_TEMPO_HARI"])
        context["akan_jatuh_tempo"] = (
            Peminjaman.query.filter(
                Peminjaman.status == "dipinjam",
                Peminjaman.tanggal_jatuh_tempo >= date.today(),
                Peminjaman.tanggal_jatuh_tempo <= batas_tempo,
            )
            .order_by(Peminjaman.tanggal_jatuh_tempo.asc())
            .all()
        )
```

-   Untuk tampilan staf/kepala, pengecekan "akan jatuh tempo" dilakukan
    **langsung lewat query SQL** (membandingkan `tanggal_jatuh_tempo`
    dengan rentang tanggal), berbeda dari versi mahasiswa yang dihitung
    di Python --- karena di sini tidak perlu property
    `hari_menuju_jatuh_tempo` per baris, cukup bandingkan rentang
    tanggal secara langsung di database (lebih efisien untuk jumlah data
    yang mungkin besar, mencakup seluruh anggota).

``` python
        if current_user.is_kepala:
            context["total_anggota"] = User.query.filter_by(role="mahasiswa").count()
            context["menunggu_persetujuan"] = User.query.filter_by(role="mahasiswa", status_akun="pending").count()
    return render_template("dashboard.html", today=date.today(), **context)
```

-   Percabangan bertingkat: di dalam cabang "bukan mahasiswa"
    (staf/kepala), ada percabangan **lagi** khusus kepala perpustakaan
    --- data jumlah total anggota dan antrean persetujuan hanya relevan
    untuk kepala, tidak untuk staf biasa.
-   `**context` --- operator *dictionary unpacking*: setiap key di
    `context` (misalnya `"total_buku"`) otomatis menjadi argumen
    terpisah untuk `render_template` (setara menulis
    `total_buku=context["total_buku"], ...` untuk semua key satu-satu).

> **Ringkasan bab:** Fungsi bantu menyiapkan data grafik, `index()`
> merangkai isi dashboard per role.

## BAB 14 --- Laporan

> **File dibahas:** `routes/laporan.py`\
> **Tujuan belajar:** Memahami laporan populer, tidak populer, mahasiswa
> aktif, dan terlambat.\
> **Prasyarat:** Bab 9

### 14.1 Buku Populer & Tidak Populer (baris 16--48)

``` python
@laporan_bp.route("/populer")
@login_required
@role_required("staf", "kepala_perpustakaan")
def buku_populer():
    hasil = (
        db.session.query(Buku, db.func.count(Peminjaman.id).label("jumlah_pinjam"))
        .join(Peminjaman, Peminjaman.buku_id == Buku.id)
        .group_by(Buku.id)
        .order_by(db.func.count(Peminjaman.id).desc())
        .limit(20)
        .all()
    )
```

-   Mirip `_data_grafik_buku_terpopuler()` di `dashboard.py`, tapi
    mengembalikan 20 baris (untuk tabel laporan lengkap) bukan 5 (untuk
    grafik ringkas), dan tidak dipecah jadi dua list terpisah --- di
    sini `hasil` dikirim langsung ke template sebagai list *tuple*
    `(Buku, jumlah_pinjam)`.

``` python
@laporan_bp.route("/tidak-populer")
@login_required
@role_required("staf", "kepala_perpustakaan")
def buku_tidak_populer():
    subq = db.session.query(Peminjaman.buku_id).distinct().subquery()
    tidak_pernah = Buku.query.filter(~Buku.id.in_(subq)).order_by(Buku.judul).all()

    jarang = (
        db.session.query(Buku, db.func.count(Peminjaman.id).label("jumlah_pinjam"))
        .join(Peminjaman, Peminjaman.buku_id == Buku.id)
        .group_by(Buku.id)
        .having(db.func.count(Peminjaman.id) <= 2)
        .order_by(db.func.count(Peminjaman.id).asc())
        .all()
    )
```

-   `db.session.query(Peminjaman.buku_id).distinct().subquery()` ---
    membuat **subquery**: daftar `buku_id` unik yang pernah muncul di
    tabel peminjaman, dibungkus sebagai query terpisah (`.subquery()`)
    yang bisa dipakai di dalam query lain.
-   `~Buku.id.in_(subq)` --- tanda `~` adalah operator **NOT** di
    SQLAlchemy: "ambil buku yang id-nya **TIDAK** ada di dalam subquery
    itu" --- setara `WHERE id NOT IN (SELECT buku_id FROM peminjaman)`
    di SQL mentah. Ini cara mencari buku yang **belum pernah** dipinjam
    sama sekali.
-   `jarang` --- berbeda dari `tidak_pernah` (pakai subquery NOT IN),
    kategori "jarang dipinjam" tetap pakai inner join biasa (buku memang
    harus **pernah** muncul di tabel peminjaman untuk bisa dihitung
    `COUNT`-nya), lalu disaring `.having(... <= 2)` untuk ambil yang
    jumlahnya sedikit.

### 14.2 Statistik Mahasiswa Peminjam (baris 55--129)

``` python
PERIODE_STATISTIK = {
    "semua": ("Semua waktu", None),
    "30": ("30 hari terakhir", 30),
    "90": ("90 hari terakhir", 90),
    "365": ("1 tahun terakhir", 365),
}
STATUS_DIHITUNG = ("dipinjam", "dikembalikan", "terlambat")
```

-   Dictionary ini berfungsi ganda: sebagai **sumber pilihan periode**
    di dropdown filter (lewat key-nya: `"semua"`, `"30"`, dst) dan
    sekaligus **data konfigurasinya** (label tampilan dan jumlah hari)
    --- satu sumber data dipakai untuk dua kebutuhan berbeda, mengurangi
    risiko dua daftar jadi tidak sinkron.
-   Komentar kode menegaskan status `"diajukan"` dan `"ditolak"`
    **sengaja tidak dihitung** sebagai aktivitas meminjam di statistik
    ini --- sesuai makna bisnisnya: belum tentu benar-benar meminjam
    kalau masih diajukan/ditolak.

``` python
def statistik_mahasiswa_peminjam(kunci_periode="semua", limit=None):
    if kunci_periode not in PERIODE_STATISTIK:
        kunci_periode = "semua"
    hari = PERIODE_STATISTIK[kunci_periode][1]
    hari_ini = date.today()

    telat = case(
        (and_(Peminjaman.status == "dikembalikan",
              Peminjaman.tanggal_kembali > Peminjaman.tanggal_jatuh_tempo), 1),
        (and_(Peminjaman.status == "dipinjam",
              Peminjaman.tanggal_jatuh_tempo < hari_ini), 1),
        else_=0,
    )
    sedang = case((Peminjaman.status == "dipinjam", 1), else_=0)
```

-   `case(...)` --- ini adalah ekspresi
    `CASE WHEN ... THEN ... ELSE ... END` di SQL, ditulis lewat
    SQLAlchemy. Setiap *tuple* adalah pasangan (kondisi,
    nilai-jika-benar); `else_=0` adalah nilai cadangan jika semua
    kondisi gagal.
-   Komentar kode menyebut ini sebagai **"padanan SQL"** dari property
    `Peminjaman.is_telat` di `models.py` --- karena query SQL **tidak
    bisa langsung memanggil** property Python, logika yang sama harus
    ditulis ulang di level SQL supaya bisa dijumlahkan (`SUM`) langsung
    oleh database untuk banyak baris sekaligus (jauh lebih efisien
    daripada mengambil semua baris lalu mengecek `is_telat` satu-satu di
    Python, seperti yang dilakukan di `dashboard.py` untuk kasus yang
    lebih sederhana).
-   `and_(...)` --- menggabungkan dua kondisi dengan **AND** secara
    eksplisit di dalam ekspresi `case`.

``` python
    q = (
        db.session.query(
            User, func.count(Peminjaman.id).label("total"),
            func.count(Peminjaman.buku_id.distinct()).label("judul_unik"),
            func.sum(sedang).label("sedang"),
            func.sum(telat).label("telat"),
            func.max(Peminjaman.tanggal_pinjam).label("terakhir"),
        )
        .join(Peminjaman, Peminjaman.user_id == User.id)
        .filter(User.role == "mahasiswa", Peminjaman.status.in_(STATUS_DIHITUNG))
    )
    if hari:
        q = q.filter(Peminjaman.tanggal_pinjam >= hari_ini - timedelta(days=hari))
```

-   `func.count(Peminjaman.buku_id.distinct())` --- menghitung jumlah
    **judul buku berbeda** yang dipinjam (bukan jumlah transaksi
    peminjaman) --- seorang mahasiswa yang meminjam buku A tiga kali
    tetap dihitung 1 judul unik, tapi 3 total peminjaman.
-   `func.sum(sedang)` dan `func.sum(telat)` --- menjumlahkan ekspresi
    `case` yang dibuat tadi (tiap baris bernilai 1 atau 0), sehingga
    hasilnya adalah **jumlah baris yang memenuhi kondisi**, dihitung
    langsung oleh database.
-   `if hari:` --- filter rentang waktu hanya ditambahkan jika periode
    yang dipilih bukan `"semua"` (yang nilainya `None`, dianggap
    *falsy*).

``` python
    q = q.group_by(User.id).order_by(
        func.count(Peminjaman.id).desc(),
        func.max(Peminjaman.tanggal_pinjam).desc(),
        User.nama_lengkap.asc(),
    )
    if limit:
        q = q.limit(limit)
```

-   Pengurutan **tiga tingkat**: pertama berdasarkan total peminjaman
    (paling banyak di atas), jika seri (sama banyak) diurutkan
    berdasarkan siapa yang **paling baru** meminjam, jika masih seri
    juga baru diurutkan alfabetis nama.

``` python
    hasil = []
    for user, total, judul_unik, sedang_n, telat_n, terakhir in q.all():
        hasil.append({
            "user": user, "total": int(total), "judul_unik": int(judul_unik),
            "sedang_dipinjam": int(sedang_n or 0), "terlambat": int(telat_n or 0),
            "terakhir": terakhir,
        })
```

-   Hasil query (list of *tuple*, karena `db.session.query` dengan
    banyak kolom) diubah menjadi list of **dictionary**, lebih mudah
    dibaca & dipakai di template (`baris.user.nama_lengkap`,
    `baris.total`, dst, lewat akses key dictionary) dibanding mengingat
    urutan posisi *tuple*.
-   `int(sedang_n or 0)` --- hasil `SUM` di SQL bisa mengembalikan
    `None` (bukan 0) jika tidak ada baris yang cocok sama sekali untuk
    grup tertentu; `or 0` memastikan nilainya tetap angka 0, bukan
    `None`, sebelum dibungkus `int(...)`.

``` python
    for i, baris in enumerate(hasil):
        if i > 0 and baris["total"] == hasil[i - 1]["total"]:
            baris["peringkat"] = hasil[i - 1]["peringkat"]
        else:
            baris["peringkat"] = i + 1
    return hasil
```

-   `enumerate(hasil)` --- memberi index (`i`) sekaligus nilai (`baris`)
    saat iterasi list.
-   Logika ini membuat **peringkat kompetisi** (seperti peringkat
    lomba): jika total peminjaman seorang mahasiswa **sama persis**
    dengan mahasiswa tepat di atasnya (`hasil[i - 1]`), keduanya diberi
    peringkat yang **sama**, bukan nomor urut berurutan --- misalnya
    jika dua orang sama-sama total 10, keduanya peringkat 2, lalu yang
    berikutnya langsung peringkat 4 (bukan 3), mengikuti pola
    `1, 2, 2, 4, 5...` sesuai komentar docstring fungsi.

``` python
def _periode_dari_request():
    kunci = request.args.get("periode", "semua")
    return kunci if kunci in PERIODE_STATISTIK else "semua"
```

-   Fungsi bantu kecil ini memastikan nilai `periode` dari URL **valid**
    (ada di `PERIODE_STATISTIK`); jika user memasukkan nilai aneh
    langsung di URL (misalnya `?periode=abc`), otomatis dikembalikan ke
    `"semua"` daripada menyebabkan error di query.

### 14.3 Route Mahasiswa Aktif & Buku Terlambat (baris 137--214)

``` python
@laporan_bp.route("/mahasiswa-aktif")
@login_required
@role_required("staf", "kepala_perpustakaan")
def mahasiswa_aktif():
    kunci = _periode_dari_request()
    hasil = statistik_mahasiswa_peminjam(kunci, limit=50)
    return render_template(
        "laporan/mahasiswa_aktif.html", hasil=hasil, periode=kunci,
        periode_opsi=PERIODE_STATISTIK, total_terbanyak=hasil[0]["total"] if hasil else 0,
    )
```

-   `hasil[0]["total"] if hasil else 0` --- mengambil total milik
    peringkat 1 (dipakai mungkin untuk menampilkan bar chart
    proporsional di template, dibandingkan dengan nilai tertinggi); jika
    `hasil` kosong (tidak ada data sama sekali), dipakai 0 sebagai
    cadangan untuk menghindari error index di luar jangkauan.

``` python
def _daftar_terlambat():
    semua = Peminjaman.query.filter_by(status="dipinjam").order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all()
    return sorted((p for p in semua if p.hari_telat > 0), key=lambda p: p.hari_telat, reverse=True)
```

-   Karena `hari_telat` adalah property Python (tidak bisa difilter
    langsung lewat SQL), semua peminjaman aktif diambil dulu, baru
    disaring (`if p.hari_telat > 0`) dan diurutkan ulang **di Python**.
-   `sorted(..., key=lambda p: p.hari_telat, reverse=True)` ---
    `key=lambda p: p.hari_telat` memberi tahu `sorted()` untuk
    mengurutkan berdasarkan nilai `hari_telat` tiap item (bukan urutan
    alami objek `Peminjaman`); `reverse=True` membuat yang paling lama
    terlambat muncul di paling atas.

``` python
@laporan_bp.route("/terlambat")
@login_required
@role_required("staf", "kepala_perpustakaan")
def buku_terlambat():
    daftar = _daftar_terlambat()
    total_denda = sum(denda_peminjaman(p) for p in daftar)
    return render_template("laporan/terlambat.html", daftar=daftar, total_denda=total_denda)
```

-   `denda_peminjaman(p)` --- dipanggil per item untuk menghitung denda
    **berjalan** (real-time, belum dibekukan) dari `utils/denda.py`,
    lalu dijumlahkan semuanya untuk ringkasan total di bagian atas
    laporan.

### 14.4 Ekspor Excel Mahasiswa Aktif dan Terlambat

Kedua laporan ini memiliki route ekspor sendiri dan hanya dapat diakses
oleh pengguna yang login dengan role `staf` atau `kepala_perpustakaan`.

#### A. Ekspor mahasiswa aktif

Route `GET /laporan/mahasiswa-aktif/ekspor` memakai
`_periode_dari_request()` untuk membaca periode yang dipilih, lalu
memanggil `statistik_mahasiswa_peminjam(kunci)` **tanpa argumen
`limit`**. Karena itu, halaman web hanya menampilkan maksimal 50
mahasiswa, sedangkan file Excel memuat seluruh mahasiswa yang memenuhi
kriteria periode.

Kolom Excel:

  Kolom               Isi
  ------------------- -------------------------------------------
  Peringkat           Peringkat berdasarkan total peminjaman
  Mahasiswa           Nama lengkap
  NIM/Username        NIM jika tersedia; jika tidak, username
  Total Dipinjam      Jumlah transaksi peminjaman yang dihitung
  Judul Berbeda       Jumlah buku berbeda yang pernah dipinjam
  Sedang Dipinjam     Jumlah transaksi berstatus `dipinjam`
  Kali Terlambat      Jumlah transaksi yang terlambat
  Terakhir Meminjam   Tanggal peminjaman terakhir

Nama file mengikuti pola `mahasiswa_aktif_<periode>_<tanggal>.xlsx`,
misalnya `mahasiswa_aktif_30_2026-10-22.xlsx`. Nilai tanggal diformat
dengan `strftime("%d-%m-%Y")`; jika tanggal terakhir tidak tersedia, sel
diisi `-`.

#### B. Ekspor buku terlambat

Route `GET /laporan/terlambat/ekspor` menggunakan `_daftar_terlambat()`
yang sama dengan halaman web. Dengan demikian, isi dan urutan daftar
ekspor mengikuti kriteria halaman: transaksi masih berstatus `dipinjam`,
telah melewati jatuh tempo, dan yang paling lama terlambat ditampilkan
lebih dahulu.

Kolom Excel:

  Kolom                 Isi
  --------------------- --------------------------------------------
  Mahasiswa             Nama lengkap peminjam
  NIM/Username          NIM jika tersedia; jika tidak, username
  No. Telepon           Nomor telepon peminjam; `-` jika kosong
  Buku                  Judul buku
  Jatuh Tempo           Tanggal jatuh tempo
  Hari Telat            Jumlah hari keterlambatan
  Denda Berjalan (Rp)   Denda saat ekspor dihitung secara langsung

Nomor telepon disertakan agar staf dapat menghubungi peminjam. Nama file
mengikuti pola `buku_terlambat_<tanggal>.xlsx`, misalnya
`buku_terlambat_2026-10-22.xlsx`.

#### C. Cara kerja pembuatan file

Pola kedua route mengikuti `ekspor_buku()` yang dibahas di Bab 11:

1.  Data query diubah menjadi list berisi baris-baris (`baris`).
2.  `buat_excel(judul_sheet, header, baris)` membuat workbook dan
    mengembalikan buffer `BytesIO`.
3.  `send_file(...)` mengirim buffer sebagai unduhan `.xlsx`.

Route ekspor tidak mengubah data di database. Laporan buku populer dan
tidak populer **tidak memiliki route ekspor** pada kode yang diperiksa.

> **Ringkasan bab:** Laporan memakai query agregat (COUNT/GROUP BY) dan
> bisa diekspor Excel.

## BAB 15 --- Kartu Anggota

> **File dibahas:** `routes/kartu.py`\
> **Tujuan belajar:** Memahami kartu anggota digital: tampil, cetak,
> kelola, perpanjang.\
> **Prasyarat:** Bab 9

### 15.1 Kartu Milik Sendiri & Anggota Lain (baris 18--48)

``` python
@kartu_bp.route("/saya")
@login_required
def kartu_saya():
    kartu = _terbitkan_kartu_jika_belum_ada(current_user)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=current_user)
```

-   Perhatikan: **tidak ada** `@role_required(...)` di sini --- hanya
    `@login_required`, artinya **semua role** (mahasiswa, staf, kepala)
    boleh mengakses kartu miliknya sendiri, sesuai komentar kode di atas
    blueprint: kartu berlaku untuk semua role.
-   `_terbitkan_kartu_jika_belum_ada(current_user)` --- dipanggil setiap
    kali halaman ini dibuka, bukan hanya saat registrasi; ini pola
    **"lazy create"** (dibuat baru saat benar-benar dibutuhkan): jika
    user ini kebetulan belum pernah punya kartu (misalnya akun sangat
    lama dari sebelum fitur kartu ada), kartunya dibuat otomatis saat
    pertama kali membuka halaman ini, tanpa perlu proses terpisah.

``` python
@kartu_bp.route("/anggota/<int:user_id>")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kartu_anggota_lain(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = _terbitkan_kartu_jika_belum_ada(anggota)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=anggota)
```

-   Berbeda dari `kartu_saya()` (tanpa pembatasan role), melihat kartu
    **orang lain** dibatasi hanya staf/kepala --- sesuai prinsip umum:
    data sendiri boleh dilihat siapa saja yang login, data orang lain
    butuh hak akses lebih tinggi.
-   `kartu_saya()`/`kartu_anggota_lain()` dan versi `_cetak`-nya
    (`kartu_saya_cetak()`, `kartu_anggota_lain_cetak()`) memakai
    **logika yang persis sama**, hanya beda nama template yang dirender
    (`kartu.html` untuk tampilan layar, `cetak.html` untuk versi siap
    cetak) --- bentuk duplikasi kecil yang disengaja demi kesederhanaan,
    daripada membuat satu fungsi dengan parameter tambahan untuk memilih
    template.

### 15.2 `kelola_kartu()` --- Daftar & Filter (baris 56--88)

``` python
@kartu_bp.route("/kelola")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kelola_kartu():
    ...
    query = KartuAnggota.query.join(User, KartuAnggota.user_id == User.id)
    ...
    if filter_status == "aktif":
        query = query.filter(KartuAnggota.status == "aktif", KartuAnggota.tanggal_kadaluarsa >= date.today())
    elif filter_status == "nonaktif":
        query = query.filter(KartuAnggota.status == "nonaktif")
    elif filter_status == "kadaluarsa":
        query = query.filter(KartuAnggota.tanggal_kadaluarsa < date.today())
```

-   Perhatikan filter `"aktif"` memakai **dua syarat sekaligus** (status
    `"aktif"` DAN belum lewat tanggal kadaluarsa) --- ini sejalan dengan
    property `bisa_dipakai` di `models.py`
    (`status == "aktif" and not is_kadaluarsa`), ditulis ulang di level
    query karena perlu memfilter di database, bukan di Python (mirip
    pola yang sama di `statistik_mahasiswa_peminjam`).
-   Filter `"kadaluarsa"` **tidak** mensyaratkan status apa pun ---
    kartu yang statusnya masih `"aktif"` tapi tanggalnya sudah lewat
    tetap termasuk kategori "kadaluarsa" di filter ini (beda konsep dari
    `bisa_dipakai`, yang mensyaratkan kedua kondisi; di sini sengaja
    memisahkan tiga sudut pandang filter yang tumpang-tindih secara
    logis, tapi berguna untuk kebutuhan tampilan yang berbeda-beda).

``` python
    tanpa_kartu = (
        User.query.outerjoin(KartuAnggota, KartuAnggota.user_id == User.id)
        .filter(KartuAnggota.id.is_(None), User.status_akun == "disetujui")
        .order_by(User.nama_lengkap.asc())
        .all()
    )
```

-   `.outerjoin(...)` ditambah `.filter(KartuAnggota.id.is_(None), ...)`
    --- pola standar SQL untuk mencari baris di tabel "kiri" (`User`)
    yang **tidak punya** pasangan di tabel "kanan" (`KartuAnggota`):
    left join akan mengisi kolom dari `KartuAnggota` dengan NULL jika
    tidak ada relasinya, lalu difilter `id IS NULL` untuk hanya
    mengambil baris yang memang tidak match.
-   `.is_(None)` --- di SQLAlchemy, perbandingan dengan `None` **harus**
    memakai `.is_(None)`, bukan `== None`, karena operator `==` Python
    biasa tidak diterjemahkan dengan benar ke SQL `IS NULL` untuk kasus
    ini.

### 15.3 `edit_kartu()`, `toggle_kartu()`, `perpanjang_kartu()` (baris 104--174)

``` python
@kartu_bp.route("/kelola/<int:kartu_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def edit_kartu(kartu_id):
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    pemilik = kartu.pemilik
    if request.method == "POST":
        nim, err = validasi_nim(request.form.get("nim", ""), wajib=pemilik.is_mahasiswa, abaikan_user_id=pemilik.id)
```

-   `pemilik = kartu.pemilik` --- memakai `backref="pemilik"` dari
    relasi di `models.py`, mengambil objek `User` pemilik kartu ini dari
    sisi `KartuAnggota` (arah kebalikan dari `user.kartu`).
-   `wajib=pemilik.is_mahasiswa` --- NIM wajib diisi hanya jika pemilik
    kartu adalah mahasiswa (sama seperti aturan di `auth.py`), konsisten
    di seluruh aplikasi.

``` python
        try:
            terbit = date.fromisoformat(request.form.get("tanggal_terbit", ""))
            kadaluarsa = date.fromisoformat(request.form.get("tanggal_kadaluarsa", ""))
        except ValueError:
            flash("Format tanggal tidak valid.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))
        if kadaluarsa < terbit:
            flash("Tanggal kadaluarsa tidak boleh lebih awal dari tanggal terbit.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))
```

-   Dua tanggal diparsing dalam **satu blok** `try/except` yang sama ---
    jika salah satu (atau keduanya) gagal diparsing, keduanya ditangani
    dengan satu pesan error yang sama, karena penyebab kegagalannya
    sama-sama "format tanggal salah", tidak perlu dibedakan pesan per
    field.
-   `kadaluarsa < terbit` --- validasi logis: kartu tidak masuk akal
    kadaluarsa sebelum diterbitkan.

``` python
        pemilik.nim = nim
        kartu.tanggal_terbit = terbit
        kartu.tanggal_kadaluarsa = kadaluarsa
        kartu.status = status
        db.session.commit()
```

-   Perhatikan baris ini mengubah **dua objek berbeda sekaligus**
    (`pemilik.nim` di tabel `User`, dan tiga atribut lain di tabel
    `KartuAnggota`) dalam satu transaksi (`db.session.commit()` tunggal)
    --- SQLAlchemy melacak perubahan di kedua objek secara terpisah,
    tapi keduanya disimpan permanen bersamaan.

``` python
@kartu_bp.route("/kelola/<int:kartu_id>/perpanjang", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def perpanjang_kartu(kartu_id):
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    hari = current_app.config["MASA_BERLAKU_KARTU_HARI"]
    dasar = max(kartu.tanggal_kadaluarsa, date.today())
    kartu.tanggal_kadaluarsa = dasar + timedelta(days=hari)
    kartu.status = "aktif"
    db.session.commit()
```

-   `dasar = max(kartu.tanggal_kadaluarsa, date.today())` --- `max()`
    dipakai pada dua objek `date` (bukan angka), Python tetap bisa
    membandingkan objek tanggal secara langsung. Logikanya (dijelaskan
    di docstring fungsi): jika kartu **masih berlaku**, perpanjangan
    dihitung dari tanggal kadaluarsa lama (menambah durasi); jika kartu
    **sudah kadaluarsa**, perpanjangan dihitung dari hari ini (tidak
    "merugikan" user dengan menghitung dari tanggal lama yang sudah
    lewat jauh).
-   `kartu.status = "aktif"` --- memperpanjang kartu juga otomatis
    mengaktifkan kembali kartu yang sebelumnya berstatus `"nonaktif"`,
    dalam satu aksi.

> **Ringkasan bab:** Satu kartu per user; ID kartu = NIM; punya masa
> berlaku dan status.

### 15.4 `toggle_kartu()` --- Aktifkan/Nonaktifkan Kartu

Route `POST /kartu/kelola/<id>/toggle` hanya dapat dipakai staf dan
kepala perpustakaan. Fungsi ini membalik status kartu: `aktif` menjadi
`nonaktif`, atau `nonaktif` menjadi `aktif`, lalu menyimpan perubahan
dan menampilkan pesan `flash`.

Berbeda dari `perpanjang_kartu()`, `toggle_kartu()` **tidak mengubah
tanggal kadaluarsa**. Kartu yang nonaktif tidak lolos properti
`KartuAnggota.bisa_dipakai`, sehingga validasi `cek_kartu_valid()`
menolak peminjaman baru. Ini merupakan cara cepat memblokir penggunaan
kartu tanpa menonaktifkan akun pengguna. Mengaktifkan kembali kartu juga
tidak memperbarui tanggal kadaluarsa; kartu yang sudah kadaluarsa tetap
tidak dapat dipakai sampai masa berlakunya diperbaiki.

## BAB 16 --- Denda dan Pengaturan

> **File dibahas:** `routes/denda.py, routes/pengaturan.py`\
> **Tujuan belajar:** Memahami pengelolaan denda dan halaman pengaturan
> sistem.\
> **Prasyarat:** Bab 9, 17

### 16.1 `_query_denda()` & `daftar_denda()` (baris 23--75)

``` python
STATUS_LABEL = {
    "belum_lunas": "Belum Lunas", "lunas": "Lunas",
    "dibebaskan": "Dibebaskan", "tidak_ada": "-",
}

def _query_denda(status, q):
    query = Peminjaman.query.filter(Peminjaman.denda > 0)
    if status in ("belum_lunas", "lunas", "dibebaskan"):
        query = query.filter(Peminjaman.status_denda == status)
    ...
```

-   `STATUS_LABEL` --- dictionary pemetaan nilai Enum database ke label
    tampilan, pola yang sama dengan `ROLE_LABEL` di `models.py`.
-   `Peminjaman.denda > 0` --- filter dasar: hanya peminjaman yang
    **sudah selesai dan dendanya dibekukan** (nilai `denda` terisi angka
    positif saat pengembalian, seperti dijelaskan di
    `kembalikan_buku()`), bukan denda yang masih berjalan/belum
    dihitung.

``` python
@denda_bp.route("/")
@login_required
@role_required("staf", "kepala_perpustakaan")
def daftar_denda():
    status = request.args.get("status", "belum_lunas")
    q = request.args.get("q", "").strip()
    if status == "berjalan":
        semua = Peminjaman.query.filter_by(status="dipinjam").order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all()
        daftar = [p for p in semua if denda_peminjaman(p) > 0 or p.hari_telat > 0]
        if q:
            k = q.lower()
            daftar = [p for p in daftar if k in p.anggota.nama_lengkap.lower()
                      or k in p.anggota.username.lower() or k in p.buku.judul.lower()]
    else:
        daftar = _query_denda(status, q).order_by(Peminjaman.tanggal_kembali.desc()).all()
```

-   Status `"berjalan"` adalah kasus **khusus**: ini bukan nilai
    `status_denda` yang ada di database, melainkan kategori buatan di
    level aplikasi untuk menampilkan peminjaman yang **masih dipinjam**
    tapi sudah telat (dendanya terus bertambah tiap hari, belum
    dibekukan). Karena itu, logikanya **tidak** lewat `_query_denda()`
    (yang mensyaratkan `denda > 0` di database), melainkan dihitung
    manual di Python memakai `denda_peminjaman(p)` (fungsi berjalan,
    bukan nilai tersimpan).
-   Pencarian untuk status `"berjalan"` juga dilakukan **manual di
    Python** (`k in p.anggota.nama_lengkap.lower()`) karena datanya
    sudah diambil semua dan disaring di memori, berbeda dari
    `_query_denda()` yang memakai `.ilike()` di level SQL.

``` python
    awal_bulan = date.today().replace(day=1)
    total_belum_lunas = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "belum_lunas").scalar() or 0
    terkumpul_bulan_ini = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "lunas", Peminjaman.tanggal_denda_selesai >= awal_bulan).scalar() or 0
```

-   `func.coalesce(func.sum(...), 0)` --- `COALESCE` di SQL
    mengembalikan nilai pertama yang **tidak NULL** dari daftar
    argumennya; di sini dipakai supaya jika `SUM` menghasilkan NULL
    (tidak ada baris cocok sama sekali), hasilnya langsung jadi 0 dari
    sisi database, bukan `None` dari Python.
-   `.scalar()` --- mengambil **satu nilai tunggal** dari hasil query
    (bukan list of tuple seperti `.all()`), cocok dipakai saat query
    memang hanya menghasilkan satu angka (hasil `SUM`).
-   `or 0` --- lapisan pengaman tambahan meski sudah ada `COALESCE`,
    untuk berjaga-jaga jika `.scalar()` tetap mengembalikan `None` dalam
    kondisi tertentu (misalnya tidak ada baris sama sekali di tabel).

### 16.2 `lunasi()` & `bebaskan()` (baris 78--111)

``` python
@denda_bp.route("/<int:peminjaman_id>/lunas", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def lunasi(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status_denda != "belum_lunas":
        flash("Denda ini tidak berstatus belum lunas.", "warning")
        return redirect(request.referrer or url_for("denda.daftar_denda"))
    p.status_denda = "lunas"
    p.tanggal_denda_selesai = date.today()
    p.denda_diproses_oleh = current_user.id
    db.session.commit()
```

-   Staf/kepala **berdua** boleh mencatat denda lunas (pembayaran
    normal).

``` python
@denda_bp.route("/<int:peminjaman_id>/bebaskan", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def bebaskan(peminjaman_id):
    """Hapus denda tanpa pembayaran (mis. alasan khusus). Khusus kepala perpustakaan."""
    ...
    p.status_denda = "dibebaskan"
    p.tanggal_denda_selesai = date.today()
    p.denda_diproses_oleh = current_user.id
    p.catatan_denda = request.form.get("catatan", "").strip()[:255] or None
```

-   Berbeda dari `lunasi()`, **hanya kepala perpustakaan** yang boleh
    membebaskan denda (menghapuskan kewajiban bayar tanpa pembayaran)
    --- tindakan ini lebih sensitif secara finansial, sehingga dibatasi
    lebih ketat.
-   `.strip()[:255]` --- memotong teks catatan maksimal 255 karakter
    **sebelum** disimpan, sesuai batas panjang kolom `catatan_denda` di
    `models.py` (`db.String(255)`) --- mencegah error database jika user
    memasukkan teks yang terlalu panjang (pemotongan dilakukan di kode,
    bukan dibiarkan database yang menolak).

### 16.3 `routes/pengaturan.py`

``` python
from utils.pengaturan import DAFTAR, nilai_saat_ini, simpan_pengaturan

@pengaturan_bp.route("/", methods=["GET", "POST"])
@login_required
@role_required("kepala_perpustakaan")
def halaman():
    if request.method == "POST":
        baru, galat = {}, []
        for kunci, _cfg, minimum, maksimum, label, satuan, _bantuan in DAFTAR:
            mentah = request.form.get(kunci, "").strip().replace(".", "")
            try:
                nilai = int(mentah)
            except ValueError:
                galat.append(f"{label}: isi dengan angka bulat.")
                continue
            if not (minimum <= nilai <= maksimum):
                galat.append(f"{label}: harus antara {minimum} dan {maksimum}.")
                continue
            baru[kunci] = nilai
```

-   `DAFTAR` (diimpor dari `utils/pengaturan.py`) --- list berisi
    *tuple* definisi semua pengaturan yang bisa diubah (kunci, info
    konfigurasi, batas minimum/maksimum, label tampilan, satuan, teks
    bantuan) --- satu sumber data dipakai untuk **membangun form secara
    otomatis** (lewat perulangan `for`) dan **memvalidasi input** dengan
    cara yang sama, sehingga menambah satu pengaturan baru di masa depan
    hanya perlu menambah satu baris di `DAFTAR`, tidak perlu menulis
    form/validasi manual satu-satu.
-   `for kunci, _cfg, minimum, maksimum, label, satuan, _bantuan in DAFTAR:`
    --- *tuple unpacking* tujuh elemen sekaligus; elemen yang tidak
    dipakai langsung di loop ini (`_cfg`, `_bantuan`) tetap diberi nama
    (dengan prefix underscore sebagai penanda "sengaja tidak dipakai di
    sini"), karena posisinya di tuple tetap harus dicocokkan.
-   `request.form.get(kunci, "").strip().replace(".", "")` ---
    `.replace(".", "")` membuang tanda titik dari input. Ini
    mengantisipasi kemungkinan input dari field yang menampilkan angka
    dengan **pemisah ribuan** (misalnya `"1.000"` untuk seribu, format
    umum Indonesia), supaya tetap bisa dikonversi jadi angka murni
    `1000` oleh `int()`.
-   `if not (minimum <= nilai <= maksimum):` --- Python mendukung
    **perbandingan berantai** (*chained comparison*): ekspresi ini
    setara `minimum <= nilai and nilai <= maksimum`, memeriksa apakah
    nilai berada dalam rentang yang diizinkan.
-   `continue` --- melanjutkan ke iterasi `for` berikutnya tanpa
    menambahkan `kunci` ini ke `baru` --- artinya field yang gagal
    validasi **tidak** ikut disimpan, sementara field lain yang valid di
    baris lain tetap diproses secara independen.

``` python
        if galat:
            for g in galat:
                flash(g, "danger")
        else:
            simpan_pengaturan(baru)
            flash("Pengaturan disimpan. Berlaku untuk peminjaman berikutnya; "
                  "peminjaman yang sudah berjalan tidak berubah jatuh temponya.", "success")
        return redirect(url_for("pengaturan.halaman"))
```

-   `if galat:` --- semua kesalahan validasi dikumpulkan dulu di list
    `galat` selama perulangan `for` di atas (bukan langsung `return` di
    baris pertama yang gagal seperti di route lain) --- supaya user bisa
    melihat **semua kesalahan sekaligus** dalam satu kali submit, bukan
    harus submit berkali-kali untuk menemukan error satu per satu.
-   `simpan_pengaturan(baru)` **hanya** dipanggil jika **tidak ada**
    error sama sekali di seluruh field --- kebijakan
    "semua-atau-tidak-sama-sekali" (*all-or-nothing*): kalau ada satu
    saja pengaturan yang nilainya tidak valid, seluruh perubahan
    dibatalkan, tidak ada yang disimpan sebagian.
-   Pesan sukses dengan sengaja menjelaskan **batasan** fitur ini:
    pengaturan baru hanya berlaku untuk peminjaman *berikutnya*,
    peminjaman yang sedang berjalan tidak otomatis ikut berubah jatuh
    temponya --- informasi penting supaya kepala perpustakaan tidak
    salah ekspektasi.

``` python
    nilai = nilai_saat_ini(current_app)
    kolom = [
        {"kunci": k, "label": label, "satuan": satuan, "bantuan": bantuan,
         "min": mn, "maks": mx, "nilai": nilai[k]}
        for k, _c, mn, mx, label, satuan, bantuan in DAFTAR
    ]
    return render_template("pengaturan/halaman.html", kolom=kolom)
```

-   Saat menampilkan form (`GET`), `DAFTAR` yang sama diubah menjadi
    list of dictionary (`kolom`) --- tiap dictionary berisi semua info
    yang dibutuhkan template untuk merender satu baris form input
    (label, satuan, batas min/maks, nilai saat ini) --- template cukup
    melakukan satu perulangan `{% for k in kolom %}` untuk menampilkan
    seluruh form pengaturan, tanpa perlu menulis HTML berulang untuk
    tiap pengaturan satu-satu.

> **Ringkasan bab:** Denda dibekukan saat pengembalian lalu
> dilunasi/dibebaskan; pengaturan disimpan di DB.

### 16.4 Ekspor Denda --- `GET /denda/ekspor`

Route ini hanya untuk staf dan kepala perpustakaan. Parameter query
`status` secara default bernilai `semua`. Route memanggil
`_query_denda(status, "")`, yaitu query yang sama dengan daftar denda
untuk status tersimpan, tetapi tanpa kata pencarian.

Kolom file Excel:

  Kolom             Isi
  ----------------- -----------------------------------------------
  Mahasiswa         Nama lengkap peminjam
  NIM/Username      NIM jika tersedia; jika tidak, username
  Buku              Judul buku
  Tgl Pinjam        Tanggal peminjaman
  Jatuh Tempo       Batas pengembalian
  Tgl Kembali       Tanggal pengembalian; `-` jika belum tersedia
  Hari Telat        Jumlah hari terlambat
  Denda (Rp)        Nilai denda sebagai angka
  Status            Label status denda
  Tgl Lunas/Bebas   Tanggal denda diselesaikan; `-` jika kosong

Tanggal ditulis menggunakan `strftime("%d-%m-%Y")`; nilai tanggal kosong
menjadi `-`. Nilai `Denda (Rp)` disimpan sebagai **angka**, bukan teks
berformat seperti `Rp 1.500`, sehingga dapat langsung dijumlahkan atau
dihitung di Excel. Nama file mengikuti pola
`laporan_denda_<tanggal>.xlsx`.

**Batasan ekspor yang perlu diketahui:**

-   Status `berjalan` tidak ikut diekspor. `_query_denda()` membatasi
    query pada `Peminjaman.denda > 0`, sedangkan denda yang masih
    berjalan dihitung secara real-time dan belum dibekukan ke kolom
    database `denda`.
-   Kolom `catatan_denda` tidak disertakan, sehingga alasan pembebasan
    denda tidak terlihat di file ekspor. Route `bebaskan()` memang
    menyimpan catatan maksimal 255 karakter, tetapi kode ekspor saat ini
    tidak mengambil kolom tersebut.
-   Filter `status=semua` berarti semua transaksi yang mempunyai denda
    tersimpan lebih dari nol; bukan berarti termasuk denda berjalan.

## BAB 17 --- Fungsi Bantu (utils)

> **File dibahas:** `utils/*.py`\
> **Tujuan belajar:** Memahami fungsi bantu yang dipakai banyak route.\
> **Prasyarat:** Bab 8, 9

### 17.1 `utils/decorators.py` (19 baris)

-   Baris 1--3: impor `wraps` (menjaga nama/docstring fungsi asli),
    `abort` (menghentikan request dengan kode error), `current_user`
    (user yang login).
-   Baris 6: `role_required(*roles)` --- menerima satu atau lebih nama
    role yang diizinkan.
-   Baris 10--11: dekorator berlapis: `decorator(f)` membungkus fungsi
    route `f`.
-   Baris 12: `@wraps(f)` --- agar nama endpoint Flask tidak berubah
    jadi `wrapped`.
-   Baris 13--14: jika belum login → `abort(401)` (tidak
    terautentikasi).
-   Baris 15--16: jika role user tidak ada di daftar → `abort(403)`
    (dilarang).
-   Baris 17: lolos semua cek → jalankan fungsi route aslinya.
-   Baris 18--19: kembalikan pembungkus dan dekoratornya.

### 17.2 `utils/pengaturan.py` (60 baris)

Mengelola pengaturan yang bisa diubah kepala perpustakaan lewat web
(disimpan di tabel `pengaturan`). - Baris 8--9: impor `db` dan model
`Pengaturan`. - Baris 11--29: `DAFTAR` --- tiap item berisi: kunci DB,
kunci di `app.config`, nilai min, nilai maks, label, satuan, teks
bantuan. Delapan pengaturan: lama pinjam (1--365 hari), maks pinjam per
mahasiswa (1--50), peringatan jatuh tempo (0--30 hari), denda per hari,
denda maksimal (0 = tanpa batas), masa tenggang, maks perpanjangan (0 =
dilarang), blokir jika ada denda (0/1). - Baris 32:
`terapkan_pengaturan(app)` --- dipanggil di `before_request` (lihat Bab
8). - Baris 34--38: `try` mengambil semua baris tabel jadi dict
`{kunci: nilai}`; jika tabel belum ada, `rollback()` lalu `return`
(aman, config default dari `config.py` dipakai). - Baris 39--44: untuk
tiap pengaturan yang ada di DB, ubah ke `int` dan timpa `app.config`;
jika nilai bukan angka (`ValueError`) diabaikan. - Baris 47--49:
`nilai_saat_ini(app)` --- dict nilai yang sedang berlaku, untuk mengisi
form pengaturan. - Baris 52--60: `simpan_pengaturan(data)` --- untuk
tiap pasangan: `db.session.get` mencari baris; ada → update `nilai`
(disimpan sebagai string), belum ada → `add` baris baru; lalu `commit()`
sekali di akhir.

### 17.3 `utils/denda.py` (64 baris)

-   Baris 2--8: impor `date`, `current_app`, `func` (fungsi SQL seperti
    SUM), `db`, `Peminjaman`.
-   Baris 11--25:
    `hitung_denda(jatuh_tempo, sampai, tarif, maks, tenggang)` ---
    **fungsi murni** (tanpa akses DB, mudah diuji).
    -   Baris 19: hari kena denda = selisih hari − masa tenggang.
    -   Baris 20--21: jika ≤ 0 atau tarif ≤ 0 → denda 0.
    -   Baris 22: total = hari × tarif.
    -   Baris 23--24: jika ada batas `maks` dan total melebihi →
        dipotong ke `maks`.
-   Baris 28--30: `denda_dari_config` --- memanggil fungsi di atas
    dengan nilai dari `app.config`.
-   Baris 33--42: `denda_peminjaman(p)` --- `dikembalikan` → pakai denda
    yang sudah dibekukan (`p.denda`); `dipinjam` → denda berjalan sampai
    hari ini; status lain → 0. (Didaftarkan sebagai global Jinja
    `denda_sekarang`.)
-   Baris 45--52: `total_denda_belum_lunas(user_id=None)` ---
    `SUM(denda)` yang `status_denda == "belum_lunas"`,
    `coalesce(..., 0)` agar hasil 0 bukan `None`; jika `user_id`
    diberikan, difilter per anggota.
-   Baris 55--60: `denda_berjalan_semua` --- menjumlahkan denda buku
    yang masih dipinjam dan telat.
-   Baris 63--64: `format_rupiah` --- angka → `"Rp 1.500"` (format
    ribuan Python memakai koma, lalu diganti titik). Didaftarkan sebagai
    filter Jinja `rupiah`.

### 17.4 `utils/pinjam.py` (80 baris) --- Aturan Validasi Peminjaman

-   Baris 1--7: impor `timedelta`, `current_app`, model, serta fungsi
    dari `denda.py` dan `kartu.py`.
-   Baris 10--16: `lama_pinjam_untuk` --- prioritas: isian petugas \>
    pengaturan khusus buku (`buku.lama_pinjam_hari`) \> pengaturan umum.
-   Baris 19--20: `hitung_jatuh_tempo` = tanggal mulai + lama pinjam.
-   Baris 23--46: `cek_tunggakan` --- jika `BLOKIR_JIKA_DENDA` mati →
    lolos. Jika aktif: (29--38) cari peminjaman `dipinjam` milik
    mahasiswa dengan `hari_telat > 0`; ada → ditolak dengan pesan jumlah
    buku & denda berjalan. (40--45) lalu cek denda belum lunas \> 0 →
    ditolak. Selain itu lolos.
-   Baris 49--60: `cek_kartu_valid` --- kartu diterbitkan otomatis bila
    belum ada; status harus `aktif` dan tidak kadaluarsa
    (`is_kadaluarsa`), jika tidak → pesan error beserta tanggal.
-   Baris 63--71: `cek_kuota_pinjam` --- `jumlah_pinjaman_aktif`
    (diajukan + dipinjam) tidak boleh ≥ `MAKS_PINJAM_PER_USER`.
-   Baris 74--80: `cek_bisa_meminjam` --- menjalankan tiga cek berurutan
    (kartu → tunggakan → kuota); berhenti di kegagalan pertama. Semua
    fungsi `cek_*` mengembalikan tuple `(True, None)` atau
    `(False, pesan)`.

### 17.5 `utils/kartu.py` (51 baris)

-   Baris 1--6: impor `date`, `timedelta`, `current_app`, `db`,
    `KartuAnggota`, `User`.
-   Baris 9--35: `validasi_nim(nim, wajib, abaikan_user_id)` →
    `(nim, error)`.
    -   18: bersihkan spasi. 19--22: kosong → error jika `wajib`
        (mahasiswa), kalau tidak `None` (staf/kepala).
    -   24--28: ambil panjang min/maks dari config (default 8--12);
        harus angka (`isdigit`) dan dalam rentang, pesan rentang
        menyesuaikan.
    -   30--34: cek keunikan NIM di tabel `users`; `abaikan_user_id`
        dipakai saat edit agar NIM milik sendiri tidak dianggap
        duplikat.
-   Baris 38--51: `terbitkan_kartu_jika_belum_ada(user)` --- jika
    `user.kartu` sudah ada, kembalikan; jika belum, buat `KartuAnggota`
    (terbit hari ini, kadaluarsa + `MASA_BERLAKU_KARTU_HARI` = 365 hari,
    status `aktif`), `commit`, kembalikan.

### 17.6 `utils/excel_export.py` (27 baris)

-   Baris 2--5: impor `BytesIO` (file di memori, tanpa menyimpan ke
    disk) dan style `openpyxl`.
-   Baris 8: `buat_excel(judul_sheet, header, baris)`.
-   Baris 10--12: buat workbook; judul sheet dipotong 31 karakter (batas
    Excel).
-   Baris 13--17: tulis header lalu beri gaya: teks putih tebal, latar
    `5C211D` (merah marun), rata tengah vertikal.
-   Baris 18--19: tulis semua baris data.
-   Baris 20--22: lebar tiap kolom = panjang teks terpanjang + 3,
    maksimal 50.
-   Baris 23: `freeze_panes="A2"` --- header tetap terlihat saat scroll.
-   Baris 24--27: simpan ke buffer, kembalikan posisi ke awal
    (`seek(0)`) lalu return untuk dikirim via `send_file`.

### 17.7 `utils/excel_import.py` (84 baris)

-   Baris 7--10: `TEMPLATE_HEADERS` --- 8 kolom wajib: judul, penulis,
    penerbit, tahun_terbit, isbn, kategori, deskripsi, stok.
-   Baris 13--33: `buat_template_excel()` --- workbook "Data Buku"
    berisi header + 1 baris contoh; lebar kolom disesuaikan (minimal
    12); dikembalikan sebagai `BytesIO`.
-   Baris 36--83: `import_buku_dari_excel(file_stream)` →
    `(jumlah_sukses, list_error)`.
    -   40--43: `load_workbook(data_only=True)` (nilai rumus, bukan
        rumusnya), baca sheet aktif mulai baris 2.
    -   47--49: lewati baris yang seluruh selnya kosong.
    -   52--54: *unpack* 8 kolom; baris yang kurang kolom diisi `None`
        dan yang berlebih dipotong.
    -   56--58: judul & penulis wajib; jika kosong → catat error, lanjut
        baris berikutnya.
    -   60--66: kategori dicari berdasarkan nama; jika belum ada dibuat
        baru dan `flush()` agar `id`-nya langsung tersedia.
    -   68--79: buat objek `Buku` (teks di-`strip`, angka dikonversi
        `int`, kolom opsional kosong → `None`/0), lalu `add` dan hitung
        sukses.
    -   80--81: error pada satu baris ditangkap dan dicatat, tidak
        menggagalkan baris lain.
    -   83--84: satu `commit()` untuk semua baris, kembalikan hasil.

> **Ringkasan bab:** Berisi dekorator role, pengaturan dinamis, hitung
> denda, validasi peminjaman, kartu, dan Excel.

## BAB 18 --- Skrip Akun Awal (seed_admin.py)

> **File dibahas:** `seed_admin.py`\
> **Tujuan belajar:** Membuat akun kepala perpustakaan pertama.\
> **Prasyarat:** Bab 3, 9

### 18.1 Cara Memakai

Dari folder `Website`, jalankan `python seed_admin.py`, lalu isi
username, email, nama lengkap, dan password.

### 18.2 Penjelasan Kode

Skrip satu kali untuk membuat akun **kepala perpustakaan** pertama
(registrasi publik hanya membuat mahasiswa). - Baris 1--4: impor
`getpass` (input password tersembunyi), `create_app`, `db`, `User`. -
Baris 6--8: buat app dan masuk `app_context()` agar bisa memakai
database di luar request. - Baris 10--11: jika sudah ada user berrole
`kepala_perpustakaan` → beri tahu dan berhenti. - Baris 13--16: minta
username, email, nama lengkap, password. - Baris 18--19: username
dipakai → batal. - Baris 21--25: buat `User` role `kepala_perpustakaan`,
`set_password` (di-hash), `add`, `commit`, cetak pesan sukses.

> **Ringkasan bab:** Skrip sekali jalan yang membuat user role
> `kepala_perpustakaan` dengan password ter-hash.

# BAGIAN V --- LAMPIRAN

## BAB 19 --- Template, CSS, dan Front-End

> **File dibahas:** `templates/`, `static/css/`, `static/`, `routes/`\
> **Tujuan belajar:** Memahami pewarisan template, navigasi per role,
> ikon, tema, pemuatan halaman, CSS responsif, dan grafik.\
> **Prasyarat:** Bab 8

### 19.1 Struktur pewarisan Jinja2

Hampir semua halaman menggunakan:

``` jinja2
{% extends "layout/base.html" %}
```

`layout/base.html` menjadi kerangka bersama (466 baris pada arsip yang
diperiksa). Template halaman mengisi blok berikut:

  ---------------------------------------------------------------------
  Blok                               Fungsi
  ---------------------------------- ----------------------------------
  `title`                            Judul tab; otomatis diakhiri
                                     `- STIKOM Kendari` oleh
                                     `base.html`

  `extra_head`                       Tambahan elemen di bagian
                                     `<head>`, misalnya pemuatan
                                     Chart.js

  `content`                          Isi utama halaman

  `scripts`                          JavaScript tambahan di bagian
                                     akhir `<body>`
  ---------------------------------------------------------------------

Pola ini menghindari pengulangan navbar, sidebar, flash message, footer,
CSS, dan JavaScript dasar di setiap file halaman.

### 19.2 Navigasi berdasarkan role

Di awal bagian body, `base.html` menetapkan:

``` jinja2
{% set pakai_sidebar = current_user.is_authenticated and current_user.is_kepala %}
```

Kepala perpustakaan mendapatkan sidebar dengan kelompok menu, antara
lain Koleksi dan Sirkulasi. Mahasiswa, staf, dan pengunjung yang belum
login menggunakan pola navigasi atas yang sesuai dengan status/role
masing-masing.

Class pada `<body>` juga berubah mengikuti kondisi, misalnya
`has-sidebar`, `role-mahasiswa`, atau `guest`. CSS memakai class ini
untuk menyesuaikan tata letak dan navigasi.

### 19.3 Ikon SVG sprite

`templates/layout/icons.html` berisi kumpulan ikon SVG yang di-include
sekali di `base.html`. Ikon dipakai ulang melalui referensi ID,
contohnya:

``` html
<svg class="icon"><use href="#i-book"></use></svg>
```

Cara ini mengurangi kebutuhan file gambar ikon terpisah dan menjaga gaya
ikon konsisten.

### 19.4 Tema terang dan gelap

Atribut `data-theme` pada elemen `<html>` menentukan tema. Skrip kecil
di bagian `<head>` membaca nilai dari `localStorage` dengan kunci `tema`
lalu menetapkan atribut sebelum halaman dirender. Tujuannya mengurangi
efek layar berkedip ketika tema tersimpan berbeda dari tema default.

Warna utama ditentukan sebagai variabel CSS di `static/css/style.css`,
misalnya `--primary` (maroon `#5c211d`), `--accent` (emas), `--danger`,
dan `--success`. Variabel ini ditimpa pada tema gelap sehingga komponen
mengikuti tema yang sedang dipilih.

### 19.5 Page loader

Loader berlogo pada `base.html` hanya ditampilkan pada endpoint
`auth.register`, `auth.login`, dan `buku.daftar_buku`. Halaman lainnya
memakai class `page-loader-hidden`, sehingga loader awal tidak menutupi
isi halaman yang tidak memerlukannya.

### 19.6 CSS desktop dan perangkat kecil

  ---------------------------------------------------------------------
  File                               Peran
  ---------------------------------- ----------------------------------
  `static/css/style.css`             Gaya utama aplikasi (1.574 baris
                                     pada arsip yang diperiksa)

  `static/css/mobile.css`            Penyesuaian perangkat kecil (213
                                     baris pada arsip yang diperiksa)
  ---------------------------------------------------------------------

Keduanya dimuat melalui `base.html`; `mobile.css` dimuat setelah
`style.css` agar aturan responsif dapat menyesuaikan gaya utama. Meta
viewport menggunakan `viewport-fit=cover` untuk mendukung layar
perangkat dengan notch dan area aman.

### 19.7 Dashboard dan grafik Chart.js

`templates/dashboard.html` memuat Chart.js 4.4.1 dari CDN cdnjs. Skrip
memeriksa:

``` javascript
if (typeof Chart === 'undefined') return;
```

Jika library gagal dimuat---misalnya karena jaringan tidak memiliki
akses internet---inisialisasi grafik dilewati dan bagian dashboard
lainnya tetap dapat tampil. Warna teks dan garis grafik disesuaikan
dengan tema melalui variabel CSS, termasuk `Chart.defaults.color`.

### 19.8 Ketergantungan internet

Font Inter dimuat dari Google Fonts dan Chart.js dari CDN. Jika aplikasi
dijalankan di jaringan kampus tanpa internet, font akan jatuh ke font
sistem dan grafik tidak tampil. Fitur aplikasi yang diproses oleh Flask
dan database tetap dapat berjalan, selama seluruh dependensi Python dan
MySQL sudah tersedia secara lokal.

### 19.9 Peta template

  ----------------------------------------------------------------------
  File                                Dipakai oleh / fungsi
  ----------------------------------- ----------------------------------
  `layout/base.html`                  Kerangka umum halaman, navigasi,
                                      flash message, footer, CSS dan
                                      JavaScript bersama

  `layout/icons.html`                 SVG sprite ikon yang digunakan
                                      ulang

  `auth/login.html`,                  `login()` dan `register()`
  `auth/register.html`                

  `auth/persetujuan.html`             `daftar_persetujuan()`

  `auth/profil.html`                  `profil()`

  `auth/daftar_pengguna.html`,        Daftar, tambah, dan edit pengguna
  `auth/tambah_pengguna.html`,        
  `auth/edit_pengguna.html`           

  `buku/daftar.html`,                 Daftar dan detail buku
  `buku/detail.html`                  

  `buku/form.html`                    `tambah_buku()` dan `edit_buku()`;
                                      satu form dipakai untuk dua fungsi

  `buku/kategori.html`,               Kelola kategori dan impor Excel
  `buku/import_excel.html`            

  `peminjaman/pengajuan.html`         Daftar pengajuan yang menunggu
                                      diproses

  `peminjaman/pinjam.html`,           Form pinjam langsung dan daftar
  `peminjaman/daftar.html`            peminjaman

  `peminjaman/riwayat_anggota.html`   `riwayat_saya()` dan
                                      `riwayat_anggota()`; perilaku
                                      tombol dapat berbeda melalui flag
                                      `bisa_batalkan`

  `peminjaman/riwayat_buku.html`      Riwayat peminjaman per buku

  `kartu/kartu.html`,                 Kartu digital, edit, dan
  `kartu/edit.html`,                  pengelolaan kartu
  `kartu/kelola.html`                 

  `kartu/cetak.html`                  Versi cetak kartu
                                      (`kartu_saya_cetak`,
                                      `kartu_anggota_lain_cetak`)

  `denda/daftar.html`                 Daftar denda, pembayaran, dan
                                      pembebasan

  `laporan/populer.html`,             Laporan buku populer dan tidak
  `laporan/tidak_populer.html`        populer

  `laporan/mahasiswa_aktif.html`,     Laporan mahasiswa aktif dan buku
  `laporan/terlambat.html`            terlambat

  `dashboard.html`                    Ringkasan statistik dan grafik

  `pengaturan/halaman.html`           Form pengaturan sistem
  ----------------------------------------------------------------------

Arsip yang diperiksa berisi **30 file template HTML**. Daftar di atas
dikelompokkan berdasarkan fungsi; beberapa template lain digunakan untuk
alur yang tidak dirinci satu per satu di tabel.

> **Ringkasan bab:** `base.html` menyediakan kerangka dan navigasi
> berdasarkan role; template khusus mengisi blok halaman, sedangkan CSS
> dan JavaScript mengatur tema, responsivitas, loader, dan grafik.

## BAB 20 --- Troubleshooting

> **Tujuan belajar:** Mendiagnosis error umum saat setup dan pemakaian.\
> **Prasyarat:** Bab 3

### 20.1 Masalah Umum dan Solusinya

  -----------------------------------------------------------------------------------------------
  Gejala                              Penyebab umum           Solusi
  ----------------------------------- ----------------------- -----------------------------------
  `Unknown column 'nim'/'denda'...`   memakai                 impor ulang dengan
                                      `Database/schema.sql`   `Website/schema.sql`
                                      lama                    

  `Can't connect to MySQL server`     MySQL belum jalan /     nyalakan MySQL; cek
                                      `.env` salah            `DB_HOST/PORT/USER/PASSWORD`

  `Access denied for user`            password/user salah     perbaiki `.env`

  `ModuleNotFoundError`               paket belum terpasang / `pip install -r requirements.txt`
                                      venv belum aktif        di venv yang benar

  `Unknown database`                  schema belum dijalankan jalankan `schema.sql`

  Tidak bisa login setelah daftar     akun masih `pending`    setujui lewat menu Persetujuan
                                                              (kepala)

  Gambar sampul tidak tampil          folder upload/izin      pastikan `static/uploads/sampul`
                                      tulis                   ada dan bisa ditulis

  Upload ditolak                      file \> 5 MB atau       kecilkan; hanya png/jpg/jpeg/webp
                                      format tidak diizinkan  (gambar) dan xlsx (Excel)

  Halaman 401/403                     belum login / role      login dengan role yang sesuai
                                      tidak berhak            

  Port 5000 dipakai                   aplikasi lain           ubah `port=` di `app.py`
  -----------------------------------------------------------------------------------------------

**Catatan keamanan:** ganti `SECRET_KEY`, jangan bagikan `.env`, matikan
`debug=True` untuk penggunaan nyata, dan jangan buka ke internet tanpa
HTTPS.

> **Ringkasan bab:** Kebanyakan masalah berasal dari skema lama, `.env`,
> atau paket belum terpasang.

## BAB 21 --- Catatan Konsistensi Dokumen Lama

Pemeriksaan terhadap arsip ZIP menunjukkan bahwa sebagian dokumentasi
pendamping belum diperbarui mengikuti kode aplikasi saat ini. Bab ini
mencatat kondisi yang ditemukan pada arsip sumber; rekomendasi
penyelarasan dokumentasi ada pada tabel berikut.

  -----------------------------------------------------------------------
  File / bagian           Keterangan lama atau    Penyesuaian yang benar
                          masalah                 
  ----------------------- ----------------------- -----------------------
  `README.md` dan         Masih menyebut role     Kode memakai role
  `Informasi/Teknis.md`   `user`/`operator`       `mahasiswa`, `staf`,
                                                  dan
                                                  `kepala_perpustakaan`

  `README.md`             Menyebut lima tabel     Skema terbaru di
                          database                `Website/schema.sql`
                                                  memiliki tujuh tabel:
                                                  `users`,
                                                  `kartu_anggota`,
                                                  `kategori`, `buku`,
                                                  `peminjaman`,
                                                  `pengaturan`, dan
                                                  `log_stok`

  `README.md` dan         Menyarankan menyalin    File `.env.example`
  `Informasi/Teknis.md`   `.env.example`          tidak ada di ZIP; buat
                                                  `Website/.env` sendiri
                                                  berdasarkan variabel di
                                                  Bab 3

  `Website/.gitignore`    Mengecualikan `.env`,   Ini membantu mencegah
                          `venv/`,                file tertentu masuk
                          `__pycache__/`, dan isi Git, tetapi **tidak
                          folder sampul kecuali   membuat ZIP otomatis
                          `.gitkeep`              aman**. Arsip yang
                                                  diperiksa justru
                                                  menyertakan
                                                  `Website/.env`; jangan
                                                  bagikan file itu
                                                  sebelum rahasia di
                                                  dalamnya dihapus dan
                                                  kredensial diganti

  `Website/schema.sql` vs Ada dua versi skema     Gunakan
  `Database/schema.sql`                           `Website/schema.sql`
                                                  karena sesuai dengan
                                                  model dan route terkini
  -----------------------------------------------------------------------

> **Catatan:** Temuan di atas merupakan koreksi dokumentasi dan panduan
> operasional. Rekomendasi keamanan pada Lampiran A adalah pekerjaan
> perbaikan kode yang perlu diterapkan dan diuji secara terpisah; jangan
> menganggap rekomendasi tersebut sudah diterapkan hanya karena
> tercantum dalam dokumen.

## LAMPIRAN A --- Catatan Temuan dan Keamanan

  --------------------------------------------------------------------------------------------------------
  No          Temuan                                  Dampak                  Saran
  ----------- --------------------------------------- ----------------------- ----------------------------
  1           `Database/schema.sql` adalah versi lama Aplikasi error jika     Pakai `Website/schema.sql`;
              (kolom `nisn`, tanpa tabel              dipakai                 hapus/ganti file lama
              `pengaturan`/`log_stok`, tanpa kolom                            
              denda)                                                          

  2           README menyebut `.env.example`, tetapi  Pemula bingung          Buat `.env.example` tanpa
              file itu tidak ada di zip               menyiapkan `.env`       nilai rahasia

  3           `seed_admin.py`, README, dan komentar   Tidak konsisten dengan  Samakan istilah
              SQL masih memakai istilah "operator"    role                    
                                                      `kepala_perpustakaan`   

  4           `.env` (password DB, `SECRET_KEY`) ikut Rahasia bisa bocor      Jangan dibagikan; ganti
              dalam zip                                                       `SECRET_KEY`

  5           `app.run(debug=True, host="0.0.0.0")`   Debug terbuka di        Matikan debug untuk
                                                      jaringan                pemakaian nyata

  6           `run.bat` memakai `python` sistem,      Paket tidak ditemukan   Aktifkan venv atau arahkan
              bukan venv                                                      ke python venv

  7           Tidak ditemukan proteksi CSRF:          Browser staf/kepala     Pasang proteksi CSRF
              pencarian istilah `csrf`/`CSRFProtect`  yang sedang login       (misalnya
              pada berkas proyek tidak menemukan      berpotensi dipancing    `Flask-WTF`/`CSRFProtect`)
              implementasi; `Flask-WTF` juga tidak    situs lain untuk        dan tambahkan token pada
              ada di `requirements.txt`               mengirim permintaan     seluruh form yang mengubah
                                                      POST tanpa persetujuan  data; uji semua route POST
                                                      pengguna                

  8           Model dan tabel `LogStok` ada, tetapi   Riwayat perubahan stok  Catat perubahan stok saat
              tidak ditemukan route yang menulis      tidak terisi meski      tambah/edit/hapus/koreksi,
              catatan ke tabel ini                    dokumentasi lama        atau hapus tabel dan klaim
                                                      menyiratkan stok        fiturnya jika memang tidak
                                                      dicatat                 digunakan

  9           Pengurangan stok di                     Dua transaksi bersamaan Gunakan penguncian baris
              `setujui_pengajuan()` dan               berisiko membaca stok   yang sesuai dukungan
              `pinjam_buku()` membaca lalu mengubah   yang sama dan           database
              stok tanpa penguncian baris/operasi     menghasilkan hitungan   (`SELECT ... FOR UPDATE`)
              atomik                                  yang keliru             atau `UPDATE` atomik dengan
                                                                              syarat stok masih `> 0`;
                                                                              tangani hasil update dan
                                                                              transaksi secara benar

  10          Tidak ditemukan pembatasan percobaan    Percobaan password      Terapkan rate limiting,
              login pada kode yang diperiksa          berulang dapat          pencatatan login gagal, dan
                                                      meningkatkan risiko     kebijakan penundaan/blokir
                                                      brute force             yang proporsional

  11          Font Inter dan Chart.js dimuat dari CDN Tanpa internet, font    Jika lingkungan harus
              eksternal                               khusus tidak tersedia   mendukung mode offline,
                                                      dan grafik dashboard    simpan dependensi yang
                                                      tidak dimuat            sesuai secara lokal di
                                                                              `static/` dan perbarui
                                                                              referensi template

  12          `ekspor_denda()` tidak mengekspor       Alasan pembebasan tidak Tambahkan kolom catatan jika
              `catatan_denda` dan tidak menyertakan   terlihat di Excel;      dibutuhkan. Jika ingin
              kategori denda berjalan                 denda yang masih        ekspor denda berjalan, buat
                                                      berjalan tidak muncul   alur terpisah yang
                                                      dalam ekspor ini        menghitung nilai real-time
                                                                              tanpa menganggapnya sebagai
                                                                              nilai denda tersimpan
  --------------------------------------------------------------------------------------------------------

## LAMPIRAN B --- Glosarium

  ---------------------------------------------------------------------
  Istilah                            Arti singkat
  ---------------------------------- ----------------------------------
  Blueprint                          Kumpulan route Flask per fitur

  Route                              Pemetaan URL ke fungsi Python

  ORM                                Menulis tabel database sebagai
                                     class Python

  Model                              Class yang mewakili satu tabel

  Query                              Perintah mengambil/mengubah data
                                     di database

  Session                            Data login sementara per pengguna
                                     (disimpan di cookie bertanda
                                     tangan)

  Hash                               Hasil pengacakan satu arah untuk
                                     menyimpan password

  Decorator                          Pembungkus fungsi, mis.
                                     `@login_required`

  Jinja2                             Mesin template HTML dengan sintaks
                                     `{{ }}` dan `{% %}`

  Context processor                  Variabel yang otomatis tersedia di
                                     semua template

  Flash                              Pesan sekali tampil setelah aksi

  Redirect                           Mengarahkan browser ke URL lain

  Foreign key                        Kolom penghubung ke tabel lain

  CASCADE                            Data turunan ikut terhapus saat
                                     induknya dihapus

  ENUM                               Kolom yang hanya boleh berisi
                                     nilai dari daftar tetap

  Index                              Struktur pencepat pencarian di
                                     database

  `.env`                             File rahasia/konfigurasi
                                     lingkungan

  venv                               Lingkungan Python terisolasi per
                                     proyek

  CRUD                               Create, Read, Update, Delete

  NIM                                Nomor Induk Mahasiswa, juga ID
                                     kartu anggota

  CSRF                               Serangan yang membuat browser
                                     pengguna yang sedang login
                                     mengirim permintaan tanpa disadari

  SVG sprite                         Kumpulan ikon SVG dalam satu
                                     dokumen yang dapat dipakai ulang
                                     lewat `<use href="#id">`

  `data-theme`                       Atribut HTML yang dipakai CSS
                                     untuk memilih tema terang atau
                                     gelap

  Penguncian baris (`FOR UPDATE`)    Mekanisme database untuk mengunci
                                     baris selama transaksi agar tidak
                                     diproses secara bersamaan oleh
                                     transaksi lain

  CDN                                Server eksternal untuk menyajikan
                                     library atau aset, misalnya
                                     Chart.js

  Rate limiting                      Pembatasan jumlah permintaan dalam
                                     jangka waktu tertentu, misalnya
                                     percobaan login
  ---------------------------------------------------------------------

------------------------------------------------------------------------

# BAGIAN VI — PENJELASAN FUNGSI SECARA MENYELURUH

Bagian ini **bukan penjelasan arti setiap baris secara terpisah**. Setiap fungsi dibahas sebagai satu unit: tujuan, input, alur proses, percabangan, pemanggilan fungsi lain, keluaran, efek samping, dan cara mengujinya. Ringkasan alur otomatis dibentuk dari struktur kode; untuk memastikan detail implementasi, lihat listing sumber lengkap di Lampiran C.

> **Catatan membaca:** ringkasan otomatis adalah peta untuk memahami kode, bukan pengganti pembacaan kode. Pada fungsi yang sangat panjang, beberapa ekspresi diringkas agar alur utamanya terbaca. Nama variabel, kondisi, dan pemanggilan di bawah ini diturunkan dari sumber proyek.

## Berkas `Website/app.py`

Berkas inti membuat aplikasi Flask, menghubungkan ekstensi, mendaftarkan blueprint, dan menyiapkan filter/handler bila didefinisikan.

### `create_app` — `Website/app.py:9–93`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `app = Flask(__name__)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pemanggilan**: `app.config.from_object(Config)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `db.init_app(app)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `login_manager.init_app(app)` — meminta fungsi/metode lain melakukan tugasnya.

- **Percabangan `if not os.path.isabs(app.config['UPLOAD_FOLDER'])`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pemanggilan**: `os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pernyataan**: `from utils.pengaturan import terapkan_pengaturan`.

- **Pernyataan**: `from utils.denda import denda_peminjaman, format_rupiah`.

- **Pernyataan**: `from flask import request`.

- **Pernyataan**: `@app.before_request
def muat_pengaturan():
    if request.endpoint != 'static':
        terapkan_pengaturan(app)`.

- **Penyimpanan nilai**: `app.jinja_env.filters['rupiah'] = format_rupiah` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `app.jinja_env.globals['denda_sekarang'] = denda_peminjaman` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pernyataan**: `@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))`.

- **Pernyataan**: `@app.context_processor
def inject_jumlah_pending_akun():
    from flask_login import current_user
    if current_user.is_authenticated and current_user.is_kepala:
        jumlah...`.

- **Pernyataan**: `@app.context_processor
def inject_jumlah_pengajuan_peminjaman():
    from flask_login import current_user
    from models import Peminjaman
    if current_user.is_authenticated ...`.

- **Pernyataan**: `@app.context_processor
def inject_tahun_sekarang():
    return {'tahun_sekarang': date.today().year}`.

- **Pernyataan**: `from routes.auth import auth_bp`.

- **Pernyataan**: `from routes.dashboard import dashboard_bp`.

- **Pernyataan**: `from routes.buku import buku_bp`.

- **Pernyataan**: `from routes.peminjaman import peminjaman_bp`.

- **Pernyataan**: `from routes.laporan import laporan_bp`.

- **Pernyataan**: `from routes.kartu import kartu_bp`.

- **Pernyataan**: `from routes.denda import denda_bp`.

- **Pernyataan**: `from routes.pengaturan import pengaturan_bp`.

- **Pemanggilan**: `app.register_blueprint(auth_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `app.register_blueprint(dashboard_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `app.register_blueprint(buku_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `app.register_blueprint(peminjaman_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `app.register_blueprint(laporan_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `app.register_blueprint(kartu_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `app.register_blueprint(denda_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `app.register_blueprint(pengaturan_bp)` — meminta fungsi/metode lain melakukan tugasnya.

- **`return app`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Flask`, `app.config.from_object`, `db.init_app`, `login_manager.init_app`, `os.makedirs`, `app.register_blueprint`, `os.path.isabs`, `os.path.join`, `User.query.get`, `terapkan_pengaturan`, `int`, `User.query.filter_by(role='mahasiswa', status_akun='pending').count`, `Peminjaman.query.filter_by(status='diajukan').count`, `date.today`, `User.query.filter_by`, `Peminjaman.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `app`, `User.query.get(int(user_id))`, `{'jumlah_pending_akun': jumlah}`, `{'jumlah_pengajuan_peminjaman': jumlah}`, `{'tahun_sekarang': date.today().year}`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `create_app.muat_pengaturan` — `Website/app.py:32–35`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.endpoint != 'static'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Pemanggilan**: `terapkan_pengaturan(app)` — meminta fungsi/metode lain melakukan tugasnya.

**Fungsi/metode yang dipanggil.** `terapkan_pengaturan`.

**Keluaran.** Tidak ada `return` eksplisit; pemanggil menerima `None` kecuali ada perilaku khusus dari framework/dekorator.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `create_app.load_user` — `Website/app.py:41–42`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return User.query.get(int(user_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `User.query.get`, `int`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `User.query.get(int(user_id))`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `create_app.inject_jumlah_pending_akun` — `Website/app.py:45–54`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Pernyataan**: `from flask_login import current_user`.

- **Percabangan `if current_user.is_authenticated and current_user.is_kepala`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

  - **Penyimpanan nilai**: `jumlah = User.query.filter_by(role='mahasiswa', status_akun='pending').count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  **Alternatif (`else`/`elif`):**

  - **Penyimpanan nilai**: `jumlah = 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return {'jumlah_pending_akun': jumlah}`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `User.query.filter_by(role='mahasiswa', status_akun='pending').count`, `User.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `{'jumlah_pending_akun': jumlah}`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `create_app.inject_jumlah_pengajuan_peminjaman` — `Website/app.py:57–66`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Pernyataan**: `from flask_login import current_user`.

- **Pernyataan**: `from models import Peminjaman`.

- **Percabangan `if current_user.is_authenticated and (current_user.is_staf or current_user.is_kepala)`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

  - **Penyimpanan nilai**: `jumlah = Peminjaman.query.filter_by(status='diajukan').count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  **Alternatif (`else`/`elif`):**

  - **Penyimpanan nilai**: `jumlah = 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return {'jumlah_pengajuan_peminjaman': jumlah}`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Peminjaman.query.filter_by(status='diajukan').count`, `Peminjaman.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `{'jumlah_pengajuan_peminjaman': jumlah}`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `create_app.inject_tahun_sekarang` — `Website/app.py:69–72`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return {'tahun_sekarang': date.today().year}`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `{'tahun_sekarang': date.today().year}`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/models.py`

Berkas model mendefinisikan struktur data ORM, relasi, serta metode yang beroperasi pada satu entitas.

### `User.set_password` — `Website/models.py:55–56`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `password`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `self.password_hash = generate_password_hash(password)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

**Fungsi/metode yang dipanggil.** `generate_password_hash`.

**Keluaran.** Tidak ada `return` eksplisit; pemanggil menerima `None` kecuali ada perilaku khusus dari framework/dekorator.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.check_password` — `Website/models.py:58–59`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `password`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return check_password_hash(self.password_hash, password)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `check_password_hash`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `check_password_hash(self.password_hash, password)`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.is_kepala` — `Website/models.py:63–64`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.role == 'kepala_perpustakaan'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.role == 'kepala_perpustakaan'`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.is_staf` — `Website/models.py:67–68`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.role == 'staf'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.role == 'staf'`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.is_mahasiswa` — `Website/models.py:71–72`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.role == 'mahasiswa'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.role == 'mahasiswa'`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.role_label` — `Website/models.py:75–76`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return ROLE_LABEL.get(self.role, self.role)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `ROLE_LABEL.get`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `ROLE_LABEL.get(self.role, self.role)`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.jumlah_pinjaman_aktif` — `Website/models.py:80–85`

**Docstring sumber:** Jumlah buku yang sedang diajukan atau dipinjam (belum dikembalikan).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return Peminjaman.query.filter(Peminjaman.user_id == self.id, Peminjaman.status.in_(STATUS_PINJAMAN_AKTIF)).count()`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Peminjaman.query.filter(Peminjaman.user_id == self.id, Peminjaman.status.in_(STATUS_PINJAMAN_AKTIF)).count`, `Peminjaman.query.filter`, `Peminjaman.status.in_`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `Peminjaman.query.filter(Peminjaman.user_id == self.id, Peminjaman.status.in_(STATUS_PINJAMAN_AKTIF)).count()`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.menunggu_persetujuan` — `Website/models.py:89–90`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.status_akun == 'pending'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.status_akun == 'pending'`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `User.ditolak_operator` — `Website/models.py:93–94`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.status_akun == 'ditolak'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.status_akun == 'ditolak'`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `KartuAnggota.nim` — `Website/models.py:107–109`

**Docstring sumber:** ID kartu = NIM pemilik kartu (satu sumber data: users.nim).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.pemilik.nim`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.pemilik.nim`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `KartuAnggota.is_kadaluarsa` — `Website/models.py:112–113`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return date.today() > self.tanggal_kadaluarsa`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `date.today() > self.tanggal_kadaluarsa`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `KartuAnggota.bisa_dipakai` — `Website/models.py:116–118`

**Docstring sumber:** Kartu boleh dipakai meminjam jika berstatus aktif & belum kadaluarsa.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.status == 'aktif' and (not self.is_kadaluarsa)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.status == 'aktif' and (not self.is_kadaluarsa)`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `Buku.total_dipinjam` — `Website/models.py:153–154`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return sum((1 for p in self.peminjaman_list))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `sum`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `sum((1 for p in self.peminjaman_list))`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `Peminjaman.hari_telat` — `Website/models.py:199–207`

**Docstring sumber:** Jumlah hari melewati jatuh tempo (0 jika belum/tidak telat).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if self.status == 'dikembalikan' and self.tanggal_kembali`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

  - **Penyimpanan nilai**: `akhir = self.tanggal_kembali` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  **Alternatif (`else`/`elif`):**

  - **Percabangan `if self.status == 'dipinjam'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

    - **Penyimpanan nilai**: `akhir = date.today()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    **Alternatif (`else`/`elif`):**

    - **`return 0`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return max(0, (akhir - self.tanggal_jatuh_tempo).days)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `max`, `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `max(0, (akhir - self.tanggal_jatuh_tempo).days)`, `0`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `Peminjaman.is_telat` — `Website/models.py:210–215`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if self.status in ('dikembalikan', 'diajukan', 'ditolak')`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Percabangan `if self.status == 'dikembalikan'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **`return self.tanggal_kembali and self.tanggal_kembali > self.tanggal_jatuh_tempo`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **`return False`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return date.today() > self.tanggal_jatuh_tempo`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `date.today() > self.tanggal_jatuh_tempo`, `False`, `self.tanggal_kembali and self.tanggal_kembali > self.tanggal_jatuh_tempo`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `Peminjaman.is_diajukan` — `Website/models.py:218–219`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return self.status == 'diajukan'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `self.status == 'diajukan'`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `Peminjaman.hari_menuju_jatuh_tempo` — `Website/models.py:222–227`

**Docstring sumber:** Jumlah hari tersisa menuju jatuh tempo (negatif jika sudah lewat).
Hanya relevan untuk peminjaman yang sedang berjalan ('dipinjam').

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if self.status != 'dipinjam'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return None`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return (self.tanggal_jatuh_tempo - date.today()).days`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(self.tanggal_jatuh_tempo - date.today()).days`, `None`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/auth.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `_email_domain_valid` — `Website/routes/auth.py:14–20`

**Docstring sumber:** Cek domain email terhadap Config.ALLOWED_EMAIL_DOMAINS.
(Sebelumnya daftar ini ada di config.py tapi tidak pernah dipakai/divalidasi.)

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `email`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Pernyataan**: `from flask import current_app`.

- **Penyimpanan nilai**: `domain = email.rsplit('@', 1)[-1].lower() if '@' in email else ''` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `allowed = current_app.config.get('ALLOWED_EMAIL_DOMAINS') or []` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return domain in allowed`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `email.rsplit('@', 1)[-1].lower`, `current_app.config.get`, `email.rsplit`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `domain in allowed`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `register` — `Website/routes/auth.py:24–90`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 20 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `username = request.form.get('username', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `email = request.form.get('email', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `nama_lengkap = request.form.get('nama_lengkap', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `nim_input = request.form.get('nim', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password = request.form.get('password', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password2 = request.form.get('password2', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not all([username, email, nama_lengkap, password])`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Semua field wajib diisi.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.register'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if password != password2`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Konfirmasi password tidak cocok.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.register'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if len(password) < 6`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Password minimal 6 karakter.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.register'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if not _email_domain_valid(email)`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Domain email tidak diizinkan. Gunakan email pribadi yang umum (gmail, yahoo, outlook, dsb).', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.register'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `(nim, err) = validasi_nim(nim_input, wajib=True)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if err`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(err, 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.register'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if User.query.filter_by(username=username).first()`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Username sudah digunakan.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.register'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if User.query.filter_by(email=email).first()`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Email sudah terdaftar.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.register'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `user = User(username=username, email=email, nama_lengkap=nama_lengkap, nim=nim, role='mahasiswa', status_akun='pending')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Pemanggilan**: `user.set_password(password)` — meminta fungsi/metode lain melakukan tugasnya.

  - **Efek/prosedur**: `db.session.add(user)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `flash('Registrasi berhasil! Akun Anda akan aktif setelah disetujui oleh kepala perpustakaan. Silakan cek kembali nanti.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.login'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return render_template('auth/register.html')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `render_template`, `request.form.get('username', '').strip`, `request.form.get('email', '').strip`, `request.form.get('nama_lengkap', '').strip`, `request.form.get`, `validasi_nim`, `User.query.filter_by(username=username).first`, `User.query.filter_by(email=email).first`, `User`, `user.set_password`, `db.session.add`, `db.session.commit`, `flash`, `redirect`, `all`, `len`, `_email_domain_valid`, `url_for`, `User.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('auth/register.html')`, `redirect(url_for('auth.login'))`, `redirect(url_for('auth.register'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `login` — `Website/routes/auth.py:94–130`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if current_user.is_authenticated`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return redirect(url_for('dashboard.index'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 6 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `username = request.form.get('username', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password = request.form.get('password', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `user = User.query.filter_by(username=username).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if user is None and username`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **Penyimpanan nilai**: `user = User.query.filter_by(nim=username).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if user and user.check_password(password)`**: bila kondisi benar, jalankan 6 pernyataan di cabang utama.

    - **Percabangan `if user.menunggu_persetujuan`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Akun Anda masih menunggu persetujuan kepala perpustakaan. Silakan coba login lagi nanti.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.login'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

    - **Percabangan `if user.ditolak_operator`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Registrasi akun Anda ditolak oleh kepala perpustakaan. Hubungi kepala perpustakaan untuk informasi lebih lanjut.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.login'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

    - **Percabangan `if not user.is_active_db`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Akun Anda dinonaktifkan. Hubungi kepala perpustakaan.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.login'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

    - **Efek/prosedur**: `login_user(user)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **Efek/prosedur**: `flash(f'Selamat datang, {user.nama_lengkap}!', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('dashboard.index'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Efek/prosedur**: `flash('Username/NIM atau password salah.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return render_template('auth/login.html')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `render_template`, `redirect`, `request.form.get('username', '').strip`, `request.form.get`, `User.query.filter_by(username=username).first`, `flash`, `url_for`, `User.query.filter_by(nim=username).first`, `user.check_password`, `login_user`, `User.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('auth/login.html')`, `redirect(url_for('dashboard.index'))`, `redirect(url_for('auth.login'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `logout` — `Website/routes/auth.py:135–138`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Efek/prosedur**: `logout_user()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash('Anda telah logout.', 'info')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('auth.login'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `logout_user`, `flash`, `redirect`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('auth.login'))`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `daftar_pengguna` — `Website/routes/auth.py:147–149`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `pengguna = User.query.order_by(User.created_at.desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('auth/daftar_pengguna.html', pengguna=pengguna)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `User.query.order_by(User.created_at.desc()).all`, `render_template`, `User.query.order_by`, `User.created_at.desc`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('auth/daftar_pengguna.html', pengguna=pengguna)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `tambah_pengguna` — `Website/routes/auth.py:155–217`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 22 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `username = request.form.get('username', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `email = request.form.get('email', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `nama_lengkap = request.form.get('nama_lengkap', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password = request.form.get('password', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `role = request.form.get('role', 'staf')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `nim_input = request.form.get('nim', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if role not in ('mahasiswa', 'staf', 'kepala_perpustakaan')`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Role tidak valid.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.tambah_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if len(password) < 6`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Password minimal 6 karakter.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.tambah_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `(nim, err) = validasi_nim(nim_input, wajib=role == 'mahasiswa')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if err`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(err, 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.tambah_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if not _email_domain_valid(email)`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Domain email tidak diizinkan. Gunakan email pribadi yang umum (gmail, yahoo, outlook, dsb).', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.tambah_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if User.query.filter_by(username=username).first()`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Username sudah digunakan.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.tambah_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if User.query.filter_by(email=email).first()`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Email sudah digunakan pengguna lain.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.tambah_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `user = User(username=username, email=email, nama_lengkap=nama_lengkap, nim=nim, role=role, status_akun='disetujui')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Pemanggilan**: `user.set_password(password)` — meminta fungsi/metode lain melakukan tugasnya.

  - **Efek/prosedur**: `db.session.add(user)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `db.session.flush()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Penyimpanan nilai**: `kartu = KartuAnggota(user_id=user.id, tanggal_terbit=date.today(), tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config['MASA_BERLAKU_KARTU_HARI']), status='aktif')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `db.session.add(kartu)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `flash(f"Pengguna '{username}' ({role}) berhasil dibuat.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return render_template('auth/tambah_pengguna.html')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `render_template`, `request.form.get('username', '').strip`, `request.form.get('email', '').strip`, `request.form.get('nama_lengkap', '').strip`, `request.form.get`, `validasi_nim`, `User.query.filter_by(username=username).first`, `User.query.filter_by(email=email).first`, `User`, `user.set_password`, `db.session.add`, `db.session.flush`, `KartuAnggota`, `db.session.commit`, `flash`, `redirect`, `len`, `_email_domain_valid` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('auth/tambah_pengguna.html')`, `redirect(url_for('auth.daftar_pengguna'))`, `redirect(url_for('auth.tambah_pengguna'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `toggle_aktif_pengguna` — `Website/routes/auth.py:223–232`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `user = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if user.id == current_user.id`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Anda tidak bisa menonaktifkan akun sendiri.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `user.is_active_db = not user.is_active_db` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Penyimpanan nilai**: `status = 'diaktifkan' if user.is_active_db else 'dinonaktifkan'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `flash(f"Akun '{user.username}' berhasil {status}.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `User.query.get_or_404`, `db.session.commit`, `flash`, `redirect`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('auth.daftar_pengguna'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `edit_pengguna` — `Website/routes/auth.py:238–321`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if user_id == current_user.id`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash("Gunakan halaman 'Profil Saya' untuk mengedit akun Anda sendiri.", 'info')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.profil'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `user = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 31 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `username = request.form.get('username', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `email = request.form.get('email', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `nama_lengkap = request.form.get('nama_lengkap', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `no_telepon = request.form.get('no_telepon', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `alamat = request.form.get('alamat', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `role = request.form.get('role', user.role)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `nim_input = request.form.get('nim', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password_baru = request.form.get('password', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password_baru2 = request.form.get('password2', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not all([username, email, nama_lengkap])`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Nama, username, dan email wajib diisi.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if password_baru or password_baru2`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Percabangan `if len(password_baru) < 6`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Password baru minimal 6 karakter.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

    - **Percabangan `if password_baru != password_baru2`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Konfirmasi password baru tidak cocok.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if role not in ('mahasiswa', 'staf', 'kepala_perpustakaan')`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Role tidak valid.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `(nim, err) = validasi_nim(nim_input, wajib=role == 'mahasiswa', abaikan_user_id=user.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if err`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(err, 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `duplikat_username = User.query.filter(User.username == username, User.id != user.id).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if duplikat_username`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Username sudah digunakan pengguna lain.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `duplikat_email = User.query.filter(User.email == email, User.id != user.id).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if duplikat_email`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Email sudah digunakan pengguna lain.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if user.is_kepala and role != 'kepala_perpustakaan'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Penyimpanan nilai**: `jumlah_kepala = User.query.filter_by(role='kepala_perpustakaan').count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Percabangan `if jumlah_kepala <= 1`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Tidak bisa mengubah role: ini adalah satu-satunya akun kepala perpustakaan yang tersisa.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.edit_pengguna', user_id=user.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `user.username = username` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `user.email = email` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `user.nama_lengkap = nama_lengkap` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `user.no_telepon = no_telepon or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `user.alamat = alamat or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `user.nim = nim` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `user.role = role` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if password_baru`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **Pemanggilan**: `user.set_password(password_baru)` — meminta fungsi/metode lain melakukan tugasnya.

  - **Pemanggilan**: `_terbitkan_kartu_jika_belum_ada(user)` — meminta fungsi/metode lain melakukan tugasnya.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Percabangan `if password_baru`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

    - **Efek/prosedur**: `flash(f"Akun '{user.username}' berhasil diperbarui dan password-nya sudah direset.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    **Alternatif (`else`/`elif`):**

    - **Efek/prosedur**: `flash(f"Akun '{user.username}' berhasil diperbarui.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return render_template('auth/edit_pengguna.html', u=user)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `User.query.get_or_404`, `render_template`, `flash`, `redirect`, `request.form.get('username', '').strip`, `request.form.get('email', '').strip`, `request.form.get('nama_lengkap', '').strip`, `request.form.get('no_telepon', '').strip`, `request.form.get('alamat', '').strip`, `request.form.get`, `validasi_nim`, `User.query.filter(User.username == username, User.id != user.id).first`, `User.query.filter(User.email == email, User.id != user.id).first`, `_terbitkan_kartu_jika_belum_ada`, `db.session.commit`, `url_for`, `all`, `User.query.filter_by(role='kepala_perpustakaan').count` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('auth/edit_pengguna.html', u=user)`, `redirect(url_for('auth.profil'))`, `redirect(url_for('auth.daftar_pengguna'))`, `redirect(url_for('auth.edit_pengguna', user_id=user.id))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `hapus_pengguna` — `Website/routes/auth.py:327–364`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `user = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if user.id == current_user.id`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Anda tidak bisa menghapus akun sendiri.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if user.is_kepala`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `jumlah_kepala = User.query.filter_by(role='kepala_perpustakaan').count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if jumlah_kepala <= 1`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Tidak bisa menghapus: ini adalah satu-satunya akun kepala perpustakaan yang tersisa.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `ada_aktif = Peminjaman.query.filter(Peminjaman.user_id == user.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if ada_aktif`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash(f"Tidak bisa menghapus '{user.username}': masih ada pengajuan/peminjaman aktif. Selesaikan (kembalikan/tolak) dulu, atau nonaktifkan saja akunnya.", 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `username = user.username` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `riwayat_lama = Peminjaman.query.filter_by(user_id=user.id).count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.delete(user)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Penyimpanan nilai**: `pesan = f"Akun '{username}' berhasil dihapus."` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if riwayat_lama`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Pernyataan**: `pesan += f' ({riwayat_lama} riwayat peminjaman lama miliknya ikut terhapus.)'`.

- **Efek/prosedur**: `flash(pesan, 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('auth.daftar_pengguna'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `User.query.get_or_404`, `Peminjaman.query.filter(Peminjaman.user_id == user.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first`, `Peminjaman.query.filter_by(user_id=user.id).count`, `db.session.delete`, `db.session.commit`, `flash`, `redirect`, `User.query.filter_by(role='kepala_perpustakaan').count`, `url_for`, `Peminjaman.query.filter`, `Peminjaman.query.filter_by`, `User.query.filter_by`, `Peminjaman.status.in_`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('auth.daftar_pengguna'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `profil` — `Website/routes/auth.py:375–420`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 19 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `email = request.form.get('email', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `nama_lengkap = request.form.get('nama_lengkap', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `no_telepon = request.form.get('no_telepon', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `alamat = request.form.get('alamat', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password_lama = request.form.get('password_lama', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password_baru = request.form.get('password_baru', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `password_baru2 = request.form.get('password_baru2', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not all([email, nama_lengkap])`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Nama dan email wajib diisi.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.profil'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `duplikat_email = User.query.filter(User.email == email, User.id != current_user.id).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if duplikat_email`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Email sudah digunakan pengguna lain.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('auth.profil'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if password_baru or password_baru2 or (password_lama and (not current_user.is_kepala))`**: bila kondisi benar, jalankan 4 pernyataan di cabang utama.

    - **Percabangan `if not current_user.is_kepala and (not current_user.check_password(password_lama))`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Password lama yang dimasukkan salah.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.profil'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

    - **Percabangan `if password_baru != password_baru2`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Konfirmasi password baru tidak cocok.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.profil'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

    - **Percabangan `if len(password_baru) < 6`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Efek/prosedur**: `flash('Password baru minimal 6 karakter.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      - **`return redirect(url_for('auth.profil'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

    - **Pemanggilan**: `current_user.set_password(password_baru)` — meminta fungsi/metode lain melakukan tugasnya.

  - **Penyimpanan nilai**: `current_user.email = email` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `current_user.nama_lengkap = nama_lengkap` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `current_user.no_telepon = no_telepon or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `current_user.alamat = alamat or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Pemanggilan**: `_terbitkan_kartu_jika_belum_ada(current_user)` — meminta fungsi/metode lain melakukan tugasnya.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `flash('Profil berhasil diperbarui.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.profil'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return render_template('auth/profil.html')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `render_template`, `request.form.get('email', '').strip`, `request.form.get('nama_lengkap', '').strip`, `request.form.get('no_telepon', '').strip`, `request.form.get('alamat', '').strip`, `request.form.get`, `User.query.filter(User.email == email, User.id != current_user.id).first`, `_terbitkan_kartu_jika_belum_ada`, `db.session.commit`, `flash`, `redirect`, `all`, `current_user.set_password`, `url_for`, `User.query.filter`, `len`, `current_user.check_password`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('auth/profil.html')`, `redirect(url_for('auth.profil'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `daftar_persetujuan` — `Website/routes/auth.py:431–437`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `pending = User.query.filter_by(role='mahasiswa', status_akun='pending').order_by(User.created_at.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('auth/persetujuan.html', pending=pending)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `User.query.filter_by(role='mahasiswa', status_akun='pending').order_by(User.created_at.asc()).all`, `render_template`, `User.query.filter_by(role='mahasiswa', status_akun='pending').order_by`, `User.created_at.asc`, `User.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('auth/persetujuan.html', pending=pending)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `setujui_pengguna` — `Website/routes/auth.py:443–465`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `user = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if user.status_akun != 'pending'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Akun ini sudah pernah diproses sebelumnya.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.daftar_persetujuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `user.status_akun = 'disetujui'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if not user.kartu`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `kartu = KartuAnggota(user_id=user.id, tanggal_terbit=date.today(), tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config['MASA_BERLAKU_KARTU_HARI']), status='aktif')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `db.session.add(kartu)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Akun '{user.username}' disetujui dan kartu anggota diterbitkan.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('auth.daftar_persetujuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `User.query.get_or_404`, `db.session.commit`, `flash`, `redirect`, `KartuAnggota`, `db.session.add`, `url_for`, `date.today`, `timedelta`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('auth.daftar_persetujuan'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `tolak_pengguna` — `Website/routes/auth.py:471–482`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `user = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if user.status_akun != 'pending'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Akun ini sudah pernah diproses sebelumnya.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('auth.daftar_persetujuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `user.status_akun = 'ditolak'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `user.is_active_db = False` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Registrasi '{user.username}' ditolak.", 'info')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('auth.daftar_persetujuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `auth_bp.route`, `role_required`, `User.query.get_or_404`, `db.session.commit`, `flash`, `redirect`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('auth.daftar_persetujuan'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/buku.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `_allowed_image` — `Website/routes/buku.py:20–22`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `filename`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return ext in current_app.config['ALLOWED_IMAGE_EXT']`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `filename.rsplit('.', 1)[-1].lower`, `filename.rsplit`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `ext in current_app.config['ALLOWED_IMAGE_EXT']`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_simpan_sampul` — `Website/routes/buku.py:25–43`

**Docstring sumber:** Simpan file gambar ke folder upload, kembalikan path relatif terhadap
folder 'static/' (selalu pakai forward-slash, aman di Windows/Linux/Mac).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `file_storage`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if not file_storage or file_storage.filename == ''`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return None`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if not _allowed_image(file_storage.filename)`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Format gambar tidak didukung (gunakan png/jpg/jpeg/webp).', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return None`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `ext = file_storage.filename.rsplit('.', 1)[-1].lower()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `nama_unik = f'{uuid.uuid4().hex}.{ext}'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `nama_aman = secure_filename(nama_unik)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `path_lengkap = os.path.join(current_app.config['UPLOAD_FOLDER'], nama_aman)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pemanggilan**: `file_storage.save(path_lengkap)` — meminta fungsi/metode lain melakukan tugasnya.

- **`return f'uploads/sampul/{nama_aman}'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `file_storage.filename.rsplit('.', 1)[-1].lower`, `secure_filename`, `os.path.join`, `file_storage.save`, `_allowed_image`, `flash`, `file_storage.filename.rsplit`, `uuid.uuid4`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `f'uploads/sampul/{nama_aman}'`, `None`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web, membaca/menulis berkas. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_isbn_duplikat` — `Website/routes/buku.py:46–52`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `isbn`, `kecuali_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if not isbn`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return None`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `q = Buku.query.filter(Buku.isbn == isbn)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if kecuali_id`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `q = q.filter(Buku.id != kecuali_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return q.first()`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Buku.query.filter`, `q.first`, `q.filter`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `q.first()`, `None`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_lama_pinjam_form` — `Website/routes/buku.py:55–58`

**Docstring sumber:** Lama pinjam khusus buku (opsional): kosong = ikut pengaturan umum.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `nilai = request.form.get('lama_pinjam_hari', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return nilai if nilai and 1 <= nilai <= 365 else None`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `request.form.get`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `nilai if nilai and 1 <= nilai <= 365 else None`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `daftar_buku` — `Website/routes/buku.py:66–112`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `q = request.args.get('q', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kategori_id = request.args.get('kategori_id', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `query = Buku.query` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `like = f'%{q}%'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `query = query.filter(db.or_(Buku.judul.ilike(like), Buku.penulis.ilike(like), Buku.isbn.ilike(like)))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if kategori_id`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `query = query.filter(Buku.kategori_id == kategori_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `daftar = query.order_by(Buku.judul.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `buku_id_aktif = set()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `maks_pinjam = current_app.config['MAKS_PINJAM_PER_USER']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `jumlah_aktif = 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if current_user.is_mahasiswa`**: bila kondisi benar, jalankan 3 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `aktif = Peminjaman.query.filter(Peminjaman.user_id == current_user.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku_id_aktif = {p.buku_id for p in aktif}` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `jumlah_aktif = len(aktif)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kuota_penuh = jumlah_aktif >= maks_pinjam` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kelompok = OrderedDict()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Perulangan** (`kat melalui kategori_list`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `buku_kat = [b for b in daftar if b.kategori_id == kat.id]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if buku_kat`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **Penyimpanan nilai**: `kelompok[kat.nama_kategori] = buku_kat` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `tanpa_kategori = [b for b in daftar if not b.kategori_id]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if tanpa_kategori`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `kelompok['Tanpa Kategori'] = tanpa_kategori` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('buku/daftar.html', daftar=daftar, kelompok=kelompok, kategori_list=kategori_list, q=q, kategori_id=kategori_id, buku_id_aktif=buku_id_aktif, kuota_penuh=kuota_penuh, jumlah_aktif=jumlah_aktif, maks_pinjam=maks_pinjam)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `request.args.get('q', '').strip`, `request.args.get`, `query.order_by(Buku.judul.asc()).all`, `Kategori.query.order_by(Kategori.nama_kategori).all`, `set`, `OrderedDict`, `render_template`, `query.filter`, `Peminjaman.query.filter(Peminjaman.user_id == current_user.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).all`, `len`, `db.or_`, `query.order_by`, `Kategori.query.order_by`, `Buku.judul.ilike`, `Buku.penulis.ilike`, `Buku.isbn.ilike`, `Buku.judul.asc`, `Peminjaman.query.filter`, `Peminjaman.status.in_`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('buku/daftar.html', daftar=daftar, kelompok=kelompok, kategori_list=kategori_list, q=q, kategori_id=kategori_id, buku_id_aktif=buku_id_aktif, kuota_penuh=kuota_penuh, jumlah_aktif=jumlah_aktif, maks_pinjam=maks_pinjam)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `detail_buku` — `Website/routes/buku.py:117–133`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `buku = Buku.query.get_or_404(buku_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `pengajuan_aktif = None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if current_user.is_mahasiswa`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `pengajuan_aktif = Peminjaman.query.filter(Peminjaman.user_id == current_user.id, Peminjaman.buku_id == buku.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `maks_pinjam = current_app.config['MAKS_PINJAM_PER_USER']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `jumlah_aktif = current_user.jumlah_pinjaman_aktif if current_user.is_mahasiswa else 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('buku/detail.html', buku=buku, pengajuan_aktif=pengajuan_aktif, kuota_penuh=jumlah_aktif >= maks_pinjam, jumlah_aktif=jumlah_aktif, maks_pinjam=maks_pinjam)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `Buku.query.get_or_404`, `render_template`, `Peminjaman.query.filter(Peminjaman.user_id == current_user.id, Peminjaman.buku_id == buku.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first`, `Peminjaman.query.filter`, `Peminjaman.status.in_`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('buku/detail.html', buku=buku, pengajuan_aktif=pengajuan_aktif, kuota_penuh=jumlah_aktif >= maks_pinjam, jumlah_aktif=jumlah_aktif, maks_pinjam=maks_pinjam)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `tambah_buku` — `Website/routes/buku.py:142–178`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 18 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `judul = request.form.get('judul', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `penulis = request.form.get('penulis', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `penerbit = request.form.get('penerbit', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `tahun_terbit = request.form.get('tahun_terbit', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `isbn = request.form.get('isbn', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `kategori_id = request.form.get('kategori_id', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `deskripsi = request.form.get('deskripsi', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `stok = max(0, request.form.get('stok', type=int, default=0) or 0)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `lokasi_rak = request.form.get('lokasi_rak', '').strip() or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not judul or not penulis`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Judul dan penulis wajib diisi.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('buku.tambah_buku'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `ada = _isbn_duplikat(isbn)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if ada`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(f"ISBN {isbn} sudah terdaftar untuk buku '{ada.judul}'. Jika ini eksemplar tambahan, tambahkan stok pada buku tersebut.", 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('buku.tambah_buku'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `sampul_path = _simpan_sampul(request.files.get('sampul'))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku = Buku(judul=judul, penulis=penulis, penerbit=penerbit or None, tahun_terbit=tahun_terbit, isbn=isbn or None, kategori_id=kategori_id or None, deskripsi=deskripsi or None, stok=stok, sampul_path=sampul_path, lokasi_rak=lokasi_rak, lama_pinjam_hari=_lama_pinjam_form())` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `db.session.add(buku)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `flash(f"Buku '{judul}' berhasil ditambahkan.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.daftar_buku'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('buku/form.html', buku=None, kategori_list=kategori_list)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `Kategori.query.order_by(Kategori.nama_kategori).all`, `render_template`, `request.form.get('judul', '').strip`, `request.form.get('penulis', '').strip`, `request.form.get('penerbit', '').strip`, `request.form.get`, `request.form.get('isbn', '').strip`, `request.form.get('deskripsi', '').strip`, `max`, `_isbn_duplikat`, `_simpan_sampul`, `Buku`, `db.session.add`, `db.session.commit`, `flash`, `redirect`, `request.form.get('lokasi_rak', '').strip`, `request.files.get` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('buku/form.html', buku=None, kategori_list=kategori_list)`, `redirect(url_for('buku.daftar_buku'))`, `redirect(url_for('buku.tambah_buku'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `edit_buku` — `Website/routes/buku.py:184–214`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `buku = Buku.query.get_or_404(buku_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 18 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `isbn_baru = request.form.get('isbn', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `ada = _isbn_duplikat(isbn_baru, kecuali_id=buku.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if ada`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(f"ISBN {isbn_baru} sudah dipakai buku '{ada.judul}'.", 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('buku.edit_buku', buku_id=buku.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `buku.judul = request.form.get('judul', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.penulis = request.form.get('penulis', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.penerbit = request.form.get('penerbit', '').strip() or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.tahun_terbit = request.form.get('tahun_terbit', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.isbn = request.form.get('isbn', '').strip() or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.kategori_id = request.form.get('kategori_id', type=int) or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.deskripsi = request.form.get('deskripsi', '').strip() or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.stok = max(0, request.form.get('stok', type=int, default=0) or 0)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.lokasi_rak = request.form.get('lokasi_rak', '').strip() or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku.lama_pinjam_hari = _lama_pinjam_form()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `sampul_baru = _simpan_sampul(request.files.get('sampul'))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if sampul_baru`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **Penyimpanan nilai**: `buku.sampul_path = sampul_baru` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `flash(f"Buku '{buku.judul}' berhasil diperbarui.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.daftar_buku'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('buku/form.html', buku=buku, kategori_list=kategori_list)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `Buku.query.get_or_404`, `Kategori.query.order_by(Kategori.nama_kategori).all`, `render_template`, `request.form.get('isbn', '').strip`, `_isbn_duplikat`, `request.form.get('judul', '').strip`, `request.form.get('penulis', '').strip`, `request.form.get`, `max`, `_lama_pinjam_form`, `_simpan_sampul`, `db.session.commit`, `flash`, `redirect`, `request.form.get('penerbit', '').strip`, `request.form.get('deskripsi', '').strip`, `request.form.get('lokasi_rak', '').strip`, `request.files.get` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('buku/form.html', buku=buku, kategori_list=kategori_list)`, `redirect(url_for('buku.daftar_buku'))`, `redirect(url_for('buku.edit_buku', buku_id=buku.id))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `hapus_buku` — `Website/routes/buku.py:220–244`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `buku = Buku.query.get_or_404(buku_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `ada_aktif = Peminjaman.query.filter(Peminjaman.buku_id == buku.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if ada_aktif`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash(f"Tidak bisa menghapus '{buku.judul}': masih ada pengajuan/peminjaman aktif atas buku ini. Selesaikan (kembalikan/tolak) dulu.", 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.daftar_buku'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `judul = buku.judul` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.delete(buku)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Buku '{judul}' berhasil dihapus.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('buku.daftar_buku'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `Buku.query.get_or_404`, `Peminjaman.query.filter(Peminjaman.buku_id == buku.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first`, `db.session.delete`, `db.session.commit`, `flash`, `redirect`, `url_for`, `Peminjaman.query.filter`, `Peminjaman.status.in_`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('buku.daftar_buku'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `ekspor_buku` — `Website/routes/buku.py:250–268`

**Docstring sumber:** Unduh seluruh koleksi buku ke Excel (format kolom sama seperti template import).

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Pernyataan**: `from datetime import date`.

- **Penyimpanan nilai**: `daftar = Buku.query.order_by(Buku.judul).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `baris = [[b.judul, b.penulis, b.penerbit or '', b.tahun_terbit or '', b.isbn or '', b.kategori.nama_kategori if b.kategori else '', b.stok, b.lokasi_rak or '', b.lama_pinjam_hari or ''] for b in daftar]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `buffer = buat_excel('Koleksi Buku', ['Judul', 'Penulis', 'Penerbit', 'Tahun', 'ISBN', 'Kategori', 'Stok', 'Lokasi Rak', 'Lama Pinjam (hari)'], baris)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return send_file(buffer, as_attachment=True, download_name=f'koleksi_buku_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `Buku.query.order_by(Buku.judul).all`, `buat_excel`, `send_file`, `Buku.query.order_by`, `date.today().isoformat`, `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `send_file(buffer, as_attachment=True, download_name=f'koleksi_buku_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `kategori` — `Website/routes/buku.py:277–289`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 3 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `nama = request.form.get('nama_kategori', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if nama and (not Kategori.query.filter_by(nama_kategori=nama).first())`**: bila kondisi benar, jalankan 3 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

    - **Efek/prosedur**: `db.session.add(Kategori(nama_kategori=nama))` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **Efek/prosedur**: `flash(f"Kategori '{nama}' ditambahkan.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    **Alternatif (`else`/`elif`):**

    - **Efek/prosedur**: `flash('Kategori kosong atau sudah ada.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.kategori'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('buku/kategori.html', kategori_list=kategori_list)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `Kategori.query.order_by(Kategori.nama_kategori).all`, `render_template`, `request.form.get('nama_kategori', '').strip`, `redirect`, `db.session.add`, `db.session.commit`, `flash`, `url_for`, `Kategori.query.order_by`, `request.form.get`, `Kategori.query.filter_by(nama_kategori=nama).first`, `Kategori`, `Kategori.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('buku/kategori.html', kategori_list=kategori_list)`, `redirect(url_for('buku.kategori'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `hapus_kategori` — `Website/routes/buku.py:295–311`

**Docstring sumber:** Hapus kategori. Buku di dalamnya TIDAK ikut terhapus: buku tsb menjadi
'Tanpa Kategori' (kategori_id di-set NULL).

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `kategori_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kat = Kategori.query.get_or_404(kategori_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `nama = kat.nama_kategori` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `jumlah_buku = len(kat.buku_list)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Perulangan** (`b melalui list(kat.buku_list)`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `b.kategori_id = None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.delete(kat)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Penyimpanan nilai**: `pesan = f"Kategori '{nama}' berhasil dihapus."` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if jumlah_buku`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Pernyataan**: `pesan += f" {jumlah_buku} buku di dalamnya kini berstatus 'Tanpa Kategori'."`.

- **Efek/prosedur**: `flash(pesan, 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('buku.kategori'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `Kategori.query.get_or_404`, `len`, `list`, `db.session.delete`, `db.session.commit`, `flash`, `redirect`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('buku.kategori'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `download_template_excel` — `Website/routes/buku.py:320–327`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `buffer = buat_template_excel()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return send_file(buffer, as_attachment=True, download_name='template_import_buku.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `buat_template_excel`, `send_file`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `send_file(buffer, as_attachment=True, download_name='template_import_buku.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `import_excel` — `Website/routes/buku.py:333–350`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 7 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `file = request.files.get('file_excel')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not file or file.filename == ''`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Pilih file Excel (.xlsx) terlebih dahulu.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('buku.import_excel'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if not file.filename.lower().endswith('.xlsx')`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('File harus berformat .xlsx', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('buku.import_excel'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `(sukses, errors) = import_buku_dari_excel(file.stream)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `flash(f'{sukses} buku berhasil diimport.', 'success' if sukses else 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Perulangan** (`err melalui errors[:20]`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

    - **Efek/prosedur**: `flash(err, 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.daftar_buku'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return render_template('buku/import_excel.html')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `buku_bp.route`, `role_required`, `render_template`, `request.files.get`, `import_buku_dari_excel`, `flash`, `redirect`, `file.filename.lower().endswith`, `url_for`, `file.filename.lower`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('buku/import_excel.html')`, `redirect(url_for('buku.daftar_buku'))`, `redirect(url_for('buku.import_excel'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/dashboard.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `_enam_bulan_terakhir` — `Website/routes/dashboard.py:16–27`

**Docstring sumber:** Kembalikan list (tahun, bulan) untuk 6 bulan terakhir, urut menaik, termasuk bulan ini.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `awal_bulan_ini = date.today().replace(day=1)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `hasil = []` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Perulangan** (`mundur melalui range(5, -1, -1)`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `bulan = awal_bulan_ini.month - mundur` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `tahun = awal_bulan_ini.year` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Perulangan** (`bulan <= 0`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

    - **Pernyataan**: `bulan += 12`.

    - **Pernyataan**: `tahun -= 1`.

  - **Pemanggilan**: `hasil.append((tahun, bulan))` — meminta fungsi/metode lain melakukan tugasnya.

- **`return hasil`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `date.today().replace`, `range`, `hasil.append`, `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `hasil`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_data_grafik_peminjaman_bulanan` — `Website/routes/dashboard.py:30–52`

**Docstring sumber:** Jumlah peminjaman per bulan, 6 bulan terakhir (untuk grafik garis/batang).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `bulan_list = _enam_bulan_terakhir()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `(tahun_awal, bulan_awal) = bulan_list[0]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `mulai = date(tahun_awal, bulan_awal, 1)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `baris = db.session.query(func.date_format(Peminjaman.tanggal_pinjam, '%Y-%m').label('bulan_kunci'), func.count(Peminjaman.id)).filter(Peminjaman.tanggal_pinjam >= mulai).group_by('bulan_kunci').all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `peta_jumlah = {kunci: jumlah for kunci, jumlah in baris}` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `(labels, data) = ([], [])` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Perulangan** (`(tahun, bulan) melalui bulan_list`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `kunci = f'{tahun:04d}-{bulan:02d}'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Pemanggilan**: `labels.append(f'{BULAN_ID[bulan - 1]} {tahun}')` — meminta fungsi/metode lain melakukan tugasnya.

  - **Pemanggilan**: `data.append(peta_jumlah.get(kunci, 0))` — meminta fungsi/metode lain melakukan tugasnya.

- **`return (labels, data)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `_enam_bulan_terakhir`, `date`, `db.session.query(func.date_format(Peminjaman.tanggal_pinjam, '%Y-%m').label('bulan_kunci'), func.count(Peminjaman.id)).filter(Peminjaman.tanggal_pinjam >= mulai).group_by('bulan_kunci').all`, `labels.append`, `data.append`, `db.session.query(func.date_format(Peminjaman.tanggal_pinjam, '%Y-%m').label('bulan_kunci'), func.count(Peminjaman.id)).filter(Peminjaman.tanggal_pinjam >= mulai).group_by`, `peta_jumlah.get`, `db.session.query(func.date_format(Peminjaman.tanggal_pinjam, '%Y-%m').label('bulan_kunci'), func.count(Peminjaman.id)).filter`, `db.session.query`, `func.date_format(Peminjaman.tanggal_pinjam, '%Y-%m').label`, `func.count`, `func.date_format`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(labels, data)`.

**Efek samping yang perlu diperhatikan.** mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_data_grafik_buku_terpopuler` — `Website/routes/dashboard.py:55–67`

**Docstring sumber:** Top N buku paling sering dipinjam (untuk grafik batang).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `limit`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `hasil = db.session.query(Buku.judul, func.count(Peminjaman.id).label('jumlah')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by(func.count(Peminjaman.id).desc()).limit(limit).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `labels = [judul for judul, _ in hasil]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `data = [jumlah for _, jumlah in hasil]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return (labels, data)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `db.session.query(Buku.judul, func.count(Peminjaman.id).label('jumlah')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by(func.count(Peminjaman.id).desc()).limit(limit).all`, `db.session.query(Buku.judul, func.count(Peminjaman.id).label('jumlah')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by(func.count(Peminjaman.id).desc()).limit`, `db.session.query(Buku.judul, func.count(Peminjaman.id).label('jumlah')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by`, `func.count(Peminjaman.id).desc`, `db.session.query(Buku.judul, func.count(Peminjaman.id).label('jumlah')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by`, `func.count`, `db.session.query(Buku.judul, func.count(Peminjaman.id).label('jumlah')).join`, `db.session.query`, `func.count(Peminjaman.id).label`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(labels, data)`.

**Efek samping yang perlu diperhatikan.** mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_data_grafik_distribusi_kategori` — `Website/routes/dashboard.py:70–82`

**Docstring sumber:** Jumlah judul buku per kategori (untuk grafik donat).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `hasil = db.session.query(Kategori.nama_kategori, func.count(Buku.id)).outerjoin(Buku, Buku.kategori_id == Kategori.id).group_by(Kategori.id).having(func.count(Buku.id) > 0).order_by(func.count(Buku.id).desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `labels = [nama for nama, _ in hasil]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `data = [jumlah for _, jumlah in hasil]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return (labels, data)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `db.session.query(Kategori.nama_kategori, func.count(Buku.id)).outerjoin(Buku, Buku.kategori_id == Kategori.id).group_by(Kategori.id).having(func.count(Buku.id) > 0).order_by(func.count(Buku.id).desc()).all`, `db.session.query(Kategori.nama_kategori, func.count(Buku.id)).outerjoin(Buku, Buku.kategori_id == Kategori.id).group_by(Kategori.id).having(func.count(Buku.id) > 0).order_by`, `func.count(Buku.id).desc`, `db.session.query(Kategori.nama_kategori, func.count(Buku.id)).outerjoin(Buku, Buku.kategori_id == Kategori.id).group_by(Kategori.id).having`, `func.count`, `db.session.query(Kategori.nama_kategori, func.count(Buku.id)).outerjoin(Buku, Buku.kategori_id == Kategori.id).group_by`, `db.session.query(Kategori.nama_kategori, func.count(Buku.id)).outerjoin`, `db.session.query`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(labels, data)`.

**Efek samping yang perlu diperhatikan.** mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `index` — `Website/routes/dashboard.py:87–187`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `context = {}` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if current_user.is_mahasiswa`**: bila kondisi benar, jalankan 15 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (22 pernyataan).

  - **Penyimpanan nilai**: `pinjaman_aktif = Peminjaman.query.filter_by(user_id=current_user.id, status='dipinjam').all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['pinjaman_aktif'] = pinjaman_aktif` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['jumlah_terlambat_saya'] = sum((1 for p in pinjaman_aktif if p.is_telat))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['denda_berjalan_saya'] = denda_berjalan_semua(current_user.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['denda_belum_lunas_saya'] = total_denda_belum_lunas(current_user.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `batas_peringatan = current_app.config['PERINGATAN_JATUH_TEMPO_HARI']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['akan_jatuh_tempo_saya'] = [p for p in pinjaman_aktif if not p.is_telat and p.hari_menuju_jatuh_tempo is not None and (p.hari_menuju_jatuh_tempo <= batas_peringatan)]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['jumlah_sedang_dipinjam'] = len(pinjaman_aktif)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['jumlah_pernah_dipinjam'] = Peminjaman.query.filter_by(user_id=current_user.id).count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['kartu_saya'] = current_user.kartu` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['maks_pinjam'] = current_app.config['MAKS_PINJAM_PER_USER']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['jumlah_kuota_terpakai'] = current_user.jumlah_pinjaman_aktif` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `buku_id_aktif = {p.buku_id for p in Peminjaman.query.filter(Peminjaman.user_id == current_user.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).all()}` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `rekomendasi = db.session.query(Buku, func.count(Peminjaman.id).label('jumlah')).join(Peminjaman, Peminjaman.buku_id == Buku.id).filter(Buku.stok > 0).group_by(Buku.id).order_by(func.count(Peminjaman.id).desc()).limit(10).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['rekomendasi_buku'] = [(b, jumlah) for b, jumlah in rekomendasi if b.id not in buku_id_aktif][:5]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  **Alternatif (`else`/`elif`):**

  - **Penyimpanan nilai**: `context['total_buku'] = Buku.query.count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['total_stok'] = sum((b.stok for b in Buku.query.all()))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['sedang_dipinjam'] = Peminjaman.query.filter_by(status='dipinjam').count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['terlambat'] = sum((1 for p in Peminjaman.query.filter_by(status='dipinjam').all() if p.is_telat))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['denda_belum_lunas'] = total_denda_belum_lunas()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['denda_berjalan'] = denda_berjalan_semua()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `(labels_bulanan, data_bulanan) = _data_grafik_peminjaman_bulanan()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['labels_grafik_bulanan'] = labels_bulanan` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['data_grafik_bulanan'] = data_bulanan` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `(labels_top, data_top) = _data_grafik_buku_terpopuler()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['labels_grafik_top_buku'] = labels_top` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['data_grafik_top_buku'] = data_top` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `top_mhs = statistik_mahasiswa_peminjam('semua', limit=5)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['labels_grafik_top_mhs'] = [b['user'].nama_lengkap for b in top_mhs]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['data_grafik_top_mhs'] = [b['total'] for b in top_mhs]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `(labels_kat, data_kat) = _data_grafik_distribusi_kategori()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['labels_grafik_kategori'] = labels_kat` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['data_grafik_kategori'] = data_kat` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `batas_tempo = date.today() + timedelta(days=current_app.config['PERINGATAN_JATUH_TEMPO_HARI'])` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['akan_jatuh_tempo'] = Peminjaman.query.filter(Peminjaman.status == 'dipinjam', Peminjaman.tanggal_jatuh_tempo >= date.today(), Peminjaman.tanggal_jatuh_tempo <= batas_tempo).order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `context['peminjaman_terbaru'] = Peminjaman.query.order_by(Peminjaman.id.desc()).limit(6).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if current_user.is_kepala`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Penyimpanan nilai**: `context['total_anggota'] = User.query.filter_by(role='mahasiswa').count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Penyimpanan nilai**: `context['menunggu_persetujuan'] = User.query.filter_by(role='mahasiswa', status_akun='pending').count()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('dashboard.html', today=date.today(), **context)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `dashboard_bp.route`, `render_template`, `Peminjaman.query.filter_by(user_id=current_user.id, status='dipinjam').all`, `sum`, `denda_berjalan_semua`, `total_denda_belum_lunas`, `len`, `Peminjaman.query.filter_by(user_id=current_user.id).count`, `db.session.query(Buku, func.count(Peminjaman.id).label('jumlah')).join(Peminjaman, Peminjaman.buku_id == Buku.id).filter(Buku.stok > 0).group_by(Buku.id).order_by(func.count(Peminjaman.id).desc()).limit(10).all`, `Buku.query.count`, `Peminjaman.query.filter_by(status='dipinjam').count`, `_data_grafik_peminjaman_bulanan`, `_data_grafik_buku_terpopuler`, `statistik_mahasiswa_peminjam`, `_data_grafik_distribusi_kategori`, `Peminjaman.query.filter(Peminjaman.status == 'dipinjam', Peminjaman.tanggal_jatuh_tempo >= date.today(), Peminjaman.tanggal_jatuh_tempo <= batas_tempo).order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all`, `Peminjaman.query.order_by(Peminjaman.id.desc()).limit(6).all`, `date.today`, `timedelta`, `User.query.filter_by(role='mahasiswa').count` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('dashboard.html', today=date.today(), **context)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/denda.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `_query_denda` — `Website/routes/denda.py:23–38`

**Docstring sumber:** Peminjaman yang memiliki denda (sudah dibekukan) sesuai filter status & pencarian.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `status`, `q`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `query = Peminjaman.query.filter(Peminjaman.denda > 0)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if status in ('belum_lunas', 'lunas', 'dibebaskan')`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `query = query.filter(Peminjaman.status_denda == status)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `like = f'%{q}%'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `query = query.join(User, Peminjaman.user_id == User.id).join(Buku, Peminjaman.buku_id == Buku.id).filter(db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like), User.nim.ilike(like), Buku.judul.ilike(like)))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return query`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Peminjaman.query.filter`, `query.filter`, `query.join(User, Peminjaman.user_id == User.id).join(Buku, Peminjaman.buku_id == Buku.id).filter`, `db.or_`, `query.join(User, Peminjaman.user_id == User.id).join`, `User.nama_lengkap.ilike`, `User.username.ilike`, `User.nim.ilike`, `Buku.judul.ilike`, `query.join`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `query`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `daftar_denda` — `Website/routes/denda.py:44–75`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `status = request.args.get('status', 'belum_lunas')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `q = request.args.get('q', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if status == 'berjalan'`**: bila kondisi benar, jalankan 3 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

  - **Penyimpanan nilai**: `semua = Peminjaman.query.filter_by(status='dipinjam').order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `daftar = [p for p in semua if denda_peminjaman(p) > 0 or p.hari_telat > 0]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Penyimpanan nilai**: `k = q.lower()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Penyimpanan nilai**: `daftar = [p for p in daftar if k in p.anggota.nama_lengkap.lower() or k in p.anggota.username.lower() or k in p.buku.judul.lower()]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  **Alternatif (`else`/`elif`):**

  - **Penyimpanan nilai**: `daftar = _query_denda(status, q).order_by(Peminjaman.tanggal_kembali.desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `awal_bulan = date.today().replace(day=1)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `total_belum_lunas = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(Peminjaman.status_denda == 'belum_lunas').scalar() or 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `terkumpul_bulan_ini = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(Peminjaman.status_denda == 'lunas', Peminjaman.tanggal_denda_selesai >= awal_bulan).scalar() or 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `terkumpul_total = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(Peminjaman.status_denda == 'lunas').scalar() or 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('denda/daftar.html', daftar=daftar, status=status, q=q, total_belum_lunas=int(total_belum_lunas), terkumpul_bulan_ini=int(terkumpul_bulan_ini), terkumpul_total=int(terkumpul_total), total_berjalan=denda_berjalan_semua(), total_daftar=sum((denda_peminjaman(p) for p in daftar)), status_label=STATUS_LABEL)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `denda_bp.route`, `role_required`, `request.args.get`, `request.args.get('q', '').strip`, `date.today().replace`, `render_template`, `Peminjaman.query.filter_by(status='dipinjam').order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all`, `_query_denda(status, q).order_by(Peminjaman.tanggal_kembali.desc()).all`, `db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(Peminjaman.status_denda == 'belum_lunas').scalar`, `db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(Peminjaman.status_denda == 'lunas', Peminjaman.tanggal_denda_selesai >= awal_bulan).scalar`, `db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(Peminjaman.status_denda == 'lunas').scalar`, `q.lower`, `date.today`, `int`, `denda_berjalan_semua`, `sum`, `Peminjaman.query.filter_by(status='dipinjam').order_by`, `_query_denda(status, q).order_by`, `db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter`, `Peminjaman.tanggal_jatuh_tempo.asc` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('denda/daftar.html', daftar=daftar, status=status, q=q, total_belum_lunas=int(total_belum_lunas), terkumpul_bulan_ini=int(terkumpul_bulan_ini), terkumpul_total=int(terkumpul_total), total_berjalan=denda_berjalan_semua(), total_daftar=sum((denda_peminjaman(p) for p in daftar)), status_label=STATUS_LABEL)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `lunasi` — `Website/routes/denda.py:81–92`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.status_denda != 'belum_lunas'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Denda ini tidak berstatus belum lunas.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(request.referrer or url_for('denda.daftar_denda'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `p.status_denda = 'lunas'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.tanggal_denda_selesai = date.today()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.denda_diproses_oleh = current_user.id` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f'Denda {format_rupiah(p.denda)} dari {p.anggota.nama_lengkap} dicatat LUNAS.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(request.referrer or url_for('denda.daftar_denda'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `denda_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `date.today`, `db.session.commit`, `flash`, `redirect`, `url_for`, `format_rupiah`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(request.referrer or url_for('denda.daftar_denda'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `bebaskan` — `Website/routes/denda.py:98–111`

**Docstring sumber:** Hapus denda tanpa pembayaran (mis. alasan khusus). Khusus kepala perpustakaan.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.status_denda != 'belum_lunas'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Denda ini tidak berstatus belum lunas.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(request.referrer or url_for('denda.daftar_denda'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `p.status_denda = 'dibebaskan'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.tanggal_denda_selesai = date.today()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.denda_diproses_oleh = current_user.id` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.catatan_denda = request.form.get('catatan', '').strip()[:255] or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f'Denda {format_rupiah(p.denda)} dari {p.anggota.nama_lengkap} dibebaskan.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(request.referrer or url_for('denda.daftar_denda'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `denda_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `date.today`, `db.session.commit`, `flash`, `redirect`, `request.form.get('catatan', '').strip`, `url_for`, `format_rupiah`, `request.form.get`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(request.referrer or url_for('denda.daftar_denda'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `ekspor_denda` — `Website/routes/denda.py:117–137`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `status = request.args.get('status', 'semua')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `daftar = _query_denda(status, '').order_by(Peminjaman.tanggal_kembali.desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `baris = [[p.anggota.nama_lengkap, p.anggota.nim or p.anggota.username, p.buku.judul, p.tanggal_pinjam.strftime('%d-%m-%Y'), p.tanggal_jatuh_tempo.strftime('%d-%m-%Y'), p.tanggal_kembali.strftime('%d-%m-%Y') if p.tanggal_kembali else '-', p.hari_telat, p.denda, STATUS_LABEL.get(p.status_denda, p.status_denda), p.tanggal_denda_selesai.strftime('%d-%m-%Y') if p.tanggal_denda_selesai else '-'] for p in daftar]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `buffer = buat_excel('Denda', ['Mahasiswa', 'NIM/Username', 'Buku', 'Tgl Pinjam', 'Jatuh Tempo', 'Tgl Kembali', 'Hari Telat', 'Denda (Rp)', 'Status', 'Tgl Lunas/Bebas'], baris)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return send_file(buffer, as_attachment=True, download_name=f'laporan_denda_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `denda_bp.route`, `role_required`, `request.args.get`, `_query_denda(status, '').order_by(Peminjaman.tanggal_kembali.desc()).all`, `buat_excel`, `send_file`, `_query_denda(status, '').order_by`, `p.tanggal_pinjam.strftime`, `p.tanggal_jatuh_tempo.strftime`, `STATUS_LABEL.get`, `Peminjaman.tanggal_kembali.desc`, `p.tanggal_kembali.strftime`, `p.tanggal_denda_selesai.strftime`, `_query_denda`, `date.today().isoformat`, `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `send_file(buffer, as_attachment=True, download_name=f'laporan_denda_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/kartu.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `kartu_saya` — `Website/routes/kartu.py:20–22`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kartu = _terbitkan_kartu_jika_belum_ada(current_user)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('kartu/kartu.html', kartu=kartu, anggota=current_user)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `_terbitkan_kartu_jika_belum_ada`, `render_template`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('kartu/kartu.html', kartu=kartu, anggota=current_user)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `kartu_saya_cetak` — `Website/routes/kartu.py:27–29`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kartu = _terbitkan_kartu_jika_belum_ada(current_user)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('kartu/cetak.html', kartu=kartu, anggota=current_user)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `_terbitkan_kartu_jika_belum_ada`, `render_template`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('kartu/cetak.html', kartu=kartu, anggota=current_user)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `kartu_anggota_lain` — `Website/routes/kartu.py:35–38`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `anggota = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kartu = _terbitkan_kartu_jika_belum_ada(anggota)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('kartu/kartu.html', kartu=kartu, anggota=anggota)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `role_required`, `User.query.get_or_404`, `_terbitkan_kartu_jika_belum_ada`, `render_template`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('kartu/kartu.html', kartu=kartu, anggota=anggota)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `kartu_anggota_lain_cetak` — `Website/routes/kartu.py:44–47`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `anggota = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kartu = _terbitkan_kartu_jika_belum_ada(anggota)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('kartu/cetak.html', kartu=kartu, anggota=anggota)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `role_required`, `User.query.get_or_404`, `_terbitkan_kartu_jika_belum_ada`, `render_template`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('kartu/cetak.html', kartu=kartu, anggota=anggota)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `kelola_kartu` — `Website/routes/kartu.py:59–88`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `q = request.args.get('q', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `filter_status = request.args.get('status', 'semua')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `query = KartuAnggota.query.join(User, KartuAnggota.user_id == User.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `like = f'%{q}%'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `query = query.filter(db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like), User.nim.ilike(like)))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if filter_status == 'aktif'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

  - **Penyimpanan nilai**: `query = query.filter(KartuAnggota.status == 'aktif', KartuAnggota.tanggal_kadaluarsa >= date.today())` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  **Alternatif (`else`/`elif`):**

  - **Percabangan `if filter_status == 'nonaktif'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

    - **Penyimpanan nilai**: `query = query.filter(KartuAnggota.status == 'nonaktif')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    **Alternatif (`else`/`elif`):**

    - **Percabangan `if filter_status == 'kadaluarsa'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

      - **Penyimpanan nilai**: `query = query.filter(KartuAnggota.tanggal_kadaluarsa < date.today())` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `daftar = query.order_by(User.nama_lengkap.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `tanpa_kartu = User.query.outerjoin(KartuAnggota, KartuAnggota.user_id == User.id).filter(KartuAnggota.id.is_(None), User.status_akun == 'disetujui').order_by(User.nama_lengkap.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('kartu/kelola.html', daftar=daftar, tanpa_kartu=tanpa_kartu, q=q, filter_status=filter_status, today=date.today())`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `role_required`, `request.args.get('q', '').strip`, `request.args.get`, `KartuAnggota.query.join`, `query.order_by(User.nama_lengkap.asc()).all`, `User.query.outerjoin(KartuAnggota, KartuAnggota.user_id == User.id).filter(KartuAnggota.id.is_(None), User.status_akun == 'disetujui').order_by(User.nama_lengkap.asc()).all`, `render_template`, `query.filter`, `db.or_`, `query.order_by`, `User.query.outerjoin(KartuAnggota, KartuAnggota.user_id == User.id).filter(KartuAnggota.id.is_(None), User.status_akun == 'disetujui').order_by`, `date.today`, `User.nama_lengkap.ilike`, `User.username.ilike`, `User.nim.ilike`, `User.nama_lengkap.asc`, `User.query.outerjoin(KartuAnggota, KartuAnggota.user_id == User.id).filter`, `KartuAnggota.id.is_`, `User.query.outerjoin`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('kartu/kelola.html', daftar=daftar, tanpa_kartu=tanpa_kartu, q=q, filter_status=filter_status, today=date.today())`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `terbitkan_kartu` — `Website/routes/kartu.py:94–101`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `user = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if user.kartu`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (2 pernyataan).

  - **Efek/prosedur**: `flash('Pengguna ini sudah memiliki kartu.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  **Alternatif (`else`/`elif`):**

  - **Pemanggilan**: `_terbitkan_kartu_jika_belum_ada(user)` — meminta fungsi/metode lain melakukan tugasnya.

  - **Efek/prosedur**: `flash(f"Kartu untuk '{user.nama_lengkap}' berhasil diterbitkan.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('kartu.kelola_kartu'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `role_required`, `User.query.get_or_404`, `redirect`, `flash`, `_terbitkan_kartu_jika_belum_ada`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('kartu.kelola_kartu'))`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `edit_kartu` — `Website/routes/kartu.py:107–142`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `kartu_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kartu = KartuAnggota.query.get_or_404(kartu_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `pemilik = kartu.pemilik` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 13 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `(nim, err) = validasi_nim(request.form.get('nim', ''), wajib=pemilik.is_mahasiswa, abaikan_user_id=pemilik.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if err`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(err, 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('kartu.edit_kartu', kartu_id=kartu.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penanganan pengecualian (`try/except`)**: menjalankan proses utama dan menangani error yang sesuai.

    - **Penyimpanan nilai**: `terbit = date.fromisoformat(request.form.get('tanggal_terbit', ''))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Penyimpanan nilai**: `kadaluarsa = date.fromisoformat(request.form.get('tanggal_kadaluarsa', ''))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Efek/prosedur**: `flash('Format tanggal tidak valid.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('kartu.edit_kartu', kartu_id=kartu.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if kadaluarsa < terbit`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Tanggal kadaluarsa tidak boleh lebih awal dari tanggal terbit.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('kartu.edit_kartu', kartu_id=kartu.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `status = request.form.get('status', kartu.status)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if status not in ('aktif', 'nonaktif')`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Status kartu tidak valid.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('kartu.edit_kartu', kartu_id=kartu.id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `pemilik.nim = nim` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `kartu.tanggal_terbit = terbit` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `kartu.tanggal_kadaluarsa = kadaluarsa` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `kartu.status = status` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `flash(f"Kartu '{pemilik.nama_lengkap}' berhasil diperbarui.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('kartu.kelola_kartu'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return render_template('kartu/edit.html', kartu=kartu, pemilik=pemilik)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `role_required`, `KartuAnggota.query.get_or_404`, `render_template`, `validasi_nim`, `request.form.get`, `db.session.commit`, `flash`, `redirect`, `date.fromisoformat`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('kartu/edit.html', kartu=kartu, pemilik=pemilik)`, `redirect(url_for('kartu.kelola_kartu'))`, `redirect(url_for('kartu.edit_kartu', kartu_id=kartu.id))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `toggle_kartu` — `Website/routes/kartu.py:148–153`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `kartu_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kartu = KartuAnggota.query.get_or_404(kartu_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kartu.status = 'nonaktif' if kartu.status == 'aktif' else 'aktif'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Kartu '{kartu.pemilik.nama_lengkap}' sekarang {kartu.status}.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(request.referrer or url_for('kartu.kelola_kartu'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `role_required`, `KartuAnggota.query.get_or_404`, `db.session.commit`, `flash`, `redirect`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(request.referrer or url_for('kartu.kelola_kartu'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `perpanjang_kartu` — `Website/routes/kartu.py:159–173`

**Docstring sumber:** Perpanjang masa berlaku. Dihitung dari tanggal kadaluarsa saat ini kalau
kartu masih berlaku, atau dari hari ini kalau sudah kadaluarsa.

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `kartu_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kartu = KartuAnggota.query.get_or_404(kartu_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `hari = current_app.config['MASA_BERLAKU_KARTU_HARI']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `dasar = max(kartu.tanggal_kadaluarsa, date.today())` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kartu.tanggal_kadaluarsa = dasar + timedelta(days=hari)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kartu.status = 'aktif'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Kartu '{kartu.pemilik.nama_lengkap}' diperpanjang sampai {kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y')}.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('kartu.kelola_kartu'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `kartu_bp.route`, `role_required`, `KartuAnggota.query.get_or_404`, `max`, `db.session.commit`, `flash`, `redirect`, `date.today`, `timedelta`, `url_for`, `kartu.tanggal_kadaluarsa.strftime`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('kartu.kelola_kartu'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/laporan.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `buku_populer` — `Website/routes/laporan.py:19–28`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `hasil = db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by(db.func.count(Peminjaman.id).desc()).limit(20).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('laporan/populer.html', hasil=hasil)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `laporan_bp.route`, `role_required`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by(db.func.count(Peminjaman.id).desc()).limit(20).all`, `render_template`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by(db.func.count(Peminjaman.id).desc()).limit`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).order_by`, `db.func.count(Peminjaman.id).desc`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by`, `db.func.count`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join`, `db.session.query`, `db.func.count(Peminjaman.id).label`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('laporan/populer.html', hasil=hasil)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `buku_tidak_populer` — `Website/routes/laporan.py:34–48`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `subq = db.session.query(Peminjaman.buku_id).distinct().subquery()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `tidak_pernah = Buku.query.filter(~Buku.id.in_(subq)).order_by(Buku.judul).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `jarang = db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).having(db.func.count(Peminjaman.id) <= 2).order_by(db.func.count(Peminjaman.id).asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('laporan/tidak_populer.html', tidak_pernah=tidak_pernah, jarang=jarang)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `laporan_bp.route`, `role_required`, `db.session.query(Peminjaman.buku_id).distinct().subquery`, `Buku.query.filter(~Buku.id.in_(subq)).order_by(Buku.judul).all`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).having(db.func.count(Peminjaman.id) <= 2).order_by(db.func.count(Peminjaman.id).asc()).all`, `render_template`, `db.session.query(Peminjaman.buku_id).distinct`, `Buku.query.filter(~Buku.id.in_(subq)).order_by`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).having(db.func.count(Peminjaman.id) <= 2).order_by`, `db.func.count(Peminjaman.id).asc`, `db.session.query`, `Buku.query.filter`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by(Buku.id).having`, `db.func.count`, `Buku.id.in_`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join(Peminjaman, Peminjaman.buku_id == Buku.id).group_by`, `db.session.query(Buku, db.func.count(Peminjaman.id).label('jumlah_pinjam')).join`, `db.func.count(Peminjaman.id).label`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('laporan/tidak_populer.html', tidak_pernah=tidak_pernah, jarang=jarang)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `statistik_mahasiswa_peminjam` — `Website/routes/laporan.py:67–129`

**Docstring sumber:** Peringkat mahasiswa berdasarkan jumlah buku yang dipinjam.

Kembalikan list dict berurut dari yang paling sering meminjam:
user, total, judul_unik, sedang_dipinjam, terlambat, terakhir, peringkat.
Urutan seri: yang lebih baru meminjam dulu, lalu nama A-Z.

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `kunci_periode`, `limit`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if kunci_periode not in PERIODE_STATISTIK`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `kunci_periode = 'semua'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `hari = PERIODE_STATISTIK[kunci_periode][1]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `hari_ini = date.today()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `telat = case((and_(Peminjaman.status == 'dikembalikan', Peminjaman.tanggal_kembali > Peminjaman.tanggal_jatuh_tempo), 1), (and_(Peminjaman.status == 'dipinjam', Peminjaman.tanggal_jatuh_tempo < hari_ini), 1), else_=0)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `sedang = case((Peminjaman.status == 'dipinjam', 1), else_=0)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `q = db.session.query(User, func.count(Peminjaman.id).label('total'), func.count(Peminjaman.buku_id.distinct()).label('judul_unik'), func.sum(sedang).label('sedang'), func.sum(telat).label('telat'), func.max(Peminjaman.tanggal_pinjam).label('terakhir')).join(Peminjaman, Peminjaman.user_id == User.id).filter(User.role == 'mahasiswa', Peminjaman.status.in_(STATUS_DIHITUNG))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if hari`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `q = q.filter(Peminjaman.tanggal_pinjam >= hari_ini - timedelta(days=hari))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `q = q.group_by(User.id).order_by(func.count(Peminjaman.id).desc(), func.max(Peminjaman.tanggal_pinjam).desc(), User.nama_lengkap.asc())` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if limit`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `q = q.limit(limit)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `hasil = []` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Perulangan** (`(user, total, judul_unik, sedang_n, telat_n, terakhir) melalui q.all()`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Pemanggilan**: `hasil.append({'user': user, 'total': int(total), 'judul_unik': int(judul_unik), 'sedang_dipinjam': int(sedang_n or 0), 'terlambat': int(telat_n or 0), 'terakhir': terakhir})` — meminta fungsi/metode lain melakukan tugasnya.

- **Perulangan** (`(i, baris) melalui enumerate(hasil)`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Percabangan `if i > 0 and baris['total'] == hasil[i - 1]['total']`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

    - **Penyimpanan nilai**: `baris['peringkat'] = hasil[i - 1]['peringkat']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    **Alternatif (`else`/`elif`):**

    - **Penyimpanan nilai**: `baris['peringkat'] = i + 1` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return hasil`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `date.today`, `case`, `db.session.query(User, func.count(Peminjaman.id).label('total'), func.count(Peminjaman.buku_id.distinct()).label('judul_unik'), func.sum(sedang).label('sedang'), func.sum(telat).label('telat'), func.max(Peminjaman.tanggal_pinjam).label('terakhir')).join(Peminjaman, Peminjaman.user_id == User.id).filter`, `q.group_by(User.id).order_by`, `q.all`, `enumerate`, `Peminjaman.status.in_`, `q.filter`, `func.count(Peminjaman.id).desc`, `func.max(Peminjaman.tanggal_pinjam).desc`, `User.nama_lengkap.asc`, `q.limit`, `hasil.append`, `and_`, `db.session.query(User, func.count(Peminjaman.id).label('total'), func.count(Peminjaman.buku_id.distinct()).label('judul_unik'), func.sum(sedang).label('sedang'), func.sum(telat).label('telat'), func.max(Peminjaman.tanggal_pinjam).label('terakhir')).join`, `q.group_by`, `func.count`, `func.max`, `int`, `db.session.query` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `hasil`.

**Efek samping yang perlu diperhatikan.** mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_periode_dari_request` — `Website/routes/laporan.py:132–134`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kunci = request.args.get('periode', 'semua')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return kunci if kunci in PERIODE_STATISTIK else 'semua'`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `request.args.get`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `kunci if kunci in PERIODE_STATISTIK else 'semua'`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `mahasiswa_aktif` — `Website/routes/laporan.py:140–150`

**Docstring sumber:** Mahasiswa yang paling sering meminjam buku (top 50).

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kunci = _periode_dari_request()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `hasil = statistik_mahasiswa_peminjam(kunci, limit=50)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('laporan/mahasiswa_aktif.html', hasil=hasil, periode=kunci, periode_opsi=PERIODE_STATISTIK, total_terbanyak=hasil[0]['total'] if hasil else 0)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `laporan_bp.route`, `role_required`, `_periode_dari_request`, `statistik_mahasiswa_peminjam`, `render_template`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('laporan/mahasiswa_aktif.html', hasil=hasil, periode=kunci, periode_opsi=PERIODE_STATISTIK, total_terbanyak=hasil[0]['total'] if hasil else 0)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `ekspor_mahasiswa_aktif` — `Website/routes/laporan.py:156–174`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kunci = _periode_dari_request()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `baris = [[b['peringkat'], b['user'].nama_lengkap, b['user'].nim or b['user'].username, b['total'], b['judul_unik'], b['sedang_dipinjam'], b['terlambat'], b['terakhir'].strftime('%d-%m-%Y') if b['terakhir'] else '-'] for b in statistik_mahasiswa_peminjam(kunci)]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `buffer = buat_excel('Mahasiswa Aktif', ['Peringkat', 'Mahasiswa', 'NIM/Username', 'Total Dipinjam', 'Judul Berbeda', 'Sedang Dipinjam', 'Kali Terlambat', 'Terakhir Meminjam'], baris)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return send_file(buffer, as_attachment=True, download_name=f'mahasiswa_aktif_{kunci}_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `laporan_bp.route`, `role_required`, `_periode_dari_request`, `buat_excel`, `send_file`, `statistik_mahasiswa_peminjam`, `b['terakhir'].strftime`, `date.today().isoformat`, `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `send_file(buffer, as_attachment=True, download_name=f'mahasiswa_aktif_{kunci}_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `_daftar_terlambat` — `Website/routes/laporan.py:177–183`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `semua = Peminjaman.query.filter_by(status='dipinjam').order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return sorted((p for p in semua if p.hari_telat > 0), key=lambda p: p.hari_telat, reverse=True)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Peminjaman.query.filter_by(status='dipinjam').order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all`, `sorted`, `Peminjaman.query.filter_by(status='dipinjam').order_by`, `Peminjaman.tanggal_jatuh_tempo.asc`, `Peminjaman.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `sorted((p for p in semua if p.hari_telat > 0), key=lambda p: p.hari_telat, reverse=True)`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `buku_terlambat` — `Website/routes/laporan.py:189–193`

**Docstring sumber:** Semua buku yang sudah lewat jatuh tempo dan belum kembali, terlama di atas.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `daftar = _daftar_terlambat()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `total_denda = sum((denda_peminjaman(p) for p in daftar))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('laporan/terlambat.html', daftar=daftar, total_denda=total_denda)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `laporan_bp.route`, `role_required`, `_daftar_terlambat`, `sum`, `render_template`, `denda_peminjaman`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('laporan/terlambat.html', daftar=daftar, total_denda=total_denda)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `ekspor_terlambat` — `Website/routes/laporan.py:199–213`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `baris = [[p.anggota.nama_lengkap, p.anggota.nim or p.anggota.username, p.anggota.no_telepon or '-', p.buku.judul, p.tanggal_jatuh_tempo.strftime('%d-%m-%Y'), p.hari_telat, denda_peminjaman(p)] for p in _daftar_terlambat()]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `buffer = buat_excel('Terlambat', ['Mahasiswa', 'NIM/Username', 'No. Telepon', 'Buku', 'Jatuh Tempo', 'Hari Telat', 'Denda Berjalan (Rp)'], baris)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return send_file(buffer, as_attachment=True, download_name=f'buku_terlambat_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `laporan_bp.route`, `role_required`, `buat_excel`, `send_file`, `p.tanggal_jatuh_tempo.strftime`, `denda_peminjaman`, `_daftar_terlambat`, `date.today().isoformat`, `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `send_file(buffer, as_attachment=True, download_name=f'buku_terlambat_{date.today().isoformat()}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/peminjaman.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `ajukan_peminjaman` — `Website/routes/peminjaman.py:21–56`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `buku = Buku.query.get_or_404(buku_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if buku.stok <= 0`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Stok buku habis, pengajuan tidak dapat dibuat.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.detail_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `aktif = Peminjaman.query.filter(Peminjaman.user_id == current_user.id, Peminjaman.buku_id == buku.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if aktif`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Anda sudah memiliki pengajuan/peminjaman aktif untuk buku ini.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.detail_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `(ok, pesan) = cek_bisa_meminjam(current_user)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if not ok`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash(pesan, 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('buku.detail_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `pengajuan = Peminjaman(user_id=current_user.id, buku_id=buku.id, tanggal_pinjam=date.today(), tanggal_jatuh_tempo=hitung_jatuh_tempo(buku, date.today()), status='diajukan')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.add(pengajuan)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Pengajuan peminjaman buku '{buku.judul}' berhasil dikirim, menunggu persetujuan staf/kepala perpustakaan.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('buku.detail_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Buku.query.get_or_404`, `Peminjaman.query.filter(Peminjaman.user_id == current_user.id, Peminjaman.buku_id == buku.id, Peminjaman.status.in_(['diajukan', 'dipinjam'])).first`, `cek_bisa_meminjam`, `Peminjaman`, `db.session.add`, `db.session.commit`, `flash`, `redirect`, `url_for`, `Peminjaman.query.filter`, `date.today`, `hitung_jatuh_tempo`, `Peminjaman.status.in_`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('buku.detail_buku', buku_id=buku_id))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `batalkan_pengajuan` — `Website/routes/peminjaman.py:62–73`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.user_id != current_user.id`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Pemanggilan**: `abort(403)` — meminta fungsi/metode lain melakukan tugasnya.

- **Percabangan `if p.status != 'diajukan'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Hanya pengajuan yang masih menunggu persetujuan yang dapat dibatalkan.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.riwayat_saya'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Efek/prosedur**: `db.session.delete(p)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash('Pengajuan peminjaman berhasil dibatalkan.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('peminjaman.riwayat_saya'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `db.session.delete`, `db.session.commit`, `flash`, `redirect`, `abort`, `url_for`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('peminjaman.riwayat_saya'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `daftar_pengajuan` — `Website/routes/peminjaman.py:82–91`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `daftar = Peminjaman.query.filter_by(status='diajukan').order_by(Peminjaman.id.asc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('peminjaman/pengajuan.html', daftar=daftar, today=date.today(), lama_pinjam_untuk=lama_pinjam_untuk)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Peminjaman.query.filter_by(status='diajukan').order_by(Peminjaman.id.asc()).all`, `render_template`, `Peminjaman.query.filter_by(status='diajukan').order_by`, `date.today`, `Peminjaman.id.asc`, `Peminjaman.query.filter_by`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('peminjaman/pengajuan.html', daftar=daftar, today=date.today(), lama_pinjam_untuk=lama_pinjam_untuk)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `setujui_pengajuan` — `Website/routes/peminjaman.py:97–128`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.status != 'diajukan'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Pengajuan ini sudah diproses sebelumnya.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_pengajuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if p.buku.stok <= 0`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash(f"Stok buku '{p.buku.judul}' habis, tidak bisa disetujui.", 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_pengajuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `(ok, pesan) = cek_kartu_valid(p.anggota)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if not ok`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash(f'Tidak bisa disetujui untuk {p.anggota.nama_lengkap}: {pesan}', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_pengajuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `lama_hari = request.form.get('lama_hari', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.status = 'dipinjam'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.diproses_oleh = current_user.id` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.tanggal_pinjam = date.today()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.tanggal_jatuh_tempo = hitung_jatuh_tempo(p.buku, date.today(), lama_hari)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pernyataan**: `p.buku.stok -= 1`.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Pengajuan '{p.buku.judul}' oleh {p.anggota.nama_lengkap} disetujui. Jatuh tempo: {p.tanggal_jatuh_tempo.strftime('%d-%m-%Y')}.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('peminjaman.daftar_pengajuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `cek_kartu_valid`, `request.form.get`, `date.today`, `hitung_jatuh_tempo`, `db.session.commit`, `flash`, `redirect`, `url_for`, `p.tanggal_jatuh_tempo.strftime`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('peminjaman.daftar_pengajuan'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `tolak_pengajuan` — `Website/routes/peminjaman.py:134–146`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.status != 'diajukan'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Pengajuan ini sudah diproses sebelumnya.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_pengajuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `p.status = 'ditolak'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.diproses_oleh = current_user.id` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.catatan = request.form.get('catatan', '').strip() or None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Pengajuan '{p.buku.judul}' oleh {p.anggota.nama_lengkap} ditolak.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('peminjaman.daftar_pengajuan'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `db.session.commit`, `flash`, `redirect`, `request.form.get('catatan', '').strip`, `url_for`, `request.form.get`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('peminjaman.daftar_pengajuan'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `pinjam_buku` — `Website/routes/peminjaman.py:155–207`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `buku = Buku.query.get_or_404(buku_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 15 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `user_id = request.form.get('user_id', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `anggota = User.query.filter_by(id=user_id, role='mahasiswa').first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not anggota`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Anggota tidak ditemukan.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('peminjaman.pinjam_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Percabangan `if buku.stok <= 0`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash('Stok buku habis, tidak bisa dipinjam.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('buku.detail_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `sudah_pinjam = Peminjaman.query.filter_by(user_id=anggota.id, buku_id=buku.id, status='dipinjam').first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if sudah_pinjam`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(f'{anggota.nama_lengkap} masih meminjam buku ini dan belum mengembalikannya.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('peminjaman.pinjam_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `(ok, pesan) = cek_bisa_meminjam(anggota)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not ok`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

    - **Efek/prosedur**: `flash(f'{anggota.nama_lengkap}: {pesan}', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **`return redirect(url_for('peminjaman.pinjam_buku', buku_id=buku_id))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **Penyimpanan nilai**: `lama_hari = request.form.get('lama_hari', type=int)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `peminjaman = Peminjaman(user_id=anggota.id, buku_id=buku.id, diproses_oleh=current_user.id, tanggal_pinjam=date.today(), tanggal_jatuh_tempo=hitung_jatuh_tempo(buku, date.today(), lama_hari), status='dipinjam')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Pernyataan**: `buku.stok -= 1`.

  - **Efek/prosedur**: `db.session.add(peminjaman)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **Efek/prosedur**: `flash(f"Buku '{buku.judul}' berhasil dipinjamkan ke {anggota.nama_lengkap}. Jatuh tempo: {peminjaman.tanggal_jatuh_tempo.strftime('%d-%m-%Y')}.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `anggota_list = User.query.filter_by(role='mahasiswa', is_active_db=True).order_by(User.nama_lengkap).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('peminjaman/pinjam.html', buku=buku, anggota_list=anggota_list, lama_default=lama_pinjam_untuk(buku))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Buku.query.get_or_404`, `User.query.filter_by(role='mahasiswa', is_active_db=True).order_by(User.nama_lengkap).all`, `render_template`, `request.form.get`, `User.query.filter_by(id=user_id, role='mahasiswa').first`, `Peminjaman.query.filter_by(user_id=anggota.id, buku_id=buku.id, status='dipinjam').first`, `cek_bisa_meminjam`, `Peminjaman`, `db.session.add`, `db.session.commit`, `flash`, `redirect`, `url_for`, `User.query.filter_by(role='mahasiswa', is_active_db=True).order_by`, `lama_pinjam_untuk`, `User.query.filter_by`, `Peminjaman.query.filter_by`, `date.today` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('peminjaman/pinjam.html', buku=buku, anggota_list=anggota_list, lama_default=lama_pinjam_untuk(buku))`, `redirect(url_for('peminjaman.daftar_peminjaman'))`, `redirect(url_for('peminjaman.pinjam_buku', buku_id=buku_id))`, `redirect(url_for('buku.detail_buku', buku_id=buku_id))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `daftar_peminjaman` — `Website/routes/peminjaman.py:216–239`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `status_filter = request.args.get('status', 'dipinjam')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `q = request.args.get('q', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `query = Peminjaman.query` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if status_filter != 'semua'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `query = query.filter_by(status=status_filter)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `like = f'%{q}%'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `query = query.join(User, Peminjaman.user_id == User.id).join(Buku, Peminjaman.buku_id == Buku.id).filter(db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like), Buku.judul.ilike(like)))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `daftar = query.order_by(Peminjaman.tanggal_pinjam.desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('peminjaman/daftar.html', daftar=daftar, status_filter=status_filter, q=q, today=date.today())`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `request.args.get`, `request.args.get('q', '').strip`, `query.order_by(Peminjaman.tanggal_pinjam.desc()).all`, `render_template`, `query.filter_by`, `query.join(User, Peminjaman.user_id == User.id).join(Buku, Peminjaman.buku_id == Buku.id).filter`, `db.or_`, `query.order_by`, `date.today`, `query.join(User, Peminjaman.user_id == User.id).join`, `User.nama_lengkap.ilike`, `User.username.ilike`, `Buku.judul.ilike`, `Peminjaman.tanggal_pinjam.desc`, `query.join`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('peminjaman/daftar.html', daftar=daftar, status_filter=status_filter, q=q, today=date.today())`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `kembalikan_buku` — `Website/routes/peminjaman.py:248–287`

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.status == 'dikembalikan'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Buku ini sudah dikembalikan sebelumnya.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if p.status != 'dipinjam'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Hanya buku yang sedang dipinjam yang bisa dikembalikan.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `p.tanggal_kembali = date.today()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.status = 'dikembalikan'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.denda = denda_dari_config(p.tanggal_jatuh_tempo, p.tanggal_kembali)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.status_denda = 'belum_lunas' if p.denda > 0 else 'tidak_ada'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pernyataan**: `p.buku.stok += 1`.

- **Percabangan `if p.tanggal_kembali > p.tanggal_jatuh_tempo`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

  - **Penyimpanan nilai**: `hari_telat = (p.tanggal_kembali - p.tanggal_jatuh_tempo).days` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if p.denda > 0 and request.form.get('bayar') == '1'`**: bila kondisi benar, jalankan 4 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

    - **Penyimpanan nilai**: `p.status_denda = 'lunas'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Penyimpanan nilai**: `p.tanggal_denda_selesai = date.today()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Penyimpanan nilai**: `p.denda_diproses_oleh = current_user.id` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Efek/prosedur**: `flash(f'Buku dikembalikan terlambat {hari_telat} hari. Denda {format_rupiah(p.denda)} sudah dibayar lunas.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    **Alternatif (`else`/`elif`):**

    - **Percabangan `if p.denda > 0`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

      - **Efek/prosedur**: `flash(f'Buku dikembalikan TERLAMBAT {hari_telat} hari. Denda {format_rupiah(p.denda)} belum dibayar — catat pembayarannya di menu Denda.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

      **Alternatif (`else`/`elif`):**

      - **Efek/prosedur**: `flash(f'Buku dikembalikan terlambat {hari_telat} hari (masih dalam masa tenggang, tanpa denda).', 'info')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  **Alternatif (`else`/`elif`):**

  - **Efek/prosedur**: `flash('Buku berhasil dikembalikan tepat waktu.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `date.today`, `denda_dari_config`, `db.session.commit`, `redirect`, `flash`, `url_for`, `request.form.get`, `format_rupiah`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(url_for('peminjaman.daftar_peminjaman'))`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `perpanjang` — `Website/routes/peminjaman.py:296–322`

**Docstring sumber:** Perpanjang jatuh tempo dari tanggal jatuh tempo saat ini (bukan dari hari ini).

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.status != 'dipinjam'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Hanya peminjaman yang sedang berjalan yang bisa diperpanjang.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if p.hari_telat > 0`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Buku sudah lewat jatuh tempo dan tidak bisa diperpanjang. Proses pengembalian terlebih dahulu.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `maks = current_app.config['MAKS_PERPANJANG']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.jumlah_perpanjang >= maks`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash(f'Batas perpanjangan tercapai (maksimal {maks} kali untuk satu peminjaman).', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `hari = request.form.get('hari', type=int) or lama_pinjam_untuk(p.buku)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `hari = max(1, min(hari, 365))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p.tanggal_jatuh_tempo = p.tanggal_jatuh_tempo + timedelta(days=hari)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pernyataan**: `p.jumlah_perpanjang += 1`.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Jatuh tempo '{p.buku.judul}' diperpanjang {hari} hari menjadi {p.tanggal_jatuh_tempo.strftime('%d-%m-%Y')} (perpanjangan ke-{p.jumlah_perpanjang}).", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(request.referrer or url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `max`, `db.session.commit`, `flash`, `redirect`, `request.form.get`, `lama_pinjam_untuk`, `min`, `timedelta`, `url_for`, `p.tanggal_jatuh_tempo.strftime`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(request.referrer or url_for('peminjaman.daftar_peminjaman'))`, `redirect(url_for('peminjaman.daftar_peminjaman'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `atur_jatuh_tempo` — `Website/routes/peminjaman.py:328–348`

**Docstring sumber:** Koreksi tanggal jatuh tempo secara langsung. Khusus kepala perpustakaan
karena bisa mengubah besar denda.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `peminjaman_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `p = Peminjaman.query.get_or_404(peminjaman_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if p.status != 'dipinjam'`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Jatuh tempo hanya bisa diatur untuk peminjaman yang sedang berjalan.', 'warning')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penanganan pengecualian (`try/except`)**: menjalankan proses utama dan menangani error yang sesuai.

  - **Penyimpanan nilai**: `baru = date.fromisoformat(request.form.get('tanggal', ''))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `flash('Format tanggal tidak valid.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if baru < p.tanggal_pinjam`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Efek/prosedur**: `flash('Jatuh tempo tidak boleh lebih awal dari tanggal pinjam.', 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `p.tanggal_jatuh_tempo = baru` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `flash(f"Jatuh tempo '{p.buku.judul}' diatur ke {baru.strftime('%d-%m-%Y')}.", 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return redirect(request.referrer or url_for('peminjaman.daftar_peminjaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Peminjaman.query.get_or_404`, `db.session.commit`, `flash`, `redirect`, `date.fromisoformat`, `url_for`, `request.form.get`, `baru.strftime`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `redirect(request.referrer or url_for('peminjaman.daftar_peminjaman'))`, `redirect(url_for('peminjaman.daftar_peminjaman'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, membentuk respons atau pesan web, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `riwayat_saya` — `Website/routes/peminjaman.py:358–368`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `q = request.args.get('q', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `query = Peminjaman.query.filter_by(user_id=current_user.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `like = f'%{q}%'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `query = query.join(Buku, Peminjaman.buku_id == Buku.id).filter(Buku.judul.ilike(like))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `daftar = query.order_by(Peminjaman.id.desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('peminjaman/riwayat_anggota.html', daftar=daftar, anggota=current_user, today=date.today(), bisa_batalkan=True, q=q)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `request.args.get('q', '').strip`, `Peminjaman.query.filter_by`, `query.order_by(Peminjaman.id.desc()).all`, `render_template`, `query.join(Buku, Peminjaman.buku_id == Buku.id).filter`, `request.args.get`, `Buku.judul.ilike`, `query.order_by`, `date.today`, `query.join`, `Peminjaman.id.desc`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('peminjaman/riwayat_anggota.html', daftar=daftar, anggota=current_user, today=date.today(), bisa_batalkan=True, q=q)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `riwayat_anggota` — `Website/routes/peminjaman.py:374–385`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `anggota = User.query.get_or_404(user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `q = request.args.get('q', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `query = Peminjaman.query.filter_by(user_id=user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `like = f'%{q}%'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `query = query.join(Buku, Peminjaman.buku_id == Buku.id).filter(Buku.judul.ilike(like))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `daftar = query.order_by(Peminjaman.id.desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('peminjaman/riwayat_anggota.html', daftar=daftar, anggota=anggota, today=date.today(), bisa_batalkan=False, q=q)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `User.query.get_or_404`, `request.args.get('q', '').strip`, `Peminjaman.query.filter_by`, `query.order_by(Peminjaman.id.desc()).all`, `render_template`, `query.join(Buku, Peminjaman.buku_id == Buku.id).filter`, `request.args.get`, `Buku.judul.ilike`, `query.order_by`, `date.today`, `query.join`, `Peminjaman.id.desc`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('peminjaman/riwayat_anggota.html', daftar=daftar, anggota=anggota, today=date.today(), bisa_batalkan=False, q=q)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `riwayat_buku` — `Website/routes/peminjaman.py:394–404`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `buku = Buku.query.get_or_404(buku_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `q = request.args.get('q', '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `query = Peminjaman.query.filter_by(buku_id=buku_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `like = f'%{q}%'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `query = query.join(User, Peminjaman.user_id == User.id).filter(db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like)))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `daftar = query.order_by(Peminjaman.tanggal_pinjam.desc()).all()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('peminjaman/riwayat_buku.html', daftar=daftar, buku=buku, today=date.today(), q=q)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `peminjaman_bp.route`, `role_required`, `Buku.query.get_or_404`, `request.args.get('q', '').strip`, `Peminjaman.query.filter_by`, `query.order_by(Peminjaman.tanggal_pinjam.desc()).all`, `render_template`, `query.join(User, Peminjaman.user_id == User.id).filter`, `request.args.get`, `db.or_`, `query.order_by`, `date.today`, `query.join`, `User.nama_lengkap.ilike`, `User.username.ilike`, `Peminjaman.tanggal_pinjam.desc`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('peminjaman/riwayat_buku.html', daftar=daftar, buku=buku, today=date.today(), q=q)`.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/routes/pengaturan.py`

Berkas ini menangani permintaan HTTP untuk satu kelompok fitur. Route biasanya membaca parameter URL/form, memeriksa sesi dan hak akses, memanggil utilitas/model, lalu mengembalikan halaman atau redirect.

### `halaman` — `Website/routes/pengaturan.py:13–43`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if request.method == 'POST'`**: bila kondisi benar, jalankan 4 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `(baru, galat) = ({}, [])` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Perulangan** (`(kunci, _cfg, minimum, maksimum, label, satuan, _bantuan) melalui DAFTAR`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

    - **Penyimpanan nilai**: `mentah = request.form.get(kunci, '').strip().replace('.', '')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Penanganan pengecualian (`try/except`)**: menjalankan proses utama dan menangani error yang sesuai.

      - **Penyimpanan nilai**: `nilai = int(mentah)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

      - **Pemanggilan**: `galat.append(f'{label}: isi dengan angka bulat.')` — meminta fungsi/metode lain melakukan tugasnya.

      - **Pernyataan**: `continue`.

    - **Percabangan `if not minimum <= nilai <= maksimum`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Pemanggilan**: `galat.append(f'{label}: harus antara {minimum} dan {maksimum}.')` — meminta fungsi/metode lain melakukan tugasnya.

      - **Pernyataan**: `continue`.

    - **Penyimpanan nilai**: `baru[kunci] = nilai` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if galat`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (2 pernyataan).

    - **Perulangan** (`g melalui galat`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

      - **Efek/prosedur**: `flash(g, 'danger')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    **Alternatif (`else`/`elif`):**

    - **Pemanggilan**: `simpan_pengaturan(baru)` — meminta fungsi/metode lain melakukan tugasnya.

    - **Efek/prosedur**: `flash('Pengaturan disimpan. Berlaku untuk peminjaman berikutnya; peminjaman yang sudah berjalan tidak berubah jatuh temponya.', 'success')` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return redirect(url_for('pengaturan.halaman'))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `nilai = nilai_saat_ini(current_app)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `kolom = [{'kunci': k, 'label': label, 'satuan': satuan, 'bantuan': bantuan, 'min': mn, 'maks': mx, 'nilai': nilai[k]} for k, _c, mn, mx, label, satuan, bantuan in DAFTAR]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return render_template('pengaturan/halaman.html', kolom=kolom)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `pengaturan_bp.route`, `role_required`, `nilai_saat_ini`, `render_template`, `redirect`, `request.form.get(kunci, '').strip().replace`, `simpan_pengaturan`, `flash`, `url_for`, `int`, `galat.append`, `request.form.get(kunci, '').strip`, `request.form.get`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `render_template('pengaturan/halaman.html', kolom=kolom)`, `redirect(url_for('pengaturan.halaman'))`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** membentuk respons atau pesan web. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/utils/decorators.py`

Berkas utilitas berisi logika yang dipakai ulang oleh route atau komponen lain.

### `role_required` — `Website/utils/decorators.py:6–19`

**Docstring sumber:** Decorator untuk membatasi akses route berdasarkan role.
Contoh: @role_required('kepala_perpustakaan') atau @role_required('staf', 'kepala_perpustakaan')

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `*roles`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Pernyataan**: `def decorator(f):

    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role not in roles...`.

- **`return decorator`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `wraps`, `f`, `abort`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `decorator`, `wrapped`, `f(*args, **kwargs)`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `role_required.decorator` — `Website/utils/decorators.py:10–18`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `f`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Pernyataan**: `@wraps(f)
def wrapped(*args, **kwargs):
    if not current_user.is_authenticated:
        abort(401)
    if current_user.role not in roles:
        abort(403)
    return f(*args...`.

- **`return wrapped`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `wraps`, `f`, `abort`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `wrapped`, `f(*args, **kwargs)`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `role_required.decorator.wrapped` — `Website/utils/decorators.py:12–17`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `*args`, `**kwargs`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if not current_user.is_authenticated`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Pemanggilan**: `abort(401)` — meminta fungsi/metode lain melakukan tugasnya.

- **Percabangan `if current_user.role not in roles`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Pemanggilan**: `abort(403)` — meminta fungsi/metode lain melakukan tugasnya.

- **`return f(*args, **kwargs)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `wraps`, `f`, `abort`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `f(*args, **kwargs)`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/utils/denda.py`

Berkas utilitas berisi logika yang dipakai ulang oleh route atau komponen lain.

### `hitung_denda` — `Website/utils/denda.py:11–25`

**Docstring sumber:** Fungsi murni (mudah diuji).

jatuh_tempo, sampai : date  -> 'sampai' = hari ini (masih dipinjam) atau tanggal kembali
tarif               : Rp per hari
maks                : batas atas denda (0 = tanpa batas)
tenggang            : hari gratis setelah jatuh tempo

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `jatuh_tempo`, `sampai`, `tarif`, `maks`, `tenggang`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `hari_kena_denda = (sampai - jatuh_tempo).days - tenggang` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if hari_kena_denda <= 0 or tarif <= 0`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return 0`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `total = hari_kena_denda * tarif` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if maks and total > maks`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `total = maks` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return total`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `total`, `0`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `denda_dari_config` — `Website/utils/denda.py:28–30`

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `jatuh_tempo`, `sampai`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `c = current_app.config` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return hitung_denda(jatuh_tempo, sampai, c['DENDA_PER_HARI'], c['DENDA_MAKS'], c['MASA_TENGGANG_HARI'])`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `hitung_denda`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `hitung_denda(jatuh_tempo, sampai, c['DENDA_PER_HARI'], c['DENDA_MAKS'], c['MASA_TENGGANG_HARI'])`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `denda_peminjaman` — `Website/utils/denda.py:33–42`

**Docstring sumber:** Denda sebuah peminjaman saat ini.
- dikembalikan : nilai yang sudah dibekukan saat pengembalian
- dipinjam     : denda berjalan sampai hari ini
- lainnya      : 0

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `p`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if p.status == 'dikembalikan'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return p.denda or 0`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if p.status == 'dipinjam'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return denda_dari_config(p.tanggal_jatuh_tempo, date.today())`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return 0`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `denda_dari_config`, `date.today`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `0`, `p.denda or 0`, `denda_dari_config(p.tanggal_jatuh_tempo, date.today())`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `total_denda_belum_lunas` — `Website/utils/denda.py:45–52`

**Docstring sumber:** Jumlah denda yang sudah dibekukan tapi belum dibayar (semua anggota atau satu anggota).

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `q = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(Peminjaman.status_denda == 'belum_lunas')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if user_id`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `q = q.filter(Peminjaman.user_id == user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return int(q.scalar() or 0)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter`, `int`, `q.filter`, `db.session.query`, `q.scalar`, `func.coalesce`, `func.sum`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `int(q.scalar() or 0)`.

**Efek samping yang perlu diperhatikan.** mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `denda_berjalan_semua` — `Website/utils/denda.py:55–60`

**Docstring sumber:** Total denda dari buku yang MASIH dipinjam dan sudah telat.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `q = Peminjaman.query.filter_by(status='dipinjam')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if user_id`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `q = q.filter_by(user_id=user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **`return sum((denda_peminjaman(p) for p in q.all()))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Peminjaman.query.filter_by`, `sum`, `q.filter_by`, `denda_peminjaman`, `q.all`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `sum((denda_peminjaman(p) for p in q.all()))`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `format_rupiah` — `Website/utils/denda.py:63–64`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `angka`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return 'Rp ' + f'{int(angka or 0):,}'.replace(',', '.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `f'{int(angka or 0):,}'.replace`, `int`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `'Rp ' + f'{int(angka or 0):,}'.replace(',', '.')`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/utils/excel_export.py`

Berkas utilitas berisi logika yang dipakai ulang oleh route atau komponen lain.

### `buat_excel` — `Website/utils/excel_export.py:8–27`

**Docstring sumber:** header: list nama kolom | baris: list of list. Kembalikan BytesIO siap dikirim.

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `judul_sheet`, `header`, `baris`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `wb = Workbook()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `ws = wb.active` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `ws.title = judul_sheet[:31]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pemanggilan**: `ws.append(header)` — meminta fungsi/metode lain melakukan tugasnya.

- **Perulangan** (`sel melalui ws[1]`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `sel.font = Font(bold=True, color='FFFFFF')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `sel.fill = PatternFill('solid', fgColor='5C211D')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `sel.alignment = Alignment(vertical='center')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Perulangan** (`r melalui baris`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Pemanggilan**: `ws.append(r)` — meminta fungsi/metode lain melakukan tugasnya.

- **Perulangan** (`(i, kolom) melalui enumerate(ws.columns, start=1)`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `terpanjang = max((len(str(c.value)) for c in kolom if c.value is not None), default=8)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = min(terpanjang + 3, 50)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `ws.freeze_panes = 'A2'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `buffer = BytesIO()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pemanggilan**: `wb.save(buffer)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `buffer.seek(0)` — meminta fungsi/metode lain melakukan tugasnya.

- **`return buffer`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Workbook`, `ws.append`, `enumerate`, `BytesIO`, `wb.save`, `buffer.seek`, `Font`, `PatternFill`, `Alignment`, `max`, `min`, `len`, `str`, `ws.cell`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `buffer`.

**Efek samping yang perlu diperhatikan.** membaca/menulis berkas. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/utils/excel_import.py`

Berkas utilitas berisi logika yang dipakai ulang oleh route atau komponen lain.

### `buat_template_excel` — `Website/utils/excel_import.py:13–33`

**Docstring sumber:** Membuat workbook Excel kosong (hanya header) sebagai template import.

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data serta menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** Tidak menerima parameter data eksplisit; metode kelas tetap dapat memakai `self` untuk membaca keadaan objek.. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `wb = Workbook()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `ws = wb.active` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `ws.title = 'Data Buku'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pemanggilan**: `ws.append(TEMPLATE_HEADERS)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `ws.append(['Contoh: Laskar Pelangi', 'Andrea Hirata', 'Bentang Pustaka', 2005, '9789793062792', 'Fiksi', 'Novel tentang pendidikan di Belitung', 3])` — meminta fungsi/metode lain melakukan tugasnya.

- **Perulangan** (`col_cells melalui ws.columns`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `length = max((len(str(cell.value)) if cell.value else 0 for cell in col_cells))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Penyimpanan nilai**: `ws.column_dimensions[col_cells[0].column_letter].width = max(12, length + 2)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `buffer = io.BytesIO()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Pemanggilan**: `wb.save(buffer)` — meminta fungsi/metode lain melakukan tugasnya.

- **Pemanggilan**: `buffer.seek(0)` — meminta fungsi/metode lain melakukan tugasnya.

- **`return buffer`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `Workbook`, `ws.append`, `io.BytesIO`, `wb.save`, `buffer.seek`, `max`, `len`, `str`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `buffer`.

**Efek samping yang perlu diperhatikan.** membaca/menulis berkas. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `import_buku_dari_excel` — `Website/utils/excel_import.py:36–84`

**Docstring sumber:** Membaca file .xlsx yang diupload, lalu insert ke tabel buku.
Mengembalikan (jumlah_sukses, list_error)

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `file_stream`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `wb = load_workbook(file_stream, data_only=True)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `ws = wb.active` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `rows = list(ws.iter_rows(min_row=2, values_only=True))` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `sukses = 0` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `errors = []` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Perulangan** (`(i, row) melalui enumerate(rows, start=2)`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Percabangan `if row is None or all((v is None for v in row))`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **Pernyataan**: `continue`.

  - **Penanganan pengecualian (`try/except`)**: menjalankan proses utama dan menangani error yang sesuai.

    - **Penyimpanan nilai**: `(judul, penulis, penerbit, tahun_terbit, isbn, kategori_nama, deskripsi, stok) = (list(row) + [None] * (len(TEMPLATE_HEADERS) - len(row)))[:len(TEMPLATE_HEADERS)]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Percabangan `if not judul or not penulis`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Pemanggilan**: `errors.append(f"Baris {i}: 'judul' dan 'penulis' wajib diisi, dilewati.")` — meminta fungsi/metode lain melakukan tugasnya.

      - **Pernyataan**: `continue`.

    - **Penyimpanan nilai**: `kategori_obj = None` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Percabangan `if kategori_nama`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

      - **Penyimpanan nilai**: `kategori_obj = Kategori.query.filter_by(nama_kategori=str(kategori_nama).strip()).first()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

      - **Percabangan `if not kategori_obj`**: bila kondisi benar, jalankan 3 pernyataan di cabang utama.

        - **Penyimpanan nilai**: `kategori_obj = Kategori(nama_kategori=str(kategori_nama).strip())` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

        - **Efek/prosedur**: `db.session.add(kategori_obj)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

        - **Efek/prosedur**: `db.session.flush()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **Penyimpanan nilai**: `buku = Buku(judul=str(judul).strip(), penulis=str(penulis).strip(), penerbit=str(penerbit).strip() if penerbit else None, tahun_terbit=int(tahun_terbit) if tahun_terbit else None, isbn=str(isbn).strip() if isbn else None, kategori_id=kategori_obj.id if kategori_obj else None, deskripsi=str(deskripsi).strip() if deskripsi else None, stok=int(stok) if stok else 0)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    - **Efek/prosedur**: `db.session.add(buku)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

    - **Pernyataan**: `sukses += 1`.

    - **Pemanggilan**: `errors.append(f'Baris {i}: gagal diproses ({e})')` — meminta fungsi/metode lain melakukan tugasnya.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return (sukses, errors)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `load_workbook`, `list`, `enumerate`, `db.session.commit`, `ws.iter_rows`, `all`, `Buku`, `db.session.add`, `errors.append`, `Kategori.query.filter_by(nama_kategori=str(kategori_nama).strip()).first`, `len`, `Kategori`, `db.session.flush`, `str(judul).strip`, `str(penulis).strip`, `Kategori.query.filter_by`, `str(penerbit).strip`, `int`, `str(isbn).strip`, `str(deskripsi).strip` dan lainnya.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(sukses, errors)`.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, mengubah atau membaca status sesi/autentikasi, membaca/menulis berkas. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/utils/kartu.py`

Berkas utilitas berisi logika yang dipakai ulang oleh route atau komponen lain.

### `validasi_nim` — `Website/utils/kartu.py:9–35`

**Docstring sumber:** Validasi NIM. Kembalikan (nim_bersih_atau_None, pesan_error_atau_None).

- wajib=True  : NIM harus diisi (dipakai untuk mahasiswa).
- wajib=False : boleh kosong (staf / kepala perpustakaan) -> dikembalikan None.
- Harus berupa angka dengan panjang antara Config.NIM_PANJANG_MIN dan
  Config.NIM_PANJANG_MAKS (default 8-12 digit).
- Harus unik di seluruh pengguna (abaikan_user_id dipakai saat edit).

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `nim`, `wajib`, `abaikan_user_id`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `nim = (nim or '').strip()` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if not nim`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Percabangan `if wajib`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **`return (None, 'NIM wajib diisi.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

  - **`return (None, None)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `p_min = current_app.config['NIM_PANJANG_MIN']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Penyimpanan nilai**: `p_maks = current_app.config['NIM_PANJANG_MAKS']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if not nim.isdigit() or not p_min <= len(nim) <= p_maks`**: bila kondisi benar, jalankan 2 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `rentang = f'{p_min}' if p_min == p_maks else f'{p_min}-{p_maks}'` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **`return (None, f'NIM harus berupa {rentang} digit angka.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `q = User.query.filter(User.nim == nim)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if abaikan_user_id`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **Penyimpanan nilai**: `q = q.filter(User.id != abaikan_user_id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if q.first()`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return (None, 'NIM sudah terdaftar pada pengguna lain.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return (nim, None)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `(nim or '').strip`, `User.query.filter`, `q.first`, `q.filter`, `nim.isdigit`, `len`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(nim, None)`, `(None, None)`, `(None, f'NIM harus berupa {rentang} digit angka.')`, `(None, 'NIM sudah terdaftar pada pengguna lain.')`, `(None, 'NIM wajib diisi.')`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `terbitkan_kartu_jika_belum_ada` — `Website/utils/kartu.py:38–51`

**Docstring sumber:** Terbitkan kartu perpustakaan digital untuk user manapun (semua role)
jika belum punya. ID kartu = NIM milik user (users.nim).

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `user`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if user.kartu`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return user.kartu`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `kartu = KartuAnggota(user_id=user.id, tanggal_terbit=date.today(), tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config['MASA_BERLAKU_KARTU_HARI']), status='aktif')` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Efek/prosedur**: `db.session.add(kartu)` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **`return kartu`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `KartuAnggota`, `db.session.add`, `db.session.commit`, `date.today`, `timedelta`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `kartu`, `user.kartu`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/utils/pengaturan.py`

Berkas utilitas berisi logika yang dipakai ulang oleh route atau komponen lain.

### `terapkan_pengaturan` — `Website/utils/pengaturan.py:32–44`

**Docstring sumber:** Salin pengaturan dari DB ke app.config. Aman dipanggil sebelum tabel dibuat.

**Tujuan dan peran.** Fungsi ini menjalankan tanggung jawab yang ditentukan oleh nama dan isi fungsi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `app`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penanganan pengecualian (`try/except`)**: menjalankan proses utama dan menangani error yang sesuai.

  - **Penyimpanan nilai**: `baris = {r.kunci: r.nilai for r in Pengaturan.query.all()}` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Efek/prosedur**: `db.session.rollback()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

  - **`return None`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Perulangan** (`(kunci, kunci_config, *_) melalui DAFTAR`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Percabangan `if kunci in baris`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **Penanganan pengecualian (`try/except`)**: menjalankan proses utama dan menangani error yang sesuai.

      - **Penyimpanan nilai**: `app.config[kunci_config] = int(baris[kunci])` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

      - **Pernyataan**: `pass`.

**Fungsi/metode yang dipanggil.** `db.session.rollback`, `Pengaturan.query.all`, `int`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `None`.

**Efek samping yang perlu diperhatikan.** mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `nilai_saat_ini` — `Website/utils/pengaturan.py:47–49`

**Docstring sumber:** Dict {kunci_db: nilai} yang sedang berlaku, untuk mengisi form Pengaturan.

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `app`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return {kunci: app.config[kunci_config] for kunci, kunci_config, *_ in DAFTAR}`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `{kunci: app.config[kunci_config] for kunci, kunci_config, *_ in DAFTAR}`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `simpan_pengaturan` — `Website/utils/pengaturan.py:52–60`

**Docstring sumber:** Simpan dict {kunci_db: int} ke tabel pengaturan (insert atau update).

**Tujuan dan peran.** Fungsi ini menjalankan aksi/perubahan data atau alur aplikasi. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `data`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Perulangan** (`(kunci, nilai) melalui data.items()`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `baris = db.session.get(Pengaturan, kunci)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if baris`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama. Jika tidak, jalankan cabang alternatif (1 pernyataan).

    - **Penyimpanan nilai**: `baris.nilai = str(nilai)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

    **Alternatif (`else`/`elif`):**

    - **Efek/prosedur**: `db.session.add(Pengaturan(kunci=kunci, nilai=str(nilai)))` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

- **Efek/prosedur**: `db.session.commit()` — menjalankan operasi yang memengaruhi database, sesi, respons web, atau alur pengguna.

**Fungsi/metode yang dipanggil.** `data.items`, `db.session.commit`, `db.session.get`, `str`, `db.session.add`, `Pengaturan`.

**Keluaran.** Tidak ada `return` eksplisit; pemanggil menerima `None` kecuali ada perilaku khusus dari framework/dekorator.

**Efek samping yang perlu diperhatikan.** kemungkinan perubahan database/transaksi, mengubah atau membaca status sesi/autentikasi. Pastikan efek ini sesuai izin pengguna dan transaksi yang diharapkan.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

## Berkas `Website/utils/pinjam.py`

Berkas utilitas berisi logika yang dipakai ulang oleh route atau komponen lain.

### `lama_pinjam_untuk` — `Website/utils/pinjam.py:10–16`

**Docstring sumber:** Tentukan lama pinjam (hari): isian petugas > pengaturan khusus buku > pengaturan umum.

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku`, `lama_hari`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if lama_hari and lama_hari > 0`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return lama_hari`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if buku is not None and buku.lama_pinjam_hari`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return buku.lama_pinjam_hari`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return current_app.config['LAMA_PINJAM_HARI']`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `current_app.config['LAMA_PINJAM_HARI']`, `lama_hari`, `buku.lama_pinjam_hari`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `hitung_jatuh_tempo` — `Website/utils/pinjam.py:19–20`

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `buku`, `mulai`, `lama_hari`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **`return mulai + timedelta(days=lama_pinjam_untuk(buku, lama_hari))`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `timedelta`, `lama_pinjam_untuk`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `mulai + timedelta(days=lama_pinjam_untuk(buku, lama_hari))`.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `cek_tunggakan` — `Website/utils/pinjam.py:23–46`

**Docstring sumber:** Jika pengaturan 'blokir jika ada denda' aktif: mahasiswa dengan buku terlambat
atau denda belum lunas tidak boleh meminjam lagi.

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `mahasiswa`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Percabangan `if not current_app.config['BLOKIR_JIKA_DENDA']`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return (True, None)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `telat = [p for p in Peminjaman.query.filter_by(user_id=mahasiswa.id, status='dipinjam').all() if p.hari_telat > 0]` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if telat`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return (False, f'Masih ada {len(telat)} buku yang terlambat dikembalikan (denda berjalan {format_rupiah(sum((denda_peminjaman(p) for p in telat)))}). Kembalikan buku tersebut terlebih dahulu.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Penyimpanan nilai**: `belum_lunas = total_denda_belum_lunas(mahasiswa.id)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if belum_lunas > 0`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return (False, f'Ada denda belum lunas sebesar {format_rupiah(belum_lunas)}. Lunasi denda di perpustakaan terlebih dahulu.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return (True, None)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `total_denda_belum_lunas`, `Peminjaman.query.filter_by(user_id=mahasiswa.id, status='dipinjam').all`, `Peminjaman.query.filter_by`, `len`, `format_rupiah`, `sum`, `denda_peminjaman`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(True, None)`, `(False, f'Masih ada {len(telat)} buku yang terlambat dikembalikan (denda berjalan {format_rupiah(sum((denda_peminjaman(p) for p in telat)))}). Kembalikan buku tersebut terlebih dahulu.')`, `(False, f'Ada denda belum lunas sebesar {format_rupiah(belum_lunas)}. Lunasi denda di perpustakaan terlebih dahulu.')`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `cek_kartu_valid` — `Website/utils/pinjam.py:49–60`

**Docstring sumber:** Kartu perpustakaan harus aktif dan belum kadaluarsa untuk bisa meminjam.
Kembalikan (True, None) atau (False, pesan).

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `mahasiswa`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `kartu = terbitkan_kartu_jika_belum_ada(mahasiswa)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if kartu.status != 'aktif'`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return (False, 'Kartu perpustakaan tidak aktif. Hubungi staf/kepala perpustakaan.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **Percabangan `if kartu.is_kadaluarsa`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return (False, f"Kartu perpustakaan sudah kadaluarsa pada {kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y')}. Minta staf/kepala perpustakaan untuk memperpanjang.")`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return (True, None)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `terbitkan_kartu_jika_belum_ada`, `kartu.tanggal_kadaluarsa.strftime`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(True, None)`, `(False, 'Kartu perpustakaan tidak aktif. Hubungi staf/kepala perpustakaan.')`, `(False, f"Kartu perpustakaan sudah kadaluarsa pada {kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y')}. Minta staf/kepala perpustakaan untuk memperpanjang.")`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `cek_kuota_pinjam` — `Website/utils/pinjam.py:63–71`

**Docstring sumber:** Maksimal Config.MAKS_PINJAM_PER_USER buku (diajukan + dipinjam) per mahasiswa.

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `mahasiswa`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Penyimpanan nilai**: `maks = current_app.config['MAKS_PINJAM_PER_USER']` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

- **Percabangan `if mahasiswa.jumlah_pinjaman_aktif >= maks`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

  - **`return (False, f'Batas peminjaman tercapai: maksimal {maks} buku per mahasiswa (termasuk pengajuan yang masih menunggu). Kembalikan salah satu buku terlebih dahulu.')`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return (True, None)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(True, None)`, `(False, f'Batas peminjaman tercapai: maksimal {maks} buku per mahasiswa (termasuk pengajuan yang masih menunggu). Kembalikan salah satu buku terlebih dahulu.')`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.

### `cek_bisa_meminjam` — `Website/utils/pinjam.py:74–80`

**Docstring sumber:** Gabungan validasi kartu + tunggakan denda + kuota. Kembalikan (True, None) atau (False, pesan).

**Tujuan dan peran.** Fungsi ini membaca, menghitung, memvalidasi, atau menyiapkan data. Nama parameter menunjukkan input yang diterima; detail arti parameter ditafsirkan dari penggunaannya di badan fungsi dan konteks modul.

**Input/parameter.** `mahasiswa`. Nilai default/tipe mengikuti definisi pada kode sumber.

**Alur kerja.**

- **Perulangan** (`cek melalui (cek_kartu_valid, cek_tunggakan, cek_kuota_pinjam)`): menjalankan blok berulang untuk memproses item atau sampai kondisi berhenti.

  - **Penyimpanan nilai**: `(ok, pesan) = cek(mahasiswa)` — menyimpan hasil ekspresi ke variabel/atribut tujuan.

  - **Percabangan `if not ok`**: bila kondisi benar, jalankan 1 pernyataan di cabang utama.

    - **`return (False, pesan)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

- **`return (True, None)`**: mengakhiri fungsi dan mengembalikan nilai tersebut kepada pemanggil.

**Fungsi/metode yang dipanggil.** `cek`.

**Keluaran.** Jalur fungsi dapat mengembalikan: `(True, None)`, `(False, pesan)`. Nilai yang benar-benar dikembalikan bergantung pada cabang kondisi yang dilalui.

**Cara memahami/menguji fungsi.** Telusuri pemanggil fungsi ini, berikan input valid, lalu uji input kosong/tidak valid serta kondisi tiap percabangan. Untuk fungsi yang mengubah data, uji pada database pengembangan dan periksa hasil akhirnya.


# BAGIAN VII --- CHECKLIST PEMAHAMAN KODE

Gunakan checklist ini setelah membaca katalog fungsi.

-   [ ] Saya bisa menjelaskan bagaimana `create_app()` membangun
    aplikasi Flask.
-   [ ] Saya paham perbedaan route (`routes/`), model (`models.py`), dan
    utilitas (`utils/`).
-   [ ] Saya bisa mengikuti data dari `request.form`/`request.args`
    sampai validasi dan query database.
-   [ ] Saya paham kapan `db.session.add()`, `delete()`, `commit()`, dan
    `rollback()` dipakai.
-   [ ] Saya bisa membedakan `render_template()`, `redirect()`,
    `flash()`, dan `abort()`.
-   [ ] Saya bisa menjelaskan status peminjaman dan perubahan stok dari
    pengajuan hingga pengembalian.
-   [ ] Saya tahu bahwa penjelasan kode bukan pengganti pengujian
    keamanan dan pengujian alur aplikasi.


# BAGIAN VIII — PANDUAN MEMBANGUN ULANG APLIKASI DARI NOL

Bab ini merupakan urutan implementasi yang dapat diikuti untuk membuat aplikasi sejenis. Agar hasilnya sama dengan proyek sumber, gunakan listing pada Lampiran C dan jangan mengganti nama kolom, endpoint, atau fungsi tanpa memperbarui pemanggilnya.

## 22. Persiapan lingkungan

1. Pasang Python versi yang kompatibel dengan dependensi proyek dan MySQL Server.
2. Buat folder kerja, misalnya `Perpus-STIKOM/Website`.
3. Buat virtual environment dari folder `Website`: `python -m venv .venv`.
4. Aktifkan environment di Windows: `.venv\\Scripts\\activate`; di Linux/macOS: `source .venv/bin/activate`.
5. Instal dependensi: `pip install -r requirements.txt`.
6. Buat database MySQL, lalu impor `Website/schema.sql` atau `Database/schema.sql`. Pastikan struktur yang dipakai sesuai dengan konfigurasi aplikasi.
7. Buat file `.env` lokal berdasarkan variabel yang dibaca `config.py`; jangan menyalin kredensial dari arsip atau memasukkan rahasia ke Git.

## 23. Urutan implementasi yang disarankan

### Tahap A — Konfigurasi dan ekstensi

Buat `config.py` untuk membaca environment dan menyimpan konfigurasi aplikasi. Buat `extensions.py` untuk objek ekstensi SQLAlchemy dan Flask-Login tanpa mengikatnya ke aplikasi terlalu awal. Pola ini memungkinkan ekstensi diinisialisasi melalui `init_app(app)`.

**Selesai jika:** aplikasi dapat membaca konfigurasi tanpa menampilkan password, dan modul ekstensi dapat diimpor tanpa circular import.

### Tahap B — Model dan skema database

1. Definisikan tabel sesuai `schema.sql` pada `models.py`.
2. Cocokkan nama tabel, nama kolom, tipe, nullable, default, primary key, foreign key, dan unique constraint.
3. Tambahkan relasi ORM hanya jika cocok dengan foreign key sebenarnya.
4. Tambahkan metode model untuk aturan yang memang menjadi tanggung jawab entitas, misalnya pemeriksaan hash kata sandi.
5. Jalankan pemeriksaan database dan uji satu operasi baca/tulis di database pengembangan.

**Selesai jika:** model dapat diimpor dan query sederhana berjalan tanpa error tabel/kolom. Jangan mengandalkan `create_all()` untuk menggantikan migrasi skema yang sudah ada.

### Tahap C — Factory/inti aplikasi

1. Buat aplikasi Flask di `app.py`.
2. Muat konfigurasi.
3. Inisialisasi `db` dan `login_manager`.
4. Daftarkan user loader untuk mengambil pengguna dari ID sesi.
5. Daftarkan blueprint route satu per satu.
6. Daftarkan filter template, error handler, dan fungsi konteks jika dipakai.
7. Jalankan aplikasi hanya melalui entry point yang ditentukan proyek.

**Selesai jika:** server dapat menyala dan route halaman awal merespons tanpa exception.

### Tahap D — Autentikasi dan otorisasi

Implementasikan login, logout, registrasi, persetujuan akun, dan pengelolaan pengguna pada `routes/auth.py`. Gunakan hash kata sandi, bukan teks asli. Gunakan dekorator role di `utils/decorators.py` pada route yang membutuhkan hak khusus. Setiap route perubahan data perlu memvalidasi input server-side; menyembunyikan tombol pada HTML saja bukan kontrol akses.

**Uji minimal:** login berhasil/gagal, akun menunggu persetujuan, logout, pengguna tanpa sesi, dan role yang tidak berwenang mengakses URL langsung.

### Tahap E — Fitur inti

Implementasikan route berdasarkan urutan ketergantungan berikut:

1. **Buku dan kategori** (`routes/buku.py`): daftar, detail, tambah/edit/hapus, sampul, impor Excel.
2. **Aturan peminjaman** (`utils/pinjam.py`): masa pinjam, validitas kartu, kuota, tunggakan, jatuh tempo.
3. **Peminjaman** (`routes/peminjaman.py`): pengajuan, persetujuan, pinjam langsung, pengembalian, perpanjangan, riwayat. Pastikan perubahan stok dan status peminjaman terjadi secara konsisten dalam transaksi.
4. **Denda** (`utils/denda.py`, `routes/denda.py`): hitung nominal, status lunas/belum lunas, pembayaran, ekspor.
5. **Kartu anggota** (`utils/kartu.py`, `routes/kartu.py`): validasi identitas, penerbitan, penonaktifan, tampilan/cetak.
6. **Dashboard dan laporan** (`routes/dashboard.py`, `routes/laporan.py`): query agregasi, filter, grafik, dan ekspor Excel.
7. **Pengaturan** (`utils/pengaturan.py`, `routes/pengaturan.py`): nilai default, baca/simpan pengaturan, penerapan ke aplikasi.

Setiap tahap harus punya uji route untuk pengguna berhak dan tidak berhak, input valid/tidak valid, serta hasil database.

### Tahap F — Template dan antarmuka

1. Buat `templates/layout/base.html` sebagai kerangka bersama.
2. Pastikan setiap halaman memperluas base template dan mengisi blok yang benar.
3. Buat template per fitur sesuai struktur direktori.
4. Gunakan `url_for()` untuk URL internal agar perubahan route tidak membuat tautan statis rusak.
5. Terapkan CSS utama pada `static/css/style.css`, lalu aturan responsif pada `static/css/mobile.css`.
6. Jika memakai Chart.js dari CDN, sediakan tampilan fallback saat CDN gagal atau koneksi internet tidak tersedia.
7. Uji tampilan desktop dan layar sempit, serta status kosong/error/sukses pada setiap halaman.

### Tahap G — Impor/ekspor Excel

Pisahkan logika workbook ke `utils/excel_import.py` dan `utils/excel_export.py`. Validasi format file, nama kolom, nilai wajib, tipe angka/tanggal, dan batas ukuran. Saat impor, kumpulkan error per baris dan jangan menyimpan sebagian data tanpa aturan yang jelas. Saat ekspor, pastikan kolom yang dihasilkan sesuai filter yang ditampilkan di halaman.

### Tahap H — Data awal dan menjalankan aplikasi

Gunakan `seed_admin.py` untuk membuat akun kepala pertama sesuai implementasi proyek. Jalankan hanya sekali atau pastikan skrip aman dijalankan berulang. Setelah database, konfigurasi, dan dependensi siap, jalankan perintah yang dipakai proyek (`run.bat` pada Windows atau entry point Flask yang sesuai).

## 24. Checklist pengujian penerimaan

- [ ] Aplikasi dapat dimulai dari environment bersih mengikuti instruksi instalasi.
- [ ] Login, logout, dan pemulihan status sesi bekerja.
- [ ] Setiap role hanya dapat mengakses route yang diizinkan.
- [ ] CRUD buku/kategori dan unggah sampul bekerja.
- [ ] Impor Excel menolak data salah dan menjelaskan kesalahan.
- [ ] Pengajuan, persetujuan, peminjaman, pengembalian, dan perpanjangan menjaga konsistensi stok.
- [ ] Denda, pembayaran, dan status lunas diuji dengan tanggal batas yang jelas.
- [ ] Kartu nonaktif tidak dapat dipakai untuk meminjam.
- [ ] Laporan dan file Excel mengikuti filter yang dipilih.
- [ ] Semua form tervalidasi di server dan dilindungi CSRF jika menggunakan autentikasi berbasis sesi.
- [ ] Tidak ada rahasia di Git/arsip distribusi; error produksi tidak membocorkan traceback atau kredensial.
- [ ] Uji backup dan pemulihan database.

## 25. Batasan reproduksi dari dokumentasi

Dokumentasi dan listing sumber dapat menjadi acuan rekonstruksi, tetapi hasil identik tetap membutuhkan versi Python/MySQL/dependensi yang sesuai, konfigurasi environment lokal, data database, dan pengujian. File `.env` sengaja tidak dicetak ke lampiran karena dapat berisi kredensial. Rahasia harus dibuat ulang oleh pengelola lingkungan.

# LAMPIRAN C — LISTING SUMBER PROYEK\n\nListing berikut disertakan agar pembaca dapat menyalin kode yang diperlukan tanpa bergantung pada arsip ZIP. Berkas rahasia `.env`, folder virtual environment, dan data kredensial tidak disertakan. File media biner seperti logo dan workbook data tidak ditampilkan sebagai teks; gunakan file aset dari paket proyek atau ganti dengan aset yang sah.\n

## `Database/schema.sql`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```sql
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
    -- NISN (10 digit) = ID kartu perpustakaan. Wajib untuk mahasiswa (divalidasi di aplikasi),
    -- boleh NULL untuk staf/kepala perpustakaan.
    nisn VARCHAR(20) DEFAULT NULL UNIQUE,
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
-- TABEL KARTU ANGGOTA (kartu perpus digital, 1-1 dengan user; ID kartu = users.nisn)
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (buku_id) REFERENCES buku(id) ON DELETE CASCADE,
    FOREIGN KEY (diproses_oleh) REFERENCES users(id) ON DELETE SET NULL
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
```


## `Informasi/Teknis.md`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```markdown
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
```


## `README.md`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```markdown
# Perpus-STIKOM
Software perpustakan STIKOM

# Kebutuhan
-Software dibuat kedalam bentuk? :
Website/Aplikasi

-Software diakses secara? :
Offline/Online

-Software diakses lewat? :
Mobile/Desktop/Keduanya

-Software hanya boleh dipakai? :
Staf/Mahasiswa/Keduanya

# Fitur

-Sistem peminjaman dan pengembalian buku
-Sistem dateline
-Sistem pencarian buku
-Sistem statistik/laporan buku populer
-Sistem statistik/laporan buku tidak populer
-Sistem 3 role (user, staf, operator)
-Sistem kartu perpus
-Sistem riwayat peserta/buku
-Sistem login dan registrasi
-Sistem manajemen buku (stok buku, informasi buku, kategori, dsb)
-Sistem upload sampul buku ke database
-Sistem pembuatan format excel jadi tinggal dimasukan data buku nya dari situ terus ketika di uploud bakalan masuk ke database sql
```


## `Website/app.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
import os
from datetime import date
from flask import Flask
from config import Config
from extensions import db, login_manager
from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Jadikan UPLOAD_FOLDER path absolut (relatif terhadap lokasi project),
    # bukan relatif terhadap folder tempat perintah dijalankan — supaya file
    # yang disimpan selalu berada di folder yang sama dengan yang disajikan
    # oleh endpoint /static, di komputer/OS manapun.
    if not os.path.isabs(app.config["UPLOAD_FOLDER"]):
        app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])

    # pastikan folder upload ada
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ---- Pengaturan dari database + helper tampilan denda ----
    from utils.pengaturan import terapkan_pengaturan
    from utils.denda import denda_peminjaman, format_rupiah
    from flask import request

    @app.before_request
    def muat_pengaturan():
        # Salin pengaturan (lama pinjam, tarif denda, dst.) dari DB ke app.config.
        if request.endpoint != "static":
            terapkan_pengaturan(app)

    app.jinja_env.filters["rupiah"] = format_rupiah
    app.jinja_env.globals["denda_sekarang"] = denda_peminjaman

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_jumlah_pending_akun():
        # Dipakai navbar untuk menampilkan badge jumlah akun yang menunggu
        # persetujuan. Hanya dihitung untuk kepala perpustakaan yang sedang login agar
        # tidak membebani query di halaman lain / role lain.
        from flask_login import current_user
        if current_user.is_authenticated and current_user.is_kepala:
            jumlah = User.query.filter_by(role="mahasiswa", status_akun="pending").count()
        else:
            jumlah = 0
        return {"jumlah_pending_akun": jumlah}

    @app.context_processor
    def inject_jumlah_pengajuan_peminjaman():
        # Dipakai navbar/sidebar untuk menampilkan badge jumlah pengajuan
        # peminjaman yang menunggu ditinjau. Hanya dihitung untuk staf/kepala perpustakaan.
        from flask_login import current_user
        from models import Peminjaman
        if current_user.is_authenticated and (current_user.is_staf or current_user.is_kepala):
            jumlah = Peminjaman.query.filter_by(status="diajukan").count()
        else:
            jumlah = 0
        return {"jumlah_pengajuan_peminjaman": jumlah}

    @app.context_processor
    def inject_tahun_sekarang():
        # Dipakai footer untuk tahun copyright, dihitung otomatis
        # (sebelumnya ditulis angka tetap "2026" di template).
        return {"tahun_sekarang": date.today().year}

    # ---- registrasi blueprint ----
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.buku import buku_bp
    from routes.peminjaman import peminjaman_bp
    from routes.laporan import laporan_bp
    from routes.kartu import kartu_bp
    from routes.denda import denda_bp
    from routes.pengaturan import pengaturan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(buku_bp)
    app.register_blueprint(peminjaman_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(kartu_bp)
    app.register_blueprint(denda_bp)
    app.register_blueprint(pengaturan_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
```


## `Website/config.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME")	

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads/sampul")
    ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_EXCEL_EXT = {"xlsx"}

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5")) * 1024 * 1024

    # ---- NILAI AWAL PENGATURAN ----
    # Nilai di bawah hanya cadangan/awal. Kepala perpustakaan bisa mengubahnya
    # kapan saja lewat menu Pengaturan (tersimpan di tabel `pengaturan`).

    # Batas hari peminjaman default
    LAMA_PINJAM_HARI = 7

    # Batas maksimal buku yang boleh dipinjam/diajukan sekaligus per mahasiswa
    # (pengajuan yang menunggu persetujuan ikut dihitung).
    MAKS_PINJAM_PER_USER = 2

    # Panjang NIM (Nomor Induk Mahasiswa) yang diterima, dalam jumlah digit angka.
    # Format NIM berbeda-beda antar kampus; sesuaikan rentang ini dengan format
    # NIM kampus Anda (mis. jika NIM selalu 10 digit, isi keduanya dengan 10).
    NIM_PANJANG_MIN = 8
    NIM_PANJANG_MAKS = 12

    # Lama masa berlaku kartu perpustakaan (hari) saat diterbitkan / diperpanjang
    MASA_BERLAKU_KARTU_HARI = 365

    # Jumlah hari sebelum jatuh tempo untuk mulai menampilkan peringatan
    # "akan jatuh tempo" ke mahasiswa & staf/kepala perpustakaan.
    PERINGATAN_JATUH_TEMPO_HARI = 3

    # ---- DENDA KETERLAMBATAN ----
    DENDA_PER_HARI = 1000        # Rp per hari keterlambatan
    DENDA_MAKS = 0               # batas atas denda per buku (Rp); 0 = tanpa batas
    MASA_TENGGANG_HARI = 0       # hari gratis setelah jatuh tempo sebelum denda dihitung
    BLOKIR_JIKA_DENDA = 1        # 1 = mahasiswa dgn denda/keterlambatan tak bisa meminjam lagi

    # ---- MANAJEMEN BUKU ----
    MAKS_PERPANJANG = 2          # berapa kali jatuh tempo boleh diperpanjang

    # Daftar domain email yang dianggap valid saat registrasi/tambah pengguna
    # (tanpa perlu sistem verifikasi OTP). Silakan tambahkan domain kampus
    # resmi di sini jika sudah tersedia, mis. "stikomkendari.ac.id".
    ALLOWED_EMAIL_DOMAINS = [
        "gmail.com",
        "yahoo.com",
        "yahoo.co.id",
        "outlook.com",
        "hotmail.com",
        "live.com",
        "icloud.com",
        "proton.me",
        "protonmail.com",
    ]
```


## `Website/extensions.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Silakan login terlebih dahulu untuk mengakses halaman ini."
login_manager.login_message_category = "warning"
```


## `Website/models.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
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
    # NIM (Nomor Induk Mahasiswa). Wajib untuk mahasiswa; opsional untuk staf/kepala perpustakaan.
    # NIM inilah yang dipakai sebagai nomor/ID kartu perpustakaan.
    nim = db.Column(db.String(20), unique=True, nullable=True)
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
    def nim(self):
        """ID kartu = NIM pemilik kartu (satu sumber data: users.nim)."""
        return self.pemilik.nim

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
    # Lokasi fisik buku di rak (mis. "Rak A-3") - membantu staf mencari buku.
    lokasi_rak = db.Column(db.String(50))
    # Lama pinjam khusus buku ini (hari). Kosong = ikut pengaturan umum.
    lama_pinjam_hari = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    peminjaman_list = db.relationship("Peminjaman", backref="buku", cascade="all, delete-orphan")
    log_stok_list = db.relationship("LogStok", backref="buku", cascade="all, delete-orphan")

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

    # ---- Denda keterlambatan ----
    # 'denda' baru diisi (dibekukan) saat buku dikembalikan. Selama masih dipinjam,
    # denda dihitung berjalan lewat utils.denda.denda_peminjaman().
    denda = db.Column(db.Integer, nullable=False, default=0)
    # 'tidak_ada' -> tidak ada denda | 'belum_lunas' -> menunggu dibayar
    # 'lunas' -> sudah dibayar | 'dibebaskan' -> dihapus oleh kepala perpustakaan
    status_denda = db.Column(
        db.Enum("tidak_ada", "belum_lunas", "lunas", "dibebaskan", name="status_denda_enum"),
        nullable=False,
        default="tidak_ada",
    )
    tanggal_denda_selesai = db.Column(db.Date)   # tanggal dibayar / dibebaskan
    denda_diproses_oleh = db.Column(db.Integer, db.ForeignKey("users.id"))
    catatan_denda = db.Column(db.String(255))
    # Berapa kali jatuh tempo sudah diperpanjang.
    jumlah_perpanjang = db.Column(db.Integer, nullable=False, default=0)

    @property
    def hari_telat(self):
        """Jumlah hari melewati jatuh tempo (0 jika belum/tidak telat)."""
        if self.status == "dikembalikan" and self.tanggal_kembali:
            akhir = self.tanggal_kembali
        elif self.status == "dipinjam":
            akhir = date.today()
        else:
            return 0
        return max(0, (akhir - self.tanggal_jatuh_tempo).days)

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


class Pengaturan(db.Model):
    """Pengaturan perpustakaan (key-value) yang bisa diubah kepala perpustakaan
    lewat halaman Pengaturan: lama pinjam, tarif denda, dsb."""
    __tablename__ = "pengaturan"

    kunci = db.Column(db.String(50), primary_key=True)
    nilai = db.Column(db.String(100), nullable=False)


class LogStok(db.Model):
    """Catatan setiap perubahan stok manual (tambah stok, buku rusak/hilang, dll.)."""
    __tablename__ = "log_stok"

    id = db.Column(db.Integer, primary_key=True)
    buku_id = db.Column(db.Integer, db.ForeignKey("buku.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    perubahan = db.Column(db.Integer, nullable=False)       # + tambah / - kurang
    stok_sesudah = db.Column(db.Integer, nullable=False)
    alasan = db.Column(db.String(100), nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)  # waktu lokal komputer server

    petugas = db.relationship("User", foreign_keys=[user_id])
```


## `Website/requirements.txt`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```text
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
mysql-connector-python==8.4.0
python-dotenv==1.0.1
openpyxl==3.1.5
Werkzeug==3.0.3
```


## `Website/routes/__init__.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python

```


## `Website/routes/auth.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from datetime import date, timedelta

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User, KartuAnggota, Peminjaman
from utils.decorators import role_required
from utils.kartu import validasi_nim, terbitkan_kartu_jika_belum_ada as _terbitkan_kartu_jika_belum_ada

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _email_domain_valid(email):
    """Cek domain email terhadap Config.ALLOWED_EMAIL_DOMAINS.
    (Sebelumnya daftar ini ada di config.py tapi tidak pernah dipakai/divalidasi.)"""
    from flask import current_app
    domain = email.rsplit("@", 1)[-1].lower() if "@" in email else ""
    allowed = current_app.config.get("ALLOWED_EMAIL_DOMAINS") or []
    return domain in allowed


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Registrasi publik HANYA untuk role 'mahasiswa', dan HARUS lewat
    # persetujuan kepala perpustakaan dulu sebelum bisa login (status_akun='pending').
    # Akun staf/kepala perpustakaan dibuat oleh kepala perpustakaan lewat menu manajemen pengguna,
    # dan otomatis langsung 'disetujui' (lihat tambah_pengguna()).
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        nim_input = request.form.get("nim", "")
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")

        if not all([username, email, nama_lengkap, password]):
            flash("Semua field wajib diisi.", "danger")
            return redirect(url_for("auth.register"))

        if password != password2:
            flash("Konfirmasi password tidak cocok.", "danger")
            return redirect(url_for("auth.register"))

        if len(password) < 6:
            flash("Password minimal 6 karakter.", "danger")
            return redirect(url_for("auth.register"))

        if not _email_domain_valid(email):
            flash("Domain email tidak diizinkan. Gunakan email pribadi yang umum (gmail, yahoo, outlook, dsb).", "danger")
            return redirect(url_for("auth.register"))

        nim, err = validasi_nim(nim_input, wajib=True)
        if err:
            flash(err, "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            nama_lengkap=nama_lengkap,
            nim=nim,
            role="mahasiswa",
            status_akun="pending",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Catatan: kartu anggota digital SENGAJA belum dibuat di sini.
        # Kartu baru diterbitkan otomatis saat kepala perpustakaan menyetujui akun
        # (lihat setujui_pengguna()), supaya masa berlaku kartu dihitung
        # sejak tanggal disetujui, bukan sejak tanggal daftar.

        flash(
            "Registrasi berhasil! Akun Anda akan aktif setelah disetujui "
            "oleh kepala perpustakaan. Silakan cek kembali nanti.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Login bisa memakai USERNAME atau NIM. Username dicocokkan lebih dulu;
        # jika tidak ada yang cocok, baru dicoba sebagai NIM (NIM bersifat unik).
        user = User.query.filter_by(username=username).first()
        if user is None and username:
            user = User.query.filter_by(nim=username).first()
        if user and user.check_password(password):
            if user.menunggu_persetujuan:
                flash(
                    "Akun Anda masih menunggu persetujuan kepala perpustakaan. "
                    "Silakan coba login lagi nanti.",
                    "warning",
                )
                return redirect(url_for("auth.login"))
            if user.ditolak_operator:
                flash(
                    "Registrasi akun Anda ditolak oleh kepala perpustakaan. "
                    "Hubungi kepala perpustakaan untuk informasi lebih lanjut.",
                    "danger",
                )
                return redirect(url_for("auth.login"))
            if not user.is_active_db:
                flash("Akun Anda dinonaktifkan. Hubungi kepala perpustakaan.", "danger")
                return redirect(url_for("auth.login"))
            login_user(user)
            flash(f"Selamat datang, {user.nama_lengkap}!", "success")
            return redirect(url_for("dashboard.index"))
        flash("Username/NIM atau password salah.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("auth.login"))


# ------------------------------------------------------------------
# Manajemen pengguna (khusus kepala perpustakaan) - membuat akun staf/kepala perpustakaan
# ------------------------------------------------------------------
@auth_bp.route("/pengguna")
@login_required
@role_required("kepala_perpustakaan")
def daftar_pengguna():
    pengguna = User.query.order_by(User.created_at.desc()).all()
    return render_template("auth/daftar_pengguna.html", pengguna=pengguna)


@auth_bp.route("/pengguna/tambah", methods=["GET", "POST"])
@login_required
@role_required("kepala_perpustakaan")
def tambah_pengguna():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "staf")
        nim_input = request.form.get("nim", "")

        if role not in ("mahasiswa", "staf", "kepala_perpustakaan"):
            flash("Role tidak valid.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        if len(password) < 6:
            flash("Password minimal 6 karakter.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        # NIM wajib untuk mahasiswa, opsional untuk staf / kepala perpustakaan
        nim, err = validasi_nim(nim_input, wajib=(role == "mahasiswa"))
        if err:
            flash(err, "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        if not _email_domain_valid(email):
            flash("Domain email tidak diizinkan. Gunakan email pribadi yang umum (gmail, yahoo, outlook, dsb).", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        # BUG LAMA: dulu hanya username yang dicek duplikatnya di sini, email
        # tidak dicek sama sekali -> submit email yang sudah dipakai bikin
        # server error 500 (UNIQUE constraint gagal di database).
        if User.query.filter_by(email=email).first():
            flash("Email sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.tambah_pengguna"))

        # Dibuat langsung oleh kepala perpustakaan -> otomatis dianggap terverifikasi,
        # tidak perlu melalui alur persetujuan seperti registrasi mandiri.
        user = User(
            username=username, email=email, nama_lengkap=nama_lengkap,
            nim=nim, role=role, status_akun="disetujui",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Kartu perpustakaan digital sekarang diterbitkan untuk SEMUA role
        # (mahasiswa, staf, maupun kepala perpustakaan), bukan cuma mahasiswa.
        kartu = KartuAnggota(
            user_id=user.id,
            tanggal_terbit=date.today(),
            tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config["MASA_BERLAKU_KARTU_HARI"]),
            status="aktif",
        )
        db.session.add(kartu)

        db.session.commit()
        flash(f"Pengguna '{username}' ({role}) berhasil dibuat.", "success")
        return redirect(url_for("auth.daftar_pengguna"))

    return render_template("auth/tambah_pengguna.html")


@auth_bp.route("/pengguna/<int:user_id>/toggle-aktif", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def toggle_aktif_pengguna(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Anda tidak bisa menonaktifkan akun sendiri.", "warning")
        return redirect(url_for("auth.daftar_pengguna"))
    user.is_active_db = not user.is_active_db
    db.session.commit()
    status = "diaktifkan" if user.is_active_db else "dinonaktifkan"
    flash(f"Akun '{user.username}' berhasil {status}.", "success")
    return redirect(url_for("auth.daftar_pengguna"))


@auth_bp.route("/pengguna/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("kepala_perpustakaan")
def edit_pengguna(user_id):
    # Edit akun sendiri diarahkan ke halaman "Profil Saya" (self-service),
    # supaya kepala perpustakaan tidak bisa tanpa sadar mengubah role/status akunnya sendiri
    # lewat form manajemen pengguna ini.
    if user_id == current_user.id:
        flash("Gunakan halaman 'Profil Saya' untuk mengedit akun Anda sendiri.", "info")
        return redirect(url_for("auth.profil"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        no_telepon = request.form.get("no_telepon", "").strip()
        alamat = request.form.get("alamat", "").strip()
        role = request.form.get("role", user.role)
        nim_input = request.form.get("nim", "")
        password_baru = request.form.get("password", "")
        password_baru2 = request.form.get("password2", "")

        if not all([username, email, nama_lengkap]):
            flash("Nama, username, dan email wajib diisi.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        # Reset password (opsional): harus valid & dikonfirmasi, supaya salah ketik
        # tidak diam-diam menyimpan password yang tidak diketahui siapa pun.
        if password_baru or password_baru2:
            if len(password_baru) < 6:
                flash("Password baru minimal 6 karakter.", "danger")
                return redirect(url_for("auth.edit_pengguna", user_id=user.id))
            if password_baru != password_baru2:
                flash("Konfirmasi password baru tidak cocok.", "danger")
                return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        if role not in ("mahasiswa", "staf", "kepala_perpustakaan"):
            flash("Role tidak valid.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        nim, err = validasi_nim(nim_input, wajib=(role == "mahasiswa"), abaikan_user_id=user.id)
        if err:
            flash(err, "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        duplikat_username = User.query.filter(User.username == username, User.id != user.id).first()
        if duplikat_username:
            flash("Username sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        duplikat_email = User.query.filter(User.email == email, User.id != user.id).first()
        if duplikat_email:
            flash("Email sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        # Jika akun ini satu-satunya operator, jangan biarkan diturunkan rolenya
        # dari sini (mencegah sistem kehilangan seluruh akses kepala perpustakaan).
        if user.is_kepala and role != "kepala_perpustakaan":
            jumlah_kepala = User.query.filter_by(role="kepala_perpustakaan").count()
            if jumlah_kepala <= 1:
                flash("Tidak bisa mengubah role: ini adalah satu-satunya akun kepala perpustakaan yang tersisa.", "warning")
                return redirect(url_for("auth.edit_pengguna", user_id=user.id))

        user.username = username
        user.email = email
        user.nama_lengkap = nama_lengkap
        user.no_telepon = no_telepon or None
        user.alamat = alamat or None
        user.nim = nim
        user.role = role

        if password_baru:
            user.set_password(password_baru)

        # kalau kartu belum pernah terbit (mis. akun lama sebelum fitur ini ada), terbitkan sekarang
        _terbitkan_kartu_jika_belum_ada(user)

        db.session.commit()
        if password_baru:
            flash(f"Akun '{user.username}' berhasil diperbarui dan password-nya sudah direset.", "success")
        else:
            flash(f"Akun '{user.username}' berhasil diperbarui.", "success")
        return redirect(url_for("auth.daftar_pengguna"))

    return render_template("auth/edit_pengguna.html", u=user)


@auth_bp.route("/pengguna/<int:user_id>/hapus", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def hapus_pengguna(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Anda tidak bisa menghapus akun sendiri.", "warning")
        return redirect(url_for("auth.daftar_pengguna"))

    if user.is_kepala:
        jumlah_kepala = User.query.filter_by(role="kepala_perpustakaan").count()
        if jumlah_kepala <= 1:
            flash("Tidak bisa menghapus: ini adalah satu-satunya akun kepala perpustakaan yang tersisa.", "warning")
            return redirect(url_for("auth.daftar_pengguna"))

    # Cegah hapus akun yang masih punya pengajuan/peminjaman AKTIF —
    # harus diselesaikan (dikembalikan/ditolak) dulu supaya stok buku &
    # data sirkulasi tetap konsisten.
    ada_aktif = Peminjaman.query.filter(
        Peminjaman.user_id == user.id,
        Peminjaman.status.in_(["diajukan", "dipinjam"]),
    ).first()
    if ada_aktif:
        flash(
            f"Tidak bisa menghapus '{user.username}': masih ada pengajuan/peminjaman aktif. "
            "Selesaikan (kembalikan/tolak) dulu, atau nonaktifkan saja akunnya.",
            "warning",
        )
        return redirect(url_for("auth.daftar_pengguna"))

    username = user.username
    riwayat_lama = Peminjaman.query.filter_by(user_id=user.id).count()
    db.session.delete(user)
    db.session.commit()

    pesan = f"Akun '{username}' berhasil dihapus."
    if riwayat_lama:
        pesan += f" ({riwayat_lama} riwayat peminjaman lama miliknya ikut terhapus.)"
    flash(pesan, "success")
    return redirect(url_for("auth.daftar_pengguna"))


# ------------------------------------------------------------------
# PROFIL SAYA (self-service, khusus staf & kepala perpustakaan) - edit data diri
# sendiri & ganti password. Tidak boleh mengubah role/status akun sendiri
# lewat sini (itu tetap lewat menu manajemen pengguna, oleh kepala perpustakaan lain).
# ------------------------------------------------------------------
@auth_bp.route("/profil", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def profil():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        no_telepon = request.form.get("no_telepon", "").strip()
        alamat = request.form.get("alamat", "").strip()
        password_lama = request.form.get("password_lama", "")
        password_baru = request.form.get("password_baru", "")
        password_baru2 = request.form.get("password_baru2", "")

        if not all([email, nama_lengkap]):
            flash("Nama dan email wajib diisi.", "danger")
            return redirect(url_for("auth.profil"))

        duplikat_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if duplikat_email:
            flash("Email sudah digunakan pengguna lain.", "danger")
            return redirect(url_for("auth.profil"))

        # ganti password bersifat opsional, tapi kalau diisi harus lengkap & valid
        # Kepala perpustakaan (role tertinggi) tidak perlu memasukkan password lama;
        # staf tetap wajib memasukkannya.
        if password_baru or password_baru2 or (password_lama and not current_user.is_kepala):
            if not current_user.is_kepala and not current_user.check_password(password_lama):
                flash("Password lama yang dimasukkan salah.", "danger")
                return redirect(url_for("auth.profil"))
            if password_baru != password_baru2:
                flash("Konfirmasi password baru tidak cocok.", "danger")
                return redirect(url_for("auth.profil"))
            if len(password_baru) < 6:
                flash("Password baru minimal 6 karakter.", "danger")
                return redirect(url_for("auth.profil"))
            current_user.set_password(password_baru)

        current_user.email = email
        current_user.nama_lengkap = nama_lengkap
        current_user.no_telepon = no_telepon or None
        current_user.alamat = alamat or None

        _terbitkan_kartu_jika_belum_ada(current_user)

        db.session.commit()
        flash("Profil berhasil diperbarui.", "success")
        return redirect(url_for("auth.profil"))

    return render_template("auth/profil.html")


# ------------------------------------------------------------------
# PERSETUJUAN AKUN ANGGOTA BARU (khusus kepala perpustakaan)
# Registrasi mandiri lewat /auth/register masuk sini dulu sebelum
# bisa login. Tidak mengubah/menyentuh proses tambah_pengguna() di atas.
# ------------------------------------------------------------------
@auth_bp.route("/pengguna/persetujuan")
@login_required
@role_required("kepala_perpustakaan")
def daftar_persetujuan():
    pending = (
        User.query.filter_by(role="mahasiswa", status_akun="pending")
        .order_by(User.created_at.asc())
        .all()
    )
    return render_template("auth/persetujuan.html", pending=pending)


@auth_bp.route("/pengguna/<int:user_id>/setujui", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def setujui_pengguna(user_id):
    user = User.query.get_or_404(user_id)

    if user.status_akun != "pending":
        flash("Akun ini sudah pernah diproses sebelumnya.", "warning")
        return redirect(url_for("auth.daftar_persetujuan"))

    user.status_akun = "disetujui"

    # terbitkan kartu anggota digital sekarang (masa berlaku dihitung
    # sejak tanggal disetujui, bukan sejak tanggal daftar)
    if not user.kartu:
        kartu = KartuAnggota(
            user_id=user.id,
            tanggal_terbit=date.today(),
            tanggal_kadaluarsa=date.today() + timedelta(days=current_app.config["MASA_BERLAKU_KARTU_HARI"]),
            status="aktif",
        )
        db.session.add(kartu)

    db.session.commit()
    flash(f"Akun '{user.username}' disetujui dan kartu anggota diterbitkan.", "success")
    return redirect(url_for("auth.daftar_persetujuan"))


@auth_bp.route("/pengguna/<int:user_id>/tolak", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def tolak_pengguna(user_id):
    user = User.query.get_or_404(user_id)

    if user.status_akun != "pending":
        flash("Akun ini sudah pernah diproses sebelumnya.", "warning")
        return redirect(url_for("auth.daftar_persetujuan"))

    user.status_akun = "ditolak"
    user.is_active_db = False
    db.session.commit()
    flash(f"Registrasi '{user.username}' ditolak.", "info")
    return redirect(url_for("auth.daftar_persetujuan"))
```


## `Website/routes/buku.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
import os
import uuid
from collections import OrderedDict
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash,
    current_app, send_file, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from models import Buku, Kategori, Peminjaman
from utils.decorators import role_required
from utils.excel_import import buat_template_excel, import_buku_dari_excel
from utils.excel_export import buat_excel

buku_bp = Blueprint("buku", __name__, url_prefix="/buku")


def _allowed_image(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXT"]


def _simpan_sampul(file_storage):
    """Simpan file gambar ke folder upload, kembalikan path relatif terhadap
    folder 'static/' (selalu pakai forward-slash, aman di Windows/Linux/Mac)."""
    if not file_storage or file_storage.filename == "":
        return None
    if not _allowed_image(file_storage.filename):
        flash("Format gambar tidak didukung (gunakan png/jpg/jpeg/webp).", "warning")
        return None

    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    nama_unik = f"{uuid.uuid4().hex}.{ext}"
    nama_aman = secure_filename(nama_unik)
    path_lengkap = os.path.join(current_app.config["UPLOAD_FOLDER"], nama_aman)
    file_storage.save(path_lengkap)

    # Path disimpan ke DB relatif terhadap folder static, dengan '/' selalu
    # (bukan os.path.join) agar konsisten dipakai ulang oleh url_for('static', ...)
    # di semua template, terlepas dari OS server-nya.
    return f"uploads/sampul/{nama_aman}"  # contoh: uploads/sampul/xxxx.jpg


def _isbn_duplikat(isbn, kecuali_id=None):
    if not isbn:
        return None
    q = Buku.query.filter(Buku.isbn == isbn)
    if kecuali_id:
        q = q.filter(Buku.id != kecuali_id)
    return q.first()


def _lama_pinjam_form():
    """Lama pinjam khusus buku (opsional): kosong = ikut pengaturan umum."""
    nilai = request.form.get("lama_pinjam_hari", type=int)
    return nilai if nilai and 1 <= nilai <= 365 else None


# ------------------------------------------------------------------
# DAFTAR & PENCARIAN BUKU (semua role bisa lihat)
# ------------------------------------------------------------------
@buku_bp.route("/")
@login_required
def daftar_buku():
    q = request.args.get("q", "").strip()
    kategori_id = request.args.get("kategori_id", type=int)

    query = Buku.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Buku.judul.ilike(like), Buku.penulis.ilike(like), Buku.isbn.ilike(like))
        )
    if kategori_id:
        query = query.filter(Buku.kategori_id == kategori_id)

    daftar = query.order_by(Buku.judul.asc()).all()
    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()

    # untuk anggota: buku mana saja yang sudah punya pengajuan/pinjaman aktif,
    # dihitung sekali di sini (bukan per-kartu) supaya tidak membebani query.
    buku_id_aktif = set()
    maks_pinjam = current_app.config["MAKS_PINJAM_PER_USER"]
    jumlah_aktif = 0
    if current_user.is_mahasiswa:
        aktif = Peminjaman.query.filter(
            Peminjaman.user_id == current_user.id,
            Peminjaman.status.in_(["diajukan", "dipinjam"]),
        ).all()
        buku_id_aktif = {p.buku_id for p in aktif}
        jumlah_aktif = len(aktif)
    kuota_penuh = jumlah_aktif >= maks_pinjam

    # Kelompokkan buku per kategori agar tampilannya seperti rak perpustakaan
    # sungguhan: tiap rak (kategori) berisi buku-bukunya sendiri, rapi dan mudah dipahami.
    kelompok = OrderedDict()
    for kat in kategori_list:
        buku_kat = [b for b in daftar if b.kategori_id == kat.id]
        if buku_kat:
            kelompok[kat.nama_kategori] = buku_kat
    tanpa_kategori = [b for b in daftar if not b.kategori_id]
    if tanpa_kategori:
        kelompok["Tanpa Kategori"] = tanpa_kategori

    return render_template(
        "buku/daftar.html", daftar=daftar, kelompok=kelompok,
        kategori_list=kategori_list, q=q, kategori_id=kategori_id,
        buku_id_aktif=buku_id_aktif,
        kuota_penuh=kuota_penuh, jumlah_aktif=jumlah_aktif, maks_pinjam=maks_pinjam,
    )


@buku_bp.route("/<int:buku_id>")
@login_required
def detail_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)

    pengajuan_aktif = None
    if current_user.is_mahasiswa:
        pengajuan_aktif = Peminjaman.query.filter(
            Peminjaman.user_id == current_user.id,
            Peminjaman.buku_id == buku.id,
            Peminjaman.status.in_(["diajukan", "dipinjam"]),
        ).first()

    maks_pinjam = current_app.config["MAKS_PINJAM_PER_USER"]
    jumlah_aktif = current_user.jumlah_pinjaman_aktif if current_user.is_mahasiswa else 0
    return render_template(
        "buku/detail.html", buku=buku, pengajuan_aktif=pengajuan_aktif,
        kuota_penuh=jumlah_aktif >= maks_pinjam, jumlah_aktif=jumlah_aktif, maks_pinjam=maks_pinjam,
    )


# ------------------------------------------------------------------
# TAMBAH / EDIT / HAPUS BUKU (khusus staf & kepala perpustakaan)
# ------------------------------------------------------------------
@buku_bp.route("/tambah", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def tambah_buku():
    if request.method == "POST":
        judul = request.form.get("judul", "").strip()
        penulis = request.form.get("penulis", "").strip()
        penerbit = request.form.get("penerbit", "").strip()
        tahun_terbit = request.form.get("tahun_terbit", type=int)
        isbn = request.form.get("isbn", "").strip()
        kategori_id = request.form.get("kategori_id", type=int)
        deskripsi = request.form.get("deskripsi", "").strip()
        stok = max(0, request.form.get("stok", type=int, default=0) or 0)
        lokasi_rak = request.form.get("lokasi_rak", "").strip() or None

        if not judul or not penulis:
            flash("Judul dan penulis wajib diisi.", "danger")
            return redirect(url_for("buku.tambah_buku"))

        ada = _isbn_duplikat(isbn)
        if ada:
            flash(f"ISBN {isbn} sudah terdaftar untuk buku '{ada.judul}'. "
                  "Jika ini eksemplar tambahan, tambahkan stok pada buku tersebut.", "warning")
            return redirect(url_for("buku.tambah_buku"))

        sampul_path = _simpan_sampul(request.files.get("sampul"))

        buku = Buku(
            judul=judul, penulis=penulis, penerbit=penerbit or None,
            tahun_terbit=tahun_terbit, isbn=isbn or None, kategori_id=kategori_id or None,
            deskripsi=deskripsi or None, stok=stok, sampul_path=sampul_path,
            lokasi_rak=lokasi_rak, lama_pinjam_hari=_lama_pinjam_form(),
        )
        db.session.add(buku)
        db.session.commit()
        flash(f"Buku '{judul}' berhasil ditambahkan.", "success")
        return redirect(url_for("buku.daftar_buku"))

    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()
    return render_template("buku/form.html", buku=None, kategori_list=kategori_list)


@buku_bp.route("/<int:buku_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def edit_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)

    if request.method == "POST":
        isbn_baru = request.form.get("isbn", "").strip()
        ada = _isbn_duplikat(isbn_baru, kecuali_id=buku.id)
        if ada:
            flash(f"ISBN {isbn_baru} sudah dipakai buku '{ada.judul}'.", "warning")
            return redirect(url_for("buku.edit_buku", buku_id=buku.id))

        buku.judul = request.form.get("judul", "").strip()
        buku.penulis = request.form.get("penulis", "").strip()
        buku.penerbit = request.form.get("penerbit", "").strip() or None
        buku.tahun_terbit = request.form.get("tahun_terbit", type=int)
        buku.isbn = request.form.get("isbn", "").strip() or None
        buku.kategori_id = request.form.get("kategori_id", type=int) or None
        buku.deskripsi = request.form.get("deskripsi", "").strip() or None
        buku.stok = max(0, request.form.get("stok", type=int, default=0) or 0)
        buku.lokasi_rak = request.form.get("lokasi_rak", "").strip() or None
        buku.lama_pinjam_hari = _lama_pinjam_form()

        sampul_baru = _simpan_sampul(request.files.get("sampul"))
        if sampul_baru:
            buku.sampul_path = sampul_baru

        db.session.commit()
        flash(f"Buku '{buku.judul}' berhasil diperbarui.", "success")
        return redirect(url_for("buku.daftar_buku"))

    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()
    return render_template("buku/form.html", buku=buku, kategori_list=kategori_list)


@buku_bp.route("/<int:buku_id>/hapus", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def hapus_buku(buku_id):
    buku = Buku.query.get_or_404(buku_id)

    # BUG LAMA: buku bisa langsung dihapus meski masih ada pengajuan/peminjaman
    # aktif atasnya. Karena relasi peminjaman_list pakai cascade
    # "all, delete-orphan", ini diam-diam menghapus seluruh riwayat
    # peminjaman buku tsb (termasuk yang sedang dipinjam), sama seperti
    # pengecekan yang sudah ada di hapus_pengguna().
    ada_aktif = Peminjaman.query.filter(
        Peminjaman.buku_id == buku.id,
        Peminjaman.status.in_(["diajukan", "dipinjam"]),
    ).first()
    if ada_aktif:
        flash(
            f"Tidak bisa menghapus '{buku.judul}': masih ada pengajuan/peminjaman aktif atas buku ini. "
            "Selesaikan (kembalikan/tolak) dulu.",
            "warning",
        )
        return redirect(url_for("buku.daftar_buku"))

    judul = buku.judul
    db.session.delete(buku)
    db.session.commit()
    flash(f"Buku '{judul}' berhasil dihapus.", "success")
    return redirect(url_for("buku.daftar_buku"))


@buku_bp.route("/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_buku():
    """Unduh seluruh koleksi buku ke Excel (format kolom sama seperti template import)."""
    from datetime import date
    daftar = Buku.query.order_by(Buku.judul).all()
    baris = [
        [b.judul, b.penulis, b.penerbit or "", b.tahun_terbit or "", b.isbn or "",
         b.kategori.nama_kategori if b.kategori else "", b.stok, b.lokasi_rak or "",
         b.lama_pinjam_hari or ""]
        for b in daftar
    ]
    buffer = buat_excel(
        "Koleksi Buku",
        ["Judul", "Penulis", "Penerbit", "Tahun", "ISBN", "Kategori", "Stok", "Lokasi Rak", "Lama Pinjam (hari)"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True, download_name=f"koleksi_buku_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ------------------------------------------------------------------
# KATEGORI
# ------------------------------------------------------------------
@buku_bp.route("/kategori", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def kategori():
    if request.method == "POST":
        nama = request.form.get("nama_kategori", "").strip()
        if nama and not Kategori.query.filter_by(nama_kategori=nama).first():
            db.session.add(Kategori(nama_kategori=nama))
            db.session.commit()
            flash(f"Kategori '{nama}' ditambahkan.", "success")
        else:
            flash("Kategori kosong atau sudah ada.", "warning")
        return redirect(url_for("buku.kategori"))

    kategori_list = Kategori.query.order_by(Kategori.nama_kategori).all()
    return render_template("buku/kategori.html", kategori_list=kategori_list)


@buku_bp.route("/kategori/<int:kategori_id>/hapus", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def hapus_kategori(kategori_id):
    """Hapus kategori. Buku di dalamnya TIDAK ikut terhapus: buku tsb menjadi
    'Tanpa Kategori' (kategori_id di-set NULL)."""
    kat = Kategori.query.get_or_404(kategori_id)
    nama = kat.nama_kategori
    jumlah_buku = len(kat.buku_list)

    for b in list(kat.buku_list):
        b.kategori_id = None
    db.session.delete(kat)
    db.session.commit()

    pesan = f"Kategori '{nama}' berhasil dihapus."
    if jumlah_buku:
        pesan += f" {jumlah_buku} buku di dalamnya kini berstatus 'Tanpa Kategori'."
    flash(pesan, "success")
    return redirect(url_for("buku.kategori"))


# ------------------------------------------------------------------
# IMPORT / EXPORT EXCEL (khusus staf & kepala perpustakaan)
# ------------------------------------------------------------------
@buku_bp.route("/template-excel")
@login_required
@role_required("staf", "kepala_perpustakaan")
def download_template_excel():
    buffer = buat_template_excel()
    return send_file(
        buffer,
        as_attachment=True,
        download_name="template_import_buku.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@buku_bp.route("/import-excel", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def import_excel():
    if request.method == "POST":
        file = request.files.get("file_excel")
        if not file or file.filename == "":
            flash("Pilih file Excel (.xlsx) terlebih dahulu.", "danger")
            return redirect(url_for("buku.import_excel"))

        if not file.filename.lower().endswith(".xlsx"):
            flash("File harus berformat .xlsx", "danger")
            return redirect(url_for("buku.import_excel"))

        sukses, errors = import_buku_dari_excel(file.stream)
        flash(f"{sukses} buku berhasil diimport.", "success" if sukses else "warning")
        for err in errors[:20]:
            flash(err, "warning")
        return redirect(url_for("buku.daftar_buku"))

    return render_template("buku/import_excel.html")
```


## `Website/routes/dashboard.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from datetime import date, timedelta
from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from sqlalchemy import func

from extensions import db
from models import Buku, Peminjaman, User, Kategori
from utils.denda import denda_berjalan_semua, total_denda_belum_lunas
from routes.laporan import statistik_mahasiswa_peminjam

dashboard_bp = Blueprint("dashboard", __name__)

BULAN_ID = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def _enam_bulan_terakhir():
    """Kembalikan list (tahun, bulan) untuk 6 bulan terakhir, urut menaik, termasuk bulan ini."""
    awal_bulan_ini = date.today().replace(day=1)
    hasil = []
    for mundur in range(5, -1, -1):
        bulan = awal_bulan_ini.month - mundur
        tahun = awal_bulan_ini.year
        while bulan <= 0:
            bulan += 12
            tahun -= 1
        hasil.append((tahun, bulan))
    return hasil


def _data_grafik_peminjaman_bulanan():
    """Jumlah peminjaman per bulan, 6 bulan terakhir (untuk grafik garis/batang)."""
    bulan_list = _enam_bulan_terakhir()
    tahun_awal, bulan_awal = bulan_list[0]
    mulai = date(tahun_awal, bulan_awal, 1)

    baris = (
        db.session.query(
            func.date_format(Peminjaman.tanggal_pinjam, "%Y-%m").label("bulan_kunci"),
            func.count(Peminjaman.id),
        )
        .filter(Peminjaman.tanggal_pinjam >= mulai)
        .group_by("bulan_kunci")
        .all()
    )
    peta_jumlah = {kunci: jumlah for kunci, jumlah in baris}

    labels, data = [], []
    for tahun, bulan in bulan_list:
        kunci = f"{tahun:04d}-{bulan:02d}"
        labels.append(f"{BULAN_ID[bulan - 1]} {tahun}")
        data.append(peta_jumlah.get(kunci, 0))
    return labels, data


def _data_grafik_buku_terpopuler(limit=5):
    """Top N buku paling sering dipinjam (untuk grafik batang)."""
    hasil = (
        db.session.query(Buku.judul, func.count(Peminjaman.id).label("jumlah"))
        .join(Peminjaman, Peminjaman.buku_id == Buku.id)
        .group_by(Buku.id)
        .order_by(func.count(Peminjaman.id).desc())
        .limit(limit)
        .all()
    )
    labels = [judul for judul, _ in hasil]
    data = [jumlah for _, jumlah in hasil]
    return labels, data


def _data_grafik_distribusi_kategori():
    """Jumlah judul buku per kategori (untuk grafik donat)."""
    hasil = (
        db.session.query(Kategori.nama_kategori, func.count(Buku.id))
        .outerjoin(Buku, Buku.kategori_id == Kategori.id)
        .group_by(Kategori.id)
        .having(func.count(Buku.id) > 0)
        .order_by(func.count(Buku.id).desc())
        .all()
    )
    labels = [nama for nama, _ in hasil]
    data = [jumlah for _, jumlah in hasil]
    return labels, data


@dashboard_bp.route("/")
@login_required
def index():
    context = {}
    if current_user.is_mahasiswa:
        pinjaman_aktif = Peminjaman.query.filter_by(
            user_id=current_user.id, status="dipinjam"
        ).all()
        context["pinjaman_aktif"] = pinjaman_aktif
        context["jumlah_terlambat_saya"] = sum(1 for p in pinjaman_aktif if p.is_telat)
        context["denda_berjalan_saya"] = denda_berjalan_semua(current_user.id)
        context["denda_belum_lunas_saya"] = total_denda_belum_lunas(current_user.id)

        # peringatan "akan jatuh tempo" (belum telat, tapi tinggal beberapa hari lagi)
        batas_peringatan = current_app.config["PERINGATAN_JATUH_TEMPO_HARI"]
        context["akan_jatuh_tempo_saya"] = [
            p for p in pinjaman_aktif
            if not p.is_telat and p.hari_menuju_jatuh_tempo is not None
            and p.hari_menuju_jatuh_tempo <= batas_peringatan
        ]

        # ringkasan singkat untuk anggota
        context["jumlah_sedang_dipinjam"] = len(pinjaman_aktif)
        context["jumlah_pernah_dipinjam"] = Peminjaman.query.filter_by(user_id=current_user.id).count()
        context["kartu_saya"] = current_user.kartu
        context["maks_pinjam"] = current_app.config["MAKS_PINJAM_PER_USER"]
        context["jumlah_kuota_terpakai"] = current_user.jumlah_pinjaman_aktif

        # rekomendasi: buku paling populer (paling sering dipinjam) yang
        # sedang tersedia stoknya dan belum sedang dipinjam/diajukan anggota ini
        buku_id_aktif = {p.buku_id for p in Peminjaman.query.filter(
            Peminjaman.user_id == current_user.id,
            Peminjaman.status.in_(["diajukan", "dipinjam"]),
        ).all()}
        rekomendasi = (
            db.session.query(Buku, func.count(Peminjaman.id).label("jumlah"))
            .join(Peminjaman, Peminjaman.buku_id == Buku.id)
            .filter(Buku.stok > 0)
            .group_by(Buku.id)
            .order_by(func.count(Peminjaman.id).desc())
            .limit(10)
            .all()
        )
        context["rekomendasi_buku"] = [
            (b, jumlah) for b, jumlah in rekomendasi if b.id not in buku_id_aktif
        ][:5]
    else:
        # staf & kepala perpustakaan melihat ringkasan umum + grafik
        context["total_buku"] = Buku.query.count()
        context["total_stok"] = sum(b.stok for b in Buku.query.all())
        context["sedang_dipinjam"] = Peminjaman.query.filter_by(status="dipinjam").count()
        context["terlambat"] = sum(
            1 for p in Peminjaman.query.filter_by(status="dipinjam").all() if p.is_telat
        )

        # denda: hal yang perlu perhatian petugas
        context["denda_belum_lunas"] = total_denda_belum_lunas()
        context["denda_berjalan"] = denda_berjalan_semua()

        # grafik: tren peminjaman 6 bulan terakhir
        labels_bulanan, data_bulanan = _data_grafik_peminjaman_bulanan()
        context["labels_grafik_bulanan"] = labels_bulanan
        context["data_grafik_bulanan"] = data_bulanan

        # grafik: buku paling sering dipinjam
        labels_top, data_top = _data_grafik_buku_terpopuler()
        context["labels_grafik_top_buku"] = labels_top
        context["data_grafik_top_buku"] = data_top

        # grafik: mahasiswa paling sering meminjam (semua waktu, top 5)
        top_mhs = statistik_mahasiswa_peminjam("semua", limit=5)
        context["labels_grafik_top_mhs"] = [b["user"].nama_lengkap for b in top_mhs]
        context["data_grafik_top_mhs"] = [b["total"] for b in top_mhs]

        # grafik: distribusi buku per kategori
        labels_kat, data_kat = _data_grafik_distribusi_kategori()
        context["labels_grafik_kategori"] = labels_kat
        context["data_grafik_kategori"] = data_kat

        # daftar penting: akan jatuh tempo dalam N hari ke depan (lihat config.PERINGATAN_JATUH_TEMPO_HARI)
        batas_tempo = date.today() + timedelta(days=current_app.config["PERINGATAN_JATUH_TEMPO_HARI"])
        context["akan_jatuh_tempo"] = (
            Peminjaman.query.filter(
                Peminjaman.status == "dipinjam",
                Peminjaman.tanggal_jatuh_tempo >= date.today(),
                Peminjaman.tanggal_jatuh_tempo <= batas_tempo,
            )
            .order_by(Peminjaman.tanggal_jatuh_tempo.asc())
            .all()
        )

        # aktivitas terbaru
        context["peminjaman_terbaru"] = (
            Peminjaman.query.order_by(Peminjaman.id.desc()).limit(6).all()
        )

        if current_user.is_kepala:
            context["total_anggota"] = User.query.filter_by(role="mahasiswa").count()
            context["menunggu_persetujuan"] = User.query.filter_by(
                role="mahasiswa", status_akun="pending"
            ).count()

    return render_template("dashboard.html", today=date.today(), **context)
```


## `Website/routes/denda.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from sqlalchemy import func

from extensions import db
from models import Peminjaman, User, Buku
from utils.decorators import role_required
from utils.denda import denda_peminjaman, denda_berjalan_semua, format_rupiah
from utils.excel_export import buat_excel

denda_bp = Blueprint("denda", __name__, url_prefix="/denda")

STATUS_LABEL = {
    "belum_lunas": "Belum Lunas",
    "lunas": "Lunas",
    "dibebaskan": "Dibebaskan",
    "tidak_ada": "-",
}


def _query_denda(status, q):
    """Peminjaman yang memiliki denda (sudah dibekukan) sesuai filter status & pencarian."""
    query = Peminjaman.query.filter(Peminjaman.denda > 0)
    if status in ("belum_lunas", "lunas", "dibebaskan"):
        query = query.filter(Peminjaman.status_denda == status)
    if q:
        like = f"%{q}%"
        query = (
            query.join(User, Peminjaman.user_id == User.id)
            .join(Buku, Peminjaman.buku_id == Buku.id)
            .filter(db.or_(
                User.nama_lengkap.ilike(like), User.username.ilike(like),
                User.nim.ilike(like), Buku.judul.ilike(like),
            ))
        )
    return query


@denda_bp.route("/")
@login_required
@role_required("staf", "kepala_perpustakaan")
def daftar_denda():
    status = request.args.get("status", "belum_lunas")
    q = request.args.get("q", "").strip()

    if status == "berjalan":
        # buku yang masih dipinjam dan sudah telat: denda masih terus bertambah
        semua = Peminjaman.query.filter_by(status="dipinjam").order_by(Peminjaman.tanggal_jatuh_tempo.asc()).all()
        daftar = [p for p in semua if denda_peminjaman(p) > 0 or p.hari_telat > 0]
        if q:
            k = q.lower()
            daftar = [p for p in daftar if k in p.anggota.nama_lengkap.lower()
                      or k in p.anggota.username.lower() or k in p.buku.judul.lower()]
    else:
        daftar = _query_denda(status, q).order_by(Peminjaman.tanggal_kembali.desc()).all()

    awal_bulan = date.today().replace(day=1)
    total_belum_lunas = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "belum_lunas").scalar() or 0
    terkumpul_bulan_ini = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "lunas", Peminjaman.tanggal_denda_selesai >= awal_bulan).scalar() or 0
    terkumpul_total = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "lunas").scalar() or 0

    return render_template(
        "denda/daftar.html", daftar=daftar, status=status, q=q,
        total_belum_lunas=int(total_belum_lunas),
        terkumpul_bulan_ini=int(terkumpul_bulan_ini),
        terkumpul_total=int(terkumpul_total),
        total_berjalan=denda_berjalan_semua(),
        total_daftar=sum(denda_peminjaman(p) for p in daftar),
        status_label=STATUS_LABEL,
    )


@denda_bp.route("/<int:peminjaman_id>/lunas", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def lunasi(peminjaman_id):
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status_denda != "belum_lunas":
        flash("Denda ini tidak berstatus belum lunas.", "warning")
        return redirect(request.referrer or url_for("denda.daftar_denda"))

    p.status_denda = "lunas"
    p.tanggal_denda_selesai = date.today()
    p.denda_diproses_oleh = current_user.id
    db.session.commit()
    flash(f"Denda {format_rupiah(p.denda)} dari {p.anggota.nama_lengkap} dicatat LUNAS.", "success")
    return redirect(request.referrer or url_for("denda.daftar_denda"))


@denda_bp.route("/<int:peminjaman_id>/bebaskan", methods=["POST"])
@login_required
@role_required("kepala_perpustakaan")
def bebaskan(peminjaman_id):
    """Hapus denda tanpa pembayaran (mis. alasan khusus). Khusus kepala perpustakaan."""
    p = Peminjaman.query.get_or_404(peminjaman_id)
    if p.status_denda != "belum_lunas":
        flash("Denda ini tidak berstatus belum lunas.", "warning")
        return redirect(request.referrer or url_for("denda.daftar_denda"))

    p.status_denda = "dibebaskan"
    p.tanggal_denda_selesai = date.today()
    p.denda_diproses_oleh = current_user.id
    p.catatan_denda = request.form.get("catatan", "").strip()[:255] or None
    db.session.commit()
    flash(f"Denda {format_rupiah(p.denda)} dari {p.anggota.nama_lengkap} dibebaskan.", "success")
    return redirect(request.referrer or url_for("denda.daftar_denda"))


@denda_bp.route("/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_denda():
    status = request.args.get("status", "semua")
    daftar = _query_denda(status, "").order_by(Peminjaman.tanggal_kembali.desc()).all()
    baris = [
        [p.anggota.nama_lengkap, p.anggota.nim or p.anggota.username, p.buku.judul,
         p.tanggal_pinjam.strftime("%d-%m-%Y"), p.tanggal_jatuh_tempo.strftime("%d-%m-%Y"),
         p.tanggal_kembali.strftime("%d-%m-%Y") if p.tanggal_kembali else "-",
         p.hari_telat, p.denda, STATUS_LABEL.get(p.status_denda, p.status_denda),
         p.tanggal_denda_selesai.strftime("%d-%m-%Y") if p.tanggal_denda_selesai else "-"]
        for p in daftar
    ]
    buffer = buat_excel(
        "Denda",
        ["Mahasiswa", "NIM/Username", "Buku", "Tgl Pinjam", "Jatuh Tempo", "Tgl Kembali",
         "Hari Telat", "Denda (Rp)", "Status", "Tgl Lunas/Bebas"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True, download_name=f"laporan_denda_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
```


## `Website/routes/kartu.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from datetime import date, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from extensions import db
from models import User, KartuAnggota
from utils.decorators import role_required
from utils.kartu import validasi_nim, terbitkan_kartu_jika_belum_ada as _terbitkan_kartu_jika_belum_ada

kartu_bp = Blueprint("kartu", __name__, url_prefix="/kartu")


# Kartu perpustakaan digital berlaku untuk SEMUA role (mahasiswa, staf, kepala
# perpustakaan). Kalau akun lama belum pernah punya kartu (dibuat sebelum fitur
# ini ada), kartunya diterbitkan otomatis saat pertama kali dibuka ("lazy create").
# ID kartu = NIM pemilik.
@kartu_bp.route("/saya")
@login_required
def kartu_saya():
    kartu = _terbitkan_kartu_jika_belum_ada(current_user)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=current_user)


@kartu_bp.route("/saya/cetak")
@login_required
def kartu_saya_cetak():
    kartu = _terbitkan_kartu_jika_belum_ada(current_user)
    return render_template("kartu/cetak.html", kartu=kartu, anggota=current_user)


@kartu_bp.route("/anggota/<int:user_id>")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kartu_anggota_lain(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = _terbitkan_kartu_jika_belum_ada(anggota)
    return render_template("kartu/kartu.html", kartu=kartu, anggota=anggota)


@kartu_bp.route("/anggota/<int:user_id>/cetak")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kartu_anggota_lain_cetak(user_id):
    anggota = User.query.get_or_404(user_id)
    kartu = _terbitkan_kartu_jika_belum_ada(anggota)
    return render_template("kartu/cetak.html", kartu=kartu, anggota=anggota)


# ------------------------------------------------------------------
# PENGATURAN KARTU PERPUSTAKAAN (staf & kepala perpustakaan)
# Daftar semua kartu, ubah NIM / masa berlaku / status, perpanjang,
# aktifkan-nonaktifkan. Kartu nonaktif atau kadaluarsa tidak bisa
# dipakai meminjam buku.
# ------------------------------------------------------------------
@kartu_bp.route("/kelola")
@login_required
@role_required("staf", "kepala_perpustakaan")
def kelola_kartu():
    q = request.args.get("q", "").strip()
    filter_status = request.args.get("status", "semua")

    query = KartuAnggota.query.join(User, KartuAnggota.user_id == User.id)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(User.nama_lengkap.ilike(like), User.username.ilike(like), User.nim.ilike(like))
        )
    if filter_status == "aktif":
        query = query.filter(KartuAnggota.status == "aktif", KartuAnggota.tanggal_kadaluarsa >= date.today())
    elif filter_status == "nonaktif":
        query = query.filter(KartuAnggota.status == "nonaktif")
    elif filter_status == "kadaluarsa":
        query = query.filter(KartuAnggota.tanggal_kadaluarsa < date.today())

    daftar = query.order_by(User.nama_lengkap.asc()).all()

    # akun yang belum punya kartu (mis. akun lama / masih pending) ditampilkan terpisah
    tanpa_kartu = (
        User.query.outerjoin(KartuAnggota, KartuAnggota.user_id == User.id)
        .filter(KartuAnggota.id.is_(None), User.status_akun == "disetujui")
        .order_by(User.nama_lengkap.asc())
        .all()
    )
    return render_template(
        "kartu/kelola.html", daftar=daftar, tanpa_kartu=tanpa_kartu,
        q=q, filter_status=filter_status, today=date.today(),
    )


@kartu_bp.route("/kelola/terbitkan/<int:user_id>", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def terbitkan_kartu(user_id):
    user = User.query.get_or_404(user_id)
    if user.kartu:
        flash("Pengguna ini sudah memiliki kartu.", "warning")
    else:
        _terbitkan_kartu_jika_belum_ada(user)
        flash(f"Kartu untuk '{user.nama_lengkap}' berhasil diterbitkan.", "success")
    return redirect(url_for("kartu.kelola_kartu"))


@kartu_bp.route("/kelola/<int:kartu_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def edit_kartu(kartu_id):
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    pemilik = kartu.pemilik

    if request.method == "POST":
        nim, err = validasi_nim(
            request.form.get("nim", ""), wajib=pemilik.is_mahasiswa, abaikan_user_id=pemilik.id
        )
        if err:
            flash(err, "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))

        try:
            terbit = date.fromisoformat(request.form.get("tanggal_terbit", ""))
            kadaluarsa = date.fromisoformat(request.form.get("tanggal_kadaluarsa", ""))
        except ValueError:
            flash("Format tanggal tidak valid.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))
        if kadaluarsa < terbit:
            flash("Tanggal kadaluarsa tidak boleh lebih awal dari tanggal terbit.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))

        status = request.form.get("status", kartu.status)
        if status not in ("aktif", "nonaktif"):
            flash("Status kartu tidak valid.", "danger")
            return redirect(url_for("kartu.edit_kartu", kartu_id=kartu.id))

        pemilik.nim = nim
        kartu.tanggal_terbit = terbit
        kartu.tanggal_kadaluarsa = kadaluarsa
        kartu.status = status
        db.session.commit()
        flash(f"Kartu '{pemilik.nama_lengkap}' berhasil diperbarui.", "success")
        return redirect(url_for("kartu.kelola_kartu"))

    return render_template("kartu/edit.html", kartu=kartu, pemilik=pemilik)


@kartu_bp.route("/kelola/<int:kartu_id>/toggle", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def toggle_kartu(kartu_id):
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    kartu.status = "nonaktif" if kartu.status == "aktif" else "aktif"
    db.session.commit()
    flash(f"Kartu '{kartu.pemilik.nama_lengkap}' sekarang {kartu.status}.", "success")
    return redirect(request.referrer or url_for("kartu.kelola_kartu"))


@kartu_bp.route("/kelola/<int:kartu_id>/perpanjang", methods=["POST"])
@login_required
@role_required("staf", "kepala_perpustakaan")
def perpanjang_kartu(kartu_id):
    """Perpanjang masa berlaku. Dihitung dari tanggal kadaluarsa saat ini kalau
    kartu masih berlaku, atau dari hari ini kalau sudah kadaluarsa."""
    kartu = KartuAnggota.query.get_or_404(kartu_id)
    hari = current_app.config["MASA_BERLAKU_KARTU_HARI"]
    dasar = max(kartu.tanggal_kadaluarsa, date.today())
    kartu.tanggal_kadaluarsa = dasar + timedelta(days=hari)
    kartu.status = "aktif"
    db.session.commit()
    flash(
        f"Kartu '{kartu.pemilik.nama_lengkap}' diperpanjang sampai "
        f"{kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y')}.",
        "success",
    )
    return redirect(url_for("kartu.kelola_kartu"))
```


## `Website/routes/laporan.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from datetime import date, timedelta

from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from sqlalchemy import and_, case, func

from extensions import db
from models import Buku, Peminjaman, User
from utils.decorators import role_required
from utils.denda import denda_peminjaman
from utils.excel_export import buat_excel

laporan_bp = Blueprint("laporan", __name__, url_prefix="/laporan")


@laporan_bp.route("/populer")
@login_required
@role_required("staf", "kepala_perpustakaan")
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
@role_required("staf", "kepala_perpustakaan")
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


# ------------------------------------------------------------------
# STATISTIK MAHASISWA PALING SERING MEMINJAM
# ------------------------------------------------------------------
# Kunci -> (label tampilan, jumlah hari ke belakang; None = seluruh riwayat)
PERIODE_STATISTIK = {
    "semua": ("Semua waktu", None),
    "30": ("30 hari terakhir", 30),
    "90": ("90 hari terakhir", 90),
    "365": ("1 tahun terakhir", 365),
}

# Hanya peminjaman yang benar-benar terjadi. 'diajukan' (belum disetujui) dan
# 'ditolak' tidak dihitung sebagai aktivitas meminjam.
STATUS_DIHITUNG = ("dipinjam", "dikembalikan", "terlambat")


def statistik_mahasiswa_peminjam(kunci_periode="semua", limit=None):
    """Peringkat mahasiswa berdasarkan jumlah buku yang dipinjam.

    Kembalikan list dict berurut dari yang paling sering meminjam:
    user, total, judul_unik, sedang_dipinjam, terlambat, terakhir, peringkat.
    Urutan seri: yang lebih baru meminjam dulu, lalu nama A-Z.
    """
    if kunci_periode not in PERIODE_STATISTIK:
        kunci_periode = "semua"
    hari = PERIODE_STATISTIK[kunci_periode][1]

    hari_ini = date.today()
    # Padanan SQL dari Peminjaman.is_telat: sudah kembali tapi lewat tempo,
    # atau belum kembali dan hari ini sudah lewat tempo.
    telat = case(
        (and_(Peminjaman.status == "dikembalikan",
              Peminjaman.tanggal_kembali > Peminjaman.tanggal_jatuh_tempo), 1),
        (and_(Peminjaman.status == "dipinjam",
              Peminjaman.tanggal_jatuh_tempo < hari_ini), 1),
        else_=0,
    )
    sedang = case((Peminjaman.status == "dipinjam", 1), else_=0)

    q = (
        db.session.query(
            User,
            func.count(Peminjaman.id).label("total"),
            func.count(Peminjaman.buku_id.distinct()).label("judul_unik"),
            func.sum(sedang).label("sedang"),
            func.sum(telat).label("telat"),
            func.max(Peminjaman.tanggal_pinjam).label("terakhir"),
        )
        .join(Peminjaman, Peminjaman.user_id == User.id)
        .filter(User.role == "mahasiswa", Peminjaman.status.in_(STATUS_DIHITUNG))
    )
    if hari:
        q = q.filter(Peminjaman.tanggal_pinjam >= hari_ini - timedelta(days=hari))

    q = q.group_by(User.id).order_by(
        func.count(Peminjaman.id).desc(),
        func.max(Peminjaman.tanggal_pinjam).desc(),
        User.nama_lengkap.asc(),
    )
    if limit:
        q = q.limit(limit)

    hasil = []
    for user, total, judul_unik, sedang_n, telat_n, terakhir in q.all():
        hasil.append({
            "user": user,
            "total": int(total),
            "judul_unik": int(judul_unik),
            "sedang_dipinjam": int(sedang_n or 0),
            "terlambat": int(telat_n or 0),
            "terakhir": terakhir,
        })
    # Peringkat kompetisi: total yang sama -> peringkat sama (1, 2, 2, 4, ...).
    for i, baris in enumerate(hasil):
        if i > 0 and baris["total"] == hasil[i - 1]["total"]:
            baris["peringkat"] = hasil[i - 1]["peringkat"]
        else:
            baris["peringkat"] = i + 1
    return hasil


def _periode_dari_request():
    kunci = request.args.get("periode", "semua")
    return kunci if kunci in PERIODE_STATISTIK else "semua"


@laporan_bp.route("/mahasiswa-aktif")
@login_required
@role_required("staf", "kepala_perpustakaan")
def mahasiswa_aktif():
    """Mahasiswa yang paling sering meminjam buku (top 50)."""
    kunci = _periode_dari_request()
    hasil = statistik_mahasiswa_peminjam(kunci, limit=50)
    return render_template(
        "laporan/mahasiswa_aktif.html",
        hasil=hasil,
        periode=kunci,
        periode_opsi=PERIODE_STATISTIK,
        total_terbanyak=hasil[0]["total"] if hasil else 0,
    )


@laporan_bp.route("/mahasiswa-aktif/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_mahasiswa_aktif():
    kunci = _periode_dari_request()
    baris = [
        [b["peringkat"], b["user"].nama_lengkap, b["user"].nim or b["user"].username,
         b["total"], b["judul_unik"], b["sedang_dipinjam"], b["terlambat"],
         b["terakhir"].strftime("%d-%m-%Y") if b["terakhir"] else "-"]
        for b in statistik_mahasiswa_peminjam(kunci)
    ]
    buffer = buat_excel(
        "Mahasiswa Aktif",
        ["Peringkat", "Mahasiswa", "NIM/Username", "Total Dipinjam", "Judul Berbeda",
         "Sedang Dipinjam", "Kali Terlambat", "Terakhir Meminjam"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True,
        download_name=f"mahasiswa_aktif_{kunci}_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def _daftar_terlambat():
    semua = (
        Peminjaman.query.filter_by(status="dipinjam")
        .order_by(Peminjaman.tanggal_jatuh_tempo.asc())
        .all()
    )
    return sorted((p for p in semua if p.hari_telat > 0), key=lambda p: p.hari_telat, reverse=True)


@laporan_bp.route("/terlambat")
@login_required
@role_required("staf", "kepala_perpustakaan")
def buku_terlambat():
    """Semua buku yang sudah lewat jatuh tempo dan belum kembali, terlama di atas."""
    daftar = _daftar_terlambat()
    total_denda = sum(denda_peminjaman(p) for p in daftar)
    return render_template("laporan/terlambat.html", daftar=daftar, total_denda=total_denda)


@laporan_bp.route("/terlambat/ekspor")
@login_required
@role_required("staf", "kepala_perpustakaan")
def ekspor_terlambat():
    baris = [
        [p.anggota.nama_lengkap, p.anggota.nim or p.anggota.username, p.anggota.no_telepon or "-",
         p.buku.judul, p.tanggal_jatuh_tempo.strftime("%d-%m-%Y"), p.hari_telat, denda_peminjaman(p)]
        for p in _daftar_terlambat()
    ]
    buffer = buat_excel(
        "Terlambat",
        ["Mahasiswa", "NIM/Username", "No. Telepon", "Buku", "Jatuh Tempo", "Hari Telat", "Denda Berjalan (Rp)"],
        baris,
    )
    return send_file(
        buffer, as_attachment=True, download_name=f"buku_terlambat_{date.today().isoformat()}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
```


## `Website/routes/peminjaman.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
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
```


## `Website/routes/pengaturan.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required

from utils.decorators import role_required
from utils.pengaturan import DAFTAR, nilai_saat_ini, simpan_pengaturan

pengaturan_bp = Blueprint("pengaturan", __name__, url_prefix="/pengaturan")


@pengaturan_bp.route("/", methods=["GET", "POST"])
@login_required
@role_required("kepala_perpustakaan")
def halaman():
    if request.method == "POST":
        baru, galat = {}, []
        for kunci, _cfg, minimum, maksimum, label, satuan, _bantuan in DAFTAR:
            mentah = request.form.get(kunci, "").strip().replace(".", "")
            try:
                nilai = int(mentah)
            except ValueError:
                galat.append(f"{label}: isi dengan angka bulat.")
                continue
            if not (minimum <= nilai <= maksimum):
                galat.append(f"{label}: harus antara {minimum} dan {maksimum}.")
                continue
            baru[kunci] = nilai

        if galat:
            for g in galat:
                flash(g, "danger")
        else:
            simpan_pengaturan(baru)
            flash("Pengaturan disimpan. Berlaku untuk peminjaman berikutnya; "
                  "peminjaman yang sudah berjalan tidak berubah jatuh temponya.", "success")
        return redirect(url_for("pengaturan.halaman"))

    nilai = nilai_saat_ini(current_app)
    kolom = [
        {"kunci": k, "label": label, "satuan": satuan, "bantuan": bantuan,
         "min": mn, "maks": mx, "nilai": nilai[k]}
        for k, _c, mn, mx, label, satuan, bantuan in DAFTAR
    ]
    return render_template("pengaturan/halaman.html", kolom=kolom)
```


## `Website/schema.sql`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```sql
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
```


## `Website/seed_admin.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
import getpass
from app import create_app
from extensions import db
from models import User

app = create_app()

with app.app_context():
    print("=== Buat Akun Kepala Perpustakaan Pertama ===")
    if User.query.filter_by(role="kepala_perpustakaan").first():
        print("Sudah ada akun kepala perpustakaan di database. Tidak perlu membuat lagi.")
    else:
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        nama_lengkap = input("Nama Lengkap: ").strip()
        password = getpass.getpass("Password: ")

        if User.query.filter_by(username=username).first():
            print("Username sudah dipakai. Batal.")
        else:
            user = User(username=username, email=email, nama_lengkap=nama_lengkap, role="kepala_perpustakaan")
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Akun operator '{username}' berhasil dibuat. Silakan login lewat halaman /auth/login.")
```


## `Website/static/css/mobile.css`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```css
/* =========================================================
   mobile.css - tampilan HP (dimuat SETELAH style.css)
   - Bottom navigation bar (tab bawah) per role
   - Tabel otomatis berubah jadi kartu (label diisi via JS di base.html)
   - Menu staf jadi drawer geser dari kiri
   - Tombol & input nyaman disentuh (>= 44px, font 16px anti-zoom iOS)
   Semua warna memakai variabel tema, jadi dark mode ikut otomatis.
   ========================================================= */

.bottom-nav { display: none; }
.detail-buku { display: flex; gap: 1.5rem; }

/* ---------- Drawer menu staf (<= 860px) ---------- */
@media (max-width: 860px) {
  .navbar-links {
    position: fixed; top: 0; left: 0; bottom: 0;
    width: min(82vw, 300px);
    margin: 0;
    padding: 1rem 0.6rem calc(1rem + env(safe-area-inset-bottom));
    display: flex; flex-direction: column; align-items: stretch; gap: 0.15rem;
    background: var(--primary-dark);
    border-top: none;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    overflow-y: auto;
    z-index: 160;
    transform: translateX(-105%);
    visibility: hidden;
    transition: transform 0.22s ease, visibility 0s linear 0.22s;
  }
  .navbar-links.open {
    transform: none; visibility: visible;
    transition: transform 0.22s ease;
    box-shadow: 8px 0 30px rgba(0, 0, 0, 0.35);
  }
  .navbar-links a, .nav-link { padding: 0.75rem 0.7rem; font-size: 0.92rem; }
  #navOverlay { z-index: 90; }
}

/* ---------- Layar HP (<= 700px) ---------- */
@media (max-width: 700px) {
  :root { --bn-h: 60px; }

  body[class*="role-"] { padding-bottom: calc(var(--bn-h) + env(safe-area-inset-bottom)); }
  body[class*="role-"] .hamburger, body.guest .hamburger { display: none; }

  /* Navbar ringkas */
  .navbar {
    flex-wrap: nowrap;
    padding: 0.5rem 0.8rem;
    padding-top: calc(0.5rem + env(safe-area-inset-top));
  }
  .navbar-left { min-width: 0; flex: 1; }
  .navbar .brand { min-width: 0; font-size: 0.9rem; }
  .navbar .brand span { overflow: hidden; text-overflow: ellipsis; }
  .navbar-right { gap: 0.4rem; flex-shrink: 0; }
  .theme-toggle, .navbar .btn-logout { width: 38px; height: 38px; padding: 0; justify-content: center; }

  /* Bottom navigation */
  .bottom-nav {
    display: flex;
    position: fixed; left: 0; right: 0; bottom: 0;
    z-index: 95;
    padding: 0 0.25rem env(safe-area-inset-bottom);
    background: var(--card-bg);
    border-top: 1px solid var(--border);
    box-shadow: 0 -4px 16px rgba(30, 20, 16, 0.08);
  }
  .bottom-nav a, .bottom-nav button {
    position: relative;
    flex: 1; min-width: 0; height: var(--bn-h);
    display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.25rem;
    background: none; border: none; cursor: pointer;
    color: var(--muted); text-decoration: none;
    font-family: inherit; font-size: 0.68rem; font-weight: 600;
    -webkit-tap-highlight-color: transparent;
  }
  .bottom-nav .nav-icon { width: 1.4rem; height: 1.4rem; }
  .bottom-nav a.active { color: var(--primary); }
  [data-theme="dark"] .bottom-nav a.active { color: var(--accent); }
  .bottom-nav a.active::before {
    content: ""; position: absolute; top: 0; left: 30%; right: 30%;
    height: 3px; border-radius: 0 0 3px 3px; background: currentColor;
  }
  .bn-badge {
    position: absolute; top: 0.45rem; left: calc(50% + 0.4rem);
    min-width: 1.05rem; height: 1.05rem; padding: 0 0.3rem;
    display: flex; align-items: center; justify-content: center;
    border-radius: 999px; background: var(--danger-solid); color: #fff;
    font-size: 0.62rem; font-weight: 700;
  }

  /* Ukuran & jarak */
  .container { padding: 0 0.8rem; margin: 0.9rem auto; }
  h2, .page-head h2 { font-size: 1.3rem; line-height: 1.25; }
  .card { padding: 1rem; border-radius: 14px; }
  .hero { border-radius: 16px; }
  .grid-3 { gap: 0.7rem; }
  .footer { padding: 1rem 1rem 1.5rem; font-size: 0.74rem; }

  /* Sentuhan nyaman */
  input, select, textarea { font-size: 16px; min-height: 44px; }
  textarea { min-height: 88px; }
  .btn { min-height: 44px; display: inline-flex; align-items: center; justify-content: center; gap: 0.4rem; }
  .btn.btn-sm { min-height: 38px; }
  .btn.btn-icon { width: 38px; height: 38px; min-height: 0; }
  .card form .form-group ~ .btn { width: 100%; margin-top: 0.4rem; }

  /* Pencarian & filter */
  .search-bar { flex-direction: row !important; flex-wrap: wrap; gap: 0.45rem; }
  .search-bar .search-field, .search-bar input, .search-bar select { flex: 1 1 100%; width: 100%; }
  .search-bar .btn { width: auto; flex: 1 1 auto; }
  .search-bar > a.btn { flex: 1 1 100%; }
  .search-bar .chip { flex: 0 0 auto; }
  .kategori-chips {
    flex-wrap: nowrap; overflow-x: auto; margin: 0 -0.8rem 1.2rem; padding: 0 0.8rem 0.4rem;
    scrollbar-width: none; scroll-snap-type: x proximity;
  }
  .kategori-chips::-webkit-scrollbar { display: none; }
  .kategori-chips .chip { flex: 0 0 auto; scroll-snap-align: start; }

  /* Kartu buku */
  .buku-card { border-radius: 14px; }
  .buku-card-cover { margin: 0.45rem 0.45rem 0; border-radius: 10px; box-shadow: 0 4px 10px rgba(30, 20, 16, 0.2); }
  .buku-card-cover::before { display: none; }
  .buku-card-actions .btn { min-height: 38px; }

  /* Pengajuan, kartu anggota */
  .pengajuan-grid { grid-template-columns: 1fr; }
  .pengajuan-actions .btn, .kartu-wrap-actions .btn { flex: 1 1 auto; min-height: 40px; }

  /* Detail buku: susun vertikal */
  .detail-buku { flex-direction: column; gap: 1rem; }
  .detail-buku > div:first-child { align-self: center; }
  .detail-buku .btn { display: flex; width: 100%; margin-top: 0.5rem; }

  /* Login / registrasi */
  .card[style*="margin:2rem auto"] { margin: 1rem auto !important; }

  /* Modal crop sampul jadi bottom sheet */
  .crop-modal { align-items: flex-end; padding: 0; }
  .crop-modal-box { max-width: none; border-radius: 18px 18px 0 0; padding: 1.1rem 1rem calc(1rem + env(safe-area-inset-bottom)); }
  .crop-modal-actions .btn { flex: 1; }

  /* ---------- TABEL -> KARTU ---------- */
  .card:has(.tbl-stack) { background: transparent; border: none; box-shadow: none; padding: 0; }
  .tbl-stack { min-width: 0 !important; margin: 0; }
  .tbl-stack thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
  .tbl-stack, .tbl-stack tbody, .tbl-stack tr, .tbl-stack td { display: block; width: 100%; }
  .tbl-stack tr, .tbl-stack tbody tr:hover {
    background: var(--card-bg);
  }
  .tbl-stack tr {
    border: 1px solid var(--border); border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 0.3rem 0.95rem; margin-bottom: 0.75rem; overflow: hidden;
  }
  .tbl-stack td {
    display: flex; justify-content: space-between; align-items: center; gap: 1rem;
    padding: 0.55rem 0; border-bottom: 1px dashed var(--border);
    font-size: 0.86rem; text-align: right;
  }
  .tbl-stack td:last-child { border-bottom: none; }
  .tbl-stack td[data-label]::before {
    content: attr(data-label);
    flex: 0 0 36%; max-width: 36%; text-align: left;
    color: var(--muted); font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.03em;
  }
  .cell-v { min-width: 0; overflow-wrap: anywhere; }
  /* sel pertama = judul kartu */
  .tbl-stack td:first-child {
    justify-content: flex-start; text-align: left;
    font-weight: 700; font-size: 0.95rem; padding-top: 0.7rem;
    border-bottom: 1px solid var(--border);
  }
  .tbl-stack td:first-child::before { display: none; }
  /* sel aksi: tombol memenuhi lebar kartu */
  .tbl-stack td[data-label="Aksi"] { display: block; text-align: left; padding: 0.7rem 0 0.5rem; }
  .tbl-stack td[data-label="Aksi"]::before { display: none; }
  .tbl-stack td[data-label="Aksi"] .cell-v { display: flex; flex-wrap: wrap; gap: 0.4rem; }
  .tbl-stack td form { display: inline-block; margin: 0; }
  .tbl-stack td .btn.btn-sm { min-height: 38px; padding: 0.4rem 0.85rem; }
  .tbl-stack td.tbl-empty { display: block; text-align: center; color: var(--muted); padding: 1.2rem 0; }
  .tbl-stack td.tbl-empty::before { display: none; }

  /* Denda, pengaturan, stok */
  .setting-row { flex-direction: column; align-items: stretch; gap: 0.5rem; }
  .setting-input { flex-shrink: 1; }
  .setting-input input, .setting-input select { width: 100%; flex: 1; text-align: left; }
  .form-stok { width: 100%; }
  .form-stok input { flex: 0 0 5.5rem; width: 5.5rem; }
  .form-stok select { flex: 1 1 8rem; min-width: 0; }
  .form-stok .btn { flex: 1 1 100%; }
  .aksi-atur { display: block; width: 100%; }
  .aksi-atur form { position: static; margin-top: 0.4rem; box-shadow: none; flex-wrap: wrap; }
  .aksi-atur input[type="date"] { flex: 1; min-width: 0; }
  .tbl-stack td .aksi-baris { width: 100%; }
  .tbl-stack td .aksi-baris form { display: flex; flex: 1 1 auto; gap: 0.4rem; }
  .tbl-stack td .aksi-baris form .btn { flex: 1; }
  .stat-box .angka.angka-rp { font-size: 1.05rem; }
  .pengajuan-actions form { width: 100%; }
  .pengajuan-actions form .btn { flex: 1; }

  /* Tabel mode profesional (Excel) tetap geser, beri petunjuk */
  .excel-card .table-scroll { max-height: 65vh; }
}

/* Layar sentuh: matikan efek "naik" saat hover */
@media (hover: none) {
  .card:hover, .stat-box:hover, .kategori-card:hover, .pengajuan-card:hover, .buku-card:hover {
    transform: none; box-shadow: var(--shadow);
  }
}
```


## `Website/static/css/style.css`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```css
/* =========================================================
   Perpustakaan STIKOM Kendari - stylesheet
   Warna diambil dari sampel piksel logo (maroon ring, emas
   pada buku/globe, biru globe). Dipakai apa adanya sebagai
   variabel CSS, disesuaikan tipis untuk kontras teks & border.
   ========================================================= */
:root {
  --primary: #5c211d;        /* maroon logo (ring luar), dipakai utk teks/aksen */
  --primary-dark: #3c1512;   /* maroon gelap - navbar, sidebar, tombol utama */
  --primary-light: #7d4038;
  --accent: #96690f;         /* emas logo, digelapkan dari #fff001 asli supaya kontras teks aman */
  --accent-dark: #74510b;
  --logo-blue: #3a5e8c;      /* biru globe pada logo */

  --bg: #f4f2ef;
  --card-bg: #ffffff;
  --border: #e1dad2;
  --text: #262220;
  --muted: #756b64;

  --danger: #a7291f;
  --warning: #8a5c0c;
  --success: #276b3f;
  --info: #3a5e8c;

  /* Varian "solid" - dipakai KHUSUS utk latar tombol/badge berisi teks putih.
     Nilainya sengaja TIDAK ditimpa di dark mode (lihat blok [data-theme="dark"]
     di bawah) supaya kontras teks putih di atasnya tetap aman di kedua mode -
     berbeda dari --primary/--accent/--danger dst. di atas yang memang dibuat
     lebih terang khusus utk mode gelap agar terbaca sebagai TEKS/border di
     atas latar gelap, bukan utk jadi latar solid. */
  --primary-solid: #5c211d;
  --accent-solid: #96690f;
  --danger-solid: #a7291f;
  --warning-solid: #8a5c0c;
  --success-solid: #276b3f;
  --info-solid: #3a5e8c;
  --logo-blue-solid: #3a5e8c;

  --shadow: 0 1px 2px rgba(30, 20, 16, 0.08);
  --radius: 6px;
  --radius-sm: 4px;
  --transition: 0.15s ease;

  /* Token khusus statistik & grafik: kontras dijamin di kedua tema */
  --radius-lg: 14px;
  --stat-angka: #5c211d;              /* maroon pekat di atas kartu putih */
  --stat-label: #5a504a;
  --chart-text: #3a322e;
  --chart-grid: rgba(60, 40, 30, 0.12);
  --surface-2: #faf8f6;
}

[data-theme="dark"] {
  --primary: #b9776a;
  --primary-dark: #6e2f27;
  --primary-light: #cf9f92;
  --accent: #c69c47;
  --accent-dark: #a17f39;
  --logo-blue: #7d9fc7;

  --bg: #17130f;
  --card-bg: #221c19;
  --border: #392e29;
  --text: #ece4de;
  --muted: #a89a90;

  --danger: #d97268;
  --warning: #d1a24d;
  --success: #58a97c;
  --info: #7d9fc7;

  --shadow: 0 1px 3px rgba(0, 0, 0, 0.45);

  --stat-angka: #f1cf83;              /* emas terang di atas kartu gelap */
  --stat-label: #cfc3ba;
  --chart-text: #e8dfd8;
  --chart-grid: rgba(255, 255, 255, 0.12);
  --surface-2: #2a2320;
}

* { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  transition: background var(--transition), color var(--transition);
  -webkit-font-smoothing: antialiased;
}

a { color: var(--primary); }

h1, h2, h3, h4 {
  font-family: inherit;
  font-weight: 600;
}
h1, h2, h3 { color: var(--primary); }
[data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3 { color: var(--accent); }

.page-head { margin-bottom: 1.2rem; }
.page-head h2 { margin-bottom: 0.2rem; }
.page-sub { color: var(--muted); font-size: 0.92rem; margin: 0; }

/* ---------------- NAVBAR ---------------- */
.navbar {
  background: var(--primary-dark);
  color: #fff;
  padding: 0.55rem 1.3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  gap: 0.8rem;
}

.navbar-left { display: flex; align-items: center; gap: 0.8rem; }

.navbar .brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 600;
  font-size: 1rem;
  color: #fff;
  text-decoration: none;
  white-space: nowrap;
}
.navbar .brand img {
  height: 34px;
  width: 34px;
  border-radius: 50%;
  background: #fff;
  padding: 2px;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.navbar-links {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.1rem;
}

.navbar-links a,
.nav-link {
  color: #e9ddd2;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.5rem 0.65rem;
  border-radius: var(--radius-sm);
  border-bottom: 2px solid transparent;
  transition: background var(--transition), color var(--transition), border-color var(--transition);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: none;
  border-top: none; border-left: none; border-right: none;
  cursor: pointer;
  font-family: inherit;
}
.navbar-links a:hover,
.nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}
.navbar-links a.active,
.nav-link.active {
  color: #fff;
  font-weight: 600;
  border-bottom-color: var(--accent);
}

/* ---------------- IKON SVG ---------------- */
.nav-icon, .icon {
  width: 1.05em;
  height: 1.05em;
  flex-shrink: 0;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  vertical-align: -0.2em;
}
.side-caret, .nav-caret {
  width: 0.85em;
  height: 0.85em;
  flex-shrink: 0;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.8;
  transition: transform var(--transition);
}
.side-group.open .side-caret,
.nav-dropdown.open .nav-caret,
.nav-dropdown-toggle:hover .nav-caret { transform: rotate(180deg); }

/* ---------------- NAVBAR DROPDOWN ---------------- */
.nav-dropdown { position: relative; }

.nav-dropdown-menu {
  display: none;
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  min-width: 190px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  box-shadow: 0 4px 14px rgba(0,0,0,0.14);
  padding: 0.3rem;
  z-index: 200;
  flex-direction: column;
  gap: 0.05rem;
}
.nav-dropdown.open .nav-dropdown-menu { display: flex; }

.nav-dropdown-menu a {
  color: var(--text) !important;
  padding: 0.5rem 0.6rem;
  border-radius: var(--radius-sm);
  font-size: 0.86rem;
  font-weight: 500;
  border-bottom: none !important;
}
.nav-dropdown-menu a:hover,
.nav-dropdown-menu a.active {
  background: rgba(92, 33, 29, 0.08) !important;
  color: var(--primary) !important;
}
[data-theme="dark"] .nav-dropdown-menu a:hover,
[data-theme="dark"] .nav-dropdown-menu a.active {
  background: rgba(198, 156, 71, 0.12) !important;
  color: var(--accent) !important;
}

.navbar-right { display: flex; align-items: center; gap: 0.6rem; }

/* ---- Info user (kanan atas): avatar bundar berinisial + nama + peran ---- */
.navbar .user-card {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.25rem 0.85rem 0.25rem 0.3rem;
  background: rgba(255, 255, 255, 0.09);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  color: #fff;
  text-decoration: none;
  min-width: 0;
  transition: background var(--transition), border-color var(--transition);
}
.navbar a.user-card-link:hover { background: rgba(255, 255, 255, 0.17); border-color: rgba(255, 255, 255, 0.28); }
.user-avatar {
  flex-shrink: 0;
  width: 2.15rem; height: 2.15rem;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: #e0b458;
  color: #2a1a04;
  font-size: 0.82rem; font-weight: 800; letter-spacing: 0.02em;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.22);
}
.avatar-staf { background: #9db8dc; color: #10233a; }
.avatar-kepala_perpustakaan { background: #f4e9d8; color: #5c211d; }
.user-meta { display: flex; flex-direction: column; line-height: 1.2; min-width: 0; }
.user-name {
  font-size: 0.84rem; font-weight: 600; color: #fff;
  max-width: 170px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.user-role { font-size: 0.68rem; font-weight: 500; color: #e6cf9f; letter-spacing: 0.03em; }

.navbar .btn-logout {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.42rem 0.9rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #fff;
  font-size: 0.82rem; font-weight: 600;
  text-decoration: none;
  transition: background var(--transition), border-color var(--transition);
}
.navbar .btn-logout:hover { background: var(--danger-solid); border-color: var(--danger-solid); }

.theme-toggle {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.14);
  color: #fff;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition);
}
.theme-toggle:hover { background: rgba(255,255,255,0.22); }

.hamburger {
  display: none;
  background: none;
  border: none;
  color: #fff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.2rem 0.5rem;
}

/* ---------------- LAYOUT ---------------- */
.container {
  max-width: 1100px;
  margin: 1.5rem auto;
  padding: 0 1rem;
}

.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1.5rem;
  margin-bottom: 1.2rem;
  box-shadow: var(--shadow);
  transition: background var(--transition), border-color var(--transition);
}

/* ---------------- TABEL ---------------- */
.table-scroll { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
  min-width: 480px;
}

th, td {
  padding: 0.6rem 0.65rem;
  border-bottom: 1px solid var(--border);
  text-align: left;
  font-size: 0.9rem;
}

th { background: rgba(92, 33, 29, 0.06); color: var(--primary); font-weight: 600; }
[data-theme="dark"] th { background: rgba(198, 156, 71, 0.08); color: var(--accent); }

tbody tr { transition: background var(--transition); }
tbody tr:hover { background: rgba(92, 33, 29, 0.04); }
[data-theme="dark"] tbody tr:hover { background: rgba(198, 156, 71, 0.05); }

/* ---------------- TOMBOL ---------------- */
.btn {
  display: inline-block;
  padding: 0.55rem 1.05rem;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  background: var(--primary-solid);
  color: #fff;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.87rem;
  font-weight: 500;
  font-family: inherit;
  transition: background var(--transition), border-color var(--transition), transform 0.12s ease, box-shadow var(--transition);
}
.btn:hover { background: var(--primary-dark); box-shadow: 0 3px 10px rgba(30, 20, 16, 0.18); transform: translateY(-1px); }
.btn:active { transform: translateY(0) scale(0.97); box-shadow: none; }
.btn-accent { background: var(--accent-solid); color: #fff; }
.btn-accent:hover { background: var(--accent-dark); }
.btn-danger { background: var(--danger-solid); }
.btn-warning { background: var(--warning-solid); color: #fff; }
.btn-sm { padding: 0.32rem 0.6rem; font-size: 0.79rem; }
.btn-muted { background: var(--muted); }

/* ---------------- FORM ---------------- */
.form-group { margin-bottom: 0.9rem; }
label { display: block; margin-bottom: 0.3rem; font-weight: 600; font-size: 0.87rem; color: var(--text); }
input, select, textarea {
  width: 100%;
  padding: 0.55rem 0.6rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.92rem;
  background: var(--card-bg);
  color: var(--text);
  transition: border-color var(--transition), box-shadow var(--transition);
}
input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(92, 33, 29, 0.12);
}
[data-theme="dark"] input:focus, [data-theme="dark"] select:focus, [data-theme="dark"] textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(198, 156, 71, 0.16);
}

/* ---------------- BADGE / FLASH ---------------- */
.badge {
  display: inline-block;
  padding: 0.16rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.74rem;
  font-weight: 600;
  color: #fff;
}
.badge-success { background: var(--success-solid); }
.badge-danger { background: var(--danger-solid); }
.badge-warning { background: var(--warning-solid); color: #fff; }
.badge-info { background: var(--info-solid); }

.flash {
  padding: 0.7rem 1rem;
  border-radius: var(--radius-sm);
  margin-bottom: 0.7rem;
  font-size: 0.9rem;
  border-left: 3px solid transparent;
}
.flash-success { background: rgba(39,107,63,0.1); color: var(--success); border-color: var(--success); }
.flash-danger  { background: rgba(167,41,31,0.08); color: var(--danger); border-color: var(--danger); }
.flash-warning { background: rgba(138,92,12,0.1); color: var(--warning); border-color: var(--warning); }
.flash-info    { background: rgba(58,94,140,0.08); color: var(--info); border-color: var(--info); }

/* ---------------- STAT BOX / DASHBOARD ---------------- */
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; }
.stat-box {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  column-gap: 0.9rem;
  align-items: center;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1rem 1.1rem 1rem 1.25rem;
  box-shadow: var(--shadow);
  overflow: hidden;
  --tone: var(--primary);
}
.stat-box::before {
  content: "";
  position: absolute; left: 0; top: 0; bottom: 0;
  width: 4px;
  background: var(--tone);
}
.stat-icon {
  grid-row: 1 / span 2;
  width: 2.8rem; height: 2.8rem;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: var(--tone);
  background: rgba(128, 128, 128, 0.14);
  background: color-mix(in srgb, var(--tone) 16%, transparent);
  transition: transform 0.25s ease;
}
.stat-icon .icon { width: 1.3rem; height: 1.3rem; }
.stat-box:hover .stat-icon { transform: scale(1.1) rotate(-6deg); }
/* warna ikon mengikuti arti data (theme-aware lewat variabel yang sudah ada) */
.tone-maroon { --tone: var(--primary); }
.tone-gold   { --tone: var(--accent); }
.tone-blue   { --tone: var(--info); }
.tone-green  { --tone: var(--success); }
.tone-red    { --tone: var(--danger); }
.tone-amber  { --tone: var(--warning); }
.stat-box:has(.tone-maroon) { --tone: var(--primary); }
.stat-box:has(.tone-gold)   { --tone: var(--accent); }
.stat-box:has(.tone-blue)   { --tone: var(--info); }
.stat-box:has(.tone-green)  { --tone: var(--success); }
.stat-box:has(.tone-red)    { --tone: var(--danger); }
.stat-box:has(.tone-amber)  { --tone: var(--warning); }
/* !important: angka statistik tidak boleh tertimpa warna lain -> selalu kontras */
.stat-box .angka {
  font-size: 1.9rem;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.01em;
  color: var(--stat-angka) !important;
  font-variant-numeric: tabular-nums;
  align-self: end;
}
.stat-box .label {
  color: var(--stat-label) !important;
  font-size: 0.84rem;
  font-weight: 500;
  margin-top: 0.2rem;
  align-self: start;
}

/* ---------------- SAMPUL BUKU ---------------- */
.buku-cover { width: 90px; height: 130px; object-fit: cover; border-radius: var(--radius-sm); border: 1px solid var(--border); }
.buku-cover-placeholder {
  width: 90px; height: 130px; border-radius: var(--radius-sm); border: 1px dashed var(--border);
  display: flex; align-items: center; justify-content: center; color: var(--muted); font-size: 0.72rem; text-align: center;
  padding: 0.3rem;
}

/* ---------------- KARTU ANGGOTA ---------------- */
.kartu-anggota {
  max-width: 380px;
  background: var(--primary-dark);
  color: #fff;
  border-radius: var(--radius);
  border-top: 4px solid var(--accent);
  padding: 1.3rem 1.5rem;
  box-shadow: var(--shadow);
  position: relative;
}
.kartu-anggota .nomor { font-size: 1.2rem; letter-spacing: 1.5px; margin: 0.6rem 0; color: var(--accent); font-weight: 700; }
.kartu-anggota .label { font-size: 0.72rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 0.04em; }
.kartu-anggota .logo-kecil { height: 40px; margin-bottom: 0.5rem; }
.kartu-anggota .role-pita {
  position: absolute; top: 0.9rem; right: 1.1rem;
  font-size: 0.66rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
  background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25);
  padding: 0.2rem 0.6rem; border-radius: var(--radius-sm);
}

/* varian warna kartu per role */
.kartu-role-staf { background: var(--logo-blue-solid); border-top-color: #fff; }
.kartu-role-kepala { background: #241412; border-top-color: var(--accent); }

.kartu-wrap-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem; }

/* ---------------- HALAMAN CETAK KARTU ---------------- */
.cetak-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem 1rem;
  background: var(--bg);
}
.cetak-hint { color: var(--muted); font-size: 0.82rem; text-align: center; max-width: 380px; }
@media print {
  .cetak-no-print { display: none !important; }
  .cetak-page { padding: 0; background: #fff; min-height: 0; }
  body { background: #fff; }
}

/* ---------------- PENCARIAN ---------------- */
.search-bar { display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; align-items: center; }
.search-bar input, .search-bar select { width: auto; flex: 1; min-width: 150px; }
.search-field { position: relative; flex: 1; min-width: 220px; }
.search-field .icon {
  position: absolute; left: 0.95rem; top: 50%;
  transform: translateY(-50%);
  width: 1.05rem; height: 1.05rem;
  color: var(--muted); pointer-events: none;
}
.search-bar .search-field input {
  width: 100%; padding: 0.7rem 1rem 0.7rem 2.6rem;
  border-radius: 999px; background: var(--card-bg);
  box-shadow: var(--shadow);
}
.search-bar .btn { border-radius: 999px; padding-left: 1.2rem; padding-right: 1.2rem; }

/* ---------------- CHIP KATEGORI ---------------- */
.kategori-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.8rem;
}
.chip {
  display: inline-block;
  padding: 0.42rem 0.95rem;
  border-radius: 999px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 0.83rem;
  font-weight: 500;
  text-decoration: none;
  transition: background var(--transition), color var(--transition), border-color var(--transition), transform var(--transition);
}
.chip:hover { border-color: var(--primary); color: var(--primary); transform: translateY(-1px); }
[data-theme="dark"] .chip:hover { border-color: var(--accent); color: var(--accent); }
.chip-active {
  background: var(--primary-solid);
  border-color: var(--primary-solid);
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(92, 33, 29, 0.28);
}
.chip-active:hover { color: #fff !important; }
[data-theme="dark"] .chip-active { background: var(--accent); border-color: var(--accent); color: #201804 !important; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); }
[data-theme="dark"] .chip-active:hover { color: #201804 !important; }

/* ---------------- RAK BUKU ---------------- */
.rak-section { margin-bottom: 2.6rem; }
.rak-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.75rem;
  margin-bottom: 1.3rem;
}
.rak-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 1.12rem;
}
.rak-icon {
  width: 2.1rem; height: 2.1rem; padding: 0.5rem;
  border-radius: 10px;
  background: rgba(92, 33, 29, 0.09);
  color: var(--primary);
}
[data-theme="dark"] .rak-icon { background: rgba(198, 156, 71, 0.14); color: var(--accent); }
.rak-count {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--stat-label);
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 0.22rem 0.7rem;
  border-radius: 999px;
  white-space: nowrap;
}

.buku-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(176px, 1fr));
  gap: 1.5rem 1.25rem;
}

/* ---- Kartu buku modern: sampul menonjol, badge stok pill, aksi jelas ---- */
.buku-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
}
.buku-card:hover { border-color: var(--primary); }
[data-theme="dark"] .buku-card:hover { border-color: var(--accent); }

.buku-card-cover {
  position: relative;
  display: block;
  margin: 0.6rem 0.6rem 0;
  aspect-ratio: 2 / 3;
  border-radius: 12px;
  overflow: hidden;
  background: var(--surface-2);
  text-decoration: none;
  box-shadow: 0 8px 18px rgba(30, 20, 16, 0.22);
}
/* efek punggung buku di sisi kiri */
.buku-card-cover::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(90deg, rgba(0,0,0,0.28) 0, rgba(255,255,255,0.14) 4px, rgba(0,0,0,0) 12px);
  pointer-events: none;
}
/* overlay "Lihat detail" saat kartu di-hover */
.buku-card-cover::before {
  content: "Lihat detail";
  position: absolute; left: 0; right: 0; bottom: 0; z-index: 2;
  padding: 1.6rem 0.5rem 0.65rem;
  background: linear-gradient(0deg, rgba(20,12,9,0.85), rgba(20,12,9,0));
  color: #fff; font-size: 0.78rem; font-weight: 600; text-align: center;
  opacity: 0; transform: translateY(6px);
  transition: opacity 0.2s ease, transform 0.2s ease;
  pointer-events: none;
}
.buku-card:hover .buku-card-cover::before { opacity: 1; transform: none; }
.buku-card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* sampul pengganti: gradasi warna + inisial judul */
.buku-card-cover .buku-cover-placeholder {
  width: 100%; height: 100%; border: none; border-radius: 0;
  flex-direction: column; gap: 0.35rem;
  color: #fff;
  background: linear-gradient(145deg, #5c211d, #8a3a2f);
}
.buku-card-cover .cover-v1 { background: linear-gradient(145deg, #3a5e8c, #24405f); }
.buku-card-cover .cover-v2 { background: linear-gradient(145deg, #96690f, #6b4a08); }
.buku-card-cover .cover-v3 { background: linear-gradient(145deg, #276b3f, #184a2b); }
.cover-inisial { font-size: 2.8rem; font-weight: 800; line-height: 1; text-shadow: 0 2px 8px rgba(0,0,0,0.3); }
.cover-ket { font-size: 0.64rem; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.85; }

/* badge stok (pill di kiri atas) */
.buku-stok-badge {
  position: absolute; z-index: 3;
  top: 0.55rem; left: 0.55rem;
  display: inline-flex; align-items: center; gap: 0.35rem;
  background: rgba(20, 14, 11, 0.78);
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
  color: #fff;
  font-size: 0.68rem;
  font-weight: 600;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
}
.buku-stok-badge::before {
  content: ""; width: 0.45rem; height: 0.45rem; border-radius: 50%;
  background: #5fd08a;
}
.buku-stok-badge.stok-habis { background: rgba(120, 22, 15, 0.9); }
.buku-stok-badge.stok-habis::before { background: #ff9a90; }

.buku-card-body { padding: 0.8rem 0.9rem 0.95rem; display: flex; flex-direction: column; gap: 0.2rem; flex: 1; }
.buku-judul {
  font-weight: 650;
  font-size: 0.95rem;
  color: var(--text) !important;
  text-decoration: none;
  line-height: 1.32;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.5em;
}
.buku-judul:hover { color: var(--primary) !important; }
[data-theme="dark"] .buku-judul:hover { color: var(--accent) !important; }
.buku-penulis { font-size: 0.8rem; color: var(--muted); }
.buku-meta { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.35rem; }
.buku-meta span {
  font-size: 0.68rem; font-weight: 500;
  color: var(--stat-label);
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 0.1rem 0.5rem; border-radius: 999px;
  max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.buku-card-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: auto; padding-top: 0.75rem; }
.buku-card-actions > * { flex: 1 1 auto; text-align: center; }
.buku-card-actions form { display: flex; }
.buku-card-actions form .btn { width: 100%; }

/* ---------------- GRID KATEGORI ---------------- */
.kategori-form-card { max-width: 620px; }
.kategori-form { display: flex; gap: 0.6rem; flex-wrap: wrap; }
.kategori-form input { flex: 1; min-width: 200px; }

.kategori-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}
.kategori-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.3rem 1rem;
  text-align: center;
  text-decoration: none;
  box-shadow: var(--shadow);
  transition: border-color var(--transition);
}
.kategori-card:hover { border-color: var(--primary); }
[data-theme="dark"] .kategori-card:hover { border-color: var(--accent); }
.kategori-icon { font-size: 1.7rem; margin-bottom: 0.4rem; }
.kategori-nama { font-weight: 600; color: var(--text); font-size: 0.95rem; }
.kategori-jumlah { font-size: 0.78rem; color: var(--muted); margin-top: 0.2rem; }

/* ---------------- EMPTY STATE ---------------- */
.empty-state { text-align: center; padding: 2.2rem 1rem; color: var(--muted); }
.empty-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }

/* ---------------- UPLOADER SAMPUL ---------------- */
.sampul-uploader { display: flex; gap: 1rem; align-items: flex-start; flex-wrap: wrap; }
.sampul-preview-box { flex-shrink: 0; }
.sampul-uploader-actions { flex: 1; min-width: 180px; }
.sampul-hint { font-size: 0.78rem; color: var(--muted); margin: 0.4rem 0 0; }

/* ---------------- MODAL CROP SAMPUL ---------------- */
.crop-modal {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 1000;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}
.crop-modal.open { display: flex; }
.crop-modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(20, 15, 13, 0.6);
}
.crop-modal-box {
  position: relative;
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 1.2rem;
  max-width: 480px;
  width: 100%;
  box-shadow: 0 12px 30px rgba(0,0,0,0.3);
}
.crop-modal-box h3 { margin: 0 0 0.8rem; font-size: 1.05rem; }
.crop-modal-image-wrap {
  width: 100%;
  max-height: 60vh;
  overflow: hidden;
  background: #111;
  border-radius: var(--radius-sm);
}
.crop-modal-image-wrap img { display: block; max-width: 100%; }
.crop-modal-hint { font-size: 0.78rem; color: var(--muted); margin: 0.6rem 0 0; }
.crop-modal-actions { display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 1rem; }

/* ---------------- LOADER TRANSISI ANTAR HALAMAN ---------------- */
.page-loader {
  position: fixed;
  inset: 0;
  z-index: 3000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: var(--bg);
  transition: opacity 0.25s ease, visibility 0s linear 0s;
}
.page-loader-logo {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #fff;
  padding: 6px;
  border: 2px solid var(--accent);
  animation: loaderPulse 1.1s ease-in-out infinite;
}
.page-loader-bar {
  width: 140px;
  height: 3px;
  border-radius: 2px;
  background: var(--border);
  overflow: hidden;
  position: relative;
}
.page-loader-bar::after {
  content: "";
  position: absolute;
  top: 0; left: -40%;
  height: 100%;
  width: 40%;
  border-radius: 2px;
  background: var(--accent);
  animation: loaderBar 1s ease-in-out infinite;
}
.page-loader-text {
  font-size: 0.8rem;
  color: var(--muted);
  letter-spacing: 0.03em;
}

@keyframes loaderPulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(150, 105, 15, 0.25); }
  50% { transform: scale(1.06); box-shadow: 0 0 0 8px rgba(150, 105, 15, 0); }
}
@keyframes loaderBar {
  0% { left: -40%; }
  100% { left: 100%; }
}

.page-loader-hidden {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.25s ease, visibility 0s linear 0.25s;
  pointer-events: none;
}

@media (prefers-reduced-motion: reduce) {
  .page-loader-logo, .page-loader-bar::after { animation: none; }
}

/* ---------------- ANIMASI (halus, hanya utk umpan-balik UI & transisi masuk) ---------------- */
@keyframes slideDown { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: none; } }

.nav-dropdown.open .nav-dropdown-menu { animation: slideDown 0.12s ease; }

/* Catatan: animasi masuk di bawah SENGAJA tidak mengubah opacity sama sekali
   (hanya transform/posisi) - supaya teks/angka selalu 100% terlihat sejak
   frame pertama, tidak pernah "nyangkut" transparan jika tab sempat tidak
   fokus saat halaman dimuat. */
@keyframes slideInSubtle {
  from { transform: translateY(8px); }
  to { transform: none; }
}
@keyframes spinOnce {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
@keyframes pulseSoft {
  0%, 100% { box-shadow: 0 0 0 0 rgba(167, 41, 31, 0.35); }
  50% { box-shadow: 0 0 0 5px rgba(167, 41, 31, 0); }
}

/* Kartu & kotak statistik bergeser halus ke posisi akhir saat halaman dimuat
   (tanpa perubahan opacity), ditunda bertahap (stagger) agar tidak "meloncat"
   bersamaan. */
.card, .stat-box, .buku-card, .kategori-card, .pengajuan-card {
  animation: slideInSubtle 0.35s ease both;
}
.grid-3 .stat-box:nth-child(1) { animation-delay: 0.02s; }
.grid-3 .stat-box:nth-child(2) { animation-delay: 0.06s; }
.grid-3 .stat-box:nth-child(3) { animation-delay: 0.1s; }
.grid-3 .stat-box:nth-child(4) { animation-delay: 0.14s; }
.grid-3 .stat-box:nth-child(5) { animation-delay: 0.18s; }
.grid-3 .stat-box:nth-child(6) { animation-delay: 0.22s; }
.chart-grid .chart-card:nth-child(1) { animation-delay: 0.04s; }
.chart-grid .chart-card:nth-child(2) { animation-delay: 0.09s; }
.chart-grid .chart-card:nth-child(3) { animation-delay: 0.14s; }

/* Kartu terasa "hidup" saat disentuh/hover: sedikit terangkat + bayangan menguat */
.card, .stat-box, .buku-card, .kategori-card, .pengajuan-card {
  transition: background var(--transition), border-color var(--transition),
              transform 0.18s ease, box-shadow 0.18s ease;
}
.card:hover, .stat-box:hover, .kategori-card:hover, .pengajuan-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(30, 20, 16, 0.12);
}
[data-theme="dark"] .card:hover,
[data-theme="dark"] .stat-box:hover,
[data-theme="dark"] .kategori-card:hover,
[data-theme="dark"] .pengajuan-card:hover {
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.4);
}
.buku-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(30, 20, 16, 0.18);
}
[data-theme="dark"] .buku-card:hover { box-shadow: 0 16px 32px rgba(0, 0, 0, 0.55); }
.buku-card-cover img { transition: transform 0.35s ease; }
.buku-card:hover .buku-card-cover img { transform: scale(1.06); }

/* Notifikasi flash bergeser halus masuk (tanpa perubahan opacity) */
.flash { animation: slideInSubtle 0.25s ease both; }

/* Badge "Terlambat" berdenyut halus supaya menarik perhatian tanpa mengganggu */
.badge-danger { animation: pulseSoft 2.2s ease-in-out infinite; }

/* Ikon tema (matahari/bulan) berputar singkat saat mode diganti */
.theme-toggle.spin-once svg { animation: spinOnce 0.4s ease; }

/* Hormati preferensi pengguna yang menonaktifkan animasi */
@media (prefers-reduced-motion: reduce) {
  .card, .stat-box, .buku-card, .kategori-card, .pengajuan-card,
  .flash, .badge-danger, .theme-toggle.spin-once svg {
    animation: none !important;
    transition: none !important;
  }
  .card:hover, .stat-box:hover, .kategori-card:hover, .pengajuan-card:hover, .buku-card:hover {
    transform: none;
  }
}

/* ---------------- FOOTER ---------------- */
.footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.8rem;
  padding: 1.5rem 1rem 2rem;
}

/* =========================================================
   RESPONSIVE / MOBILE
   ========================================================= */
@media (max-width: 860px) {
  .navbar { flex-wrap: wrap; }
  .hamburger { display: inline-flex; align-items: center; }

  .navbar-links {
    display: none;
    flex-direction: column;
    width: 100%;
    align-items: stretch;
    gap: 0.1rem;
    margin-top: 0.6rem;
    border-top: 1px solid rgba(255,255,255,0.12);
    padding-top: 0.5rem;
  }
  .navbar-links.open { display: flex; }
  .navbar-links a, .nav-link { padding: 0.6rem 0.4rem; width: 100%; border-bottom: none; border-left: 2px solid transparent; }
  .navbar-links a.active, .nav-link.active { border-left-color: var(--accent); border-bottom: none; background: rgba(255,255,255,0.06); }

  .navbar-right { margin-left: auto; }
  .user-meta { display: none; }                 /* HP: cukup avatar bundar */
  .navbar .user-card { padding: 0.2rem; }
  .navbar .btn-logout { padding: 0.5rem; }
  .navbar .btn-logout span { display: none; }

  .nav-dropdown-menu {
    display: none;
    position: static;
    box-shadow: none;
    border: none;
    background: rgba(0,0,0,0.14);
    margin: 0.1rem 0 0.1rem 1.2rem;
    min-width: 0;
  }
  .nav-dropdown.open .nav-dropdown-menu { display: flex; }
  .nav-dropdown-menu a { color: #e9ddd2 !important; }
  .nav-dropdown-menu a:hover, .nav-dropdown-menu a.active {
    background: rgba(255,255,255,0.1) !important;
    color: #fff !important;
  }
}

@media (max-width: 600px) {
  .container { padding: 0 0.6rem; margin: 1rem auto; }
  .card { padding: 1rem; }
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .kartu-anggota { max-width: 100%; }
  .search-bar { flex-direction: column; align-items: stretch; }
  .search-bar input, .search-bar select, .search-bar .btn { width: 100%; }
  th, td { font-size: 0.82rem; padding: 0.45rem 0.4rem; }
  .buku-cover, .buku-cover-placeholder { width: 64px; height: 92px; }

  .buku-grid { grid-template-columns: repeat(2, 1fr); gap: 0.9rem 0.7rem; }
  .buku-card-body { padding: 0.65rem 0.7rem 0.8rem; }
  .buku-judul { font-size: 0.88rem; }
  .cover-inisial { font-size: 2.2rem; }
  .kategori-grid { grid-template-columns: repeat(2, 1fr); }
  .rak-header h3 { font-size: 1rem; }
}

/* =========================================================
   MODE PROFESIONAL (Excel-like) - Koleksi Buku
   Tampilan padat khusus staf/operator: baris rapat, header
   sticky, garis tegas, tanpa sampul.
   ========================================================= */
.mode-tampilan-switch {
  display: inline-flex;
  gap: 0.25rem;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.25rem;
  margin: 0.7rem 0 1.2rem;
}
.mode-btn {
  border: none;
  background: transparent;
  color: var(--text);
  padding: 0.45rem 1rem;
  border-radius: 999px;
  font-size: 0.84rem;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  transition: background var(--transition), color var(--transition);
}
.mode-btn:hover { background: rgba(92, 33, 29, 0.06); }
[data-theme="dark"] .mode-btn:hover { background: rgba(198, 156, 71, 0.08); }
.mode-btn-active {
  background: var(--primary) !important;
  color: #fff !important;
}
[data-theme="dark"] .mode-btn-active { background: var(--accent) !important; color: #201804 !important; }

.excel-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.8rem 0.9rem 0.4rem;
}
.excel-toolbar-title { font-weight: 600; font-size: 0.92rem; color: var(--primary); }
[data-theme="dark"] .excel-toolbar-title { color: var(--accent); }

.excel-card { padding: 0; overflow: hidden; }
.excel-card .table-scroll { max-height: 72vh; overflow-y: auto; }

.tabel-excel {
  min-width: 760px;
  border-collapse: separate;
  border-spacing: 0;
  font-variant-numeric: tabular-nums;
}
.tabel-excel thead th {
  position: sticky;
  top: 0;
  z-index: 2;
  background: rgba(92, 33, 29, 0.08);
  border-right: 1px solid var(--border);
  border-bottom: 2px solid var(--primary);
  white-space: nowrap;
  padding: 0.5rem 0.6rem;
  font-size: 0.82rem;
  user-select: none;
}
[data-theme="dark"] .tabel-excel thead th { background: rgba(198, 156, 71, 0.1); border-bottom-color: var(--accent); }
.tabel-excel thead th[data-urut="naik"]::after { content: " \25B2"; font-size: 0.7em; }
.tabel-excel thead th[data-urut="turun"]::after { content: " \25BC"; font-size: 0.7em; }

.tabel-excel td {
  border-right: 1px solid var(--border);
  padding: 0.42rem 0.6rem;
  font-size: 0.85rem;
  white-space: nowrap;
}
.tabel-excel td:nth-child(2) { white-space: normal; min-width: 220px; }

.tabel-excel tbody tr:nth-child(even) { background: rgba(0, 0, 0, 0.02); }
[data-theme="dark"] .tabel-excel tbody tr:nth-child(even) { background: rgba(255, 255, 255, 0.03); }
.tabel-excel tbody tr:hover { background: rgba(150, 105, 15, 0.1) !important; }

.tabel-excel tr.baris-stok-habis td { color: var(--danger); }

.tabel-excel .sel-angka { text-align: right; }
.tabel-excel .sel-aksi { white-space: nowrap; }
.tabel-excel .sel-aksi form { display: inline; }
.tabel-excel .sel-aksi .btn-sm { margin-right: 0.25rem; }

.excel-footnote {
  margin: 0;
  padding: 0.55rem 0.8rem;
  font-size: 0.78rem;
  color: var(--muted);
  border-top: 1px solid var(--border);
}

@media (max-width: 600px) {
  .mode-tampilan-switch { width: 100%; }
  .mode-btn { flex: 1; text-align: center; }
}

/* =========================================================
   DASHBOARD - statistik & grafik (staf/operator)
   ========================================================= */
.dash-section { margin-top: 1.8rem; }
.dash-section-title { display: flex; align-items: baseline; gap: 0.5rem; margin-bottom: 0.6rem; }
.dash-section-sub { font-size: 0.78rem; font-weight: 400; color: var(--muted); }

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}
.chart-card { display: flex; flex-direction: column; }
.chart-card-title { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.7rem; color: var(--primary); }
[data-theme="dark"] .chart-card-title { color: var(--accent); }
.chart-wrap { position: relative; height: 230px; }

@media (max-width: 600px) {
  .chart-wrap { height: 200px; }
}

/* =========================================================
   Kontras tabel mode profesional - header & isi dibuat solid
   supaya tidak tumpang tindih dengan baris yang tergulir di
   baliknya saat header dalam posisi sticky.
   ========================================================= */
:root { --excel-head-bg: #ece4de; --excel-row-alt-bg: #f7f5f2; }
[data-theme="dark"] { --excel-head-bg: #2c231f; --excel-row-alt-bg: #1e1815; }

.tabel-excel thead th {
  background: var(--excel-head-bg) !important;
  color: var(--primary);
  opacity: 1;
}
[data-theme="dark"] .tabel-excel thead th { color: var(--accent); }

.tabel-excel tbody td {
  background: var(--card-bg);
  color: var(--text);
}
.tabel-excel tbody tr:nth-child(even) td { background: var(--excel-row-alt-bg); }
.tabel-excel tbody tr:hover td { background: rgba(150, 105, 15, 0.12) !important; }
.tabel-excel tr.baris-stok-habis td { color: var(--danger); background: var(--card-bg); }
[data-theme="dark"] .tabel-excel tr.baris-stok-habis td { background: var(--card-bg); }

/* =========================================================
   SIDEBAR NAVIGASI - khusus akun OPERATOR
   ========================================================= */
body.has-sidebar { }

.app-main { min-width: 0; }
body.has-sidebar .app-main {
  margin-left: 240px;
  transition: margin-left var(--transition);
}

.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: 240px;
  background: var(--primary-dark);
  color: #fff;
  display: flex;
  flex-direction: column;
  z-index: 150;
  overflow-y: auto;
  border-right: 1px solid rgba(255,255,255,0.08);
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 1.05rem 1.1rem;
  font-weight: 700;
  font-size: 0.92rem;
  line-height: 1.25;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  text-decoration: none;
  color: #fff;
}
.sidebar-brand img {
  height: 38px; width: 38px;
  border-radius: 50%;
  background: #fff;
  padding: 2px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  flex-shrink: 0;
}

.sidebar-nav {
  padding: 0.7rem 0.6rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  flex: 1;
}
.sidebar-nav-label {
  font-size: 0.67rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(233,221,210,0.5);
  padding: 0.7rem 0.7rem 0.25rem;
}

.side-link {
  color: #e9ddd2;
  text-decoration: none;
  padding: 0.6rem 0.7rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
  transition: background var(--transition), color var(--transition);
  justify-content: space-between;
}
.side-link .side-link-main { display: flex; align-items: center; gap: 0.6rem; }
.side-link:hover { background: rgba(255,255,255,0.08); color: #fff; }
.side-link.active {
  background: rgba(255,255,255,0.1);
  color: #fff;
  font-weight: 600;
  box-shadow: inset 3px 0 0 var(--accent);
}

.side-submenu {
  display: none;
  flex-direction: column;
  margin: 0.1rem 0 0.2rem 1.5rem;
  gap: 0.05rem;
  border-left: 1px solid rgba(255,255,255,0.14);
  padding-left: 0.6rem;
}
.side-group.open .side-submenu { display: flex; }
.side-submenu a {
  color: #e9ddd2;
  text-decoration: none;
  padding: 0.5rem 0.6rem;
  border-radius: var(--radius-sm);
  font-size: 0.81rem;
}
.side-submenu a:hover { background: rgba(255,255,255,0.08); color: #fff; }
.side-submenu a.active { background: rgba(255,255,255,0.1); color: #fff; font-weight: 600; box-shadow: inset 3px 0 0 var(--accent); }

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 140;
}

.navbar-compact .brand { display: none; }

@media (max-width: 900px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform var(--transition);
  }
  .sidebar.open { transform: translateX(0); }
  body.has-sidebar .app-main { margin-left: 0; }
  .sidebar-overlay.open { display: block; }
  .navbar-compact .brand { display: flex; }
}

/* =========================================================
   KARTU PENGAJUAN PEMINJAMAN (staf/operator)
   ========================================================= */
.pengajuan-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
.pengajuan-card { display: flex; flex-direction: column; gap: 0.3rem; }
.pengajuan-card-head { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.2rem; }
.pengajuan-tanggal { font-size: 0.74rem; color: var(--muted); }
.pengajuan-judul { margin: 0.1rem 0 0; font-size: 1.02rem; }
.pengajuan-meta { margin: 0; font-size: 0.84rem; color: var(--muted); }
.pengajuan-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.6rem; }
.pengajuan-form-tolak textarea {
  margin-top: 0.6rem;
  resize: vertical;
  font-family: inherit;
  font-size: 0.85rem;
}


/* =========================================================
   TAMPILAN LEBIH HIDUP
   Banner sapaan, warna per rak, stok menipis, animasi masuk
   bertahap. Semua animasi hanya transform (tanpa opacity)
   dan dimatikan bila pengguna memilih reduced-motion.
   ========================================================= */
.hero {
  position: relative;
  display: flex; align-items: center; justify-content: space-between;
  gap: 1rem;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1.4rem;
  border-radius: var(--radius-lg);
  overflow: hidden;
  color: #fff;
  background:
    radial-gradient(circle at 92% 20%, rgba(224, 180, 88, 0.30), transparent 42%),
    linear-gradient(120deg, #3c1512, #6e2f27);
  border-bottom: 3px solid var(--accent-solid);
  box-shadow: var(--shadow);
}
[data-theme="dark"] .hero {
  background:
    radial-gradient(circle at 92% 20%, rgba(198, 156, 71, 0.22), transparent 42%),
    linear-gradient(120deg, #2a0f0c, #4d1f19);
}
.hero-text { position: relative; z-index: 1; min-width: 0; }
.hero-sapa { display: block; font-size: 0.86rem; font-weight: 500; color: #ecd7a4; }
.hero h2.hero-nama { margin: 0.1rem 0 0.35rem; font-size: 1.6rem; color: #fff; }
.hero .hero-info { margin: 0; font-size: 0.85rem; color: #e9ddd2; }
.hero-deco {
  position: absolute; right: 1.2rem; top: 50%;
  width: 6.5rem; height: 6.5rem;
  margin-top: -3.25rem;
  fill: none; stroke: #e0b458; stroke-width: 1.4;
  stroke-linecap: round; stroke-linejoin: round;
  opacity: 0.28;
  animation: melayang 6s ease-in-out infinite;
}
@keyframes melayang {
  0%, 100% { transform: translateY(0) rotate(-4deg); }
  50% { transform: translateY(-8px) rotate(3deg); }
}

/* ikon rak berganti warna agar tiap kategori mudah dibedakan */
.rak-section:nth-of-type(4n+2) .rak-icon { background: rgba(58, 94, 140, 0.14); color: var(--info); }
.rak-section:nth-of-type(4n+3) .rak-icon { background: rgba(150, 105, 15, 0.16); color: var(--accent); }
.rak-section:nth-of-type(4n+4) .rak-icon { background: rgba(39, 107, 63, 0.14); color: var(--success); }

/* stok menipis (<= 2) memakai titik kuning */
.buku-stok-badge.stok-tipis::before { background: #ffc857; }

/* kartu buku muncul bergiliran (hanya geser, tidak mengubah opacity) */
.buku-grid .buku-card:nth-child(2) { animation-delay: 0.05s; }
.buku-grid .buku-card:nth-child(3) { animation-delay: 0.10s; }
.buku-grid .buku-card:nth-child(4) { animation-delay: 0.15s; }
.buku-grid .buku-card:nth-child(5) { animation-delay: 0.20s; }
.buku-grid .buku-card:nth-child(6) { animation-delay: 0.25s; }
.buku-grid .buku-card:nth-child(n+7) { animation-delay: 0.30s; }

/* umpan balik tekan tombol */
.btn:active, .btn-logout:active, .chip:active { transform: scale(0.96); }

@media (max-width: 600px) {
  .hero { padding: 1.1rem 1.1rem; }
  .hero h2.hero-nama { font-size: 1.3rem; }
  .hero-deco { width: 4.5rem; height: 4.5rem; margin-top: -2.25rem; right: 0.6rem; }
  .stat-icon { width: 2.3rem; height: 2.3rem; }
  .stat-icon .icon { width: 1.1rem; height: 1.1rem; }
  .stat-box { column-gap: 0.65rem; padding: 0.85rem 0.8rem 0.85rem 1rem; }
  .stat-box .angka { font-size: 1.55rem; }
}
@media (prefers-reduced-motion: reduce) {
  .hero-deco { animation: none; }
  .stat-box:hover .stat-icon { transform: none; }
}


/* ---- Tombol lihat/sembunyikan password ---- */
.pw-field { position: relative; display: block; }
.pw-field input { width: 100%; padding-right: 2.7rem; }
.pw-toggle {
  position: absolute; right: 0.3rem; top: 50%;
  transform: translateY(-50%);
  display: flex; align-items: center; justify-content: center;
  width: 2rem; height: 2rem;
  background: none; border: none; border-radius: 50%;
  color: var(--muted); cursor: pointer;
  transition: color var(--transition), background var(--transition);
}
.pw-toggle:hover { color: var(--primary); background: rgba(92, 33, 29, 0.08); }
[data-theme="dark"] .pw-toggle:hover { color: var(--accent); background: rgba(198, 156, 71, 0.12); }
.pw-toggle .icon { width: 1.1rem; height: 1.1rem; }


/* =========================================================
   SISTEM TOMBOL AKSI (Edit, Hapus, Lihat, Setujui, dll.)
   Tombol kecil dibuat "lembut": latar samar + garis tipis,
   warna hanya menandai jenis aksi. Solid penuh baru muncul
   saat di-hover, sehingga tabel tidak ramai oleh blok warna.
   ========================================================= */
.btn { border-radius: 8px; font-weight: 600; }

.btn.btn-sm {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 0.35rem;
  padding: 0.36rem 0.75rem;
  font-size: 0.78rem; line-height: 1.2;
  border-radius: 8px;
  white-space: nowrap;
  background: var(--surface-2);
  color: var(--text);
  border: 1px solid var(--border);
  box-shadow: none;
}
.btn.btn-sm .icon { width: 0.95rem; height: 0.95rem; }
.btn.btn-sm:hover {
  background: rgba(92, 33, 29, 0.08); color: var(--primary); border-color: var(--primary);
  transform: none; box-shadow: none;
}
[data-theme="dark"] .btn.btn-sm:hover { background: rgba(198, 156, 71, 0.12); color: var(--accent); border-color: var(--accent); }

/* Hapus / Tolak */
.btn.btn-sm.btn-danger { color: var(--danger); background: rgba(167, 41, 31, 0.08); border-color: rgba(167, 41, 31, 0.32); }
[data-theme="dark"] .btn.btn-sm.btn-danger { background: rgba(217, 114, 104, 0.12); border-color: rgba(217, 114, 104, 0.4); }
.btn.btn-sm.btn-danger:hover { background: var(--danger-solid); color: #fff; border-color: var(--danger-solid); }

/* Aktifkan / Nonaktifkan */
.btn.btn-sm.btn-warning { color: var(--warning); background: rgba(138, 92, 12, 0.09); border-color: rgba(138, 92, 12, 0.32); }
[data-theme="dark"] .btn.btn-sm.btn-warning { background: rgba(209, 162, 77, 0.12); border-color: rgba(209, 162, 77, 0.4); }
.btn.btn-sm.btn-warning:hover { background: var(--warning-solid); color: #fff; border-color: var(--warning-solid); }

/* Setujui / Kembalikan */
.btn.btn-sm.btn-success { color: var(--success); background: rgba(39, 107, 63, 0.09); border-color: rgba(39, 107, 63, 0.32); }
[data-theme="dark"] .btn.btn-sm.btn-success { background: rgba(88, 169, 124, 0.12); border-color: rgba(88, 169, 124, 0.4); }
.btn.btn-sm.btn-success:hover { background: var(--success-solid); color: #fff; border-color: var(--success-solid); }

/* Aksi utama (Ajukan, Perpanjang, Tinjau, Pinjamkan) */
.btn.btn-sm.btn-accent { color: var(--accent-dark); background: rgba(150, 105, 15, 0.11); border-color: rgba(150, 105, 15, 0.38); }
[data-theme="dark"] .btn.btn-sm.btn-accent { color: var(--accent); background: rgba(198, 156, 71, 0.13); border-color: rgba(198, 156, 71, 0.42); }
.btn.btn-sm.btn-accent:hover { background: var(--accent-solid); color: #fff; border-color: var(--accent-solid); }
[data-theme="dark"] .btn.btn-sm.btn-accent:hover { background: var(--accent); color: #201804; border-color: var(--accent); }

/* Netral / tidak bisa diklik (mis. "Stok kosong") */
.btn.btn-sm.btn-muted { color: var(--muted); background: transparent; }
span.btn.btn-sm.btn-muted:hover { background: transparent; color: var(--muted); border-color: var(--border); }

/* Tombol ikon persegi (Edit, Hapus) */
.btn.btn-icon { width: 2rem; height: 2rem; padding: 0; }
.btn.btn-icon .icon { width: 1rem; height: 1rem; }

/* Tombol Batal / Reset */
.btn.btn-ghost {
  background: transparent; color: var(--text);
  border: 1px solid var(--border); box-shadow: none;
  padding: 0.5rem 1rem; font-size: 0.85rem;
}
.btn.btn-ghost:hover { background: rgba(92, 33, 29, 0.06); border-color: var(--primary); color: var(--primary); transform: none; box-shadow: none; }
[data-theme="dark"] .btn.btn-ghost:hover { background: rgba(198, 156, 71, 0.1); border-color: var(--accent); color: var(--accent); }

/* Barisan aksi di tabel & kartu buku */
td form { margin: 0; }
.buku-card-actions > a.btn-accent { order: -1; }
.buku-card-actions form:has(.btn-icon) { flex: 0 0 auto; }
.buku-card-actions .btn.btn-icon { flex: 0 0 auto; width: 2rem; }
.tabel-excel .sel-aksi { white-space: nowrap; }
.tabel-excel .sel-aksi form { display: inline-block; vertical-align: middle; }


/* =========================================================
   DENDA, PENGATURAN & MANAJEMEN STOK
   ========================================================= */
.stat-box .angka.angka-rp { font-size: 1.3rem; letter-spacing: 0; }
a.stat-link { text-decoration: none; color: inherit; cursor: pointer; }

/* aksi berjajar di tabel peminjaman */
.aksi-baris { display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; }
.aksi-baris form { margin: 0; }
td form + form, td form + a { margin-left: 0.25rem; }

/* panel kecil "Atur Tempo" (khusus kepala) */
.aksi-atur { position: relative; display: inline-block; }
.aksi-atur > summary { list-style: none; cursor: pointer; }
.aksi-atur > summary::-webkit-details-marker { display: none; }
.aksi-atur form {
  position: absolute; right: 0; top: calc(100% + 6px); z-index: 30;
  display: flex; gap: 0.4rem; align-items: center;
  background: var(--card-bg); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.6rem; box-shadow: 0 6px 18px rgba(0,0,0,0.18);
}
.aksi-atur input[type="date"] { width: auto; padding: 0.35rem 0.5rem; font-size: 0.85rem; }

/* isian lama pinjam pada kartu pengajuan */
.lama-hari { display: inline-flex; align-items: center; gap: 0.35rem; margin: 0; font-size: 0.8rem; font-weight: 500; color: var(--muted); }
.lama-hari input { width: 4rem; padding: 0.3rem 0.4rem; font-size: 0.85rem; text-align: center; }
.pengajuan-actions form { display: inline-flex; align-items: center; gap: 0.4rem; flex-wrap: wrap; }

/* form penyesuaian stok */
.form-stok { display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center; }
.form-stok input { width: 6.2rem; padding: 0.35rem 0.5rem; font-size: 0.85rem; }
.form-stok select { width: auto; min-width: 11rem; padding: 0.35rem 0.5rem; font-size: 0.85rem; }

/* halaman pengaturan */
.setting-row {
  display: flex; justify-content: space-between; align-items: center; gap: 1rem;
  padding: 0.8rem 0; border-bottom: 1px dashed var(--border);
}
.setting-row:last-of-type { border-bottom: none; }
.setting-label { min-width: 0; flex: 1; }
.setting-label label { margin: 0; }
.setting-label small { display: block; color: var(--muted); font-size: 0.78rem; margin-top: 0.15rem; }
.setting-input { display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }
.setting-input input, .setting-input select { width: 8.5rem; text-align: right; }
.setting-satuan { min-width: 2.6rem; font-size: 0.82rem; color: var(--muted); }

/* baris buku stok menipis di tabel mode profesional */
.tabel-excel tr.baris-stok-tipis td { color: var(--warning); }

/* ---------------- Laporan: Mahasiswa Aktif ---------------- */
.mono { font-variant-numeric: tabular-nums; letter-spacing: 0.02em; }
.tabel-peringkat .no-peringkat { display: inline-block; min-width: 1.9rem; font-weight: 700; color: var(--muted); }
.tabel-peringkat .no-peringkat.no-top { color: var(--primary); }
[data-theme="dark"] .tabel-peringkat .no-peringkat.no-top { color: var(--accent); }
.bar-angka { display: inline-flex; align-items: center; gap: 0.6rem; min-width: 7.5rem; }
.bar-angka strong { font-variant-numeric: tabular-nums; min-width: 1.6rem; }
.bar { flex: 1; height: 6px; min-width: 3.5rem; background: var(--surface-2); border-radius: 3px; overflow: hidden; }
.bar i { display: block; height: 100%; background: var(--primary); }
[data-theme="dark"] .bar i { background: var(--accent); }
```


## `Website/templates/auth/daftar_pengguna.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Manajemen Pengguna{% endblock %}
{% block content %}
<h2>Manajemen Pengguna</h2>
<div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.5rem;">
  <a href="{{ url_for('auth.tambah_pengguna') }}" class="btn">+ Tambah Pengguna</a>
  <a href="{{ url_for('auth.daftar_persetujuan') }}" class="btn btn-accent">
    <svg class="icon"><use href="#i-user-check"></use></svg> Persetujuan Akun Baru
    {% if jumlah_pending_akun %}<span class="badge badge-danger" style="margin-left:0.3rem;">{{ jumlah_pending_akun }}</span>{% endif %}
  </a>
</div>

<div class="card" style="margin-top:1rem;">
  <div class="table-scroll">
  <table>
    <thead>
      <tr><th>Nama</th><th>Username</th><th>NIM</th><th>Email</th><th>Role</th><th>Persetujuan</th><th>Status</th><th>Aksi</th></tr>
    </thead>
    <tbody>
      {% for u in pengguna %}
      <tr>
        <td>{{ u.nama_lengkap }}</td>
        <td>{{ u.username }}</td>
        <td>{{ u.nim or '-' }}</td>
        <td>{{ u.email }}</td>
        <td>{{ u.role_label }}</td>
        <td>
          {% if u.status_akun == 'disetujui' %}<span class="badge badge-success">Disetujui</span>
          {% elif u.status_akun == 'pending' %}<span class="badge badge-warning">Menunggu</span>
          {% else %}<span class="badge badge-danger">Ditolak</span>{% endif %}
        </td>
        <td>
          {% if u.is_active_db %}<span class="badge badge-success">Aktif</span>
          {% else %}<span class="badge badge-danger">Nonaktif</span>{% endif %}
        </td>
        <td>
          <div style="display:flex; gap:0.35rem; flex-wrap:wrap;">
            {% if u.id != current_user.id %}
              <a href="{{ url_for('auth.edit_pengguna', user_id=u.id) }}" class="btn btn-sm"><svg class="icon"><use href="#i-edit"></use></svg> Edit</a>
              <a href="{{ url_for('kartu.kartu_anggota_lain', user_id=u.id) }}" class="btn btn-sm"><svg class="icon"><use href="#i-id-card"></use></svg> Kartu</a>
              {% if u.role == 'mahasiswa' %}
                <a href="{{ url_for('peminjaman.riwayat_anggota', user_id=u.id) }}" class="btn btn-sm"><svg class="icon"><use href="#i-clock"></use></svg> Riwayat</a>
              {% endif %}
              <form method="POST" action="{{ url_for('auth.toggle_aktif_pengguna', user_id=u.id) }}" style="display:inline;">
                <button class="btn btn-sm btn-warning" type="submit">
                  {{ 'Nonaktifkan' if u.is_active_db else 'Aktifkan' }}
                </button>
              </form>
              <form method="POST" action="{{ url_for('auth.hapus_pengguna', user_id=u.id) }}" style="display:inline;"
                    onsubmit="return confirm('Hapus akun &quot;' + {{ u.username|tojson }} + '&quot; secara permanen? Seluruh riwayat peminjaman miliknya juga akan ikut terhapus. Tindakan ini tidak bisa dibatalkan.');">
                <button class="btn btn-sm btn-danger btn-icon" type="submit" title="Hapus" aria-label="Hapus"><svg class="icon"><use href="#i-trash"></use></svg></button>
              </form>
            {% else %}
              <span class="page-sub" style="font-size:0.78rem;">Akun Anda sendiri — edit lewat Profil Saya</span>
            {% endif %}
          </div>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
</div>
{% endblock %}
```


## `Website/templates/auth/edit_pengguna.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Edit Pengguna{% endblock %}
{% block content %}
<div class="card" style="max-width:480px;">
  <h2>Edit Pengguna</h2>
  <p class="page-sub" style="margin-top:-0.4rem;">Mengubah data akun <strong>{{ u.username }}</strong>.</p>
  <form method="POST" autocomplete="off">
    <div class="form-group">
      <label>Nama Lengkap</label>
      <input type="text" name="nama_lengkap" value="{{ u.nama_lengkap }}" required>
    </div>
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" value="{{ u.username }}" required autocomplete="off">
    </div>
    <div class="form-group">
      <label>Email</label>
      <input type="email" name="email" value="{{ u.email }}" required>
    </div>
    <div class="form-group">
      <label>No. Telepon</label>
      <input type="text" name="no_telepon" value="{{ u.no_telepon or '' }}">
    </div>
    <div class="form-group">
      <label>Alamat</label>
      <textarea name="alamat" rows="2">{{ u.alamat or '' }}</textarea>
    </div>
    <div class="form-group">
      <label>Role</label>
      <select name="role">
        <option value="mahasiswa" {{ 'selected' if u.role == 'mahasiswa' }}>Mahasiswa</option>
        <option value="staf" {{ 'selected' if u.role == 'staf' }}>Staf</option>
        <option value="kepala_perpustakaan" {{ 'selected' if u.role == 'kepala_perpustakaan' }}>Kepala Perpustakaan</option>
      </select>
    </div>
    <div class="form-group">
      <label>NIM <small style="color:var(--muted);">(wajib untuk mahasiswa, {{ config.NIM_PANJANG_MIN }}-{{ config.NIM_PANJANG_MAKS }} digit)</small></label>
      <input type="text" name="nim" value="{{ u.nim or '' }}" inputmode="numeric" maxlength="{{ config.NIM_PANJANG_MAKS }}" pattern="\d*">
    </div>
    <div class="form-group">
      <label>Reset Password (opsional)</label>
      <input type="password" name="password" data-toggle-pw autocomplete="new-password" placeholder="Kosongkan jika tidak ingin mengubah password">
    </div>
    <div class="form-group">
      <label>Konfirmasi Password Baru</label>
      <input type="password" name="password2" data-toggle-pw autocomplete="new-password" placeholder="Ulangi password baru">
    </div>
    <button class="btn" type="submit">Simpan Perubahan</button>
    <a href="{{ url_for('auth.daftar_pengguna') }}" class="btn btn-ghost">Batal</a>
  </form>
</div>
{% endblock %}
```


## `Website/templates/auth/login.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="card" style="max-width:400px; margin:2rem auto; text-align:center;">
  <img src="{{ url_for('static', filename='img/logo_stikom.png') }}" alt="Logo" style="width:80px; margin-bottom:0.6rem;">
  <h2 style="margin-top:0;">Login Perpustakaan</h2>
  <form method="POST" style="text-align:left;" data-loader="Memproses login...">
    <div class="form-group">
      <label>Username atau NIM</label>
      <input type="text" name="username" required autofocus autocomplete="username">
    </div>
    <div class="form-group">
      <label>Password</label>
      <div style="position:relative;">
        <input type="password" name="password" id="passwordInput" required style="padding-right:2.4rem;">
        <button type="button" onclick="togglePasswordVisibility()"
                style="position:absolute; right:6px; top:50%; transform:translateY(-50%); background:none; border:none; cursor:pointer; font-size:1rem;">
          <span id="eyeIcon"><svg class="icon"><use href="#i-eye"></use></svg></span>
        </button>
      </div>
    </div>
    <button class="btn" type="submit" style="width:100%;">Login</button>
  </form>
  <p style="margin-top:1rem; font-size:0.88rem;">
    Belum punya akun? <a href="{{ url_for('auth.register') }}" class="js-nav-loader">Daftar sebagai mahasiswa</a>
  </p>
</div>
{% endblock %}

{% block scripts %}
<script>
  function togglePasswordVisibility() {
    var input = document.getElementById('passwordInput');
    var icon = document.getElementById('eyeIcon');
    if (input.type === 'password') {
      input.type = 'text';
      icon.innerHTML = '<svg class="icon"><use href="#i-eye-off"></use></svg>';
    } else {
      input.type = 'password';
      icon.innerHTML = '<svg class="icon"><use href="#i-eye"></use></svg>';
    }
  }
</script>
{% endblock %}
```


## `Website/templates/auth/persetujuan.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Persetujuan Akun{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-user-check"></use></svg> Persetujuan Akun Mahasiswa Baru</h2>
  <p class="page-sub">Registrasi mandiri lewat halaman publik harus disetujui di sini sebelum mahasiswa bisa login.</p>
</div>

<a href="{{ url_for('auth.daftar_pengguna') }}" class="btn btn-sm btn-muted" style="margin-bottom:1rem;">&larr; Kembali ke Manajemen Pengguna</a>

{% if not pending %}
  <div class="card empty-state">
    <svg class="icon" style="width:2.2rem;height:2.2rem;"><use href="#i-inbox"></use></svg>
    <p>Tidak ada pendaftaran yang menunggu persetujuan saat ini.</p>
  </div>
{% else %}
  <div class="card">
    <div class="table-scroll">
    <table>
      <thead>
        <tr><th>Nama Lengkap</th><th>NIM</th><th>Username</th><th>Email</th><th>Daftar Pada</th><th>Aksi</th></tr>
      </thead>
      <tbody>
        {% for u in pending %}
        <tr>
          <td>{{ u.nama_lengkap }}</td>
          <td>{{ u.nim or '-' }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.created_at.strftime('%d-%m-%Y %H:%M') }}</td>
          <td style="white-space:nowrap;">
            <form method="POST" action="{{ url_for('auth.setujui_pengguna', user_id=u.id) }}" style="display:inline;">
              <button class="btn btn-sm btn-success" type="submit">Setujui</button>
            </form>
            <form method="POST" action="{{ url_for('auth.tolak_pengguna', user_id=u.id) }}" style="display:inline;"
                  onsubmit="return confirm('Yakin tolak registrasi &quot;' + {{ u.username|tojson }} + '&quot;?');">
              <button class="btn btn-sm btn-danger" type="submit">Tolak</button>
            </form>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    </div>
  </div>
{% endif %}
{% endblock %}
```


## `Website/templates/auth/profil.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Profil Saya{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-user"></use></svg> Profil Saya</h2>
  <p class="page-sub">Kelola data diri dan password akun Anda sendiri ({{ current_user.role_label }}).</p>
</div>

<div class="card" style="max-width:480px;">
  <form method="POST">
    <div class="form-group">
      <label>Username</label>
      <input type="text" value="{{ current_user.username }}" disabled>
    </div>
    <div class="form-group">
      <label>Nama Lengkap</label>
      <input type="text" name="nama_lengkap" value="{{ current_user.nama_lengkap }}" required>
    </div>
    <div class="form-group">
      <label>Email</label>
      <input type="email" name="email" value="{{ current_user.email }}" required>
    </div>
    <div class="form-group">
      <label>No. Telepon</label>
      <input type="text" name="no_telepon" value="{{ current_user.no_telepon or '' }}">
    </div>
    <div class="form-group">
      <label>Alamat</label>
      <textarea name="alamat" rows="2">{{ current_user.alamat or '' }}</textarea>
    </div>

    <hr style="border:none; border-top:1px solid var(--border); margin:1.1rem 0;">
    <p class="page-sub" style="margin-bottom:0.6rem;">Ganti password (opsional — kosongkan semua jika tidak ingin mengganti)</p>

    {% if not current_user.is_kepala %}
    <div class="form-group">
      <label>Password Lama</label>
      <input type="password" name="password_lama" data-toggle-pw autocomplete="current-password">
    </div>
    {% endif %}
    <div class="form-group">
      <label>Password Baru</label>
      <input type="password" name="password_baru" data-toggle-pw autocomplete="new-password">
    </div>
    <div class="form-group">
      <label>Konfirmasi Password Baru</label>
      <input type="password" name="password_baru2" data-toggle-pw autocomplete="new-password">
    </div>

    <button class="btn" type="submit">Simpan Perubahan</button>
  </form>
</div>

<div class="card" style="max-width:480px;">
  <h3 style="margin-top:0;"><svg class="icon"><use href="#i-id-card"></use></svg> Kartu Perpustakaan Saya</h3>
  <p class="page-sub">Lihat dan unduh kartu perpustakaan digital Anda.</p>
  <a href="{{ url_for('kartu.kartu_saya') }}" class="btn btn-accent">Lihat Kartu Saya</a>
</div>
{% endblock %}
```


## `Website/templates/auth/register.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Registrasi{% endblock %}
{% block content %}
<div class="card" style="max-width:450px; margin:2rem auto; text-align:center;">
  <img src="{{ url_for('static', filename='img/logo_stikom.png') }}" alt="Logo" style="width:80px; margin-bottom:0.6rem;">
  <h2 style="margin-top:0;">Registrasi Mahasiswa Baru</h2>
  <p style="font-size:0.82rem; color:var(--muted); margin-top:-0.4rem;">
    Akun baru akan ditinjau dan disetujui terlebih dahulu oleh kepala perpustakaan sebelum bisa digunakan untuk login.
  </p>
  <form method="POST" style="text-align:left;" data-loader="Memproses pendaftaran...">
    <div class="form-group">
      <label>Nama Lengkap</label>
      <input type="text" name="nama_lengkap" required>
    </div>
    <div class="form-group">
      <label>NIM</label>
      <input type="text" name="nim" inputmode="numeric" minlength="{{ config.NIM_PANJANG_MIN }}" maxlength="{{ config.NIM_PANJANG_MAKS }}" pattern="[0-9]+" required>
      <small style="font-size:0.78rem; color:var(--muted);">NIM akan menjadi ID kartu perpustakaan Anda ({{ config.NIM_PANJANG_MIN }}-{{ config.NIM_PANJANG_MAKS }} digit angka).</small>
    </div>
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" required>
    </div>
    <div class="form-group">
      <label>Email</label>
      <input type="email" name="email" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" id="pw1" data-toggle-pw required autocomplete="new-password" oninput="cekKecocokanPassword()">
    </div>
    <div class="form-group">
      <label>Konfirmasi Password</label>
      <input type="password" name="password2" id="pw2" data-toggle-pw required autocomplete="new-password" oninput="cekKecocokanPassword()">
      <small id="pesanCocok" style="font-size:0.78rem;"></small>
    </div>
    <button class="btn" type="submit" style="width:100%;">Daftar</button>
  </form>
  <p style="margin-top:1rem; font-size:0.88rem;">
    Sudah punya akun? <a href="{{ url_for('auth.login') }}">Login di sini</a>
  </p>
</div>
{% endblock %}

{% block scripts %}
<script>
  function cekKecocokanPassword() {
    var pw1 = document.getElementById('pw1').value;
    var pw2 = document.getElementById('pw2').value;
    var pesan = document.getElementById('pesanCocok');
    if (!pw2) { pesan.textContent = ''; return; }
    if (pw1 === pw2) {
      pesan.textContent = 'Password cocok';
      pesan.style.color = 'var(--success)';
    } else {
      pesan.textContent = 'Password belum sama';
      pesan.style.color = 'var(--danger)';
    }
  }
</script>
{% endblock %}
```


## `Website/templates/auth/tambah_pengguna.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Tambah Pengguna{% endblock %}
{% block content %}
<div class="card" style="max-width:450px;">
  <h2>Tambah Pengguna</h2>
  <form method="POST">
    <div class="form-group">
      <label>Nama Lengkap</label>
      <input type="text" name="nama_lengkap" required>
    </div>
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" required>
    </div>
    <div class="form-group">
      <label>Email</label>
      <input type="email" name="email" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" data-toggle-pw required autocomplete="new-password">
    </div>
    <div class="form-group">
      <label>Role</label>
      <select name="role">
        <option value="staf">Staf</option>
        <option value="kepala_perpustakaan">Kepala Perpustakaan</option>
        <option value="mahasiswa">Mahasiswa</option>
      </select>
    </div>
    <div class="form-group">
      <label>NIM <small style="color:var(--muted);">(wajib untuk mahasiswa, {{ config.NIM_PANJANG_MIN }}-{{ config.NIM_PANJANG_MAKS }} digit)</small></label>
      <input type="text" name="nim" inputmode="numeric" maxlength="{{ config.NIM_PANJANG_MAKS }}" pattern="\d*">
    </div>
    <button class="btn" type="submit">Simpan</button>
    <a href="{{ url_for('auth.daftar_pengguna') }}" class="btn btn-ghost">Batal</a>
  </form>
</div>
{% endblock %}
```


## `Website/templates/buku/daftar.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Daftar Buku{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-book"></use></svg> Koleksi Buku</h2>
  <p class="page-sub" id="labelModeTampilan">Jelajahi koleksi berdasarkan rak kategori, seperti di perpustakaan sungguhan.</p>
</div>

<form method="GET" class="search-bar" data-loader="Mencari buku...">
  <div class="search-field">
    <svg class="icon"><use href="#i-search"></use></svg>
    <input type="text" name="q" placeholder="Cari judul, penulis, atau ISBN..." value="{{ q }}">
  </div>
  {% if kategori_id %}<input type="hidden" name="kategori_id" value="{{ kategori_id }}">{% endif %}
  <button class="btn" type="submit">Cari</button>
  {% if current_user.is_staf or current_user.is_kepala %}
    <a href="{{ url_for('buku.tambah_buku') }}" class="btn btn-accent">+ Tambah Buku</a>
    <a href="{{ url_for('buku.ekspor_buku') }}" class="btn btn-ghost"><svg class="icon"><use href="#i-download"></use></svg> Ekspor Excel</a>
  {% endif %}
</form>

{% if current_user.is_staf or current_user.is_kepala %}
  <div class="mode-tampilan-switch" role="group" aria-label="Ganti mode tampilan">
    <button type="button" id="btnModeRak" class="mode-btn" onclick="setModeTampilan('rak')"><svg class="icon"><use href="#i-folder"></use></svg> Mode Rak</button>
    <button type="button" id="btnModeProfesional" class="mode-btn" onclick="setModeTampilan('profesional')"><svg class="icon"><use href="#i-bar-chart"></use></svg> Mode Profesional</button>
  </div>
{% endif %}

<div id="viewRak">
<div class="kategori-chips">
  <a href="{{ url_for('buku.daftar_buku', **({'q': q} if q else {})) }}"
     class="chip{{ ' chip-active' if not kategori_id else '' }}">Semua Rak</a>
  {% for k in kategori_list %}
    <a href="{{ url_for('buku.daftar_buku', kategori_id=k.id, **({'q': q} if q else {})) }}"
       class="chip{{ ' chip-active' if kategori_id == k.id else '' }}">{{ k.nama_kategori }}</a>
  {% endfor %}
</div>

{% if not daftar %}
  <div class="card empty-state">
    <svg class="icon" style="width:2.2rem;height:2.2rem;"><use href="#i-inbox"></use></svg>
    <p>Tidak ada buku ditemukan. Coba kata kunci atau kategori lain.</p>
  </div>
{% else %}
  {% for nama_kategori, buku_list in kelompok.items() %}
    <section class="rak-section">
      <div class="rak-header">
        <h3><svg class="icon rak-icon"><use href="#i-folder"></use></svg>{{ nama_kategori }}</h3>
        <span class="rak-count">{{ buku_list|length }} judul</span>
      </div>
      <div class="buku-grid">
        {% for b in buku_list %}
          <div class="buku-card">
            <a href="{{ url_for('buku.detail_buku', buku_id=b.id) }}" class="buku-card-cover">
              {% if b.sampul_path %}
                <img src="{{ url_for('static', filename=b.sampul_path.replace('static/', '', 1)) }}" alt="Sampul {{ b.judul }}">
              {% else %}
                <div class="buku-cover-placeholder cover-v{{ b.id % 4 }}">
                  <span class="cover-inisial">{{ (b.judul or '?')[:1]|upper }}</span>
                  <span class="cover-ket">Tanpa sampul</span>
                </div>
              {% endif %}
              <span class="buku-stok-badge {{ 'stok-habis' if b.stok == 0 else '' }}">
                {{ 'Kosong' if b.stok == 0 else b.stok ~ ' stok' }}
              </span>
            </a>
            <div class="buku-card-body">
              <a href="{{ url_for('buku.detail_buku', buku_id=b.id) }}" class="buku-judul">{{ b.judul }}</a>
              <div class="buku-penulis">{{ b.penulis }}</div>
              {% if b.tahun_terbit or b.penerbit %}
                <div class="buku-meta">
                  {% if b.tahun_terbit %}<span>{{ b.tahun_terbit }}</span>{% endif %}
                  {% if b.penerbit %}<span title="{{ b.penerbit }}">{{ b.penerbit }}</span>{% endif %}
                </div>
              {% endif %}
              {% if current_user.is_staf or current_user.is_kepala %}
                <div class="buku-card-actions">
                  <a href="{{ url_for('buku.edit_buku', buku_id=b.id) }}" class="btn btn-sm btn-icon" title="Edit" aria-label="Edit"><svg class="icon"><use href="#i-edit"></use></svg></a>
                  {% if b.stok > 0 %}
                    <a href="{{ url_for('peminjaman.pinjam_buku', buku_id=b.id) }}" class="btn btn-sm btn-accent"><svg class="icon"><use href="#i-book-open"></use></svg> Pinjamkan</a>
                  {% endif %}
                  {% if current_user.is_kepala %}
                    <form method="POST" action="{{ url_for('buku.hapus_buku', buku_id=b.id) }}"
                          onsubmit="return confirm('Yakin hapus buku ini?');">
                      <button class="btn btn-sm btn-danger btn-icon" type="submit" title="Hapus" aria-label="Hapus"><svg class="icon"><use href="#i-trash"></use></svg></button>
                    </form>
                  {% endif %}
                </div>
              {% elif current_user.is_mahasiswa %}
                <div class="buku-card-actions">
                  {% if b.id in buku_id_aktif %}
                    <span class="btn btn-sm btn-muted" style="cursor:default;">Sudah diajukan</span>
                  {% elif kuota_penuh %}
                    <span class="btn btn-sm btn-muted" style="cursor:default;" title="Maksimal {{ maks_pinjam }} buku">Kuota penuh</span>
                  {% elif b.stok > 0 %}
                    <form method="POST" action="{{ url_for('peminjaman.ajukan_peminjaman', buku_id=b.id) }}"
                          onsubmit="return confirm('Ajukan peminjaman buku ini?');">
                      <button class="btn btn-sm btn-accent" type="submit">Ajukan</button>
                    </form>
                  {% else %}
                    <span class="btn btn-sm btn-muted" style="cursor:default;">Stok kosong</span>
                  {% endif %}
                </div>
              {% endif %}
            </div>
          </div>
        {% endfor %}
      </div>
    </section>
  {% endfor %}
{% endif %}
</div>

{% if current_user.is_staf or current_user.is_kepala %}
<div id="viewProfesional" style="display:none;">
  {% if not daftar %}
    <div class="card empty-state">
      <svg class="icon" style="width:2.2rem;height:2.2rem;"><use href="#i-inbox"></use></svg>
      <p>Tidak ada buku ditemukan. Coba kata kunci atau kategori lain.</p>
    </div>
  {% else %}
    <div class="card excel-card" id="excelCard">
      <div class="excel-toolbar">
        <span class="excel-toolbar-title"><svg class="icon"><use href="#i-bar-chart"></use></svg> Stok Buku — Tampilan Spreadsheet</span>
      </div>
      <div class="table-scroll">
        <table class="tabel-excel">
          <thead>
            <tr>
              <th style="width:2.5rem;">No</th>
              <th>Judul</th>
              <th>Penulis</th>
              <th>Penerbit</th>
              <th>Tahun</th>
              <th>ISBN</th>
              <th>Kategori</th>
              <th>Lokasi Rak</th>
              <th style="text-align:right;">Stok</th>
              <th>Aksi</th>
            </tr>
          </thead>
          <tbody>
            {% for b in daftar %}
              <tr class="{{ 'baris-stok-habis' if b.stok == 0 else '' }}">
                <td class="sel-angka">{{ loop.index }}</td>
                <td><a href="{{ url_for('buku.detail_buku', buku_id=b.id) }}">{{ b.judul }}</a></td>
                <td>{{ b.penulis }}</td>
                <td>{{ b.penerbit or '-' }}</td>
                <td class="sel-angka">{{ b.tahun_terbit or '-' }}</td>
                <td>{{ b.isbn or '-' }}</td>
                <td>{{ b.kategori.nama_kategori if b.kategori else '-' }}</td>
                <td>{{ b.lokasi_rak or '-' }}</td>
                <td class="sel-angka">{{ b.stok }}</td>
                <td class="sel-aksi">
                  <a href="{{ url_for('buku.edit_buku', buku_id=b.id) }}" class="btn btn-sm btn-icon" title="Edit" aria-label="Edit"><svg class="icon"><use href="#i-edit"></use></svg></a>
                  {% if b.stok > 0 %}
                    <a href="{{ url_for('peminjaman.pinjam_buku', buku_id=b.id) }}" class="btn btn-sm btn-accent"><svg class="icon"><use href="#i-book-open"></use></svg> Pinjamkan</a>
                  {% endif %}
                  {% if current_user.is_kepala %}
                    <form method="POST" action="{{ url_for('buku.hapus_buku', buku_id=b.id) }}"
                          onsubmit="return confirm('Yakin hapus buku ini?');" style="display:inline;">
                      <button class="btn btn-sm btn-danger btn-icon" type="submit" title="Hapus" aria-label="Hapus"><svg class="icon"><use href="#i-trash"></use></svg></button>
                    </form>
                  {% endif %}
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      <p class="excel-footnote">{{ daftar|length }} judul ditampilkan · klik header kolom untuk mengurutkan.</p>
    </div>
  {% endif %}
</div>
{% endif %}
{% endblock %}

{% block scripts %}
<script>
  // ---- Mode Tampilan (Rak / Profesional) — khusus staf & operator ----
  // Murni tampilan di sisi browser: memakai data yang sama yang sudah
  // dirender server (elemen viewProfesional hanya disembunyikan/ditampilkan
  // lewat CSS), jadi TIDAK ada request/endpoint baru dan TIDAK mengubah
  // data/alur backend sama sekali — aman dari risiko bug di sistem lain.
  function setModeTampilan(mode) {
    var viewRak = document.getElementById('viewRak');
    var viewPro = document.getElementById('viewProfesional');
    var btnRak = document.getElementById('btnModeRak');
    var btnPro = document.getElementById('btnModeProfesional');
    var label = document.getElementById('labelModeTampilan');
    if (!viewRak) return; // halaman ini tidak punya toggle (bukan staf/kepala perpustakaan)

    if (mode === 'profesional' && viewPro) {
      viewRak.style.display = 'none';
      viewPro.style.display = 'block';
      if (btnRak) btnRak.classList.remove('mode-btn-active');
      if (btnPro) btnPro.classList.add('mode-btn-active');
      if (label) label.textContent = 'Mode profesional: data stok ditampilkan padat seperti spreadsheet, tanpa sampul.';
    } else {
      viewRak.style.display = 'block';
      if (viewPro) viewPro.style.display = 'none';
      if (btnRak) btnRak.classList.add('mode-btn-active');
      if (btnPro) btnPro.classList.remove('mode-btn-active');
      if (label) label.textContent = 'Jelajahi koleksi berdasarkan rak kategori, seperti di perpustakaan sungguhan.';
    }
    try { localStorage.setItem('modeTampilanBuku', mode); } catch (e) { /* abaikan jika storage diblokir */ }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var tersimpan = 'rak';
    try { tersimpan = localStorage.getItem('modeTampilanBuku') || 'rak'; } catch (e) {}
    setModeTampilan(tersimpan);

    // urutkan tabel Excel dengan klik header kolom (naik/turun bergantian)
    var tabel = document.querySelector('.tabel-excel');
    if (!tabel) return;
    var ths = tabel.querySelectorAll('thead th');
    ths.forEach(function (th, idx) {
      if (idx === 0 || idx === ths.length - 1) return; // lewati kolom No & Aksi
      th.style.cursor = 'pointer';
      th.title = 'Klik untuk urutkan';
      th.addEventListener('click', function () {
        var tbody = tabel.querySelector('tbody');
        var baris = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
        var naik = th.getAttribute('data-urut') !== 'naik';
        ths.forEach(function (t) { t.removeAttribute('data-urut'); });
        th.setAttribute('data-urut', naik ? 'naik' : 'turun');

        baris.sort(function (a, b) {
          var va = a.children[idx].textContent.trim();
          var vb = b.children[idx].textContent.trim();
          var na = parseFloat(va), nb = parseFloat(vb);
          var cmp = (!isNaN(na) && !isNaN(nb)) ? na - nb : va.localeCompare(vb, 'id');
          return naik ? cmp : -cmp;
        });
        baris.forEach(function (tr, i) {
          tr.children[0].textContent = i + 1; // penomoran ulang kolom "No"
          tbody.appendChild(tr);
        });
      });
    });
  });
</script>
{% endblock %}
```


## `Website/templates/buku/detail.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}{{ buku.judul }}{% endblock %}
{% block content %}
<div class="card detail-buku">
  <div>
    {% if buku.sampul_path %}
      <img src="{{ url_for('static', filename=buku.sampul_path.replace('static/', '', 1)) }}" style="width:160px; border-radius:6px;">
    {% else %}
      <div class="buku-cover-placeholder" style="width:160px; height:220px;">Tidak ada sampul</div>
    {% endif %}
  </div>
  <div>
    <h2>{{ buku.judul }}</h2>
    <p><strong>Penulis:</strong> {{ buku.penulis }}</p>
    <p><strong>Penerbit:</strong> {{ buku.penerbit or '-' }} ({{ buku.tahun_terbit or '-' }})</p>
    <p><strong>ISBN:</strong> {{ buku.isbn or '-' }}</p>
    <p><strong>Kategori:</strong> {{ buku.kategori.nama_kategori if buku.kategori else '-' }}</p>
    <p><strong>Stok tersedia:</strong> {{ buku.stok }}</p>
    {% if buku.lokasi_rak %}<p><strong>Lokasi rak:</strong> {{ buku.lokasi_rak }}</p>{% endif %}
    <p><strong>Lama pinjam:</strong> {{ buku.lama_pinjam_hari or config.LAMA_PINJAM_HARI }} hari{% if config.DENDA_PER_HARI > 0 %} · denda keterlambatan {{ config.DENDA_PER_HARI|rupiah }}/hari{% endif %}</p>
    <p>{{ buku.deskripsi or '' }}</p>

    {% if current_user.is_staf or current_user.is_kepala %}
      <a href="{{ url_for('buku.edit_buku', buku_id=buku.id) }}" class="btn">Edit Buku</a>
      <a href="{{ url_for('peminjaman.riwayat_buku', buku_id=buku.id) }}" class="btn">Riwayat Peminjaman</a>
      {% if buku.stok > 0 %}
        <a href="{{ url_for('peminjaman.pinjam_buku', buku_id=buku.id) }}" class="btn btn-warning">Pinjamkan Buku</a>
      {% endif %}
    {% endif %}

    {% if current_user.is_mahasiswa %}
      {% if pengajuan_aktif %}
        {% if pengajuan_aktif.status == 'diajukan' %}
          <div class="flash flash-warning" style="position:static; margin-top:0.8rem;">
            Pengajuan peminjaman Anda untuk buku ini sedang menunggu persetujuan staf/kepala perpustakaan.
          </div>
        {% else %}
          <div class="flash flash-info" style="position:static; margin-top:0.8rem;">
            Anda sedang meminjam buku ini. Jatuh tempo: {{ pengajuan_aktif.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}.
          </div>
        {% endif %}
      {% elif kuota_penuh %}
        <div class="flash flash-warning" style="position:static; margin-top:0.8rem;">
          Batas peminjaman tercapai ({{ jumlah_aktif }}/{{ maks_pinjam }} buku). Kembalikan salah satu buku terlebih dahulu untuk meminjam buku lain.
        </div>
      {% elif buku.stok > 0 %}
        <p style="margin-top:0.8rem; font-size:0.85rem; color:var(--muted);">Kuota pinjam Anda: {{ jumlah_aktif }}/{{ maks_pinjam }} buku.</p>
        <form method="POST" action="{{ url_for('peminjaman.ajukan_peminjaman', buku_id=buku.id) }}"
              onsubmit="return confirm('Ajukan peminjaman buku ini? Permintaan akan ditinjau oleh staf/kepala perpustakaan.');" style="margin-top:0.5rem;">
          <button class="btn btn-accent" type="submit">Ajukan Peminjaman</button>
        </form>
      {% else %}
        <p class="badge badge-danger" style="margin-top:0.5rem;">Stok buku sedang kosong</p>
      {% endif %}
    {% endif %}
  </div>
</div>
{% endblock %}
```


## `Website/templates/buku/form.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}{{ 'Edit' if buku else 'Tambah' }} Buku{% endblock %}

{% block extra_head %}
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.6.2/cropper.min.css">
{% endblock %}

{% block content %}
<div class="card" style="max-width:600px;">
  <h2>{{ 'Edit Buku' if buku else 'Tambah Buku Baru' }}</h2>
  <form method="POST" enctype="multipart/form-data">
    <div class="form-group">
      <label>Judul</label>
      <input type="text" name="judul" required value="{{ buku.judul if buku else '' }}">
    </div>
    <div class="form-group">
      <label>Penulis</label>
      <input type="text" name="penulis" required value="{{ buku.penulis if buku else '' }}">
    </div>
    <div class="form-group">
      <label>Penerbit</label>
      <input type="text" name="penerbit" value="{{ buku.penerbit if buku else '' }}">
    </div>
    <div class="form-group">
      <label>Tahun Terbit</label>
      <input type="number" name="tahun_terbit" value="{{ buku.tahun_terbit if buku else '' }}">
    </div>
    <div class="form-group">
      <label>ISBN</label>
      <input type="text" name="isbn" value="{{ buku.isbn if buku else '' }}">
    </div>
    <div class="form-group">
      <label>Kategori</label>
      <select name="kategori_id">
        <option value="">- Pilih Kategori -</option>
        {% for k in kategori_list %}
          <option value="{{ k.id }}" {% if buku and buku.kategori_id == k.id %}selected{% endif %}>{{ k.nama_kategori }}</option>
        {% endfor %}
      </select>
    </div>
    <div class="form-group">
      <label>Stok</label>
      <input type="number" name="stok" min="0" value="{{ buku.stok if buku else 0 }}">
    </div>
    <div class="form-group">
      <label>Lokasi Rak</label>
      <input type="text" name="lokasi_rak" maxlength="50" placeholder="mis. Rak A-3" value="{{ buku.lokasi_rak if buku and buku.lokasi_rak else '' }}">
    </div>
    <div class="form-group">
      <label>Lama Pinjam Khusus Buku Ini (hari)</label>
      <input type="number" name="lama_pinjam_hari" min="1" max="365" placeholder="Kosongkan = ikut pengaturan umum ({{ config.LAMA_PINJAM_HARI }} hari)" value="{{ buku.lama_pinjam_hari if buku and buku.lama_pinjam_hari else '' }}">
      <p class="sampul-hint">Contoh: isi 3 untuk buku referensi/favorit yang cepat habis.</p>
    </div>
    <div class="form-group">
      <label>Deskripsi</label>
      <textarea name="deskripsi" rows="3">{{ buku.deskripsi if buku else '' }}</textarea>
    </div>

    <div class="form-group">
      <label>Sampul Buku (gambar)</label>
      <div class="sampul-uploader">
        <div class="sampul-preview-box">
          <img id="previewSampul" class="buku-cover"
               {% if buku and buku.sampul_path %}
                 src="{{ url_for('static', filename=buku.sampul_path.replace('static/', '', 1)) }}"
               {% else %}
                 style="display:none;"
               {% endif %}>
          <div class="buku-cover-placeholder" id="previewPlaceholder"
               {% if buku and buku.sampul_path %}style="display:none;"{% endif %}>Belum ada sampul</div>
        </div>
        <div class="sampul-uploader-actions">
          <label for="inputSampul" class="btn btn-sm btn-accent"><svg class="icon"><use href="#i-image"></use></svg> Pilih &amp; Crop Sampul</label>
          <input type="file" name="sampul" id="inputSampul" accept="image/*" hidden>
          <p class="sampul-hint">Foto akan dipotong otomatis mengikuti rasio sampul buku sebelum diunggah.</p>
        </div>
      </div>
    </div>

    <button class="btn" type="submit">Simpan</button>
    <a href="{{ url_for('buku.daftar_buku') }}" class="btn btn-ghost">Batal</a>
  </form>
</div>

<!-- Modal crop sampul -->
<div class="crop-modal" id="cropModal">
  <div class="crop-modal-backdrop"></div>
  <div class="crop-modal-box">
    <h3><svg class="icon"><use href="#i-crop"></use></svg> Sesuaikan Sampul Buku</h3>
    <div class="crop-modal-image-wrap">
      <img id="cropTargetImage" src="" alt="Gambar untuk dipotong">
    </div>
    <p class="crop-modal-hint">Geser &amp; perbesar/kecilkan area kotak untuk memilih bagian sampul.</p>
    <div class="crop-modal-actions">
      <button type="button" class="btn btn-sm btn-muted" id="btnBatalCrop">Batal</button>
      <button type="button" class="btn btn-sm" id="btnCropTerapkan"><svg class="icon"><use href="#i-check"></use></svg> Gunakan Potongan Ini</button>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script src="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.6.2/cropper.min.js"></script>
<script>
(function () {
  var inputSampul = document.getElementById('inputSampul');
  var modal = document.getElementById('cropModal');
  var cropImage = document.getElementById('cropTargetImage');
  var btnBatal = document.getElementById('btnBatalCrop');
  var btnTerapkan = document.getElementById('btnCropTerapkan');
  var previewImg = document.getElementById('previewSampul');
  var previewPlaceholder = document.getElementById('previewPlaceholder');
  var cropperInstance = null;
  var namaFileAsli = 'sampul.jpg';

  if (!inputSampul) return;

  // Rasio sampul buku, mengikuti rasio kartu sampul di tampilan daftar buku
  var RASIO_SAMPUL = 3 / 4.3;

  inputSampul.addEventListener('change', function () {
    var file = inputSampul.files && inputSampul.files[0];
    if (!file) return;
    namaFileAsli = file.name;

    var url = URL.createObjectURL(file);
    cropImage.src = url;
    modal.classList.add('open');

    cropImage.onload = function () {
      if (cropperInstance) cropperInstance.destroy();
      cropperInstance = new Cropper(cropImage, {
        aspectRatio: RASIO_SAMPUL,
        viewMode: 1,
        dragMode: 'move',
        autoCropArea: 1,
        background: false,
        responsive: true,
      });
    };
  });

  function tutupModal() {
    modal.classList.remove('open');
    if (cropperInstance) { cropperInstance.destroy(); cropperInstance = null; }
  }

  btnBatal.addEventListener('click', function () {
    inputSampul.value = '';
    tutupModal();
  });

  // Tutup modal juga saat klik area gelap di luar kotak crop
  modal.querySelector('.crop-modal-backdrop').addEventListener('click', function () {
    inputSampul.value = '';
    tutupModal();
  });

  btnTerapkan.addEventListener('click', function () {
    if (!cropperInstance) return;
    cropperInstance.getCroppedCanvas({
      width: 600,
      height: Math.round(600 / RASIO_SAMPUL),
      imageSmoothingQuality: 'high',
    }).toBlob(function (blob) {
      var namaBaru = namaFileAsli.replace(/\.[^.]+$/, '') + '.jpg';
      var fileHasil = new File([blob], namaBaru, { type: 'image/jpeg' });

      var dt = new DataTransfer();
      dt.items.add(fileHasil);
      inputSampul.files = dt.files;

      var previewUrl = URL.createObjectURL(blob);
      previewImg.src = previewUrl;
      previewImg.style.display = 'block';
      if (previewPlaceholder) previewPlaceholder.style.display = 'none';

      tutupModal();
    }, 'image/jpeg', 0.9);
  });
})();
</script>
{% endblock %}
```


## `Website/templates/buku/import_excel.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Import Buku dari Excel{% endblock %}
{% block content %}
<div class="card" style="max-width:550px;">
  <h2>Import Data Buku dari Excel</h2>
  <p>
    1. Unduh template kosong terlebih dahulu.<br>
    2. Isi data buku pada template tersebut (jangan mengubah nama kolom di baris pertama).<br>
    3. Upload kembali file .xlsx yang sudah diisi.
  </p>
  <a href="{{ url_for('buku.download_template_excel') }}" class="btn"><svg class="icon"><use href="#i-download"></use></svg> Unduh Template Excel</a>

  <hr style="margin:1.2rem 0;">

  <form method="POST" enctype="multipart/form-data">
    <div class="form-group">
      <label>File Excel (.xlsx)</label>
      <input type="file" name="file_excel" accept=".xlsx" required>
    </div>
    <button class="btn" type="submit">Upload & Import</button>
  </form>
</div>
{% endblock %}
```


## `Website/templates/buku/kategori.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Kategori Buku{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-folder"></use></svg> Kategori Buku</h2>
  <p class="page-sub">Kelola rak kategori supaya koleksi buku mudah ditemukan.</p>
</div>

<div class="card kategori-form-card">
  <form method="POST" class="kategori-form">
    <input type="text" name="nama_kategori" placeholder="Nama kategori baru, mis. Fiksi, Sejarah, Teknologi..." required>
    <button class="btn btn-accent" type="submit">+ Tambah Kategori</button>
  </form>
</div>

{% if kategori_list %}
<div class="kategori-grid">
  {% for k in kategori_list %}
    <div class="kategori-item" style="display:flex; flex-direction:column; gap:0.4rem;">
      <a href="{{ url_for('buku.daftar_buku', kategori_id=k.id) }}" class="kategori-card">
        <svg class="icon kategori-icon"><use href="#i-book"></use></svg>
        <div class="kategori-nama">{{ k.nama_kategori }}</div>
        <div class="kategori-jumlah">{{ k.buku_list|length }} buku</div>
      </a>
      {% if current_user.is_staf or current_user.is_kepala %}
      <form method="POST" action="{{ url_for('buku.hapus_kategori', kategori_id=k.id) }}"
            onsubmit="return confirm('Hapus kategori &quot;' + {{ k.nama_kategori|tojson }} + '&quot;?{% if k.buku_list %} {{ k.buku_list|length }} buku di dalamnya tidak ikut terhapus, tetapi menjadi Tanpa Kategori.{% endif %}');">
        <button class="btn btn-sm btn-danger" type="submit" style="width:100%;"><svg class="icon"><use href="#i-trash"></use></svg> Hapus</button>
      </form>
      {% endif %}
    </div>
  {% endfor %}
</div>
{% else %}
  <div class="card empty-state">
    <svg class="icon" style="width:2.2rem;height:2.2rem;"><use href="#i-folder"></use></svg>
    <p>Belum ada kategori. Tambahkan kategori pertama Anda di atas.</p>
  </div>
{% endif %}
{% endblock %}
```


## `Website/templates/dashboard.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Dashboard{% endblock %}

{% block extra_head %}
{% if not current_user.is_mahasiswa %}
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
{% endif %}
{% endblock %}

{% block content %}
<div class="hero">
  <div class="hero-text">
    <span class="hero-sapa" id="heroSapa">Selamat datang</span>
    <h2 class="hero-nama">{{ current_user.nama_lengkap }}</h2>
    <p class="hero-info"><span id="heroTanggal">{{ today.strftime('%d-%m-%Y') }}</span> · {{ current_user.role_label }}</p>
  </div>
  <svg class="hero-deco" aria-hidden="true"><use href="#i-book-open"></use></svg>
</div>

{% if current_user.is_mahasiswa %}
  {% if jumlah_terlambat_saya %}
    <div class="flash flash-danger" style="position:static;">
      Anda memiliki {{ jumlah_terlambat_saya }} buku yang sudah <strong>lewat batas waktu</strong> pengembalian. Segera kembalikan ke perpustakaan.
    </div>
  {% endif %}
  {% if akan_jatuh_tempo_saya %}
    <div class="flash flash-warning" style="position:static;">
      Anda memiliki {{ akan_jatuh_tempo_saya|length }} buku yang akan <strong>segera jatuh tempo</strong> dalam {{ config.PERINGATAN_JATUH_TEMPO_HARI }} hari ke depan. Yuk kembalikan tepat waktu ya!
    </div>
  {% endif %}

  {% if denda_belum_lunas_saya %}
    <div class="flash flash-danger no-auto-hide" style="position:static;">
      Anda memiliki denda belum lunas <strong>{{ denda_belum_lunas_saya|rupiah }}</strong>. Silakan lunasi di perpustakaan{% if config.BLOKIR_JIKA_DENDA %} — peminjaman baru ditahan sampai denda lunas{% endif %}.
    </div>
  {% endif %}
  {% if denda_berjalan_saya %}
    <div class="flash flash-warning no-auto-hide" style="position:static;">
      Denda keterlambatan berjalan <strong>{{ denda_berjalan_saya|rupiah }}</strong> dan bertambah {{ config.DENDA_PER_HARI|rupiah }} setiap hari sampai buku dikembalikan.
    </div>
  {% endif %}

  <div class="grid-3">
    <div class="stat-box">
      <span class="stat-icon tone-maroon"><svg class="icon"><use href="#i-clipboard"></use></svg></span>
      <div class="angka">{{ jumlah_kuota_terpakai }}/{{ maks_pinjam }}</div>
      <div class="label">Kuota Pinjam Terpakai</div>
    </div>
    <div class="stat-box"><span class="stat-icon tone-blue"><svg class="icon"><use href="#i-book-open"></use></svg></span><div class="angka">{{ jumlah_sedang_dipinjam }}</div><div class="label">Sedang Dipinjam</div></div>
    <div class="stat-box"><span class="stat-icon tone-gold"><svg class="icon"><use href="#i-clock"></use></svg></span><div class="angka">{{ jumlah_pernah_dipinjam }}</div><div class="label">Total Pernah Dipinjam</div></div>
    <div class="stat-box">
      <span class="stat-icon tone-green"><svg class="icon"><use href="#i-id-card"></use></svg></span>
      <div class="angka" style="font-size:1.15rem;">
        {% if kartu_saya %}
          {% if kartu_saya.is_kadaluarsa %}<span class="badge badge-danger">Kadaluarsa</span>{% elif kartu_saya.status == 'aktif' %}<span class="badge badge-success">Aktif</span>{% else %}<span class="badge badge-danger">Nonaktif</span>{% endif %}
        {% else %}
          <span class="badge badge-warning">Belum Terbit</span>
        {% endif %}
      </div>
      <div class="label">Status Kartu Perpustakaan</div>
    </div>
    {% if config.DENDA_PER_HARI > 0 %}
    <div class="stat-box">
      <span class="stat-icon {{ 'tone-red' if (denda_belum_lunas_saya or denda_berjalan_saya) else 'tone-green' }}"><svg class="icon"><use href="#i-coins"></use></svg></span>
      <div class="angka angka-rp">{{ (denda_belum_lunas_saya + denda_berjalan_saya)|rupiah }}</div>
      <div class="label">Total Denda Saya</div>
    </div>
    {% endif %}
  </div>

  <h3><svg class="icon"><use href="#i-book-open"></use></svg> Buku yang sedang Anda pinjam</h3>
  {% if pinjaman_aktif %}
    <div class="card">
      <div class="table-scroll">
  <table>
        <thead><tr><th>Judul Buku</th><th>Tgl Pinjam</th><th>Jatuh Tempo</th><th>Status</th></tr></thead>
        <tbody>
        {% for p in pinjaman_aktif %}
          <tr>
            <td>{{ p.buku.judul }}</td>
            <td>{{ p.tanggal_pinjam.strftime('%d-%m-%Y') }}</td>
            <td>{{ p.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}</td>
            <td>
              {% if p.is_telat %}
                <span class="badge badge-danger">Terlambat {{ p.hari_telat }} hari · {{ denda_sekarang(p)|rupiah }}</span>
              {% elif p.hari_menuju_jatuh_tempo is not none and p.hari_menuju_jatuh_tempo <= config.PERINGATAN_JATUH_TEMPO_HARI %}
                <span class="badge badge-warning">Segera Tempo ({{ p.hari_menuju_jatuh_tempo }}h)</span>
              {% else %}
                <span class="badge badge-success">Tepat waktu</span>
              {% endif %}
            </td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
</div>
    </div>
  {% else %}
    <p>Anda tidak sedang meminjam buku apapun.</p>
  {% endif %}

  <section class="dash-section">
    <h3 class="dash-section-title"><svg class="icon"><use href="#i-flame"></use></svg> Rekomendasi Buku Populer</h3>
    {% if rekomendasi_buku %}
      <div class="buku-grid">
        {% for b, jumlah in rekomendasi_buku %}
          <div class="buku-card">
            <a href="{{ url_for('buku.detail_buku', buku_id=b.id) }}" class="buku-card-cover">
              {% if b.sampul_path %}
                <img src="{{ url_for('static', filename=b.sampul_path.replace('static/', '', 1)) }}" alt="Sampul {{ b.judul }}">
              {% else %}
                <div class="buku-cover-placeholder cover-v{{ b.id % 4 }}">
                  <span class="cover-inisial">{{ (b.judul or '?')[:1]|upper }}</span>
                  <span class="cover-ket">Tanpa sampul</span>
                </div>
              {% endif %}
              <span class="buku-stok-badge">{{ jumlah }}x dipinjam</span>
            </a>
            <div class="buku-card-body">
              <a href="{{ url_for('buku.detail_buku', buku_id=b.id) }}" class="buku-judul">{{ b.judul }}</a>
              <div class="buku-penulis">{{ b.penulis }}</div>
              <div class="buku-card-actions">
                <form method="POST" action="{{ url_for('peminjaman.ajukan_peminjaman', buku_id=b.id) }}"
                      onsubmit="return confirm('Ajukan peminjaman buku ini?');">
                  <button class="btn btn-sm btn-accent" type="submit">Ajukan</button>
                </form>
              </div>
            </div>
          </div>
        {% endfor %}
      </div>
    {% else %}
      <div class="card empty-state" style="padding:1rem;">
        <p style="margin:0;">Belum ada data peminjaman untuk dijadikan rekomendasi. Jelajahi <a href="{{ url_for('buku.daftar_buku') }}">koleksi buku</a> kami!</p>
      </div>
    {% endif %}
  </section>

{% else %}
  {# ================= DASHBOARD STAF & OPERATOR ================= #}
  <div class="grid-3">
    <div class="stat-box"><span class="stat-icon tone-maroon"><svg class="icon"><use href="#i-book"></use></svg></span><div class="angka">{{ total_buku }}</div><div class="label">Judul Buku</div></div>
    <div class="stat-box"><span class="stat-icon tone-gold"><svg class="icon"><use href="#i-folder"></use></svg></span><div class="angka">{{ total_stok }}</div><div class="label">Total Stok</div></div>
    <div class="stat-box"><span class="stat-icon tone-blue"><svg class="icon"><use href="#i-book-open"></use></svg></span><div class="angka">{{ sedang_dipinjam }}</div><div class="label">Sedang Dipinjam</div></div>
    <div class="stat-box"><span class="stat-icon tone-red"><svg class="icon"><use href="#i-alert"></use></svg></span><div class="angka">{{ terlambat }}</div><div class="label">Terlambat</div></div>
    <a class="stat-box stat-link" href="{{ url_for('denda.daftar_denda') }}"><span class="stat-icon tone-amber"><svg class="icon"><use href="#i-coins"></use></svg></span><div class="angka angka-rp">{{ (denda_belum_lunas + denda_berjalan)|rupiah }}</div><div class="label">Denda (belum lunas + berjalan)</div></a>
    {% if current_user.is_kepala %}
    <div class="stat-box"><span class="stat-icon tone-green"><svg class="icon"><use href="#i-users"></use></svg></span><div class="angka">{{ total_anggota }}</div><div class="label">Total Mahasiswa</div></div>
    <div class="stat-box"><span class="stat-icon tone-amber"><svg class="icon"><use href="#i-clock"></use></svg></span><div class="angka">{{ menunggu_persetujuan }}</div><div class="label">Menunggu Persetujuan</div></div>
    {% endif %}
  </div>

  <section class="dash-section">
    <h3 class="dash-section-title"><svg class="icon"><use href="#i-bell"></use></svg> Segera Jatuh Tempo <span class="dash-section-sub">({{ config.PERINGATAN_JATUH_TEMPO_HARI }} hari ke depan)</span></h3>
    {% if akan_jatuh_tempo %}
      <div class="card">
        <div class="table-scroll">
        <table>
          <thead><tr><th>Buku</th><th>Peminjam</th><th>Jatuh Tempo</th></tr></thead>
          <tbody>
            {% for p in akan_jatuh_tempo %}
            <tr>
              <td>{{ p.buku.judul }}</td>
              <td>{{ p.anggota.nama_lengkap }}</td>
              <td>
                {{ p.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}
                {% if p.tanggal_jatuh_tempo == today %}<span class="badge badge-warning" style="margin-left:0.4rem;">Hari ini</span>{% endif %}
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        </div>
      </div>
    {% else %}
      <div class="card empty-state" style="padding:1rem;">
        <p style="margin:0;">Tidak ada peminjaman yang jatuh tempo dalam {{ config.PERINGATAN_JATUH_TEMPO_HARI }} hari ke depan.</p>
      </div>
    {% endif %}
  </section>

  <section class="dash-section">
    <h3 class="dash-section-title"><svg class="icon"><use href="#i-bar-chart"></use></svg> Statistik &amp; Grafik</h3>
    <div class="chart-grid">
      <div class="card chart-card">
        <div class="chart-card-title">Tren Peminjaman (6 Bulan Terakhir)</div>
        <div class="chart-wrap"><canvas id="grafikBulanan"></canvas></div>
      </div>
      <div class="card chart-card">
        <div class="chart-card-title">Buku Paling Sering Dipinjam</div>
        <div class="chart-wrap"><canvas id="grafikTopBuku"></canvas></div>
      </div>
      <div class="card chart-card">
        <div class="chart-card-title">Mahasiswa Paling Sering Meminjam</div>
        <div class="chart-wrap"><canvas id="grafikTopMahasiswa"></canvas></div>
      </div>
      <div class="card chart-card">
        <div class="chart-card-title">Distribusi Koleksi per Kategori</div>
        <div class="chart-wrap"><canvas id="grafikKategori"></canvas></div>
      </div>
    </div>
  </section>

  <section class="dash-section">
    <h3 class="dash-section-title"><svg class="icon"><use href="#i-clock"></use></svg> Aktivitas Peminjaman Terbaru</h3>
    {% if peminjaman_terbaru %}
      <div class="card">
        <div class="table-scroll">
        <table>
          <thead><tr><th>Buku</th><th>Peminjam</th><th>Tgl Pinjam</th><th>Status</th></tr></thead>
          <tbody>
            {% for p in peminjaman_terbaru %}
            <tr>
              <td>{{ p.buku.judul }}</td>
              <td>{{ p.anggota.nama_lengkap }}</td>
              <td>{{ p.tanggal_pinjam.strftime('%d-%m-%Y') }}</td>
              <td>
                {% if p.status == 'dikembalikan' %}<span class="badge badge-success">Dikembalikan</span>
                {% elif p.is_telat %}<span class="badge badge-danger">Terlambat</span>
                {% else %}<span class="badge badge-info">Dipinjam</span>{% endif %}
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        </div>
      </div>
    {% else %}
      <div class="card empty-state" style="padding:1rem;">
        <p style="margin:0;">Belum ada aktivitas peminjaman.</p>
      </div>
    {% endif %}
  </section>
{% endif %}
{% endblock %}

{% block scripts %}
<script>
  document.addEventListener('DOMContentLoaded', function () {
    var jam = new Date().getHours();
    var sapa = jam < 11 ? 'Selamat pagi' : jam < 15 ? 'Selamat siang' : jam < 18 ? 'Selamat sore' : 'Selamat malam';
    var elSapa = document.getElementById('heroSapa');
    if (elSapa) elSapa.textContent = sapa + ',';
    var elTgl = document.getElementById('heroTanggal');
    if (elTgl) {
      try { elTgl.textContent = new Date().toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) {}
    }
  });
</script>
<script>
  // Animasi hitung-naik utk angka statistik (mis. 128 dianimasikan dari 0 -> 128)
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.stat-box .angka').forEach(function (el) {
      var teks = el.textContent.trim();
      if (!/^\d+$/.test(teks)) return; // lewati yang bukan angka murni (mis. badge status)
      var target = parseInt(teks, 10);
      if (target === 0) return;
      var durasi = 600, mulai = null;
      function langkah(ts) {
        if (!mulai) mulai = ts;
        var progres = Math.min((ts - mulai) / durasi, 1);
        var nilaiSekarang = Math.round(target * (1 - Math.pow(1 - progres, 3))); // ease-out
        el.textContent = nilaiSekarang;
        if (progres < 1) requestAnimationFrame(langkah);
        else el.textContent = target;
      }
      requestAnimationFrame(langkah);
    });
  });
</script>
{% if not current_user.is_mahasiswa %}
<script>
  document.addEventListener('DOMContentLoaded', function () {
    if (typeof Chart === 'undefined') return; // CDN gagal dimuat (mis. tidak ada internet) -> lewati grafik, dashboard lain tetap jalan

    var dataBulanan = { labels: {{ labels_grafik_bulanan|tojson }}, data: {{ data_grafik_bulanan|tojson }} };
    var dataTopBuku = { labels: {{ labels_grafik_top_buku|tojson }}, data: {{ data_grafik_top_buku|tojson }} };
    var dataTopMhs = { labels: {{ labels_grafik_top_mhs|tojson }}, data: {{ data_grafik_top_mhs|tojson }} };
    var dataKategori = { labels: {{ labels_grafik_kategori|tojson }}, data: {{ data_grafik_kategori|tojson }} };
    var grafikAktif = [];

    function cssVar(nama) {
      return getComputedStyle(document.documentElement).getPropertyValue(nama).trim();
    }

    function tambahPesanKosong(canvas, teks) {
      var wrap = canvas.parentElement;
      if (!wrap) return;
      var lama = wrap.querySelector('.chart-kosong');
      if (lama) lama.remove();
      wrap.insertAdjacentHTML('beforeend', '<p class="chart-kosong" style="text-align:center;color:var(--muted);font-size:0.85rem;">' + teks + '</p>');
    }

    // Gambar semua grafik memakai warna tema yang sedang aktif.
    // Dipanggil saat halaman dimuat DAN setiap kali mode terang/gelap diganti,
    // sehingga teks/garis grafik tidak pernah menyatu dengan latar kartu.
    function gambarGrafik() {
      grafikAktif.forEach(function (g) { g.destroy(); });
      grafikAktif = [];

      var warnaPrimer = cssVar('--primary');
      var warnaAksen = cssVar('--accent');
      var warnaTeks = cssVar('--chart-text');
      var warnaGaris = cssVar('--chart-grid');
      var warnaKartu = cssVar('--card-bg');
      var paletteKategori = [
        warnaPrimer, warnaAksen, cssVar('--info'), cssVar('--success'),
        cssVar('--warning'), cssVar('--primary-light'), cssVar('--danger')
      ];

      Chart.defaults.color = warnaTeks;
      Chart.defaults.borderColor = warnaGaris;
      Chart.defaults.font.family = "Inter, 'Segoe UI', Roboto, Arial, sans-serif";

      var skalaTeks = { ticks: { color: warnaTeks, precision: 0 }, grid: { color: warnaGaris }, beginAtZero: true };
      var skalaLabel = { ticks: { color: warnaTeks }, grid: { color: warnaGaris } };

      var elBulanan = document.getElementById('grafikBulanan');
      if (elBulanan) {
        grafikAktif.push(new Chart(elBulanan, {
          type: 'line',
          data: {
            labels: dataBulanan.labels,
            datasets: [{
              label: 'Jumlah Peminjaman',
              data: dataBulanan.data,
              borderColor: warnaAksen,
              backgroundColor: warnaAksen + '33',
              pointBackgroundColor: warnaAksen,
              tension: 0.35, fill: true, pointRadius: 4,
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { x: skalaLabel, y: skalaTeks }
          }
        }));
      }

      var elTopBuku = document.getElementById('grafikTopBuku');
      if (elTopBuku) {
        grafikAktif.push(new Chart(elTopBuku, {
          type: 'bar',
          data: {
            labels: dataTopBuku.labels,
            datasets: [{ label: 'Kali Dipinjam', data: dataTopBuku.data, backgroundColor: warnaAksen, borderRadius: 6 }]
          },
          options: {
            indexAxis: 'y', responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { x: skalaTeks, y: skalaLabel }
          }
        }));
        if (dataTopBuku.labels.length === 0) tambahPesanKosong(elTopBuku, 'Belum ada data peminjaman.');
      }

      var elTopMhs = document.getElementById('grafikTopMahasiswa');
      if (elTopMhs) {
        grafikAktif.push(new Chart(elTopMhs, {
          type: 'bar',
          data: {
            labels: dataTopMhs.labels,
            datasets: [{ label: 'Buku Dipinjam', data: dataTopMhs.data, backgroundColor: warnaAksen, borderRadius: 6 }]
          },
          options: {
            indexAxis: 'y', responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { x: skalaTeks, y: skalaLabel }
          }
        }));
        if (dataTopMhs.labels.length === 0) tambahPesanKosong(elTopMhs, 'Belum ada data peminjaman.');
      }

      var elKategori = document.getElementById('grafikKategori');
      if (elKategori) {
        grafikAktif.push(new Chart(elKategori, {
          type: 'doughnut',
          data: {
            labels: dataKategori.labels,
            datasets: [{ data: dataKategori.data, backgroundColor: paletteKategori, borderColor: warnaKartu, borderWidth: 2 }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { color: warnaTeks, boxWidth: 12, padding: 10 } } }
          }
        }));
        if (dataKategori.labels.length === 0) tambahPesanKosong(elKategori, 'Belum ada buku berkategori.');
      }
    }

    gambarGrafik();

    // Gambar ulang grafik otomatis ketika tombol tema (terang/gelap) ditekan
    new MutationObserver(function () { gambarGrafik(); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  });
</script>
{% endif %}
{% endblock %}
```


## `Website/templates/denda/daftar.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Denda Keterlambatan{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-coins"></use></svg> Denda Keterlambatan</h2>
  <p class="page-sub">
    {% if config.DENDA_PER_HARI > 0 %}
      Tarif saat ini <strong>{{ config.DENDA_PER_HARI|rupiah }}</strong> per hari{% if config.MASA_TENGGANG_HARI %}, tenggang {{ config.MASA_TENGGANG_HARI }} hari{% endif %}{% if config.DENDA_MAKS %}, maksimal {{ config.DENDA_MAKS|rupiah }} per buku{% endif %}.
    {% else %}
      Denda sedang <strong>dinonaktifkan</strong> (tarif Rp 0).
    {% endif %}
    {% if current_user.is_kepala %}<a href="{{ url_for('pengaturan.halaman') }}">Ubah pengaturan denda</a>{% endif %}
  </p>
</div>

<div class="grid-3">
  <div class="stat-box"><span class="stat-icon tone-red"><svg class="icon"><use href="#i-alert"></use></svg></span><div class="angka angka-rp">{{ total_belum_lunas|rupiah }}</div><div class="label">Belum Lunas</div></div>
  <div class="stat-box"><span class="stat-icon tone-amber"><svg class="icon"><use href="#i-clock"></use></svg></span><div class="angka angka-rp">{{ total_berjalan|rupiah }}</div><div class="label">Berjalan (buku belum kembali)</div></div>
  <div class="stat-box"><span class="stat-icon tone-green"><svg class="icon"><use href="#i-check-circle"></use></svg></span><div class="angka angka-rp">{{ terkumpul_bulan_ini|rupiah }}</div><div class="label">Terkumpul Bulan Ini</div></div>
  <div class="stat-box"><span class="stat-icon tone-gold"><svg class="icon"><use href="#i-coins"></use></svg></span><div class="angka angka-rp">{{ terkumpul_total|rupiah }}</div><div class="label">Total Terkumpul</div></div>
</div>

<div class="search-bar" style="margin-top:1.2rem;">
  <a href="{{ url_for('denda.daftar_denda', status='belum_lunas', q=q) }}" class="chip{{ ' chip-active' if status=='belum_lunas' else '' }}">Belum Lunas</a>
  <a href="{{ url_for('denda.daftar_denda', status='berjalan', q=q) }}" class="chip{{ ' chip-active' if status=='berjalan' else '' }}">Berjalan</a>
  <a href="{{ url_for('denda.daftar_denda', status='lunas', q=q) }}" class="chip{{ ' chip-active' if status=='lunas' else '' }}">Lunas</a>
  <a href="{{ url_for('denda.daftar_denda', status='dibebaskan', q=q) }}" class="chip{{ ' chip-active' if status=='dibebaskan' else '' }}">Dibebaskan</a>
  <a href="{{ url_for('denda.daftar_denda', status='semua', q=q) }}" class="chip{{ ' chip-active' if status=='semua' else '' }}">Semua</a>
</div>

<form method="GET" class="search-bar">
  <input type="hidden" name="status" value="{{ status }}">
  <input type="text" name="q" placeholder="Cari nama, username, NIM, atau judul buku..." value="{{ q }}">
  <button class="btn" type="submit">Cari</button>
  {% if q %}<a href="{{ url_for('denda.daftar_denda', status=status) }}" class="btn btn-ghost">Reset</a>{% endif %}
  <a href="{{ url_for('denda.ekspor_denda', status=status if status != 'berjalan' else 'semua') }}" class="btn btn-ghost"><svg class="icon"><use href="#i-download"></use></svg> Ekspor Excel</a>
</form>

<div class="card">
  <div class="table-scroll">
  <table>
    <thead>
      <tr><th>Mahasiswa</th><th>Buku</th><th>Jatuh Tempo</th><th>Tgl Kembali</th><th>Hari Telat</th><th>Denda</th><th>Status</th><th>Aksi</th></tr>
    </thead>
    <tbody>
      {% for p in daftar %}
      <tr>
        <td>{{ p.anggota.nama_lengkap }}<br><small style="color:var(--muted);">{{ p.anggota.nim or p.anggota.username }}</small></td>
        <td>{{ p.buku.judul }}</td>
        <td>{{ p.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}</td>
        <td>{{ p.tanggal_kembali.strftime('%d-%m-%Y') if p.tanggal_kembali else '-' }}</td>
        <td>{{ p.hari_telat }} hari</td>
        <td><strong>{{ denda_sekarang(p)|rupiah }}</strong></td>
        <td>
          {% if p.status == 'dipinjam' %}<span class="badge badge-warning">Berjalan</span>
          {% elif p.status_denda == 'belum_lunas' %}<span class="badge badge-danger">Belum Lunas</span>
          {% elif p.status_denda == 'lunas' %}<span class="badge badge-success">Lunas {{ p.tanggal_denda_selesai.strftime('%d-%m-%Y') if p.tanggal_denda_selesai }}</span>
          {% elif p.status_denda == 'dibebaskan' %}<span class="badge badge-info" title="{{ p.catatan_denda or '' }}">Dibebaskan</span>
          {% endif %}
        </td>
        <td>
          {% if p.status == 'dipinjam' %}
            <form method="POST" action="{{ url_for('peminjaman.kembalikan_buku', peminjaman_id=p.id) }}"
                  onsubmit="return confirm('Konfirmasi pengembalian buku ini?');">
              <button class="btn btn-sm btn-success" type="submit"><svg class="icon"><use href="#i-check"></use></svg> Kembalikan</button>
              <button class="btn btn-sm btn-accent" type="submit" name="bayar" value="1">Kembalikan &amp; Lunasi</button>
            </form>
          {% elif p.status_denda == 'belum_lunas' %}
            <form method="POST" action="{{ url_for('denda.lunasi', peminjaman_id=p.id) }}"
                  onsubmit="return confirm('Catat denda {{ p.denda|rupiah }} sebagai LUNAS?');">
              <button class="btn btn-sm btn-success" type="submit"><svg class="icon"><use href="#i-check-circle"></use></svg> Tandai Lunas</button>
            </form>
            {% if current_user.is_kepala %}
            <form method="POST" action="{{ url_for('denda.bebaskan', peminjaman_id=p.id) }}"
                  onsubmit="var c = prompt('Alasan membebaskan denda (opsional):'); if (c === null) return false; this.catatan.value = c; return true;">
              <input type="hidden" name="catatan" value="">
              <button class="btn btn-sm btn-warning" type="submit">Bebaskan</button>
            </form>
            {% endif %}
          {% else %}-{% endif %}
        </td>
      </tr>
      {% else %}
      <tr><td colspan="8">Tidak ada data denda untuk filter ini.</td></tr>
      {% endfor %}
    </tbody>
  </table>
  </div>
  {% if daftar %}<p class="excel-footnote" style="border-top:none;">{{ daftar|length }} data · total pada daftar ini <strong>{{ total_daftar|rupiah }}</strong></p>{% endif %}
</div>
{% endblock %}
```


## `Website/templates/kartu/cetak.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
<!DOCTYPE html>
<html lang="id" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kartu Perpustakaan - {{ anggota.nama_lengkap }}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <div class="cetak-page">
    <div class="kartu-anggota {{ 'kartu-role-staf' if anggota.role == 'staf' else ('kartu-role-kepala' if anggota.role == 'kepala_perpustakaan' else '') }}">
      <span class="role-pita">{{ anggota.role_label }}</span>
      <img src="{{ url_for('static', filename='img/logo_stikom.png') }}" alt="Logo" class="logo-kecil">
      <div class="label">Kartu Perpustakaan STIKOM Kendari</div>
      <div class="label" style="margin-top:0.4rem;">NIM</div>
      <div class="nomor">{{ kartu.nim or '-' }}</div>
      <div style="font-size:1.05rem; margin-bottom:0.5rem;">{{ anggota.nama_lengkap }}</div>
      <div style="font-size:0.8rem; opacity:0.85;">
        Terbit: {{ kartu.tanggal_terbit.strftime('%d-%m-%Y') }} &nbsp;|&nbsp;
        Berlaku s.d.: {{ kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y') }}
      </div>
      <div style="margin-top:0.6rem;">
        {% if kartu.is_kadaluarsa %}
          <span class="badge badge-danger">Kadaluarsa</span>
        {% elif kartu.status == 'aktif' %}
          <span class="badge badge-success">Aktif</span>
        {% else %}
          <span class="badge badge-danger">Nonaktif</span>
        {% endif %}
      </div>
    </div>

    <div class="cetak-no-print" style="display:flex; gap:0.6rem; flex-wrap:wrap; justify-content:center;">
      <button class="btn btn-accent" onclick="window.print()"><svg class="icon"><use href="#i-printer"></use></svg> Cetak / Simpan sebagai PDF</button>
      <button class="btn" style="background:#888;" onclick="window.close()">Tutup Tab Ini</button>
    </div>
    <p class="cetak-hint cetak-no-print">
      Pada dialog cetak yang muncul, pilih tujuan <strong>"Simpan sebagai PDF"</strong> untuk mengunduh kartu ini sebagai file PDF.
    </p>
  </div>

  <script>
    // otomatis buka dialog cetak begitu halaman siap, memudahkan alur "download"
    window.addEventListener('load', function () {
      setTimeout(function () { window.print(); }, 300);
    });
  </script>
</body>
</html>
```


## `Website/templates/kartu/edit.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Atur Kartu Perpustakaan{% endblock %}
{% block content %}
<div class="card" style="max-width:480px;">
  <h2>Atur Kartu Perpustakaan</h2>
  <p class="page-sub" style="margin-top:-0.4rem;">
    Pemilik: <strong>{{ pemilik.nama_lengkap }}</strong> ({{ pemilik.role_label }})
  </p>
  <form method="POST">
    <div class="form-group">
      <label>NIM (ID Kartu) {% if pemilik.is_mahasiswa %}<small style="color:var(--muted);">wajib, {{ config.NIM_PANJANG_MIN }}-{{ config.NIM_PANJANG_MAKS }} digit</small>{% else %}<small style="color:var(--muted);">opsional</small>{% endif %}</label>
      <input type="text" name="nim" value="{{ pemilik.nim or '' }}" inputmode="numeric" maxlength="{{ config.NIM_PANJANG_MAKS }}" pattern="[0-9]*" {{ 'required' if pemilik.is_mahasiswa }}>
    </div>
    <div class="form-group">
      <label>Tanggal Terbit</label>
      <input type="date" name="tanggal_terbit" value="{{ kartu.tanggal_terbit.isoformat() }}" required>
    </div>
    <div class="form-group">
      <label>Berlaku Sampai</label>
      <input type="date" name="tanggal_kadaluarsa" value="{{ kartu.tanggal_kadaluarsa.isoformat() }}" required>
    </div>
    <div class="form-group">
      <label>Status</label>
      <select name="status">
        <option value="aktif" {{ 'selected' if kartu.status == 'aktif' }}>Aktif</option>
        <option value="nonaktif" {{ 'selected' if kartu.status == 'nonaktif' }}>Nonaktif</option>
      </select>
    </div>
    <button class="btn" type="submit">Simpan</button>
    <a href="{{ url_for('kartu.kelola_kartu') }}" class="btn btn-ghost">Batal</a>
  </form>
</div>
{% endblock %}
```


## `Website/templates/kartu/kartu.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Kartu Perpustakaan{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-id-card"></use></svg> Kartu Perpustakaan Digital</h2>
  {% if anggota.id != current_user.id %}<p class="page-sub">Milik: {{ anggota.nama_lengkap }} ({{ anggota.role_label }})</p>{% endif %}
</div>

<div class="kartu-anggota {{ 'kartu-role-staf' if anggota.role == 'staf' else ('kartu-role-kepala' if anggota.role == 'kepala_perpustakaan' else '') }}">
  <span class="role-pita">{{ anggota.role_label }}</span>
  <img src="{{ url_for('static', filename='img/logo_stikom.png') }}" alt="Logo" class="logo-kecil">
  <div class="label">Kartu Perpustakaan STIKOM Kendari</div>
  <div class="label" style="margin-top:0.4rem;">NIM</div>
  <div class="nomor">{{ kartu.nim or '-' }}</div>
  <div style="font-size:1.05rem; margin-bottom:0.5rem;">{{ anggota.nama_lengkap }}</div>
  <div style="font-size:0.8rem; opacity:0.85;">
    Terbit: {{ kartu.tanggal_terbit.strftime('%d-%m-%Y') }} &nbsp;|&nbsp;
    Berlaku s.d.: {{ kartu.tanggal_kadaluarsa.strftime('%d-%m-%Y') }}
  </div>
  <div style="margin-top:0.6rem;">
    {% if kartu.is_kadaluarsa %}
      <span class="badge badge-danger">Kadaluarsa</span>
    {% elif kartu.status == 'aktif' %}
      <span class="badge badge-success">Aktif</span>
    {% else %}
      <span class="badge badge-danger">Nonaktif</span>
    {% endif %}
  </div>
</div>

<div class="kartu-wrap-actions">
  {% if anggota.id == current_user.id %}
    <a href="{{ url_for('kartu.kartu_saya_cetak') }}" target="_blank" class="btn btn-accent"><svg class="icon"><use href="#i-download"></use></svg> Download Kartu (PDF)</a>
  {% else %}
    {% if kartu.id and (current_user.is_staf or current_user.is_kepala) %}
      <a href="{{ url_for('kartu.edit_kartu', kartu_id=kartu.id) }}" class="btn"><svg class="icon"><use href="#i-edit"></use></svg> Atur Kartu</a>
    {% endif %}
    <a href="{{ url_for('kartu.kartu_anggota_lain_cetak', user_id=anggota.id) }}" target="_blank" class="btn btn-accent"><svg class="icon"><use href="#i-download"></use></svg> Download Kartu (PDF)</a>
  {% endif %}
</div>
{% endblock %}
```


## `Website/templates/kartu/kelola.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Kelola Kartu Perpustakaan{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-id-card"></use></svg> Kelola Kartu Perpustakaan</h2>
  <p class="page-sub">Atur NIM (ID kartu), masa berlaku, dan status kartu. Kartu nonaktif atau kadaluarsa tidak dapat dipakai untuk meminjam buku.</p>
</div>

<form method="GET" style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:1rem;">
  <input type="text" name="q" placeholder="Cari nama / username / NIM..." value="{{ q }}" style="flex:1; min-width:220px;">
  <select name="status">
    <option value="semua" {{ 'selected' if filter_status == 'semua' }}>Semua status</option>
    <option value="aktif" {{ 'selected' if filter_status == 'aktif' }}>Aktif</option>
    <option value="nonaktif" {{ 'selected' if filter_status == 'nonaktif' }}>Nonaktif</option>
    <option value="kadaluarsa" {{ 'selected' if filter_status == 'kadaluarsa' }}>Kadaluarsa</option>
  </select>
  <button class="btn" type="submit">Cari</button>
</form>

<div class="card">
  {% if daftar %}
  <div class="table-scroll">
  <table>
    <thead>
      <tr><th>NIM</th><th>Nama</th><th>Role</th><th>Terbit</th><th>Berlaku s.d.</th><th>Status</th><th>Aksi</th></tr>
    </thead>
    <tbody>
    {% for k in daftar %}
      <tr>
        <td>{{ k.nim or '-' }}</td>
        <td>{{ k.pemilik.nama_lengkap }}<br><small style="color:var(--muted);">{{ k.pemilik.username }}</small></td>
        <td>{{ k.pemilik.role_label }}</td>
        <td>{{ k.tanggal_terbit.strftime('%d-%m-%Y') }}</td>
        <td>{{ k.tanggal_kadaluarsa.strftime('%d-%m-%Y') }}</td>
        <td>
          {% if k.is_kadaluarsa %}<span class="badge badge-danger">Kadaluarsa</span>
          {% elif k.status == 'aktif' %}<span class="badge badge-success">Aktif</span>
          {% else %}<span class="badge badge-danger">Nonaktif</span>{% endif %}
          {% if not k.nim %}<span class="badge badge-warning">NIM kosong</span>{% endif %}
        </td>
        <td>
          <div style="display:flex; gap:0.35rem; flex-wrap:wrap;">
            <a href="{{ url_for('kartu.kartu_anggota_lain', user_id=k.user_id) }}" class="btn btn-sm"><svg class="icon"><use href="#i-eye"></use></svg> Lihat</a>
            <a href="{{ url_for('kartu.edit_kartu', kartu_id=k.id) }}" class="btn btn-sm"><svg class="icon"><use href="#i-edit"></use></svg> Atur</a>
            <form method="POST" action="{{ url_for('kartu.perpanjang_kartu', kartu_id=k.id) }}" style="display:inline;"
                  onsubmit="return confirm('Perpanjang masa berlaku kartu ini selama {{ config.MASA_BERLAKU_KARTU_HARI }} hari?');">
              <button class="btn btn-sm btn-accent" type="submit">Perpanjang</button>
            </form>
            <form method="POST" action="{{ url_for('kartu.toggle_kartu', kartu_id=k.id) }}" style="display:inline;">
              <button class="btn btn-sm btn-warning" type="submit">{{ 'Nonaktifkan' if k.status == 'aktif' else 'Aktifkan' }}</button>
            </form>
          </div>
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
  </div>
  {% else %}
    <div class="empty-state"><p>Tidak ada kartu yang cocok dengan pencarian.</p></div>
  {% endif %}
</div>

{% if tanpa_kartu %}
<h3 style="margin-top:1.5rem;">Akun yang belum memiliki kartu</h3>
<div class="card">
  <div class="table-scroll">
  <table>
    <thead><tr><th>Nama</th><th>NIM</th><th>Role</th><th>Aksi</th></tr></thead>
    <tbody>
    {% for u in tanpa_kartu %}
      <tr>
        <td>{{ u.nama_lengkap }}</td>
        <td>{{ u.nim or '-' }}</td>
        <td>{{ u.role_label }}</td>
        <td>
          <form method="POST" action="{{ url_for('kartu.terbitkan_kartu', user_id=u.id) }}" style="display:inline;">
            <button class="btn btn-sm btn-accent" type="submit">Terbitkan Kartu</button>
          </form>
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
  </div>
</div>
{% endif %}
{% endblock %}
```


## `Website/templates/laporan/mahasiswa_aktif.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Mahasiswa Paling Aktif Meminjam{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-users"></use></svg> Mahasiswa Paling Sering Meminjam</h2>
  <p class="page-sub">Peringkat berdasarkan jumlah buku yang dipinjam. Pengajuan yang belum disetujui atau ditolak tidak dihitung.</p>
</div>

<div class="search-bar" style="justify-content:space-between;">
  <div class="kategori-chips" style="margin:0;">
    {% for kunci, (label, _hari) in periode_opsi.items() %}
      <a class="chip {{ 'chip-active' if kunci == periode else '' }}" href="{{ url_for('laporan.mahasiswa_aktif', periode=kunci) }}">{{ label }}</a>
    {% endfor %}
  </div>
  <a class="btn btn-sm btn-accent" href="{{ url_for('laporan.ekspor_mahasiswa_aktif', periode=periode) }}"><svg class="icon"><use href="#i-download"></use></svg> Ekspor Excel</a>
</div>

<div class="card">
  <div class="table-scroll">
  <table class="tabel-peringkat">
    <thead>
      <tr>
        <th>Mahasiswa</th><th>NIM</th><th>Total Dipinjam</th>
        <th>Judul Berbeda</th><th>Sedang Dipinjam</th><th>Terlambat</th><th>Terakhir Meminjam</th>
      </tr>
    </thead>
    <tbody>
      {% for b in hasil %}
      <tr>
        <td class="sel-nama">
          <span class="no-peringkat {{ 'no-top' if b.peringkat <= 3 else '' }}">{{ b.peringkat }}</span>
          <a href="{{ url_for('peminjaman.riwayat_anggota', user_id=b.user.id) }}">{{ b.user.nama_lengkap }}</a>
        </td>
        <td class="mono">{{ b.user.nim or b.user.username }}</td>
        <td>
          <span class="bar-angka">
            <span class="bar" aria-hidden="true"><i style="width: {{ (b.total / total_terbanyak * 100)|round(0)|int }}%"></i></span>
            <strong>{{ b.total }}</strong>
          </span>
        </td>
        <td>{{ b.judul_unik }}</td>
        <td>{{ b.sedang_dipinjam or '-' }}</td>
        <td>{% if b.terlambat %}<span class="badge badge-danger">{{ b.terlambat }}x</span>{% else %}-{% endif %}</td>
        <td>{{ b.terakhir.strftime('%d-%m-%Y') if b.terakhir else '-' }}</td>
      </tr>
      {% else %}
      <tr><td colspan="7">Belum ada data peminjaman pada periode ini.</td></tr>
      {% endfor %}
    </tbody>
  </table>
  </div>
  {% if hasil %}
  <p class="excel-footnote" style="border-top:none; padding-left:0;">
    Menampilkan {{ hasil|length }} mahasiswa teratas ({{ periode_opsi[periode][0]|lower }}). Peringkat yang sama berarti jumlah pinjam sama; nama diurutkan dari yang terbaru meminjam. Ekspor Excel memuat seluruh mahasiswa, bukan hanya 50 teratas.
  </p>
  {% endif %}
</div>
{% endblock %}
```


## `Website/templates/laporan/populer.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Buku Populer{% endblock %}
{% block content %}
<h2><svg class="icon"><use href="#i-trend-up"></use></svg> Statistik Buku Paling Populer</h2>
<div class="card">
  <div class="table-scroll">
  <table>
    <thead><tr><th>#</th><th>Judul</th><th>Penulis</th><th>Jumlah Dipinjam</th></tr></thead>
    <tbody>
      {% for buku, jumlah in hasil %}
      <tr>
        <td>{{ loop.index }}</td>
        <td><a href="{{ url_for('buku.detail_buku', buku_id=buku.id) }}">{{ buku.judul }}</a></td>
        <td>{{ buku.penulis }}</td>
        <td>{{ jumlah }}</td>
      </tr>
      {% else %}
      <tr><td colspan="4">Belum ada data peminjaman.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
</div>
{% endblock %}
```


## `Website/templates/laporan/terlambat.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Buku Terlambat{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-alert"></use></svg> Buku Terlambat Dikembalikan</h2>
  <p class="page-sub">{{ daftar|length }} buku lewat jatuh tempo · denda berjalan <strong>{{ total_denda|rupiah }}</strong>. Urut dari yang paling lama terlambat.</p>
</div>

<div class="search-bar">
  <a href="{{ url_for('laporan.ekspor_terlambat') }}" class="btn btn-ghost"><svg class="icon"><use href="#i-download"></use></svg> Ekspor Excel (untuk menghubungi peminjam)</a>
</div>

<div class="card">
  <div class="table-scroll">
  <table>
    <thead><tr><th>Mahasiswa</th><th>Buku</th><th>Jatuh Tempo</th><th>Hari Telat</th><th>Denda Berjalan</th><th>Aksi</th></tr></thead>
    <tbody>
      {% for p in daftar %}
      <tr>
        <td>{{ p.anggota.nama_lengkap }}<br><small style="color:var(--muted);">{{ p.anggota.no_telepon or p.anggota.email }}</small></td>
        <td>{{ p.buku.judul }}</td>
        <td>{{ p.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}</td>
        <td><span class="badge badge-danger">{{ p.hari_telat }} hari</span></td>
        <td><strong>{{ denda_sekarang(p)|rupiah }}</strong></td>
        <td>
          <form method="POST" action="{{ url_for('peminjaman.kembalikan_buku', peminjaman_id=p.id) }}"
                onsubmit="return confirm('Konfirmasi pengembalian buku ini?');">
            <button class="btn btn-sm btn-success" type="submit"><svg class="icon"><use href="#i-check"></use></svg> Kembalikan</button>
            <button class="btn btn-sm btn-accent" type="submit" name="bayar" value="1">Kembalikan &amp; Lunasi</button>
          </form>
          <a href="{{ url_for('peminjaman.riwayat_anggota', user_id=p.user_id) }}" class="btn btn-sm"><svg class="icon"><use href="#i-clock"></use></svg> Riwayat</a>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="6">Tidak ada buku yang terlambat. 🎉</td></tr>
      {% endfor %}
    </tbody>
  </table>
  </div>
</div>
{% endblock %}
```


## `Website/templates/laporan/tidak_populer.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Buku Tidak Populer{% endblock %}
{% block content %}
<h2><svg class="icon"><use href="#i-trend-down"></use></svg> Statistik Buku Tidak Populer</h2>

<h3>Belum Pernah Dipinjam Sama Sekali</h3>
<div class="card">
  <div class="table-scroll">
  <table>
    <thead><tr><th>Judul</th><th>Penulis</th><th>Stok</th></tr></thead>
    <tbody>
      {% for buku in tidak_pernah %}
      <tr>
        <td><a href="{{ url_for('buku.detail_buku', buku_id=buku.id) }}">{{ buku.judul }}</a></td>
        <td>{{ buku.penulis }}</td>
        <td>{{ buku.stok }}</td>
      </tr>
      {% else %}
      <tr><td colspan="3">Semua buku pernah dipinjam minimal 1 kali.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
</div>

<h3>Jarang Dipinjam (maks. 2 kali)</h3>
<div class="card">
  <div class="table-scroll">
  <table>
    <thead><tr><th>Judul</th><th>Penulis</th><th>Jumlah Dipinjam</th></tr></thead>
    <tbody>
      {% for buku, jumlah in jarang %}
      <tr>
        <td><a href="{{ url_for('buku.detail_buku', buku_id=buku.id) }}">{{ buku.judul }}</a></td>
        <td>{{ buku.penulis }}</td>
        <td>{{ jumlah }}</td>
      </tr>
      {% else %}
      <tr><td colspan="3">Tidak ada data.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
</div>
{% endblock %}
```


## `Website/templates/layout/base.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
<!DOCTYPE html>
<html lang="id" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <meta name="theme-color" content="#3c1512">
  <title>{% block title %}Perpustakaan{% endblock %} - STIKOM Kendari</title>
  <link rel="icon" href="{{ url_for('static', filename='img/logo_stikom.png') }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/mobile.css') }}">
  <script>
    /* Terapkan tema tersimpan SEBELUM halaman dirender, agar tidak "berkedip" */
    (function () {
      var tema = localStorage.getItem('tema') || 'light';
      document.documentElement.setAttribute('data-theme', tema);
    })();
  </script>
  {% block extra_head %}{% endblock %}
</head>
{% set pakai_sidebar = current_user.is_authenticated and current_user.is_kepala %}
<body class="{{ 'has-sidebar' if pakai_sidebar else '' }} {{ ('role-' ~ current_user.role) if current_user.is_authenticated else 'guest' }}">
  {% set tampilkan_loader_awal = (request.endpoint in ['auth.register', 'auth.login', 'buku.daftar_buku']) %}
  <div class="page-loader{{ '' if tampilkan_loader_awal else ' page-loader-hidden' }}" id="pageLoader">
    <img src="{{ url_for('static', filename='img/logo_stikom.png') }}" alt="Memuat" class="page-loader-logo">
    <div class="page-loader-bar"></div>
    <div class="page-loader-text">Memuat...</div>
  </div>

  {% include "layout/icons.html" %}

  {% if pakai_sidebar %}
    {# ================= SIDEBAR - khusus akun KEPALA PERPUSTAKAAN ================= #}
    <aside class="sidebar" id="sidebarOperator">
      <a href="{{ url_for('dashboard.index') }}" class="sidebar-brand">
        <img src="{{ url_for('static', filename='img/logo_stikom.png') }}" alt="Logo STIKOM Kendari">
        <span>Perpustakaan<br>STIKOM Kendari</span>
      </a>
      <nav class="sidebar-nav">
        <a class="side-link" href="{{ url_for('dashboard.index') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-home"></use></svg>Dashboard</span>
        </a>

        <div class="sidebar-nav-label">Koleksi</div>
        <div class="side-group">
          <button type="button" class="side-link side-group-toggle">
            <span class="side-link-main"><svg class="nav-icon"><use href="#i-book"></use></svg>Koleksi Buku</span>
            <svg class="side-caret"><use href="#i-chevron-down"></use></svg>
          </button>
          <div class="side-submenu">
            <a href="{{ url_for('buku.daftar_buku') }}"><svg class="nav-icon"><use href="#i-book"></use></svg>Daftar Buku</a>
            <a href="{{ url_for('buku.kategori') }}"><svg class="nav-icon"><use href="#i-folder"></use></svg>Kategori</a>
            <a href="{{ url_for('buku.import_excel') }}"><svg class="nav-icon"><use href="#i-upload"></use></svg>Import Excel</a>
            <a href="{{ url_for('buku.ekspor_buku') }}"><svg class="nav-icon"><use href="#i-download"></use></svg>Ekspor Excel</a>
          </div>
        </div>

        <div class="sidebar-nav-label">Sirkulasi</div>
        <a class="side-link" href="{{ url_for('peminjaman.daftar_peminjaman') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-book-open"></use></svg>Peminjaman</span>
        </a>
        <a class="side-link" href="{{ url_for('peminjaman.daftar_pengajuan') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-clipboard"></use></svg>Pengajuan</span>
          {% if jumlah_pengajuan_peminjaman %}<span class="badge badge-danger">{{ jumlah_pengajuan_peminjaman }}</span>{% endif %}
        </a>
        <a class="side-link" href="{{ url_for('denda.daftar_denda') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-coins"></use></svg>Denda</span>
        </a>
        <div class="side-group">
          <button type="button" class="side-link side-group-toggle">
            <span class="side-link-main"><svg class="nav-icon"><use href="#i-bar-chart"></use></svg>Laporan</span>
            <svg class="side-caret"><use href="#i-chevron-down"></use></svg>
          </button>
          <div class="side-submenu">
            <a href="{{ url_for('laporan.buku_terlambat') }}"><svg class="nav-icon"><use href="#i-alert"></use></svg>Buku Terlambat</a>
            <a href="{{ url_for('laporan.buku_populer') }}"><svg class="nav-icon"><use href="#i-flame"></use></svg>Buku Populer</a>
            <a href="{{ url_for('laporan.mahasiswa_aktif') }}"><svg class="nav-icon"><use href="#i-users"></use></svg>Mahasiswa Aktif</a>
            <a href="{{ url_for('laporan.buku_tidak_populer') }}"><svg class="nav-icon"><use href="#i-trend-down"></use></svg>Buku Tidak Populer</a>
          </div>
        </div>

        <div class="sidebar-nav-label">Administrasi</div>
        <a class="side-link" href="{{ url_for('kartu.kelola_kartu') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-id-card"></use></svg>Kelola Kartu</span>
        </a>
        <a class="side-link" href="{{ url_for('auth.daftar_pengguna') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-users"></use></svg>Pengguna</span>
        </a>
        <a class="side-link" href="{{ url_for('pengaturan.halaman') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-settings"></use></svg>Pengaturan</span>
        </a>
        <a class="side-link" href="{{ url_for('auth.daftar_persetujuan') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-user-check"></use></svg>Persetujuan</span>
          {% if jumlah_pending_akun %}<span class="badge badge-danger">{{ jumlah_pending_akun }}</span>{% endif %}
        </a>

        <div class="sidebar-nav-label">Akun Saya</div>
        <a class="side-link" href="{{ url_for('kartu.kartu_saya') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-id-card"></use></svg>Kartu Saya</span>
        </a>
        <a class="side-link" href="{{ url_for('auth.profil') }}">
          <span class="side-link-main"><svg class="nav-icon"><use href="#i-user"></use></svg>Profil Saya</span>
        </a>
      </nav>
    </aside>
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleMenuMobile()"></div>
  {% endif %}

  <div class="app-main">
    <nav class="navbar {{ 'navbar-compact' if pakai_sidebar else '' }}">
      <div class="navbar-left">
        <button class="hamburger" id="btnHamburger" aria-label="Buka menu" onclick="toggleMenuMobile()"><svg class="nav-icon"><use href="#i-menu"></use></svg></button>
        <a href="{{ url_for('dashboard.index') if current_user.is_authenticated else url_for('auth.login') }}" class="brand">
          <img src="{{ url_for('static', filename='img/logo_stikom.png') }}" alt="Logo STIKOM Kendari">
          <span>Perpustakaan STIKOM Kendari</span>
        </a>
      </div>

      {% if not pakai_sidebar %}
      <div class="navbar-links" id="navLinks">
        {% if current_user.is_authenticated %}
          <a class="nav-link" href="{{ url_for('dashboard.index') }}"><svg class="nav-icon"><use href="#i-home"></use></svg>Dashboard</a>

          {% if current_user.is_mahasiswa %}
            <a class="nav-link" href="{{ url_for('buku.daftar_buku') }}"><svg class="nav-icon"><use href="#i-book"></use></svg>Koleksi Buku</a>
            <a class="nav-link" href="{{ url_for('kartu.kartu_saya') }}"><svg class="nav-icon"><use href="#i-id-card"></use></svg>Kartu Perpustakaan</a>
            <a class="nav-link" href="{{ url_for('peminjaman.riwayat_saya') }}"><svg class="nav-icon"><use href="#i-clock"></use></svg>Riwayat Saya</a>
          {% endif %}

          {% if current_user.is_staf %}
            <div class="nav-dropdown">
              <button type="button" class="nav-link nav-dropdown-toggle">
                <svg class="nav-icon"><use href="#i-book"></use></svg>Koleksi Buku <svg class="nav-caret"><use href="#i-chevron-down"></use></svg>
              </button>
              <div class="nav-dropdown-menu">
                <a href="{{ url_for('buku.daftar_buku') }}"><svg class="nav-icon"><use href="#i-book"></use></svg>Daftar Buku</a>
                <a href="{{ url_for('buku.kategori') }}"><svg class="nav-icon"><use href="#i-folder"></use></svg>Kategori</a>
                <a href="{{ url_for('buku.import_excel') }}"><svg class="nav-icon"><use href="#i-upload"></use></svg>Import Excel</a>
                <a href="{{ url_for('buku.ekspor_buku') }}"><svg class="nav-icon"><use href="#i-download"></use></svg>Ekspor Excel</a>
              </div>
            </div>
            <a class="nav-link" href="{{ url_for('peminjaman.daftar_peminjaman') }}"><svg class="nav-icon"><use href="#i-book-open"></use></svg>Peminjaman</a>
            <a class="nav-link" href="{{ url_for('peminjaman.daftar_pengajuan') }}">
              <svg class="nav-icon"><use href="#i-clipboard"></use></svg>Pengajuan
              {% if jumlah_pengajuan_peminjaman %}<span class="badge badge-danger" style="margin-left:0.3rem;">{{ jumlah_pengajuan_peminjaman }}</span>{% endif %}
            </a>
            <a class="nav-link" href="{{ url_for('denda.daftar_denda') }}"><svg class="nav-icon"><use href="#i-coins"></use></svg>Denda</a>
            <div class="nav-dropdown">
              <button type="button" class="nav-link nav-dropdown-toggle">
                <svg class="nav-icon"><use href="#i-bar-chart"></use></svg>Laporan <svg class="nav-caret"><use href="#i-chevron-down"></use></svg>
              </button>
              <div class="nav-dropdown-menu">
                <a href="{{ url_for('laporan.buku_terlambat') }}"><svg class="nav-icon"><use href="#i-alert"></use></svg>Buku Terlambat</a>
                <a href="{{ url_for('laporan.buku_populer') }}"><svg class="nav-icon"><use href="#i-flame"></use></svg>Buku Populer</a>
                <a href="{{ url_for('laporan.mahasiswa_aktif') }}"><svg class="nav-icon"><use href="#i-users"></use></svg>Mahasiswa Aktif</a>
                <a href="{{ url_for('laporan.buku_tidak_populer') }}"><svg class="nav-icon"><use href="#i-trend-down"></use></svg>Buku Tidak Populer</a>
              </div>
            </div>
            <a class="nav-link" href="{{ url_for('kartu.kelola_kartu') }}"><svg class="nav-icon"><use href="#i-id-card"></use></svg>Kelola Kartu</a>
            <a class="nav-link" href="{{ url_for('kartu.kartu_saya') }}"><svg class="nav-icon"><use href="#i-id-card"></use></svg>Kartu Saya</a>
            <a class="nav-link" href="{{ url_for('auth.profil') }}"><svg class="nav-icon"><use href="#i-user"></use></svg>Profil Saya</a>
          {% endif %}
        {% endif %}
      </div>
      {% endif %}

      <div class="navbar-right">
        {% if current_user.is_authenticated %}
          {# Avatar bundar berisi inisial nama (tanpa foto profil) #}
          {% set _bagian = (current_user.nama_lengkap or '').split() %}
          {% set inisial = ((_bagian[0][:1] ~ (_bagian[-1][:1] if _bagian|length > 1 else '')) if _bagian else '?')|upper %}
          {% if current_user.is_mahasiswa %}<div class="user-card">{% else %}<a href="{{ url_for('auth.profil') }}" class="user-card user-card-link" title="Profil Saya">{% endif %}
            <span class="user-avatar avatar-{{ current_user.role }}" aria-hidden="true">{{ inisial }}</span>
            <span class="user-meta">
              <span class="user-name">{{ current_user.nama_lengkap }}</span>
              <span class="user-role">{{ current_user.role_label }}</span>
            </span>
          {% if current_user.is_mahasiswa %}</div>{% else %}</a>{% endif %}
          <a href="{{ url_for('auth.logout') }}" class="btn-logout" title="Logout" aria-label="Logout"><svg class="nav-icon"><use href="#i-log-out"></use></svg><span>Logout</span></a>
        {% else %}
          <a href="{{ url_for('auth.login') }}" class="btn btn-sm btn-accent js-nav-loader">Login</a>
          <a href="{{ url_for('auth.register') }}" class="js-nav-loader" style="color:#f4e9d8; font-size:0.85rem;">Daftar</a>
        {% endif %}
        <button class="theme-toggle" id="btnTema" onclick="toggleTema()" aria-label="Ganti mode gelap/terang" title="Ganti mode gelap/terang">
          <svg class="nav-icon" id="iconTemaGelap"><use href="#i-moon"></use></svg>
          <svg class="nav-icon" id="iconTemaTerang" style="display:none;"><use href="#i-sun"></use></svg>
        </button>
      </div>
    </nav>

    <div class="container">
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          {% for category, message in messages %}
            <div class="flash flash-{{ category }}">{{ message }}</div>
          {% endfor %}
        {% endif %}
      {% endwith %}

      {% block content %}{% endblock %}
    </div>

    <div class="footer">
      &copy; {{ tahun_sekarang }} Perpustakaan STIKOM Kendari — dijalankan secara lokal.
    </div>
  </div>

  {# ================= BOTTOM NAV (khusus HP, lihat mobile.css) ================= #}
  {% if current_user.is_authenticated %}
  <div class="sidebar-overlay" id="navOverlay" onclick="toggleMenuMobile()"></div>
  <nav class="bottom-nav" aria-label="Menu utama">
    <a href="{{ url_for('dashboard.index') }}"><svg class="nav-icon"><use href="#i-home"></use></svg><span>Beranda</span></a>
    {% if current_user.is_mahasiswa %}
      <a href="{{ url_for('buku.daftar_buku') }}"><svg class="nav-icon"><use href="#i-book"></use></svg><span>Buku</span></a>
      <a href="{{ url_for('kartu.kartu_saya') }}"><svg class="nav-icon"><use href="#i-id-card"></use></svg><span>Kartu</span></a>
      <a href="{{ url_for('peminjaman.riwayat_saya') }}"><svg class="nav-icon"><use href="#i-clock"></use></svg><span>Riwayat</span></a>
    {% else %}
      <a href="{{ url_for('buku.daftar_buku') }}"><svg class="nav-icon"><use href="#i-book"></use></svg><span>Buku</span></a>
      <a href="{{ url_for('peminjaman.daftar_peminjaman') }}"><svg class="nav-icon"><use href="#i-book-open"></use></svg><span>Pinjam</span></a>
      <a href="{{ url_for('peminjaman.daftar_pengajuan') }}"><svg class="nav-icon"><use href="#i-clipboard"></use></svg><span>Pengajuan</span>{% if jumlah_pengajuan_peminjaman %}<span class="bn-badge">{{ jumlah_pengajuan_peminjaman }}</span>{% endif %}</a>
      <button type="button" onclick="toggleMenuMobile()" aria-label="Buka menu lengkap"><svg class="nav-icon"><use href="#i-menu"></use></svg><span>Menu</span></button>
    {% endif %}
  </nav>
  {% endif %}

  <script>
    /* ---------------- TABEL -> KARTU DI HP ----------------
       Beri label kolom pada tiap sel supaya mobile.css bisa menampilkan
       "LABEL: isi" per baris. Di desktop tabel tetap tampil normal. */
    (function () {
      document.querySelectorAll('.table-scroll table:not(.tabel-excel)').forEach(function (tabel) {
        var judul = Array.prototype.map.call(tabel.querySelectorAll('thead th'), function (th) { return th.textContent.trim(); });
        if (!judul.length) return;
        tabel.classList.add('tbl-stack');
        tabel.querySelectorAll('tbody tr').forEach(function (tr) {
          Array.prototype.forEach.call(tr.children, function (td, i) {
            if (td.colSpan > 1) { td.classList.add('tbl-empty'); return; }
            if (judul[i]) td.setAttribute('data-label', judul[i]);
            var bungkus = document.createElement('span');
            bungkus.className = 'cell-v';
            while (td.firstChild) bungkus.appendChild(td.firstChild);
            td.appendChild(bungkus);
          });
        });
      });
    })();
  </script>

  <script>
    /* ---------------- TOMBOL LIHAT PASSWORD ----------------
       Semua <input type="password" data-toggle-pw> otomatis diberi ikon mata. */
    (function () {
      document.querySelectorAll('input[data-toggle-pw]').forEach(function (input) {
        var wrap = document.createElement('span');
        wrap.className = 'pw-field';
        input.parentNode.insertBefore(wrap, input);
        wrap.appendChild(input);

        var tombol = document.createElement('button');
        tombol.type = 'button';
        tombol.className = 'pw-toggle';
        tombol.setAttribute('aria-label', 'Tampilkan password');
        tombol.setAttribute('title', 'Tampilkan password');
        tombol.innerHTML = '<svg class="icon"><use href="#i-eye"></use></svg>';
        wrap.appendChild(tombol);

        tombol.addEventListener('click', function () {
          var tampil = input.type === 'password';
          input.type = tampil ? 'text' : 'password';
          tombol.querySelector('use').setAttribute('href', tampil ? '#i-eye-off' : '#i-eye');
          var label = tampil ? 'Sembunyikan password' : 'Tampilkan password';
          tombol.setAttribute('aria-label', label);
          tombol.setAttribute('title', label);
          input.focus();
        });
      });
    })();

    /* ---------------- LOADER TRANSISI ANTAR HALAMAN ---------------- */
    (function () {
      var loader = document.getElementById('pageLoader');
      if (!loader) return;

      var teksLoader = loader.querySelector('.page-loader-text');
      var PATH_BUKU = "{{ url_for('buku.daftar_buku') }}".replace(/\/+$/, '');

      function sembunyikanLoader() { loader.classList.add('page-loader-hidden'); }
      function tampilkanLoader(teks) {
        if (teksLoader) teksLoader.textContent = teks || 'Memuat...';
        loader.classList.remove('page-loader-hidden');
      }

      // Sembunyikan loader begitu halaman ini selesai dimuat (termasuk saat
      // dibuka dari cache back/forward browser, via event 'pageshow').
      window.addEventListener('load', sembunyikanLoader);
      window.addEventListener('pageshow', sembunyikanLoader);
      if (document.readyState === 'complete') sembunyikanLoader();
      // Cadangan: loader awal jangan menutupi halaman terlalu lama bila ada
      // gambar/font yang lambat dimuat.
      setTimeout(sembunyikanLoader, 8000);

      function klikBiasa(e) {
        return !(e.defaultPrevented || e.button !== 0 ||
                 e.metaKey || e.ctrlKey || e.shiftKey || e.altKey);
      }

      // Link bertanda class "js-nav-loader" (mis. ke halaman registrasi/login).
      document.querySelectorAll('a.js-nav-loader').forEach(function (a) {
        a.addEventListener('click', function (e) {
          if (!klikBiasa(e)) return;
          if (a.target && a.target !== '' && a.target !== '_self') return;
          tampilkanLoader();
        });
      });

      // Semua link ke halaman daftar buku (menu, bottom-nav, dashboard,
      // filter kategori, paginasi) - query buku bisa lama, jadi beri tahu
      // pengguna bahwa halaman sedang dimuat. Link unduhan (ekspor dsb.)
      // tidak ikut karena path-nya berbeda.
      document.addEventListener('click', function (e) {
        if (!klikBiasa(e)) return;
        var a = e.target.closest ? e.target.closest('a[href]') : null;
        if (!a || (a.target && a.target !== '_self')) return;
        if (a.origin !== location.origin) return;
        if (a.pathname.replace(/\/+$/, '') !== PATH_BUKU) return;
        tampilkanLoader('Memuat data buku...');
      });

      // Form bertanda data-loader="teks" (login, registrasi, pencarian buku).
      document.addEventListener('submit', function (e) {
        var form = e.target;
        if (!form || !form.hasAttribute || !form.hasAttribute('data-loader')) return;
        // tunggu handler lain (mis. confirm) selesai; kalau dibatalkan, jangan tampilkan
        setTimeout(function () {
          if (!e.defaultPrevented) tampilkanLoader(form.getAttribute('data-loader'));
        }, 0);
      });
    })();

    function toggleTema() {
      var root = document.documentElement;
      var temaSekarang = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', temaSekarang);
      localStorage.setItem('tema', temaSekarang);
      perbaruiIkonTema();

      var tombolTema = document.getElementById('btnTema');
      if (tombolTema) {
        tombolTema.classList.remove('spin-once');
        void tombolTema.offsetWidth; // reset agar animasi bisa diputar ulang
        tombolTema.classList.add('spin-once');
      }
    }

    function perbaruiIkonTema() {
      var tema = document.documentElement.getAttribute('data-theme');
      var iconGelap = document.getElementById('iconTemaGelap');
      var iconTerang = document.getElementById('iconTemaTerang');
      if (!iconGelap || !iconTerang) return;
      iconGelap.style.display = tema === 'dark' ? 'none' : '';
      iconTerang.style.display = tema === 'dark' ? '' : 'none';
    }

    // ---- Menu mobile: buka/tutup sidebar (operator) ATAU navLinks (role lain) ----
    function toggleMenuMobile() {
      var sidebar = document.getElementById('sidebarOperator');
      if (sidebar) {
        sidebar.classList.toggle('open');
        var overlay = document.getElementById('sidebarOverlay');
        if (overlay) overlay.classList.toggle('open');
      } else {
        var navLinks = document.getElementById('navLinks');
        if (navLinks) navLinks.classList.toggle('open');
        var navOverlay = document.getElementById('navOverlay');
        if (navOverlay) navOverlay.classList.toggle('open', navLinks && navLinks.classList.contains('open'));
      }
    }

    document.addEventListener('DOMContentLoaded', function () {
      perbaruiIkonTema();

      var path = window.location.pathname;

      // tandai link menu yang sedang aktif di navbar atas (termasuk dropdown)
      document.querySelectorAll('.navbar-links a').forEach(function (a) {
        if (a.getAttribute('href') === path) {
          a.classList.add('active');
          var dropdownParent = a.closest('.nav-dropdown');
          if (dropdownParent) {
            dropdownParent.querySelector('.nav-dropdown-toggle').classList.add('active');
          }
        }
      });

      // tandai tab aktif di bottom nav (HP)
      document.querySelectorAll('.bottom-nav a').forEach(function (a) {
        if (a.getAttribute('href') === path) a.classList.add('active');
      });

      // tandai link menu yang sedang aktif di sidebar (operator), termasuk submenu
      document.querySelectorAll('.sidebar-nav a').forEach(function (a) {
        if (a.getAttribute('href') === path) {
          a.classList.add('active');
          var groupParent = a.closest('.side-group');
          if (groupParent) {
            groupParent.classList.add('open');
            groupParent.querySelector('.side-group-toggle').classList.add('active');
          }
        }
      });

      // tutup menu mobile otomatis saat memilih salah satu link
      document.querySelectorAll('.navbar-links a, .sidebar-nav a').forEach(function (a) {
        a.addEventListener('click', function () {
          var navLinks = document.getElementById('navLinks');
          if (navLinks) navLinks.classList.remove('open');
          var navOv = document.getElementById('navOverlay');
          if (navOv) navOv.classList.remove('open');
          var sidebar = document.getElementById('sidebarOperator');
          if (sidebar && window.innerWidth <= 900) {
            sidebar.classList.remove('open');
            var overlay = document.getElementById('sidebarOverlay');
            if (overlay) overlay.classList.remove('open');
          }
          document.querySelectorAll('.nav-dropdown.open').forEach(function (d) { d.classList.remove('open'); });
        });
      });

      // buka/tutup dropdown navbar atas (Koleksi Buku / Laporan, untuk staf)
      document.querySelectorAll('.nav-dropdown-toggle').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          var dropdown = btn.closest('.nav-dropdown');
          var sudahTerbuka = dropdown.classList.contains('open');
          document.querySelectorAll('.nav-dropdown.open').forEach(function (d) { d.classList.remove('open'); });
          if (!sudahTerbuka) dropdown.classList.add('open');
        });
      });
      document.addEventListener('click', function (e) {
        if (!e.target.closest('.nav-dropdown')) {
          document.querySelectorAll('.nav-dropdown.open').forEach(function (d) { d.classList.remove('open'); });
        }
      });

      // buka/tutup submenu sidebar (Koleksi Buku / Laporan, untuk operator)
      document.querySelectorAll('.side-group-toggle').forEach(function (btn) {
        btn.addEventListener('click', function () {
          btn.closest('.side-group').classList.toggle('open');
        });
      });

      // notifikasi flash otomatis hilang setelah beberapa detik
      document.querySelectorAll('.flash:not(.no-auto-hide)').forEach(function (el) {
        setTimeout(function () {
          el.style.transition = 'opacity 0.4s ease';
          el.style.opacity = '0';
          setTimeout(function () { el.remove(); }, 400);
        }, 4000);
      });
    });
  </script>
  {% block scripts %}{% endblock %}
</body>
</html>
```


## `Website/templates/layout/icons.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{# =========================================================
   SPRITE IKON (SVG, garis tipis - menggantikan emoji)
   Dipakai lewat: <svg class="icon"><use href="#i-nama"></use></svg>
   ========================================================= #}
<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
  <defs>
    <symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9a1 1 0 0 0 1 1H10v-6h4v6h3.5a1 1 0 0 0 1-1v-9"/></symbol>
    <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/></symbol>
    <symbol id="i-book-open" viewBox="0 0 24 24"><path d="M12 5.5C10.4 4 8 3.3 4 3.5v14c4 -.2 6.4.5 8 2 1.6-1.5 4-2.2 8-2v-14c-4-.2-6.4.5-8 2Z"/><path d="M12 5.5v14"/></symbol>
    <symbol id="i-folder" viewBox="0 0 24 24"><path d="M3.5 6.5A1.5 1.5 0 0 1 5 5h4l2 2h8a1.5 1.5 0 0 1 1.5 1.5v9A1.5 1.5 0 0 1 19 19H5a1.5 1.5 0 0 1-1.5-1.5v-11Z"/></symbol>
    <symbol id="i-upload" viewBox="0 0 24 24"><path d="M12 15V4"/><path d="m7.5 8.5 4.5-4.5 4.5 4.5"/><path d="M4.5 15v3.5A1.5 1.5 0 0 0 6 20h12a1.5 1.5 0 0 0 1.5-1.5V15"/></symbol>
    <symbol id="i-clipboard" viewBox="0 0 24 24"><rect x="5" y="4.5" width="14" height="17" rx="1.5"/><rect x="8.5" y="2.5" width="7" height="3.5" rx="1"/><path d="M8.5 11h7M8.5 15h7M8.5 19h4"/></symbol>
    <symbol id="i-bar-chart" viewBox="0 0 24 24"><path d="M4 20V10M12 20V4M20 20v-7"/><path d="M2.5 20h19"/></symbol>
    <symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M2.8 19c.7-3.2 3.2-5 6.2-5s5.5 1.8 6.2 5"/><path d="M15.5 5.3c1.5.4 2.6 1.8 2.6 3.4 0 1.6-1.1 3-2.6 3.4"/><path d="M17 14.3c2.4.5 4.1 2.1 4.7 4.7"/></symbol>
    <symbol id="i-user-check" viewBox="0 0 24 24"><circle cx="9.5" cy="8" r="3.5"/><path d="M2.8 19.5c.7-3.4 3.3-5.3 6.7-5.3s6 1.9 6.7 5.3"/><path d="m15.5 11.5 2 2 3.5-3.8"/></symbol>
    <symbol id="i-id-card" viewBox="0 0 24 24"><rect x="2.5" y="5" width="19" height="14" rx="1.8"/><circle cx="8" cy="12" r="2.1"/><path d="M5 16.3c.6-1.4 1.6-2.1 3-2.1s2.4.7 3 2.1"/><path d="M14 9.5h4.5M14 13h4.5"/></symbol>
    <symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.6"/><path d="M4.5 20c.9-3.8 3.6-5.8 7.5-5.8s6.6 2 7.5 5.8"/></symbol>
    <symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.3M12 19.2v2.3M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M2.5 12h2.3M19.2 12h2.3M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></symbol>
    <symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14.2A8.5 8.5 0 1 1 9.8 4a6.8 6.8 0 0 0 10.2 10.2Z"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17"/></symbol>
    <symbol id="i-search" viewBox="0 0 24 24"><circle cx="10.8" cy="10.8" r="6.3"/><path d="m20 20-4.3-4.3"/></symbol>
    <symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 4.5v15M4.5 12h15"/></symbol>
    <symbol id="i-edit" viewBox="0 0 24 24"><path d="M4 20h4L18.5 9.5a2.4 2.4 0 0 0-4-4L4 16v4Z"/><path d="m13.5 6.5 4 4"/></symbol>
    <symbol id="i-trash" viewBox="0 0 24 24"><path d="M4.5 7h15M9.5 7V4.8A1.3 1.3 0 0 1 10.8 3.5h2.4A1.3 1.3 0 0 1 14.5 4.8V7"/><path d="M6.5 7 7.3 19.2A1.5 1.5 0 0 0 8.8 20.5h6.4a1.5 1.5 0 0 0 1.5-1.3L17.5 7"/><path d="M10.3 11v6M13.7 11v6"/></symbol>
    <symbol id="i-download" viewBox="0 0 24 24"><path d="M12 3.5v11"/><path d="m7.5 10.5 4.5 4.5 4.5-4.5"/><path d="M4.5 17v2A1.5 1.5 0 0 0 6 20.5h12A1.5 1.5 0 0 0 19.5 19v-2"/></symbol>
    <symbol id="i-eye" viewBox="0 0 24 24"><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3"/></symbol>
    <symbol id="i-eye-off" viewBox="0 0 24 24"><path d="M3.5 3.5l17 17"/><path d="M10.6 5.7A10.6 10.6 0 0 1 12 5.5c6 0 9.5 6.5 9.5 6.5a15.7 15.7 0 0 1-3.3 4.1M7.3 7.3C4.8 8.9 2.5 12 2.5 12s3.5 6.5 9.5 6.5c1.1 0 2.1-.2 3-.5"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><path d="m4.5 12.5 5 5 10-11"/></symbol>
    <symbol id="i-check-circle" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m8 12.3 2.7 2.7L16.3 9"/></symbol>
    <symbol id="i-x" viewBox="0 0 24 24"><path d="M5.5 5.5l13 13M18.5 5.5l-13 13"/></symbol>
    <symbol id="i-x-circle" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/></symbol>
    <symbol id="i-bell" viewBox="0 0 24 24"><path d="M6 10.5a6 6 0 0 1 12 0c0 4 1.5 5.5 1.5 5.5h-15S6 14.5 6 10.5Z"/><path d="M10 19a2.2 2.2 0 0 0 4 0"/></symbol>
    <symbol id="i-alert" viewBox="0 0 24 24"><path d="M12 3.5 22 20.5H2Z"/><path d="M12 10v4.2"/><circle cx="12" cy="17.3" r=".3" fill="currentColor" stroke="none"/></symbol>
    <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.3l3.5 2"/></symbol>
    <symbol id="i-arrow-left" viewBox="0 0 24 24"><path d="M19 12H5M10.5 6 5 12l5.5 6"/></symbol>
    <symbol id="i-inbox" viewBox="0 0 24 24"><path d="M4 12.5h4.3l1.4 2.5h4.6l1.4-2.5H20"/><path d="m4 12.5 1.8-7A1.5 1.5 0 0 1 7.2 4.5h9.6a1.5 1.5 0 0 1 1.4 1l1.8 7V18a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 18v-5.5Z"/></symbol>
    <symbol id="i-image" viewBox="0 0 24 24"><rect x="3" y="4.5" width="18" height="15" rx="1.8"/><circle cx="8.3" cy="9.3" r="1.8"/><path d="m4 18 5.5-5.5a1.7 1.7 0 0 1 2.4 0L14 14.6l2-2a1.7 1.7 0 0 1 2.4 0L21 15.2"/></symbol>
    <symbol id="i-crop" viewBox="0 0 24 24"><path d="M6 2v14a1.5 1.5 0 0 0 1.5 1.5H22"/><path d="M18 22V8A1.5 1.5 0 0 0 16.5 6.5H2"/></symbol>
    <symbol id="i-printer" viewBox="0 0 24 24"><path d="M7 8.5V3.5h10v5"/><rect x="4" y="8.5" width="16" height="8" rx="1.5"/><rect x="7" y="14" width="10" height="7" rx="1"/></symbol>
    <symbol id="i-flame" viewBox="0 0 24 24"><path d="M12 2.5s5 4.5 5 9.7A5 5 0 0 1 7 12.2c0-1 .3-1.8.8-2.6.4 1 1.2 1.6 2 1.6-.6-3.4 1-5.5 2.2-8.7Z"/></symbol>
    <symbol id="i-trend-down" viewBox="0 0 24 24"><path d="M3.5 7 10 13.5l3.5-3.5 7 7"/><path d="M15.5 17h5v-5"/></symbol>
    <symbol id="i-trend-up" viewBox="0 0 24 24"><path d="M3.5 17 10 10.5l3.5 3.5 7-7"/><path d="M15.5 7h5v5"/></symbol>
    <symbol id="i-log-out" viewBox="0 0 24 24"><path d="M9 20H5.5A1.5 1.5 0 0 1 4 18.5v-13A1.5 1.5 0 0 1 5.5 4H9"/><path d="M16 16.5 21 12l-5-4.5"/><path d="M21 12H9"/></symbol>
    <symbol id="i-scissors" viewBox="0 0 24 24"><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="6.5" cy="17.5" r="2.5"/><path d="m20 5-13 14M9 12l11 7"/></symbol>
    <symbol id="i-pen" viewBox="0 0 24 24"><path d="M4 19.5c3-.3 4.6-1 5.8-2.2L18.3 8.8a2 2 0 0 0-2.8-2.8L7 14.5c-1.2 1.2-1.9 2.8-2.2 5Z"/></symbol>
    <symbol id="i-chevron-down" viewBox="0 0 24 24"><path d="m5.5 8.5 6.5 7 6.5-7"/></symbol>
    <symbol id="i-wave" viewBox="0 0 24 24"><path d="M4 14.5c1-3 2.8-5.5 5.3-6.8a3.6 3.6 0 0 1 5.2 1.9M4 14.5s2 1.5 2.3 2.7c.3 1.2-.6 2.3-1.8 2.1M14.5 9.6l2.7-1.6a1.8 1.8 0 0 1 2.5 2.4l-4.2 6.4a5.5 5.5 0 0 1-6.6 1.9l-3.6-1.4"/></symbol>
    <symbol id="i-coins" viewBox="0 0 24 24"><ellipse cx="9" cy="7" rx="5.5" ry="2.8"/><path d="M3.5 7v4c0 1.5 2.5 2.8 5.5 2.8s5.5-1.3 5.5-2.8V7"/><path d="M3.5 11v4c0 1.5 2.5 2.8 5.5 2.8 1 0 2-.1 2.8-.4"/><path d="M14.5 10.2c3.2.2 6 1.3 6 2.8v4c0 1.5-2.5 2.8-5.5 2.8s-5.5-1.3-5.5-2.8v-1"/></symbol>
    <symbol id="i-settings" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7"/></symbol>
  </defs>
</svg>
```


## `Website/templates/peminjaman/daftar.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Daftar Peminjaman{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-book-open"></use></svg> Daftar Peminjaman</h2>
  <p class="page-sub">Kelola peminjaman aktif dan riwayat pengembalian buku.</p>
</div>

<div class="search-bar">
  <a href="{{ url_for('peminjaman.daftar_pengajuan') }}" class="btn btn-sm btn-accent">
    <svg class="icon"><use href="#i-clipboard"></use></svg> Pengajuan Peminjaman
    {% if jumlah_pengajuan_peminjaman %}<span class="badge badge-danger" style="margin-left:0.3rem;">{{ jumlah_pengajuan_peminjaman }}</span>{% endif %}
  </a>
  <a href="{{ url_for('peminjaman.daftar_peminjaman', status='dipinjam', q=q) }}"
     class="chip{{ ' chip-active' if status_filter=='dipinjam' else '' }}">Sedang Dipinjam</a>
  <a href="{{ url_for('peminjaman.daftar_peminjaman', status='dikembalikan', q=q) }}"
     class="chip{{ ' chip-active' if status_filter=='dikembalikan' else '' }}">Sudah Dikembalikan</a>
  <a href="{{ url_for('peminjaman.daftar_peminjaman', status='ditolak', q=q) }}"
     class="chip{{ ' chip-active' if status_filter=='ditolak' else '' }}">Ditolak</a>
  <a href="{{ url_for('peminjaman.daftar_peminjaman', status='semua', q=q) }}"
     class="chip{{ ' chip-active' if status_filter=='semua' else '' }}">Semua</a>
</div>

<form method="GET" class="search-bar">
  <input type="hidden" name="status" value="{{ status_filter }}">
  <input type="text" name="q" placeholder="Cari nama/username/NIM mahasiswa atau judul buku..." value="{{ q }}">
  <button class="btn" type="submit">Cari</button>
  {% if q %}<a href="{{ url_for('peminjaman.daftar_peminjaman', status=status_filter) }}" class="btn btn-ghost">Reset</a>{% endif %}
</form>

<div class="card">
  <div class="table-scroll">
  <table>
    <thead>
      <tr><th>Mahasiswa</th><th>Buku</th><th>Tgl Pinjam</th><th>Jatuh Tempo</th><th>Tgl Kembali</th><th>Status</th><th>Denda</th><th>Aksi</th></tr>
    </thead>
    <tbody>
      {% for p in daftar %}
      <tr>
        <td>{{ p.anggota.nama_lengkap }}</td>
        <td>{{ p.buku.judul }}</td>
        <td>{{ p.tanggal_pinjam.strftime('%d-%m-%Y') }}</td>
        <td>{{ p.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}{% if p.jumlah_perpanjang %}<br><small style="color:var(--muted);">diperpanjang {{ p.jumlah_perpanjang }}x</small>{% endif %}</td>
        <td>{{ p.tanggal_kembali.strftime('%d-%m-%Y') if p.tanggal_kembali else '-' }}</td>
        <td>
          {% if p.status == 'dikembalikan' %}
            <span class="badge badge-success">Dikembalikan</span>
          {% elif p.status == 'diajukan' %}
            <span class="badge badge-warning">Menunggu Persetujuan</span>
          {% elif p.status == 'ditolak' %}
            <span class="badge badge-danger">Ditolak</span>
          {% elif p.is_telat %}
            <span class="badge badge-danger">Terlambat {{ p.hari_telat }} hari</span>
          {% elif p.hari_menuju_jatuh_tempo is not none and p.hari_menuju_jatuh_tempo <= config.PERINGATAN_JATUH_TEMPO_HARI %}
            <span class="badge badge-warning">⏰ Segera Tempo ({{ p.hari_menuju_jatuh_tempo }}h)</span>
          {% else %}
            <span class="badge badge-info">Dipinjam</span>
          {% endif %}
        </td>
        <td>
          {% set d = denda_sekarang(p) %}
          {% if d > 0 %}
            <strong>{{ d|rupiah }}</strong>
            {% if p.status == 'dipinjam' %}<br><small style="color:var(--muted);">berjalan</small>
            {% elif p.status_denda == 'belum_lunas' %}<br><span class="badge badge-danger">Belum lunas</span>
            {% elif p.status_denda == 'lunas' %}<br><span class="badge badge-success">Lunas</span>
            {% elif p.status_denda == 'dibebaskan' %}<br><span class="badge badge-info">Dibebaskan</span>{% endif %}
          {% else %}-{% endif %}
        </td>
        <td>
          {% if p.status == 'dipinjam' %}
          <div class="aksi-baris">
          <form method="POST" action="{{ url_for('peminjaman.kembalikan_buku', peminjaman_id=p.id) }}"
                onsubmit="return confirm('Konfirmasi pengembalian buku ini?');">
            <button class="btn btn-sm btn-success" type="submit"><svg class="icon"><use href="#i-check"></use></svg> Kembalikan</button>
            {% if denda_sekarang(p) > 0 %}<button class="btn btn-sm btn-accent" type="submit" name="bayar" value="1">Kembalikan &amp; Lunasi</button>{% endif %}
          </form>
          {% if p.hari_telat == 0 and p.jumlah_perpanjang < config.MAKS_PERPANJANG %}
          <form method="POST" action="{{ url_for('peminjaman.perpanjang', peminjaman_id=p.id) }}"
                onsubmit="return confirm('Perpanjang jatuh tempo buku ini?');">
            <button class="btn btn-sm" type="submit"><svg class="icon"><use href="#i-clock"></use></svg> Perpanjang</button>
          </form>
          {% endif %}
          {% if current_user.is_kepala %}
          <details class="aksi-atur">
            <summary class="btn btn-sm"><svg class="icon"><use href="#i-pen"></use></svg> Atur Tempo</summary>
            <form method="POST" action="{{ url_for('peminjaman.atur_jatuh_tempo', peminjaman_id=p.id) }}">
              <input type="date" name="tanggal" value="{{ p.tanggal_jatuh_tempo.isoformat() }}" min="{{ p.tanggal_pinjam.isoformat() }}" required>
              <button class="btn btn-sm btn-accent" type="submit">Simpan</button>
            </form>
          </details>
          {% endif %}
          </div>
          {% elif p.status == 'diajukan' %}
            <a href="{{ url_for('peminjaman.daftar_pengajuan') }}" class="btn btn-sm btn-accent">Tinjau</a>
          {% endif %}
        </td>
      </tr>
      {% else %}
      <tr><td colspan="8">Tidak ada data.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
</div>
{% endblock %}
```


## `Website/templates/peminjaman/pengajuan.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Pengajuan Peminjaman{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-clipboard"></use></svg> Pengajuan Peminjaman</h2>
  <p class="page-sub">Tinjau permintaan peminjaman yang diajukan mandiri oleh mahasiswa, lalu setujui atau tolak.</p>
</div>

{% if not daftar %}
  <div class="card empty-state">
    <svg class="icon" style="width:2.2rem;height:2.2rem;"><use href="#i-inbox"></use></svg>
    <p>Tidak ada pengajuan peminjaman yang menunggu saat ini.</p>
  </div>
{% else %}
  <div class="pengajuan-grid">
    {% for p in daftar %}
      <div class="card pengajuan-card">
        <div class="pengajuan-card-head">
          <span class="badge badge-warning">Menunggu Persetujuan</span>
          <span class="pengajuan-tanggal">Diajukan sejak {{ p.tanggal_pinjam.strftime('%d-%m-%Y') }}</span>
        </div>
        <h3 class="pengajuan-judul">{{ p.buku.judul }}</h3>
        <p class="pengajuan-meta">{{ p.buku.penulis }} &nbsp;·&nbsp; Stok saat ini: {{ p.buku.stok }}</p>
        <p class="pengajuan-meta"><strong>Pemohon:</strong> {{ p.anggota.nama_lengkap }} ({{ p.anggota.username }})</p>

        <div class="pengajuan-actions">
          <form method="POST" action="{{ url_for('peminjaman.setujui_pengajuan', peminjaman_id=p.id) }}"
                onsubmit="return confirm('Setujui pengajuan ini? Stok buku akan berkurang 1.');">
            <label class="lama-hari" title="Jatuh tempo = hari ini + lama pinjam">
              <span>Pinjam</span>
              <input type="number" name="lama_hari" min="1" max="365" value="{{ lama_pinjam_untuk(p.buku) }}" inputmode="numeric">
              <span>hari</span>
            </label>
            <button class="btn btn-sm btn-success" type="submit"><svg class="icon"><use href="#i-check"></use></svg> Setujui</button>
          </form>
          <button type="button" class="btn btn-sm btn-danger" onclick="bukaTolak({{ p.id }})"><svg class="icon"><use href="#i-x"></use></svg> Tolak</button>
          <a href="{{ url_for('buku.detail_buku', buku_id=p.buku.id) }}" class="btn btn-sm btn-muted">Lihat Buku</a>
        </div>

        <form id="formTolak{{ p.id }}" method="POST" action="{{ url_for('peminjaman.tolak_pengajuan', peminjaman_id=p.id) }}"
              class="pengajuan-form-tolak" style="display:none;">
          <textarea name="catatan" rows="2" placeholder="Alasan penolakan (opsional)..."></textarea>
          <div class="pengajuan-actions" style="margin-top:0.5rem;">
            <button class="btn btn-sm btn-danger" type="submit">Kirim Penolakan</button>
            <button class="btn btn-sm btn-muted" type="button" onclick="tutupTolak({{ p.id }})">Batal</button>
          </div>
        </form>
      </div>
    {% endfor %}
  </div>
{% endif %}
{% endblock %}

{% block scripts %}
<script>
  function bukaTolak(id) {
    var form = document.getElementById('formTolak' + id);
    if (form) { form.style.display = 'block'; }
  }
  function tutupTolak(id) {
    var form = document.getElementById('formTolak' + id);
    if (form) { form.style.display = 'none'; }
  }
</script>
{% endblock %}
```


## `Website/templates/peminjaman/pinjam.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Pinjamkan Buku{% endblock %}
{% block content %}
<div class="card" style="max-width:500px;">
  <h2>Pinjamkan Buku: {{ buku.judul }}</h2>
  <p>Stok tersedia: <strong>{{ buku.stok }}</strong></p>
  <form method="POST">
    <div class="form-group">
      <label>Pilih Mahasiswa</label>
      <select name="user_id" required>
        <option value="">- Pilih Mahasiswa -</option>
        {% for a in anggota_list %}
          <option value="{{ a.id }}">{{ a.nama_lengkap }} ({{ a.nim or a.username }}) — kuota {{ a.jumlah_pinjaman_aktif }}/{{ config.MAKS_PINJAM_PER_USER }}</option>
        {% endfor %}
      </select>
    </div>
    <div class="form-group">
      <label>Lama pinjam (hari)</label>
      <input type="number" name="lama_hari" min="1" max="365" value="{{ lama_default }}" inputmode="numeric">
      <p class="sampul-hint">Jatuh tempo = hari ini + lama pinjam. Nilai awal mengikuti {{ 'pengaturan khusus buku ini' if buku.lama_pinjam_hari else 'pengaturan umum perpustakaan' }}. Denda: {{ config.DENDA_PER_HARI|rupiah }}/hari setelah jatuh tempo.</p>
    </div>
    <button class="btn" type="submit">Proses Peminjaman</button>
    <a href="{{ url_for('buku.detail_buku', buku_id=buku.id) }}" class="btn btn-ghost">Batal</a>
  </form>
</div>
{% endblock %}
```


## `Website/templates/peminjaman/riwayat_anggota.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Riwayat Peminjaman{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-clock"></use></svg> {{ 'Riwayat & Pengajuan Saya' if bisa_batalkan else 'Riwayat Peminjaman - ' ~ anggota.nama_lengkap }}</h2>
  {% if bisa_batalkan %}<p class="page-sub">Semua pengajuan dan riwayat peminjaman buku Anda, dari yang terbaru.</p>{% endif %}
</div>

<form method="GET" class="search-bar">
  <input type="text" name="q" placeholder="Cari judul buku..." value="{{ q }}">
  <button class="btn" type="submit">Cari</button>
  {% if q %}<a href="{{ url_for(request.endpoint, **request.view_args) }}" class="btn btn-ghost">Reset</a>{% endif %}
</form>

<div class="card">
  <div class="table-scroll">
  <table>
    <thead>
      <tr>
        <th>Buku</th><th>Tgl Pinjam</th><th>Jatuh Tempo</th><th>Tgl Kembali</th><th>Status</th><th>Denda</th>
        {% if bisa_batalkan %}<th>Aksi</th>{% endif %}
      </tr>
    </thead>
    <tbody>
      {% for p in daftar %}
      <tr>
        <td>{{ p.buku.judul }}</td>
        <td>{{ p.tanggal_pinjam.strftime('%d-%m-%Y') }}</td>
        <td>{{ p.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}</td>
        <td>{{ p.tanggal_kembali.strftime('%d-%m-%Y') if p.tanggal_kembali else '-' }}</td>
        <td>
          {% if p.status == 'dikembalikan' %}
            <span class="badge badge-success">Dikembalikan</span>
          {% elif p.status == 'diajukan' %}
            <span class="badge badge-warning">Menunggu Persetujuan</span>
          {% elif p.status == 'ditolak' %}
            <span class="badge badge-danger" title="{{ p.catatan or '' }}">Ditolak{{ ' — ' ~ p.catatan if p.catatan }}</span>
          {% elif p.is_telat %}
            <span class="badge badge-danger">Terlambat {{ p.hari_telat }} hari</span>
          {% elif p.hari_menuju_jatuh_tempo is not none and p.hari_menuju_jatuh_tempo <= config.PERINGATAN_JATUH_TEMPO_HARI %}
            <span class="badge badge-warning">⏰ Segera Tempo ({{ p.hari_menuju_jatuh_tempo }}h)</span>
          {% else %}
            <span class="badge badge-info">Dipinjam</span>
          {% endif %}
        </td>
        <td>
          {% set d = denda_sekarang(p) %}
          {% if d > 0 %}
            <strong>{{ d|rupiah }}</strong>
            {% if p.status == 'dipinjam' %}<br><small style="color:var(--muted);">berjalan</small>
            {% elif p.status_denda == 'belum_lunas' %}<br><span class="badge badge-danger">Belum lunas</span>
            {% elif p.status_denda == 'lunas' %}<br><span class="badge badge-success">Lunas</span>
            {% elif p.status_denda == 'dibebaskan' %}<br><span class="badge badge-info">Dibebaskan</span>{% endif %}
          {% else %}-{% endif %}
        </td>
        {% if bisa_batalkan %}
        <td>
          {% if p.status == 'diajukan' %}
          <form method="POST" action="{{ url_for('peminjaman.batalkan_pengajuan', peminjaman_id=p.id) }}"
                onsubmit="return confirm('Batalkan pengajuan peminjaman ini?');">
            <button class="btn btn-sm btn-danger" type="submit">Batalkan</button>
          </form>
          {% else %}
            -
          {% endif %}
        </td>
        {% endif %}
      </tr>
      {% else %}
      <tr><td colspan="{{ 7 if bisa_batalkan else 6 }}">Belum ada riwayat peminjaman.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
</div>
{% endblock %}
```


## `Website/templates/peminjaman/riwayat_buku.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Riwayat Peminjaman Buku{% endblock %}
{% block content %}
<h2>Riwayat Peminjaman - {{ buku.judul }}</h2>

<form method="GET" class="search-bar">
  <input type="text" name="q" placeholder="Cari nama/username/NIM mahasiswa..." value="{{ q }}">
  <button class="btn" type="submit">Cari</button>
  {% if q %}<a href="{{ url_for(request.endpoint, **request.view_args) }}" class="btn btn-ghost">Reset</a>{% endif %}
</form>

<div class="card">
  <div class="table-scroll">
  <table>
    <thead>
      <tr><th>Mahasiswa</th><th>Tgl Pinjam</th><th>Jatuh Tempo</th><th>Tgl Kembali</th><th>Status</th></tr>
    </thead>
    <tbody>
      {% for p in daftar %}
      <tr>
        <td>{{ p.anggota.nama_lengkap }}</td>
        <td>{{ p.tanggal_pinjam.strftime('%d-%m-%Y') }}</td>
        <td>{{ p.tanggal_jatuh_tempo.strftime('%d-%m-%Y') }}</td>
        <td>{{ p.tanggal_kembali.strftime('%d-%m-%Y') if p.tanggal_kembali else '-' }}</td>
        <td>
          {% if p.status == 'dikembalikan' %}
            <span class="badge badge-success">Dikembalikan</span>
          {% elif p.is_telat %}
            <span class="badge badge-danger">Terlambat</span>
          {% else %}
            <span class="badge badge-info">Dipinjam</span>
          {% endif %}
        </td>
      </tr>
      {% else %}
      <tr><td colspan="5">Belum pernah dipinjam.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
</div>
{% endblock %}
```


## `Website/templates/pengaturan/halaman.html`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```html
{% extends "layout/base.html" %}
{% block title %}Pengaturan Perpustakaan{% endblock %}
{% block content %}
<div class="page-head">
  <h2><svg class="icon"><use href="#i-settings"></use></svg> Pengaturan Perpustakaan</h2>
  <p class="page-sub">Atur lama peminjaman, tarif denda, dan aturan lainnya. Perubahan berlaku untuk peminjaman berikutnya.</p>
</div>

<form method="POST">
  <div class="card">
    <h3 style="margin-top:0;">Jatuh tempo &amp; peminjaman</h3>
    {% for f in kolom if f.kunci in ['lama_pinjam_hari', 'maks_pinjam', 'maks_perpanjang', 'peringatan_hari'] %}
      {{ baris(f) }}
    {% endfor %}
  </div>

  <div class="card">
    <h3 style="margin-top:0;">Denda keterlambatan</h3>
    {% for f in kolom if f.kunci in ['denda_per_hari', 'denda_maks', 'masa_tenggang_hari', 'blokir_jika_denda'] %}
      {{ baris(f) }}
    {% endfor %}
    <p class="page-sub" style="margin-top:0.8rem;">
      Contoh: tarif Rp 1.000/hari, tenggang 0 hari → buku telat 5 hari didenda Rp 5.000.
      Denda buku yang masih dipinjam dihitung berjalan setiap hari, lalu dibekukan saat buku dikembalikan.
    </p>
  </div>

  <button class="btn" type="submit">Simpan Pengaturan</button>
  <a href="{{ url_for('dashboard.index') }}" class="btn btn-ghost">Batal</a>
</form>
{% endblock %}

{# satu baris pengaturan: label + isian + satuan + penjelasan #}
{% macro baris(f) %}
<div class="setting-row">
  <div class="setting-label">
    <label for="f_{{ f.kunci }}">{{ f.label }}</label>
    <small>{{ f.bantuan }}</small>
  </div>
  <div class="setting-input">
    {% if f.kunci == 'blokir_jika_denda' %}
      <select id="f_{{ f.kunci }}" name="{{ f.kunci }}">
        <option value="1" {{ 'selected' if f.nilai == 1 }}>Ya, blokir</option>
        <option value="0" {{ 'selected' if f.nilai == 0 }}>Tidak</option>
      </select>
    {% else %}
      <input id="f_{{ f.kunci }}" type="number" name="{{ f.kunci }}" min="{{ f.min }}" max="{{ f.maks }}" value="{{ f.nilai }}" required inputmode="numeric">
      <span class="setting-satuan">{{ f.satuan }}</span>
    {% endif %}
  </div>
</div>
{% endmacro %}
```


## `Website/utils/__init__.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python

```


## `Website/utils/decorators.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(*roles):
    """Decorator untuk membatasi akses route berdasarkan role.
    Contoh: @role_required('kepala_perpustakaan') atau @role_required('staf', 'kepala_perpustakaan')
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator
```


## `Website/utils/denda.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
"""Perhitungan denda keterlambatan."""
from datetime import date

from flask import current_app
from sqlalchemy import func

from extensions import db
from models import Peminjaman


def hitung_denda(jatuh_tempo, sampai, tarif, maks=0, tenggang=0):
    """Fungsi murni (mudah diuji).

    jatuh_tempo, sampai : date  -> 'sampai' = hari ini (masih dipinjam) atau tanggal kembali
    tarif               : Rp per hari
    maks                : batas atas denda (0 = tanpa batas)
    tenggang            : hari gratis setelah jatuh tempo
    """
    hari_kena_denda = (sampai - jatuh_tempo).days - tenggang
    if hari_kena_denda <= 0 or tarif <= 0:
        return 0
    total = hari_kena_denda * tarif
    if maks and total > maks:
        total = maks
    return total


def denda_dari_config(jatuh_tempo, sampai):
    c = current_app.config
    return hitung_denda(jatuh_tempo, sampai, c["DENDA_PER_HARI"], c["DENDA_MAKS"], c["MASA_TENGGANG_HARI"])


def denda_peminjaman(p):
    """Denda sebuah peminjaman saat ini.
    - dikembalikan : nilai yang sudah dibekukan saat pengembalian
    - dipinjam     : denda berjalan sampai hari ini
    - lainnya      : 0"""
    if p.status == "dikembalikan":
        return p.denda or 0
    if p.status == "dipinjam":
        return denda_dari_config(p.tanggal_jatuh_tempo, date.today())
    return 0


def total_denda_belum_lunas(user_id=None):
    """Jumlah denda yang sudah dibekukan tapi belum dibayar (semua anggota atau satu anggota)."""
    q = db.session.query(func.coalesce(func.sum(Peminjaman.denda), 0)).filter(
        Peminjaman.status_denda == "belum_lunas"
    )
    if user_id:
        q = q.filter(Peminjaman.user_id == user_id)
    return int(q.scalar() or 0)


def denda_berjalan_semua(user_id=None):
    """Total denda dari buku yang MASIH dipinjam dan sudah telat."""
    q = Peminjaman.query.filter_by(status="dipinjam")
    if user_id:
        q = q.filter_by(user_id=user_id)
    return sum(denda_peminjaman(p) for p in q.all())


def format_rupiah(angka):
    return "Rp " + f"{int(angka or 0):,}".replace(",", ".")
```


## `Website/utils/excel_export.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
"""Ekspor data ke file Excel (.xlsx) dengan header tebal & lebar kolom otomatis."""
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


def buat_excel(judul_sheet, header, baris):
    """header: list nama kolom | baris: list of list. Kembalikan BytesIO siap dikirim."""
    wb = Workbook()
    ws = wb.active
    ws.title = judul_sheet[:31]
    ws.append(header)
    for sel in ws[1]:
        sel.font = Font(bold=True, color="FFFFFF")
        sel.fill = PatternFill("solid", fgColor="5C211D")
        sel.alignment = Alignment(vertical="center")
    for r in baris:
        ws.append(r)
    for i, kolom in enumerate(ws.columns, start=1):
        terpanjang = max((len(str(c.value)) for c in kolom if c.value is not None), default=8)
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = min(terpanjang + 3, 50)
    ws.freeze_panes = "A2"
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
```


## `Website/utils/excel_import.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
import io
from openpyxl import Workbook, load_workbook

from extensions import db
from models import Buku, Kategori

TEMPLATE_HEADERS = [
    "judul", "penulis", "penerbit", "tahun_terbit",
    "isbn", "kategori", "deskripsi", "stok",
]


def buat_template_excel():
    """Membuat workbook Excel kosong (hanya header) sebagai template import."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Data Buku"
    ws.append(TEMPLATE_HEADERS)

    # baris contoh (boleh dihapus user sebelum upload)
    ws.append([
        "Contoh: Laskar Pelangi", "Andrea Hirata", "Bentang Pustaka",
        2005, "9789793062792", "Fiksi", "Novel tentang pendidikan di Belitung", 3,
    ])

    for col_cells in ws.columns:
        length = max(len(str(cell.value)) if cell.value else 0 for cell in col_cells)
        ws.column_dimensions[col_cells[0].column_letter].width = max(12, length + 2)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


def import_buku_dari_excel(file_stream):
    """Membaca file .xlsx yang diupload, lalu insert ke tabel buku.
    Mengembalikan (jumlah_sukses, list_error)
    """
    wb = load_workbook(file_stream, data_only=True)
    ws = wb.active

    rows = list(ws.iter_rows(min_row=2, values_only=True))
    sukses = 0
    errors = []

    for i, row in enumerate(rows, start=2):
        if row is None or all(v is None for v in row):
            continue  # baris kosong, lewati

        try:
            judul, penulis, penerbit, tahun_terbit, isbn, kategori_nama, deskripsi, stok = (
                list(row) + [None] * (len(TEMPLATE_HEADERS) - len(row))
            )[: len(TEMPLATE_HEADERS)]

            if not judul or not penulis:
                errors.append(f"Baris {i}: 'judul' dan 'penulis' wajib diisi, dilewati.")
                continue

            kategori_obj = None
            if kategori_nama:
                kategori_obj = Kategori.query.filter_by(nama_kategori=str(kategori_nama).strip()).first()
                if not kategori_obj:
                    kategori_obj = Kategori(nama_kategori=str(kategori_nama).strip())
                    db.session.add(kategori_obj)
                    db.session.flush()

            buku = Buku(
                judul=str(judul).strip(),
                penulis=str(penulis).strip(),
                penerbit=str(penerbit).strip() if penerbit else None,
                tahun_terbit=int(tahun_terbit) if tahun_terbit else None,
                isbn=str(isbn).strip() if isbn else None,
                kategori_id=kategori_obj.id if kategori_obj else None,
                deskripsi=str(deskripsi).strip() if deskripsi else None,
                stok=int(stok) if stok else 0,
            )
            db.session.add(buku)
            sukses += 1
        except Exception as e:
            errors.append(f"Baris {i}: gagal diproses ({e})")

    db.session.commit()
    return sukses, errors
```


## `Website/utils/kartu.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
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
```


## `Website/utils/pengaturan.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
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
```


## `Website/utils/pinjam.py`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```python
from datetime import timedelta

from flask import current_app

from models import Peminjaman
from utils.denda import denda_peminjaman, format_rupiah, total_denda_belum_lunas
from utils.kartu import terbitkan_kartu_jika_belum_ada


def lama_pinjam_untuk(buku, lama_hari=None):
    """Tentukan lama pinjam (hari): isian petugas > pengaturan khusus buku > pengaturan umum."""
    if lama_hari and lama_hari > 0:
        return lama_hari
    if buku is not None and buku.lama_pinjam_hari:
        return buku.lama_pinjam_hari
    return current_app.config["LAMA_PINJAM_HARI"]


def hitung_jatuh_tempo(buku, mulai, lama_hari=None):
    return mulai + timedelta(days=lama_pinjam_untuk(buku, lama_hari))


def cek_tunggakan(mahasiswa):
    """Jika pengaturan 'blokir jika ada denda' aktif: mahasiswa dengan buku terlambat
    atau denda belum lunas tidak boleh meminjam lagi."""
    if not current_app.config["BLOKIR_JIKA_DENDA"]:
        return True, None

    telat = [
        p for p in Peminjaman.query.filter_by(user_id=mahasiswa.id, status="dipinjam").all()
        if p.hari_telat > 0
    ]
    if telat:
        return False, (
            f"Masih ada {len(telat)} buku yang terlambat dikembalikan "
            f"(denda berjalan {format_rupiah(sum(denda_peminjaman(p) for p in telat))}). "
            "Kembalikan buku tersebut terlebih dahulu."
        )

    belum_lunas = total_denda_belum_lunas(mahasiswa.id)
    if belum_lunas > 0:
        return False, (
            f"Ada denda belum lunas sebesar {format_rupiah(belum_lunas)}. "
            "Lunasi denda di perpustakaan terlebih dahulu."
        )
    return True, None


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
    """Gabungan validasi kartu + tunggakan denda + kuota. Kembalikan (True, None) atau (False, pesan)."""
    for cek in (cek_kartu_valid, cek_tunggakan, cek_kuota_pinjam):
        ok, pesan = cek(mahasiswa)
        if not ok:
            return False, pesan
    return True, None
```


## `run.bat`

**Peran berkas:** sumber lengkap dari paket proyek. Gunakan bagian penjelasan fungsi dan bab terkait untuk memahami bagaimana berkas ini dipanggil.

```bat
@echo off
title Aplikasi Perpustakaan
cd /d "%~dp0"

start "" http://127.0.0.1:5000/
python Website/app.py
pause
```

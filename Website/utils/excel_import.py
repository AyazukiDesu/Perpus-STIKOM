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

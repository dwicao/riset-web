#!/usr/bin/env python3
"""Generate soal_zikir_adab_100pg.pdf dari bank_soal.py"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from bank_soal import SECTIONS, ALL, KUNCI

_REPLACEMENTS = {
    '\u2018': "'", '\u2019': "'", '\u201a': "'",
    '\u201c': '"', '\u201d': '"', '\u201e': '"',
    '\u2014': ' - ', '\u2013': '-', '\u2026': '...',
    '\u00a0': ' ', '\uf000': '',
}

def S(text):
    if not isinstance(text, str):
        return text
    for k, v in _REPLACEMENTS.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'ignore').decode('latin-1')

_orig_multi, _orig_cell = FPDF.multi_cell, FPDF.cell
def _patched_multi(self, *args, **kwargs):
    args = tuple(S(a) for a in args)
    kwargs = {k: (S(v) if isinstance(v, str) else v) for k, v in kwargs.items()}
    return _orig_multi(self, *args, **kwargs)
def _patched_cell(self, *args, **kwargs):
    args = tuple(S(a) for a in args)
    kwargs = {k: (S(v) if isinstance(v, str) else v) for k, v in kwargs.items()}
    return _orig_cell(self, *args, **kwargs)
FPDF.multi_cell = _patched_multi
FPDF.cell = _patched_cell

PRIMARY = (16, 92, 72)
DARK = (35, 38, 45)
GREY = (120, 126, 138)
CREAM = (247, 250, 247)

class Report(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(15, 14, 15)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('helvetica', 'I', 8); self.set_text_color(*GREY)
        self.cell(130, 8, '100 Soal Pilihan Ganda - Zikir dan Adab (Kumpulan Matan)', new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(55, 8, f'Hal. {self.page_no()}', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*PRIMARY); self.set_line_width(0.5)
        self.line(15, 14.5, 195, 14.5)
        self.set_text_color(0, 0, 0); self.ln(1.5)

def h_band(pdf, text):
    pdf.set_fill_color(*PRIMARY); pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 10.5)
    pdf.set_x(15)
    pdf.multi_cell(0, 8, '  ' + text, fill=True)
    pdf.ln(2); pdf.set_text_color(*DARK)

def question(pdf, num, soal, opsi, rujukan):
    pdf.set_x(15)
    pdf.set_font('helvetica', 'B', 9.5)
    pdf.set_fill_color(*CREAM)
    pdf.set_text_color(*PRIMARY)
    pdf.multi_cell(0, 5.2, f'{num:>3}.  {soal}', fill=True)
    pdf.set_text_color(*DARK)
    labels = ['A', 'B', 'C', 'D']
    for lab, opt in zip(labels, opsi):
        pdf.set_x(22)
        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(0, 5, f'{lab}.  {opt}')
    pdf.set_x(22)
    pdf.set_font('helvetica', 'I', 7); pdf.set_text_color(*GREY)
    pdf.multi_cell(0, 4.5, f'Rujukan: {rujukan}')
    pdf.set_text_color(*DARK)
    pdf.ln(1.6)

pdf = Report()

# ------------------------------------------------ COVER
pdf.add_page()
pdf.set_fill_color(*PRIMARY); pdf.rect(0, 0, 210, 88, style='F')
pdf.set_text_color(255, 255, 255)
pdf.set_xy(15, 16); pdf.set_font('helvetica', 'B', 27)
pdf.multi_cell(180, 12, '100 Soal\nZikir dan Adab')
pdf.set_xy(15, 52); pdf.set_font('helvetica', '', 12.5)
pdf.multi_cell(180, 8, 'Kumpulan Matan untuk Penuntut Ilmu\nTingkat Pertama')
pdf.set_text_color(*DARK)
pdf.set_xy(15, 100)
pdf.set_font('helvetica', 'B', 11); pdf.cell(0, 7, 'Paket Latihan untuk Santri', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', '', 10)
pdf.multi_cell(180, 5.6, '100 soal pilihan ganda (PG) dengan 4 opsi jawaban, dibagi dalam 10 bagian tematik mengikuti isi kitab. Setiap soal disertai rujukan hadis/bab kitab agar santri belajar, bukan sekadar menebak. Kunci jawaban ada di halaman terakhir.')
pdf.ln(4)
pdf.set_x(15)
pdf.set_font('helvetica', 'B', 10); pdf.cell(0, 6, 'Sumber Materi', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', '', 9)
pdf.multi_cell(180, 5, 'KITAB: Zikir dan Adab (Al-Adzkar wal-Adab)\nPENYUSUN: Dr. Abdul Muhsin bin Muhammad al-Qasim (Imam & Khatib Masjid Nabawi) - Serial Mutun Thalibil ilm, Tingkat Pertama\nSUMBER PDF: https://d1.islamhouse.com/data/id/ih_books/single/id-mustawa1-pp.pdf (diunduh 17 Nov 2026)')
pdf.ln(2)
pdf.set_x(15)
pdf.set_font('helvetica', 'B', 10); pdf.cell(0, 6, 'Tentang Matan', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', '', 9)
pdf.multi_cell(180, 5, 'Teks matan (hadis-hadis) bersifat klasik dan bebas dikutip. Buku terjemahan ini disusun berbasis tahkik ~5000 manuskrip. Naskah dan terjemahan milik penyusun/Kitab al-Qasim; dokumen ini dibuat semata-mata untuk tujuan pendidikan pesantren.')

# ------------------------------------------------ PETUNJUK & KISI-KISI
pdf.add_page()
h_band(pdf, 'Petunjuk Pengerjaan')
pdf.set_font('helvetica', '', 9.5)
petunjuk = [
    'Kerjakan secara mandiri. Waktu yang disarankan: 90 menit untuk 100 soal.',
    'Pilih SATU jawaban yang paling tepat (A/B/C/D).',
    'Nilai: 1 poin per soal benar; tidak ada pengurangan poin untuk jawaban salah.',
    'Setelah selesai, cocokkan di halaman KUNCI JAWABAN (di akhir dokumen) dan hitung skor Anda.',
    'Untuk koreksi dan belajar: lihat kolom "Rujukan" di bawah tiap soal untuk mencari hadis/bab pada kitab sumber.',
    'Catatan: transliterasi nama dan lafaz hadis disederhanakan agar mudah dibaca (tanpa harakat).',
]
for i, p in enumerate(petunjuk, 1):
    pdf.set_x(15)
    pdf.multi_cell(0, 5.5, f'{i}.  {p}')
pdf.ln(2)
h_band(pdf, 'Kisi-kisi / Cakupan Materi')
rows = []
start = 1
for key, name, qs, _ in SECTIONS:
    end = start + len(qs) - 1
    rows.append((f'{key}', name, f'{start}-{end}', str(len(qs))))
    start = end + 1
pdf.set_font('helvetica', 'B', 8.5)
pdf.set_fill_color(*PRIMARY); pdf.set_text_color(255, 255, 255)
pdf.set_x(15)
for h, w in zip(['Bagian', 'Cakupan Materi', 'No. Soal', 'Jml'], [14, 128, 22, 12]):
    pdf.cell(w, 7, ' ' + h, fill=True)
pdf.ln()
pdf.set_font('helvetica', '', 8.5); pdf.set_text_color(*DARK)
fill = False
for r in rows:
    pdf.set_fill_color(*CREAM)
    pdf.set_x(15)
    pdf.cell(14, 6.5, ' ' + r[0], fill=fill)
    pdf.cell(128, 6.5, ' ' + r[1][:96], fill=fill)
    pdf.cell(22, 6.5, ' ' + r[2], fill=fill)
    pdf.cell(12, 6.5, ' ' + r[3], fill=fill)
    pdf.ln()
    fill = not fill
pdf.ln(3)
pdf.set_font('helvetica', 'I', 8); pdf.set_text_color(*GREY)
pdf.set_x(15)
pdf.multi_cell(0, 5, 'Distribusi soal mengikuti komposisi isi kitab (salat dan malam/tidur paling banyak pembahasannya). Semua soal dan jawaban diverifikasi langsung dari teks terjemah Indonesia kitab sumber.')

# ------------------------------------------------ SOAL
for key, name, qs, offset in SECTIONS:
    pdf.add_page()
    h_band(pdf, f'Bagian {key} — {name}')
    for i, (soal, opsi, kunci_idx, rujukan) in enumerate(qs):
        num = offset + i
        question(pdf, num, soal, opsi, rujukan)

# ------------------------------------------------ KUNCI JAWABAN
pdf.add_page()
h_band(pdf, 'Kunci Jawaban')
pdf.set_font('helvetica', '', 10)
per_row = 10
col_w = (180) / per_row
for start in range(0, 100, per_row):
    pdf.set_x(15)
    for j in range(start, start + per_row):
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(*PRIMARY)
        pdf.cell(col_w, 7, f'{j+1}', align='C')
    pdf.ln()
    pdf.set_x(15)
    for j in range(start, start + per_row):
        pdf.set_font('helvetica', 'B', 13)
        pdf.set_text_color(*DARK)
        pdf.set_fill_color(*CREAM)
        pdf.cell(col_w, 8, KUNCI[j], align='C', fill=True)
    pdf.ln()
    pdf.ln(2)
pdf.ln(3)
h_band(pdf, 'Skor & Rubrik Sederhana')
pdf.set_font('helvetica', '', 9.5)
rubrik = [
    ('90-100', 'Mumtaz — sangat hafal dan paham zikir & adab.'),
    ('75-89', 'Jayyid — baik; ulangi bagian yang salah.'),
    ('60-74', 'Maqbul — cukup; perlu murojaah rutin tiap bab.'),
    ('< 60', 'Kurang — pelajari ulang kitabnya dari awal bersama pembimbing.'),
]
for rentang, ket in rubrik:
    pdf.set_x(15)
    pdf.multi_cell(0, 5.5, f'{rentang}  :  {ket}')
pdf.ln(2)
pdf.set_font('helvetica', 'I', 8); pdf.set_text_color(*GREY)
pdf.set_x(15)
pdf.multi_cell(0, 5, 'Dokumen ini dibuat 17 Nov 2026 dari sumber resmi. Isi soal bersifat edukatif untuk pesantren dan tidak menggantikan bimbingan guru/kyai. Perbaikan: koreksi lafaz via Kitab sumber atau Pembimbing.')

OUT = 'soal_zikir_adab_100pg.pdf'
pdf.output(OUT)
print('PDF selesai:', OUT, '| halaman:', pdf.page_no(), '| soal:', len(ALL))

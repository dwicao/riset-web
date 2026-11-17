#!/usr/bin/env python3
"""Generate roadmap_santri.pdf — versi cetak Ringkas dari Roadmap Santri."""
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

PRIMARY = (20, 83, 45)
GOLD = (202, 138, 4)
DARK = (28, 25, 23)
GREY = (110, 105, 95)
CREAM = (250, 247, 239)

def S(t):
    repl = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2014': ' - ', '\u2013': '-', '\u2026': '...', '\u00a0': ' ', '\u2192': '->'}
    for k, v in repl.items():
        t = t.replace(k, v)
    return t.encode('latin-1', 'ignore').decode('latin-1')

class Report(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(14, 14, 14)
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('helvetica', 'I', 7.5); self.set_text_color(*GREY)
        self.cell(120, 8, 'Roadmap Santri - Peta Jalan Setelah Lulus Pondok', new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(64, 8, f'Hal. {self.page_no()}', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*PRIMARY); self.set_line_width(0.5)
        self.line(14, 14.5, 196, 14.5)
        self.set_text_color(0, 0, 0); self.ln(2)

pdf = Report()

def band(text, color=PRIMARY, h=9):
    pdf.set_fill_color(*color); pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_x(14)
    pdf.multi_cell(0, h, '  ' + S(text), fill=True)
    pdf.ln(2.5); pdf.set_text_color(*DARK)

def body(text, size=9.5):
    pdf.set_x(14)
    pdf.set_font('helvetica', '', size)
    pdf.multi_cell(0, 5.2, S(text))
    pdf.ln(1)

def bullets(items, size=9):
    pdf.set_font('helvetica', '', size)
    for it in items:
        pdf.set_x(16)
        pdf.multi_cell(0, 4.8, '-  ' + S(it))
    pdf.ln(1)

def load_jalur():
    src = open('data_jalur.js', encoding='utf-8').read()
    entries = [m[0] for m in re.finditer(r"\{\s*id: '[^']+',.*?\n  \},", src, re.S)]
    out = []
    for e in entries:
        def f(key):
            m = re.search(rf"{key}: '([^']*)'", e)
            return m.group(1) if m else ''
        steps = re.findall(r"'([^']{30,400})'", re.search(r"steps: \[(.*?)\]", e, re.S).group(1))
        syarat = re.findall(r"'([^']{8,300})'", re.search(r"syarat: \[(.*?)\]", e, re.S).group(1))
        tips = re.findall(r"'([^']{15,400})'", re.search(r"tips: \[(.*?)\]", e, re.S).group(1))
        resiko = re.findall(r"'([^']{10,300})'", re.search(r"resiko: \[(.*?)\]", e, re.S).group(1))
        out.append(dict(id=f('id'), name=f('name'), summary=f('summary'), contoh=f('contoh'),
                        steps=steps, syarat=syarat, prospek=f('prospek'), tips=tips, resiko=resiko))
    return out

def load_list(src, name):
    m = re.search(rf"const {name} = \[(.*?)\n\];", src, re.S)
    items = re.findall(r"\[\s*'([^']{20,400})',\s*\[([^\]]*)\]\s*\]|\['([^']{20,400})'\]", m.group(1), re.S)
    return m.group(1)

# ------------------------------------------------------------- COVER
pdf.add_page()
pdf.set_fill_color(*PRIMARY); pdf.rect(0, 0, 210, 92, style='F')
pdf.set_text_color(255, 255, 255)
pdf.set_xy(14, 16); pdf.set_font('helvetica', 'B', 30)
pdf.multi_cell(182, 13, 'Roadmap Santri')
pdf.set_xy(14, 42); pdf.set_font('helvetica', '', 13)
pdf.multi_cell(182, 8, 'Peta Jalan Setelah Lulus Pondok Pesantren\n14 jalur hidup - alur 6 tahap - checklist 30-60-90 hari')
pdf.set_xy(14, 68); pdf.set_font('helvetica', 'I', 9.5)
pdf.multi_cell(182, 5.5, 'Terinspirasi dari roadmap.sh (Kamran Ahmed) | dwicao/riset-web | 17 Nov 2026')
pdf.set_text_color(*DARK)
pdf.set_y(104)
pdf.set_font('helvetica', 'B', 11); pdf.set_x(14)
pdf.cell(0, 7, 'Untuk Siapa?', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body('Santri lulusan SMA/SMK/MA/MTs/Diniyah/Tahfidz yang sedang menentukan langkah setelah mondok; orang tua, pengurus pondok, dan pembimbing sebagai bahan diskusi.')
pdf.set_font('helvetica', 'B', 11); pdf.set_x(14)
pdf.cell(0, 7, 'Cara Pakai Dokumen Ini', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
bullets(['Baca Alur 6 Tahap (halaman 2) agar orientasi benar sebelum memilih jalur.',
         'Telusuri 14 jalur — pilih 1 utama + 1 cadangan.',
         'Ikuti Checklist 30-60-90 Hari untuk 90 hari pertama setelah lulus.',
         'Ajak orang tua/ulama/mentor diskusi — dokumen ini kompas, bukan vonis.'])

# ------------------------------------------------------------- ALUR
pdf.add_page()
band('ALUR BESAR: 6 Tahap dari Lulus ke Hidup Mandiri')
TAHAP = [('1. Kenali Dirimu', 'Catat hafalan, skill, minat, dan modal yang kamu punya sekarang.'),
         ('2. Tentukan Prioritas', 'Ilmu dulu? Penghasilan dulu? Keluarga dulu? Jujur pada diri sendiri.'),
         ('3. Pilih Jalur Utama + Cadangan', 'Satu jalur utama, satu cadangan — jangan sepuluh sekaligus.'),
         ('4. Siapkan Syarat', 'Ijazah, SKCK, CV, hafalan tambahan, atau modal — lengkapi dulu.'),
         ('5. Eksekusi 90 Hari', 'Ikuti checklist 30-60-90 hari. Ukur hasilnya, bukan perasaannya.'),
         ('6. Review & Pivot', 'Kalau tidak cocok, ganti jalur. Itu bukan gagal — itu data.')]
for i, (t, d) in enumerate(TAHAP):
    pdf.set_x(14)
    pdf.set_fill_color(*CREAM); pdf.set_font('helvetica', 'B', 10.5); pdf.set_text_color(*PRIMARY)
    pdf.multi_cell(0, 6.5, '  ' + S(t), fill=True)
    pdf.set_x(20); pdf.set_font('helvetica', '', 9.5); pdf.set_text_color(*DARK)
    pdf.multi_cell(0, 5, S(d))
    if i < len(TAHAP) - 1:
        pdf.set_x(14); pdf.set_font('helvetica', 'B', 10); pdf.set_text_color(*GOLD)
        pdf.cell(0, 5, '        |', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(*DARK)
pdf.ln(2)
body('Aturan sederhana: 1 jalur utama + 1 jalur cadangan. Kombinasi umum yang bekerja baik untuk santri: kerja formal (utama) + mengajar TPQ (sampingan); kuliah (utama) + freelance (sampingan); wirausaha (utama) + dakwah digital (sampingan).')

# ------------------------------------------------------------- 14 JALUR
pdf.add_page()
band('14 JALUR HIDUP SETELAH LULUS')
body('Nomor urut mengikuti urutan peta asli di web/HTML. Setiap jalur berisi: gambaran, contoh konkret, langkah, syarat, prospek, tips, dan risiko.')
for j in load_jalur():
    pdf.ln(1)
    pdf.set_fill_color(*CREAM); pdf.set_font('helvetica', 'B', 11); pdf.set_text_color(*PRIMARY)
    pdf.set_x(14)
    pdf.multi_cell(0, 7, '  ' + S(j['name'].upper()), fill=True)
    pdf.set_text_color(*DARK)
    body(j['summary'], 9)
    body('Contoh konkret: ' + j['contoh'], 8.5)
    bullets([f'Langkah {i+1}: {s}' for i, s in enumerate(j['steps'])], 8.5)
    bullets(['Syarat: ' + '; '.join(j['syarat'])], 8.5)
    body('Prospek: ' + j['prospek'], 8.5)
    bullets(['Tips: ' + t for t in j['tips']], 8.5)
    bullets(['Risiko: ' + t for t in j['resiko']], 8.5)

# ------------------------------------------------------------- CHECKLIST
pdf.add_page()
band('CHECKLIST 30-60-90 HARI', GOLD)
CL = [('30 Hari - Kenali Diri & Arah', [
        'Tulis 10 hal: skill, hafalan, pengalaman, hobi, isi kantong',
        'Tanya 5 alumni: mereka di mana & bagaimana sampai di sana',
        'Pilih 2 jalur paling cocok dari daftar di atas',
        'Rapikan ijazah, KK, KTP, SKCK, pasfoto',
        'Buka tabungan darurat (meski kecil) & catat pengeluaran']),
      ('60 Hari - Persiapan & Uji Coba', [
        'Daftar/test/kursus untuk jalur pilihanmu',
        'Buat CV/profil + portofolio (foto, tulisan, testimoni)',
        '1 proyek nyata: ngajar 1x, jual 10 produk, lamar 5 loker',
        'Bangun jaringan: alumni, remaja masjid, komunitas profesimu',
        'Evaluasi: apakah jalur ini masih cocok?']),
      ('90 Hari - Eksekusi & Komitmen', [
        'Putuskan 1 jalur utama + 1 cadangan',
        'Rencana 6-12 bulan (target, tanggal, langkah)',
        'Keputusan konkret: daftar kampus / kontrak kerja / komitmen usaha',
        'Evaluasi bersama orang tua/ulama/mentor',
        'Ulangi siklus tiap 90 hari selama 1 tahun'])]
for title, items in CL:
    pdf.set_font('helvetica', 'B', 10.5); pdf.set_text_color(*PRIMARY); pdf.set_x(14)
    pdf.cell(0, 7, S(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*DARK)
    for it in items:
        pdf.set_x(17); pdf.set_font('helvetica', '', 9.5)
        pdf.multi_cell(0, 5.5, '[ ]  ' + S(it))
    pdf.ln(2)

# ------------------------------------------------------------- FAQ
pdf.add_page()
band('FAQ SINGKAT')
FAQ = [('Mondok itu menganggur?', 'Tidak. Mondok membentuk karakter, disiplin, dan keilmuan; banyak santri langsung bekerja/kuliah/usaha setelah lulus.'),
       ('Harus kuliah setelah lulus?', 'Tidak wajib. Banyak jalur sukses tanpa kuliah: vokasi, wirausaha, freelance, tahfidz.'),
       ('Tidak punya ijazah SMA?', 'Ikut Paket C/penyetaraan, atau jalur vokasi/BLK. Konsultasi dengan pengurus dan Dinas Pendidikan setempat.'),
       ('Tidak punya modal wirausaha?', 'Mulai pre-order/dropship/titip jual dari komunitas sendiri; KUR tersedia setelah usaha berjalan.'),
       ('Takut ditolak?', 'Pilih 1 utama + 1 cadangan; penolakan = data, bukan akhir.'),
       ('Orang tua ingin saya jadi ustadz, saya mau kerja?', 'Komunikasikan rencana konkret + bukti hasil (mis. kerja 2-3 tahun lalu ngajar paruh waktu).'),
       ('Boleh pilih 2 jalur?', 'Boleh: 1 utama + 1 sampingan/cadangan. Hindari 2 jalur besar sekaligus di awal.'),
       ('Kapan waktu ideal memutuskan?', 'Idealnya sebelum wisuda. Wajar eksplorasi 1-3 bulan setelah lulus dengan checklist di atas.')]
for q, a in FAQ:
    pdf.set_font('helvetica', 'B', 9.5); pdf.set_text_color(*PRIMARY); pdf.set_x(14)
    pdf.multi_cell(0, 5.5, S('Q: ' + q))
    pdf.set_text_color(*DARK)
    body(S('A: ' + a), 9)
body('Disusun 17 Nov 2026. Terinspirasi dari roadmap.sh. Konten panduan umum, bukan fatwa atau nasihat karier personal. Lisensi: MIT (dokumen ini); referensi inspirasi: roadmap.sh (Kamran Ahmed).')

pdf.output('roadmap_santri.pdf')
print('PDF selesai: roadmap_santri.pdf, halaman:', pdf.page_no())

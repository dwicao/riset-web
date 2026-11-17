#!/usr/bin/env python3
"""Generate laporan_gaji_teknologi_indonesia.pdf (fpdf2 + matplotlib charts)."""
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

df = pd.read_csv('data_bersih.csv')
b = df[df['base_tahun'] >= 12_000_000].copy()
N = len(df); NB = len(b)

def jt(v):  return f'Rp {v/1e6:,.0f} jt'.replace(',', '.')
def pct(x): return f'{x:.1f}%'

med_base = b['base_tahun'].median(); p25 = b['base_tahun'].quantile(.25); p75 = b['base_tahun'].quantile(.75)
mean_base = b['base_tahun'].mean(); max_base = b['base_tahun'].max()
med_total = b['total_kompensasi'].median()
pct_allow = (b['allowance_tahun'] > 0).mean() * 100
pct_rsu = (b['rsu_tahun'] > 0).mean() * 100
female = (df['jenis_kelamin'] == 'Perempuan').mean() * 100
med_exp = df['pengalaman_tahun'].median(); med_umur = df['umur'].median()

g_med = b.groupby('jenis_kelamin')['base_tahun'].median()
med_l = g_med.get('Laki-Laki', 0); med_p = g_med.get('Perempuan', 0)
edu_med = b.groupby('pendidikan')['base_tahun'].median() / 1e6
kotas = df['kota'].value_counts()
jkt = int(kotas.get('Jakarta', 0))
cov = df['coverage_asuransi'].value_counts()
cov_no = int(cov.get('Tidak ada', 0)); cov_bpjs = int(cov.get('BPJS saja', 0)); cov_both = int(cov.get('BPJS + Swasta', 0))

PRIMARY = (62, 106, 225); DARK = (35, 38, 45); GREY = (120, 126, 138)

class Report(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=17)
        self.set_margins(16, 15, 16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('helvetica', 'I', 8); self.set_text_color(*GREY)
        self.cell(120, 8, 'Survei Gaji Teknologi Indonesia - Laporan Analisis', new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(58, 8, f'Hal. {self.page_no()}', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*PRIMARY); self.set_line_width(0.5)
        self.line(16, 15.5, 194, 15.5)
        self.set_text_color(0, 0, 0); self.ln(2)

def h1(pdf, text, num):
    pdf.ln(2)
    pdf.set_fill_color(*PRIMARY); pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 13)
    pdf.cell(0, 9, f'  {num}.  {text}', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3); pdf.set_text_color(*DARK)

def h2(pdf, text):
    pdf.ln(1.5); pdf.set_font('helvetica', 'B', 10.5); pdf.set_text_color(*PRIMARY)
    pdf.cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*DARK); pdf.ln(1)

def body(pdf, text):
    pdf.set_x(16)
    pdf.set_font('helvetica', '', 9.5)
    pdf.multi_cell(0, 5, text)
    pdf.ln(1)

def bullets(pdf, items):
    pdf.set_font('helvetica', '', 9.5)
    for it in items:
        pdf.set_x(16)
        pdf.multi_cell(0, 5, '-  ' + it)
    pdf.ln(1)

def img(pdf, path, w=150, caption=None):
    pdf.image(path, x=(210 - w) / 2, w=w)
    if caption:
        pdf.set_font('helvetica', 'I', 8); pdf.set_text_color(*GREY)
        pdf.cell(0, 5, caption, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(*DARK)
    pdf.ln(2)

def table(pdf, headers, rows, widths):
    pdf.set_font('helvetica', 'B', 8.5)
    pdf.set_fill_color(*PRIMARY); pdf.set_text_color(255, 255, 255)
    for h, w in zip(headers, widths):
        pdf.cell(w, 7, ' ' + h, fill=True)
    pdf.ln()
    pdf.set_font('helvetica', '', 8.5); pdf.set_text_color(*DARK)
    fill = False
    for row in rows:
        pdf.set_fill_color(240, 243, 255)
        for i, (v, w) in enumerate(zip(row, widths)):
            pdf.cell(w, 6.5, ' ' + str(v), fill=fill)
        pdf.ln()
        fill = not fill
    pdf.ln(2)

pdf = Report()

# ------------------------------------------------------------- COVER
pdf.add_page()
pdf.set_fill_color(*PRIMARY); pdf.rect(0, 0, 210, 78, style='F')
pdf.set_text_color(255, 255, 255)
pdf.set_xy(16, 18); pdf.set_font('helvetica', 'B', 25)
pdf.multi_cell(178, 11, 'Survei Gaji\nTeknologi Indonesia')
pdf.set_xy(16, 46); pdf.set_font('helvetica', '', 12)
pdf.multi_cell(178, 7, 'Analisis 416 responden: base salary, bonus, RSU, posisi,\npengalaman, pendidikan, gender, dan asuransi (Feb 2020 - Jan 2022)')
pdf.set_text_color(*DARK)
pdf.set_xy(16, 92); pdf.set_font('helvetica', 'B', 10)
pdf.cell(0, 6, 'Ringkasan Eksekutif', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', '', 9.5)
bullets(pdf, [
    f'416 responden mengisi survei; 403 isian base salary valid dipakai untuk statistik gaji (13 isian di bawah Rp 12 jt/tahun dikeluarkan).',
    f'Median base salary: {jt(med_base)}/tahun (p25 {jt(p25)} - p75 {jt(p75)}); rata-rata {jt(mean_base)}; maksimum {jt(max_base)}.',
    f'Median total kompensasi (base + bonus + RSU): {jt(med_total)}/tahun.',
    f'80.9% responden menerima allowance/bonus; 8.4% menerima RSU/stock.',
    f'88.2% responden laki-laki, 11.8% perempuan; median umur {med_umur:.0f} tahun; median pengalaman {med_exp:.0f} tahun.',
    f'Jakarta ({jkt} responden, {jkt/N*100:.0f}%) mendominasi; diikuti Bandung, Malang, Surabaya.',
])
pdf.ln(4); pdf.set_x(16)
pdf.set_font('helvetica', 'I', 8.5); pdf.set_text_color(*GREY)
pdf.multi_cell(178, 5, 'Sumber data: Google Sheets "Survei Gaji Teknologi Indonesia" (gid 1811584495), diunduh 17 Nov 2026.\nhttps://docs.google.com/spreadsheets/d/1DBE6v5nYliDCUl8IQR9b-KS9-wlkw9-Wp2K0pQqNg6o/edit\nLaporan ini dibuat otomatis: cleaning -> statistik -> chart -> PDF (fpdf2 + matplotlib).')
pdf.set_text_color(*DARK)

# ------------------------------------------------------------- 1. METODOLOGI
pdf.add_page()
h1(pdf, 'Metodologi & Sumber Data', 1)
h2(pdf, 'Sumber')
body(pdf, 'Data berasal dari Google Form survei gaji teknologi di Indonesia yang disebar lewat komunitas developer, lalu diexport ke Google Sheets (sheet gid=1811584495, 416 baris, 12 kolom). Periode pengisian: 15 Feb 2020 - 25 Jan 2022.')
h2(pdf, 'Pembersihan data')
bullets(pdf, [
    'Angka format Indonesia diparse: titik = ribuan (mis. "216.000.000" -> Rp 216.000.000), koma = desimal ("1,5" tahun pengalaman -> 1.5).',
    'Jumlah RSU dan allowance berisi "tidak ada" diubah menjadi 0.',
    'Pengalaman bernilai -1 (3 responden) dianggap 0 (fresh graduate); "6+ Tahun" -> 6; nilai negatif lain di-clip ke 0.',
    'Base salary < Rp 12 jt/tahun (13 responden, kemungkinan isian per bulan) dikeluarkan dari statistik gaji; tetap ada di data_bersih.csv dengan kolom base_valid=False.',
    'Kota dinormalkan (Jakarta & variannya -> Jakarta; Kota Malang/Malang -> Malang; Singapore/Singapura -> Singapura).',
    'Pendidikan dinormalkan ke SMA / SMK / Diploma (D3/D4) / S1 / S2 / Lainnya (S1=268+, SMK=42, S2=34, dst.).',
    'Posisi/Jabatan dikelompokkan ke 15 kelompok peran (rules keyword: front/back/fullstack/mobile/data/devops/qa/...) dan 5 level (Intern, Junior, Mid/Staff, Senior, Lead/Manajerial).',
    'Coverage Asuransi (teks bebas) dikategorikan: Tidak ada / BPJS saja / BPJS + Swasta / Swasta saja / Ada (detail tidak jelas) / lainnya.',
])
h2(pdf, 'Definisi')
bullets(pdf, [
    'Total kompensasi = base salary + allowance/bonus + RSU/stock.',
    'Statistik gaji (median, p25/p75, mean, max) memakai n=403 (base valid). Statistik profil (gender, kota, asuransi, pendidikan) memakai n=416.',
    'Median dipakai sebagai ukuran utama karena distribusi gaji sangat miring (skewed) ke kanan.',
])

# ------------------------------------------------------------- 2. PROFIL
h1(pdf, 'Profil Responden', 2)
body(pdf, f'Responden: {N} orang; {female:.1f}% perempuan, {100-female:.1f}% laki-laki. Median umur {med_umur:.0f} tahun, median pengalaman kerja {med_exp:.0f} tahun.')
table(pdf, ['Metrik', 'Nilai'], [
    ['Jumlah responden', str(N)],
    ['Periode pengisian', '2020-02-15 s/d 2022-01-25'],
    ['Median umur', f'{med_umur:.0f} tahun (rentang 19-50)'],
    ['Median pengalaman', f'{med_exp:.0f} tahun'],
    ['Perempuan', f'49 ({female:.1f}%)'],
    ['S1 / SMK / S2', '268 / 42 / 34 responden'],
], [70, 100])
img(pdf, 'charts/05_kota.png', 165, 'Gambar 1. Top 8 kota domisili responden (batang) dan median base salary (garis).')
body(pdf, f'Jakarta mendominasi sampel ({jkt} responden, {jkt/N*100:.1f}%) - mencerminkan konsentrasi kantor pusat startup/teknologi. Median gaji Jakarta lebih tinggi daripada Malang/Surabaya, tetapi lonjakan di Singapura (median ~Rp 780 jt) perlu dibaca hati-hati: kemungkinan isian tersebut memakai SGD yang tercantum tanpa konversi.')

# ------------------------------------------------------------- 3. KOMPENSASI
h1(pdf, 'Kompensasi: Base, Bonus, dan RSU', 3)
h2(pdf, 'Distribusi base salary')
img(pdf, 'charts/01_distribusi_base.png', 165, 'Gambar 2. Distribusi base salary per tahun (403 isian valid, sumbu x dipotong di Rp 800 jt).')
body(pdf, f'Median {jt(med_base)} per tahun - setara Rp {med_base/12e6:,.1f} jt per bulan. Rentang p25-p75: {jt(p25)} - {jt(p75)}. Distribusi sangat miring ke kanan: masih ada ekor outlier hingga Rp 3,15 miliar/tahun (kemungkinan C-level/direksi). Karena itu median jauh lebih representatif daripada mean ({jt(mean_base)}).'.replace(',', '.'))
h2(pdf, 'Pengalaman kerja')
img(pdf, 'charts/02_base_vs_pengalaman.png', 165, 'Gambar 3. Median base salary vs tahun pengalaman (9 = 9+).')
body(pdf, 'Pola naik umum: 0 thn (92 jt) -> 5-6 thn (~240 jt) -> 9+ thn (400 jt). Sedikit anomali di 7-8 tahun (162/159 jt, n=20/12) kemungkinan karena komposisi responden saat itu lebih banyak mid-level di luar Jakarta; sampel kecil membuat median fluktuatif.')
h2(pdf, 'Bonus & RSU')
img(pdf, 'charts/07_komposisi.png', 120, 'Gambar 4. Komposisi agregat total kompensasi.')
bullets(pdf, [
    f'{pct(pct_allow)} responden menerima allowance/bonus (rata-rata Rp 91 jt/tahun; median Rp 30 jt/tahun).',
    f'{pct(pct_rsu)} responden menerima RSU/stock/stock option; komposisi agregatnya 22.5% dari total kompensasi - didorong segelintir paket sangat besar (maks Rp 15 miliar).',
    f'Median total kompensasi: {jt(med_total)}/tahun.',
])
h2(pdf, 'Ukuran perusahaan')
img(pdf, 'charts/10_ukuran_perusahaan.png', 165, 'Gambar 5. Median base salary vs jumlah karyawan tech di perusahaan.')
body(pdf, 'Pola U terbalik yang menarik: perusahaan kecil (1-10 karyawan tech, umumnya startup seed/early) membayar median Rp 204 jt - bahkan lebih tinggi dari perusahaan menengah (51-200, Rp 104 jt). Perusahaan >1000 karyawan tech membayar Rp 214 jt. Startup tahap awal cenderung membayar mahal untuk talenta inti, sementara skala menengah paling menekan biaya.')

# ------------------------------------------------------------- 4. POSISI & LEVEL
h1(pdf, 'Berdasarkan Posisi & Level', 4)
img(pdf, 'charts/09_level_posisi.png', 165, 'Gambar 6. Median base salary per level (Intern n=1, hati-hati baca).')
img(pdf, 'charts/06_posisi.png', 165, 'Gambar 7. Median base salary per kelompok posisi (n = jumlah responden per kelompok).')
body(pdf, 'Management/Leadership memimpin (median 360 jt, n=61, umumnya Manager/Head/C-level/Lead), disusul Data (200 jt) dan Software Engineer umum (180 jt). Di ujung bawah: Web (54 jt), IT Support/General (62 jt), QA/Testing (78 jt). Catatan: kelompok Security hanya n=3 - jangan digeneralisasi.')

# ------------------------------------------------------------- 5. GENDER
h1(pdf, 'Gender Pay Gap', 5)
img(pdf, 'charts/03_gaji_per_gender.png', 125, 'Gambar 8. Base salary per jenis kelamin (boxplot; titik = mean).')
body(pdf, f'Median Laki-Laki {jt(med_l)} vs Perempuan {jt(med_p)} - selisih sekitar {(1-med_p/med_l)*100:.1f}% lebih rendah untuk perempuan. Namun jangan langsung disimpulkan sebagai gap murni: sampel perempuan hanya 49 (11.8%), mayoritas berada di gaji < Rp 300 jt, dan belum dikontrol terhadap pengalaman/level/kota. Data ini cukup untuk bendera merah, belum cukup untuk angka gap yang final.')

# ------------------------------------------------------------- 6. PENDIDIKAN
h1(pdf, 'Pendidikan', 6)
img(pdf, 'charts/04_gaji_per_pendidikan.png', 155, 'Gambar 9. Median base salary per pendidikan terakhir.')
body(pdf, 'Pola tidak sepenuhnya monoton: S1 (150 jt) di atas SMK (70 jt) dan D3/D4 (108 jt), S2 (240 jt) tertinggi. SMA (110 jt) justru di atas SMK - kemungkinan karena responden SMA lebih sering senior/self-taught. Konfunder terbesar adalah pengalaman & level; pendidikan bukan satu-satunya penentu.')

# ------------------------------------------------------------- 7. ASURANSI
h1(pdf, 'Coverage Asuransi Kesehatan', 7)
img(pdf, 'charts/08_asuransi.png', 165, 'Gambar 10. Kategori coverage asuransi yang ditawarkan perusahaan (n=416).')
bullets(pdf, [
    f'{cov_no} responden ({cov_no/N*100:.1f}%) menyatakan perusahaan TIDAK menawarkan asuransi.',
    f'{cov_bpjs} responden ({cov_bpjs/N*100:.1f}%): BPJS saja; {cov_both} responden ({cov_both/N*100:.1f}%): BPJS + swasta/full.',
    'Sisanya: ada tapi detail tidak jelas (51), lainnya (50), nilai manfaat (22), swasta saja (3) - jawaban teks bebas sulit diverifikasi.',
    'Kesimpulan praktis: saat negosiasi, asuransi layak jadi komponen total reward, bukan sekadar base salary.',
])

# ------------------------------------------------------------- 8. KETERBATASAN
h1(pdf, 'Keterbatasan & Catatan', 8)
bullets(pdf, [
    'Bukan sampel acak: survei sebar komunitas (self-selection bias), condong ke pekerja laki-laki S1 di Jakarta dan perusahaan startup/teknologi.',
    'Data 2020-2022 (era pre-GenAI). Pasar gaji tech saat ini kemungkinan lebih tinggi; angka di sini adalah baseline historis, bukan benchmark 2026.',
    'Gaji self-reported: bisa overstatement/understatement; tidak ada verifikasi slip gaji.',
    'Outlier ekstrem (base sampai Rp 3,15 miliar; RSU sampai Rp 15 miliar) menarik mean jauh di atas median.',
    'Jawaban asuransi = teks bebas; kategori "Ada (detail tidak jelas)" besar (12.3%).',
    'Responden Singapura mungkin mengisi dalam SGD tanpa konversi; jangan bandingkan langsung dengan rupiah.',
    '13 isian base < Rp 12 jt/tahun dikeluarkan dari statistik gaji (kemungkinan isian per bulan).',
])
h2(pdf, 'Rekomendasi penggunaan')
bullets(pdf, [
    'Untuk negosiasi gaji: pakai p25-p75 (Rp 72-300 jt) sebagai jangkar, bukan mean.',
    'Untuk perusahaan: bandingkan dengan median per level & kota, bukan angka global.',
    'Untuk penelitian lanjutan: ambil sampel baru (2024-2026), kontrol pengalaman & kota, sertakan gaji pokok vs bonus terpisah, dan konversi mata uang asing.',
])

# ------------------------------------------------------------- 9. LAMPIRAN
h1(pdf, 'Lampiran: File & Reproduksi', 9)
body(pdf, 'Seluruh angka pada laporan ini dapat direproduksi dari folder gaji-teknologi/:')
table(pdf, ['File', 'Isi'], [
    ['survei_mentah.csv', 'Export asli Google Sheets (48 KB, 416 baris)'],
    ['data_bersih.csv', 'Hasil cleaning + kolom turunan (total_kompensasi, kelompok_posisi, ...)'],
    ['analisis.py', 'Pipeline cleaning + statistik (stats_ringkasan.json)'],
    ['make_charts_gaji.py', '10 chart PNG (charts/)'],
    ['build_pdf.py', 'Script pembuat PDF ini'],
    ['ringkasan_gaji_teknologi.md', 'Catatan analisis singkat'],
], [62, 108])
body(pdf, 'Cara menjalankan ulang: python3 analisis.py && python3 make_charts_gaji.py && python3 build_pdf.py')
pdf.ln(4)
pdf.set_font('helvetica', 'I', 8); pdf.set_text_color(*GREY)
pdf.multi_cell(0, 4.5, 'Dibuat otomatis pada 17 November 2026. Lisensi data survei mengikuti pemilik Google Sheets; chart & laporan berlisensi bebas pakai dengan atribusi (CC-BY 4.0).')

pdf.output('laporan_gaji_teknologi_indonesia.pdf')
print('PDF selesai: laporan_gaji_teknologi_indonesia.pdf, hal:', pdf.page_no())

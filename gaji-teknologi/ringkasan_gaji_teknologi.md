# Analisis Survei Gaji Teknologi Indonesia (2020–2022)

**Sumber:** Google Sheets — https://docs.google.com/spreadsheets/d/1DBE6v5nYliDCUl8IQR9b-KS9-wlkw9-Wp2K0pQqNg6o/edit?gid=1811584495 (gid 1811584495), diunduh 17 Nov 2026.
**Isi:** 416 jawaban Google Form (15 Feb 2020 – 25 Jan 2022): base salary setahun, allowance/bonus, RSU, posisi, pengalaman, pendidikan, kota, asuransi.

## Temuan utama
- Median base salary (n=403 valid): **Rp 144 jt/tahun** (p25 Rp 72 jt – p75 Rp 300 jt); rata-rata Rp 242 jt; maks Rp 3,15 miliar.
- Median total kompensasi (base+bonus+RSU): **Rp 216 jt/tahun**.
- 80,9% dapat allowance/bonus; 8,4% dapat RSU (agregat 22,5% dari total kompensasi karena segelintir paket besar).
- Gender: 88,2% laki-laki; median perempuan (Rp 132 jt) ~8,3% di bawah laki-laki (Rp 144 jt) — beda belum dikontrol pengalaman/level.
- Pendidikan: S2 tertinggi (240 jt), S1 150 jt, D3/D4 108 jt, MA 110 jt, SMK 70 jt.
- Posisi: Management/Leadership 360 jt > Data 200 jt > SWE umum 180 jt > ... > Web 54 jt.
- 87,8% bekerja/menetap di Jakarta-Bandung-Malang (Jakarta sendiri 247 responden / 59,4%).
- Asuransi: 31,7% tidak ada; 31,7% BPJS saja; 6,3% BPJS+swasta; sisanya ambigu (teks bebas).
- 13 isian base < Rp 12 jt/tahun dikeluarkan dari statistik gaji (kemungkinan isian per bulan).

## File
- `survei_mentah.csv` — export asli Google Sheets
- `data_bersih.csv` — hasil cleaning (+`total_kompensasi`, `kelompok_posisi`, `level_posisi`, `coverage_asuransi`, `base_valid`)
- `analisis.py` → cleaning & `stats_ringkasan.json`
- `make_charts_gaji.py` → `charts/01..10*.png`
- `build_pdf.py` → `laporan_gaji_teknologi_indonesia.pdf` (8 hal)

## Reproduksi
```bash
python3 analisis.py && python3 make_charts_gaji.py && python3 build_pdf.py
```

## Catatan penting
Data self-reported, era 2020–2022 (pre-GenAI), sampel komunitas (bukan acak), gaji dalam rupiah kecuali Singapura (mungkin SGD tanpa konversi). Jangan dipakai sebagai benchmark tunggal tanpa pembaruan sampel.

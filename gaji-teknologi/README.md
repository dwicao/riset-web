# gaji-teknologi

Analisis **Survei Gaji Teknologi Indonesia** (Feb 2020 – Jan 2022, 416 responden dari Google Form/Sheets).

Sumber data: [Google Sheets (gid 1811584495)](https://docs.google.com/spreadsheets/d/1DBE6v5nYliDCUl8IQR9b-KS9-wlkw9-Wp2K0pQqNg6o/edit?gid=1811584495)

## Hasil utama

- Median base salary: **Rp 144 jt/tahun** (p25 Rp 72 – p75 Rp 300)
- Median total kompensasi (base + bonus + RSU): **Rp 216 jt/tahun**
- Top posisi: Management/Leadership Rp 360 jt; Data Rp 200 jt; SWE umum Rp 180 jt
- Gender: perempuan median Rp 132 jt vs laki-laki Rp 144 jt (kontroversial, belum dikontrol pengalaman)
- 31,7% perusahaan tidak menawarkan asuransi kesehatan

## File

| File | Fungsi |
|---|---|
| `survei_mentah.csv` | Export asli Google Sheets |
| `data_bersih.csv` | Hasil cleaning + kolom turunan |
| `analisis.py` | Cleaning + `stats_ringkasan.json` |
| `make_charts_gaji.py` | 10 chart → `charts/*.png` |
| `build_pdf.py` | Laporan PDF → `laporan_gaji_teknologi_indonesia.pdf` |
| `ringkasan_gaji_teknologi.md` | Catatan analisis |

## Menjalankan ulang

```bash
python3 analisis.py && python3 make_charts_gaji.py && python3 build_pdf.py
```

Lihat `laporan_gaji_teknologi_indonesia.pdf` untuk metodologi, chart lengkap, dan keterbatasan.

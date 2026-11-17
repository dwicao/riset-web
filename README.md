# riset-web

Kumpulan analisis & proyek belajar, dirapikan per project. Setiap folder berisi data, skrip reproduksi, chart, dan laporan.

## Projects

| Folder | Isi | Hasil |
|---|---|---|
| [`gaji-teknologi/`](gaji-teknologi/) | Analisis Survei Gaji Teknologi Indonesia 2020–2022 (416 responden) | `gaji-teknologi/laporan_gaji_teknologi_indonesia.pdf` · **Live:** https://gaji-teknologi.surge.sh |
| [`soal-matan-santri/`](soal-matan-santri/) | 100 Soal Pilihan Ganda — Kitab Zikir dan Adab (untuk santri) | `soal-matan-santri/soal_zikir_adab_100pg.pdf` · **Live:** https://soal-matan-santri.surge.sh |
| [`roadmap-santri/`](roadmap-santri/) | Peta jalan santri setelah lulus pondok: 14 jalur, interaktif ala roadmap.sh | `roadmap-santri/index.html` · **Live:** https://roadmap-santri.surge.sh |

## Aturan main

- Setiap project punya folder sendiri: `data*.csv`, `charts/`, `laporan*.pdf|md`, skrip `.py`, dan README/ringkasan.
- Jangan commit data mentah yang sensitif; data survei gaji direpo ini bersifat anonim agregat.

## Reproduksi cepat

```bash
cd gaji-teknologi && python3 analisis.py && python3 make_charts_gaji.py && python3 build_pdf.py
cd ../soal-matan-santri && python3 generate_soal.py
cd ../roadmap-santri && python3 build_pdf.py
```

Terakhir diperbarui: 17 Nov 2026.

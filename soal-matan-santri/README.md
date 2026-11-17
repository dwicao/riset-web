# soal-matan-santri

**Live:** https://soal-matan-santri.surge.sh

**100 Soal Pilihan Ganda — Kitab Zikir dan Adab** (Kumpulan Matan untuk Penuntut Ilmu, Tingkat Pertama), paket latihan untuk santri, output PDF.

## Tentang soal

- 100 PG (A–D), 1 jawaban benar per soal, **kunci jawaban di halaman terakhir** PDF.
- Dibagi 10 bagian tematik mengikuti struktur kitab: Keutamaan (8) · Bersuci (4) · Salat (21) · Sakit (5) · Jenazah & Musibah (9) · Safar & Haji (9) · Rumah, Makanan & Pakaian (10) · Malam, Tidur & Mimpi (14) · Zikir Pagi/Petang & Zikir Bebas (12) · Adab Sosial, Lisan & Akhlak (8).
- Setiap soal memuat **Rujukan** (perawi/kitab) agar bisa ditelusuri di kitab sumber.
- Semua jawaban diverifikasi terhadap teks kitab (terjemah Indonesia) — bukan tebakan umum.

## Sumber materi

KITAB: Zikir dan Adab (Al-Adzkar wal-Adab) — Dr. Abdul Muhsin bin Muhammad al-Qasim (Imam & Khatib Masjid Nabawi) — Serial *Mutun Thalibil 'ilm* Tingkat Pertama.
PDF sumber: https://d1.islamhouse.com/data/id/ih_books/single/id-mustawa1-pp.pdf (diunduh 17 Nov 2026, 252 hal, ditahkik ±5000 manuskrip).

> Catatan distribusi: PDF sumber & teks ekstraksi **tidak** disimpan di repo ini (hak cipta penerbit). Unduh sendiri dari tautan di atas. Konten soal & laporan di repo ini adalah karya turunan untuk pendidikan.

## File

| File | Isi |
|---|---|
| `soal_zikir_adab_100pg.pdf` | **Output utama** — 100 soal + pembahasan rujukan + kunci jawaban + rubrik skor |
| `bank_soal.py` | 100 soal (data) + definisi bagian & offset nomor |
| `generate_soal.py` | Builder PDF (fpdf2) |

## Reproduksi

```bash
python3 generate_soal.py   # menghasilkan soal_zikir_adab_100pg.pdf
```

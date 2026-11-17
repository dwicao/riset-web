#!/usr/bin/env python3
"""Hitung agregat dari data_bersih.csv -> site/data.js (untuk chart web)."""
import json
import numpy as np
import pandas as pd

df = pd.read_csv('data_bersih.csv')
b = df[df['base_tahun'] >= 12_000_000].copy()
JT = 1e6

# 1. Histogram base (bin 50 jt sampai 800+)
bins = list(range(0, 850, 50))  # 0,50,...,800
counts, edges = np.histogram(b['base_tahun'] / JT, bins=bins + [np.inf])
hist = [{'label': f'{int(e)}-{int(e)+50}', 'count': int(c)} for e, c in zip(edges[:-1], counts[:-1])]
hist[-1] = {'label': '800+', 'count': int(counts[-1])}
median_base = float(b['base_tahun'].median() / JT)

# 2. Median per tahun pengalaman (9 = 9+)
exp_med = b.groupby(b['pengalaman_tahun'].clip(upper=9).astype(int))['base_tahun'].median() / JT
exp_n = b.groupby(b['pengalaman_tahun'].clip(upper=9).astype(int))['base_tahun'].count()
pengalaman = [{'x': int(i), 'median': round(float(v), 1), 'n': int(exp_n[i])} for i, v in exp_med.items()]

# 3. Gender: median, p25, p75
def gstat(name):
    s = b[b['jenis_kelamin'] == name]['base_tahun'] / JT
    return {'median': round(float(s.median()), 1), 'p25': round(float(s.quantile(.25)), 1), 'p75': round(float(s.quantile(.75)), 1), 'n': int(len(s))}
gender = {'Laki-Laki': gstat('Laki-Laki'), 'Perempuan': gstat('Perempuan')}

# 4. Pendidikan (urut)
orden = ['SMA', 'SMK', 'Diploma (D3/D4)', 'S1', 'S2']
gm = b.groupby('pendidikan')['base_tahun'].median() / JT
gn = b.groupby('pendidikan')['base_tahun'].count()
pendidikan = [{'label': k, 'median': round(float(gm[k]), 1), 'n': int(gn[k])} for k in orden if k in gm.index]

# 5. Kota: top 8 responden + median (base valid)
top_kota = df['kota'].value_counts().head(8).index.tolist()
kota = []
for k in top_kota:
    n_all = int((df['kota'] == k).sum())
    s = b[b['kota'] == k]['base_tahun']
    kota.append({'kota': k, 'n': n_all, 'median': round(float(s.median() / JT), 1) if len(s) else 0})

# 6. Kelompok posisi (urut median)
gm = (b.groupby('kelompok_posisi')['base_tahun'].median() / JT).sort_values()
gn = b.groupby('kelompok_posisi')['base_tahun'].count().reindex(gm.index)
posisi = [{'label': k, 'median': round(float(v), 1), 'n': int(gn[k])} for k, v in gm.items()]

# 7. Komposisi agregat kompensasi
komposisi = {
    'base': round(float(b['base_tahun'].sum() / JT), 1),
    'allowance': round(float(b['allowance_tahun'].sum() / JT), 1),
    'rsu': round(float(b['rsu_tahun'].sum() / JT), 1),
}

# 8. Coverage asuransi (semua responden)
cnt = df['coverage_asuransi'].value_counts()
asuransi = [{'label': k, 'n': int(v)} for k, v in cnt.items()]

# 9. Level posisi (urut jenjang)
orden = ['Intern/Fresh Grad', 'Junior', 'Mid/Staff', 'Senior', 'Lead/Manajerial']
gm = b.groupby('level_posisi')['base_tahun'].median() / JT
gn = b.groupby('level_posisi')['base_tahun'].count()
level = [{'label': k, 'median': round(float(gm[k]), 1), 'n': int(gn[k])} for k in orden if k in gm.index]

# 10. Ukuran perusahaan
bins2 = [-1, 10, 50, 200, 1000, np.inf]
labels = ['1-10', '11-50', '51-200', '201-1000', '>1000']
kat = pd.cut(b['karyawan_tech'], bins=bins2, labels=labels)
gm = b.groupby(kat, observed=True)['base_tahun'].median() / JT
gn = b.groupby(kat, observed=True)['base_tahun'].count()
ukuran = [{'label': str(k), 'median': round(float(v), 1), 'n': int(gn[k])} for k, v in gm.items()]

data = {
    'n': int(len(df)), 'n_valid': int(len(b)),
    'periode': '2020-02-15 s/d 2022-01-25',
    'median_base': median_base,
    'p25': round(float(b['base_tahun'].quantile(.25) / JT), 1),
    'p75': round(float(b['base_tahun'].quantile(.75) / JT), 1),
    'total_median': round(float(b['total_kompensasi'].median() / JT), 1),
    'mean': round(float(b['base_tahun'].mean() / JT), 1),
    'hist': hist, 'pengalaman': pengalaman, 'gender': gender,
    'pendidikan': pendidikan, 'kota': kota, 'posisi': posisi,
    'komposisi': komposisi, 'asuransi': asuransi,
    'level': level, 'ukuran': ukuran,
}
with open('site/data.js', 'w', encoding='utf-8') as f:
    f.write('// Dibuat otomatis dari data_bersih.csv — jangan diedit manual.\n')
    f.write('const GAJI = ')
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    f.write(';\n')
print('data.js ditulis. n_valid =', data['n_valid'])

#!/usr/bin/env python3
"""Analisis Survei Gaji Teknologi Indonesia (425 responden -> 416 setelah dedup sheet).

Input : survei_mentah.csv (export Google Sheets gid=1811584495)
Output: data_bersih.csv, charts/*.png, laporan_gaji_teknologi_indonesia.pdf
"""
import re, json
from collections import Counter
import pandas as pd
import numpy as np

IN, OUT_CSV = 'survei_mentah.csv', 'data_bersih.csv'
CH = 'charts'

# ---------------------------------------------------------------- parsing
def pnum(x, desimal_koma=False):
    """Parse angka format Indonesia (titik ribuan, koma desimal)."""
    if pd.isna(x):
        return np.nan
    s = str(x).strip().lower()
    if s in ('', '-', 'tidak ada', 'none', 'null'):
        return np.nan
    if desimal_koma:
        s2 = s.replace('tahun', '').replace('+', '').strip()
        m = re.search(r'\d+([.,]\d+)?', s2)
        if m:
            return float(m.group().replace(',', '.'))
        return np.nan
    if re.fullmatch(r'[\d.]+', s):
        s2 = s.replace('.', '')
        return float(s2) if s2.isdigit() else np.nan
    return np.nan

def norm_kota(x):
    s = re.sub(r'\s+', ' ', str(x).strip().lower())
    if s.startswith(('jakarta', 'dki')):
        return 'Jakarta'
    if 'malang' in s:
        return 'Malang'
    if s in ('singapore', 'singapura'):
        return 'Singapura'
    if 'tangerang selatan' in s:
        return 'Tangerang Selatan'
    if 'remote' in s:
        return s.title()
    return s.title()

def norm_pendidikan(x):
    s = re.sub(r'\s+', ' ', str(x).strip().lower())
    s = s.replace('.', '').replace(',', ' ')
    if not s or s == 'nan':
        return 'Tidak diisi'
    if s.startswith(('s3', 'doktor')):
        return 'S3'
    if s.startswith(('s2', 'magister')):
        return 'S2'
    if s.startswith(('s1', 'sarjana', 's kom', 'skom', 'bsc', 'b sc', 'beng', 'st')):
        return 'S1'
    if 'diploma' in s or s.startswith(('d3', 'd4')):
        return 'Diploma (D3/D4)'
    if s.startswith('smk'):
        return 'SMK'
    if s.startswith(('sma', 'ma ', 'aliyah')) or s == 'ma':
        return 'SMA'
    return 'Lainnya'

def role_group(t):
    t = str(t).lower()
    if any(k in t for k in ['design', 'ui', 'ux', 'graphic']): return 'Design'
    if 'security' in t or 'pentest' in t: return 'Security'
    if 'data' in t: return 'Data'
    if any(k in t for k in ['devops', 'sre', 'infra', 'cloud', 'platform', 'sysadmin', 'network', 'ops']): return 'DevOps/Infra'
    if any(k in t for k in ['qa', 'quality', 'test', 'automation']): return 'QA/Testing'
    if any(k in t for k in ['android', 'ios', 'mobile', 'flutter', 'react native']): return 'Mobile'
    if 'front' in t: return 'Frontend'
    if 'back' in t: return 'Backend'
    if 'fullstack' in t or 'full stack' in t or 'full-stack' in t: return 'Fullstack'
    if 'web' in t: return 'Web'
    if any(k in t for k in ['cto', 'chief', 'director', 'direktur', 'head', 'manager', 'lead', 'principal', 'architect', 'vp']): return 'Management/Leadership'
    if any(k in t for k in ['product', 'project', 'scrum', 'analyst', 'business']): return 'Product/Project/Analytics'
    if any(k in t for k in ['it support', 'it staff', 'it specialist', 'support', 'helpdesk', 'technician']): return 'IT Support/General'
    if any(k in t for k in ['software', 'engineer', 'developer', 'program', 'sde', 'coding']): return 'Software Engineer (umum)'
    if any(k in t for k in ['staff', 'staf']): return 'IT Support/General'
    return 'Lainnya'

def level_group(t):
    t = str(t).lower()
    if any(k in t for k in ['intern', 'magang', 'fresh grad', 'freshgrad']): return 'Intern/Fresh Grad'
    if any(k in t for k in ['junior', 'jr', 'jr.']): return 'Junior'
    if any(k in t for k in ['senior', 'sr', 'sr.']): return 'Senior'
    if any(k in t for k in ['lead', 'principal', 'manager', 'head', 'cto', 'director', 'direktur', 'vp', 'architect']): return 'Lead/Manajerial'
    return 'Mid/Staff'

def coverage_group(x):
    s = re.sub(r'\s+', ' ', str(x).strip().lower())
    if s in ('', 'nan', '-', '0', 'tidak ada', 'tidak', 'no', 'none', 'kosong'):
        return 'Tidak ada'
    if 'bpjs' in s:
        return 'BPJS + Swasta' if any(k in s for k in ['swasta', 'all', 'full', 'lengkap', 'fwd']) else 'BPJS saja'
    if re.fullmatch(r'[\d.]+', s):
        return 'Lainnya (nilai manfaat)'
    if any(k in s for k in ['swasta', 'asuransi']):
        return 'Swasta saja'
    if any(k in s for k in ['ya', 'yes', 'ada', 'all', 'full', 'reimburse', 'lengkap']):
        return 'Ada (detail tidak jelas)'
    return 'Lainnya'

# ---------------------------------------------------------------- load & clean
df = pd.read_csv(IN)
df.columns = [c.strip() for c in df.columns]
df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
df['jenis_kelamin'] = df['Jenis Kelamin'].str.strip().str.title()
df['umur'] = df['Umur'].map(lambda v: pnum(v))
df['kota'] = df['Kota'].map(norm_kota)
df['karyawan_tech'] = df['Jumlah Karyawan Teknologi di Perusahaan'].map(pnum)
df['base_tahun'] = df['Base Salary Setahun'].map(pnum)
df['allowance_tahun'] = df['Total Allowance+Bonus Setahun'].map(pnum).fillna(0)
df['rsu_tahun'] = df['Jumlah RSU/Stock/Stock Option'].map(pnum).fillna(0)
df['pengalaman_tahun'] = df['Lama Pengalaman (Tahun)'].map(lambda v: pnum(v, desimal_koma=True)).fillna(0).clip(lower=0)
df['pendidikan'] = df['Pendidikan Terakhir'].map(norm_pendidikan)
df['kelompok_posisi'] = df['Posisi/Jabatan'].map(role_group)
df['level_posisi'] = df['Posisi/Jabatan'].map(level_group)
df['coverage_asuransi'] = df['Coverage Asuransi'].map(coverage_group)

df['total_kompensasi'] = df['base_tahun'] + df['allowance_tahun'] + df['rsu_tahun']
# base < 12jt/tahun dianggap implausibel (kemungkinan isian per bulan) -> tidak dipakai utk statistik gaji
df['base_valid'] = df['base_tahun'] >= 12_000_000
valid = df[df['base_valid']]
print('Responden:', len(df), '| base valid (>=12jt):', len(valid))
print('Median base valid (Rp):', int(valid['base_tahun'].median()))
print('Median total komp (Rp):', int(valid['total_kompensasi'].median()))

df.to_csv(OUT_CSV, index=False)

# ---------------------------------------------------------------- helper stats
def rp(n):
    return f'Rp {n/1e6:,.0f} jt'.replace(',', '.')

stats = {
    'n': int(len(df)),
    'periode': f"{df['Timestamp'].min().date()} s/d {df['Timestamp'].max().date()}",
    'base_valid_n': int(len(valid)),
    'base_median': float(valid['base_tahun'].median()),
    'base_mean': float(valid['base_tahun'].mean()),
    'base_p25': float(valid['base_tahun'].quantile(.25)),
    'base_p75': float(valid['base_tahun'].quantile(.75)),
    'base_max': float(valid['base_tahun'].max()),
    'total_median': float(valid['total_kompensasi'].median()),
    'pct_allowance_gt0': float((valid['allowance_tahun'] > 0).mean() * 100),
    'pct_rsu_gt0': float((valid['rsu_tahun'] > 0).mean() * 100),
    'female_pct': float((df['jenis_kelamin'] == 'Perempuan').mean() * 100),
    'exp_median': float(df['pengalaman_tahun'].median()),
    'umur_median': float(df['umur'].median()),
}
with open('stats_ringkasan.json', 'w') as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print(json.dumps(stats, indent=2))

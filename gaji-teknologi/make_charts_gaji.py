#!/usr/bin/env python3
"""Chart untuk laporan Survei Gaji Teknologi Indonesia."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches

df = pd.read_csv('data_bersih.csv')
base_valid = df[df['base_tahun'] >= 12_000_000].copy()
C = {'utama': '#3E6AE1', 'aksen': '#E4572E', 'hijau': '#4C9F38', 'emas': '#F2A104', 'ungu': '#B54494', 'teal': '#5FB8A6', 'abu': '#8A8F98'}

def style(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, fontsize=12.5, fontweight='bold', pad=10)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    ax.grid(axis='x' if xlabel is None else 'y', linestyle=':', alpha=.5)
    ax.spines[['top', 'right']].set_visible(False)

def rp_axis(ax):
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v/1e6:,.0f}'))

# 1. Distribusi base salary (valid) -------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.6))
base_m = base_valid['base_tahun'] / 1e6
ax.hist(base_m.clip(upper=800), bins=40, color=C['utama'], edgecolor='white')
med = base_valid['base_tahun'].median() / 1e6
ax.axvline(med, color=C['aksen'], lw=2, ls='--')
ax.text(med + 8, ax.get_ylim()[1] * .92, f'Median = Rp {med:.0f} jt', color=C['aksen'], fontweight='bold')
style(ax, 'Distribusi Base Salary per Tahun (n=%d, dipotong di Rp 800 jt)' % len(base_valid), 'Base salary (Rp juta)', 'Jumlah responden')
plt.tight_layout(); plt.savefig('charts/01_distribusi_base.png', dpi=150); plt.close()

# 2. Median base per tahun pengalaman ------------------------------------
g = base_valid.groupby(base_valid['pengalaman_tahun'].clip(upper=9).astype(int))['base_tahun']
med = g.median() / 1e6; n = g.count()
fig, ax = plt.subplots(figsize=(10, 4.6))
bars = ax.bar(med.index.astype(str), med.values, color=C['hijau'])
for b, v, nn in zip(bars, med.values, n.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f'{v:.0f}\n(n={nn})', ha='center', fontsize=8)
ax.set_ylim(0, med.max() * 1.25)
style(ax, 'Median Base Salary per Tahun Pengalaman', 'Lama pengalaman (tahun; 9 = 9+)', 'Median base (Rp juta)')
plt.tight_layout(); plt.savefig('charts/02_base_vs_pengalaman.png', dpi=150); plt.close()

# 3. Gaji per jenis kelamin ----------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.8))
groups = ['Laki-Laki', 'Perempuan']
data = [base_valid[base_valid['jenis_kelamin'] == g]['base_tahun'] / 1e6 for g in groups]
bp = ax.boxplot(data, tick_labels=groups, patch_artist=True, showmeans=True)
for patch, c in zip(bp['boxes'], [C['utama'], C['ungu']]):
    patch.set_facecolor(c); patch.set_alpha(.75)
ax.set_ylim(0, 800)
for i, gname in enumerate(groups):
    sub = base_valid[base_valid['jenis_kelamin'] == gname]['base_tahun']
    mv = sub.median() / 1e6; p75 = sub.quantile(.75) / 1e6
    ax.text(i + 1, p75 + 25, f'median {mv:.0f} jt', ha='center', fontweight='bold', fontsize=9)
style(ax, 'Base Salary per Jenis Kelamin (y dipotong 800 jt)', ylabel='Base salary (Rp juta)')
plt.tight_layout(); plt.savefig('charts/03_gaji_per_gender.png', dpi=150); plt.close()

# 4. Median base per pendidikan -------------------------------------------
orden = ['SMA', 'SMK', 'Diploma (D3/D4)', 'S1', 'S2', 'S3']
g = base_valid.groupby('pendidikan')['base_tahun']
med = g.median() / 1e6; n = g.count()
med = med.reindex([o for o in orden if o in med.index]); n = n.reindex(med.index)
fig, ax = plt.subplots(figsize=(9, 4.6))
bars = ax.bar(med.index, med.values, color=C['emas'])
for b, v, nn in zip(bars, med.values, n.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f'{v:.0f} (n={nn})', ha='center', fontsize=8.5)
ax.set_ylim(0, med.max() * 1.22)
style(ax, 'Median Base Salary per Pendidikan Terakhir', ylabel='Median base (Rp juta)')
plt.tight_layout(); plt.savefig('charts/04_gaji_per_pendidikan.png', dpi=150); plt.close()

# 5. Kota: responden + median base ----------------------------------------
top_kota = df['kota'].value_counts().head(8).index.tolist()
sub = base_valid[base_valid['kota'].isin(top_kota)]
gn = df[df['kota'].isin(top_kota)].groupby('kota').size().reindex(top_kota)
gm = sub.groupby('kota')['base_tahun'].median().reindex(top_kota) / 1e6
fig, ax = plt.subplots(figsize=(10.5, 4.8))
ax.bar(gn.index, gn.values, color=C['utama'], alpha=.85, label='Jumlah responden')
ax.set_ylabel('Jumlah responden')
ax2 = ax.twinx()
ax2.plot(gm.index, gm.values, color=C['aksen'], marker='o', lw=2, label='Median base (Rp jt)')
ax2.set_ylabel('Median base (Rp juta)'); ax2.spines[['top']].set_visible(False)
ax.set_title('Top 8 Kota Domisili Responden & Median Base Salary', fontsize=12.5, fontweight='bold')
plt.xticks(rotation=20, ha='right')
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='lower right')
plt.tight_layout(); plt.savefig('charts/05_kota.png', dpi=150); plt.close()

# 6. Median base per kelompok posisi ---------------------------------------
g = base_valid.groupby('kelompok_posisi')['base_tahun']
med = (g.median() / 1e6).sort_values(); n = g.count().reindex(med.index)
fig, ax = plt.subplots(figsize=(10, 5.6))
bars = ax.barh(med.index, med.values, color=C['teal'])
for b, v, nn in zip(bars, med.values, n.values):
    ax.text(v + 3, b.get_y() + b.get_height() / 2, f'{v:.0f} jt (n={nn})', va='center', fontsize=8.5)
ax.set_xlim(0, med.max() * 1.28)
style(ax, 'Median Base Salary per Kelompok Posisi', 'Median base (Rp juta)')
plt.tight_layout(); plt.savefig('charts/06_posisi.png', dpi=150); plt.close()

# 7. Komposisi total kompensasi (agregat) ----------------------------------
sums = [base_valid['base_tahun'].sum(), base_valid['allowance_tahun'].sum(), base_valid['rsu_tahun'].sum()]
fig, ax = plt.subplots(figsize=(6.8, 5.2))
ax.pie(sums, labels=['Base salary', 'Allowance/Bonus', 'RSU/Stock'], autopct='%1.1f%%',
       startangle=90, colors=[C['utama'], C['emas'], C['ungu']], wedgeprops=dict(width=0.42))
ax.set_title('Komposisi Agregat Total Kompensasi\n(n=%d responden dengan base valid)' % len(base_valid), fontsize=12, fontweight='bold')
plt.tight_layout(); plt.savefig('charts/07_komposisi.png', dpi=150); plt.close()

# 8. Coverage asuransi ------------------------------------------------------
cnt = df['coverage_asuransi'].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(9.5, 5))
bars = ax.barh(cnt.index, cnt.values, color=C['utama'])
for b, v in zip(bars, cnt.values):
    ax.text(v + 1.5, b.get_y() + b.get_height() / 2, f'{v} ({v/len(df)*100:.1f}%)', va='center', fontsize=9)
ax.set_xlim(0, cnt.max() * 1.22)
style(ax, 'Coverage Asuransi yang Ditawarkan Perusahaan (n=%d)' % len(df), xlabel='Jumlah responden')
plt.tight_layout(); plt.savefig('charts/08_asuransi.png', dpi=150); plt.close()

# 9. Level posisi vs median base -------------------------------------------
orden = ['Intern/Fresh Grad', 'Junior', 'Mid/Staff', 'Senior', 'Lead/Manajerial']
g = base_valid.groupby('level_posisi')['base_tahun']
med = (g.median() / 1e6).reindex([o for o in orden if o in g.median().index]); n = g.count().reindex(med.index)
fig, ax = plt.subplots(figsize=(9.5, 4.6))
bars = ax.bar(med.index, med.values, color=C['utama'])
for b, v, nn in zip(bars, med.values, n.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f'{v:.0f}\n(n={nn})', ha='center', fontsize=8)
ax.set_ylim(0, med.max() * 1.25)
style(ax, 'Median Base Salary per Level Posisi', ylabel='Median base (Rp juta)')
plt.tight_layout(); plt.savefig('charts/09_level_posisi.png', dpi=150); plt.close()

# 10. Ukuran perusahaan vs median base --------------------------------------
bins = [-1, 10, 50, 200, 1000, np.inf]
labels = ['1-10', '11-50', '51-200', '201-1000', '>1000']
kat = pd.cut(base_valid['karyawan_tech'], bins=bins, labels=labels)
g = base_valid.groupby(kat, observed=True)['base_tahun']
med = g.median() / 1e6; n = g.count()
fig, ax = plt.subplots(figsize=(9.5, 4.6))
bars = ax.bar(med.index.astype(str), med.values, color=C['hijau'])
for b, v, nn in zip(bars, med.values, n.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f'{v:.0f}\n(n={nn})', ha='center', fontsize=8)
ax.set_ylim(0, med.max() * 1.25)
style(ax, 'Median Base Salary per Jumlah Karyawan Tech di Perusahaan', 'Karyawan teknologi di perusahaan', 'Median base (Rp juta)')
plt.tight_layout(); plt.savefig('charts/10_ukuran_perusahaan.png', dpi=150); plt.close()

print('Charts selesai.')

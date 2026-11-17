#!/usr/bin/env python3
"""Ekspor 100 soal dari bank_soal.py -> site/soal.js (format web)."""
import json
import sys
sys.path.insert(0, '.')
from bank_soal import SECTIONS, ALL

BAGIAN = [{'key': k, 'nama': n, 'jumlah': len(qs)} for k, n, qs, _ in SECTIONS]
soal = []
num = 0
for key, nama, qs, offset in SECTIONS:
    for soal_teks, opsi, kunci, rujukan in qs:
        num += 1
        soal.append({
            'n': num,
            'bagian': key,
            'soal': soal_teks,
            'opsi': opsi,
            'jawaban': kunci,   # 0-3
            'rujukan': rujukan,
        })

payload = {'bagian': BAGIAN, 'soal': soal}
with open('site/soal.js', 'w', encoding='utf-8') as f:
    f.write('// Dibuat otomatis dari bank_soal.py — jangan diedit manual.\n')
    f.write('const SOAL = ')
    f.write(json.dumps(payload, ensure_ascii=False, separators=(',', ':')))
    f.write(';\n')
print('soal.js ditulis:', len(soal), 'soal,', len(BAGIAN), 'bagian')

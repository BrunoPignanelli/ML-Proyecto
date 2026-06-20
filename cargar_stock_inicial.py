"""
cargar_stock_inicial.py
-----------------------
Script one-time: carga el stock inicial desde Libro1.xlsx a la tabla `stock` de Supabase.

Uso:
    python cargar_stock_inicial.py

Re-ejecutable: usa UPSERT (ON CONFLICT DO UPDATE) — seguro correrlo varias veces.

Requiere en .env (o como variable de entorno):
    SUPABASE_URL=https://xxxx.supabase.co
    SUPABASE_SERVICE_KEY=eyJ...   ← service_role key (NO la anon key)

La service_role key se encuentra en:
    Supabase dashboard → Settings → API → Project API keys → service_role
"""
import openpyxl
import json
import os
import math
import urllib.request
import urllib.error

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SUPABASE_URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')

if not SUPABASE_URL:
    raise SystemExit("ERROR: SUPABASE_URL no está configurado en .env")
if not SUPABASE_SERVICE_KEY:
    raise SystemExit("ERROR: SUPABASE_SERVICE_KEY no está configurado en .env\n"
                     "Obtenerlo en: Supabase dashboard → Settings → API → service_role")

HEADERS = {
    'apikey': SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'resolution=merge-duplicates',  # UPSERT: ON CONFLICT (cod) DO UPDATE
}


def safe_int(v):
    try:
        f = float(v or 0)
        return 0 if math.isnan(f) or math.isinf(f) else int(f)
    except (TypeError, ValueError):
        return 0


def norm(v):
    if v is None:
        return ''
    s = str(v).strip().replace('\xa0', ' ')
    return s


print("Leyendo Libro1.xlsx...")
wb = openpyxl.load_workbook('Libro1.xlsx', read_only=True, data_only=True)
ws = wb['Hoja1']
rows = list(ws.iter_rows(values_only=True))
wb.close()

if not rows:
    raise SystemExit("ERROR: Hoja1 de Libro1.xlsx está vacía")

cols = [norm(c) for c in rows[0]]
print(f"  Columnas detectadas: {cols[:8]}...")

records = []
for row in rows[1:]:
    if not any(row):
        continue
    r = dict(zip(cols, row))

    cod_raw = r.get('Prod.')
    if cod_raw is None:
        continue
    cod = str(cod_raw).strip().rstrip('.0')
    if not cod or cod == '0':
        continue

    desc = norm(r.get('Descripción de Producto', '') or '')
    if not desc:
        continue

    familia = norm(r.get('Familia', '') or '')
    cantidad = safe_int(r.get('Stock'))

    records.append({
        'cod': cod,
        'descripcion': desc,
        'familia': familia,
        'cantidad': cantidad,
    })

print(f"  {len(records)} productos encontrados en Libro1.xlsx")

BATCH = 500
url = f"{SUPABASE_URL}/rest/v1/stock"
total_ok = 0

for i in range(0, len(records), BATCH):
    batch = records[i:i + BATCH]
    payload = json.dumps(batch).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  Batch {i // BATCH + 1} ({len(batch)} filas) → HTTP {resp.status} OK")
            total_ok += len(batch)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"  ERROR en batch {i // BATCH + 1}: HTTP {e.code}\n  {body}")
        raise

print(f"\nStock inicial cargado: {total_ok} productos.")
print("Verificar en Supabase SQL editor:")
print("  SELECT COUNT(*), SUM(cantidad) FROM stock;")

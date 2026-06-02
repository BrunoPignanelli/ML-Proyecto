import json

with open('comparativa_agencias.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

src = (
    "# ── TABLA DE MAPEO: que etiqueta usa cada agencia por tipo de producto ─────\n"
    "#\n"
    "# Esta tabla es la parte mas importante: muestra exactamente a que categoria\n"
    "# de cada agencia se mapea cada tipo de producto unificado.\n"
    "# Si algun mapeo parece incorrecto, corregi el MAPPING en la celda anterior.\n"
    "\n"
    "rows = []\n"
    "for ucat, ucat_name in UNIFIED_CATS.items():\n"
    "    row = {'Categoria unificada': ucat_name}\n"
    "    for ag in agencies_list:\n"
    "        label = MAPPING.get(ag, {}).get(ucat)\n"
    "        if label is None:\n"
    "            row[ag] = '—'\n"
    "            continue\n"
    "        price = agency_prices_norm.get(ag, {}).get(norm(label))\n"
    "        if price and agency_meta.get(ag) == 'sin IVA':\n"
    "            price = round(price * IVA, 2)\n"
    "        row[ag] = f\"{label}  (${price:,.0f})\" if price else label\n"
    "    rows.append(row)\n"
    "\n"
    "df_map = pd.DataFrame(rows).set_index('Categoria unificada')\n"
    "\n"
    "# Mostrar transpuesto: filas = agencias, columnas = categorias unificadas\n"
    "df_T = df_map.T\n"
    "pd.set_option('display.max_colwidth', 30)\n"
    "pd.set_option('display.max_columns', 20)\n"
    "pd.set_option('display.width', 500)\n"
    "print('Filas = agencias, Columnas = categorias unificadas')\n"
    "print('Cada celda = como la llama la agencia + precio bruto')\n"
    "print('Si una celda muestra el nombre incorrecto, hay que corregir el MAPPING')\n"
    "print()\n"
    "df_T"
)

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": src
}

# Insertar después del MAPPING (índice 5)
nb['cells'].insert(6, new_cell)

with open('comparativa_agencias.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f'OK - Notebook tiene {len(nb["cells"])} celdas')
for i, c in enumerate(nb['cells']):
    s = ''.join(c['source'])[:65].replace('\n', ' ')
    print(f'  [{i:2}] {c["cell_type"]:8}  {s!r}')

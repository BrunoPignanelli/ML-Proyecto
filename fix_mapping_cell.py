import json

with open('comparativa_agencias.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

# Buscar y quitar la celda de mapeo que está en posición incorrecta (índice 6)
# Identificarla por su source
mapping_cell = None
mapping_idx = None
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    if 'Filas = agencias, Columnas = categorias' in src or 'df_T = df_map.T' in src:
        mapping_cell = c
        mapping_idx = i
        break

if mapping_cell:
    nb['cells'].pop(mapping_idx)
    print(f'Celda de mapeo removida del índice {mapping_idx}')

# Encontrar el índice de la celda de comparativa (que define agencies_list, norm, etc.)
comp_idx = None
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    if 'agencies_list = list(MAPPING.keys())' in src:
        comp_idx = i
        break

print(f'Celda comparativa (agencies_list) en índice {comp_idx}')

# Insertar la celda de mapeo DESPUÉS de la celda comparativa
src = (
    "# ── TABLA DE MAPEO: que etiqueta usa cada agencia por tipo de producto ─────\n"
    "#\n"
    "# Esta tabla muestra de forma clara la unificacion:\n"
    "# - Fila = agencia\n"
    "# - Columna = categoria unificada\n"
    "# - Celda = como LA LLAMA ESA AGENCIA en su tarifa + el precio bruto\n"
    "#\n"
    "# Si una celda parece incorrecta (la agencia usa otra categoria para ese producto),\n"
    "# hay que corregir el MAPPING en la celda 'CATEGORIAS UNIFICADAS'.\n"
    "\n"
    "rows = []\n"
    "for ucat, ucat_name in UNIFIED_CATS.items():\n"
    "    row = {'Agencia / Categoria unificada': ucat_name}\n"
    "    for ag in agencies_list:\n"
    "        label = MAPPING.get(ag, {}).get(ucat)\n"
    "        if label is None:\n"
    "            row[ag] = 'N/A'\n"
    "            continue\n"
    "        price = agency_prices_norm.get(ag, {}).get(norm(label))\n"
    "        if price and agency_meta.get(ag) == 'sin IVA':\n"
    "            price = round(price * IVA, 2)\n"
    "        row[ag] = f'{label}  (${price:,.0f})' if price else label\n"
    "    rows.append(row)\n"
    "\n"
    "df_map = pd.DataFrame(rows).set_index('Agencia / Categoria unificada')\n"
    "\n"
    "# Transponer: filas=agencias, columnas=categorias unificadas\n"
    "df_T = df_map.T\n"
    "df_T.index.name = 'Agencia'\n"
    "\n"
    "pd.set_option('display.max_colwidth', 32)\n"
    "pd.set_option('display.max_columns', 20)\n"
    "pd.set_option('display.width', 600)\n"
    "\n"
    "print('COMO SE UNIFICA: cada celda muestra el nombre que usa la agencia + precio bruto')\n"
    "print('Fila = agencia  |  Columna = categoria unificada')\n"
    "print()\n"
    "df_T\n"
)

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": src
}

insert_at = comp_idx + 1
nb['cells'].insert(insert_at, new_cell)
print(f'Celda de mapeo insertada en índice {insert_at}')

with open('comparativa_agencias.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f'Notebook guardado con {len(nb["cells"])} celdas')

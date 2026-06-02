import json

with open('comparativa_agencias.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

def code_cell(src):
    return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src}

def md_cell(src):
    return {"cell_type":"markdown","metadata":{},"source":src}

md_como = md_cell(
    "## Cómo funciona la clasificación\n\n"
    "Cada producto pasa por **dos pasos**:\n\n"
    "### Paso 1 — Familia del producto\n\n"
    "```\n"
    "Familia\n"
    "│\n"
    "├── LUBRICANTES        → ¿\"TAMBOR\"/\"205\" en descripción? → lubricante_tambor\n"
    "│                                                         → lubricante_caja\n"
    "├── BATERIAS           → extraer amperaje (\"90A\")\n"
    "│                         ≤110A → bateria_chica  |  >110A → bateria_grande\n"
    "├── ACCES./CAM MOTO    → camara  (sin importar el rodado)\n"
    "├── MOTO               → cub_moto\n"
    "├── GIGANTE/OTR        → cub_camion_r20_r22\n"
    "├── VIALES/IND.        → rodado ≥38\" → xgde  |  resto → gde\n"
    "├── AGR DEL.           → rodado ≥38\"→xgde | ≥28\"→gde | ≥24\"→med | resto→del\n"
    "├── AGR TRAS.          → rodado ≥38\"→xgde | ≥30\"→gde | ≥24\"→med\n"
    "├── PASEO              → rodado ≤14\" → r12_r14  |  resto → r15_r19\n"
    "└── CAMIONETA/PICK UP  → rodado ≤14\"→r12 | ≤19\"→r15 | ≥20\"→camion\n"
    "```\n\n"
    "### Paso 2 — Extraer rodado de la descripción (3 intentos)\n\n"
    "```\n"
    "\"14.9 - 24  14PR TT\"  → intento 1: dígito + espacios + guión + 2-3 dígitos  → 24\"\n"
    "\"7.50-16    8PR TT\"   → intento 2: guión sin espacio + 2-3 dígitos          → 16\"\n"
    "\"175/65 TR 14\"        → intento 3: R + espacio opcional + 2 dígitos         → 14\"\n"
    "\"11L-16     8PR TT\"   → intento 2: -16                                      → 16\"\n"
    "```"
)

cell_por_producto = code_cell(
    "# ── Precio de envío por producto × agencia (bruto y efectivo) ─────────────\n"
    "for ag in agencies_list:\n"
    "    df[f'{ag}_bruto']    = df['categoria_unif'].apply(lambda c: lookup_price(ag, c))\n"
    "    df[f'{ag}_efectivo'] = df['categoria_unif'].apply(lambda c: lookup_effective(ag, c))\n"
    "\n"
    "eff_cols = [f'{ag}_efectivo' for ag in agencies_list]\n"
    "df['PRECIO_EF_MIN']  = df[eff_cols].min(axis=1)\n"
    "df['MEJOR_AGENCIA']  = df[eff_cols].idxmin(axis=1).str.replace('_efectivo', '', regex=False)\n"
    "\n"
    "out_cols = (['Prod.', 'Descripción de Producto', 'Familia', 'categoria_nombre',\n"
    "             'MEJOR_AGENCIA', 'PRECIO_EF_MIN'] + eff_cols)\n"
    "df_out = df[out_cols].copy()\n"
    "df_out.columns = (['Prod.', 'Descripción', 'Familia', 'Categoría',\n"
    "                   'MEJOR AGENCIA', 'PRECIO EF. MIN'] + agencies_list)\n"
    "\n"
    "print(f'Productos clasificados: {len(df_out)}')\n"
    "print('\\nMejor agencia por cantidad de productos (precio efectivo):')\n"
    "print(df_out['MEJOR AGENCIA'].value_counts().to_string())\n"
    "df_out.head(20)"
)

cell_ranking = code_cell(
    "# ── Ranking por categoría: precio efectivo + canje + frecuencia ──────────\n"
    "print('=== RANKING POR CATEGORÍA  (precio efectivo · canje · frecuencia) ===\\n')\n"
    "for ucat, ucat_name in UNIFIED_CATS.items():\n"
    "    scores = {}\n"
    "    for ag in agencies_list:\n"
    "        bruto = lookup_price(ag, ucat)\n"
    "        eff   = lookup_effective(ag, ucat)\n"
    "        if eff is not None:\n"
    "            freq_label, freq_days = agency_freq[ag]\n"
    "            scores[ag] = (bruto, eff, freq_label, freq_days)\n"
    "    if not scores:\n"
    "        continue\n"
    "    sorted_scores = sorted(scores.items(), key=lambda x: x[1][1])\n"
    "    print(f'{ucat_name}:')\n"
    "    for i, (ag, (bruto, eff, flabel, fdays)) in enumerate(sorted_scores, 1):\n"
    "        canje_pct = agency_canje.get(ag, 0) * 100\n"
    "        canje_str = f'canje {canje_pct:.0f}%' if canje_pct > 0 else 'sin canje'\n"
    "        freq_str  = f'{flabel} ({fdays}d/sem)'\n"
    "        note      = '  <- MEJOR' if i == 1 else ''\n"
    "        print(f'  {i:2}. {ag:<45}  ${bruto:>8,.0f} -> ${eff:>8,.0f}  {canje_str:<12}  {freq_str}{note}')\n"
    "    print()"
)

cell_export = code_cell(
    "# ── Exportar a Excel ─────────────────────────────────────────────────────\n"
    "output_file = 'comparativa_resultado.xlsx'\n"
    "\n"
    "df_agencias = pd.DataFrame([\n"
    "    {'Agencia': ag,\n"
    "     'Canje %': round(agency_canje[ag]*100, 0),\n"
    "     'Factor efectivo': round(1 - agency_canje[ag], 4),\n"
    "     'IVA': agency_meta[ag],\n"
    "     'Frecuencia': agency_freq[ag][0],\n"
    "     'Dias/semana': agency_freq[ag][1]}\n"
    "    for ag in agencies_list\n"
    "]).sort_values('Canje %', ascending=False)\n"
    "\n"
    "cols_exp = (['Prod.', 'Descripción de Producto', 'Familia', 'categoria_nombre',\n"
    "             'MEJOR_AGENCIA', 'PRECIO_EF_MIN']\n"
    "            + [f'{ag}_efectivo' for ag in agencies_list]\n"
    "            + [f'{ag}_bruto'    for ag in agencies_list])\n"
    "df_exp_prod = df[cols_exp].copy()\n"
    "df_exp_prod.columns = (['Codigo', 'Descripcion', 'Familia', 'Categoria Unificada',\n"
    "                         'Mejor Agencia', 'Precio Ef. Min']\n"
    "                        + [f'{ag} (ef.)'    for ag in agencies_list]\n"
    "                        + [f'{ag} (bruto)'  for ag in agencies_list])\n"
    "\n"
    "df_fam = (df[['Familia','categoria_nombre','MEJOR_AGENCIA','PRECIO_EF_MIN']]\n"
    "          .groupby(['Familia','categoria_nombre','MEJOR_AGENCIA'])['PRECIO_EF_MIN']\n"
    "          .mean().reset_index())\n"
    "df_fam.columns = ['Familia','Categoria Unificada','Mejor Agencia','Precio Ef. Promedio']\n"
    "\n"
    "with pd.ExcelWriter(output_file, engine='openpyxl') as writer:\n"
    "    df_agencias.to_excel(writer,    sheet_name='Agencias', index=False)\n"
    "    df_view_con_freq.to_excel(writer, sheet_name='Por Categoria (ef.)')\n"
    "    df_exp_prod.to_excel(writer,    sheet_name='Por Producto', index=False)\n"
    "    df_fam.to_excel(writer,         sheet_name='Por Familia', index=False)\n"
    "\n"
    "print(f'Exportado: {output_file}')\n"
    "print('  Hoja 1 Agencias:           canje % + frecuencia')\n"
    "print('  Hoja 2 Por Categoria:      precios efectivos + fila frecuencias')\n"
    "print('  Hoja 3 Por Producto:       1437 productos con precio ef. y bruto')\n"
    "print('  Hoja 4 Por Familia:        resumen por familia')"
)

# Conservar celdas 0-7 (intro, imports, libro1, sheet-parse, precios+canje+freq, mapping, comparativa, classify)
# Agregar: markdown explicacion, verificacion (era indice 8), por_producto, ranking, export
good_cells = (nb['cells'][:8]          # 0..7
              + [md_como]              # markdown clasificacion
              + [nb['cells'][8]]       # verificacion (95a985c6)
              + [cell_por_producto, cell_ranking, cell_export])

nb['cells'] = good_cells
nb['nbformat'] = 4
nb['nbformat_minor'] = 5

with open('comparativa_agencias.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f'Notebook reconstruido: {len(nb["cells"])} celdas')
for i, c in enumerate(nb['cells']):
    src_preview = ''.join(c['source'])[:65].replace('\n', ' ')
    print(f'  [{i:2}] {c["cell_type"]:8}  {src_preview!r}')

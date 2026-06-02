import json

with open('comparativa_agencias.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

# ── Celda 1: función de optimización ──────────────────────────────────────
src_func = """\
# ── OPTIMIZADOR DE ENVÍOS ─────────────────────────────────────────────────
# Dado un pedido {codigo_producto: cantidad}, calcula:
#   MODO 1 - Misma agencia:   ranking de agencias con el costo total del pedido
#   MODO 2 - Por producto:    cada producto va a la agencia más barata para ese tipo
# La diferencia entre ambos totales muestra el costo de consolidar en una sola agencia.

def buscar_producto(codigo):
    \"\"\"Busca el producto en df por código; tolera int, float y string.\"\"\"
    cod_str = str(codigo).strip().rstrip('.0') if str(codigo).endswith('.0') else str(codigo).strip()
    # Intentar match exacto sobre la columna Prod. como string
    mask = df['Prod.'].astype(str).str.strip().str.rstrip('0').str.rstrip('.') == cod_str
    hit = df[mask]
    if hit.empty:
        # Segundo intento: comparación numérica
        try:
            mask2 = df['Prod.'] == float(codigo)
            hit = df[mask2]
        except (ValueError, TypeError):
            pass
    return hit.iloc[0] if not hit.empty else None


def calcular_envio(pedido, mostrar_detalle=True):
    \"\"\"
    pedido: dict {codigo_producto: cantidad}
    Ej: {20046: 10, 31186: 5, 130108: 20}
    \"\"\"
    # ── Resolver productos ────────────────────────────────────────────────
    lineas = []
    for cod, qty in pedido.items():
        prod = buscar_producto(cod)
        if prod is None:
            print(f"  ADVERTENCIA: codigo {cod!r} no encontrado en Libro1")
            continue
        ucat = prod['categoria_unif']
        lineas.append({
            'codigo':      cod,
            'descripcion': str(prod['Descripcion de Producto'] if 'Descripcion de Producto' in prod.index
                               else prod['Descripción de Producto'])[:55],
            'familia':     prod['Familia'],
            'categoria':   prod['categoria_nombre'],
            'ucat':        ucat,
            'cantidad':    qty,
        })

    if not lineas:
        print("No se encontraron productos en el pedido.")
        return None, None

    if mostrar_detalle:
        print("Productos del pedido:")
        for l in lineas:
            print(f"  {l['codigo']}  {l['descripcion'][:50]:<50}  qty={l['cantidad']:>4}  → {l['categoria']}")
        print()

    # ── MODO 1: Toda la carga en UNA sola agencia ─────────────────────────
    modo1 = []
    for ag in agencies_list:
        freq_label, freq_days = agency_freq[ag]
        total = 0.0
        sin_precio = []
        detalles = []
        for l in lineas:
            p = lookup_effective(ag, l['ucat'])
            if p is None:
                sin_precio.append(l['descripcion'][:30])
            else:
                subtotal = p * l['cantidad']
                total += subtotal
                detalles.append((l['descripcion'], l['cantidad'], p, subtotal))
        modo1.append({
            'Agencia':       ag,
            'Total (ef.)':   round(total, 0) if not sin_precio else None,
            'Frecuencia':    freq_label,
            'Dias/sem':      freq_days,
            'Sin precio':    ', '.join(sin_precio) if sin_precio else '',
            '_detalles':     detalles,
        })

    df_m1 = (pd.DataFrame(modo1)
               .drop(columns=['_detalles'])
               .sort_values('Total (ef.)'))

    # ── MODO 2: Cada producto a su MEJOR agencia ──────────────────────────
    total_m2 = 0.0
    modo2 = []
    for l in lineas:
        precios_ag = {ag: lookup_effective(ag, l['ucat'])
                      for ag in agencies_list
                      if lookup_effective(ag, l['ucat']) is not None}
        if not precios_ag:
            modo2.append({
                'Codigo':       l['codigo'],
                'Descripcion':  l['descripcion'],
                'Categoria':    l['categoria'],
                'Cantidad':     l['cantidad'],
                'Mejor Agencia':'SIN PRECIO',
                'Precio ef.':   None,
                'Subtotal':     None,
                'Frecuencia':   '',
            })
            continue
        mejor_ag = min(precios_ag, key=precios_ag.get)
        precio   = precios_ag[mejor_ag]
        subtotal = precio * l['cantidad']
        total_m2 += subtotal
        modo2.append({
            'Codigo':       l['codigo'],
            'Descripcion':  l['descripcion'],
            'Categoria':    l['categoria'],
            'Cantidad':     l['cantidad'],
            'Mejor Agencia':mejor_ag,
            'Precio ef.':   precio,
            'Subtotal':     round(subtotal, 0),
            'Frecuencia':   agency_freq[mejor_ag][0],
        })

    df_m2 = pd.DataFrame(modo2)

    # ── Resumen de agencias necesarias en modo 2 ──────────────────────────
    agencias_m2 = df_m2['Mejor Agencia'].value_counts()

    return df_m1, df_m2, round(total_m2, 0), agencias_m2


print("Funcion calcular_envio() lista.")
print("Uso:  df_m1, df_m2, total_m2, agencias_m2 = calcular_envio(PEDIDO)")
"""

# ── Celda 2: ingreso del pedido y resultado ────────────────────────────────
src_pedido = """\
# ── PEDIDO — editar aqui con los productos y cantidades ──────────────────
#
# Formato: {codigo_producto: cantidad}
# El codigo es el valor de la columna "Prod." de Libro1.
# Ejemplos de codigos: 20046 (camara auto), 31186 (bateria), 130108 (aceite 1L)

PEDIDO = {
    20046:  10,   # CAMARA SELETTO KR16 TR15
    20052:   5,   # CAMARA SELETTO 7.50-16
    31186:   8,   # BATERIA ENERGIZER 90A (chica)
    31189:   3,   # BATERIA ENERGIZER 120A (grande)
    130108: 20,   # ENI I-RIDE 20W-50 1LT
}

# ── Calcular ──────────────────────────────────────────────────────────────
df_m1, df_m2, total_m2, agencias_m2 = calcular_envio(PEDIDO)

pd.set_option('display.float_format', '${:,.0f}'.format)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.max_rows', 30)

# ── MODO 1: Una sola agencia ──────────────────────────────────────────────
print("=" * 70)
print("MODO 1: TODA LA CARGA EN UNA SOLA AGENCIA")
print("=" * 70)
print(df_m1[df_m1['Sin precio'] == ''].to_string(index=False))
if df_m1['Sin precio'].any():
    print()
    print("Agencias que no cubren todos los productos del pedido:")
    print(df_m1[df_m1['Sin precio'] != ''][['Agencia','Sin precio']].to_string(index=False))

# ── MODO 2: Cada producto a la mejor agencia ──────────────────────────────
print()
print("=" * 70)
print("MODO 2: CADA PRODUCTO A SU MEJOR AGENCIA")
print("=" * 70)
print(df_m2.to_string(index=False))
print()
print(f"Total Modo 2: ${total_m2:,.0f}")
print()
print("Agencias necesarias en Modo 2:")
for ag, n in agencias_m2.items():
    freq_label, freq_days = agency_freq.get(ag, ('?', 0))
    print(f"  {ag:<45}  {n} producto(s)  |  {freq_label} ({freq_days}d/sem)")

# ── Comparativa final ─────────────────────────────────────────────────────
mejor_m1_total = df_m1[df_m1['Sin precio'] == '']['Total (ef.)'].min()
mejor_m1_ag    = df_m1[df_m1['Sin precio'] == ''].iloc[0]['Agencia']

print()
print("=" * 70)
print("COMPARATIVA")
print("=" * 70)
print(f"  Modo 1 (mejor agencia unica):   ${mejor_m1_total:>10,.0f}  [{mejor_m1_ag}]")
print(f"  Modo 2 (split por producto):    ${total_m2:>10,.0f}  ({len(agencias_m2)} agencia(s))")
diferencia = mejor_m1_total - total_m2
if diferencia > 0:
    print(f"  Costo de consolidar:            ${diferencia:>10,.0f}  mas caro en Modo 1")
    print(f"  -> Conviene dividir el envio entre {len(agencias_m2)} agencia(s)")
else:
    print(f"  Ahorro de consolidar:           ${-diferencia:>10,.0f}  mas barato en Modo 1")
    print(f"  -> Conviene mandar todo con {mejor_m1_ag}")
"""

# Insertar ambas celdas al final (antes del export)
export_idx = None
for i, c in enumerate(nb['cells']):
    if '# -- Exportar a Excel' in ''.join(c['source']) or 'comparativa_resultado.xlsx' in ''.join(c['source']):
        export_idx = i
        break

if export_idx is None:
    export_idx = len(nb['cells'])

cell_func   = {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src_func}
cell_pedido = {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src_pedido}

nb['cells'].insert(export_idx, cell_pedido)
nb['cells'].insert(export_idx, cell_func)

with open('comparativa_agencias.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f'OK - {len(nb["cells"])} celdas')
for i, c in enumerate(nb['cells']):
    s = ''.join(c['source'])[:65].replace('\n',' ')
    print(f'  [{i:2}] {c["cell_type"]:8} {s!r}')

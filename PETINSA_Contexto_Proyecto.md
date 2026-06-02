# Proyecto PETINSA — Recomendador de Agencias de Envío

**Documento de contexto para el equipo**
Última actualización: Mayo 2026

---

## TL;DR — en 30 segundos

PETINSA, distribuidora de neumáticos, hoy elige manualmente entre **14 agencias de transporte** para cada envío. Cada agencia categoriza distinto los productos y tiene su propia tarifa, y algunas ofrecen **canje** (parte del envío se paga con gomas en lugar de dinero). La decisión es intuitiva y genera sobrecostos.

**Objetivo:** construir un sistema que reciba un producto + cantidad y devuelva las 3 agencias más convenientes en costo neto.

**Estado actual:** prototipo funcionando en Python + Streamlit con dos componentes clave:
1. Una tabla de equivalencias **producto → categoría de envío por agencia** (ya hecha en dos versiones: la mía + la del compañero).
2. Un motor que calcula bruto, canje, neto y ordena.

**Lo que falta:** validar las equivalencias con un trabajador de PETINSA, decidir interpretación del canje, y armar la presentación académica.

---

## 1. El problema en detalle

### Contexto del negocio

PETINSA vende neumáticos y los envía al interior del país. Usa 14 agencias de transporte para esa logística:

DAC · NASAZZI · MEGAM · Transportes Nagar (Ruta 1) · SELEGUIN · EXPRESO ROCHA · BULEVAR (ACC) · PERICO · TRUJILLO · GONFER · 3EME (El Chambon) · Martin Escudero (Lascano) · Arzuaga · Franchi

Cada agencia tiene:
- **Su propia categorización** (DAC dice "Rodado 15 a 18", MEGAM dice "Cubierta auto (15 a 17)", Nagar dice simplemente "Auto" — para el mismo producto).
- **Su propio tarifario** mensual.
- **Su propio canje** (porcentaje del envío que PETINSA paga con gomas en lugar de dinero): va de 0% a 100%.
- **Su propia frecuencia de retiro** (L a V, lunes/miércoles/viernes, según disponibilidad, etc.).
- **Su propia zona de cobertura** (algunas son universales, otras solo zonas específicas).

### La decisión que hay que automatizar

Hoy un trabajador mira el catálogo de tarifas y elige a ojo. Queremos que el sistema, dado:
- producto (código o medida)
- cantidad
- destino (opcional)

devuelva un **Top 3** ordenado por costo neto, con explicación.

---

## 2. Análisis del Excel de tarifas

**Archivo:** `COMPARATIVA_AGENCIAS.xlsx` — 18 hojas, una por mes (desde Diciembre 2023 hasta Mayo 2026).

### Estructura por hoja (verificado en `Costo ag. Mayo 2026`)

| Fila | Contenido |
|------|-----------|
| 0 | Etiqueta "Agencias" |
| 2 | Canje (`0.1`, `0.25`, `0.4`, `1`, `No tiene`) |
| 3 | Descuento al superar $400.000 (no poblado en Mayo 2026) |
| 4 | Frecuencia + aumento previsto |
| 5 | Nombre de la agencia |
| 6 | Encabezado "Categorías / Precios IVA incl" |
| 7+ | Filas de datos (categoría, precio) |

### Canjes en Mayo 2026

| Agencia | Canje |
|---|---|
| SELEGUIN, TRUJILLO, Franchi | **100%** |
| NASAZZI | 40% |
| MEGAM, BULEVAR | 25% |
| GONFER | 15% |
| DAC | 10% |
| EXPRESO ROCHA, Nagar, PERICO, 3EME, Martin Escudero, Arzuaga | 0% |

### Particularidades importantes

1. **GONFER** tiene precios *sin IVA* ("Empresa literal E"). El parser le suma 22%.
2. **Arzuaga** publica dos precios para la misma categoría según destino (Young/Paysandú vs Trinidad).
3. **BULEVAR (ACC)** tiene dos modalidades: "con levante" y "sin levante / piso".
4. **Frecuencia variable:** algunas agencias retiran cuando tienen carga (ej. 3EME). Un envío urgente para jueves no puede ir por una agencia que retira solo lunes/miércoles/viernes.
5. **La dificultad central:** las categorías no son comparables 1-a-1 entre agencias. Para una `205/70 R16`:
   - DAC → "Rodado 15 a 18"
   - NASAZZI → "Rodado 15 a 19"
   - MEGAM → "Cubierta auto (15 a 17)"
   - Nagar → "Auto"
   - EXPRESO ROCHA → "Cubierta chica hasta 205/70.16"

---

## 3. Catálogo de productos de PETINSA

**Archivo:** `Libro1.xlsx` (catálogo exportado del ERP) — **1.437 productos**.

### Cuatro niveles de categorización interna

| Nivel | Cantidad | Ejemplo |
|---|---|---|
| Producto individual | 1.437 | `MOMO M20 PRO VT 185/65 R 15 88H` |
| **Ramo** (línea comercial) | **54** | `MOMO PASEO`, `PIRELLI PASEO RADIAL EUROPA`, `BATERIAS ENERGIZER` |
| Familia Ramo (código) | 54 | `2411`, `400`, `1006` |
| Familia | 18 | `PASEO`, `AGRICOLA TRAS.`, `BATERIAS` |

Las cuatro vienen del ERP, **no las inventamos nosotros**.

---

## 4. La regla de categorización para el envío

**Esto es lo más importante del proyecto y lo que hay que poder defender.**

### En una frase

> Construimos una categorización de envío de **dos niveles**: el primero viene heredado del catálogo interno de PETINSA (el **ramo**), y el segundo se deriva de las dimensiones físicas del producto (**rodado** en pulgadas, o **amperaje** en baterías), porque son los criterios que efectivamente usan las agencias para tarifar.

### Las 16 categorías unificadas de envío

(Categorías comunes a todas las agencias, definidas por nosotros como capa intermedia)

1. Cubierta Moto / Atado Moto
2. Cubierta Auto R13-R14
3. Cubierta Auto R15-R18 (Paseo)
4. Cubierta Camioneta R16-R19
5. Cubierta Auto/Camioneta R19-R22
6. Cubierta Camión Chico/Mediano
7. Cubierta Camión Grande / Semirremolque
8. Cubierta Agrícola Delantera Chica
9. Cubierta Agrícola Trasera Mediana (24-26")
10. Cubierta Agrícola Trasera Grande (28-34")
11. Cubierta Agrícola Extra Grande (+34")
12. Neumático Vial / OTR
13. Protector de Neumático *(13 está vacío en la numeración)*
14. Batería Chica (hasta 110 Amp)
15. Batería Grande (+110 Amp)
16. Lubricantes (caja/lata/tambor)

### Cómo se aplica la regla

**38 de los 54 ramos van directamente a una sola categoría** (mapeo 1-a-1):
- `PASEO RADIAL EUROPA` → siempre `Cubierta Auto R15-R18`
- `LUBRICANTES MOTOR` → siempre `Lubricantes`
- `NEUMATICO MOTO REG` → siempre `Cubierta Moto`
- etc.

**16 ramos se subdividen** según una dimensión física del producto, leída de la descripción con regex:

| Tipo de producto | Criterio de subdivisión |
|---|---|
| Cubiertas de auto/camioneta/pickup | Rodado en pulgadas: 13-14, 15-18, 16-19, 19-22 |
| Cubiertas agrícolas traseras | Rodado: 24-26", 28-34", +34" |
| Cubiertas de camión | Rodado < 22.5 vs ≥ 22.5 |
| Baterías | Amperaje: ≤110 A vs >110 A |
| Cámaras (familia GOODTIRE CAMARA…) | Se asignan a la categoría de la cubierta que llevan adentro |

### Por qué este corte y no otro

**No los elegimos arbitrariamente — los heredamos del tarifario de las agencias.** Cuando DAC tiene una fila "Cubierta auto R15-R18" y otra distinta "Cubierta auto R13-R14" con precio diferente, el corte está en 15. Cuando NASAZZI distingue "Batería hasta 110 A" y "Batería mayor 110 A", ese es el umbral.

**Esto le da la regla legitimidad técnica:** refleja la realidad comercial de las agencias, no una decisión nuestra.

---

## 5. Fórmula del costo neto y el debate del canje

```
bruto = precio_categoria_agencia × cantidad
neto  = bruto × (1 − canje)
```

### Dos interpretaciones del canje

**Interpretación A (la implementada por default):** el canje es el % pagado con gomas, así que no sale dinero. Bajo esta interpretación, agencias con canje 100% (SELEGUIN, TRUJILLO, Franchi) tienen `neto = 0`.

- Matemáticamente correcto desde el dinero efectivo.
- Operativamente engañoso: las gomas también tienen costo.

**Interpretación B (más realista):** las gomas tienen costo de oportunidad. Si una goma se vende a $100 pero le cuesta a PETINSA $60, el costo real del canje no es 0% sino 60% del bruto:

```
neto_realista = bruto × (1 − canje × (1 − margen_costo_goma))
```

donde `margen_costo_goma` ∈ [0, 1] es el cociente costo/precio de venta.

**Recomendación:** implementar las dos interpretaciones y dejar que el usuario elija. Defenderlo así frente al profe es honesto: muestra que entendimos que el canje no es magia.

---

## 6. Estado de los archivos del equipo

### Archivo 1 (Claude) — `Equivalencias_PETINSA_Agencias.xlsx`

**Estructura:**
- Hoja 1: 1.437 productos × 14 agencias, con categoría asignada y precio por cada cruce.
- Hoja 2: Resumen por familia (18 filas × 14 agencias, valor modal).
- Hoja 3: Leyenda con código de colores y estadísticas.

**Cobertura (20.118 celdas = 1.437 × 14):**
- 🟢 Verde (78%): mapeo de alta confianza
- 🟡 Amarillo (13%): razonable, validar
- 🟠 Naranja (1%): pocos casos a revisar
- ⬜ Gris (8%): la agencia no maneja ese tipo de producto

**Lo que tiene de fuerte:** colores de confianza por celda, distinción "no aplica vs precio omitido", reglas explícitas en código por agencia.

### Archivo 2 (compañero) — `Categorias_Agencias_Clasificacion_Productos.xlsx`

**Estructura:**
- Hoja 1: 16 categorías unificadas × 14 agencias (tarifario consolidado).
- Hoja 2: 1.437 productos clasificados, cada uno con su categoría unificada + Cat. ID.
- Hoja 3: Resumen por categoría (cantidad de productos, precio promedio, descripción del criterio).

**Lo que tiene de fuerte:** capa intermedia de 16 categorías unificadas que simplifica el matcher, Cat. ID numérico, columna "Equivalencias en planilla original" que documenta nombres de cada agencia.

### Comparación rápida

Ambos enfoques terminaron en lo mismo a nivel macro (1.437 productos × 14 agencias con rodado parseado), pero el del compañero introduce una **mejora real**: la capa intermedia de 16 categorías. Con eso:

- **Modelo mío:** producto → categoría específica por cada agencia → 14 categorías distintas → 14 precios. Necesita una regla por agencia.
- **Modelo del compañero:** producto → 1 categoría unificada → 14 precios (lookup directo). Más simple de mantener.

**Recomendación:** usar el del compañero como tabla maestra del sistema. Sumarle del mío los colores de confianza y la documentación de qué celdas requieren validación.

### Archivo 3 (Claude) — `Comparacion_Categorizaciones.xlsx`

Documento que compara los dos archivos en 5 hojas: resumen ejecutivo, categorías lado a lado, mapeo familia→categoría con dispersión, 8 casos a discutir, recomendación de integración. Útil para que vean qué decisiones aún no están cerradas.

---

## 7. Arquitectura del prototipo en código

```
proyecto/
├── parser.py          # Lee el Excel de tarifas y devuelve DataFrame normalizado
├── matcher.py         # Parsea medida + reglas por agencia + función buscar_categoria()
├── recomendador.py    # Calcula bruto/canje/neto, ordena, devuelve Top N
├── app_streamlit.py   # Interfaz web
└── README.md
```

### `parser.py`
- Lee la hoja seleccionada del Excel mensual.
- Devuelve un DataFrame con columnas: `agencia / canje / categoria / precio_iva_incl / frecuencia`.
- Maneja casos especiales: GONFER sin IVA (le suma 22%), Arzuaga con dos destinos (Young/Paysandú vs Trinidad).

### `matcher.py`
- **Parser de medida:** 13 patrones de regex que detectan el rodado en cualquier formato (métrico `205/60 R 15`, agrícola `23.1-30`, moto `90/90-18`, reforzado `LT215/85 R 16`, vial `30.5L32`, etc.). Cobertura: 100% para todo lo que tiene medida.
- **Reglas por agencia** (`REGLAS_POR_AGENCIA`): para cada agencia hay reglas tipo `if rodado entre X e Y y tipo == Z → categoría 'Cubierta auto (15 a 17)'`.
- **Fallback difuso** (`difflib.get_close_matches`) cuando no matchea ninguna regla.

**Estado de cobertura:**

| Agencia | Reglas explícitas |
|---|---|
| DAC, NASAZZI, MEGAM, Nagar, SELEGUIN, EXPRESO ROCHA | ✅ con reglas |
| BULEVAR, PERICO, TRUJILLO, GONFER, 3EME, Martin Escudero, Arzuaga, Franchi | ❌ solo fallback difuso |

### `recomendador.py`
- Recibe medida + cantidad.
- Itera por las 14 agencias, llama a `buscar_categoria()`, calcula bruto/canje/neto.
- Ordena ascendente por neto.
- Devuelve la lista completa con metadata (método de match, confianza, frecuencia).

### `app_streamlit.py`
- **Sidebar:** subir Excel + seleccionar mes + toggle de interpretación del canje.
- **Form:** medida (texto libre) + cantidad + destino (opcional).
- **Resultados:** Top 3 en tarjetas (🥇 🥈 🥉) con costo neto destacado + tabla completa de las 14 agencias + advertencias de baja confianza.

### Cómo correrlo

```bash
pip install pandas openpyxl streamlit
streamlit run app_streamlit.py
```

### Verificación con casos reales (Mayo 2026)

| Consulta | Top 1 | Detalle |
|---|---|---|
| `205/70 R16` × 4 | SELEGUIN, neto $0 | canje 100%, categoría `Cubierta auto` |
| `11.2-24` × 2 | SELEGUIN, neto $0 | canje 100%, `Tractor mediana 24 a 26` |
| `Bateria chica` × 1 | SELEGUIN, neto $0 | canje 100%, `Baterias chicas` |

⚠️ **Observar:** las 3 agencias con canje 100% siempre salen primeras bajo Interpretación A. Bajo Interpretación B esto se corrige.

---

## 8. Justificación académica (para la presentación de Aprendizaje Automático)

### Por qué reglas y no Machine Learning en la etapa 1

> *"Aplicamos un sistema basado en reglas porque la lógica de negocio es conocida y determinística, no hay datos históricos etiquetados, y se necesita explicabilidad total para que la empresa confíe en la herramienta. Usar ML acá sería complejidad sin ganancia."*

**Los tres criterios que justifican reglas sobre ML:**
1. La lógica está explícita en el Excel de tarifas (mapeo categoría → precio).
2. No hay historial de envíos etiquetados con "esta fue la decisión correcta".
3. PETINSA necesita auditar cada decisión (es plata real).

### Dónde sí entra ML (etapa 2 y 3)

| Problema | Tipo de modelo | Datos necesarios |
|---|---|---|
| Mapear medida nueva → categoría por agencia | Clasificación multiclase | Historial de envíos facturados |
| Predecir costo final real (incluye extras, devoluciones) | Regresión | Costo estimado vs costo real facturado |
| Recomendar agencia considerando calidad, no solo precio | Sistema de recomendación / ranking | Historial de elecciones, reclamos, tiempos |
| Detectar envíos anómalos | Detección de anomalías | Histórico de envíos |

### Conexión explícita con la materia

- El **matching difuso** (`difflib`) es un baseline de similitud textual, comparable con técnicas de NLP clásico (TF-IDF).
- El **diseño** está preparado para sumar `scikit-learn` cuando haya historial.
- El **trade-off reglas vs ML** es un debate académico válido y central en la materia: cuándo cada uno, por qué.

---

## 9. Lo que aún tenemos que cerrar antes de la entrega

### Validaciones con un trabajador de PETINSA (15-30 min de conversación)

1. **Las 70 celdas amarillas/naranjas** del archivo de equivalencias (cámaras de ACCES. OTRAS M tratadas como cubiertas, agrícolas delanteras vs traseras chicas en agencias chicas).
2. **El umbral exacto** de rodado en agrícolas (¿24-26 incluye 24 y 26 o solo 24 y 25?).
3. **Arzuaga**: ¿se usa más para Young/Paysandú o para Trinidad por defecto?
4. **BULEVAR (ACC)**: ¿"con levante" o "sin levante / piso" es la modalidad por defecto?
5. **GIGANTE**: criterio exacto para separar Camión Chico/Mediano vs Grande/Semirremolque.
6. **Protector de Neumático**: ¿categoría separada o se fusiona con bulto/bolsa?
7. **PASEO con 1 producto en R13-R14**: confirmar qué código exacto es.

### Decisiones técnicas pendientes

- [ ] Activar la **Interpretación B** del canje con un slider para `margen_costo_goma`.
- [ ] Completar las **reglas explícitas** para las 8 agencias que hoy usan fallback difuso (BULEVAR, PERICO, TRUJILLO, GONFER, 3EME, Martin Escudero, Arzuaga, Franchi).
- [ ] Decidir si la tabla maestra es la del compañero o la integración de ambas.
- [ ] Agregar **filtro por destino** y **filtro por día de la semana** (cruzar con frecuencia de retiro).

### Entregables académicos

- [ ] Documento escrito (con esta estructura).
- [ ] Presentación oral (planteamiento → metodología → demo → mejoras futuras).
- [ ] Demo en vivo de la app Streamlit con 3-4 casos representativos.
- [ ] Diapositivas que muestren la evolución del proyecto (de catálogo→envío→fusión).

---

## 10. Mejoras futuras (para mencionar en la presentación)

### Etapa 2 — Post-piloto, con uso real

- Guardar historial: medida, agencia elegida, costo estimado, fecha.
- Comparar costo estimado vs costo real facturado → detectar desvíos.
- Incorporar tiempos de entrega reales por agencia y destino.
- Incorporar reclamos / errores / extravíos como variable de calidad.
- Score compuesto: `score = w1·costo_neto + w2·tiempo_entrega + w3·reclamos`.

### Etapa 3 — ML real

- Clasificador supervisado para mapeo medida → categoría (entrenado con envíos facturados).
- Modelo predictivo de costo final con canje real cobrado.
- Recomendador por aprendizaje por refuerzo (maximiza utilidad a largo plazo).

### Reportes para PETINSA

- Ahorro mensual generado por la herramienta (vs elección histórica).
- Distribución de elecciones por agencia.
- Categorías más enviadas y tarifa promedio.
- Alertas: "agencia X subió sus precios más del Y%".

---

## 11. Glosario rápido

- **Canje:** porcentaje del envío que PETINSA paga con gomas en lugar de dinero.
- **Rodado:** diámetro de la llanta en pulgadas (ej. R14, R22.5).
- **Familia / Ramo:** categorización interna de PETINSA, sale del ERP.
- **Categoría unificada de envío:** capa intermedia (16 categorías) que definimos nosotros para alinear las 14 agencias.
- **Bruto:** precio × cantidad.
- **Neto:** lo que efectivamente se paga en dinero después del canje.
- **OTR:** "Off-The-Road", neumáticos para maquinaria pesada / vial / industrial.
- **Cat. ID:** identificador numérico de cada una de las 16 categorías unificadas.

---

## 12. Resumen de archivos del proyecto

| Archivo | Autor | Para qué sirve |
|---|---|---|
| `COMPARATIVA_AGENCIAS.xlsx` | PETINSA | Tarifario mensual de las 14 agencias (input) |
| `Libro1.xlsx` | PETINSA | Catálogo de 1.437 productos exportado del ERP (input) |
| `Equivalencias_PETINSA_Agencias.xlsx` | Yo (chat con Claude) | Tabla 1.437 productos × 14 agencias con colores de confianza |
| `Categorias_Agencias_Clasificacion_Productos.xlsx` | Compañero | Tabla con 16 categorías unificadas + clasificación de 1.437 productos |
| `Comparacion_Categorizaciones.xlsx` | Yo (chat con Claude) | Comparación de los dos enfoques anteriores con casos a discutir |
| `parser.py`, `matcher.py`, `recomendador.py`, `app_streamlit.py` | Yo (chat con Claude) | Código del prototipo funcional |

---

*Si algo no se entiende o falta contexto, preguntar antes de codear/decidir. Las dos categorizaciones (mía y del compañero) no son rivales — son evolución del mismo problema. La idea es fusionar lo mejor de cada una para la entrega final.*

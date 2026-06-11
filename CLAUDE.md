# CLAUDE.md

## ESTADO ACTUAL Y PRÓXIMOS PASOS

### Lo que está hecho y funcionando
- **Calculadora de envíos** — busca productos, arma pedido, calcula Modo 1 (una agencia) y Modo 2 (mejor por producto), ranking por costo verdadero y toggle de canje A/B
- **14 agencias** con precios, canje y frecuencia desde `COMPARATIVA AGENCIAS.xlsx` (hoja activa: `Costo ag. Mayo 2026`)
- **Búsqueda accent-insensitive** con `normStr()` en autocomplete y catálogo
- **Dashboard** con KPIs, gráficas Chart.js e historial de pedidos
- **Supabase integration** — conectado y funcionando; tabla `pedidos` creada; credenciales inyectadas en `.env` y en el HTML generado; fallback a localStorage si no hay credenciales
- **PWA** — `manifest.json`, `sw.js`, `icon.svg` listos; se activa automáticamente al deployar en Vercel (HTTPS)
- **Mobile responsive** — Bootstrap 5, media query @575px, touch targets 44px, iOS no-zoom inputs, tabs icon-only en mobile, overflow-x:hidden
- **Costo verdadero** — nueva columna en Modo 1 y lógica de ranking: `bruto × (1 - 0.25 × canje)`. Diferencia tres métricas: bruto (precio lista), neto (cashflow), costo (costo económico real considerando que las cubiertas de canje tienen markup 25%)
- **Autenticación** — login con email/password vía Supabase Auth. Rol `admin` ve todo (incluyendo Dashboard); rol `tenant` ve solo Calcular Envio y Catálogo. Sesión en sessionStorage (se limpia al cerrar el tab). Botón "Salir" en navbar.

### Deploy — DONE
- **URL de producción:** `ml-proyecto.vercel.app/petinsa_envios.html`
- Repo `BrunoPignanelli/ML-Proyecto` rama `main` conectado a Vercel — cada merge a `main` redeploya automáticamente
- Variables de entorno `SUPABASE_URL` y `SUPABASE_KEY` configuradas en Vercel
- PWA activo en producción (HTTPS) — instalable desde Chrome/Safari en el teléfono

### Usuarios Supabase Auth (creados 2026-06-11)
| Email | Role |
|---|---|
| brunixbruno1010@gmail.com | admin |
| ddaronch@petinsa.com.uy | admin |
| priscilagerlach9@gmail.com | admin |

Para crear nuevos usuarios (tenant o admin): usar el service role key vía `POST /auth/v1/admin/users` con `user_metadata: {"role": "admin"|"tenant"}`. Ver memory/reference_supabase.md para credenciales.

---

## 0. Deployment Constraint

**The app must remain a static site deployable on Vercel via GitHub.**

Current architecture: Python runs locally to generate `petinsa_envios.html` (a self-contained HTML+JS file with data embedded as JSON). Vercel serves that file statically — no server-side Python at runtime. This is intentional and must be preserved.

The app is a **PWA (Progressive Web App)**. Once hosted on Vercel (HTTPS), users can install it on their phone home screen from Chrome/Safari — it opens full-screen like a native app and works offline. The PWA shell files (`manifest.json`, `sw.js`, `icon.svg`) are static files committed to the repo and served by Vercel alongside the HTML.

**Default rule:** every feature must be implementable within this static constraint (client-side JS, data embedded at build time).

**Exception:** if a future feature would be exponentially more valuable but requires a server (e.g., real-time ERP sync, FastAPI backend), do not implement it silently — flag it explicitly so the trade-off can be evaluated before deciding.

---

## 1. Quickstart Commands

### Build & Run

```bash
# Regenerate the standalone HTML app (main deliverable for PETINSA)
python generar_html.py

# Run the Jupyter notebook interactively
jupyter notebook comparativa_agencias.ipynb

# Execute the notebook end-to-end non-interactively
jupyter nbconvert --to notebook --execute comparativa_agencias.ipynb --output comparativa_agencias_ejecutado.ipynb
```

### Notebook Repair / Injection Scripts
These scripts modify `comparativa_agencias.ipynb` programmatically — run from the repo root:

```bash
python rebuild_nb.py          # Full notebook reconstruction (use when cell order breaks)
python add_optimizer.py       # Inject calcular_envio() and PEDIDO cells before export cell
python insert_mapping_cell.py # Insert mapping-table cell at index 6
python fix_mapping_cell.py    # Move misplaced mapping cell to correct position
```

### Install Dependencies

```bash
pip install pandas openpyxl jupyter python-dotenv
# python-dotenv is required for Supabase credential injection
```

### Supabase Setup — DONE

Supabase está conectado. Proyecto: `tfdxcjbxmrhrcjgbknnt.supabase.co`. Tabla `pedidos` creada con RLS habilitado y política `allow_all`. Credenciales en `.env` local (gitignored) e inyectadas en el HTML generado.

Para regenerar el HTML con las credenciales (siempre correr esto después de cambiar `html_template.py`):

```bash
python3 generar_html.py
```

`generar_html.py` lee el `.env` via `python-dotenv` e inyecta `__SUPABASE_URL__` / `__SUPABASE_KEY__` en el HTML. Si `SUPABASE_URL` está vacío, el app cae back a `localStorage` automáticamente.

Para Vercel: agregar `SUPABASE_URL` y `SUPABASE_KEY` en Settings → Environment Variables (mismos valores que el `.env` local). Luego redeploy.

### PWA Install (after deploying to Vercel)
- **Android Chrome:** tap "Instalar app" banner or menu → "Agregar a pantalla de inicio"
- **iOS Safari:** menú compartir → "Agregar a inicio"
- The service worker caches the HTML shell for offline use; Supabase API calls always go through the network.

### Export Results

```bash
# Excel export is the last cell in the notebook — outputs comparativa_resultado.xlsx
# Run notebook or trigger cell manually in Jupyter
```

---

## 2. Codebase Architecture & Key Files

### Entrypoints

| File | Purpose |
|---|---|
| `generar_html.py` | **Primary deliverable generator.** Reads both Excel files, classifies products, resolves prices, and renders `petinsa_envios.html`. Entry point for producing the app. |
| `comparativa_agencias.ipynb` | **Interactive analysis notebook.** Used for exploration, verification, and generating `comparativa_resultado.xlsx`. |
| `petinsa_envios.html` | **Standalone HTML+JS app** for PETINSA staff — no Python needed at runtime. Generated output, not edited directly. |

### PWA Static Files (served by Vercel alongside the HTML)

| File | Purpose |
|---|---|
| `manifest.json` | PWA manifest — app name, theme color, start URL, icon reference. Required for "Add to Home Screen". |
| `sw.js` | Service worker — caches HTML/CDN assets for offline use, passes Supabase API calls through unchanged. Cache versioned as `petinsa-v1`; increment on breaking changes. |
| `icon.svg` | App icon — dark blue (#1a3a5c) background with white truck. Used by Android Chrome; iOS uses a page screenshot as fallback. |

### Core Business Logic

| File | Responsibility |
|---|---|
| `generar_html_data.py` | `classify(familia, desc)` — the central classification function mapping each product to one of 14 unified categories using family name + regex on description. Also defines `UNIFIED_CATS` dict and `MAPPING` dict. |
| `generar_html.py` | Loads Excel data, calls `classify()`, resolves agency prices via `build_prices()`, serializes JSON, and injects it into the HTML template. Also contains `pick_price_col()` (GONFER special case), `parse_canje()`, `parse_freq()`. |
| `html_template.py` | Raw HTML/CSS/JS string for the frontend app. Contains the search UI, ranking logic, and canje toggle — all client-side. |

### Data Layer

| File | Role |
|---|---|
| `COMPARATIVA AGENCIAS.xlsx` | Source of truth for tariffs — 18 sheets (one per month). Sheet `Costo ag. Mayo 2026` is the active one. Row 5 = agency names, row 2 = canje, row 4 = frequency, row 7+ = categories + prices. |
| `Libro1.xlsx` | PETINSA's ERP product catalog — 1,437 products. Key columns: `Prod.`, `Descripción de Producto`, `Familia`, `Ramo`, `Stock`, `P. Lista`. |
| `Categorias_Agencias_Clasificacion_Productos.xlsx` | Teammate's file with 16 unified categories × 14 agencies tarifario + product classification. Recommended as master table. |
| `comparativa_resultado.xlsx` | Generated output — not a source file, overwritten on every notebook run. |

### Critical Configuration

- **`html_template.py` is the active template** — `generar_html.py` imports `HTML_TEMPLATE` from it at generation time. All UI/JS changes go in `html_template.py`. The inline template in `generar_html.py` (lines ~351-1127) is legacy and overridden by the import.
- **PWA cache version** (`sw.js` line 2: `const CACHE = 'petinsa-v1'`): increment the version string (e.g., `petinsa-v2`) whenever the app shell changes significantly so old caches are purged on next visit.
- **`MAPPING` dict** (in `generar_html_data.py` and duplicated in `generar_html.py`): Maps `{agency_name: {unified_cat_key: agency_label_string}}`. This is the core lookup table. Any change to agency category names in the tariff Excel requires updating this dict.
- **`UNIFIED_CATS` dict**: The 14 unified category keys and their human-readable names. These keys are the stable internal identifiers used everywhere.
- **`IVA = 1.22`**: GONFER publishes prices without IVA. This multiplier is applied only to GONFER prices during parsing.
- **Active sheet name**: `'Costo ag. Mayo 2026'` is hardcoded in `generar_html.py` line ~254. Update this every month.

---

## 3. Development Guidelines & Patterns

### Data Flow

```
Libro1.xlsx
    └─► classify(familia, desc) → unified_cat key (e.g. 'cub_auto_r15_r19')

COMPARATIVA AGENCIAS.xlsx
    └─► parse sheet → agency_prices_norm: {agency: {norm(label): price}}

MAPPING dict
    └─► {agency: {unified_cat: label}} (links the two above)

build_prices(MAPPING)
    └─► prices_data: {agency: {unified_cat: effective_price_iva_incl}}
        └─► JSON-embedded in HTML or used directly in notebook
```

**Canje formulas (tres métricas diferenciadas):**
```python
neto  = bruto * (1 - canje)           # Cashflow: plata que sale de la empresa
costo = bruto * (1 - 0.25 * canje)    # Costo verdadero: considera que cubiertas de canje tienen markup 25%
# Interpretación B (pendiente): neto = bruto * (1 - canje * (1 - margen_costo_goma))
```
El ranking en Modo 1 y Modo 2 usa `costo` (costo verdadero). La columna "Total neto" sigue mostrando el cashflow.

### Naming Conventions

- **Unified category keys**: `snake_case`, prefixed by type: `cub_`, `bateria_`, `lubricante_`, `camara`, `bulto_general`
- **Functions**: `snake_case` — `classify()`, `extract_rim()`, `extract_amp()`, `norm()`, `build_prices()`, `parse_canje()`, `parse_freq()`
- **Notebook utility scripts**: `verb_noun.py` pattern (`add_optimizer.py`, `fix_mapping_cell.py`, `rebuild_nb.py`)
- **Variables in notebook**: `df` = product DataFrame, `df_out` = export view, `agencies_list` = ordered list of 14 agency names, `agency_canje` / `agency_freq` / `agency_meta` = per-agency metadata dicts
- **Column naming in exports**: Spanish, human-readable (`Descripción`, `Familia`, `Mejor Agencia`)

### `norm()` — Use Everywhere for String Matching

The `norm()` function is the canonical normalizer for all string comparisons against Excel data:

```python
def norm(s):
    # strips whitespace, lowercases, removes accents, normalizes \xa0
```

**Always use `norm()` when looking up agency category labels from the parsed Excel.** Raw string comparison will fail due to accents, case, and non-breaking spaces.

### `classify()` — Rule Priority Order Matters

The `classify(familia, desc)` function uses an `if/elif` chain. The order is intentional:
1. `LUBRICANTE` check first (avoids false match on other families)
2. `BATERIA` before generic checks
3. `ACCES`/`CAM MOTO` (accessories/chambers) before `MOTO`
4. `GIGANTE`/`VIAL`/`IND.` before `PASEO`/`CAMIONETA`
5. `PASEO` and `CAMIONETA` last among tires

Do not reorder these branches. Families like `VIALES/IND.` would otherwise fall through to wrong categories.

### Error Handling

- Missing products: logged with `print(f"ADVERTENCIA: codigo {cod!r} no encontrado en Libro1")` — no exceptions raised.
- Missing prices (`None`): silently excluded from ranking; agencies without a price for a category are shown as `'N/A'` or `'—'` in mapping tables.
- GONFER IVA: handled at parse time via multiplier, not at query time.
- No try/except for Excel loading — if files are missing or misnamed, the script crashes with a raw openpyxl/FileNotFoundError (intentional for dev workflow).

### Notebook Cell Injection Scripts

When adding new cells to `comparativa_agencias.ipynb`, the pattern is always:
```python
nb = json.load(open('comparativa_agencias.ipynb'))
# ... build cell dict with {"cell_type","execution_count":None,"metadata":{},"outputs":[],"source":src}
nb['cells'].insert(idx, new_cell)
json.dump(nb, open('comparativa_agencias.ipynb','w'), ensure_ascii=False, indent=1)
```
Use `rebuild_nb.py` as the reference for how cells are ordered.

---

## 4. Known Gotchas & Constraints

### MAPPING is duplicated
`MAPPING` and `UNIFIED_CATS` are defined identically in both `generar_html_data.py` and `generar_html.py`. If you update category labels or add a new agency, **update both files**. This is intentional (notebook and HTML generator are independent pipelines) but easy to forget.

### GONFER has no IVA — multiplier only applies at parse time
GONFER's raw prices in the Excel are pre-IVA. The `IVA = 1.22` multiplier is applied when building `prices_data`. If you add any new price comparison path, remember to check `agency_meta[ag] == 'sin IVA'` before comparing prices.

### Active month sheet is hardcoded
`'Costo ag. Mayo 2026'` appears hardcoded in `generar_html.py`. When a new monthly tariff is added to the Excel, this string must be updated manually.

### `extract_rim()` has three fallback patterns — order matters
```python
# Pattern 1: "14.9 - 24" → matches " - 24"   (agrícolas with space-dash-space)
# Pattern 2: "7.50-16"   → matches "-16"      (radiales with dash)
# Pattern 3: "175/65 R14"→ matches "R14"      (metric format)
```
Pattern 1 catches agrícola formats before pattern 2 to avoid grabbing the wrong number (e.g., in `14.9 - 24`, pattern 2 would grab `9` not `24`).

### Agencies with 100% canje — costo verdadero resuelve el problema
SELEGUIN, TRUJILLO, y Franchi tienen `canje=1.0` → `neto = $0`. Antes siempre rankeaban #1, lo cual era engañoso. Ahora el ranking usa `costo = bruto × 0.75` para estas agencias, reflejando que las cubiertas entregadas en canje tienen un costo real del 75% del precio lista. Interpretación B (slider `margen_costo_goma`) sigue pendiente como mejora futura.

### 8 agencies lack explicit mapping rules in the notebook's original `matcher.py` spec
BULEVAR, PERICO, TRUJILLO, GONFER, 3EME, Martin Escudero, Arzuaga, Franchi — their mappings exist in `MAPPING` but were originally fallback-only. In `generar_html.py`/`generar_html_data.py`, all 14 agencies now have explicit `MAPPING` entries.

### `Prod.` column type is inconsistent
Product codes come from the ERP as floats (e.g., `20046.0`). `buscar_producto()` handles this with `.rstrip('.0')` normalization. When querying by product code, always convert via `str(cod).strip().rstrip('.0')`.

### `Arzuaga` has two price columns (Young/Paysandú vs Trinidad)
`pick_price_col()` selects `ci[1]` (second column) for most agencies — for Arzuaga this defaults to the Young/Paysandú price. The Trinidad price is not surfaced in the current implementation.

---

## 5. Required Skills & Approach Guidelines

These are the skill areas that must be applied when working on this project. Read these before writing any code.

### Clean Code
- **Single responsibility:** each function does one thing. `classify()` classifies, `norm()` normalizes, `build_prices()` builds prices. Don't merge concerns.
- **No magic numbers:** rim thresholds (14, 19, 22.5, 24, 28, 30, 38), amp threshold (110), IVA (1.22) must be named constants or clearly commented, never bare literals scattered through the code.
- **Avoid duplication:** `MAPPING` and `UNIFIED_CATS` are already duplicated across two files — this is a known debt. Don't add more duplication. If a third script needs them, import from a shared module.
- **Keep scripts short and purposeful:** the notebook injection scripts (`rebuild_nb.py`, `add_optimizer.py`) are each ~150 lines and do exactly one job. New utility scripts should follow the same discipline.

### UI/UX for Non-Technical Users
- **The end user is a PETINSA warehouse worker, not a developer.** The HTML app must require zero technical knowledge.
- **All user-facing text must be in Spanish** — labels, error messages, column headers, button text, tooltips. No English in the UI.
- **Results must be scannable at a glance:** the Top 3 ranking with clear cost display is the primary output. Don't bury the answer in tables.
- **Fail gracefully with friendly messages:** if a product isn't found or a price is missing, show a clear Spanish message — never a raw error or blank output.
- **Mobile-aware:** Bootstrap 5 is already in use. All new UI components must use Bootstrap classes and be responsive. Test mentally at ~375px width (phone).
- **Autocomplete and search must be forgiving:** product descriptions contain accents, abbreviations, and mixed casing — always use `norm()` before comparing.

### Frontend Stack (HTML app only)
- **Bootstrap 5.3.3** + **Bootstrap Icons 1.11.3** — use for all layout, components, and icons. Do not introduce other CSS frameworks.
- **Chart.js 4.4.3** — already loaded for charts. Use it if visualization is needed; don't add other charting libraries.
- **Vanilla JavaScript only** — no React, Vue, jQuery, or other frameworks. The app is a single standalone `.html` file with no build step. Keep it that way.
- **All JS is embedded in the HTML template** (`html_template.py`). New frontend logic goes there, not in separate `.js` files.

### Mobile / PWA Guidelines
- **`html,body { overflow-x: hidden }`** is set globally — never add `width > 100vw` elements.
- **All inputs must have `font-size: 16px` on mobile** — the `@media (max-width:575px)` block in `html_template.py` enforces this to prevent iOS auto-zoom.
- **Touch targets: 44px minimum** — primary buttons (`.btn-p`, `.btn-warning`) and `.form-control` enforce `min-height: 44px` in the mobile media query.
- **`@media (hover:none)`** block suppresses hover effects on touch devices — keep it up to date when adding new hover styles.
- **Supabase async pattern**: all storage functions (`loadOrders`, `saveOrder`, `deleteOrder`) are `async` and use `fetch()` directly against the Supabase REST API. `SUPABASE_URL` and `SUPABASE_KEY` are injected at build time by `generar_html.py` from `.env`. If `SUPABASE_URL` is empty, functions fall back to `localStorage`.
- **Service worker scope**: `sw.js` is at repo root → scope `/`. The HTML is at `/petinsa_envios.html`. Both are covered. Do not move `sw.js` to a subdirectory or the scope will break.

### Data Handling & Defensive Coding
- **Assume Excel data is dirty.** Cells can be `None`, empty strings, floats where strings are expected, `\xa0` non-breaking spaces. Always sanitize with `norm()` and guard with `if value and isinstance(value, ...)`.
- **Never trust column positions.** The tariff Excel has a non-standard layout (agency names at row 5, prices from row 7). When parsing new sheets or adding new months, re-verify the row/col offsets — they can shift.
- **Type coercion for product codes:** always `str(cod).strip().rstrip('.0')` — never compare raw ERP codes as floats or ints.
- **`None` prices are valid:** an agency legitimately may not ship a product type (e.g., SELEGUIN has `None` for `lubricante_tambor`). Treat `None` as "does not apply", not as an error.

### Regex & Classification
- **The `extract_rim()` function is fragile** — it handles 3 tire format families. Before adding a new regex pattern, test against all existing formats: `205/65 R15`, `14.9 - 24`, `7.50-16`, `LT215/85 R16`, `90/90-18`.
- **The `classify()` if/elif chain is load-bearing.** Any new product family must be inserted at the correct priority position (see Section 3). Always add a comment explaining why the new branch sits where it does.

### Spanish Domain Knowledge (Tires)
- **Rodado = rim diameter in inches.** R14 = 14-inch rim. Agrícola uses different notation (e.g., `14.9-24` means the rim is 24 inches).
- **Canje = barter percentage.** Not a discount — PETINSA pays that portion with physical tires, not cash. 100% canje = zero cash cost, but non-zero real cost.
- **Familia vs Ramo:** Familia is the top-level ERP grouping (18 total), Ramo is the commercial line (54 total). `classify()` uses Familia; the notebook uses both.
- **IVA = 22% in Uruguay.** GONFER is the only agency that publishes pre-IVA prices. All other prices in the Excel are already IVA-inclusive.

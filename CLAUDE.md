# CLAUDE.md

## ESTADO ACTUAL Y PRÓXIMOS PASOS

### Lo que está hecho y funcionando
- **Calculadora de envíos** — busca productos, arma pedido, ranking de agencias por costo real (una sola agencia por pedido)
- **Fórmula de costo real con canje** — `costo = bruto × (1 - canje × (1 - %costo_mercadería))`. Slider ajustable (default 60%). Diferencia: tarifa bruta · efectivo (cashflow) · costo real (costo económico considerando el costo de la mercadería entregada en canje).
- **14 agencias** con precios, canje y frecuencia desde `COMPARATIVA AGENCIAS.xlsx` (hoja activa: `Costo ag. Mayo 2026`)
- **Filtro por destino** — dropdown con los 19 departamentos de Uruguay (hardcodeado). Al seleccionar departamento, filtra agencias que cubren ese destino usando `AG_DEST`. El aviso "no encontrado" solo aparece si hay datos de cobertura Y el departamento no matchea ninguna agencia (no aparece si `AG_DEST` está vacío).
- **Autocomplete de clientes** — 635 clientes con localidad cargados desde Excel ("Clientes - dpto - radios activo"). Al seleccionar un cliente se completa automáticamente el campo Localidad. Opción para crear nuevos clientes (se guardan en localStorage).
- **Búsqueda accent-insensitive** con `normStr()` en todos los autocompletes y catálogo
- **Escanear Llanta** — tab con cámara/upload de imagen. Tesseract.js (OCR, corre en el browser, sin costo) lee el código de medida (ej: 205/55 R16) y busca productos coincidentes en el catálogo. En mobile abre la cámara trasera directo.
- **Dashboard** con KPIs, gráficas Chart.js e historial de pedidos
- **Supabase integration** — conectado y funcionando; tablas `pedidos` y `stock` creadas; credenciales inyectadas en `.env` y en el HTML generado; fallback a localStorage si no hay credenciales
- **Control de stock en tiempo real** — tabla `stock` en Supabase con 1.436 productos y sus stocks iniciales desde Libro1.xlsx. Al guardar un pedido, la RPC `save_order_and_decrement_stock` descuenta automáticamente el stock de cada producto en la misma transacción. Si el stock no alcanza, el pedido no se guarda y el usuario ve el error.
- **PWA** — `manifest.json`, `sw.js`, `icon.svg` listos; se activa automáticamente al deployar en Vercel (HTTPS)
- **Mobile responsive** — Bootstrap 5, media query @575px, touch targets 44px, iOS no-zoom inputs, tabs icon-only en mobile, overflow-x:hidden
- **Autenticación** — login con email/password vía Supabase Auth. Rol `admin` ve todo (incluyendo Dashboard); rol `tenant` ve solo Calcular Envío, Escanear Llanta y Catálogo. Sesión en sessionStorage (se limpia al cerrar el tab). Botón "Salir" en navbar.

### Deploy
- **URL de producción:** `ml-proyecto.vercel.app/petinsa_envios.html`
- Repo `BrunoPignanelli/ML-Proyecto` rama `main` conectado a Vercel — cada merge a `main` redeploya automáticamente
- Variables de entorno `SUPABASE_URL` y `SUPABASE_KEY` configuradas en Vercel
- PWA activo en producción (HTTPS) — instalable desde Chrome/Safari en el teléfono
- **Rama de desarrollo activa:** `pri` — los cambios se desarrollan ahí y se mergean a `main` cuando están aprobados

### Usuarios Supabase Auth (creados 2026-06-11)
| Email | Role |
|---|---|
| brunixbruno1010@gmail.com | admin |
| ddaronch@petinsa.com.uy | admin |
| priscilagerlach9@gmail.com | admin |

Para crear nuevos usuarios (tenant o admin): usar el service role key vía `POST /auth/v1/admin/users` con `user_metadata: {"role": "admin"|"tenant"}`.

---

## 0. Deployment Constraint

**The app must remain a static site deployable on Vercel via GitHub.**

Current architecture: Python runs locally to generate `petinsa_envios.html` (a self-contained HTML+JS file with data embedded as JSON). Vercel serves that file statically — no server-side Python at runtime. This is intentional and must be preserved.

All features must use client-side JS only. No external paid APIs — the tire scanner uses Tesseract.js (runs in the browser, free, no API key). The only external services are Supabase (free tier) for data persistence and Auth.

The app is a **PWA (Progressive Web App)**. Once hosted on Vercel (HTTPS), users can install it on their phone home screen from Chrome/Safari — it opens full-screen like a native app and works offline for the app shell. The PWA shell files (`manifest.json`, `sw.js`, `icon.svg`) are static files committed to the repo.

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
```

### Install Dependencies

```bash
pip install pandas openpyxl jupyter python-dotenv
```

### Supabase Setup — DONE

Supabase está conectado. Proyecto: `tfdxcjbxmrhrcjgbknnt.supabase.co`. Credenciales en `.env` local (gitignored) e inyectadas en el HTML generado.

```bash
# Siempre correr esto después de cambiar html_template.py
python3 generar_html.py

# Re-cargar stock inicial desde Libro1.xlsx (correr si se actualiza el Excel)
SUPABASE_SERVICE_KEY=sb_secret_... python3 cargar_stock_inicial.py
```

`generar_html.py` lee el `.env` via `python-dotenv` e inyecta `__SUPABASE_URL__` / `__SUPABASE_KEY__` en el HTML. Si `SUPABASE_URL` está vacío, el app cae back a `localStorage`.

---

## 2. Codebase Architecture & Key Files

### Entrypoints

| File | Purpose |
|---|---|
| `generar_html.py` | **Primary deliverable generator.** Reads Excel files, builds catalog + prices + clients + agency destinations, renders `petinsa_envios.html`. Run after any change to `html_template.py`. |
| `html_template.py` | **Active HTML/CSS/JS template.** All UI and logic changes go here. Imported by `generar_html.py`. |
| `petinsa_envios.html` | **Generated output** — standalone app for PETINSA. Never edit directly; always regenerate. |

### PWA Static Files

| File | Purpose |
|---|---|
| `manifest.json` | PWA manifest — name, theme, icon, start URL |
| `sw.js` | Service worker — caches shell for offline. Cache key: `petinsa-v1` — increment on breaking changes |
| `icon.svg` | App icon |

### Core Business Logic

| File | Responsibility |
|---|---|
| `generar_html_data.py` | `classify(familia, desc)` — maps products to 14 unified shipping categories. Also `UNIFIED_CATS` and `MAPPING` dicts. |
| `generar_html.py` | Loads Excel data, classifies products, resolves agency prices, parses client list + agency destinations, serializes JSON, injects into template. |
| `html_template.py` | All frontend: HTML structure, CSS (Bootstrap 5), JavaScript logic (search, canje calc, Tesseract OCR, Supabase calls, auth). |

### Data Layer

| File | Role |
|---|---|
| `COMPARATIVA AGENCIAS.xlsx` | Tarifas — hoja activa: `Costo ag. Mayo 2026`. Actualizar nombre de hoja mensualmente en `generar_html.py`. |
| `Libro1.xlsx` | Catálogo ERP de PETINSA — 1.437 productos. También fuente del stock inicial. |
| `cargar_stock_inicial.py` | Script one-time para seedear/re-cargar la tabla `stock` en Supabase desde Libro1.xlsx. Requiere `SUPABASE_SERVICE_KEY` en `.env`. |
| `Clientes según departamento y Agencias con localidades.xlsx` | Hoja 2 "Clientes - dpto - radios activo": 635 clientes con localidad. Hoja 3 "Destinos de agencias": cobertura por agencia. |

### Critical Configuration

- **`html_template.py` es el template activo** — la template inline en `generar_html.py` (legado) es ignorada por el import al final.
- **Placeholders en el template**: `__CATALOG__`, `__AGENCIES__`, `__PRICES__`, `__UCATS__`, `__AG_NAMES__`, `__CLIENTS__`, `__AG_DESTINATIONS__`, `__SUPABASE_URL__`, `__SUPABASE_KEY__`
- **Hoja activa del tarifario**: `'Costo ag. Mayo 2026'` hardcodeada en `generar_html.py`. Actualizar mensualmente.
- **`MAPPING` duplicado**: definido en `generar_html_data.py` Y en `generar_html.py`. Actualizar ambos si se cambian categorías o agencias.

---

## 3. Fórmula de Costo Real con Canje

```
Costo real = bruto × (1 - canje × (1 - %costo_mercadería))
Efectivo   = bruto × (1 - canje)
```

- `%costo_mercadería`: costo de la mercadería entregada en canje como % de su precio de venta. Ajustable con slider (default 60%).
- El ranking de agencias siempre usa **costo real** (no efectivo ni bruto).
- Una agencia con 100% canje y mercadería al 60% de costo tiene costo real = 60% de la tarifa bruta (no es gratis).

Funciones JS en `html_template.py`:
- `getPctCosto()` — lee el slider
- `getEfectivo(ag, uc)` — cashflow
- `getCostoReal(ag, uc)` — costo económico real (usado para ranking)

---

## 4. Escanear Llanta (OCR)

**Tecnología:** Tesseract.js v4 (corre en el browser, sin costo, sin API).

**Flujo:**
1. Usuario sube imagen o toma foto (en mobile abre cámara trasera con `capture="environment"`)
2. Tesseract.js extrae todo el texto de la imagen
3. Regex busca patrones de medida: `205/55 R16`, `7.50-16`, `14.9-24`, `LT215/85R16`
4. Se parsea ancho / perfil / rodado
5. Se busca en CATALOG por rodado obligatorio + términos adicionales
6. Resultados con botón "Agregar al pedido"

**Patrones de regex en `parsearMedidaLlanta(text)`:**
- Métrico: `\d{3}/\d{2,3}\s*[Rr]\s*\d{2}` (ej: 205/55 R16)
- Convencional: `\d+[.,]\d+[-\s]\d{2}` (ej: 7.50-16)
- Agrícola: `\d+[.,]\d+\s*-\s*\d{2}` (ej: 14.9 - 24)

---

## 5. Development Guidelines

### Calcular Envío
- Un pedido va por **una única agencia** — no hay Modo 2 (fue eliminado).
- El filtro por destino (`agVaADestino`) usa `AG_DEST` (del Excel), aplica `normStr` para comparar. Si la agencia no tiene datos de destino, no se filtra.
- Si el destino no coincide con ninguna agencia conocida → aviso amarillo + muestra todas.

### UI/UX
- **Todos los textos en español** — sin inglés en la UI.
- **Mobile-first**: touch targets ≥44px, font-size 16px en inputs (iOS no-zoom), tabs icon-only en mobile.
- **Bootstrap 5.3.3** + Bootstrap Icons — no introducir otros frameworks CSS.
- **Vanilla JS only** — no React, Vue, jQuery. El HTML es un único archivo autocontenido.
- Tesseract.js se carga desde CDN solo cuando se usa el tab "Escanear Llanta".

### Data Handling
- Excel puede tener celdas `None`, `\xa0`, floats donde se esperan strings → siempre usar `norm()` en Python y `normStr()` en JS.
- Códigos de producto del ERP vienen como floats (ej: `20046.0`) → normalizar con `str(cod).strip().rstrip('.0')`.
- `None` en precio = la agencia no cubre esa categoría (no es error).

### Naming
- Categorías unificadas: `snake_case` con prefijos `cub_`, `bateria_`, `lubricante_`, `camara`, `bulto_general`
- Funciones JS: `camelCase` — `getBruto`, `getEfectivo`, `getCostoReal`, `agVaADestino`, `cliSearch`, `analizarLlanta`

---

## 6. Known Gotchas

- **`MAPPING` duplicado** en `generar_html_data.py` y `generar_html.py` — actualizar ambos si cambian categorías.
- **GONFER sin IVA** — multiplica por `IVA = 1.22` al parsear. No aplicar de nuevo en consultas.
- **Hoja del tarifario hardcodeada** — `'Costo ag. Mayo 2026'` en `generar_html.py`. Actualizar cada mes.
- **Arzuaga tiene dos columnas de precio** (Young/Paysandú vs Trinidad) — `pick_price_col()` usa la segunda. Trinidad no está expuesta.
- **Tesseract.js en mobile**: la calidad del OCR depende de la nitidez de la foto. Si falla, el usuario puede tipear la medida manualmente en el buscador del catálogo.
- **`.env` requerido localmente** para que las credenciales Supabase se inyecten. Sin `.env`, el HTML generado cae a localStorage.
- **Stock en Supabase vs stock en CATALOG**: el campo `st` embebido en el HTML es un snapshot de lectura (para el tab Catálogo). El stock autoritativo y vivo está en la tabla `stock` de Supabase — solo se modifica vía la RPC al guardar pedidos.
- **`saveOrder()` usa RPC, no REST directo**: desde 2026-06-19, guardar un pedido llama `POST /rest/v1/rpc/save_order_and_decrement_stock` en lugar de `POST /rest/v1/pedidos`. La tabla `stock` tiene RLS sin políticas — el anon key no puede escribirla directamente; solo la RPC (SECURITY DEFINER) puede.
- **Schema real de `pedidos`**: columnas `fecha, nped, cliente, destino, vendedor, obs, canje_modo, lineas, m1_agencia, m1_bru, m1_net, m2_net, m2_ags`. No existe `pct_costo` — el campo JS homónimo no se persiste en la DB. La RPC inserta solo las columnas que existen.
- **Destino es `<select>`, no `<input>`**: el campo `f-dest` es un `<select>` con los 19 departamentos. Los clientes cuya `localidad` sea el nombre exacto del departamento (ej: "Artigas") se auto-completan; los que tienen ciudad (ej: "Bella Union") dejan el select vacío.
- **`SUPABASE_SERVICE_KEY` solo para scripts locales** — nunca se embebe en el HTML. Se usa únicamente en `cargar_stock_inicial.py`.

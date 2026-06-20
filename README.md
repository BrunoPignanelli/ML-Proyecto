# PETINSA — Sistema de Envíos

App web para cotizar y gestionar envíos de llantas y repuestos automotores.
Desarrollada para PETINSA (Uruguay) como proyecto del curso de Machine Learning.

## Descripción

El sistema permite a los vendedores de PETINSA:

- **Calcular el costo de envío** de un pedido a cualquier departamento del Uruguay, comparando 14 agencias de transporte en tiempo real.
- **Escanear llantas con la cámara del celular**: OCR (Tesseract.js) lee el código de medida impreso en la goma (ej: `205/55 R16`) y busca los productos coincidentes en el catálogo.
- **Consultar el catálogo** de 1.437 productos con stock en tiempo real.
- **Registrar pedidos** con descuento automático de stock (transacción atómica en Supabase).
- **Dashboard** con KPIs, historial de pedidos y gráficas de ventas.

La app es una **PWA (Progressive Web App)**: se puede instalar en el celular desde Chrome/Safari y funciona como una app nativa.

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | HTML + CSS (Bootstrap 5) + JavaScript vanilla |
| OCR | Tesseract.js v4 (corre en el browser, sin costo) |
| Backend / DB | Supabase (PostgreSQL + Auth + RLS) |
| Build | Python 3.9 + openpyxl + pandas |
| Deploy | Vercel (static hosting, deploy automático desde GitHub) |
| PWA | manifest.json + Service Worker |

> **Sin servidor en runtime.** Python corre localmente para generar el HTML; Vercel sirve ese archivo estático. Todo el procesamiento ocurre en el browser del usuario.

## Requisitos

- Python 3.9+
- Acceso a los archivos Excel de datos (ver sección siguiente)
- (Opcional) Cuenta en Supabase para persistencia de pedidos y stock

```bash
pip install pandas openpyxl python-dotenv
```

## Archivos de datos requeridos

Deben estar en la raíz del proyecto:

| Archivo | Contenido |
|---|---|
| `Libro1.xlsx` | Catálogo ERP con 1.437 productos (hoja `Hoja1`) |
| `COMPARATIVA AGENCIAS.xlsx` | Tarifas de 14 agencias (hoja `Costo ag. Mayo 2026`) |
| `Clientes según departamento y Agencias con localidades.xlsx` | 635 clientes + cobertura de destinos (opcional) |

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```
SUPABASE_URL=https://<proyecto>.supabase.co
SUPABASE_KEY=<anon_key>
```

Sin `.env` el app funciona igual pero usa `localStorage` en lugar de Supabase (sin persistencia entre dispositivos ni control de stock).

## Ejecución

```bash
# Regenerar la app tras cualquier cambio en el código o los Excel
python generar_html.py
# → produce petinsa_envios.html (~400 KB); abrir en el browser
```

```bash
# Cargar stock inicial a Supabase (una sola vez, o al actualizar Libro1.xlsx)
SUPABASE_SERVICE_KEY=<service_role_key> python cargar_stock_inicial.py
```

Para desarrollar localmente con OCR funcional, servir el archivo via HTTP (Tesseract.js requiere HTTP, no funciona con `file://`):

```bash
python3 -m http.server 8787
# → abrir http://localhost:8787/petinsa_envios.html
```

## Estructura del proyecto

```
generar_html.py              Script principal: lee Excel, clasifica productos, genera HTML
generar_html_data.py         Clasificación en 17 categorías de envío + MAPPING de agencias
html_template.py             Template HTML/CSS/JS (modificar aquí, nunca en el .html)
cargar_stock_inicial.py      Script one-time: carga la tabla stock en Supabase

Libro1.xlsx                  Catálogo ERP — 1.437 productos con stock
COMPARATIVA AGENCIAS.xlsx    Tarifas y canje de 14 agencias (actualizar mensualmente)
Clientes según...xlsx        Clientes con localidad + cobertura de destinos por agencia

petinsa_envios.html          Output generado — NO editar manualmente
manifest.json                PWA manifest (nombre, ícono, colores)
sw.js                        Service Worker — caché offline del shell de la app
icon.svg                     Ícono de la PWA
```

## Arquitectura

```
Excel (Libro1.xlsx, COMPARATIVA AGENCIAS.xlsx, Clientes.xlsx)
        │
        ▼  python generar_html.py
┌───────────────────────────────────┐
│  generar_html_data.py             │
│  classify(familia, desc)          │  ← clasifica cada producto en 1 de 17 categorías
│  MAPPING[agencia][cat] = label    │  ← traduce categoría a columna del Excel de tarifas
└───────────────┬───────────────────┘
                │ serializa CATALOG, PRICES, CLIENTS, AG_DESTINATIONS como JSON
                ▼
        petinsa_envios.html          ← app completa en un solo archivo
                │
        ┌───────┴────────┐
        │                │
  Browser del usuario   Supabase
  (JS vanilla,          (pedidos, stock,
   Tesseract.js,         autenticación)
   Bootstrap 5)
        │
        ▼  git push origin main
      Vercel (deploy automático)
  ml-proyecto.vercel.app/petinsa_envios.html
```

## Fórmula de costo real con canje

Las agencias cobran parte en mercadería (canje) en lugar de efectivo. El costo real considera el costo de esa mercadería:

```
Costo real = tarifa_bruta × (1 - canje × (1 - %costo_mercadería))
Efectivo   = tarifa_bruta × (1 - canje)
```

Donde `%costo_mercadería` es el costo de la mercadería entregada en canje como porcentaje de su precio de venta (ajustable con slider, default 60%).

## Base de datos (Supabase)

Tablas principales:

| Tabla | Descripción |
|---|---|
| `pedidos` | Historial de pedidos con líneas, agencia, costos y modo de canje |
| `stock` | Stock en tiempo real de cada producto (decrementado al guardar pedido) |

El stock se descuenta mediante la RPC `save_order_and_decrement_stock` (transacción atómica: si el stock no alcanza, el pedido no se guarda).

RLS activo en ambas tablas. Rol `admin` accede a todo; rol `tenant` solo a Calcular Envío, Escanear Llanta y Catálogo.

## Deploy

El repo `BrunoPignanelli/ML-Proyecto` en GitHub está conectado a Vercel. Cada merge a la rama `main` redeploya automáticamente.

```bash
# Mergear cambios a producción
git checkout main
git merge <rama-de-desarrollo>
git push origin main
```

URL de producción: `ml-proyecto.vercel.app/petinsa_envios.html`

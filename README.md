# PETINSA — Sistema de Envíos

App web para cotizar envíos de llantas y repuestos automotores.
Genera un único archivo HTML autocontenido con todos los datos embebidos como JSON.
Deploy estático en Vercel; persistencia y autenticación vía Supabase (free tier).

## Entorno

**Python 3.9+**

```bash
pip install pandas openpyxl python-dotenv
```

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```
SUPABASE_URL=https://<proyecto>.supabase.co
SUPABASE_KEY=<anon_key>
```

Sin `.env` el app funciona igual pero usa `localStorage` en lugar de Supabase.

## Ejecución

```bash
# Comando principal — regenerar la app tras cualquier cambio
python generar_html.py
# → produce petinsa_envios.html (~400 KB); abrir en el browser
```

```bash
# Cargar stock inicial a Supabase (una sola vez, o al actualizar Libro1.xlsx)
SUPABASE_SERVICE_KEY=<service_role_key> python cargar_stock_inicial.py
```

## Estructura de archivos

```
generar_html.py           Script principal: lee Excel, clasifica productos, genera HTML
generar_html_data.py      Lógica de clasificación en 17 categorías de envío + MAPPING de agencias
html_template.py          Template HTML/CSS/JS de la app (modificar aquí, nunca en el .html)
cargar_stock_inicial.py   Script one-time: seedea la tabla stock en Supabase

Libro1.xlsx               Catálogo ERP — 1.437 productos con stock
COMPARATIVA AGENCIAS.xlsx Tarifas y porcentaje de canje de 14 agencias (actualizar mensualmente)
Clientes según...xlsx     635 clientes con localidad + cobertura de destinos por agencia

petinsa_envios.html       Output generado — NO editar manualmente
manifest.json / sw.js     Archivos PWA (instalable en el celular desde Chrome/Safari)
```

## Arquitectura

```
Excel (Libro1.xlsx, COMPARATIVA AGENCIAS.xlsx)
        ↓ generar_html.py
    Catalog JSON + Prices JSON + Clients JSON
        ↓ inyectados en html_template.py
    petinsa_envios.html  ←→  Supabase (pedidos + stock en tiempo real)
        ↓ git push origin main
    Vercel (deploy automático)
```

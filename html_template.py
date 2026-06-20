"""
Template HTML — PETINSA Sistema de Envios
Se importa desde generar_html.py
"""

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PETINSA - Envios</title>
<meta name="theme-color" content="#1a3a5c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="PETINSA">
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/icon.svg">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
<style>
:root{--azul:#1a3a5c;--azul-c:#e8f0f8;--azul-m:#2c5282;}
html,body{overflow-x:hidden;}
body{background:#f4f6f9;font-size:.91rem;}
.navbar{background:var(--azul)!important;}
.tab-btn{cursor:pointer;padding:.45rem 1.1rem;border:none;background:transparent;
         border-bottom:3px solid transparent;color:#555;font-weight:500;}
.tab-btn.active{border-bottom-color:var(--azul);color:var(--azul);font-weight:700;}
.tab-btn:hover:not(.active){background:#f0f0f0;border-radius:4px 4px 0 0;}
.card{border:none;box-shadow:0 1px 6px rgba(0,0,0,.09);border-radius:10px;}
.ch{background:var(--azul);color:#fff;border-radius:10px 10px 0 0;padding:.65rem 1rem;font-weight:600;}
.btn-p{background:var(--azul);color:#fff;border:none;}
.btn-p:hover{background:#142d47;color:#fff;}
#ac-box{position:absolute;z-index:9999;background:#fff;border:1px solid #ccc;
        border-radius:0 0 8px 8px;width:100%;max-height:270px;overflow-y:auto;
        box-shadow:0 4px 14px rgba(0,0,0,.18);top:100%;left:0;}
.ac-it{padding:.42rem .8rem;cursor:pointer;border-bottom:1px solid #f0f0f0;}
.ac-it:hover{background:var(--azul-c);}
.ac-cod{font-weight:700;color:var(--azul);margin-right:.4rem;font-size:.82rem;}
.ac-fam{font-size:.76rem;color:#888;}
.bcat{background:var(--azul-c);color:var(--azul);border-radius:20px;padding:1px 8px;font-size:.74rem;}
.rank-1{background:#fff9e6;}.rank-2{background:#f0fff4;}.rank-3{background:#f0f8ff;}
.neto0{color:#198754;font-weight:700;}
.ptag{font-weight:600;color:var(--azul);}
.qty-inp{width:68px!important;text-align:center;}
.cat-tr:hover{background:var(--azul-c);cursor:pointer;}
.pg-btn{cursor:pointer;padding:3px 9px;border-radius:5px;border:1px solid #ddd;
        margin:0 2px;background:#fff;font-size:.84rem;}
.pg-btn.active{background:var(--azul);color:#fff;border-color:var(--azul);}
#ocnt{background:var(--azul);color:#fff;border-radius:50%;padding:0 5px;font-size:.72rem;margin-left:3px;}
.field-row label{font-weight:600;font-size:.84rem;color:#444;}
.kpi-card{border:none!important;border-radius:12px!important;}
.chart-wrap{position:relative;height:220px;}
.toast-container{position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;}
#cli-ac-box{position:absolute;z-index:9998;background:#fff;border:1px solid #ccc;
            border-radius:0 0 8px 8px;width:100%;max-height:240px;overflow-y:auto;
            box-shadow:0 4px 14px rgba(0,0,0,.18);top:100%;left:0;}
.cli-ac-it{padding:.42rem .8rem;cursor:pointer;border-bottom:1px solid #f0f0f0;display:flex;justify-content:space-between;align-items:center;}
.cli-ac-it:hover{background:var(--azul-c);}
.cli-ac-loc{font-size:.78rem;color:#888;white-space:nowrap;margin-left:.5rem;}
.cli-ac-new{padding:.42rem .8rem;cursor:pointer;color:var(--azul);font-size:.85rem;font-weight:600;border-top:1px solid #e0e0e0;}
.cli-ac-new:hover{background:var(--azul-c);}
.ag-sin-cobert{opacity:.45;}
.dest-badge{display:inline-block;font-size:.72rem;background:#e8f0f8;color:#1a3a5c;border-radius:20px;padding:1px 7px;margin-left:.4rem;}
@media print{
  nav,.tab-btn,#results-btns,.card-header button,#f-obs-row{display:none!important;}
  .card{box-shadow:none!important;border:1px solid #ddd!important;}
}
@media (max-width:575px){
  body{font-size:.875rem;}
  .container-fluid{padding-left:.65rem!important;padding-right:.65rem!important;}
  /* Tabs: equal-width, icon-only */
  .tab-btn{flex:1;padding:.7rem .2rem;font-size:.78rem;text-align:center;white-space:nowrap;}
  .tab-txt{display:none;}
  /* Inputs: 16px prevents iOS zoom; 44px min-height for touch */
  input,select,.form-control,.form-select,.form-control-sm{font-size:16px!important;}
  .form-control,.form-select{min-height:44px;}
  .form-control-sm{min-height:40px;}
  /* Touch targets for primary buttons */
  .btn-p,.btn-warning{min-height:44px;font-size:.9rem;}
  /* Card padding reduction */
  .card-body{padding:.6rem!important;}
  .ch{padding:.5rem .75rem!important;font-size:.87rem;}
  /* Qty input in order table */
  .qty-inp{width:56px!important;}
  /* Autocomplete: cap at 40% of viewport height */
  #ac-box{max-height:40vh;}
  .ac-it{padding:.65rem .75rem;}
  /* Charts */
  .chart-wrap{height:175px;}
  /* Summary cards: reduce large price font */
  #summary-cards .fs-3{font-size:1.25rem!important;}
  /* Flex gap reduction */
  .gap-4{gap:.5rem!important;}
  .gap-3{gap:.4rem!important;}
}
/* Suppress hover effects on touch-only devices */
@media (hover:none){
  .tab-btn:hover:not(.active){background:transparent!important;}
  .cat-tr:hover{background:transparent!important;}
  .btn-p:hover{background:var(--azul)!important;}
}
/* Login overlay */
#login-overlay{position:fixed;inset:0;background:var(--azul);z-index:9999;display:flex;align-items:center;justify-content:center;}
#login-card{background:#fff;border-radius:12px;padding:2rem;width:100%;max-width:360px;box-shadow:0 8px 32px rgba(0,0,0,.25);}
#login-card .logo{font-size:1.5rem;font-weight:700;color:var(--azul);margin-bottom:.25rem;}
#login-card .sub{font-size:.85rem;color:#666;margin-bottom:1.5rem;}
</style>
</head>
<body>

<!-- LOGIN OVERLAY -->
<div id="login-overlay" style="display:none">
  <div id="login-card">
    <div class="logo"><i class="bi bi-truck me-2"></i>PETINSA</div>
    <div class="sub">Sistema de Envios &mdash; Iniciar sesion</div>
    <div class="mb-3">
      <label class="form-label fw-semibold small">Email</label>
      <input id="l-email" type="email" class="form-control" placeholder="usuario@petinsa.com" autocomplete="username">
    </div>
    <div class="mb-3">
      <label class="form-label fw-semibold small">Contrasena</label>
      <input id="l-pass" type="password" class="form-control" placeholder="••••••••" autocomplete="current-password"
             onkeydown="if(event.key===\'Enter\')doLogin()">
    </div>
    <div id="l-err" class="text-danger small mb-2" style="display:none"></div>
    <button class="btn btn-p w-100" id="l-btn" onclick="doLogin()">Ingresar</button>
  </div>
</div>

<!-- NAVBAR -->
<nav class="navbar navbar-dark px-3 py-2 mb-0">
  <span class="navbar-brand fw-bold fs-5 text-truncate" style="max-width:65vw">
    <i class="bi bi-truck me-2"></i>PETINSA<span class="d-none d-sm-inline"> &mdash; Sistema de Envios</span>
  </span>
  <span class="text-white-50 small d-none d-sm-inline">Tarifas Mayo 2026</span>
  <div id="btn-logout" style="display:none" class="ms-auto d-flex align-items-center gap-2">
    <span id="user-label" class="text-white-50 small d-none d-sm-inline"></span>
    <button class="btn btn-sm btn-outline-light py-0" onclick="doLogout()">
      <i class="bi bi-box-arrow-right me-1"></i><span class="d-none d-sm-inline">Salir</span>
    </button>
  </div>
</nav>

<div class="container-fluid px-3 pt-3">

  <!-- TABS -->
  <div class="d-flex border-bottom mb-3">
    <button class="tab-btn active" id="btn-calc" onclick="showTab('calc')">
      <i class="bi bi-calculator"></i><span class="tab-txt ms-1">Calcular Envio</span>
      <span id="ocnt" style="display:none">0</span>
    </button>
    <button class="tab-btn" id="btn-scan" onclick="showTab('scan')">
      <i class="bi bi-camera"></i><span class="tab-txt ms-1">Escanear Llanta</span>
    </button>
    <button class="tab-btn" id="btn-cat" onclick="showTab('cat')">
      <i class="bi bi-grid"></i><span class="tab-txt ms-1">Catalogo</span>
    </button>
    <button class="tab-btn" id="btn-dash" onclick="showTab('dash')">
      <i class="bi bi-bar-chart-line"></i><span class="tab-txt ms-1">Dashboard</span>
    </button>
  </div>

  <!-- ===== TAB CALCULADORA ===== -->
  <div id="tab-calc">
    <div class="row g-3">

      <!-- Datos del pedido -->
      <div class="col-12">
        <div class="card">
          <div class="ch"><i class="bi bi-file-text me-2"></i>Datos del pedido</div>
          <div class="card-body">
            <div class="row g-2">
              <div class="col-12 col-sm-4 col-md-2">
                <label class="form-label mb-1 fw-semibold small">N&deg; Pedido</label>
                <input id="f-nped" class="form-control form-control-sm" placeholder="Ej: 00123">
              </div>
              <div class="col-12 col-sm-8 col-md-3">
                <label class="form-label mb-1 fw-semibold small">Cliente</label>
                <div class="position-relative">
                  <input id="f-cliente" class="form-control form-control-sm" placeholder="Nombre del cliente" autocomplete="off">
                  <div id="cli-ac-box" style="display:none"></div>
                </div>
              </div>
              <div class="col-12 col-sm-6 col-md-3">
                <label class="form-label mb-1 fw-semibold small">Localidad / Destino</label>
                <select id="f-dest" class="form-select form-select-sm">
                  <option value="">— Departamento —</option>
                  <option>Artigas</option>
                  <option>Canelones</option>
                  <option>Cerro Largo</option>
                  <option>Colonia</option>
                  <option>Durazno</option>
                  <option>Flores</option>
                  <option>Florida</option>
                  <option>Lavalleja</option>
                  <option>Maldonado</option>
                  <option>Montevideo</option>
                  <option>Paysandú</option>
                  <option>Río Negro</option>
                  <option>Rivera</option>
                  <option>Rocha</option>
                  <option>Salto</option>
                  <option>San José</option>
                  <option>Soriano</option>
                  <option>Tacuarembó</option>
                  <option>Treinta y Tres</option>
                </select>
                <div id="dest-aviso" class="small text-warning mt-1" style="display:none"><i class="bi bi-exclamation-triangle me-1"></i>Destino no encontrado en coberturas — mostrando todas las agencias</div>
              </div>
              <div class="col-6 col-sm-3 col-md-2">
                <label class="form-label mb-1 fw-semibold small">Fecha</label>
                <input id="f-fecha" type="date" class="form-control form-control-sm">
              </div>
              <div class="col-6 col-sm-3 col-md-2">
                <label class="form-label mb-1 fw-semibold small">Vendedor</label>
                <input id="f-vendedor" class="form-control form-control-sm" placeholder="Nombre">
              </div>
              <div class="col-12" id="f-obs-row">
                <label class="form-label mb-1 fw-semibold small">Observaciones</label>
                <input id="f-obs" class="form-control form-control-sm" placeholder="Opcional">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Buscador -->
      <div class="col-12">
        <div class="card">
          <div class="ch"><i class="bi bi-search me-2"></i>Agregar productos al pedido</div>
          <div class="card-body pb-2">
            <div class="position-relative">
              <input id="prod-search" class="form-control"
                     placeholder="Buscar por codigo, descripcion o ramo..."
                     autocomplete="off">
              <div id="ac-box" style="display:none"></div>
            </div>
            <div class="text-muted small mt-1">Minimo 2 caracteres para buscar</div>
          </div>
        </div>
      </div>

      <!-- Lineas del pedido -->
      <div class="col-12">
        <div class="card">
          <div class="ch d-flex justify-content-between align-items-center">
            <span><i class="bi bi-cart3 me-2"></i>Lineas del pedido</span>
            <div>
              <button class="btn btn-sm btn-light me-2" onclick="clearOrder()">
                <i class="bi bi-x-circle me-1"></i>Limpiar
              </button>
              <button class="btn btn-sm btn-warning fw-bold" onclick="calculate()">
                <i class="bi bi-calculator me-1"></i>Calcular envio
              </button>
            </div>
          </div>
          <div class="card-body p-0">
            <div id="order-empty" class="text-center text-muted py-4">
              <i class="bi bi-cart3 fs-2 d-block mb-2 opacity-30"></i>
              Busca productos arriba para armar el pedido
            </div>
            <div class="table-responsive">
            <table class="table table-sm mb-0" id="order-table" style="display:none">
              <thead class="table-light">
                <tr>
                  <th>Codigo</th><th>Descripcion</th><th class="d-none d-sm-table-cell">Categoria envio</th>
                  <th class="text-center" style="width:80px">Cant.</th>
                  <th style="width:36px"></th>
                </tr>
              </thead>
              <tbody id="order-body"></tbody>
            </table>
            </div>
          </div>
        </div>
      </div>

      <!-- RESULTADOS -->
      <div class="col-12" id="results-section" style="display:none">

        <!-- Canje -->
        <div class="card mb-3">
          <div class="card-body py-2">
            <div class="d-flex flex-wrap align-items-center gap-3">
              <span class="fw-semibold small"><i class="bi bi-percent me-1"></i>% costo mercadería sobre venta:</span>
              <input type="range" min="0" max="100" value="60" id="margin-sl" class="form-range" style="width:140px;">
              <span id="margin-lbl" class="fw-bold" style="min-width:2.5rem;">60%</span>
              <span class="text-muted small">Costo real = efectivo + canje × <span id="margin-lbl2">60%</span></span>
            </div>
          </div>
        </div>

        <!-- Summary cards -->
        <div class="row g-3 mb-3" id="summary-cards"></div>

        <!-- Ranking agencias -->
        <div class="card mb-3">
          <div class="ch"><i class="bi bi-trophy me-2"></i>Ranking de agencias para este pedido</div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-sm table-hover mb-0">
                <thead class="table-light"><tr>
                  <th>#</th><th>Agencia</th>
                  <th class="text-end d-none d-sm-table-cell">Tarifa bruta</th>
                  <th class="text-end d-none d-sm-table-cell">Efectivo</th>
                  <th class="text-end">Costo real</th>
                  <th>Canje</th>
                  <th class="d-none d-sm-table-cell">Frecuencia</th>
                  <th class="d-none d-sm-table-cell">Dias/sem</th>
                </tr></thead>
                <tbody id="m1-body"></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Botones de accion -->
        <div id="results-btns" class="d-flex gap-2 flex-wrap mb-3">
          <button class="btn btn-p" onclick="guardarPedido()">
            <i class="bi bi-save me-1"></i>Guardar pedido
          </button>
          <button class="btn btn-outline-secondary" onclick="downloadCSV()">
            <i class="bi bi-download me-1"></i>Descargar CSV
          </button>
          <button class="btn btn-outline-secondary" onclick="window.print()">
            <i class="bi bi-printer me-1"></i>Imprimir
          </button>
        </div>

      </div><!-- /results -->
    </div><!-- /row -->
  </div><!-- /tab-calc -->

  <!-- ===== TAB ESCANEAR LLANTA ===== -->
  <div id="tab-scan" style="display:none">
    <div class="row g-3">

      <!-- Captura -->
      <div class="col-12">
        <div class="card">
          <div class="ch"><i class="bi bi-camera me-2"></i>Escanear llanta</div>
          <div class="card-body">
            <p class="text-muted small mb-3">Sacá una foto o subí una imagen de la llanta. El sistema lee el código (ej: <strong>205/55 R16</strong>) y busca el producto en el catálogo.</p>
            <div class="d-flex flex-wrap gap-2 mb-3">
              <!-- En mobile abre la camara; en desktop abre el selector de archivo -->
              <label class="btn btn-p" for="scan-input" style="cursor:pointer;min-height:44px;display:flex;align-items:center;">
                <i class="bi bi-camera me-2"></i>Tomar / subir foto
              </label>
              <input id="scan-input" type="file" accept="image/*" capture="environment" style="display:none">
              <button class="btn btn-warning fw-bold" id="scan-btn" onclick="analizarLlanta()" disabled style="min-height:44px;">
                <i class="bi bi-cpu me-1"></i>Analizar con IA
              </button>
            </div>
            <!-- Preview -->
            <div id="scan-preview-wrap" style="display:none" class="mb-3">
              <img id="scan-preview" src="" alt="preview" class="img-fluid rounded" style="max-height:280px;object-fit:contain;border:2px solid var(--azul-c);">
            </div>
            <!-- Resultado lectura -->
            <div id="scan-result" style="display:none"></div>
          </div>
        </div>
      </div>

      <!-- Productos encontrados -->
      <div class="col-12">
        <div id="scan-productos" style="display:none">
          <div class="card">
            <div class="ch" id="scan-prod-title"><i class="bi bi-list-ul me-2"></i>Productos encontrados</div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-sm table-hover mb-0">
                  <thead class="table-light"><tr>
                    <th>Codigo</th><th>Descripcion</th><th>Familia</th>
                    <th class="text-center">Stock</th><th></th>
                  </tr></thead>
                  <tbody id="scan-prod-body"></tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div><!-- /tab-scan -->

  <!-- ===== TAB CATALOGO ===== -->
  <div id="tab-cat" style="display:none">
    <div class="card">
      <div class="ch"><i class="bi bi-grid me-2"></i>Catalogo de Productos</div>
      <div class="card-body">
        <div class="row g-2 mb-3">
          <div class="col-12 col-md-5">
            <input id="cat-q" class="form-control" placeholder="Buscar codigo, descripcion, ramo...">
          </div>
          <div class="col-12 col-md-3">
            <select id="cat-fam" class="form-select"><option value="">Todas las familias</option></select>
          </div>
          <div class="col-12 col-md-4 d-flex align-items-center justify-content-start justify-content-md-end">
            <span id="cat-cnt" class="text-muted small"></span>
          </div>
        </div>
        <div class="table-responsive">
          <table class="table table-sm table-hover mb-0">
            <thead class="table-light"><tr>
              <th>Codigo</th><th>Descripcion</th><th>Familia</th><th>Ramo</th>
              <th class="text-end">P. Lista</th>
              <th class="text-end">Stock</th>
              <th class="text-end">Disp. 30d</th>
              <th class="text-end">Meses Stk</th>
              <th>Cat. Envio</th><th></th>
            </tr></thead>
            <tbody id="cat-body"></tbody>
          </table>
        </div>
        <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
          <span class="text-muted small" id="cat-pg-info"></span>
          <div id="cat-pg" class="d-flex flex-wrap gap-1"></div>
        </div>
      </div>
    </div>
  </div><!-- /tab-cat -->

  <!-- ===== TAB DASHBOARD ===== -->
  <div id="tab-dash" style="display:none">

    <!-- KPI cards -->
    <div class="row g-3 mb-3" id="dash-kpis"></div>

    <!-- Sin datos -->
    <div id="dash-empty" class="text-center py-5 text-muted" style="display:none">
      <i class="bi bi-bar-chart-line fs-1 d-block mb-3 opacity-25"></i>
      <h5>No hay pedidos guardados</h5>
      <p>Calculen y guarden pedidos en la pestana "Calcular Envio" para ver el tablero.</p>
    </div>

    <div id="dash-content" style="display:none">
      <!-- Graficos fila 1 -->
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="ch"><i class="bi bi-trophy me-1"></i>Productos mas enviados (top 10)</div>
            <div class="card-body"><div class="chart-wrap"><canvas id="ch-prods"></canvas></div></div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100">
            <div class="ch"><i class="bi bi-geo-alt me-1"></i>Destinos frecuentes (top 10)</div>
            <div class="card-body"><div class="chart-wrap"><canvas id="ch-dests"></canvas></div></div>
          </div>
        </div>
      </div>

      <!-- Graficos fila 2 -->
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="ch"><i class="bi bi-people me-1"></i>Clientes que mas compran (top 10)</div>
            <div class="card-body"><div class="chart-wrap"><canvas id="ch-clis"></canvas></div></div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100">
            <div class="ch"><i class="bi bi-pie-chart me-1"></i>Gasto neto por agencia (Modo 1)</div>
            <div class="card-body"><div class="chart-wrap"><canvas id="ch-ags"></canvas></div></div>
          </div>
        </div>
      </div>

      <!-- Historial de pedidos -->
      <div class="card mb-3">
        <div class="ch d-flex justify-content-between align-items-center">
          <span><i class="bi bi-clock-history me-2"></i>Historial de pedidos guardados</span>
          <div>
            <button class="btn btn-sm btn-light me-2" onclick="exportHistorial()">
              <i class="bi bi-download me-1"></i>Exportar historial
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="borrarDatos()">
              <i class="bi bi-trash3 me-1"></i>Borrar datos
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-sm table-hover mb-0">
              <thead class="table-light"><tr>
                <th>Fecha</th><th>N&deg; Ped.</th><th>Cliente</th><th>Destino</th>
                <th>Vendedor</th><th>Productos</th>
                <th class="text-end">Total neto</th>
                <th>Agencia</th><th></th>
              </tr></thead>
              <tbody id="hist-body"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div><!-- /tab-dash -->

</div><!-- /container -->

<!-- Modal Nuevo Cliente -->
<div class="modal fade" id="modal-nuevo-cli" tabindex="-1">
  <div class="modal-dialog modal-sm">
    <div class="modal-content">
      <div class="modal-header" style="background:var(--azul);color:#fff;padding:.75rem 1rem;">
        <h6 class="modal-title mb-0"><i class="bi bi-person-plus me-2"></i>Nuevo cliente</h6>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <label class="form-label small fw-semibold">Nombre</label>
          <input id="ncli-nombre" class="form-control form-control-sm" placeholder="Nombre del cliente">
        </div>
        <div class="mb-1">
          <label class="form-label small fw-semibold">Localidad / Destino</label>
          <input id="ncli-loc" class="form-control form-control-sm" placeholder="Ciudad de destino" onkeydown="if(event.key==='Enter')confirmarNuevoCli()">
        </div>
      </div>
      <div class="modal-footer" style="padding:.6rem 1rem;">
        <button class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
        <button class="btn btn-p btn-sm" onclick="confirmarNuevoCli()"><i class="bi bi-check2 me-1"></i>Guardar</button>
      </div>
    </div>
  </div>
</div>

<!-- Toast -->
<div class="toast-container">
  <div id="main-toast" class="toast text-white border-0 align-items-center" role="alert">
    <div class="d-flex">
      <div class="toast-body fw-semibold" id="toast-msg">OK</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>
  </div>
</div>

<!-- ===== DATOS ===== -->
<script>
const CATALOG       = __CATALOG__;
const AGENCIES      = __AGENCIES__;
const PRICES        = __PRICES__;
const UCATS         = __UCATS__;
const AG_NAMES      = __AG_NAMES__;
const CLIENTS       = __CLIENTS__;
const AG_DEST       = __AG_DESTINATIONS__;
</script>

<!-- ===== LOGICA ===== -->
<script>
// ── Estado ────────────────────────────────────────────────────────────────
const order = new Map();
let catFiltered = [], catPage = 1;
const PG = 25;
let lastM1 = [], lastTot1 = 0;
let chartInstances = {};
const LS_KEY = 'petinsa_orders_v1';
const SUPABASE_URL = '__SUPABASE_URL__';
const SUPABASE_KEY = '__SUPABASE_KEY__';
const SB_HEADERS = {
  'apikey': SUPABASE_KEY,
  'Authorization': 'Bearer ' + SUPABASE_KEY,
  'Content-Type': 'application/json',
  'Prefer': 'return=minimal'
};
// Returns headers with the logged-in user's JWT, refreshing silently if near expiry
async function getAuthHeaders() {
  const raw = localStorage.getItem(AUTH_KEY);
  if (!raw) return SB_HEADERS;
  let session = JSON.parse(raw);
  if (session.refresh && session.expires_at && Date.now() > session.expires_at - 300000) {
    session = await refreshSession(session.refresh) || session;
  }
  return { ...SB_HEADERS, 'Authorization': 'Bearer ' + (session.token || SUPABASE_KEY) };
}
async function refreshSession(refreshToken) {
  try {
    const r = await fetch(SUPABASE_URL + '/auth/v1/token?grant_type=refresh_token', {
      method: 'POST',
      headers: { 'apikey': SUPABASE_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken })
    });
    if (!r.ok) throw new Error();
    const data = await r.json();
    const role = data.user?.user_metadata?.role || 'tenant';
    const session = {
      token: data.access_token,
      refresh: data.refresh_token,
      role,
      email: data.user?.email || '',
      expires_at: Date.now() + ((data.expires_in || 3600) * 1000)
    };
    localStorage.setItem(AUTH_KEY, JSON.stringify(session));
    return session;
  } catch(e) {
    localStorage.removeItem(AUTH_KEY);
    $('login-overlay').style.display = 'flex';
    return null;
  }
}
const AZUL = '#1a3a5c';
const COLORS = ['#1a3a5c','#2196F3','#4CAF50','#FF9800','#E91E63',
                '#9C27B0','#00BCD4','#FF5722','#607D8B','#795548'];

// ── Utils ─────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const fmt   = n => (n===null||n===undefined||isNaN(n)) ? '-' : '$' + Math.round(n).toLocaleString('es-UY');
const today = () => new Date().toISOString().slice(0,10);
const esc   = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const normStr = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();

function showToast(msg, type='success') {
  const t = $('main-toast');
  t.className = 'toast text-white border-0 align-items-center bg-' + type;
  $('toast-msg').textContent = msg;
  bootstrap.Toast.getOrCreateInstance(t, {delay:3000}).show();
}

// ── Tabs ─────────────────────────────────────────────────────────────────
function showTab(t) {
  ['calc','scan','cat','dash'].forEach(id => {
    $('tab-'+id).style.display = (t===id) ? '' : 'none';
    $('btn-'+id).classList.toggle('active', t===id);
  });
  if (t === 'dash') buildDashboard();
}

// ── Autocomplete ─────────────────────────────────────────────────────────
let acResults = [], acIdx = -1;

function acSearch(q) {
  const box = $('ac-box');
  if (q.length < 2) { box.style.display='none'; acResults=[]; return; }
  const ql = normStr(q);
  acResults = CATALOG.filter(p =>
    normStr(p.c).includes(ql) ||
    normStr(p.d).includes(ql) ||
    normStr(p.r).includes(ql)
  ).slice(0, 14);
  if (!acResults.length) { box.style.display='none'; return; }
  box.innerHTML = acResults.map((p,i) =>
    '<div class="ac-it" data-i="'+i+'">' +
    '<span class="ac-cod">'+esc(p.c)+'</span>'+esc(p.d.substring(0,65))+
    '<br><span class="ac-fam">'+esc(p.f)+' &middot; '+esc(p.cn)+'</span></div>'
  ).join('');
  box.querySelectorAll('.ac-it').forEach(el => {
    el.addEventListener('mousedown', e => {
      e.preventDefault();
      addProduct(acResults[parseInt(el.dataset.i)]);
    });
  });
  box.style.display = '';
  acIdx = -1;
}

function acKey(e) {
  const n = acResults.length;
  if (!n) return;
  if (e.key==='ArrowDown') { acIdx=Math.min(acIdx+1,n-1); hlAC(); e.preventDefault(); }
  else if (e.key==='ArrowUp') { acIdx=Math.max(acIdx-1,0); hlAC(); e.preventDefault(); }
  else if (e.key==='Enter' && acIdx>=0) { addProduct(acResults[acIdx]); e.preventDefault(); }
  else if (e.key==='Escape') { $('ac-box').style.display='none'; }
}
function hlAC() {
  $('ac-box').querySelectorAll('.ac-it').forEach((el,i) =>
    el.style.background = i===acIdx ? 'var(--azul-c)' : '');
}

const srch = $('prod-search');
srch.addEventListener('input', () => acSearch(srch.value.trim()));
srch.addEventListener('keydown', acKey);
document.addEventListener('click', e => {
  if (!e.target.closest('#prod-search') && !e.target.closest('#ac-box'))
    $('ac-box').style.display='none';
});

// ── Clientes ──────────────────────────────────────────────────────────────
const CLI_KEY = 'petinsa_clientes_v1';
function loadCustomClients() {
  try { return JSON.parse(localStorage.getItem(CLI_KEY)||'[]'); } catch(e) { return []; }
}
function saveClient(nombre, localidad) {
  const list = loadCustomClients();
  const n = normStr(nombre).trim();
  const exists = list.find(c => normStr(c.nombre).trim() === n);
  if (exists) { exists.localidad = localidad; }
  else { list.push({ nombre: nombre.trim(), localidad: localidad.trim() }); }
  localStorage.setItem(CLI_KEY, JSON.stringify(list));
}
function allClients() {
  const custom = loadCustomClients();
  const base = Array.isArray(CLIENTS) ? CLIENTS : [];
  const seen = new Set(custom.map(c => normStr(c.nombre)));
  return [...custom, ...base.filter(c => !seen.has(normStr(c.nombre)))];
}

let cliAcIdx = -1, cliAcResults = [];

function cliSearch(q) {
  const box = $('cli-ac-box');
  if (q.length < 2) { box.style.display='none'; cliAcResults=[]; return; }
  const ql = normStr(q);
  cliAcResults = allClients().filter(c => normStr(c.nombre).includes(ql)).slice(0, 12);
  const exactMatch = cliAcResults.some(c => normStr(c.nombre) === ql);
  let html = cliAcResults.map((c,i) =>
    '<div class="cli-ac-it" data-i="'+i+'">'+
    '<span>'+esc(c.nombre)+'</span>'+
    '<span class="cli-ac-loc">'+esc(c.localidad||'')+'</span></div>'
  ).join('');
  if (!exactMatch) {
    html += '<div class="cli-ac-new" id="cli-ac-new"><i class="bi bi-person-plus me-1"></i>Crear cliente "<strong>'+esc(q)+'</strong>"</div>';
  }
  if (!html) { box.style.display='none'; return; }
  box.innerHTML = html;
  box.querySelectorAll('.cli-ac-it').forEach(el => {
    el.addEventListener('mousedown', e => { e.preventDefault(); selectClient(cliAcResults[parseInt(el.dataset.i)]); });
  });
  const newBtn = document.getElementById('cli-ac-new');
  if (newBtn) newBtn.addEventListener('mousedown', e => { e.preventDefault(); abrirNuevoCli(q); });
  box.style.display = '';
  cliAcIdx = -1;
}
function selectClient(c) {
  $('f-cliente').value = c.nombre;
  $('f-dest').value = c.localidad || '';
  $('cli-ac-box').style.display = 'none';
  cliAcResults = [];
  if ($('results-section').style.display !== 'none') doCalc();
}
function abrirNuevoCli(nombre) {
  $('ncli-nombre').value = nombre;
  $('ncli-loc').value = '';
  $('cli-ac-box').style.display = 'none';
  new bootstrap.Modal(document.getElementById('modal-nuevo-cli')).show();
  setTimeout(() => $('ncli-loc').focus(), 400);
}
function confirmarNuevoCli() {
  const nombre = $('ncli-nombre').value.trim();
  const loc = $('ncli-loc').value.trim();
  if (!nombre) { $('ncli-nombre').focus(); return; }
  saveClient(nombre, loc);
  $('f-cliente').value = nombre;
  $('f-dest').value = loc;
  bootstrap.Modal.getInstance(document.getElementById('modal-nuevo-cli')).hide();
  showToast('Cliente guardado ✓', 'success');
  if ($('results-section').style.display !== 'none') doCalc();
}
const cliInp = $('f-cliente');
cliInp.addEventListener('input', () => cliSearch(cliInp.value.trim()));
cliInp.addEventListener('keydown', e => {
  const n = cliAcResults.length;
  if (e.key==='ArrowDown') { cliAcIdx=Math.min(cliAcIdx+1,n-1); hlCliAC(); e.preventDefault(); }
  else if (e.key==='ArrowUp') { cliAcIdx=Math.max(cliAcIdx-1,0); hlCliAC(); e.preventDefault(); }
  else if (e.key==='Enter' && cliAcIdx>=0) { selectClient(cliAcResults[cliAcIdx]); e.preventDefault(); }
  else if (e.key==='Escape') { $('cli-ac-box').style.display='none'; }
});
function hlCliAC() {
  $('cli-ac-box').querySelectorAll('.cli-ac-it').forEach((el,i) =>
    el.style.background = i===cliAcIdx ? 'var(--azul-c)' : '');
}
document.addEventListener('click', e => {
  if (!e.target.closest('#f-cliente') && !e.target.closest('#cli-ac-box'))
    $('cli-ac-box').style.display='none';
});
$('f-dest').addEventListener('change', () => {
  if ($('results-section').style.display !== 'none') doCalc();
});

// ── Pedido ────────────────────────────────────────────────────────────────
function addProduct(p) {
  $('ac-box').style.display='none'; srch.value=''; acResults=[];
  if (order.has(p.c)) order.get(p.c).qty += 1;
  else order.set(p.c, Object.assign({}, p, {qty:1}));
  renderOrder();
  $('results-section').style.display='none';
}

function removeItem(cod) { order.delete(cod); renderOrder(); $('results-section').style.display='none'; }
function updateQty(cod, val) {
  const q = parseInt(val);
  if (isNaN(q)||q<=0) { removeItem(cod); return; }
  if (order.has(cod)) order.get(cod).qty = q;
}
function clearOrder() { order.clear(); renderOrder(); $('results-section').style.display='none'; }

function renderOrder() {
  const n = order.size;
  $('ocnt').textContent = n; $('ocnt').style.display = n>0 ? '' : 'none';
  $('order-empty').style.display = n===0 ? '' : 'none';
  $('order-table').style.display = n>0   ? '' : 'none';
  $('order-body').innerHTML = [...order.values()].map(p =>
    '<tr>' +
    '<td><code>'+esc(p.c)+'</code></td>' +
    '<td>'+esc(p.d.substring(0,55))+'</td>' +
    '<td class="d-none d-sm-table-cell"><span class="bcat">'+esc(p.cn)+'</span></td>' +
    '<td class="text-center"><input type="number" class="form-control form-control-sm qty-inp d-inline-block"'+
      ' value="'+p.qty+'" min="1" data-cod="'+esc(p.c)+'"></td>' +
    '<td><button class="btn btn-sm btn-outline-danger py-0" data-cod="'+esc(p.c)+'">'+
      '<i class="bi bi-trash3"></i></button></td>' +
    '</tr>'
  ).join('');
  $('order-body').querySelectorAll('input[data-cod]').forEach(el =>
    el.addEventListener('change', () => updateQty(el.dataset.cod, el.value)));
  $('order-body').querySelectorAll('button[data-cod]').forEach(el =>
    el.addEventListener('click', () => removeItem(el.dataset.cod)));
}

// ── Calculo ───────────────────────────────────────────────────────────────
function getPctCosto() { return parseFloat($('margin-sl').value) / 100; }
function getBruto(ag, uc) { return ((PRICES[ag]||{})[uc]) ?? null; }
// Efectivo = lo que sale de caja
function getEfectivo(ag, uc) {
  const b = getBruto(ag, uc); if (b===null) return null;
  const a = AGENCIES.find(x => x.nombre===ag);
  return b * (1 - (a ? a.canje : 0));
}
// Costo real = efectivo + canje × %costo_mercadería
// = bruto × (1 - canje × (1 - %costo))
function getCostoReal(ag, uc) {
  const b = getBruto(ag, uc); if (b===null) return null;
  const a = AGENCIES.find(x => x.nombre===ag);
  const cj = a ? a.canje : 0;
  return b * (1 - cj * (1 - getPctCosto()));
}
// Mantener getNeto como alias de getCostoReal para compatibilidad interna
function getNeto(ag, uc) { return getCostoReal(ag, uc); }
function getCosto(ag, uc) { return getCostoReal(ag, uc); }
function getRankScore(ag, uc) { return getCostoReal(ag, uc); }

function calculate() {
  if (!order.size) { alert('Agrega productos al pedido primero.'); return; }
  $('results-section').style.display = '';
  doCalc();
  $('results-section').scrollIntoView({behavior:'smooth'});
}

function agVaADestino(agNombre, destino) {
  if (!destino) return true;
  const d = normStr(destino);
  const dests = AG_DEST[agNombre];
  if (!dests || !dests.length) return true; // sin datos → no filtrar
  return dests.some(loc => {
    const l = normStr(loc);
    return l.includes(d) || d.includes(l);
  });
}

function doCalc() {
  const lines = [...order.values()].map(p =>
    ({cod:p.c, desc:p.d.substring(0,55), cat:p.cn, uc:p.uc, qty:p.qty}));
  const destino = ($('f-dest').value || '').trim();

  // Agencias que van al destino (o todas si no hay destino)
  const agsActivas = AGENCIES.filter(a =>
    AG_NAMES.includes(a.nombre) && agVaADestino(a.nombre, destino));

  // Aviso solo si hay datos de cobertura Y el destino no aparece en ninguna agencia
  const agsConDatos = AGENCIES.filter(a =>
    AG_NAMES.includes(a.nombre) && (AG_DEST[a.nombre]||[]).length > 0);
  const hayFiltro = destino && agsConDatos.length > 0 &&
    agsConDatos.some(a => agVaADestino(a.nombre, destino));
  $('dest-aviso') && ($('dest-aviso').style.display =
    (destino && agsConDatos.length > 0 && !hayFiltro) ? '' : 'none');

  const m1 = agsActivas.map(ag => {
    let bru=0, efect=0, cost=0; const mis=[];
    for (const l of lines) {
      const b=getBruto(ag.nombre,l.uc), e=getEfectivo(ag.nombre,l.uc), c=getCostoReal(ag.nombre,l.uc);
      if (b===null) mis.push(l.cat);
      else { bru+=b*l.qty; efect+=e*l.qty; cost+=c*l.qty; }
    }
    return {ag, bru, efect:mis.length?null:efect, cost:mis.length?null:cost, mis};
  }).filter(r=>r.cost!==null).sort((a,b)=>a.cost-b.cost||a.bru-b.bru);

  lastM1=[...m1];
  lastTot1 = m1.length ? m1[0].cost : 0;

  renderM1(m1);
  renderSummary(m1);
}

$('margin-sl').addEventListener('input', () => {
  const v = $('margin-sl').value + '%';
  $('margin-lbl').textContent = v;
  $('margin-lbl2').textContent = v;
  if ($('results-section').style.display!=='none') doCalc();
});

// ── Render Modo 1 ─────────────────────────────────────────────────────────
function renderM1(rows) {
  const medals=['&#127945;','&#127946;','&#127947;'];
  $('m1-body').innerHTML = rows.map((r,i) => {
    const cls=i<3?'rank-'+(i+1):'';
    return '<tr class="'+cls+'">'+
      '<td>'+(medals[i]||i+1+'.')+'</td>'+
      '<td class="fw-semibold">'+esc(r.ag.nombre)+'</td>'+
      '<td class="text-end text-muted d-none d-sm-table-cell">'+fmt(r.bru)+'</td>'+
      '<td class="text-end text-muted d-none d-sm-table-cell">'+fmt(r.efect)+'</td>'+
      '<td class="text-end"><span class="ptag">'+fmt(r.cost)+'</span></td>'+
      '<td><span class="badge bg-secondary">'+Math.round(r.ag.canje*100)+'%</span></td>'+
      '<td class="d-none d-sm-table-cell">'+esc(r.ag.freq)+'</td>'+
      '<td class="text-center d-none d-sm-table-cell"><span class="badge '+(r.ag.dias>=5?'bg-success':'bg-warning text-dark')+'">'+
        r.ag.dias+'d</span></td>'+
      '</tr>';
  }).join('');
}

// ── Render Summary ────────────────────────────────────────────────────────
function renderSummary(m1) {
  if (!m1.length) { $('summary-cards').innerHTML=''; return; }
  const best=m1[0];
  const pedInfo=[
    $('f-nped').value?'Pedido #'+$('f-nped').value:'',
    $('f-cliente').value,
    $('f-dest').value
  ].filter(Boolean).join(' | ');
  $('summary-cards').innerHTML=
    '<div class="col-sm-6 col-lg-4"><div class="card text-white" style="background:var(--azul)">'+
    '<div class="card-body text-center py-3">'+
    (pedInfo?'<div class="small mb-1 opacity-75">'+esc(pedInfo)+'</div>':'')+
    '<div class="small mb-1 opacity-75">Mejor opcion</div>'+
    '<div class="fs-3 fw-bold">'+fmt(best.cost)+'</div>'+
    '<div class="small mt-1 fw-semibold">'+esc(best.ag.nombre)+'</div>'+
    '<div class="small opacity-75">'+esc(best.ag.freq)+' &middot; canje '+Math.round(best.ag.canje*100)+'%</div>'+
    '</div></div></div>'+
    (m1[1]?
    '<div class="col-sm-6 col-lg-4"><div class="card bg-light">'+
    '<div class="card-body text-center py-3">'+
    '<div class="small text-muted mb-1">2da opcion</div>'+
    '<div class="fs-4 fw-bold text-secondary">'+fmt(m1[1].cost)+'</div>'+
    '<div class="small fw-semibold">'+esc(m1[1].ag.nombre)+'</div>'+
    '<div class="small text-muted">'+esc(m1[1].ag.freq)+' &middot; canje '+Math.round(m1[1].ag.canje*100)+'%</div>'+
    '</div></div></div>':'')+
    (m1[2]?
    '<div class="col-sm-6 col-lg-4"><div class="card bg-light">'+
    '<div class="card-body text-center py-3">'+
    '<div class="small text-muted mb-1">3ra opcion</div>'+
    '<div class="fs-4 fw-bold text-secondary">'+fmt(m1[2].cost)+'</div>'+
    '<div class="small fw-semibold">'+esc(m1[2].ag.nombre)+'</div>'+
    '<div class="small text-muted">'+esc(m1[2].ag.freq)+' &middot; canje '+Math.round(m1[2].ag.canje*100)+'%</div>'+
    '</div></div></div>':'');
}

// ── Supabase / storage ────────────────────────────────────────────────────
async function loadOrders() {
  if (!SUPABASE_URL) {
    try { return JSON.parse(localStorage.getItem(LS_KEY)||'[]'); } catch(e) { return []; }
  }
  try {
    const r = await fetch(
      `${SUPABASE_URL}/rest/v1/pedidos?select=*&order=created_at.desc&limit=500`,
      {headers: await getAuthHeaders()}
    );
    if (!r.ok) throw new Error();
    return await r.json();
  } catch(e) {
    try { return JSON.parse(localStorage.getItem(LS_KEY)||'[]'); } catch(_) { return []; }
  }
}

async function saveOrder(record) {
  if (!SUPABASE_URL) {
    try {
      const arr = JSON.parse(localStorage.getItem(LS_KEY)||'[]');
      arr.unshift(record);
      if (arr.length>500) arr.splice(500);
      localStorage.setItem(LS_KEY, JSON.stringify(arr));
    } catch(e) {}
    return;
  }
  const lineasParaStock = (record.lineas || []).map(l => ({ cod: l.cod, qty: l.qty }));
  const r = await fetch(`${SUPABASE_URL}/rest/v1/rpc/save_order_and_decrement_stock`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify({ p_record: record, p_lineas: lineasParaStock })
  });
  if (!r.ok) {
    const errBody = await r.json().catch(() => ({}));
    const msg = errBody.message || errBody.hint || 'Error al guardar en Supabase';
    throw new Error(msg);
  }
}

async function deleteOrder(id) {
  if (!SUPABASE_URL) {
    try {
      const arr = JSON.parse(localStorage.getItem(LS_KEY)||'[]').filter(o=>o.id!==id);
      localStorage.setItem(LS_KEY, JSON.stringify(arr));
    } catch(e) {}
    return;
  }
  await fetch(`${SUPABASE_URL}/rest/v1/pedidos?id=eq.${id}`, {
    method: 'DELETE', headers: await getAuthHeaders()
  });
}

async function deleteAllOrders() {
  if (!SUPABASE_URL) { localStorage.removeItem(LS_KEY); return; }
  await fetch(`${SUPABASE_URL}/rest/v1/pedidos?id=gt.0`, {
    method: 'DELETE', headers: await getAuthHeaders()
  });
}

async function refreshDashboard() {
  const orders = await loadOrders();
  $('dash-empty').style.display   = orders.length===0 ? '' : 'none';
  $('dash-content').style.display = orders.length>0   ? '' : 'none';
  renderKPIs(orders);
  if (orders.length>0) {
    renderBarChart('ch-prods', topProds(orders));
    renderBarChart('ch-dests', topDests(orders));
    renderBarChart('ch-clis',  topClis(orders));
    renderDoughnut('ch-ags',   topAgs(orders));
    renderHistorial(orders);
  }
}

async function guardarPedido() {
  if (!lastM1.length) {
    alert('Primero calcular el envio.'); return;
  }
  const btn = document.querySelector('[onclick="guardarPedido()"]');
  if (btn) { btn.disabled=true; btn.innerHTML='<span class="spinner-border spinner-border-sm me-1"></span>Guardando...'; }
  try {
    const best = lastM1[0];
    const rec = {
      fecha:    $('f-fecha').value,
      nped:     $('f-nped').value,
      cliente:  $('f-cliente').value,
      destino:  $('f-dest').value,
      vendedor: $('f-vendedor').value,
      obs:      $('f-obs').value,
      pct_costo:  getPctCosto(),
      lineas: [...order.values()].map(p => ({cod:p.c, desc:p.d.substring(0,60), cat:p.cn, uc:p.uc, qty:p.qty})),
      m1_agencia: best.ag.nombre,
      m1_bru:     Math.round(best.bru),
      m1_net:     Math.round(best.cost),
    };
    await saveOrder(rec);
    const _cliN = $('f-cliente').value.trim(), _cliD = $('f-dest').value.trim();
    if (_cliN) saveClient(_cliN, _cliD);
    showToast('Pedido guardado correctamente ✓', 'success');
    await refreshDashboard();
  } catch(e) {
    showToast('Error al guardar el pedido', 'danger');
  } finally {
    if (btn) { btn.disabled=false; btn.innerHTML='<i class="bi bi-save me-1"></i>Guardar pedido'; }
  }
}

// ── Descargar CSV ─────────────────────────────────────────────────────────
function downloadCSV() {
  if (!lastM1.length) { alert('Primero calcular el envio.'); return; }
  const nped  = $('f-nped').value || 'pedido';
  const fecha = $('f-fecha').value || today();
  const rows  = [
    ['PETINSA - Resultado de Envio'],
    ['N Pedido', $('f-nped').value],
    ['Cliente',  $('f-cliente').value],
    ['Destino',  $('f-dest').value],
    ['Fecha',    $('f-fecha').value],
    ['Vendedor', $('f-vendedor').value],
    [],
    ['Ranking de agencias'],
    ['#','Agencia','Tarifa Bruta','Efectivo','Costo Real','Canje %','Frecuencia','Dias/sem'],
    ...lastM1.map((r,i)=>[i+1,r.ag.nombre,Math.round(r.bru),Math.round(r.efect),Math.round(r.cost),
                          Math.round(r.ag.canje*100)+'%',r.ag.freq,r.ag.dias]),
  ];
  const csv = '﻿' + rows.map(r => r.join(',')).join('\r\n');
  const blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href=url; a.download='PETINSA_'+nped+'_'+fecha+'.csv';
  a.click(); URL.revokeObjectURL(url);
  showToast('CSV descargado', 'success');
}

// ── Dashboard ─────────────────────────────────────────────────────────────
async function buildDashboard() {
  await refreshDashboard();
}

function renderKPIs(orders) {
  const n        = orders.length;
  const totalNet = orders.reduce((s,o)=>s+(o.m1_net||0),0);
  const totalBru = orders.reduce((s,o)=>s+(o.m1_bru||0),0);
  const agMap    = {};
  orders.forEach(o => { if(o.m1_agencia) agMap[o.m1_agencia]=(agMap[o.m1_agencia]||0)+1; });
  const topAg    = Object.entries(agMap).sort((a,b)=>b[1]-a[1])[0];
  const cliMap   = {};
  orders.forEach(o => { const c=o.cliente||'Sin nombre'; cliMap[c]=(cliMap[c]||0)+1; });
  const topCli   = Object.entries(cliMap).sort((a,b)=>b[1]-a[1])[0];

  $('dash-kpis').innerHTML =
    kpiCard('bi-receipt','Total pedidos','bg-primary', n, ''),
    kpiCard('bi-currency-dollar','Gasto neto total (M1)','bg-success', fmt(totalNet), ''),
    kpiCard('bi-building','Agencia mas usada','bg-warning text-dark', topAg?topAg[0]:'-', topAg?topAg[1]+' pedidos':''),
    kpiCard('bi-person-check','Cliente top','bg-info', topCli?topCli[0]:'-', topCli?topCli[1]+' pedidos':'');

  $('dash-kpis').innerHTML = [
    kpiCard('bi-receipt',       'Total pedidos guardados',  '#1a3a5c',  n,                ''),
    kpiCard('bi-currency-dollar','Gasto neto total (Modo 1)','#198754', fmt(totalNet),    ''),
    kpiCard('bi-building',      'Agencia mas usada',         '#e67e22', topAg?topAg[0]:'-', topAg?topAg[1]+' ped.':''),
    kpiCard('bi-person-check',  'Cliente con mas pedidos',  '#8e44ad', topCli?topCli[0]:'-', topCli?topCli[1]+' ped.':''),
  ].join('');
}

function kpiCard(icon, label, bg, val, sub) {
  return '<div class="col-6 col-sm-6 col-md-3">'+
    '<div class="card text-white" style="background:'+bg+'">'+
    '<div class="card-body py-3">'+
    '<i class="bi '+icon+' fs-3 opacity-50"></i>'+
    '<div class="fs-3 fw-bold mt-1">'+val+'</div>'+
    '<div class="small opacity-75">'+label+(sub?' &mdash; '+sub:'')+'</div>'+
    '</div></div></div>';
}

function topProds(orders) {
  const m={};
  orders.forEach(o=>(o.lineas||[]).forEach(l=>{
    if(!m[l.cod]) m[l.cod]={label:l.desc.substring(0,22), val:0};
    m[l.cod].val+=l.qty;
  }));
  return Object.values(m).sort((a,b)=>b.val-a.val).slice(0,10);
}
function topDests(orders) {
  const m={};
  orders.forEach(o=>{ const d=o.destino||'Sin destino'; m[d]=(m[d]||0)+1; });
  return Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,10)
    .map(([l,v])=>({label:l,val:v}));
}
function topClis(orders) {
  const m={};
  orders.forEach(o=>{ const c=o.cliente||'Sin nombre'; m[c]=(m[c]||0)+1; });
  return Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,10)
    .map(([l,v])=>({label:l,val:v}));
}
function topAgs(orders) {
  const m={};
  orders.forEach(o=>{ if(o.m1_agencia&&o.m1_net) m[o.m1_agencia]=(m[o.m1_agencia]||0)+o.m1_net; });
  return Object.entries(m).sort((a,b)=>b[1]-a[1])
    .map(([l,v])=>({label:l.split(' ')[0],val:Math.round(v)}));
}

function renderBarChart(id, data) {
  if (chartInstances[id]) { chartInstances[id].destroy(); }
  const ctx = $(id).getContext('2d');
  chartInstances[id] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map(d=>d.label),
      datasets:[{
        data: data.map(d=>d.val),
        backgroundColor: COLORS.slice(0, data.length),
        borderRadius: 5,
      }]
    },
    options: {
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{y:{beginAtZero:true, grid:{color:'#f0f0f0'}},x:{grid:{display:false}}}
    }
  });
}

function renderDoughnut(id, data) {
  if (chartInstances[id]) { chartInstances[id].destroy(); }
  const ctx = $(id).getContext('2d');
  chartInstances[id] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.map(d=>d.label),
      datasets:[{data:data.map(d=>d.val), backgroundColor:COLORS}]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{position:'right', labels:{font:{size:11}}}}
    }
  });
}

function renderHistorial(orders) {
  $('hist-body').innerHTML = orders.slice(0,50).map(o =>
    '<tr>'+
    '<td>'+esc(o.fecha||'-')+'</td>'+
    '<td>'+(o.nped?'<code>'+esc(o.nped)+'</code>':'-')+'</td>'+
    '<td>'+esc(o.cliente||'-')+'</td>'+
    '<td>'+esc(o.destino||'-')+'</td>'+
    '<td>'+esc(o.vendedor||'-')+'</td>'+
    '<td class="text-center">'+(o.lineas?o.lineas.length:0)+'</td>'+
    '<td class="text-end ptag">'+(o.m1_net!==null?fmt(o.m1_net):'-')+'</td>'+
    '<td>'+esc(o.m1_agencia||'-')+'</td>'+
    '<td>'+
      '<button class="btn btn-xs btn-sm btn-outline-danger py-0" data-id="'+o.id+'" onclick="borrarOrden('+o.id+')">'+
      '<i class="bi bi-trash3"></i></button>'+
    '</td>'+
    '</tr>'
  ).join('');
}

async function borrarOrden(id) {
  if (!confirm('Borrar este pedido del historial?')) return;
  try {
    await deleteOrder(id);
    await refreshDashboard();
    showToast('Pedido borrado', 'warning');
  } catch(e) { showToast('Error al borrar el pedido', 'danger'); }
}

async function borrarDatos() {
  if (!confirm('Borrar TODOS los pedidos guardados? Esta accion no se puede deshacer.')) return;
  try {
    await deleteAllOrders();
    await refreshDashboard();
    showToast('Datos borrados', 'warning');
  } catch(e) { showToast('Error al borrar los datos', 'danger'); }
}

async function exportHistorial() {
  const orders = await loadOrders();
  if (!orders.length) { alert('No hay pedidos guardados.'); return; }
  const rows = [
    ['Fecha','N Pedido','Cliente','Destino','Vendedor','Productos',
     'Costo Real','Tarifa Bruta','Agencia','% Costo mercadería','Obs'],
    ...orders.map(o=>[
      o.fecha, o.nped, '"'+(o.cliente||'').replace(/"/g,'""')+'"',
      '"'+(o.destino||'').replace(/"/g,'""')+'"',
      o.vendedor, o.lineas?o.lineas.length:0,
      o.m1_net, o.m1_bru, o.m1_agencia, o.pct_costo!=null?Math.round(o.pct_costo*100)+'%':'',
      '"'+(o.obs||'').replace(/"/g,'""')+'"',
    ])
  ];
  const csv = '﻿'+rows.map(r=>r.join(',')).join('\r\n');
  const blob = new Blob([csv],{type:'text/csv;charset=utf-8'});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href=url; a.download='PETINSA_historial_'+today()+'.csv';
  a.click(); URL.revokeObjectURL(url);
  showToast('Historial exportado', 'success');
}

// ── Catalogo ───────────────────────────────────────────────────────────────
const famSel=$('cat-fam');
[...new Set(CATALOG.map(p=>p.f))].sort().forEach(f=>{
  const o=document.createElement('option'); o.value=f; o.textContent=f; famSel.appendChild(o);
});

function filterCat() {
  const q=normStr($('cat-q').value), fam=$('cat-fam').value;
  catFiltered=CATALOG.filter(p=>
    (!fam||p.f===fam)&&
    (!q||normStr(p.c).includes(q)||normStr(p.d).includes(q)||normStr(p.r).includes(q))
  );
  catPage=1; renderCat();
}

function renderCat() {
  const total=catFiltered.length, pages=Math.max(1,Math.ceil(total/PG));
  const start=(catPage-1)*PG, slice=catFiltered.slice(start,start+PG);
  $('cat-cnt').textContent=total.toLocaleString()+' productos'+(total<CATALOG.length?' (filtrado)':'');
  $('cat-pg-info').textContent='Mostrando '+(start+1)+'-'+Math.min(start+PG,total)+' de '+total;
  $('cat-body').innerHTML=slice.map(p=>{
    const inOrd=order.has(p.c);
    const stCls=p.st>50?'text-success':p.st>0?'text-warning':'text-danger';
    const mkCls=p.ms<2&&p.ms>0?'text-danger fw-semibold':'';
    return '<tr class="cat-tr" data-cod="'+esc(p.c)+'">'+
      '<td><code class="text-primary">'+esc(p.c)+'</code></td>'+
      '<td>'+esc(p.d.substring(0,60))+'</td>'+
      '<td class="text-muted small">'+esc(p.f)+'</td>'+
      '<td class="text-muted small">'+esc((p.r||'').substring(0,28))+'</td>'+
      '<td class="text-end">'+(p.pl>0?'$'+p.pl.toLocaleString('es-UY'):'-')+'</td>'+
      '<td class="text-end '+stCls+' fw-semibold">'+p.st.toLocaleString()+'</td>'+
      '<td class="text-end">'+p.d3.toLocaleString()+'</td>'+
      '<td class="text-end '+mkCls+'">'+(p.ms>0?p.ms:'-')+'</td>'+
      '<td><span class="bcat">'+esc(p.cn)+'</span></td>'+
      '<td><button class="btn btn-sm '+(inOrd?'btn-success':'btn-outline-primary')+' py-0 add-cat" data-cod="'+esc(p.c)+'">'+
        '<i class="bi '+(inOrd?'bi-cart-check':'bi-cart-plus')+'"></i></button></td>'+
      '</tr>';
  }).join('');
  $('cat-body').querySelectorAll('.cat-tr').forEach(tr=>
    tr.addEventListener('click', e=>{ if(!e.target.closest('.add-cat')) showDetail(tr.dataset.cod); }));
  $('cat-body').querySelectorAll('.add-cat').forEach(btn=>
    btn.addEventListener('click', e=>{
      e.stopPropagation();
      const p=CATALOG.find(x=>x.c===btn.dataset.cod);
      if(p){addProduct(p);showTab('calc');}
    }));
  const pgDiv=$('cat-pg');
  if(pages<=1){pgDiv.innerHTML='';return;}
  const nums=[...new Set([1,...Array.from({length:5},(_,i)=>Math.max(1,Math.min(pages,catPage-2+i))),pages])].sort((a,b)=>a-b);
  let pgH='';
  nums.forEach((n,i)=>{
    if(i>0&&nums[i]-nums[i-1]>1) pgH+='<span class="px-1">...</span>';
    pgH+='<span class="pg-btn '+(n===catPage?'active':'')+'" data-pg="'+n+'">'+n+'</span>';
  });
  pgDiv.innerHTML=
    '<span class="pg-btn" data-pg="'+(catPage-1)+'"><i class="bi bi-chevron-left"></i></span>'+
    pgH+'<span class="pg-btn" data-pg="'+(catPage+1)+'"><i class="bi bi-chevron-right"></i></span>';
  pgDiv.querySelectorAll('.pg-btn').forEach(b=>b.addEventListener('click',()=>{
    const p=parseInt(b.dataset.pg);
    if(p>=1&&p<=pages){catPage=p;renderCat();$('cat-body').closest('.card').scrollIntoView({behavior:'smooth'});}
  }));
}

$('cat-q').addEventListener('input', filterCat);
$('cat-fam').addEventListener('change', filterCat);

// ── Detalle modal ─────────────────────────────────────────────────────────
function showDetail(cod) {
  const p=CATALOG.find(x=>x.c===cod); if(!p) return;
  const rows=AGENCIES.filter(a=>AG_NAMES.includes(a.nombre))
    .map(ag=>{ const b=getBruto(ag.nombre,p.uc),e=getEfectivo(ag.nombre,p.uc),c=getCostoReal(ag.nombre,p.uc);
               return b!==null?{ag,b,e,c}:null;}).filter(Boolean).sort((a,b)=>a.c-b.c||a.b-b.b);
  const prev=document.getElementById('det-modal'); if(prev) prev.remove();
  const el=document.createElement('div'); el.id='det-modal';
  el.innerHTML=
    '<div class="modal fade" id="dm-i" tabindex="-1"><div class="modal-dialog modal-lg">'+
    '<div class="modal-content">'+
    '<div class="modal-header" style="background:var(--azul);color:#fff">'+
    '<h5 class="modal-title"><code>'+esc(p.c)+'</code> &mdash; '+esc(p.d.substring(0,55))+'</h5>'+
    '<button class="btn-close btn-close-white" data-bs-dismiss="modal"></button></div>'+
    '<div class="modal-body">'+
    '<div class="row mb-3">'+
    '<div class="col-sm-4"><small class="text-muted">Familia</small><br>'+esc(p.f)+'</div>'+
    '<div class="col-sm-4"><small class="text-muted">Ramo</small><br>'+esc(p.r||'-')+'</div>'+
    '<div class="col-sm-4"><small class="text-muted">Cat. envio</small><br><span class="bcat">'+esc(p.cn)+'</span></div>'+
    '</div>'+
    '<div class="row mb-3 text-center">'+
    '<div class="col-3"><small class="text-muted d-block">P. Lista</small><strong>'+(p.pl>0?'$'+p.pl.toLocaleString():'-')+'</strong></div>'+
    '<div class="col-3"><small class="text-muted d-block">Stock</small><strong class="'+(p.st>0?'text-success':'text-danger')+'">'+p.st.toLocaleString()+'</strong></div>'+
    '<div class="col-3"><small class="text-muted d-block">Pedido</small><strong>'+p.pe.toLocaleString()+'</strong></div>'+
    '<div class="col-3"><small class="text-muted d-block">Disp. 30d</small><strong>'+p.d3.toLocaleString()+'</strong></div>'+
    '</div>'+
    '<h6>Precios de envio (por unidad)</h6>'+
    '<div class="table-responsive"><table class="table table-sm"><thead class="table-light"><tr>'+
    '<th>#</th><th>Agencia</th><th class="text-end">Bruto</th><th class="text-end">Efectivo</th><th class="text-end">Costo real</th>'+
    '<th>Canje</th><th>Frec.</th></tr></thead><tbody>'+
    rows.map((r,i)=>'<tr class="'+(i<3?'rank-'+(i+1):'')+'">'+
      '<td>'+(['&#127945;','&#127946;','&#127947;'][i]||i+1+'.')+'</td>'+
      '<td class="fw-semibold">'+esc(r.ag.nombre)+'</td>'+
      '<td class="text-end text-muted">'+fmt(r.b)+'</td>'+
      '<td class="text-end text-muted">'+fmt(r.e)+'</td>'+
      '<td class="text-end"><span class="ptag">'+fmt(r.c)+'</span></td>'+
      '<td><span class="badge bg-secondary">'+Math.round(r.ag.canje*100)+'%</span></td>'+
      '<td>'+esc(r.ag.freq)+'</td></tr>'
    ).join('')+
    '</tbody></table></div></div>'+
    '<div class="modal-footer">'+
    '<button class="btn btn-p" id="dm-add"><i class="bi bi-cart-plus me-1"></i>Agregar al pedido</button>'+
    '<button class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>'+
    '</div></div></div></div>';
  document.body.appendChild(el);
  const modal=new bootstrap.Modal(document.getElementById('dm-i'));
  modal.show();
  document.getElementById('dm-add').addEventListener('click',()=>{addProduct(p);modal.hide();showTab('calc');});
}

// ── Auth ──────────────────────────────────────────────────────────────────
const AUTH_KEY = 'petinsa_session';

async function doLogin() {
  const email = $('l-email').value.trim();
  const pass  = $('l-pass').value;
  const err   = $('l-err');
  const btn   = $('l-btn');
  if (!email || !pass) { err.textContent='Ingresa email y contrasena.'; err.style.display=''; return; }
  btn.disabled = true; btn.textContent = 'Ingresando...';
  err.style.display = 'none';
  try {
    const r = await fetch(SUPABASE_URL + '/auth/v1/token?grant_type=password', {
      method: 'POST',
      headers: { 'apikey': SUPABASE_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass })
    });
    const data = await r.json();
    if (!r.ok) { err.textContent = data.error_description || data.msg || 'Usuario o contrasena incorrectos.'; err.style.display=''; return; }
    const role = data.user?.user_metadata?.role || 'tenant';
    const expires_at = Date.now() + ((data.expires_in || 3600) * 1000);
    localStorage.setItem(AUTH_KEY, JSON.stringify({ token: data.access_token, refresh: data.refresh_token, role, email, expires_at }));
    applySession({ role, email });
    loadOrders().then(orders => { renderKPIs(orders); });
  } catch(e) {
    err.textContent = 'Error de conexion. Intenta nuevamente.'; err.style.display='';
  } finally {
    btn.disabled = false; btn.textContent = 'Ingresar';
  }
}

function applySession(session) {
  $('login-overlay').style.display = 'none';
  $('btn-dash').style.display = session.role === 'admin' ? '' : 'none';
  $('btn-logout').style.display = '';
  $('user-label').textContent = session.email;
}

function doLogout() {
  localStorage.removeItem(AUTH_KEY);
  location.reload();
}

// ── Escanear Llanta ───────────────────────────────────────────────────────
(function() {
  const inp = $('scan-input');
  inp.addEventListener('change', () => {
    const file = inp.files[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {
      $('scan-preview').src = e.target.result;
      $('scan-preview-wrap').style.display = '';
      $('scan-btn').disabled = false;
      $('scan-result').style.display = 'none';
      $('scan-productos').style.display = 'none';
    };
    reader.readAsDataURL(file);
  });
})();

function parsearMedidaLlanta(texto) {
  // Normalización base: aplanar saltos de línea y espacios múltiples
  let t = texto.replace(/\n/g, ' ').replace(/\s+/g, ' ');

  // Generar versiones alternativas para tolerar artefactos del OCR
  const versiones = [
    t,
    // Sustituciones comunes de OCR: O→0, I/l→1
    t.replace(/O/g,'0').replace(/\bI\b/g,'1').replace(/l(?=\d)/g,'1'),
    // Remover espacios dentro de secuencias de dígitos (artefacto frecuente de Tesseract)
    t.replace(/(\d)\s+(\d)/g,'$1$2'),
    // Ambas correcciones juntas
    t.replace(/O/g,'0').replace(/(\d)\s+(\d)/g,'$1$2'),
  ];

  for (const v of versiones) {
    // Métrico: 205/55R16, 205/55 R16, LT215/85R16, 205|55R16, 20555R16 (sin separador por OCR)
    let m = v.match(/(?:LT|P)?\s*(\d{3})\s*[\/\\|]?\s*(\d{2,3})\s*[Rr]\s*(\d{2}(?:[.,]\d)?)/);
    if (m) {
      const width=parseInt(m[1]), profile=parseInt(m[2]), rim=parseFloat(m[3].replace(',','.'));
      return { spec: width+'/'+profile+' R'+rim, width, profile, rim,
               raw: m[0].replace(/\s+/g,'') };
    }
    // Convencional: 7.50-16
    m = v.match(/(\d+)[.,](\d{2})\s*[-–]\s*(\d{2})/);
    if (m) {
      const rim=parseInt(m[3]);
      return { spec: m[1]+'.'+m[2]+'-'+rim, rim, raw: m[0] };
    }
    // Agrícola: 14.9 - 24
    m = v.match(/(\d{2})[.,](\d)\s*[-–]\s*(\d{2})/);
    if (m) {
      const rim=parseInt(m[3]);
      return { spec: m[1]+'.'+m[2]+'-'+rim, rim, raw: m[0] };
    }
  }
  return null;
}

async function analizarLlanta() {
  const btn = $('scan-btn');
  const file = $('scan-input').files[0];
  if (!file) {
    const resultEl = $('scan-result');
    resultEl.style.display = '';
    resultEl.innerHTML = '<div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i>Primero seleccioná una imagen usando el botón "Tomar / subir foto".</div>';
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Leyendo imagen...';
  $('scan-result').style.display = 'none';
  $('scan-productos').style.display = 'none';

  try {
    // Preprocesar imagen: escala de grises + normalización + umbralización binaria
    // Esto convierte texto en relieve (goma oscura) en pixels blancos sobre negro,
    // que Tesseract lee mucho mejor que gradientes sutiles.
    const imageDataUrl = await new Promise((res, rej) => {
      const img = new Image();
      img.onload = () => {
        try {
          const MAX_W = 1400;
          const scale = img.width > MAX_W ? MAX_W / img.width : 1;
          const canvas = document.createElement('canvas');
          canvas.width  = Math.round(img.width  * scale);
          canvas.height = Math.round(img.height * scale);
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

          const id = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const d  = id.data;

          // 1) Convertir a escala de grises y buscar min/max
          const gray = new Uint8Array(canvas.width * canvas.height);
          let mn = 255, mx = 0;
          for (let i = 0; i < d.length; i += 4) {
            const g = Math.round(0.299*d[i] + 0.587*d[i+1] + 0.114*d[i+2]);
            gray[i >> 2] = g;
            if (g < mn) mn = g;
            if (g > mx) mx = g;
          }

          // 2) Normalizar al rango completo [0,255] y umbralizar al 50%
          const range = mx - mn || 1;
          for (let j = 0; j < gray.length; j++) {
            const norm = Math.round((gray[j] - mn) / range * 255);
            const bin  = norm > 127 ? 255 : 0;
            const base = j * 4;
            d[base] = d[base+1] = d[base+2] = bin;
            d[base+3] = 255;
          }
          ctx.putImageData(id, 0, 0);
          res(canvas.toDataURL('image/png'));
        } catch(err) { rej(err); }
      };
      img.onerror = rej;
      img.src = URL.createObjectURL(file);
    });

    // Cargar Tesseract.js dinámicamente (solo cuando se necesita)
    if (!window.Tesseract) {
      btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Cargando OCR...';
      await new Promise((res, rej) => {
        const s = document.createElement('script');
        s.src = 'https://unpkg.com/tesseract.js@v4/dist/tesseract.min.js';
        s.onload = res; s.onerror = rej;
        document.head.appendChild(s);
      });
    }

    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Procesando OCR...';

    const result = await Tesseract.recognize(imageDataUrl, 'eng', {
      logger: m => {
        if (m.status === 'recognizing text')
          btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>'+
            Math.round(m.progress*100)+'%...';
      }
    });

    const texto = result.data.text;
    const data  = parsearMedidaLlanta(texto);

    const resultEl = $('scan-result');
    resultEl.style.display = '';

    if (!data) {
      resultEl.innerHTML =
        '<div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i>'+
        'No se encontró un código de medida. Intentá con una foto más nítida y de cerca del lateral de la llanta.'+
        '<details class="mt-2" open><summary class="small fw-bold">Texto detectado por OCR</summary>'+
        '<pre class="small mt-1 p-2 bg-light border rounded" style="white-space:pre-wrap;max-height:150px;overflow-y:auto">'+(esc(texto)||'<em class="text-muted">(sin texto)</em>')+'</pre></details></div>';
      return;
    }

    resultEl.innerHTML =
      '<div class="alert alert-success d-flex align-items-center gap-3 mb-0">'+
      '<i class="bi bi-check-circle-fill fs-4 flex-shrink-0"></i>'+
      '<div>'+
        '<div class="fw-bold fs-5">'+esc(data.spec)+'</div>'+
        '<div class="small text-muted">'+
          (data.width  ? 'Ancho: <strong>'+data.width+'mm</strong> &nbsp; ' : '')+
          (data.profile? 'Perfil: <strong>'+data.profile+'%</strong> &nbsp; ' : '')+
          'Rodado: <strong>R'+data.rim+'</strong>'+
        '</div>'+
      '</div></div>';

    buscarEnCatalogo(data);

  } catch(e) {
    const resultEl = $('scan-result');
    resultEl.style.display = '';
    const msg = e instanceof Error ? e.message : (e ? String(e) : 'error desconocido');
    resultEl.innerHTML =
      '<div class="alert alert-danger"><i class="bi bi-exclamation-triangle me-2"></i>'+
      'Error al procesar la imagen: '+esc(msg)+'</div>';
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-cpu me-1"></i>Analizar';
  }
}

function buscarEnCatalogo(data) {
  if (!data.rim && !data.spec) { $('scan-productos').style.display='none'; return; }

  // Regex de rodado: matchea "R15", "R 15", "KR15" pero NO "TR15" (tipo válvula)
  // (?<!t) evita TR15; r\s* permite espacio entre R y número
  const rimRx = data.rim
    ? new RegExp('(?<!t)r\\s*' + data.rim + '(?!\\d)', 'i')
    : null;

  const countMatches = p => {
    const fields = normStr(p.c) + ' ' + normStr(p.d) + ' ' + normStr(p.r);
    let score = 0;
    if (rimRx && rimRx.test(fields)) score++;
    if (data.width   && fields.includes(String(data.width)))   score++;
    if (data.profile && fields.includes('/'+data.profile))     score++;
    return score;
  };

  // Filtro: rodado obligatorio
  const resultados = CATALOG.filter(p => {
    if (!rimRx) return false;
    const haystack = normStr(p.d) + ' ' + normStr(p.r);
    return rimRx.test(haystack);
  }).sort((a, b) => countMatches(b) - countMatches(a))
    .slice(0, 20);

  const wrap = $('scan-productos');
  if (!resultados.length) {
    wrap.style.display = '';
    $('scan-prod-title').innerHTML = '<i class="bi bi-search me-2"></i>Sin coincidencias en el catálogo';
    $('scan-prod-body').innerHTML =
      '<tr><td colspan="5" class="text-muted text-center py-3">No se encontraron productos con esa medida.</td></tr>';
    wrap.style.display = '';
    return;
  }

  $('scan-prod-title').innerHTML = '<i class="bi bi-list-ul me-2"></i>Productos encontrados ('+ resultados.length +')';
  $('scan-prod-body').innerHTML = resultados.map(p =>
    '<tr>'+
    '<td><code>'+esc(p.c)+'</code></td>'+
    '<td>'+esc(p.d.substring(0,60))+'</td>'+
    '<td><span class="bcat">'+esc(p.f)+'</span></td>'+
    '<td class="text-center"><span class="'+(p.st>0?'text-success fw-bold':'text-danger')+'">'+p.st+'</span></td>'+
    '<td><button class="btn btn-sm btn-p py-0" onclick="agregarDesdeScan(\''+esc(p.c)+'\')">'+
      '<i class="bi bi-cart-plus"></i></button></td>'+
    '</tr>'
  ).join('');
  wrap.style.display = '';
}

function agregarDesdeScan(cod) {
  const p = CATALOG.find(x => x.c === cod);
  if (!p) return;
  addProduct(p);
  showTab('calc');
  showToast(p.d.substring(0,40)+' agregado al pedido', 'success');
}

// ── Init ──────────────────────────────────────────────────────────────────
$('f-fecha').value = today();
filterCat();
(async function checkSession() {
  const raw = localStorage.getItem(AUTH_KEY);
  if (!raw) { $('login-overlay').style.display = 'flex'; return; }
  let session = JSON.parse(raw);
  if (session.expires_at && Date.now() > session.expires_at) {
    if (session.refresh) {
      session = await refreshSession(session.refresh);
      if (!session) return;
    } else {
      localStorage.removeItem(AUTH_KEY);
      $('login-overlay').style.display = 'flex';
      return;
    }
  }
  applySession(session);
  loadOrders().then(orders => { renderKPIs(orders); });
})();
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}
</script>
</body>
</html>'''

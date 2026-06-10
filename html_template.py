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
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
<style>
:root{--azul:#1a3a5c;--azul-c:#e8f0f8;--azul-m:#2c5282;}
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
@media print{
  nav,.tab-btn,#results-btns,.card-header button,#f-obs-row{display:none!important;}
  .card{box-shadow:none!important;border:1px solid #ddd!important;}
}
@media (max-width:575px){
  body{font-size:.85rem;}
  .tab-btn{padding:.4rem .65rem;}
  .tab-btn .tab-txt{display:none;}
  #ac-box{max-height:40vh;}
  .ac-it{padding:.55rem .8rem;}
  .qty-inp{width:52px!important;}
  .d-flex.gap-4{gap:.5rem!important;}
  .chart-wrap{height:180px;}
  .container-fluid{padding-left:.75rem!important;padding-right:.75rem!important;}
  input,select,.form-control,.form-select{font-size:16px!important;}
}
</style>
</head>
<body>

<!-- NAVBAR -->
<nav class="navbar navbar-dark px-3 py-2 mb-0">
  <span class="navbar-brand fw-bold fs-5 text-truncate" style="max-width:220px">
    <i class="bi bi-truck me-2"></i>PETINSA &mdash; Sistema de Envios
  </span>
  <span class="text-white-50 small d-none d-sm-inline">Tarifas Mayo 2026</span>
</nav>

<div class="container-fluid px-3 pt-3">

  <!-- TABS -->
  <div class="d-flex border-bottom mb-3">
    <button class="tab-btn active" id="btn-calc" onclick="showTab('calc')">
      <i class="bi bi-calculator"></i><span class="tab-txt ms-1">Calcular Envio</span>
      <span id="ocnt" style="display:none">0</span>
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
              <div class="col-6 col-sm-4 col-md-2">
                <label class="form-label mb-1 fw-semibold small">N&deg; Pedido</label>
                <input id="f-nped" class="form-control form-control-sm" placeholder="Ej: 00123">
              </div>
              <div class="col-12 col-sm-8 col-md-3">
                <label class="form-label mb-1 fw-semibold small">Cliente</label>
                <input id="f-cliente" class="form-control form-control-sm" placeholder="Nombre del cliente">
              </div>
              <div class="col-12 col-sm-6 col-md-3">
                <label class="form-label mb-1 fw-semibold small">Localidad / Destino</label>
                <input id="f-dest" class="form-control form-control-sm" placeholder="Ciudad de destino">
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
            <div class="d-flex align-items-center gap-4 flex-wrap">
              <span class="fw-semibold"><i class="bi bi-percent me-1"></i>Canje:</span>
              <div class="form-check form-check-inline mb-0">
                <input class="form-check-input" type="radio" name="cj" id="cj-a" value="A" checked>
                <label class="form-check-label" for="cj-a">A &mdash; Ahorro real (neto puede ser $0)</label>
              </div>
              <div class="form-check form-check-inline mb-0">
                <input class="form-check-input" type="radio" name="cj" id="cj-b" value="B">
                <label class="form-check-label" for="cj-b">B &mdash; Canje con costo de oportunidad</label>
              </div>
              <div id="margin-wrap" style="display:none" class="d-flex align-items-center gap-2">
                <label class="mb-0 small">Costo/Venta goma:</label>
                <input type="range" min="0" max="100" value="60" id="margin-sl" class="form-range flex-grow-1" style="min-width:80px;max-width:120px">
                <span id="margin-lbl">60%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Summary cards -->
        <div class="row g-3 mb-3" id="summary-cards"></div>

        <!-- Modo 1 -->
        <div class="card mb-3">
          <div class="ch"><i class="bi bi-building me-2"></i>Modo 1 &mdash; Todo en una sola agencia</div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-sm table-hover mb-0">
                <thead class="table-light"><tr>
                  <th>#</th><th>Agencia</th>
                  <th class="text-end">Total bruto</th>
                  <th class="text-end">Total neto</th>
                  <th>Canje</th><th>Frecuencia</th><th>Dias/sem</th>
                </tr></thead>
                <tbody id="m1-body"></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Modo 2 -->
        <div class="card mb-3">
          <div class="ch"><i class="bi bi-diagram-3 me-2"></i>Modo 2 &mdash; Mejor agencia por producto</div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-sm table-hover mb-0">
                <thead class="table-light"><tr>
                  <th>Codigo</th><th>Descripcion</th><th>Categoria</th>
                  <th class="text-center">Cant.</th>
                  <th>Mejor Agencia</th>
                  <th class="text-end">$/u neto</th>
                  <th class="text-end">Subtotal</th>
                  <th>Frecuencia</th>
                </tr></thead>
                <tbody id="m2-body"></tbody>
                <tfoot>
                  <tr class="table-light fw-bold">
                    <td colspan="6" class="text-end">Total Modo 2:</td>
                    <td class="text-end ptag" id="m2-total">-</td>
                    <td></td>
                  </tr>
                </tfoot>
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

  <!-- ===== TAB CATALOGO ===== -->
  <div id="tab-cat" style="display:none">
    <div class="card">
      <div class="ch"><i class="bi bi-grid me-2"></i>Catalogo de Productos</div>
      <div class="card-body">
        <div class="row g-2 mb-3">
          <div class="col-md-5">
            <input id="cat-q" class="form-control" placeholder="Buscar codigo, descripcion, ramo...">
          </div>
          <div class="col-md-3">
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
                <th class="text-end">Neto M1</th>
                <th class="text-end">Neto M2</th>
                <th>Agencia M1</th><th></th>
              </tr></thead>
              <tbody id="hist-body"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div><!-- /tab-dash -->

</div><!-- /container -->

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
const CATALOG  = __CATALOG__;
const AGENCIES = __AGENCIES__;
const PRICES   = __PRICES__;
const UCATS    = __UCATS__;
const AG_NAMES = __AG_NAMES__;
</script>

<!-- ===== LOGICA ===== -->
<script>
// ── Estado ────────────────────────────────────────────────────────────────
const order = new Map();
let catFiltered = [], catPage = 1;
const PG = 25;
let lastM1 = [], lastM2 = [], lastTot2 = 0, lastTot1 = 0;
let chartInstances = {};
const LS_KEY = 'petinsa_orders_v1';
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
  ['calc','cat','dash'].forEach(id => {
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
function canjeF(cj) {
  const m = document.querySelector('input[name="cj"]:checked').value;
  if (m==='A') return 1 - cj;
  const mg = parseFloat($('margin-sl').value)/100;
  return 1 - cj*(1-mg);
}
function getBruto(ag, uc) { return ((PRICES[ag]||{})[uc]) ?? null; }
function getNeto(ag, uc) {
  const b = getBruto(ag, uc); if (b===null) return null;
  const a = AGENCIES.find(x => x.nombre===ag);
  return b * canjeF(a ? a.canje : 0);
}
function getRankScore(ag, uc) {
  const b = getBruto(ag, uc); if (b===null) return null;
  const a = AGENCIES.find(x => x.nombre===ag);
  const cj = a ? a.canje : 0;
  const mode = document.querySelector('input[name="cj"]:checked').value;
  if (mode==='A' && cj>=1.0) return b * 0.75;
  return getNeto(ag, uc);
}

function calculate() {
  if (!order.size) { alert('Agrega productos al pedido primero.'); return; }
  $('results-section').style.display = '';
  doCalc();
  $('results-section').scrollIntoView({behavior:'smooth'});
}

function doCalc() {
  const lines = [...order.values()].map(p =>
    ({cod:p.c, desc:p.d.substring(0,55), cat:p.cn, uc:p.uc, qty:p.qty}));

  // Modo 1
  const m1 = AGENCIES.filter(a => AG_NAMES.includes(a.nombre)).map(ag => {
    let bru=0, net=0, score=0; const mis=[];
    for (const l of lines) {
      const b=getBruto(ag.nombre,l.uc), n=getNeto(ag.nombre,l.uc), s=getRankScore(ag.nombre,l.uc);
      if (b===null) mis.push(l.cat);
      else { bru+=b*l.qty; net+=n*l.qty; score+=s*l.qty; }
    }
    return {ag, bru, net:mis.length?null:net, score:mis.length?null:score, mis};
  }).filter(r=>r.net!==null).sort((a,b)=>a.score-b.score||a.bru-b.bru);

  // Modo 2
  let tot2=0;
  const m2 = lines.map(l => {
    let bestAg=null, bestScore=Infinity, bestN=null, bestB=null;
    for (const ag of AGENCIES) {
      if (!AG_NAMES.includes(ag.nombre)) continue;
      const s=getRankScore(ag.nombre,l.uc);
      if (s!==null && s<bestScore) { bestScore=s; bestN=getNeto(ag.nombre,l.uc); bestB=getBruto(ag.nombre,l.uc); bestAg=ag; }
    }
    const sub = bestAg ? bestN*l.qty : null;
    if (sub!==null) tot2+=sub;
    return {...l, bestAg, bestB, bestN, sub};
  });

  lastM1=[...m1]; lastM2=[...m2]; lastTot2=tot2;
  lastTot1 = m1.length ? m1[0].net : 0;

  renderM1(m1);
  renderM2(m2, tot2);
  renderSummary(m1, tot2);
}

document.querySelectorAll('input[name="cj"]').forEach(r => r.addEventListener('change', () => {
  $('margin-wrap').style.display = r.value==='B' ? '' : 'none';
  if ($('results-section').style.display!=='none') doCalc();
}));
$('margin-sl').addEventListener('input', () => {
  $('margin-lbl').textContent = $('margin-sl').value+'%';
  if ($('results-section').style.display!=='none') doCalc();
});

// ── Render Modo 1 ─────────────────────────────────────────────────────────
function renderM1(rows) {
  const medals=['&#127945;','&#127946;','&#127947;'];
  $('m1-body').innerHTML = rows.map((r,i) => {
    const cls=i<3?'rank-'+(i+1):'';
    const isZero=r.net<1;
    const netH=isZero?'<span class="neto0">$0 <small>(canje 100%)</small></span>'
                     :'<span class="ptag">'+fmt(r.net)+'</span>';
    return '<tr class="'+cls+'">'+
      '<td>'+(medals[i]||i+1+'.')+'</td>'+
      '<td class="fw-semibold">'+esc(r.ag.nombre)+'</td>'+
      '<td class="text-end text-muted">'+fmt(r.bru)+'</td>'+
      '<td class="text-end">'+netH+'</td>'+
      '<td><span class="badge bg-secondary">'+Math.round(r.ag.canje*100)+'%</span></td>'+
      '<td>'+esc(r.ag.freq)+'</td>'+
      '<td class="text-center"><span class="badge '+(r.ag.dias>=5?'bg-success':'bg-warning text-dark')+'">'+
        r.ag.dias+'d</span></td>'+
      '</tr>';
  }).join('');
}

// ── Render Modo 2 ─────────────────────────────────────────────────────────
function renderM2(rows, tot2) {
  $('m2-body').innerHTML = rows.map(r => {
    const isZero=r.sub!==null&&r.sub<1;
    const subH=isZero?'<span class="neto0">$0</span>':'<span class="ptag">'+fmt(r.sub)+'</span>';
    return '<tr>'+
      '<td><code>'+esc(r.cod)+'</code></td>'+
      '<td>'+esc(r.desc)+'</td>'+
      '<td><span class="bcat">'+esc(r.cat)+'</span></td>'+
      '<td class="text-center">'+r.qty+'</td>'+
      '<td class="fw-semibold">'+(r.bestAg?esc(r.bestAg.nombre):'Sin precio')+'</td>'+
      '<td class="text-end">'+fmt(r.bestN)+'</td>'+
      '<td class="text-end">'+subH+'</td>'+
      '<td>'+(r.bestAg?esc(r.bestAg.freq):'')+'</td>'+
      '</tr>';
  }).join('');
  $('m2-total').innerHTML='<span class="ptag">'+fmt(tot2)+'</span>';
}

// ── Render Summary ────────────────────────────────────────────────────────
function renderSummary(m1, tot2) {
  if (!m1.length) { $('summary-cards').innerHTML=''; return; }
  const best=m1[0];
  const diff=best.net-tot2;
  const pct=best.net>0?Math.abs(diff/best.net*100).toFixed(1):0;
  const pedInfo=[
    $('f-nped').value?'Pedido #'+$('f-nped').value:'',
    $('f-cliente').value,
    $('f-dest').value
  ].filter(Boolean).join(' | ');
  let diffB='';
  if (Math.abs(diff)<1) diffB='<span class="badge bg-secondary">Mismo costo</span>';
  else if (diff>0) diffB='<span class="badge bg-danger">M1 cuesta '+fmt(diff)+' mas</span>';
  else diffB='<span class="badge bg-success">M1 ahorra '+fmt(-diff)+'</span>';

  const m2Ags=[...new Set(lastM2.filter(r=>r.bestAg).map(r=>r.bestAg.nombre))];
  $('summary-cards').innerHTML=
    '<div class="col-md-4"><div class="card text-white" style="background:var(--azul)">'+
    '<div class="card-body text-center py-3">'+
    (pedInfo?'<div class="small mb-1 opacity-75">'+esc(pedInfo)+'</div>':'')+
    '<div class="small mb-1 opacity-75">Modo 1 &mdash; Mejor agencia unica</div>'+
    '<div class="fs-3 fw-bold">'+(best.net<1?'$0 &#10003;':fmt(best.net))+'</div>'+
    '<div class="small mt-1 fw-semibold">'+esc(best.ag.nombre)+'</div>'+
    '<div class="small opacity-75">'+esc(best.ag.freq)+' &middot; canje '+Math.round(best.ag.canje*100)+'%</div>'+
    '</div></div></div>'+

    '<div class="col-md-4"><div class="card text-white" style="background:#198754">'+
    '<div class="card-body text-center py-3">'+
    '<div class="small mb-1 opacity-75">Modo 2 &mdash; Mejor por producto</div>'+
    '<div class="fs-3 fw-bold">'+(tot2<1?'$0 &#10003;':fmt(tot2))+'</div>'+
    '<div class="small mt-1">'+m2Ags.length+' agencia(s)</div>'+
    '<div class="small opacity-75">'+esc(m2Ags.slice(0,2).join(', '))+(m2Ags.length>2?'...':'')+'</div>'+
    '</div></div></div>'+

    '<div class="col-md-4"><div class="card bg-light">'+
    '<div class="card-body text-center py-3">'+
    '<div class="small text-muted mb-2">Comparativa</div>'+
    '<div class="mb-2">'+diffB+'</div>'+
    '<div class="small text-muted">'+pct+'% diferencia</div>'+
    '<div class="small text-muted">'+(diff>0?'Conviene dividir el envio':'Conviene una sola agencia')+'</div>'+
    '</div></div></div>';
}

// ── Guardar pedido ────────────────────────────────────────────────────────
function loadOrders() {
  try { return JSON.parse(localStorage.getItem(LS_KEY)||'[]'); }
  catch(e) { return []; }
}
function saveOrders(arr) { localStorage.setItem(LS_KEY, JSON.stringify(arr)); }

function guardarPedido() {
  if (!lastM1.length && !lastM2.length) {
    alert('Primero calcular el envio.'); return;
  }
  const best = lastM1.length ? lastM1[0] : null;
  const rec = {
    id: Date.now(),
    ts: new Date().toISOString(),
    fecha:    $('f-fecha').value,
    nped:     $('f-nped').value,
    cliente:  $('f-cliente').value,
    destino:  $('f-dest').value,
    vendedor: $('f-vendedor').value,
    obs:      $('f-obs').value,
    canje_modo: document.querySelector('input[name="cj"]:checked').value,
    lineas: [...order.values()].map(p => ({cod:p.c, desc:p.d.substring(0,60), cat:p.cn, uc:p.uc, qty:p.qty})),
    m1_agencia: best ? best.ag.nombre : null,
    m1_bru:     best ? Math.round(best.bru) : null,
    m1_net:     best ? Math.round(best.net) : null,
    m2_net:     Math.round(lastTot2),
    m2_ags:     [...new Set(lastM2.filter(r=>r.bestAg).map(r=>r.bestAg.nombre))],
  };
  const orders = loadOrders();
  orders.unshift(rec);
  if (orders.length > 500) orders.splice(500);
  saveOrders(orders);
  showToast('Pedido guardado correctamente', 'success');
}

// ── Descargar CSV ─────────────────────────────────────────────────────────
function downloadCSV() {
  if (!lastM1.length && !lastM2.length) { alert('Primero calcular el envio.'); return; }
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
    ['MODO 1 - Una sola agencia'],
    ['#','Agencia','Total Bruto','Total Neto','Canje %','Frecuencia','Dias/sem'],
    ...lastM1.map((r,i)=>[i+1,r.ag.nombre,Math.round(r.bru),Math.round(r.net),
                          Math.round(r.ag.canje*100)+'%',r.ag.freq,r.ag.dias]),
    [],
    ['MODO 2 - Por producto'],
    ['Codigo','Descripcion','Categoria','Cantidad','Mejor Agencia','Precio neto/u','Subtotal','Frecuencia'],
    ...lastM2.map(r=>[r.cod,'"'+r.desc.replace(/"/g,'""')+'"',r.cat,r.qty,
                      r.bestAg?r.bestAg.nombre:'Sin precio',
                      r.bestN!==null?Math.round(r.bestN):'',
                      r.sub!==null?Math.round(r.sub):'',
                      r.bestAg?r.bestAg.freq:'']),
    ['','','','','','Total',Math.round(lastTot2),''],
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
function buildDashboard() {
  const orders = loadOrders();
  $('dash-empty').style.display   = orders.length===0 ? '' : 'none';
  $('dash-content').style.display = orders.length>0   ? '' : 'none';
  renderKPIs(orders);
  if (orders.length>0) {
    renderBarChart('ch-prods',  topProds(orders));
    renderBarChart('ch-dests',  topDests(orders));
    renderBarChart('ch-clis',   topClis(orders));
    renderDoughnut('ch-ags',    topAgs(orders));
    renderHistorial(orders);
  }
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
  return '<div class="col-md-3 col-sm-6">'+
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
    '<td class="text-end">'+(o.m2_net!==null?fmt(o.m2_net):'-')+'</td>'+
    '<td>'+esc(o.m1_agencia||'-')+'</td>'+
    '<td>'+
      '<button class="btn btn-xs btn-sm btn-outline-danger py-0" data-id="'+o.id+'" onclick="borrarOrden('+o.id+')">'+
      '<i class="bi bi-trash3"></i></button>'+
    '</td>'+
    '</tr>'
  ).join('');
}

function borrarOrden(id) {
  if (!confirm('Borrar este pedido del historial?')) return;
  const orders = loadOrders().filter(o=>o.id!==id);
  saveOrders(orders);
  buildDashboard();
  showToast('Pedido borrado', 'warning');
}

function borrarDatos() {
  if (!confirm('Borrar TODOS los pedidos guardados? Esta accion no se puede deshacer.')) return;
  localStorage.removeItem(LS_KEY);
  buildDashboard();
  showToast('Datos borrados', 'warning');
}

function exportHistorial() {
  const orders = loadOrders();
  if (!orders.length) { alert('No hay pedidos guardados.'); return; }
  const rows = [
    ['Fecha','N Pedido','Cliente','Destino','Vendedor','Productos',
     'Neto M1','Bruto M1','Neto M2','Agencia M1','Agencias M2','Canje','Obs'],
    ...orders.map(o=>[
      o.fecha, o.nped, '"'+(o.cliente||'').replace(/"/g,'""')+'"',
      '"'+(o.destino||'').replace(/"/g,'""')+'"',
      o.vendedor, o.lineas?o.lineas.length:0,
      o.m1_net, o.m1_bru, o.m2_net, o.m1_agencia,
      '"'+(o.m2_ags||[]).join(';')+'"', o.canje_modo,
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
    .map(ag=>{ const b=getBruto(ag.nombre,p.uc),n=getNeto(ag.nombre,p.uc);
               return b!==null?{ag,b,n}:null;}).filter(Boolean).sort((a,b)=>{const sa=getRankScore(a.ag.nombre,p.uc)??a.n,sb=getRankScore(b.ag.nombre,p.uc)??b.n;return sa-sb||a.b-b.b;});
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
    '<th>#</th><th>Agencia</th><th class="text-end">Bruto</th><th class="text-end">Neto</th>'+
    '<th>Canje</th><th>Frec.</th></tr></thead><tbody>'+
    rows.map((r,i)=>'<tr class="'+(i<3?'rank-'+(i+1):'')+'">'+
      '<td>'+(['&#127945;','&#127946;','&#127947;'][i]||i+1+'.')+'</td>'+
      '<td class="fw-semibold">'+esc(r.ag.nombre)+'</td>'+
      '<td class="text-end text-muted">'+fmt(r.b)+'</td>'+
      '<td class="text-end">'+(r.n<1?'<span class="neto0">$0</span>':'<span class="ptag">'+fmt(r.n)+'</span>')+'</td>'+
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

// ── Init ──────────────────────────────────────────────────────────────────
$('f-fecha').value = today();
filterCat();
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

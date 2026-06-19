---
name: petinsa-quality
description: >
  Comprehensive quality skill for the PETINSA ML-Proyecto shipping calculator app.
  ALWAYS use this skill when working on any file in ML-Proyecto: html_template.py,
  generar_html.py, generar_html_data.py, CLAUDE.md, sw.js, or petinsa_envios.html.
  Covers UI/UX standards, business logic validation, code quality checks, and the
  full deploy workflow. Trigger on any task involving feature additions, bug fixes,
  refactors, or code review in this project — even if the user doesn't explicitly
  ask for a quality check.
---

# PETINSA Quality Skill

## Project Context (read this first)
Static HTML+JS app for PETINSA warehouse workers in Uruguay. Python runs locally to
generate `petinsa_envios.html` — Vercel serves it statically. All UI changes go in
`html_template.py`, never directly in the generated HTML. Architecture must stay static.
End users are non-technical warehouse workers, not developers.

Full context: read `CLAUDE.md` at the repo root before any non-trivial change.

---

## 1. Before Any Change

- [ ] Read `CLAUDE.md` to understand current state and constraints
- [ ] Identify which files are affected (`html_template.py`, `generar_html.py`, `generar_html_data.py`)
- [ ] If touching the active sheet name, verify it matches the current month in `generar_html.py` (~line 254)
- [ ] If touching `MAPPING` or `UNIFIED_CATS`, update **both** `generar_html.py` AND `generar_html_data.py`
- [ ] Never edit `petinsa_envios.html` directly — it's generated output

---

## 2. Business Logic Validation

### Canje Formulas (critical — verify before any pricing change)
```
neto  = bruto × (1 - canje)              # Cashflow: plata que sale
costo = bruto × (1 - 0.25 × canje)       # Costo verdadero: markup 25% en cubiertas
```
- `costo` is used for ranking in both Modo 1 and Modo 2
- `getRankScore()` must delegate to `getCosto()` — never hardcode 0.75 for specific canje values
- Formula works for any canje% (0%, 25%, 31%, 100%) — verify no hardcoded edge cases

### GONFER IVA (common gotcha)
- GONFER prices in Excel are pre-IVA → multiplier `IVA = 1.22` applied at parse time
- If adding new price comparison paths, check `agency_meta[ag] == 'sin IVA'` before comparing
- Never apply IVA to other agencies — they're already IVA-inclusive

### Product Code Normalization
- Always: `str(cod).strip().rstrip('.0')` — ERP exports floats like `20046.0`
- Never compare raw floats/ints as product codes

### classify() Priority Order
Before adding/reordering branches in `classify()`:
1. LUBRICANTE first
2. BATERIA before generic
3. ACCES/CAM MOTO before MOTO
4. GIGANTE/VIAL/IND. before PASEO/CAMIONETA
5. PASEO and CAMIONETA last among tires

### norm() — Use Everywhere for String Matching
Any comparison against Excel data must use `norm()`. Raw comparison fails on accents,
case, and `\xa0` non-breaking spaces.

---

## 3. Code Quality Checklist

### JavaScript (html_template.py)
- [ ] No `var` — use `const`/`let`
- [ ] Async functions (`loadOrders`, `saveOrder`, `deleteOrder`) must stay `async`
- [ ] All user-visible strings must be in Spanish
- [ ] No direct DOM manipulation with hardcoded English text
- [ ] New functions follow existing naming: `camelCase`, single responsibility
- [ ] No jQuery, React, Vue — vanilla JS only
- [ ] `$('id')` is the local helper for `document.getElementById` — use it

### Python (generar_html.py, generar_html_data.py)
- [ ] Assume Excel cells can be `None`, empty string, float, or `\xa0` — sanitize with `norm()`
- [ ] No bare column position assumptions — verify row/col offsets if parsing new sheets
- [ ] Missing prices (`None`) are valid — don't raise errors, exclude from ranking silently
- [ ] No try/except around Excel loading — intentional crash for missing files is correct

### Security
- [ ] No user input concatenated into SQL or eval
- [ ] Supabase credentials only via `.env` injection at build time — never hardcoded in template
- [ ] No `innerHTML` with unsanitized user input — use `esc()` helper for all user-controlled strings

---

## 4. UI/UX Standards

### Mobile-First (375px minimum)
- [ ] All new inputs: `font-size: 16px` on mobile (prevents iOS auto-zoom) — add to `@media (max-width:575px)` block
- [ ] Touch targets: `min-height: 44px` for all buttons and interactive elements
- [ ] Never add elements with `width > 100vw` — global `overflow-x: hidden` is set
- [ ] New hover styles must be suppressed in `@media (hover:none)` block
- [ ] Test mentally at 375px: can the user tap, read, and scroll?

### Bootstrap 5 Usage
- [ ] Use Bootstrap classes for layout — no custom CSS grids
- [ ] Responsive columns: always define `col-*` (xs) before `col-sm-*`, `col-md-*`
- [ ] Tables with 5+ columns: use `d-none d-sm-table-cell` to hide secondary columns on mobile
- [ ] Icons: Bootstrap Icons 1.11.3 only — no other icon libraries

### Spanish & PETINSA Workers
- [ ] All labels, buttons, error messages, placeholders in Spanish
- [ ] Error messages must be friendly — never show raw JS errors or stack traces
- [ ] Results must be scannable at a glance — Top 3 ranking is the primary output
- [ ] Autocomplete must use `norm()` — workers type with/without accents

### Visual Consistency
- [ ] Primary color: `var(--azul)` (#1a3a5c) — never hardcode hex in new components
- [ ] Card headers use `.ch` class pattern
- [ ] Ranking rows: `.rank-1` (yellow), `.rank-2` (green), `.rank-3` (blue)
- [ ] Zero-neto values: use `.neto0` class (green, bold)

---

## 5. Authentication
- [ ] Login overlay (`#login-overlay`) must appear on load when no session
- [ ] `applySession()` hides `#btn-dash` for non-admin users — never skip this
- [ ] All new features that show sensitive data (orders, history) must check role
- [ ] `doLogout()` must clear sessionStorage and reload — no partial state

---

## 6. Supabase & Data Persistence
- [ ] `SUPABASE_URL` and `SUPABASE_KEY` injected at build time via `generar_html.py` from `.env`
- [ ] All storage functions must keep `localStorage` fallback (for offline/no-credentials use)
- [ ] New columns in `pedidos` table require: SQL migration in Supabase + update `saveOrder()` + update `loadOrders()`
- [ ] Never expose service role key in HTML — publishable key only

---

## 7. Deploy Workflow (run after every change)

```bash
# 1. Regenerate HTML with latest data + credentials
python3 generar_html.py

# 2. Open locally and verify the change works
open petinsa_envios.html

# 3. Commit with descriptive message
git add html_template.py petinsa_envios.html  # add other changed files
git commit -m "Brief description of what and why"

# 4. Push to brunix (triggers Vercel preview)
git push origin brunix

# 5. When ready for production: merge to main
git checkout main && git merge brunix && git push origin main && git checkout brunix
```

### Pre-deploy Checklist
- [ ] `python3 generar_html.py` runs without errors
- [ ] HTML file size is reasonable (~300-400KB) — large spikes indicate data bloat
- [ ] Supabase credentials appear in generated HTML (grep for `tfdxcjb`)
- [ ] Login screen appears on fresh load (no sessionStorage)
- [ ] Mobile layout tested at 375px width (Chrome DevTools)

---

## 8. Self-Improvement Protocol

After completing any non-trivial task, ask:
1. **Was there a gotcha not documented in CLAUDE.md?** → Add it to Section 4 (Known Gotchas)
2. **Did a formula or business rule change?** → Update Section 3 (Data Flow / Canje formula)
3. **Was a new pattern established?** → Add it to this skill under the relevant section
4. **Did a deploy step fail or require extra steps?** → Update Section 7 (Deploy Workflow)

Keep CLAUDE.md and this skill in sync. If a rule appears in both, CLAUDE.md is the
source of truth — update it first, then reflect the change here.

---

## Quick Reference: Files to Edit by Task Type

| Task | Files to edit |
|---|---|
| UI change | `html_template.py` → `python3 generar_html.py` |
| New product category | `generar_html_data.py` + `generar_html.py` (both MAPPING dicts) |
| New agency | Same as above + verify tariff sheet columns |
| Pricing logic | `html_template.py` (getCosto, getNeto, getRankScore) |
| New Supabase column | SQL migration + `html_template.py` (saveOrder/loadOrders) |
| Monthly tariff update | `generar_html.py` line ~254 (sheet name) |
| New auth user | `POST /auth/v1/admin/users` with service role key (see memory) |

# Skills — Diseño Mobile Responsive

Referencia técnica para implementar y mantener el diseño responsive de `petinsa_envios.html`.
Stack: Bootstrap 5.3.3 + Vanilla JS + CSS custom. Sin frameworks adicionales.

---

## 1. Bootstrap 5 Responsive Grid

**Breakpoints:**
| Nombre | Ancho mínimo | Clase prefix |
|--------|-------------|--------------|
| xs     | <576px      | `col-*`      |
| sm     | ≥576px      | `col-sm-*`   |
| md     | ≥768px      | `col-md-*`   |
| lg     | ≥992px      | `col-lg-*`   |

**Regla:** siempre definir el comportamiento `xs` primero. `col-12 col-sm-6 col-md-3` = ancho completo en mobile, mitad en tablet, cuarto en desktop.

**Anti-patrón:** `col-md-3 col-sm-6` sin `col-*` → a menos de 576px Bootstrap no tiene instrucciones y usa `col` (auto), que puede quedar aplastado.

---

## 2. Tablas Responsive

- **Regla:** toda `<table>` debe estar dentro de `<div class="table-responsive">`
- Esto agrega scroll horizontal nativo cuando la tabla no cabe, en vez de romper el layout
- Para tablas con 7+ columnas en mobile: el scroll horizontal es la solución aceptable
- Para tablas críticas (ej. resultados): considerar ocultar columnas secundarias con `d-none d-md-table-cell` y mostrarlas solo en desktop

---

## 3. Touch-Friendly UI

- **Tap targets mínimo 44×44px** (WCAG 2.1 AA) — todos los botones e inputs deben cumplirlo
- **iOS zoom automático:** si un `<input>` tiene `font-size < 16px`, iOS hace zoom al enfocar. Usar `font-size: 16px` mínimo en inputs en mobile
- **Espaciado táctil:** mínimo 8px entre elementos clicables
- Botones de acción principal: usar `btn-lg` o `min-height: 44px` en mobile

---

## 4. Navegación en Mobile

- **Tabs con texto largo:** en mobile mostrar solo íconos, ocultar texto con `d-none d-sm-inline` o una clase custom `.tab-txt`
- Los íconos de Bootstrap Icons (`bi bi-*`) son suficientemente descriptivos solos
- Alternativa para muchos tabs: stack vertical con `flex-direction: column` bajo breakpoint

---

## 5. Formularios en Mobile

- Todos los campos deben apilarse a `col-12` en xs — nunca dejar campos inline en pantallas <576px
- `form-control-sm` puede ser demasiado pequeño para dedos; preferir `form-control` en mobile
- Labels siempre arriba del input (comportamiento default de Bootstrap con `form-label`)
- Inputs de tipo `date`, `number`, `range`: nativo del browser en mobile, no necesitan librerías

---

## 6. Anchos Fijos — Eliminar

- **Problema:** `width: 68px` en un input dentro de una tabla en una pantalla de 375px ocupa el 18% de la pantalla y no deja espacio para el resto
- **Solución:** usar `width: 100%` o clases Bootstrap. Solo usar `min-width` si es absolutamente necesario
- **Excepción:** botones de íconos puros (delete, edit) pueden tener `width: 36px` si son solo ícono

---

## 7. Flexbox en Mobile

- `flex-wrap: wrap` es obligatorio en cualquier `d-flex` que tenga múltiples elementos en fila
- `gap-4` (1.5rem) es excesivo en 375px — reducir a `gap-2` (0.5rem) con media query
- `justify-content-between` no refleja automáticamente; si los elementos deben apilarse, cambiar a `flex-column` en mobile
- Patrón seguro: `d-flex flex-wrap gap-2`

---

## 8. Autocomplete y Dropdowns

- `max-height: 270px` en un dropdown ocupa ~40% de la pantalla de 667px y ~70% de pantallas más chicas
- Usar `max-height: 40vh` para que nunca tape más del 40% de la pantalla
- `z-index` del dropdown debe superar al teclado virtual (z-index: 9999 es suficiente)
- Items del autocomplete: mínimo `padding: .6rem .8rem` para touch cómodo (~44px altura)
- Descripciones largas: truncar con `text-overflow: ellipsis` o limitar `substring()`

---

## 9. Media Queries Custom

Cuando Bootstrap no llega, usar:

```css
/* Solo mobile */
@media (max-width: 575px) {
  /* aquí */
}

/* Tablet y arriba */
@media (min-width: 576px) {
  /* aquí */
}
```

**Regla en este proyecto:** usar media queries solo para lo que Bootstrap no cubre. No duplicar lo que hacen las clases `col-*`, `d-none`, etc.

---

## 10. Testing

**Proceso:**
1. Chrome → F12 → Toggle Device Toolbar (Ctrl+Shift+M)
2. Seleccionar **iPhone SE** (375×667) — el más restrictivo
3. Checks obligatorios:
   - Sin scroll horizontal en el `<body>`
   - Todos los botones/inputs accesibles con el dedo (mínimo 44px)
   - Texto legible sin hacer zoom
   - Formularios apilados, no aplastados
   - Tablas con scroll horizontal nativo
   - Autocomplete no tapa toda la pantalla
4. Probar también en **iPad Mini** (768×1024) para verificar breakpoint `md`

**Herramientas:**
- Chrome DevTools responsive mode
- Abrir el archivo `.html` directamente (no necesita servidor)

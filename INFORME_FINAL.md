# Informe Final
## Sistema de Recomendación de Agencias de Envío para PETINSA
### Proyecto de Aprendizaje Automático — Junio 2026

---

**Autores:** Bruno Pignanelli · Priscila Gerlach  
**Empresa:** PETINSA (distribuidora de neumáticos, Uruguay)  
**Entregable en producción:** `ml-proyecto.vercel.app/petinsa_envios.html`

---

## Resumen Ejecutivo

Este proyecto consistió en el diseño, desarrollo y despliegue de un sistema de recomendación de agencias de transporte para PETINSA, una empresa distribuidora de neumáticos del Uruguay. Ante la necesidad de decidir entre 14 agencias de envío para cada pedido, donde cada agencia tiene su propia estructura de precios, nomenclatura de productos y sistema de canje, la empresa carecía de un proceso sistematizado para tomar esa decisión. El resultado del proyecto es una aplicación web progresiva (PWA), instalable en el celular de los empleados, que dado un pedido de productos devuelve en segundos el ranking de agencias ordenado por costo real, diferenciando entre precio bruto, cashflow efectivo y costo económico verdadero. La aplicación está en producción desde junio de 2026.

---

## 1. Propuesta Inicial

### 1.1 Contexto de la Empresa

PETINSA es una empresa distribuidora de neumáticos que opera en Uruguay. Su modelo de negocio consiste en vender neumáticos a clientes del interior del país y coordinar los envíos a través de agencias de transporte privadas. Para cada pedido, la empresa debe seleccionar cuál de sus 14 agencias habituales realizará el envío.

Las 14 agencias con las que trabaja PETINSA son: DAC, NASAZZI, MEGAM, Transportes Nagar (Ruta 1), SELEGUIN, EXPRESO ROCHA, BULEVAR (ACC), PERICO, TRUJILLO, GONFER, 3EME (El Chambon), Martin Escudero (Lascano), Arzuaga y Franchi.

### 1.2 El Problema Identificado

La decisión de qué agencia usar para cada envío se tomaba de forma intuitiva. El trabajador responsable consultaba mentalmente el tarifario y elegía según su experiencia. Este proceso presentaba cuatro problemas concretos:

**Heterogeneidad de categorías.** Cada agencia clasifica los productos de manera diferente. Una cubierta `205/70 R16` puede ser llamada "Rodado 15 a 18" por DAC, "Rodado 15 a 19" por NASAZZI, "Cubierta auto (15 a 17)" por MEGAM, o simplemente "Auto" por Nagar. No existe un lenguaje común, lo que hace imposible comparar precios directamente.

**Complejidad del canje.** Varias agencias ofrecen "canje": en lugar de cobrar el envío en dinero, aceptan que PETINSA pague parcial o totalmente con neumáticos. Los porcentajes van del 0% al 100%, y su interpretación económica no es trivial —un envío con 100% de canje no es gratuito para la empresa, porque los neumáticos entregados también tienen un costo de oportunidad.

**Volumen de información.** El tarifario de 14 agencias se actualiza mensualmente. Consultarlo manualmente en cada pedido es lento y propenso a errores.

**Falta de trazabilidad.** No existía registro histórico de las decisiones tomadas ni de los costos incurridos, por lo que era imposible analizar si las elecciones habían sido eficientes.

### 1.3 Objetivo del Proyecto

Construir un sistema que, dado un pedido de uno o más productos con sus cantidades (y opcionalmente el destino del envío), devuelva automáticamente el ranking de las agencias más convenientes, ordenadas por costo real, con información clara sobre el precio bruto, el cashflow efectivo y el costo económico verdadero del canje.

### 1.4 Beneficios Esperados para la Empresa

- **Reducción de costos de envío** mediante comparación objetiva y sistemática entre agencias.
- **Eliminación del criterio intuitivo** en favor de datos concretos, comparables y auditables.
- **Ahorro de tiempo** en la toma de decisión: de una consulta manual de varios minutos a una respuesta en segundos.
- **Trazabilidad y análisis histórico** de todos los envíos realizados, habilitando reportes de gasto y detección de patrones.
- **Herramienta accesible desde el celular**, instalable como aplicación nativa, sin necesidad de computadora ni conocimientos técnicos por parte del usuario final.

---

## 2. Marco Teórico y Decisiones Metodológicas

### 2.1 Sistema Basado en Reglas vs. Machine Learning

Una decisión central del proyecto fue definir si el núcleo del sistema de recomendación sería un modelo de machine learning o un sistema basado en reglas. Se optó por reglas, fundamentado en tres criterios:

1. **La lógica de negocio es explícita y conocida.** Las reglas de tarifación están documentadas en el Excel mensual de cada agencia. No hay ambigüedad que requiera inferencia estadística.

2. **No existen datos históricos etiquetados.** Para entrenar un modelo supervisado se necesitaría un histórico de pedidos con la etiqueta "esta fue la agencia correcta". PETINSA no contaba con ese registro.

3. **La explicabilidad es un requisito.** PETINSA necesita poder auditar cada decisión del sistema, ya que se trata de dinero real. Un modelo caja negra no sería aceptable operativamente.

Sin embargo, el diseño del sistema contempla la incorporación futura de ML cuando el historial de pedidos guardado en la base de datos sea suficiente (ver sección de mejoras futuras).

### 2.2 Arquitectura del Sistema

Se evaluaron dos arquitecturas posibles:

**Opción A — Servidor Python (Streamlit).** Un prototipo inicial se construyó con Streamlit, que permite crear interfaces web desde Python de forma rápida. Esta opción resultó descartada porque requería un servidor Python en ejecución permanente, lo que implicaba costos de infraestructura y mantenimiento que PETINSA no podía asumir.

**Opción B — Aplicación estática con generación en build time.** La arquitectura elegida. Python ejecuta localmente para generar un único archivo HTML con todos los datos embebidos. Ese archivo se sirve desde Vercel de forma estática y gratuita. No hay backend en tiempo de ejecución. Esta decisión permitió que la solución sea sostenible a largo plazo sin costos operativos.

---

## 3. Desarrollo

### 3.1 Análisis de los Datos Disponibles

El proyecto partió de dos fuentes de datos provistas por PETINSA:

**Tarifario de agencias (`COMPARATIVA AGENCIAS.xlsx`).** Archivo con 18 hojas, una por mes desde diciembre de 2023 hasta mayo de 2026. Cada hoja contiene los nombres de las 14 agencias, su porcentaje de canje, su frecuencia de retiro y su listado de categorías con precios (IVA incluido, excepto GONFER que publica precios sin IVA).

**Catálogo de productos (`Libro1.xlsx`).** Exportación del ERP de PETINSA con 1.437 productos. Cada producto tiene código, descripción, familia, ramo, stock y precio de lista.

El análisis de estos datos reveló el desafío central del proyecto: **las categorías del tarifario de cada agencia no son comparables entre sí**. Para poder comparar precios entre las 14 agencias, era necesario construir una capa intermedia de categorías unificadas.

### 3.2 Diseño de la Categorización Unificada

Este fue el aporte técnico más importante del proyecto y la pieza que requirió mayor análisis.

**El problema.** Para una misma cubierta, cada agencia usa un nombre diferente. Compararlas directamente es imposible sin una referencia común.

**La solución.** Se definieron 16 categorías unificadas de envío que sirven como lingua franca entre todas las agencias. Estas categorías no son arbitrarias: se derivaron directamente de los criterios que las propias agencias usan para separar precios en su tarifario.

Las 16 categorías son:
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
13. Cámara (por tipo de cubierta)
14. Batería Chica (hasta 110 Amp)
15. Batería Grande (+110 Amp)
16. Lubricantes (caja / lata / tambor)

**Regla de asignación.** Cada uno de los 1.437 productos del catálogo de PETINSA se asigna a una de estas categorías mediante la función `classify()`, que aplica la siguiente lógica en dos pasos:

*Paso 1:* 38 de los 54 ramos del catálogo se mapean directamente a una categoría unificada. Por ejemplo, cualquier producto del ramo `LUBRICANTES MOTOR` va a la categoría `Lubricantes`, y cualquier producto del ramo `NEUMATICO MOTO REG` va a `Cubierta Moto`.

*Paso 2:* Los 16 ramos restantes se subdividen según una dimensión física leída con expresiones regulares de la descripción del producto. El criterio varía según el tipo:
- Cubiertas de auto y camioneta: se extrae el **rodado en pulgadas** (R13, R14, R15, R16, etc.)
- Cubiertas agrícolas traseras: rodado con umbrales en 24", 28" y 34"
- Cubiertas de camión: umbral en 22.5"
- Baterías: amperaje con umbral en 110 Amp

Los umbrales fueron heredados del propio tarifario de las agencias, no definidos arbitrariamente. Cuando DAC cobra diferente para R14 y R15, el corte está en 15. Esto le da legitimidad técnica a la categorización: refleja la realidad comercial, no una decisión del equipo.

### 3.3 Fórmula del Costo Real con Canje

Un aspecto crítico del proyecto fue modelar correctamente el canje. El canje es un mecanismo por el cual la agencia acepta que PETINSA pague parte del envío con neumáticos en lugar de dinero. Los porcentajes varían por agencia (entre 0% y 100%).

Se identificaron dos interpretaciones posibles:

**Interpretación A (cashflow).** El canje reduce directamente el dinero que sale de la empresa:
```
Efectivo = bruto × (1 − canje)
```
Bajo esta interpretación, una agencia con 100% de canje tiene efectivo = 0. Matemáticamente correcto desde el punto de vista del flujo de caja, pero operativamente engañoso: los neumáticos entregados también tienen un costo.

**Interpretación B (costo real).** Los neumáticos entregados en canje tienen un costo de producción. Si una cubierta se vende a $100 pero le cuesta a PETINSA $60, entregarla en canje no es gratuito:
```
Costo real = bruto × (1 − canje × (1 − %costo_mercadería))
```
donde `%costo_mercadería` es el cociente costo/precio de venta de las cubiertas (ajustable con un slider, default 60%).

**Decisión:** Se implementaron ambas interpretaciones. La app muestra las tres métricas (bruto, efectivo y costo real) y usa el costo real para el ranking. El usuario puede ajustar el porcentaje de costo de mercadería para reflejar la realidad de su empresa. Este enfoque fue validado académicamente: muestra comprensión de que el canje no es "magia" y que la decisión depende del margen de la empresa.

### 3.4 Prototipo Inicial (Streamlit)

El primer entregable fue un prototipo funcional en Python con interfaz Streamlit, compuesto por cuatro módulos:

- **`parser.py`**: lee el Excel mensual y devuelve un DataFrame normalizado con categorías, precios y canjes por agencia.
- **`matcher.py`**: recibe una medida de llanta en texto libre y la mapea a la categoría correcta mediante 13 patrones de regex. Incluye fallback difuso con `difflib` para medidas no reconocidas.
- **`recomendador.py`**: calcula bruto, canje y neto para cada agencia, y devuelve el ranking.
- **`app_streamlit.py`**: interfaz web con formulario de entrada, toggle de interpretación de canje y resultados en tarjetas Top 3 (🥇🥈🥉).

El prototipo fue validado con casos reales del tarifario de mayo de 2026 y demostró la viabilidad de la solución. Sin embargo, su dependencia de un servidor Python lo hacía inviable para uso productivo en PETINSA.

### 3.5 Migración a Aplicación Estática PWA

Ante la restricción de no poder mantener un servidor, se rediseñó la arquitectura completa. La decisión fue radical pero efectiva: **separar el tiempo de construcción del tiempo de ejecución**.

El nuevo pipeline funciona así:

```
[Tiempo de construcción — máquina del desarrollador]
  Excel de tarifas
  Catálogo de productos          →  generar_html.py  →  petinsa_envios.html
  Lista de clientes

[Tiempo de ejecución — browser del usuario]
  petinsa_envios.html  (datos embebidos como JSON, lógica en JavaScript)
```

`petinsa_envios.html` es un archivo autocontenido de ~330KB que incluye todos los datos del catálogo, tarifas, clientes y destinos serializados como JSON, más toda la lógica de la aplicación en JavaScript. Vercel lo sirve de forma estática y gratuita desde un repositorio de GitHub.

Esta arquitectura logra cero costo operativo y disponibilidad global, a cambio de un paso de regeneración manual al actualizar datos (una vez por mes, cuando PETINSA actualiza el tarifario).

### 3.6 Features Desarrollados en la Aplicación

La aplicación final incluye los siguientes módulos:

**Calculadora de Envíos.** El usuario busca productos por código o descripción (búsqueda insensible a acentos), arma un pedido con múltiples productos y cantidades, ingresa el cliente (con autocompletado de 635 clientes reales de PETINSA) y el destino. La aplicación filtra automáticamente las agencias que cubren esa localidad y devuelve el ranking completo con las tres métricas de costo.

**Escanear Llanta.** Feature sin equivalente en el prototipo Streamlit. El usuario abre la cámara trasera del celular o sube una foto de una llanta. Tesseract.js (motor de OCR de código abierto que corre completamente en el browser, sin costo y sin API externa) extrae el texto de la imagen y busca patrones de medida con regex. Los productos coincidentes del catálogo aparecen con un botón "Agregar al pedido".

**Catálogo.** Vista completa de los 1.437 productos con filtros por familia y búsqueda. Permite consultar la categoría de envío y el precio de lista de cualquier producto.

**Dashboard (solo administradores).** Vista de KPIs: pedidos del día, pedidos de la semana, agencia más utilizada, total gastado. Incluye gráficas de evolución temporal y distribución por agencia (Chart.js), e historial completo de todos los pedidos guardados.

**Autenticación con roles.** Login con email y contraseña mediante Supabase Auth. El rol `admin` tiene acceso completo incluyendo el dashboard. El rol `tenant` (empleados operativos) accede solo a la calculadora, el escáner y el catálogo. La sesión se mantiene en `sessionStorage` y se limpia al cerrar el tab.

**PWA (Progressive Web App).** Una vez instalada desde Chrome o Safari, la aplicación abre en pantalla completa como una app nativa. El service worker cachea el shell para uso offline. Los empleados de PETINSA pueden instalarla en su celular desde la URL de producción.

**Persistencia con Supabase.** Cada pedido calculado puede guardarse en la base de datos de Supabase (PostgreSQL). Si no hay conexión a internet o no están configuradas las credenciales, la app cae automáticamente a `localStorage`. El historial queda disponible desde cualquier dispositivo autenticado.

### 3.7 Despliegue en Producción

El despliegue se realizó en dos plataformas complementarias:

**Supabase** para la capa de datos y autenticación: base de datos PostgreSQL con la tabla `pedidos`, autenticación con roles via Supabase Auth, y API REST para lectura/escritura desde el frontend.

**Vercel** para el hosting estático: repositorio GitHub (`BrunoPignanelli/ML-Proyecto`) conectado a Vercel en la rama `main`. Cada merge a `main` dispara automáticamente un nuevo deploy. Las credenciales de Supabase se configuran como variables de entorno en Vercel y se inyectan en el HTML en tiempo de generación.

La URL de producción es: `ml-proyecto.vercel.app/petinsa_envios.html`

El flujo de trabajo del equipo separó las ramas de desarrollo (`pri`, `brunix`) de la rama de producción (`main`), garantizando que los cambios en desarrollo no afecten a los usuarios hasta ser aprobados.

---

## 4. Arquitectura de Seguridad

La aplicación maneja datos sensibles de negocio: historial de pedidos, precios, clientes y stock. Durante el desarrollo se diseñó e implementó una arquitectura de seguridad en capas que protege tanto los datos almacenados como los endpoints de la API.

### 4.1 Autenticación con Roles (Supabase Auth)

El acceso a la aplicación requiere autenticación con email y contraseña mediante Supabase Auth. Se definieron dos roles con permisos diferenciados:

| Rol | Acceso |
|---|---|
| `admin` | Calculadora de envíos, Escanear Llanta, Catálogo, Dashboard completo, borrado de pedidos |
| `tenant` | Calculadora de envíos, Escanear Llanta, Catálogo (sin Dashboard, sin borrado) |

El rol se almacena en el campo `user_metadata.role` de cada usuario en Supabase Auth. El sistema lo lee del JWT al momento del login y lo usa para mostrar u ocultar secciones en la UI.

Los usuarios activos del sistema son tres, todos con rol `admin`: el equipo de PETINSA que utilizará la herramienta en operaciones diarias.

### 4.2 Row-Level Security (RLS) en la Base de Datos

Row-Level Security es una funcionalidad de PostgreSQL que permite definir políticas de acceso a nivel de fila dentro de la propia base de datos, independientemente de quién haga la llamada a la API. Esto garantiza que incluso si la lógica del frontend es comprometida, la base de datos rechaza operaciones no autorizadas.

Se habilitó RLS en todas las tablas públicas del proyecto:

**Tabla `pedidos`** — Tres políticas independientes:

| Política | Operación | Condición |
|---|---|---|
| `read_authenticated` | SELECT | Cualquier usuario con JWT válido |
| `insert_authenticated` | INSERT | Cualquier usuario con JWT válido |
| `delete_admin_only` | DELETE | Solo si `jwt.user_metadata.role = 'admin'` |

Esta granularidad es deliberada: un empleado operativo (`tenant`) puede calcular y guardar pedidos, pero no puede borrar el historial, ni siquiera desde la consola del browser o con una llamada directa a la API.

**Tabla `stock`** — RLS habilitado sin políticas explícitas, lo que equivale a denegar todo acceso directo. La tabla solo puede ser modificada por la función RPC interna del servidor (ver sección 4.3).

### 4.3 Operaciones Atómicas con RPC y SECURITY DEFINER

Para garantizar la consistencia entre el guardado de un pedido y el descuento del stock correspondiente, se implementó una función PostgreSQL `save_order_and_decrement_stock` que ejecuta ambas operaciones en una única transacción. Si cualquiera de los dos pasos falla (por ejemplo, stock insuficiente), toda la transacción se revierte automáticamente.

Esta función utiliza el modificador `SECURITY DEFINER`, que le permite ejecutarse con los permisos del propietario de la base de datos en lugar de los del usuario que la invoca. Esto resuelve un problema de diseño: la tabla `stock` no permite escritura directa (RLS sin políticas), pero la función sí puede modificarla internamente. Los permisos de ejecución de la función están restringidos al rol `authenticated` y al `service_role`; el rol `anon` (sin autenticación) no puede llamarla.

### 4.4 Separación de Claves de API

Supabase maneja dos tipos de claves con privilegios radicalmente diferentes:

**Clave pública (`anon key` / `publishable key`):** Se incluye en el HTML generado y está visible en el repositorio de GitHub. Esto es intencional y seguro porque, con las políticas RLS correctamente configuradas, esta clave no otorga acceso a ningún dato sin un JWT de usuario válido. Su único rol es identificar el proyecto al momento de autenticar.

**Clave de servicio (`service_role key`):** Tiene acceso total a la base de datos ignorando el RLS. Esta clave nunca se incluye en el HTML ni se sube al repositorio. Vive exclusivamente en el archivo `.env` local (incluido en `.gitignore`) y se usa únicamente para operaciones administrativas puntuales, como la carga inicial del stock desde el ERP.

Este principio de mínimo privilegio garantiza que una exposición accidental del código fuente no comprometa la integridad de los datos.

### 4.5 Uso del JWT del Usuario en Todas las Llamadas

Un error común en aplicaciones que usan Supabase desde el browser es utilizar la clave pública (`anon key`) como token de autorización en todas las llamadas, incluso después de que el usuario se autenticó. En ese escenario, las políticas RLS que requieren un usuario autenticado no funcionan porque el servidor las evalúa contra el token enviado en el header `Authorization`, no contra la sesión del cliente.

En esta aplicación, todas las llamadas a la API de Supabase utilizan el JWT personal del usuario logueado como token Bearer. La función `getAuthHeaders()` recupera el token activo de `localStorage` y lo inyecta automáticamente en cada request, garantizando que el RLS funcione correctamente para cada usuario.

### 4.6 Sesiones Persistentes con Refresh Token

El mecanismo de sesión fue diseñado para balancear seguridad y usabilidad:

- La sesión se guarda en `localStorage` (persiste entre cierres del browser, conveniente para un equipo interno).
- Se almacena tanto el `access_token` (JWT de corta duración, 1 hora) como el `refresh_token` (larga duración).
- Cuando el `access_token` está próximo a expirar (menos de 5 minutos), la aplicación lo renueva automáticamente en segundo plano llamando al endpoint `/auth/v1/token?grant_type=refresh_token` de Supabase. El usuario no nota ninguna interrupción.
- Si el refresh falla (token revocado o expirado), la sesión se limpia y aparece el formulario de login.
- El botón "Salir" limpia completamente el `localStorage`, garantizando que en una computadora compartida el usuario pueda cerrar sesión de forma definitiva.

### 4.7 Cifrado en Tránsito

Toda la comunicación entre el browser del usuario y los servidores (Vercel para el HTML, Supabase para los datos y la autenticación) ocurre sobre HTTPS con certificados TLS administrados por las propias plataformas. En producción, la URL `ml-proyecto.vercel.app` fuerza HTTPS automáticamente, eliminando cualquier posibilidad de comunicación en texto plano.

---

## 5. Problemas Enfrentados

### 5.1 Heterogeneidad de los Datos del ERP

El catálogo exportado del ERP presentaba inconsistencias sistemáticas. Los códigos de producto venían como números flotantes (`20046.0` en lugar de `"20046"`), las celdas podían contener `None`, strings vacíos, espacios no separables (`\xa0`) o mayúsculas inconsistentes. Cada campo debía ser normalizado antes de cualquier comparación. La solución fue una función `norm()` en Python y su equivalente `normStr()` en JavaScript, aplicadas de forma sistemática en todos los puntos de lectura y comparación.

### 5.2 Imposibilidad de Comparar Categorías entre Agencias

El problema central del proyecto, descrito en la sección 3.2, requirió el mayor trabajo analítico. No existía ninguna documentación previa que relacionara las categorías de las 14 agencias. Fue necesario leer y analizar el tarifario de cada agencia, identificar los criterios físicos subyacentes (rodado, amperaje) y construir la tabla de equivalencias completa. Este trabajo se realizó en paralelo por dos miembros del equipo con enfoques distintos, y la decisión de cuál adoptar como tabla maestra fue tomada después de una comparación formal de ambos enfoques.

### 5.3 Interpretación del Canje

La fórmula del canje generó debate. Una primera versión trataba el canje como un descuento puro, lo que llevaba a que tres agencias (SELEGUIN, TRUJILLO, Franchi) con 100% de canje siempre aparecían primeras con costo = $0, independientemente del producto o cantidad. Esto era matemáticamente correcto pero operativamente engañoso. La solución fue implementar la Interpretación B con el slider de costo de mercadería, que refleja que entregar neumáticos en canje tiene un costo real para la empresa.

### 5.4 Restricción de Infraestructura

El prototipo Streamlit, aunque funcionalmente correcto, no era viable para producción porque requería un servidor Python en ejecución permanente. PETINSA no tiene infraestructura técnica propia. La solución implicó un rediseño completo de la arquitectura —abandonar el enfoque de servidor y migrar a generación estática— lo que significó reescribir toda la lógica de Python a JavaScript del lado del cliente.

### 5.5 Limitaciones del OCR en Condiciones Reales

El escaneo de llantas con Tesseract.js funciona bien con imágenes nítidas, pero la calidad del reconocimiento depende de las condiciones de iluminación y la nitidez de la foto. En condiciones subóptimas (fotos borrosas, llantas sucias, ángulos oblicuos), el OCR puede fallar o dar resultados incorrectos. Se implementó un fallback explícito: si el escaneo no da resultados satisfactorios, el usuario puede tipear la medida manualmente en el buscador del catálogo.

---

## 6. Conclusión

### 6.1 Beneficios Logrados

El proyecto entregó a PETINSA una herramienta operativa concreta que transforma un proceso manual, lento y propenso a errores en una decisión objetiva, trazable y ejecutable en segundos desde el celular.

**Sistematización de la decisión logística.** El proceso de selección de agencia dejó de depender del criterio individual del trabajador y pasó a basarse en datos concretos y comparables.

**Claridad sobre el costo real del canje.** La diferenciación entre precio bruto, cashflow efectivo y costo real con canje le da a la empresa por primera vez una herramienta para entender el verdadero costo económico de cada envío, independientemente de si se paga en efectivo o en neumáticos.

**Trazabilidad histórica.** El historial de pedidos guardado en Supabase es el primer registro sistematizado de decisiones logísticas que tiene la empresa. En el mediano plazo, este historial habilitará análisis de ahorro real generado, distribución de gasto por agencia y detección de patrones.

**Accesibilidad total.** La aplicación es instalable en cualquier celular sin necesidad de conocimientos técnicos. Un empleado de PETINSA puede calcular el mejor envío para un pedido en menos de un minuto, desde cualquier lugar, sin computadora.

**Costo operativo cero.** El stack tecnológico elegido (Vercel + Supabase free tier + Tesseract.js en browser) no genera costos recurrentes para la empresa.

### 6.2 Conexión con la Materia

El proyecto ilustra un principio fundamental del aprendizaje automático: **no todo problema de optimización requiere un modelo estadístico**. Cuando la lógica de negocio es conocida, los datos están estructurados y la explicabilidad es un requisito, los sistemas basados en reglas son superiores al machine learning. La elección de cuándo aplicar ML y cuándo no es en sí misma una competencia central de la disciplina.

Al mismo tiempo, el diseño del sistema fue hecho intencionalmente para facilitar la incorporación futura de ML: el historial en Supabase proveerá los datos etiquetados necesarios para entrenar un modelo de clasificación de categorías, y la arquitectura de la app está preparada para incorporar módulos de `scikit-learn` en el pipeline de generación cuando ese momento llegue.

### 6.3 Trabajo Futuro

Las mejoras prioritarias identificadas para la siguiente etapa son:

- **Comparación costo estimado vs. costo real facturado**: conectar el historial de la app con las facturas reales de las agencias para medir la precisión del estimador.
- **Score compuesto**: incorporar tiempo de entrega, frecuencia de reclamos y puntualidad como variables adicionales al ranking, no solo el precio.
- **Actualización automática del tarifario**: hoy el nombre de la hoja activa del Excel se actualiza manualmente cada mes. Un proceso automatizado de lectura y comparación de hojas eliminaría esta tarea recurrente.
- **Clasificador supervisado**: una vez acumulado suficiente historial de envíos reales, entrenar un modelo que aprenda los patrones de elección óptima, superando las limitaciones de las reglas explícitas.

---

## Anexo: Stack Tecnológico

| Componente | Tecnología | Rol |
|---|---|---|
| Generación de app | Python 3 + pandas + openpyxl | Lee Excel, clasifica productos, genera HTML |
| Frontend | HTML + CSS + JavaScript (vanilla) | Toda la UI y lógica del cliente |
| Framework CSS | Bootstrap 5.3.3 | Layout, componentes, responsive |
| Gráficas | Chart.js 4.4.3 | Dashboard KPIs |
| OCR | Tesseract.js v4 | Escaneo de llantas (corre en browser) |
| Base de datos | Supabase (PostgreSQL) | Historial de pedidos |
| Autenticación | Supabase Auth | Login con roles |
| Hosting | Vercel (static) | Sirve `petinsa_envios.html` |
| CI/CD | GitHub Actions (via Vercel) | Deploy automático en merge a `main` |
| PWA | Web App Manifest + Service Worker | Instalación en celular, uso offline |

---

*Documento generado: Junio 2026*

# Analytics y Business Intelligence: Transformando Datos en Decisiones

## Introducción

### ¿Por qué es importante Analytics y BI?

Imagina que eres el Data Engineer de **FinTech Analytics**, una empresa fintech que procesa millones de transacciones diarias. Has construido un Data Warehouse perfecto con modelado dimensional impecable (Tema 1) y pipelines dbt que transforman datos crudos en tablas analíticas limpias (Tema 2).

Pero entonces llega el CEO y pregunta: *"¿Cómo vamos este mes?"*

Tu Data Warehouse tiene terabytes de datos perfectamente estructurados... pero eso no responde la pregunta. Lo que el CEO necesita es:

- **Un número**: "Crecimos 15% vs. mes anterior"
- **Contexto visual**: Un gráfico que muestre la tendencia
- **Alertas proactivas**: "Ojo, la retención cayó 3 puntos"
- **Capacidad de explorar**: "Quiero ver desglosado por región"

**Analytics y Business Intelligence es el puente entre tu Data Warehouse y las decisiones de negocio.**

### Contexto en Data Engineering

En el ecosistema de datos moderno, tu rol como Data Engineer no termina cuando el dato está en el warehouse:

```
                                    ← HASTA AQUÍ LLEGASTE →

Fuentes → Ingesta → Transformación → Data Warehouse → ANALYTICS/BI → Decisiones
  ↓          ↓            ↓               ↓               ↓            ↓
(APIs)   (Airflow)     (dbt)        (Star Schema)    (Dashboards)  (Acciones)
                                                       (KPIs)
                                                      (Alertas)
```

Tu Data Warehouse es el **motor**, pero Analytics y BI son el **tablero de instrumentos** que permite a los "conductores" (ejecutivos, analistas, equipos) tomar decisiones informadas.

### Analogía del Mundo Real: El Panel de Control de un Avión

Piensa en la cabina de un avión comercial:

- **Datos crudos**: Sensores capturando miles de métricas (temperatura, presión, velocidad, altitud, combustible, posición GPS...)
- **Data Warehouse**: Sistema central que almacena y organiza todos estos datos
- **Dashboard (BI)**: El panel de instrumentos que muestra solo lo relevante:
  - Altitud actual (un número grande y claro)
  - Velocidad (gauge visual)
  - Combustible restante (indicador con alertas)
  - Ruta (mapa con contexto)

Un piloto no necesita ver datos crudos de 10,000 sensores. Necesita **los indicadores correctos, en el formato correcto, en el momento correcto**.

**Eso es exactamente lo que hace un buen sistema de Analytics y BI para una empresa.**

---

## Conceptos Fundamentales

### Concepto 1: Business Intelligence (BI) - Qué Es y Qué No Es

**Definición Simple**: Business Intelligence es el conjunto de estrategias, tecnologías y prácticas para transformar datos en información accionable que apoye la toma de decisiones.

**Lo que BI SÍ es**:
- Dashboards que muestran el estado del negocio
- Reportes que responden preguntas de negocio
- Alertas que notifican cuando algo importante pasa
- Análisis que permiten explorar y entender patrones

**Lo que BI NO es**:
- Magia que toma decisiones automáticamente
- Reemplazo del criterio humano
- Una herramienta que funciona sin datos de calidad
- Un proyecto de "una sola vez" (es continuo)

**Analogía del Mundo Real**:

BI es como el sistema de alarmas y monitores de un hospital:
- Los sensores (tu Data Warehouse) capturan signos vitales
- El monitor (dashboard) muestra información relevante
- Las alarmas (alertas) avisan cuando algo está fuera de rango
- El médico (usuario de negocio) toma la decisión final

El monitor no reemplaza al médico, pero le permite actuar más rápido y con mejor información.

**Por qué es importante para Data Engineers**:

1. **Diseñas para consumo**: Cuando modelas tu DWH, debes pensar en cómo se visualizará
2. **Optimizas queries**: Los dashboards ejecutan queries constantemente; deben ser eficientes
3. **Defines métricas**: Las fórmulas de KPIs deben implementarse correctamente en el DWH
4. **Aseguras calidad**: Datos incorrectos = dashboards incorrectos = decisiones incorrectas

---

### Concepto 2: Métricas vs. KPIs vs. Dimensiones

Esta distinción es fundamental y frecuentemente confundida:

**Métricas (Measures)**

Son valores numéricos que pueden ser medidos y agregados:
- Ventas totales: $1,500,000
- Número de usuarios: 50,000
- Tiempo promedio de carga: 2.3 segundos
- Tickets de soporte: 847

**Características de las métricas**:
- Son siempre números
- Pueden sumarse, promediarse, contarse
- Sin contexto, son solo números

**KPIs (Key Performance Indicators)**

Son métricas específicas que indican el progreso hacia objetivos de negocio:
- Tasa de conversión: 3.2% (objetivo: 5%)
- Customer Lifetime Value: $1,200 (objetivo: $1,500)
- Net Promoter Score: 42 (objetivo: 50)
- Churn Rate: 4.5% (objetivo: <3%)

**Características de los KPIs**:
- Son métricas con **contexto de objetivo**
- Tienen **umbrales** (rojo/amarillo/verde)
- Son **pocos y estratégicos** (5-10 máximo)
- Están **alineados con metas de negocio**

**Dimensiones (Dimensions)**

Son atributos descriptivos que dan contexto a las métricas:
- Tiempo: año, trimestre, mes, semana, día
- Geografía: país, región, ciudad, tienda
- Producto: categoría, subcategoría, marca
- Cliente: segmento, canal de adquisición, antigüedad

**Características de las dimensiones**:
- Son texto o categorías
- Permiten filtrar y agrupar métricas
- Responden "¿por qué?" y "¿dónde?"

**Analogía Práctica - Tu Cuenta Bancaria**:

| Concepto | Ejemplo |
|----------|---------|
| **Métrica** | Saldo: $5,000 |
| **KPI** | Tasa de ahorro: 15% del ingreso (objetivo: 20%) |
| **Dimensión** | Por tipo de gasto: Alimentación, Transporte, Entretenimiento |

---

### Concepto 3: La Pirámide de Métricas

Las métricas de una organización no son todas iguales. Se organizan en una pirámide:

```
                    /\
                   /  \
                  / C  \      ← ESTRATÉGICAS (CEO, Board)
                 / E O  \        Revenue, Profit, Market Share
                /________\
               /          \
              /  TÁCTICAS  \   ← TÁCTICAS (Directores, VPs)
             / Conversion,  \     Customer Acquisition Cost,
            / Churn, LTV     \    Team Productivity
           /_________________ \
          /                    \
         /     OPERATIVAS       \  ← OPERATIVAS (Managers, Teams)
        / Response Time, Tickets \    Daily Active Users,
       / Uptime, Throughput       \   Bug Count, Deploys/Day
      /____________________________\
```

**Métricas Operativas (Base)**:
- Medidas día a día
- Muchas (50-100+)
- Cambian rápidamente
- Usadas por equipos tácticos
- Ejemplo: "Tiempo promedio de respuesta del servidor: 145ms"

**Métricas Tácticas (Medio)**:
- Agregaciones semanales/mensuales
- Moderadas (10-30)
- Usadas por directores
- Ejemplo: "Costo de adquisición de cliente: $85"

**Métricas Estratégicas (Cima)**:
- Agregaciones trimestrales/anuales
- Pocas (3-7)
- Usadas por C-level y board
- Ejemplo: "Margen de beneficio neto: 12%"

**Por qué importa esta estructura**:

1. **Evita información inútil**: El CEO no necesita ver uptime del servidor
2. **Crea responsabilidad clara**: Cada nivel tiene sus métricas
3. **Permite drill-down**: De estratégico a operativo cuando hay problemas
4. **Alinea la organización**: Todos saben qué medir

---

### Concepto 4: Principios de Diseño de Dashboards

Un dashboard efectivo sigue principios claros:

**Principio 1: Un Dashboard = Una Audiencia = Un Propósito**

❌ **Malo**: Dashboard "general" con todo para todos
✅ **Bueno**: Dashboard "Ventas - Equipo Comercial - Seguimiento Semanal"

**Principio 2: Los Números Más Importantes Arriba**

La información más crítica debe verse en los primeros 3 segundos:

```
┌─────────────────────────────────────────────────────────────┐
│  💰 Revenue: $2.1M (+12%)    👥 Users: 45K (+5%)    📈 NPS: 42  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Gráfico de tendencia principal - grande y visible]        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  [Detalles secundarios]        [Filtros y controles]        │
└─────────────────────────────────────────────────────────────┘
```

**Principio 3: Comparación Siempre**

Un número solo no significa nada:
- ❌ "Ventas: $500,000"
- ✅ "Ventas: $500,000 (+15% vs. mes anterior, 95% del objetivo)"

**Principio 4: Menos es Más**

- 3-5 KPIs por dashboard (máximo 7)
- Colores con significado (rojo=malo, verde=bueno)
- Espacios en blanco para respirar
- Sin decoración innecesaria

**Principio 5: Accionable**

Cada elemento debe responder: "¿Y ahora qué hago con esto?"
- Alertas con umbrales claros
- Drill-down para investigar
- Filtros para segmentar

---

### Concepto 5: Antipatrones en Dashboards

Errores comunes que debes evitar:

**Antipatrón 1: El Dashboard "Frankenstein"**

Demasiadas métricas sin conexión lógica. 50 gráficos en una pantalla donde nadie sabe qué mirar primero.

**Solución**: Un dashboard = una historia coherente

**Antipatrón 2: El Dashboard "Sin Contexto"**

Números sin comparación, sin objetivo, sin tendencia.

❌ "Usuarios activos: 10,000"
✅ "Usuarios activos: 10,000 (↓15% vs. semana pasada, objetivo: 12,000)"

**Antipatrón 3: El Dashboard "Pixel Art"**

Gráficos 3D, gradientes rainbow, animaciones excesivas. Bonito pero ilegible.

**Solución**: Minimalismo funcional. Si un elemento no añade información, elimínalo.

**Antipatrón 4: El Dashboard "Datos Muertos"**

Dashboards que nadie mira porque:
- Se actualizan muy lento (datos de hace 2 días)
- Métricas que nadie entiende
- Sin alertas ni notificaciones

**Solución**: Datos frescos, métricas relevantes, alertas activas

**Antipatrón 5: El Dashboard "Vanity Metrics"**

Métricas que suben pero no importan:
- "Visitantes totales" (pero ¿cuántos compran?)
- "Descargas de app" (pero ¿cuántos la usan?)
- "Seguidores en redes" (pero ¿cuántos son clientes?)

**Solución**: Enfócate en métricas que impactan el negocio

---

### Concepto 6: Data Storytelling

Los mejores analistas no solo muestran datos, **cuentan historias con datos**.

**Estructura de una Historia con Datos**:

1. **Contexto**: ¿Cuál es la situación? ¿Por qué estamos viendo esto?
2. **Problema/Oportunidad**: ¿Qué descubrimos? ¿Qué nos sorprende?
3. **Análisis**: ¿Qué dicen los datos? ¿Qué patrones vemos?
4. **Recomendación**: ¿Qué deberíamos hacer?
5. **Impacto esperado**: ¿Qué pasará si actuamos (o no actuamos)?

**Ejemplo de Storytelling**:

❌ **Sin historia**: "El churn aumentó de 3% a 4.5%"

✅ **Con historia**:
> "En los últimos 3 meses, nuestra tasa de abandono subió de 3% a 4.5%.
> Investigando por segmento, descubrimos que el 80% del incremento viene de usuarios
> que compraron durante la promoción de diciembre pero no volvieron a comprar.
>
> Estos usuarios tienen un LTV promedio de $50, comparado con $200 de usuarios orgánicos.
>
> Recomendamos: (1) Mejorar onboarding post-promoción, (2) Crear programa de
> fidelización específico. Impacto estimado: reducir churn a 3.5% y recuperar
> $250K/año en revenue."

---

### Concepto 7: Herramientas de BI Modernas

Las herramientas de BI más usadas actualmente:

**Tier Enterprise (Grandes empresas)**:
- **Tableau**: El estándar de la industria, muy visual
- **Power BI**: Integración Microsoft, excelente para empresas con stack MS
- **Looker**: Modelo semántico centralizado, adquirido por Google

**Tier Mid-Market**:
- **Metabase**: Open source, fácil de usar, ideal para startups
- **Apache Superset**: Open source robusto, mantenido por Airbnb/Apache
- **Redash**: Simple y efectivo para equipos técnicos

**Tier Self-Service**:
- **Google Data Studio**: Gratis, integración con Google
- **Preset**: Superset managed, más fácil de desplegar

**¿Cuál elegir?**

| Criterio | Recomendación |
|----------|---------------|
| Presupuesto limitado | Metabase, Superset |
| Empresa Microsoft | Power BI |
| Visualizaciones complejas | Tableau |
| Equipo técnico pequeño | Metabase, Redash |
| Escala enterprise | Looker, Tableau |

**Nota importante para Data Engineers**:

Tu rol no es dominar estas herramientas a nivel experto, sino:
1. Entender cómo se conectan a tu DWH
2. Optimizar queries que ejecutan
3. Proveer modelos de datos bien estructurados
4. Documentar métricas y sus definiciones

---

### Concepto 8: Operaciones OLAP

OLAP (Online Analytical Processing) es el conjunto de operaciones que permiten a los usuarios explorar datos multidimensionales de forma interactiva. Piensa en tu Data Warehouse como un cubo de Rubik de datos: OLAP te permite girarlo, cortarlo y verlo desde diferentes ángulos.

**Analogía del Mundo Real - Google Maps**:

Las operaciones OLAP son como navegar en Google Maps:
- **Zoom out** (Roll-up): Ver el país completo
- **Zoom in** (Drill-down): Ver una calle específica
- **Filtrar** (Slice): Mostrar solo restaurantes
- **Múltiples filtros** (Dice): Restaurantes italianos abiertos ahora
- **Rotar vista** (Pivot): Cambiar de mapa a vista satélite

**Las 5 Operaciones OLAP Fundamentales**:

**1. Drill-Down (Desglosar)**

Navegar de lo general a lo específico, añadiendo niveles de detalle.

```
Ventas Anuales: $10M
    ↓ drill-down por trimestre
Q1: $2.2M | Q2: $2.5M | Q3: $2.8M | Q4: $2.5M
    ↓ drill-down por mes (Q3)
Jul: $0.9M | Ago: $1.0M | Sep: $0.9M
    ↓ drill-down por día
Sep 15: $32K | Sep 16: $28K | ...
```

**Uso típico**: "Las ventas de Q3 fueron altas, ¿qué mes contribuyó más?"

**2. Roll-Up (Agregar)**

Lo opuesto a drill-down: agregar datos a un nivel superior.

```
Ventas por tienda: Tienda A: $500K, Tienda B: $300K, Tienda C: $200K
    ↑ roll-up por región
Región Norte: $1M (Tiendas A+B+C)
    ↑ roll-up por país
España: $5M (todas las regiones)
```

**Uso típico**: "Quiero ver el total nacional, no el detalle por tienda"

**3. Slice (Cortar)**

Filtrar el cubo por UN valor de UNA dimensión, obteniendo una "rebanada".

```
Cubo de Ventas: [Tiempo] x [Producto] x [Región]
    ↓ slice: Tiempo = "2024"
Resultado: Todas las ventas de 2024, por producto y región
```

**Uso típico**: "Muéstrame solo los datos del año actual"

**4. Dice (Subcubo)**

Filtrar por MÚLTIPLES valores de MÚLTIPLES dimensiones, obteniendo un subcubo.

```
Cubo de Ventas: [Tiempo] x [Producto] x [Región]
    ↓ dice: Tiempo IN (Q1, Q2) AND Producto = "Electrónica" AND Región IN ("Norte", "Sur")
Resultado: Subcubo con solo esas combinaciones
```

**Uso típico**: "Quiero comparar electrónica en norte y sur durante el primer semestre"

**5. Pivot (Rotar)**

Cambiar la orientación del análisis, intercambiando filas por columnas.

```
ANTES (Pivot original):
         | Ene  | Feb  | Mar
Producto A| 100 | 120 | 110
Producto B| 80  | 90  | 85

DESPUÉS (Pivot rotado):
         | Producto A | Producto B
Ene      | 100        | 80
Feb      | 120        | 90
Mar      | 110        | 85
```

**Uso típico**: "Quiero ver los productos en columnas y el tiempo en filas"

**Por qué importa para Data Engineers**:

1. **Diseño de índices**: Debes optimizar para las operaciones OLAP más frecuentes
2. **Pre-agregaciones**: Calcular roll-ups comunes para mejor performance
3. **Modelado dimensional**: Las jerarquías de dimensiones habilitan drill-down/roll-up
4. **Cubos OLAP**: Algunas herramientas (SSAS, Kylin) requieren definir cubos explícitos

---

### Concepto 9: Gobernanza de Métricas

A medida que una organización crece, las métricas se multiplican y fragmentan. Marketing tiene su definición de "usuario activo", Producto tiene otra, y Finanzas una tercera. Este caos se llama **"métrica sprawl"** y es uno de los problemas más comunes en Analytics.

**Analogía del Mundo Real - El Diccionario de la RAE**:

Imagina si cada persona definiera las palabras como quisiera. "Mesa" podría significar una cosa para ti y otra para mí. La comunicación sería imposible.

La RAE existe para dar definiciones oficiales y evitar el caos. **La gobernanza de métricas es la "RAE" de tus datos**: define oficialmente qué significa cada métrica para toda la organización.

**Los 4 Pilares de la Gobernanza de Métricas**:

**1. Diccionario de Métricas Centralizado**

Un repositorio único donde se documentan todas las métricas:

```yaml
# Ejemplo de entrada en diccionario de métricas
metric:
  name: "Monthly Active Users (MAU)"
  definition: "Usuarios únicos que realizaron al menos 1 acción en los últimos 30 días"
  formula: "COUNT(DISTINCT user_id) WHERE last_action_date >= CURRENT_DATE - 30"
  source_table: "analytics.fact_user_actions"
  owner: "Equipo de Producto"
  refresh_frequency: "Diario"
  valid_from: "2024-01-01"
  related_metrics: ["DAU", "WAU", "Retention Rate"]
  caveats: "Excluye usuarios de prueba y bots conocidos"
```

**2. Ownership Claro**

Cada métrica tiene un "dueño" responsable de:
- Mantener la definición actualizada
- Responder preguntas sobre la métrica
- Aprobar cambios en la fórmula
- Comunicar cambios a stakeholders

| Métrica | Owner | Equipo |
|---------|-------|--------|
| Revenue | CFO | Finanzas |
| MAU | VP Producto | Producto |
| CAC | CMO | Marketing |
| NPS | VP Customer Success | CX |

**3. Versionado y Changelog**

Las métricas evolucionan. Documentar cambios es crítico:

```markdown
## Changelog: Monthly Active Users (MAU)

### v2.0 (2024-06-01)
- CAMBIO: Excluir usuarios con menos de 2 acciones (antes: 1)
- RAZÓN: Reducir ruido de bots no detectados
- IMPACTO: MAU bajó ~5% vs definición anterior

### v1.0 (2024-01-01)
- Definición inicial
```

**4. Auditoría y Linaje**

Saber de dónde vienen los datos y cómo se transforman:

```
Fuente: raw.user_events
    ↓
Staging: staging.stg_user_actions (limpieza)
    ↓
Intermediate: analytics.int_user_activity (agregación)
    ↓
Mart: analytics.dim_users + analytics.fact_user_actions
    ↓
Métrica: MAU (calculada en BI tool)
```

**Herramientas para Gobernanza de Métricas**:

| Herramienta | Tipo | Uso |
|-------------|------|-----|
| dbt (metrics layer) | Open source | Definir métricas en código |
| Atlan | Catálogo | Documentación y linaje |
| Monte Carlo | Observabilidad | Alertas de anomalías |
| Looker LookML | Capa semántica | Definiciones centralizadas |

**Errores Comunes en Gobernanza**:

1. **No tener diccionario**: Cada equipo inventa sus métricas
2. **Diccionario desactualizado**: Existe pero nadie lo mantiene
3. **Sin ownership**: Métricas huérfanas que nadie entiende
4. **Sin comunicación**: Cambios que rompen dashboards sin aviso

**Por qué importa para Data Engineers**:

1. **Implementas las fórmulas**: Tú escribes el SQL que calcula las métricas
2. **Mantienes el linaje**: Documenta de dónde vienen los datos
3. **Alertas de calidad**: Detecta cuando una métrica se comporta raro
4. **Single source of truth**: Tu DWH debe ser la fuente oficial

---

## Aplicaciones Prácticas

### Caso de Uso 1: E-commerce - Dashboard de Ventas

**Contexto**: RestaurantData Co. necesita un dashboard para su equipo comercial.

**KPIs principales**:
1. Revenue diario/semanal/mensual
2. Ticket promedio
3. Tasa de conversión (visitantes → compradores)
4. Top productos vendidos
5. Revenue por canal (web, app, tienda física)

**Diseño del dashboard**:

```
┌─────────────────────────────────────────────────────────────────┐
│  📅 Hoy: 15/03/2024                    [Filtro: Último Mes ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  💰 Revenue        🛒 Pedidos       🎫 Ticket Promedio          │
│  $125,430          1,847            $67.89                       │
│  ↑ 12% vs ayer     ↑ 8%             ↑ 3%                        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  [GRÁFICO: Tendencia de revenue últimos 30 días]                │
│                                                                  │
│  $150K ─────────────────────────────*                           │
│  $100K ────────*─────────────*─────/                            │
│   $50K ──*────/ \───────────/ \───/                             │
│         01   05   10   15   20   25   30                        │
│                                                                  │
├────────────────────────────┬────────────────────────────────────┤
│  📊 Por Canal              │  🏆 Top 5 Productos                │
│  Web: 45% ($56,443)        │  1. Menú Ejecutivo: $12,340        │
│  App: 35% ($43,900)        │  2. Pizza Familiar: $8,920         │
│  Físico: 20% ($25,087)     │  3. Combo Burger: $7,650           │
│                            │  4. Ensalada Premium: $5,890       │
│                            │  5. Postre del Día: $4,320         │
└────────────────────────────┴────────────────────────────────────┘
```

### Caso de Uso 2: SaaS - Métricas de Producto

**Contexto**: CloudAPI Systems quiere medir la salud de su producto.

**KPIs principales (Pirate Metrics - AARRR)**:
1. **Acquisition**: Nuevos usuarios registrados
2. **Activation**: % que completan onboarding
3. **Retention**: % que vuelven en 7/30 días
4. **Revenue**: MRR, ARPU
5. **Referral**: NPS, usuarios que refieren

**Dashboard de retención**:

```
┌─────────────────────────────────────────────────────────────────┐
│  RETENCIÓN DE USUARIOS - Cohortes Mensuales                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Cohorte    │ M0    │ M1    │ M2    │ M3    │ M4    │ M5       │
│  ───────────┼───────┼───────┼───────┼───────┼───────┼──────────│
│  Ene 2024   │ 100%  │ 45%   │ 32%   │ 28%   │ 25%   │ 24%      │
│  Feb 2024   │ 100%  │ 48%   │ 35%   │ 30%   │ 27%   │          │
│  Mar 2024   │ 100%  │ 52%   │ 38%   │ 33%   │          │          │
│  Abr 2024   │ 100%  │ 55%   │ 40%   │          │          │          │
│  May 2024   │ 100%  │ 58%   │          │          │          │          │
│                                                                  │
│  💡 Insight: La retención M1 mejoró 13 puntos desde enero       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Caso de Uso 3: Finanzas - OKRs y Métricas Ejecutivas

**Contexto**: FinTech Analytics necesita un dashboard para el board.

**Estructura OKR**:

```
OBJETIVO: Aumentar rentabilidad 20%

├── KR1: Reducir CAC de $100 a $75  [75% ████████░░]
│   └── Métricas: CAC por canal, ROI por campaña
│
├── KR2: Aumentar LTV de $500 a $700  [60% ██████░░░░]
│   └── Métricas: Churn, ticket promedio, frecuencia
│
└── KR3: Mejorar margen de 15% a 20%  [40% ████░░░░░░]
    └── Métricas: Costo operativo, pricing optimization
```

---

## Errores Comunes

### Error 1: Crear dashboards sin entender el negocio

**Por qué ocurre**: Data Engineers crean dashboards técnicamente correctos pero que nadie usa porque no responden preguntas reales de negocio.

**Cómo evitarlo**:
- Habla con los usuarios antes de diseñar
- Pregunta: "¿Qué decisión tomarías con este dato?"
- Itera basándote en feedback real

### Error 2: Definiciones inconsistentes de métricas

**Por qué ocurre**: Marketing define "usuario activo" de una forma, Producto de otra, y Finanzas de otra.

**Cómo evitarlo**:
- Crea un **diccionario de métricas** centralizado
- Implementa las fórmulas en tu capa semántica (dbt, Looker LookML)
- Documenta todo en un lugar accesible

### Error 3: Dashboards que nunca se actualizan

**Por qué ocurre**: Se crea un dashboard inicial, pero nadie lo mantiene.

**Cómo evitarlo**:
- Asigna un "owner" a cada dashboard
- Revisa dashboards trimestralmente
- Elimina los que nadie usa

### Error 4: Confundir correlación con causalidad

**Por qué ocurre**: "Las ventas subieron cuando lanzamos la campaña, entonces la campaña funcionó"

**Cómo evitarlo**:
- Siempre pregunta: "¿Qué más cambió en ese periodo?"
- Usa grupos de control cuando sea posible
- Sé honesto sobre las limitaciones del análisis

---

## Checklist de Aprendizaje

### Conceptos Básicos
- [ ] Puedo explicar qué es Business Intelligence en mis propias palabras
- [ ] Entiendo la diferencia entre métrica, KPI y dimensión
- [ ] Conozco la pirámide de métricas (operativas, tácticas, estratégicas)
- [ ] Sé identificar antipatrones en dashboards
- [ ] Entiendo las 5 operaciones OLAP (drill-down, roll-up, slice, dice, pivot)

### Diseño de Dashboards
- [ ] Puedo diseñar un dashboard para una audiencia específica
- [ ] Aplico los principios de diseño (contexto, comparación, simplicidad)
- [ ] Evito los antipatrones comunes
- [ ] Entiendo cómo estructurar una historia con datos

### Aplicación Práctica
- [ ] Puedo definir KPIs relevantes para diferentes tipos de negocio
- [ ] Sé elegir las métricas correctas para cada nivel organizacional
- [ ] Entiendo cómo las herramientas de BI se conectan con el Data Warehouse
- [ ] Puedo documentar definiciones de métricas de forma clara

### Gobernanza y Operaciones
- [ ] Sé qué es un diccionario de métricas y por qué es importante
- [ ] Entiendo los 4 pilares de gobernanza (diccionario, ownership, versionado, linaje)
- [ ] Puedo aplicar operaciones OLAP para explorar datos

### Conexión con Data Engineering
- [ ] Entiendo cómo mi diseño de DWH impacta la creación de dashboards
- [ ] Sé optimizar queries para consumo de BI
- [ ] Puedo colaborar efectivamente con analistas y usuarios de negocio
- [ ] Conozco las principales herramientas de BI del mercado

---

## Resumen

Analytics y Business Intelligence transforman tus datos estructurados en información accionable. Como Data Engineer, tu rol es fundamental:

1. **Diseña para consumo**: Tu modelado dimensional debe facilitar la creación de dashboards
2. **Define métricas claras**: Las fórmulas de KPIs deben implementarse consistentemente
3. **Optimiza para performance**: Los dashboards ejecutan queries constantemente
4. **Documenta todo**: Sin documentación, cada métrica se interpreta diferente

Recuerda la analogía del avión: tu Data Warehouse es el sistema de sensores, Analytics y BI son el panel de instrumentos. Sin un buen panel, el piloto más experimentado no puede volar seguro.

En los siguientes ejemplos y ejercicios, pondrás estos conceptos en práctica diseñando KPIs, creando dashboards mock, y construyendo un proyecto completo de métricas analíticas.

---

**Siguiente paso**: [02-EJEMPLOS.md](02-EJEMPLOS.md) - Ejemplos prácticos de KPIs y dashboards
---

## 🧭 Navegación

⬅️ **Anterior**: [Herramientas DWH - Proyecto Práctico](../tema-2-herramientas-dwh/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)

# Tema 1: Ejemplos Trabajados Paso a Paso

## 📖 Cómo Usar Esta Guía

Esta sección contiene **ejemplos resueltos completamente** para que veas cómo aplicar los conceptos de estadística en situaciones reales.

**Metodología:**
1. Lee el problema completo
2. Intenta pensar cómo lo resolverías tú
3. Lee la solución paso a paso
4. Ejecuta el código en Python para verificar

**Importante:** No te saltes los ejemplos pensando "ya lo entiendo". Cada uno enseña algo nuevo.

---

## 📊 Ejemplo 1: Análisis de Ventas Semanales de un Restaurante

### Contexto

Trabajas en **DataBite** y te piden analizar las ventas de la última semana para determinar si el restaurante está cumpliendo sus objetivos.

**Datos:**
```
Lunes:    145.30€
Martes:   132.50€
Miércoles: 189.75€
Jueves:   156.20€
Viernes:  198.50€
Sábado:   234.80€
Domingo:  175.40€
```

**Objetivo del Negocio:** Vender en promedio 170€ por día.

### Pregunta 1: ¿Cuál fue la venta promedio de la semana?

**Paso 1: Identificar qué necesitamos**
- Queremos saber el valor "promedio" → Necesitamos la **media**

**Paso 2: Organizar los datos**
```python
ventas = [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40]
```

**Paso 3: Calcular la media manualmente**
```
Suma = 145.30 + 132.50 + 189.75 + 156.20 + 198.50 + 234.80 + 175.40
Suma = 1,232.45€

Cantidad de días = 7

Media = 1,232.45 / 7 = 176.06€
```

**Paso 4: Calcular con Python**
```python
ventas = [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40]

# Forma básica
media = sum(ventas) / len(ventas)
print(f"Venta promedio: {media:.2f}€")
# Output: Venta promedio: 176.06€
```

**Paso 5: Interpretar el resultado**
```
✓ La venta promedio fue 176.06€
✓ El objetivo era 170€
✓ ¡Cumplimos el objetivo! (176.06 > 170)
```

### Pregunta 2: ¿Las ventas fueron estables o variables?

**Paso 1: Identificar qué necesitamos**
- Queremos medir la **variabilidad** → Necesitamos la **desviación estándar**

**Paso 2: Calcular la desviación estándar manualmente**

```
Paso 2.1: Ya tenemos la media = 176.06€

Paso 2.2: Calcular diferencias con la media
145.30 - 176.06 = -30.76
132.50 - 176.06 = -43.56
189.75 - 176.06 = 13.69
156.20 - 176.06 = -19.86
198.50 - 176.06 = 22.44
234.80 - 176.06 = 58.74
175.40 - 176.06 = -0.66

Paso 2.3: Elevar al cuadrado cada diferencia
(-30.76)² = 946.18
(-43.56)² = 1,897.47
(13.69)² = 187.42
(-19.86)² = 394.42
(22.44)² = 503.55
(58.74)² = 3,450.39
(-0.66)² = 0.44

Paso 2.4: Sumar los cuadrados
946.18 + 1,897.47 + 187.42 + 394.42 + 503.55 + 3,450.39 + 0.44 = 7,379.87

Paso 2.5: Dividir por cantidad (varianza)
Varianza = 7,379.87 / 7 = 1,054.27

Paso 2.6: Raíz cuadrada (desviación estándar)
Desviación = √1,054.27 = 32.47€
```

**Paso 3: Calcular con Python**
```python
import math

ventas = [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40]
media = sum(ventas) / len(ventas)

# Calcular varianza
diferencias_cuadradas = [(v - media) ** 2 for v in ventas]
varianza = sum(diferencias_cuadradas) / len(ventas)

# Calcular desviación estándar
desviacion = math.sqrt(varianza)

print(f"Media: {media:.2f}€")
print(f"Desviación estándar: {desviacion:.2f}€")
```

**Paso 4: Interpretar el resultado**
```
Media = 176.06€
Desviación = 32.47€

Interpretación:
- Las ventas se desvían ±32.47€ del promedio
- Esto es aproximadamente el 18% del promedio (32.47/176.06)
- Para un restaurante, esto indica VARIABILIDAD MODERADA
- Es normal que el fin de semana venda más
```

**Paso 5: Análisis avanzado**
```python
# ¿Qué días fueron "normales" y cuáles "atípicos"?
rango_normal_min = media - desviacion
rango_normal_max = media + desviacion

print(f"Rango normal de ventas: {rango_normal_min:.2f}€ a {rango_normal_max:.2f}€")

dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
for dia, venta in zip(dias, ventas):
    if venta < rango_normal_min:
        estado = "⬇️ Bajo"
    elif venta > rango_normal_max:
        estado = "⬆️ Alto"
    else:
        estado = "✓ Normal"
    print(f"{dia}: {venta:.2f}€ {estado}")
```

**Output:**
```
Rango normal de ventas: 143.59€ a 208.53€

Lun: 145.30€ ✓ Normal
Mar: 132.50€ ⬇️ Bajo
Mié: 189.75€ ✓ Normal
Jue: 156.20€ ✓ Normal
Vie: 198.50€ ✓ Normal
Sáb: 234.80€ ⬆️ Alto (fin de semana)
Dom: 175.40€ ✓ Normal
```

**Conclusión del Ejemplo:**
- ✅ El restaurante cumplió su objetivo (176€ > 170€)
- ✅ Las ventas son moderadamente variables (32€ de desviación)
- ✅ El sábado fue un día excepcional
- ⚠️ El martes estuvo por debajo de lo normal (investigar por qué)

---

## 🚀 Ejemplo 2: Monitoreo de API - Cumplir un SLA

### Contexto

Trabajas en **CloudMetrics** (sistema de gestión de pedidos). Tu equipo tiene un **SLA** (Service Level Agreement) que dice:

> "El 95% de las peticiones a la API deben responder en menos de 100ms"

Tienes los tiempos de respuesta de las últimas 20 peticiones.

**Datos (en milisegundos):**
```
[12, 15, 18, 14, 16, 22, 19, 17, 21, 23,
 25, 18, 20, 16, 19, 24, 28, 31, 150, 18]
```

### Pregunta: ¿Estamos cumpliendo el SLA?

**Paso 1: Entender qué mide el SLA**
- "95% de peticiones < 100ms" → Necesitamos el **Percentil 95**

**Paso 2: Organizar los datos**
```python
tiempos = [12, 15, 18, 14, 16, 22, 19, 17, 21, 23,
           25, 18, 20, 16, 19, 24, 28, 31, 150, 18]
```

**Paso 3: Calcular el Percentil 95 manualmente**

```
Paso 3.1: Ordenar los datos
[12, 14, 15, 16, 16, 17, 18, 18, 18, 19,
 19, 20, 21, 22, 23, 24, 25, 28, 31, 150]

Paso 3.2: Calcular la posición del P95
Posición = (95/100) * 20 = 19

Paso 3.3: Tomar el valor en esa posición
Posición 19 → 31ms

P95 = 31ms
```

**Paso 4: Calcular con Python**
```python
tiempos = [12, 15, 18, 14, 16, 22, 19, 17, 21, 23,
           25, 18, 20, 16, 19, 24, 28, 31, 150, 18]

# Ordenar
tiempos_ordenados = sorted(tiempos)

# Calcular posición del P95
n = len(tiempos_ordenados)
posicion = int((95 / 100) * n)

# Obtener valor
p95 = tiempos_ordenados[posicion - 1]

print(f"Percentil 95: {p95}ms")
print(f"SLA: < 100ms")
print(f"Estado: {'✅ CUMPLE' if p95 < 100 else '❌ NO CUMPLE'}")
```

**Output:**
```
Percentil 95: 31ms
SLA: < 100ms
Estado: ✅ CUMPLE
```

**Paso 5: Análisis más profundo**

```python
# Calcular otras métricas
media = sum(tiempos) / len(tiempos)
tiempos_ordenados = sorted(tiempos)
mediana = tiempos_ordenados[len(tiempos) // 2]

# Calcular varios percentiles
p50 = tiempos_ordenados[int(0.50 * len(tiempos))]
p75 = tiempos_ordenados[int(0.75 * len(tiempos))]
p99 = tiempos_ordenados[int(0.99 * len(tiempos))]

print(f"\n📊 Análisis Completo de Performance:")
print(f"  Media:        {media:.1f}ms")
print(f"  Mediana (P50): {mediana}ms")
print(f"  P75:          {p75}ms")
print(f"  P95:          {p95}ms")
print(f"  P99:          {p99}ms")
print(f"  Máximo:       {max(tiempos)}ms")

# Detectar outliers
if max(tiempos) > p95 * 3:
    print(f"\n⚠️  Outlier detectado: {max(tiempos)}ms")
    print(f"  Esto es {max(tiempos) / media:.1f}x la media")
    print(f"  Acción: Investigar esta petición específica")
```

**Output:**
```
📊 Análisis Completo de Performance:
  Media:        25.2ms
  Mediana (P50): 19ms
  P75:          24ms
  P95:          31ms
  P99:          150ms
  Máximo:       150ms

⚠️  Outlier detectado: 150ms
  Esto es 6.0x la media
  Acción: Investigar esta petición específica
```

**Paso 6: Interpretación para el equipo**

```
✅ SLA STATUS: CUMPLIENDO

Métricas clave:
- P95 = 31ms (objetivo: <100ms) ✓
- P99 = 150ms → El 99% responde en <150ms

Observaciones:
1. La API responde muy rápido en general (mediana 19ms)
2. Hay 1 petición que tardó 150ms (outlier)
   → Revisar logs de esa petición específica
   → Posible causa: base de datos lenta, cache miss, etc.
3. El P95 (31ms) está muy por debajo del objetivo (100ms)
   → Tenemos margen de seguridad de 69ms

Recomendación:
- Configurar alerta si P95 > 80ms (80% del SLA)
- Monitorear el outlier de 150ms
```

**Conclusión del Ejemplo:**
- ✅ Cumplimos el SLA (P95 < 100ms)
- ✅ Aprendimos por qué P95 es mejor que la media para SLAs
- ✅ Detectamos un outlier que requiere investigación
- ✅ Establecimos umbrales de alerta proactivos

---

## 🛒 Ejemplo 3: Identificar Productos Más Vendidos

### Contexto

Eres analista de datos en **DataBite** y te piden identificar qué productos se venden más para optimizar el inventario.

**Datos: IDs de productos vendidos hoy**
```
[101, 102, 101, 103, 101, 105, 102, 101, 104, 102,
 101, 103, 101, 102, 106, 101, 102, 101, 103, 101]
```

**Catálogo de productos:**
```
101: Hamburguesa Clásica (8.50€)
102: Pizza Margarita (10.00€)
103: Ensalada César (7.50€)
104: Pasta Carbonara (9.00€)
105: Sushi Roll (12.00€)
106: Tacos (8.00€)
```

### Pregunta 1: ¿Cuál es el producto más vendido?

**Paso 1: Identificar qué necesitamos**
- Queremos el valor más frecuente → Necesitamos la **moda**

**Paso 2: Contar manualmente**
```
101: ||||| ||||| = 10 veces
102: ||||| = 5 veces
103: ||| = 3 veces
104: | = 1 vez
105: | = 1 vez
106: | = 1 vez
```

**Paso 3: Identificar la moda**
```
Moda = 101 (Hamburguesa Clásica) con 10 ventas
```

**Paso 4: Calcular con Python (básico)**
```python
from collections import Counter

productos_vendidos = [101, 102, 101, 103, 101, 105, 102, 101, 104, 102,
                      101, 103, 101, 102, 106, 101, 102, 101, 103, 101]

# Contar frecuencias
contador = Counter(productos_vendidos)

# Encontrar el más común
producto_mas_vendido = contador.most_common(1)[0]
print(f"Producto más vendido: {producto_mas_vendido[0]} ({producto_mas_vendido[1]} veces)")
```

**Output:**
```
Producto más vendido: 101 (10 veces)
```

### Pregunta 2: ¿Cuánto representan las ventas del producto top?

**Paso 1: Calcular el porcentaje**
```python
catalogo = {
    101: "Hamburguesa Clásica",
    102: "Pizza Margarita",
    103: "Ensalada César",
    104: "Pasta Carbonara",
    105: "Sushi Roll",
    106: "Tacos"
}

total_ventas = len(productos_vendidos)
ventas_top = contador.most_common(1)[0][1]
porcentaje = (ventas_top / total_ventas) * 100

print(f"\n📊 Análisis del Producto Top:")
print(f"Producto: {catalogo[101]}")
print(f"Ventas: {ventas_top}/{total_ventas} = {porcentaje:.1f}%")
```

**Output:**
```
📊 Análisis del Producto Top:
Producto: Hamburguesa Clásica
Ventas: 10/20 = 50.0%

¡La mitad de todas las ventas son hamburguesas!
```

### Pregunta 3: Crear un reporte completo

**Código completo:**
```python
from collections import Counter

productos_vendidos = [101, 102, 101, 103, 101, 105, 102, 101, 104, 102,
                      101, 103, 101, 102, 106, 101, 102, 101, 103, 101]

catalogo = {
    101: ("Hamburguesa Clásica", 8.50),
    102: ("Pizza Margarita", 10.00),
    103: ("Ensalada César", 7.50),
    104: ("Pasta Carbonara", 9.00),
    105: ("Sushi Roll", 12.00),
    106: ("Tacos", 8.00)
}

# Contar ventas
contador = Counter(productos_vendidos)
total_productos = len(productos_vendidos)

print("🏆 RANKING DE PRODUCTOS MÁS VENDIDOS\n")
print(f"{'Pos':<4} {'Producto':<22} {'Ventas':<8} {'%':<7} {'Ingresos'}")
print("=" * 60)

# Calcular ingresos y mostrar ranking
ranking = contador.most_common()
for i, (id_producto, cantidad) in enumerate(ranking, 1):
    nombre, precio = catalogo[id_producto]
    porcentaje = (cantidad / total_productos) * 100
    ingresos = cantidad * precio

    # Barra visual
    barra = "█" * int(cantidad / 2)

    print(f"{i:<4} {nombre:<22} {cantidad:<8} {porcentaje:5.1f}%  {ingresos:6.2f}€")
    print(f"     {barra}")

# Total de ingresos
total_ingresos = sum(contador[id_prod] * catalogo[id_prod][1]
                     for id_prod in contador)
print("=" * 60)
print(f"{'TOTAL':<26} {total_productos:<8}        {total_ingresos:6.2f}€")
```

**Output:**
```
🏆 RANKING DE PRODUCTOS MÁS VENDIDOS

Pos  Producto               Ventas   %       Ingresos
============================================================
1    Hamburguesa Clásica    10       50.0%   85.00€
     █████
2    Pizza Margarita        5        25.0%   50.00€
     ██
3    Ensalada César         3        15.0%   22.50€
     █
4    Pasta Carbonara        1         5.0%    9.00€

5    Sushi Roll             1         5.0%   12.00€

6    Tacos                  1         5.0%    8.00€

============================================================
TOTAL                      20               186.50€
```

**Conclusión del Ejemplo:**
- ✅ Identificamos que la Hamburguesa es el producto estrella (50% de ventas)
- ✅ Los 2 productos top representan el 75% de las ventas
- ✅ 3 productos solo vendieron 1 unidad (revisar si mantenerlos en el menú)
- ✅ Calculamos ingresos por producto para decisiones de negocio

**Decisiones de negocio basadas en datos:**
1. Asegurar stock suficiente de hamburguesas y pizzas
2. Considerar promociones para pasta, sushi y tacos
3. Analizar rentabilidad (margen) de cada producto, no solo volumen

---

## 📈 Ejemplo 4: Comparar Dos Sucursales de un Restaurante

### Contexto

Tienes dos sucursales de DataBite y quieres saber cuál es más estable en sus ventas.

**Datos: Ventas de los últimos 10 días**

Sucursal Centro:
```python
ventas_centro = [100, 105, 98, 102, 101, 99, 103, 100, 104, 98]
```

Sucursal Playa (zona turística):
```python
ventas_playa = [50, 180, 75, 200, 60, 195, 45, 185, 70, 190]
```

### Pregunta: ¿Cuál sucursal es más estable?

**Paso 1: Calcular métricas básicas**

```python
import math

def calcular_estadisticas(datos, nombre):
    media = sum(datos) / len(datos)

    # Varianza
    diferencias = [(x - media) ** 2 for x in datos]
    varianza = sum(diferencias) / len(datos)

    # Desviación estándar
    desviacion = math.sqrt(varianza)

    # Mediana
    ordenados = sorted(datos)
    n = len(ordenados)
    if n % 2 == 0:
        mediana = (ordenados[n//2 - 1] + ordenados[n//2]) / 2
    else:
        mediana = ordenados[n//2]

    print(f"\n📊 {nombre}")
    print(f"  Ventas: {datos}")
    print(f"  Media:              {media:.2f}€")
    print(f"  Mediana:            {mediana:.2f}€")
    print(f"  Desviación Estándar: {desviacion:.2f}€")
    print(f"  Coef. Variación:    {(desviacion/media)*100:.1f}%")

    return media, desviacion

# Analizar ambas sucursales
media_centro, desv_centro = calcular_estadisticas(ventas_centro, "SUCURSAL CENTRO")
media_playa, desv_playa = calcular_estadisticas(ventas_playa, "SUCURSAL PLAYA")
```

**Output:**
```
📊 SUCURSAL CENTRO
  Ventas: [100, 105, 98, 102, 101, 99, 103, 100, 104, 98]
  Media:              101.00€
  Mediana:            100.50€
  Desviación Estándar: 2.28€
  Coef. Variación:    2.3%

📊 SUCURSAL PLAYA
  Ventas: [50, 180, 75, 200, 60, 195, 45, 185, 70, 190]
  Media:              125.00€
  Mediana:            122.50€
  Desviación Estándar: 65.72€
  Coef. Variación:    52.6%
```

**Paso 2: Comparar y concluir**

```python
print("\n" + "="*60)
print("COMPARACIÓN DE SUCURSALES")
print("="*60)

print(f"\n💰 INGRESOS:")
print(f"  Centro: {media_centro:.2f}€/día")
print(f"  Playa:  {media_playa:.2f}€/día")
print(f"  → La Playa vende {media_playa - media_centro:.2f}€ más por día")

print(f"\n📊 ESTABILIDAD:")
print(f"  Centro: ±{desv_centro:.2f}€ (muy estable)")
print(f"  Playa:  ±{desv_playa:.2f}€ (muy variable)")

print(f"\n💡 INTERPRETACIÓN:")
if desv_centro < 10:
    print(f"  ✅ Centro: PREDECIBLE - Fácil gestionar inventario")
if desv_playa > 50:
    print(f"  ⚠️  Playa: IMPREDECIBLE - Necesita más stock de seguridad")

print(f"\n🎯 RECOMENDACIONES:")
print(f"  • Centro: Modelo estable, puede optimizar costos")
print(f"  • Playa: Mayor riesgo, pero mayor retorno promedio")
print(f"  • Playa necesita inventario flexible y más staff en días pico")
```

**Conclusión del Ejemplo:**
- ✅ Ambas sucursales tienen características muy diferentes
- ✅ Centro: Menos ingresos pero MUY predecible
- ✅ Playa: Más ingresos pero MUY variable (dependencia del turismo)
- ✅ Cada una necesita estrategia operativa diferente

---

## ✅ Resumen de Aprendizajes

De estos 4 ejemplos has aprendido:

1. **Ejemplo 1:** Análisis completo con media, desviación y detección de días atípicos
2. **Ejemplo 2:** Uso de percentiles para SLAs y detección de outliers
3. **Ejemplo 3:** Aplicación de moda para decisiones de negocio (inventario, menú)
4. **Ejemplo 4:** Comparación de estabilidad usando coeficiente de variación

---

## 🎯 Próximo Paso

Ahora que has visto ejemplos resueltos, es tu turno de practicar:

➡️ **Continúa con:** `03-EJERCICIOS.md`

Allí encontrarás problemas similares para resolver por tu cuenta, con soluciones al final para que verifiques tu trabajo.

---

**Última actualización:** 2025-10-18  
**Duración de lectura:** 45-60 minutos

# Tema 1: Introducción a Python y Estadística Descriptiva

## 📚 ¿Qué Aprenderás en Este Tema?

Al finalizar este tema serás capaz de:
- ✅ Entender qué es la estadística descriptiva y por qué es fundamental en Data Engineering
- ✅ Calcular e interpretar medidas de tendencia central (media, mediana, moda)
- ✅ Calcular e interpretar medidas de dispersión (varianza, desviación estándar)
- ✅ Trabajar con percentiles para análisis avanzados
- ✅ Aplicar estos conceptos con Python
- ✅ Validar datos antes de analizarlos

**Duración estimada:** 1-2 semanas  
**Nivel:** Principiante (no se requiere conocimiento previo)

---

## 🎯 ¿Por Qué Estadística en Data Engineering?

### El Rol del Data Engineer

Un **Data Engineer** no es un estadístico, pero usa estadística constantemente para:

1. **Validar Calidad de Datos**
   ```
   ¿Este dato tiene sentido?
   → Si el promedio de edad es 150 años... ¡hay un problema!
   ```

2. **Detectar Anomalías**
   ```
   Las ventas hoy fueron 10x el promedio...
   → ¿Es real o un error?
   ```

3. **Monitorear Sistemas**
   ```
   El P95 de tiempo de respuesta subió...
   → Hay problemas de performance
   ```

4. **Reportar Métricas de Negocio**
   ```
   ¿Cuánto vendemos en promedio?
   ¿Cuál es el ticket promedio?
   ```

### Ejemplo Real: Tu Primer Día en Yurest

Imagina que hoy es tu primer día trabajando con datos del sistema **Yurest** (ventas de restaurantes).

Te pasan este archivo CSV con las ventas del día:

```csv
ticket_id,monto,hora
1,45.50,12:30
2,78.20,13:15
3,125.00,14:00
4,10000.00,15:30  ← ¿Esto es real?
5,34.80,16:45
```

**Pregunta**: ¿Cómo sabes si 10,000€ es una venta legítima o un error?

**Respuesta**: ¡Estadística!

```python
ventas = [45.50, 78.20, 125.00, 10000.00, 34.80]

promedio = calcular_media(ventas)  # 2,056.70€
mediana = calcular_mediana(ventas)  # 78.20€

# ¡Problema! El promedio y la mediana son MUY diferentes
# → Hay un outlier (valor extremo)
```

---

## 📊 Parte 1: Medidas de Tendencia Central

Las medidas de tendencia central nos ayudan a responder: **¿Cuál es el valor "típico" de mis datos?**

### 1.1 La Media (Promedio)

#### ¿Qué es?

La **media** es el valor promedio. Se calcula sumando todos los valores y dividiendo por cuántos hay.

**Fórmula matemática:**
```
Media = (Suma de todos los valores) / (Cantidad de valores)

media = Σx / n
```

No te asustes con la notación. **Σ** (sigma) significa "sumar todo".

#### Ejemplo Paso a Paso

Tienes las ventas de 5 días:

```
Lunes:    100€
Martes:   150€
Miércoles: 200€
Jueves:   120€
Viernes:  180€
```

**Cálculo:**
```
Paso 1: Sumar todos los valores
100 + 150 + 200 + 120 + 180 = 750€

Paso 2: Contar cuántos valores hay
5 días

Paso 3: Dividir
750 / 5 = 150€

La media es 150€
```

#### ¿Qué significa?

"En promedio, vendemos 150€ por día"

#### En Python:

```python
ventas = [100, 150, 200, 120, 180]

# Forma básica (sin funciones)
suma = sum(ventas)  # 750
cantidad = len(ventas)  # 5
media = suma / cantidad  # 150.0

print(f"La media es: {media}€")
```

#### ⚠️ Problema de la Media: Los Outliers

La media se ve MUY afectada por valores extremos.

**Ejemplo:**
```
Ventas normales: 100€, 110€, 105€, 115€
Día especial (boda): 5,000€

Media = (100 + 110 + 105 + 115 + 5000) / 5 = 1,086€
```

¿Dices que "en promedio vendes 1,086€"? **¡No!** Eso no representa un día típico.

**Solución:** Usar la mediana.

---

### 1.2 La Mediana

#### ¿Qué es?

La **mediana** es el valor del medio cuando ordenas todos los datos de menor a mayor.

**Ventaja:** No se ve afectada por valores extremos.

#### Ejemplo Paso a Paso (Cantidad Impar)

```
Ventas: 100€, 150€, 200€, 120€, 180€

Paso 1: Ordenar de menor a mayor
100€, 120€, 150€, 180€, 200€
              ↑
          Este es el del medio

Mediana = 150€
```

#### Ejemplo Paso a Paso (Cantidad Par)

```
Ventas: 100€, 150€, 200€, 120€

Paso 1: Ordenar
100€, 120€, 150€, 200€
        ↑     ↑
    Estos son los dos del medio

Paso 2: Promediar los dos del medio
(120 + 150) / 2 = 135€

Mediana = 135€
```

#### Comparación: Media vs Mediana

```python
# Datos normales
ventas_normales = [100, 110, 105, 115, 108]
media = 107.6€
mediana = 108€
# ✓ Ambas son similares → Los datos son "normales"

# Datos con outlier
ventas_con_outlier = [100, 110, 105, 115, 5000]
media = 1,086€   # ← Muy afectada
mediana = 110€   # ← Representa mejor el valor típico
# ⚠ Son MUY diferentes → Hay un outlier
```

#### ¿Cuándo usar cada una?

| Situación | Usar |
|-----------|------|
| Datos sin outliers | **Media** (más precisa) |
| Datos con outliers | **Mediana** (más robusta) |
| Salarios | **Mediana** (pocos CEOs con salarios altísimos) |
| Tiempos de respuesta API | **Mediana** (algunas requests muy lentas) |
| Notas de examen (sin trampas) | **Media** (representa bien el rendimiento general) |

---

### 1.3 La Moda

#### ¿Qué es?

La **moda** es el valor que más se repite.

**Nota:** Puede haber una moda, varias, o ninguna.

#### Ejemplo: Productos Más Vendidos

```
IDs de productos vendidos hoy:
101 (Hamburguesa)
102 (Pizza)
101 (Hamburguesa)
103 (Ensalada)
101 (Hamburguesa)
102 (Pizza)
104 (Pasta)

Conteo:
101 → aparece 3 veces ← MODA
102 → aparece 2 veces
103 → aparece 1 vez
104 → aparece 1 vez

La moda es 101 (Hamburguesa)
```

#### Tipos de Moda

**Unimodal:** Una sola moda
```
[1, 2, 2, 2, 3, 4]
Moda = 2
```

**Bimodal:** Dos modas
```
[1, 1, 1, 2, 3, 4, 4, 4]
Modas = 1 y 4
```

**Sin moda dominante:** Todos aparecen igual
```
[1, 2, 3, 4, 5]
Todos aparecen una vez → Todos son "modas"
```

#### ¿Cuándo es útil?

- Identificar el producto más vendido
- Encontrar la talla más común
- Detectar el error más frecuente en logs
- Analizar patrones de comportamiento

---

## 📏 Parte 2: Medidas de Dispersión

Las medidas de dispersión responden: **¿Qué tan dispersos o "esparcidos" están los datos?**

### 2.1 La Varianza

#### ¿Qué mide?

La **varianza** mide qué tan lejos están los valores de la media.

- **Varianza baja:** Los datos están juntos, cerca de la media
- **Varianza alta:** Los datos están dispersos, lejos de la media

#### Concepto Intuitivo

Imagina dos restaurantes:

**Restaurante A:** Ventas = [98€, 100€, 102€, 99€, 101€]
```
Promedio: 100€
Todos los días vende CASI 100€
→ Negocio ESTABLE, predecible
```

**Restaurante B:** Ventas = [20€, 180€, 50€, 200€, 50€]
```
Promedio: 100€ (¡igual que A!)
Pero las ventas varían MUCHO
→ Negocio IMPREDECIBLE, volátil
```

La varianza captura esta diferencia.

#### Cálculo Paso a Paso

**Ejemplo:** Calcular la varianza de [2, 4, 6, 8]

```
Paso 1: Calcular la media
media = (2 + 4 + 6 + 8) / 4 = 5

Paso 2: Calcular la diferencia de cada valor con la media
2 - 5 = -3
4 - 5 = -1
6 - 5 = 1
8 - 5 = 3

Paso 3: Elevar al cuadrado cada diferencia (para quitar el signo negativo)
(-3)² = 9
(-1)² = 1
(1)² = 1
(3)² = 9

Paso 4: Sumar todas las diferencias al cuadrado
9 + 1 + 1 + 9 = 20

Paso 5: Dividir por la cantidad de valores
20 / 4 = 5

Varianza = 5
```

#### Fórmula (no memorizar, solo referencia)

```
Varianza = Σ(x - media)² / n

Donde:
- Σ = sumar
- x = cada valor
- media = la media que calculamos
- n = cantidad de valores
```

#### ⚠️ Problema de la Varianza

Está en **unidades al cuadrado**. Si medimos euros, la varianza está en "euros²" 🤔

¿Qué significa "euros al cuadrado"? No es intuitivo.

**Solución:** Usar la desviación estándar.

---

### 2.2 La Desviación Estándar

#### ¿Qué es?

La **desviación estándar** es la raíz cuadrada de la varianza.

```
Desviación Estándar = √Varianza
```

**Ventaja:** Está en las mismas unidades que los datos originales.

#### Ejemplo

```
Ventas = [98€, 100€, 102€, 99€, 101€]

Varianza = 2 euros²  ← No intuitivo
Desviación Estándar = √2 = 1.41€  ← ¡Intuitivo!
```

**Interpretación:**
"Las ventas se desvían en promedio 1.41€ del promedio (100€)"

#### Comparación de Estabilidad

```python
# Ventas estables
restaurante_a = [98, 100, 102, 99, 101]
desviacion_a = 1.41€  # ← MUY BAJA → Estable ✓

# Ventas volátiles
restaurante_b = [20, 180, 50, 200, 50]
desviacion_b = 72.66€  # ← MUY ALTA → Impredecible ⚠
```

#### Regla Práctica (Regla 68-95-99.7)

Para datos con distribución normal:

- **68%** de los datos están a ±1 desviación estándar de la media
- **95%** de los datos están a ±2 desviaciones estándar de la media
- **99.7%** de los datos están a ±3 desviaciones estándar de la media

**Uso práctico:** Detectar outliers

```python
if valor > (media + 2 * desviacion):
    print("¡Outlier! Este valor es anormalmente alto")
```

---

## 📈 Parte 3: Percentiles

### 3.1 ¿Qué son los Percentiles?

Los **percentiles** dividen tus datos ordenados en 100 partes iguales.

**Percentil P**: El P% de los datos son menores o iguales a este valor.

#### Percentiles Comunes

| Percentil | Nombre | Significado |
|-----------|--------|-------------|
| P25 | Primer cuartil (Q1) | 25% de los datos están por debajo |
| P50 | Mediana (Q2) | 50% de los datos están por debajo |
| P75 | Tercer cuartil (Q3) | 75% de los datos están por debajo |
| P95 | Percentil 95 | 95% de los datos están por debajo |
| P99 | Percentil 99 | 99% de los datos están por debajo |

### 3.2 Ejemplo Visual

Imagina que 100 personas hacen un examen:

```
Notas ordenadas de menor a mayor:
10, 15, 20, ..., 75, 80, 85, ..., 95, 100

P50 (mediana) = la nota de la persona en posición 50
P95 = la nota de la persona en posición 95
```

Si sacaste P95 = 90 puntos:
- Significa que **el 95% de las personas sacó MENOS que tú**
- Solo el 5% sacó más
- ¡Estás en el top 5%!

### 3.3 Uso en SLAs (Service Level Agreements)

**Caso real en Agora:**

Queremos que nuestra API responda rápido. ¿Cómo definimos "rápido"?

❌ **Mal:** "La media debe ser < 50ms"
- Problema: Un request de 10 segundos arruina la media
- No representa la experiencia del usuario típico

✅ **Bien:** "El P95 debe ser < 100ms"
- Significa: El 95% de los usuarios esperan menos de 100ms
- Ignoramos el 5% de casos extremos (outliers)
- Representa mejor la experiencia real

**Ejemplo:**

```
Tiempos de respuesta (ms): [10, 12, 15, 18, 20, 22, 25, 30, 35, 500]

Media = 68.7ms   ← Afectada por el 500ms
P50 = 21ms       ← Tiempo típico
P95 = 47.5ms     ← El 95% responde en < 48ms

Conclusión: ¡Cumplimos el SLA! (P95 < 100ms)
```

---

## 🛡️ Parte 4: Validación de Datos

### 4.1 ¿Por Qué Validar?

En el mundo real, los datos son **sucios**:

```python
# Esto es lo que RECIBES:
datos = [100, 150, "doscientos", None, -50, 999999, 120]
        #     ✓    ✓      ❌        ❌   ❌     ❌      ✓
```

Si intentas calcular la media sin validar:
```python
sum(datos) / len(datos)  # ← CRASH! 💥
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

### 4.2 Validaciones Esenciales

#### 1. Tipo de Dato

```python
def validar_lista_numeros(datos):
    if not isinstance(datos, list):
        raise TypeError("Los datos deben ser una lista")
    
    for valor in datos:
        if not isinstance(valor, (int, float)):
            raise TypeError(f"Todos los elementos deben ser números, encontrado: {type(valor)}")
```

#### 2. Lista No Vacía

```python
if len(datos) == 0:
    raise ValueError("No puedes calcular la media de una lista vacía")
```

#### 3. Valores Válidos

```python
for valor in datos:
    if valor < 0 and solo_positivos:
        raise ValueError(f"Se encontró un valor negativo: {valor}")
    
    if math.isinf(valor):
        raise ValueError(f"Se encontró un valor infinito")
    
    if math.isnan(valor):
        raise ValueError(f"Se encontró un NaN (Not a Number)")
```

---

## ✅ Resumen del Tema

### Medidas de Tendencia Central
| Medida | Qué es | Cuándo usar |
|--------|---------|-------------|
| **Media** | Promedio aritmético | Datos sin outliers |
| **Mediana** | Valor del medio | Datos con outliers |
| **Moda** | Valor más frecuente | Identificar lo más común |

### Medidas de Dispersión
| Medida | Qué mide | Unidades |
|--------|----------|----------|
| **Varianza** | Dispersión al cuadrado | Unidades² |
| **Desviación Estándar** | Dispersión | Mismas que los datos |

### Percentiles
| Percentil | Uso típico |
|-----------|------------|
| P25, P50, P75 | Análisis exploratorio, boxplots |
| P95, P99 | SLAs, monitoreo de performance |

---

## 🎯 Checklist de Aprendizaje

Antes de continuar a los ejemplos y ejercicios, verifica que entiendes:

- [ ] Puedo explicar qué es la media con mis propias palabras
- [ ] Entiendo por qué la mediana es mejor para outliers
- [ ] Sé calcular manualmente la mediana (con papel y lápiz)
- [ ] Entiendo qué mide la desviación estándar
- [ ] Puedo explicar qué significa "P95 = 100ms"
- [ ] Entiendo por qué validar datos es crítico

---

## 📚 Próximo Paso

Ahora que entiendes la teoría, es momento de:

1. ✅ Ver **ejemplos trabajados** paso a paso → `02-EJEMPLOS.md`
2. ✅ Practicar con **ejercicios guiados** → `03-EJERCICIOS.md`
3. ✅ Construir el **proyecto práctico** → `04-proyecto-practico/`

**¡No te saltes los ejercicios!** La práctica es esencial para consolidar el aprendizaje.

---

**Última actualización:** 2025-10-18  
**Duración de lectura:** 30-45 minutos


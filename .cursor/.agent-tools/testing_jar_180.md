# Testing Manual - JAR-180: Misión 2 del Juego

## ✅ Checklist de Testing

### 1. Verificación de Archivos
- [x] `game.html` modificado correctamente (~1850 líneas)
- [x] `README_JUEGO_WEB.md` actualizado
- [x] `CHANGELOG.md` actualizado
- [x] No hay errores de sintaxis HTML

### 2. Testing Funcional

#### A. Flujo Completo (Misión 1 → 2A → 2B)

**Pasos para probar**:
1. Abrir `documentacion/juego/game.html` en navegador
2. Hacer clic en "NUEVA PARTIDA"
3. Ingresar nombre (ej: "TestUser")
4. Avanzar por las escenas de historia (1-4) presionando Enter o botones
5. Completar Misión 1:
   - Calcular media de: 145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40
   - Respuesta correcta: **176.06€**
   - Verificar: +100 XP, botón "CONTINUAR" aparece
6. Hacer clic en "CONTINUAR" → Debe ir a Escena 5 (Tutorial Mediana)
7. Avanzar por Escenas 5 y 6 (tutoriales)
8. Completar Misión 2A:
   - Datos: 50, 60, 55, 58, 500, 52, 57
   - Verificar: Outlier (500) destacado en **rojo**
   - Calcular mediana: **57€**
   - Verificar: +75 XP, comparación media vs mediana en feedback
   - Verificar: Botón "CONTINUAR A MISIÓN 2B"
9. Hacer clic en "CONTINUAR A MISIÓN 2B" → Debe ir a Escena 7
10. Completar Misión 2B:
    - Datos: 120, 135, 128, 200, 125, 132, 210, 130, 122
    - Verificar: Outliers (200, 210) destacados en **rojo**
    - Calcular mediana: **130€**
    - Verificar: +125 XP, análisis de outliers con IQR
    - Verificar: Total XP acumulado = 300 XP

#### B. Visualización de Outliers

**Verificar**:
- [ ] En Misión 2A: El valor 500€ aparece en **rojo** en:
  - Tarjetas de datos
  - Gráfico de barras
- [ ] En Misión 2B: Los valores 200€ y 210€ aparecen en **rojo** en:
  - Tarjetas de datos
  - Gráfico de barras
- [ ] Valores normales mantienen gradiente azul/morado

#### C. Calculadora

**Verificar**:
- [ ] Funciona con clicks
- [ ] Funciona con teclado numérico
- [ ] Botón "Copiar" pasa resultado al campo de respuesta
- [ ] Operaciones básicas (+, -, *, /) funcionan correctamente

#### D. Panel de Ayuda

**Verificar**:
- [ ] Muestra suma total correcta
- [ ] Muestra cantidad de datos correcta
- [ ] Muestra mín/máx correctos
- [ ] Fórmula se actualiza según la misión

#### E. Guardado y Carga

**Verificar**:
- [ ] Al completar Misión 1, se guarda en localStorage
- [ ] Al recargar página, botón "CARGAR PARTIDA" aparece
- [ ] Al cargar, continúa desde donde se quedó
- [ ] XP y nivel se mantienen

#### F. Respuestas Incorrectas

**Verificar**:
- [ ] Misión 2A: Ingresar valor incorrecto (ej: 100) → Muestra hint correcto
- [ ] Misión 2B: Ingresar valor incorrecto (ej: 150) → Muestra hint correcto
- [ ] Feedback es constructivo, no punitivo

### 3. Testing de Navegación

**Verificar**:
- [ ] Tecla Enter avanza escenas correctamente
- [ ] Botones "Atrás" funcionan en escenas de historia
- [ ] Transiciones suaves entre pantallas
- [ ] No hay pantallas en blanco o errores visuales

### 4. Testing Cross-Browser

**Probar en**:
- [ ] Chrome (versión actual)
- [ ] Firefox (versión actual)
- [ ] Edge (versión actual)
- [ ] Safari (si disponible)

**Verificar en cada navegador**:
- [ ] Visualización correcta
- [ ] Calculadora funciona
- [ ] Outliers se ven en rojo
- [ ] Guardado funciona (localStorage)
- [ ] No hay errores en consola (F12)

### 5. Testing Responsive (Móvil)

**Probar en**:
- [ ] Móvil vertical (375px width)
- [ ] Móvil horizontal (667px width)
- [ ] Tablet (768px width)

**Verificar**:
- [ ] Texto legible sin zoom
- [ ] Botones clickeables
- [ ] Calculadora usable
- [ ] Gráficos se adaptan
- [ ] No hay scroll horizontal

### 6. Testing de Consola

**Abrir DevTools (F12) y verificar**:
- [ ] No hay errores JavaScript en consola
- [ ] No hay warnings críticos
- [ ] localStorage se actualiza correctamente
- [ ] Funciones se ejecutan sin errores

## 📊 Resultados Esperados

### Cálculos Correctos

**Misión 1**:
- Datos: 145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40
- Media: **176.06€**

**Misión 2A**:
- Datos: 50, 60, 55, 58, 500, 52, 57
- Mediana: **57€** (ordenados: 50, 52, 55, **57**, 58, 60, 500)
- Media: **118.86€** (distorsionada por outlier)
- Outliers: [500] (índice 4)

**Misión 2B**:
- Datos: 120, 135, 128, 200, 125, 132, 210, 130, 122
- Mediana: **130€** (ordenados: 120, 122, 125, 128, **130**, 132, 135, 200, 210)
- Media: **144.67€**
- Outliers (IQR): [200, 210] (índices 3, 6)

### XP Total

- Misión 1: +100 XP
- Misión 2A: +75 XP
- Misión 2B: +125 XP
- **Total: 300 XP**

## 🐛 Problemas Conocidos

Ninguno detectado en la implementación.

## ✅ Criterios de Éxito

Para considerar el testing completo, todos los checkboxes deben estar marcados:

- [ ] Flujo completo funciona (Misión 1 → 2A → 2B)
- [ ] Outliers se visualizan correctamente en rojo
- [ ] Cálculos de mediana son correctos
- [ ] Sistema de progresión funciona
- [ ] Guardado/carga funciona
- [ ] Funciona en al menos 2 navegadores
- [ ] Responsive en móvil
- [ ] No hay errores en consola

## 📝 Notas de Testing

**Fecha**: 2025-10-19
**Tester**: [Pendiente de testing manual por usuario]
**Navegador principal**: [Pendiente]
**Resultado**: [Pendiente]

---

**Instrucciones para el usuario**:
1. Abrir `documentacion/juego/game.html` en el navegador
2. Seguir los pasos de testing
3. Marcar checkboxes según se vayan probando
4. Reportar cualquier problema encontrado

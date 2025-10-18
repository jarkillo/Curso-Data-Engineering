"""
Ejemplos Prácticos: Calculadora de Estadísticas

Este archivo contiene ejemplos EJECUTABLES que puedes correr
para ver las funciones en acción.

CÓMO USAR:
1. Asegúrate de estar en el directorio del proyecto
2. Ejecuta: python ejemplos_practicos.py
3. Lee los comentarios y observa los resultados
"""

from src.estadisticas import (
    calcular_media,
    calcular_mediana,
    calcular_moda,
    calcular_varianza,
    calcular_desviacion_estandar,
    calcular_percentiles,
)


def imprimir_separador(titulo):
    """Imprime un separador visual bonito."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)


def ejemplo_1_ventas_restaurante():
    """
    EJEMPLO 1: Análisis de Ventas de un Restaurante (Yurest)
    
    Contexto: Tienes las ventas de una semana y necesitas entender
    cómo está yendo el negocio.
    """
    imprimir_separador("EJEMPLO 1: Ventas de Restaurante")
    
    # Ventas diarias en euros
    ventas_semana = [120.50, 135.75, 98.30, 145.00, 132.80, 110.25, 155.60]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    print("\n📊 Ventas de la semana:")
    for dia, venta in zip(dias, ventas_semana):
        print(f"  {dia:12s}: {venta:7.2f}€")
    
    # Calcular estadísticas
    media = calcular_media(ventas_semana)
    mediana = calcular_mediana(ventas_semana)
    desviacion = calcular_desviacion_estandar(ventas_semana)
    
    print(f"\n📈 Análisis:")
    print(f"  Venta promedio (media):     {media:.2f}€")
    print(f"  Venta típica (mediana):     {mediana:.2f}€")
    print(f"  Desviación estándar:        {desviacion:.2f}€")
    
    # Interpretación
    print(f"\n💡 Interpretación:")
    if desviacion < 20:
        print(f"  ✓ Las ventas son MUY ESTABLES (desv. {desviacion:.1f}€)")
        print(f"    → Puedes predecir las ventas con confianza")
    elif desviacion < 40:
        print(f"  ~ Las ventas son MODERADAMENTE VARIABLES (desv. {desviacion:.1f}€)")
        print(f"    → Hay cierta variabilidad pero es manejable")
    else:
        print(f"  ⚠ Las ventas son MUY VARIABLES (desv. {desviacion:.1f}€)")
        print(f"    → Difícil predecir, investiga las causas")
    
    # ¿Qué día fue mejor?
    dia_mejor = dias[ventas_semana.index(max(ventas_semana))]
    print(f"\n  🏆 Mejor día: {dia_mejor} ({max(ventas_semana):.2f}€)")


def ejemplo_2_tiempos_api():
    """
    EJEMPLO 2: Análisis de Tiempos de Respuesta de API (Agora)
    
    Contexto: Monitoreas una API y necesitas saber si cumple el SLA
    (Service Level Agreement) de que el 95% de peticiones respondan
    en menos de 100ms.
    """
    imprimir_separador("EJEMPLO 2: Tiempos de Respuesta de API")
    
    # Tiempos de respuesta en milisegundos
    tiempos_ms = [12, 15, 13, 18, 14, 16, 15, 17, 19, 250, 14, 16]
    #                                              ↑ Este es un outlier!
    
    print("\n⏱️  Tiempos de respuesta registrados (ms):")
    print(f"  {tiempos_ms}")
    
    # Calcular estadísticas
    media = calcular_media(tiempos_ms)
    mediana = calcular_mediana(tiempos_ms)
    percentiles = calcular_percentiles(tiempos_ms, [50, 95, 99])
    
    print(f"\n📊 Estadísticas:")
    print(f"  Media:           {media:.1f}ms")
    print(f"  Mediana (P50):   {mediana:.1f}ms")
    print(f"  Percentil 95:    {percentiles[95]:.1f}ms")
    print(f"  Percentil 99:    {percentiles[99]:.1f}ms")
    
    # Comparar media vs mediana
    print(f"\n🔍 Análisis:")
    print(f"  La MEDIA ({media:.1f}ms) es mucho mayor que la MEDIANA ({mediana:.1f}ms)")
    print(f"  → Esto indica que hay OUTLIERS (valores extremos)")
    print(f"  → La mediana representa mejor el tiempo 'típico'")
    
    # Verificar SLA
    sla_objetivo = 100
    print(f"\n✅ Verificación de SLA:")
    print(f"  Objetivo: 95% de peticiones < {sla_objetivo}ms")
    
    if percentiles[95] < sla_objetivo:
        print(f"  ✓ CUMPLE: P95 = {percentiles[95]:.1f}ms < {sla_objetivo}ms")
    else:
        print(f"  ✗ NO CUMPLE: P95 = {percentiles[95]:.1f}ms > {sla_objetivo}ms")
    
    # Detectar outliers
    desv = calcular_desviacion_estandar(tiempos_ms)
    outliers = [t for t in tiempos_ms if abs(t - media) > 2 * desv]
    
    if outliers:
        print(f"\n⚠️  Outliers detectados (> 2 desviaciones): {outliers}")
        print(f"  → Investiga estas peticiones lentas")


def ejemplo_3_productos_mas_vendidos():
    """
    EJEMPLO 3: Identificar Productos Más Vendidos (Yurest)
    
    Contexto: Tienes los IDs de productos vendidos en un día y
    necesitas saber cuál es el más popular.
    """
    imprimir_separador("EJEMPLO 3: Productos Más Vendidos")
    
    # IDs de productos vendidos
    productos_vendidos = [
        101, 102, 101, 103, 101, 102, 104, 101, 105, 102,
        101, 103, 106, 101, 102, 101, 104, 101
    ]
    
    # Catálogo de productos
    catalogo = {
        101: "Hamburguesa Clásica",
        102: "Pizza Margarita",
        103: "Ensalada César",
        104: "Pasta Carbonara",
        105: "Sushi Roll",
        106: "Tacos"
    }
    
    print(f"\n📦 Total de productos vendidos: {len(productos_vendidos)}")
    print(f"\n🛒 Ventas registradas (IDs): {productos_vendidos}")
    
    # Calcular moda (producto más vendido)
    moda = calcular_moda(productos_vendidos)
    
    print(f"\n🏆 Producto(s) más vendido(s):")
    for producto_id in moda:
        nombre = catalogo.get(producto_id, "Desconocido")
        cantidad = productos_vendidos.count(producto_id)
        porcentaje = (cantidad / len(productos_vendidos)) * 100
        print(f"  • {nombre} (ID {producto_id})")
        print(f"    → Vendido {cantidad} veces ({porcentaje:.1f}% del total)")
    
    # Ranking completo
    print(f"\n📊 Ranking completo:")
    ids_unicos = sorted(set(productos_vendidos))
    ventas_por_producto = [(pid, productos_vendidos.count(pid)) for pid in ids_unicos]
    ventas_por_producto.sort(key=lambda x: x[1], reverse=True)
    
    for i, (pid, cantidad) in enumerate(ventas_por_producto, 1):
        nombre = catalogo.get(pid, "Desconocido")
        barra = "█" * (cantidad * 2)
        print(f"  {i}. {nombre:22s} {barra} ({cantidad})")


def ejemplo_4_estabilidad_datos():
    """
    EJEMPLO 4: Comparar Estabilidad de Diferentes Conjuntos de Datos
    
    Contexto: Comparamos dos sucursales de un restaurante para ver
    cuál tiene ventas más estables.
    """
    imprimir_separador("EJEMPLO 4: Comparación de Estabilidad")
    
    # Ventas de dos sucursales
    sucursal_a = [100, 102, 98, 101, 99, 103, 97, 101, 100, 102]
    sucursal_b = [50, 150, 75, 125, 60, 180, 40, 160, 70, 140]
    
    print("\n🏪 Sucursal A (Centro):")
    print(f"  Ventas: {sucursal_a}")
    media_a = calcular_media(sucursal_a)
    desv_a = calcular_desviacion_estandar(sucursal_a)
    print(f"  Media: {media_a:.1f}€, Desv. Estándar: {desv_a:.1f}€")
    
    print("\n🏪 Sucursal B (Turística):")
    print(f"  Ventas: {sucursal_b}")
    media_b = calcular_media(sucursal_b)
    desv_b = calcular_desviacion_estandar(sucursal_b)
    print(f"  Media: {media_b:.1f}€, Desv. Estándar: {desv_b:.1f}€")
    
    print(f"\n📊 Comparación:")
    print(f"  Ambas tienen una media similar:")
    print(f"    Sucursal A: {media_a:.1f}€")
    print(f"    Sucursal B: {media_b:.1f}€")
    
    print(f"\n  PERO la estabilidad es MUY diferente:")
    print(f"    Sucursal A: Desv. {desv_a:.1f}€ → MUY ESTABLE ✓")
    print(f"    Sucursal B: Desv. {desv_b:.1f}€ → MUY VARIABLE ⚠")
    
    print(f"\n💡 Conclusión:")
    print(f"  • Sucursal A: Predecible, fácil gestionar inventario")
    print(f"  • Sucursal B: Impredecible, necesita más stock de seguridad")


def ejemplo_5_validacion_robusta():
    """
    EJEMPLO 5: Demostración de Validación Robusta
    
    Contexto: Mostramos cómo las validaciones previenen errores.
    """
    imprimir_separador("EJEMPLO 5: Validación Robusta")
    
    print("\n✅ CASOS VÁLIDOS:")
    
    # Caso 1: Lista normal
    try:
        resultado = calcular_media([1, 2, 3, 4, 5])
        print(f"  ✓ calcular_media([1,2,3,4,5]) = {resultado}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Caso 2: Lista con floats
    try:
        resultado = calcular_media([1.5, 2.5, 3.5])
        print(f"  ✓ calcular_media([1.5, 2.5, 3.5]) = {resultado}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print("\n❌ CASOS INVÁLIDOS (errores detectados correctamente):")
    
    # Caso 1: Lista vacía
    try:
        resultado = calcular_media([])
        print(f"  ✓ Resultado: {resultado}")
    except ValueError as e:
        print(f"  ✓ ValueError detectado: '{e}'")
    
    # Caso 2: No es una lista
    try:
        resultado = calcular_media("12345")
        print(f"  ✓ Resultado: {resultado}")
    except TypeError as e:
        print(f"  ✓ TypeError detectado: '{e}'")
    
    # Caso 3: Lista con string
    try:
        resultado = calcular_media([1, 2, "tres", 4])
        print(f"  ✓ Resultado: {resultado}")
    except TypeError as e:
        print(f"  ✓ TypeError detectado: '{e}'")
    
    print("\n💡 Observa cómo cada error da un mensaje CLARO y ÚTIL")
    print("   Esto es FUNDAMENTAL en producción para debuggear rápido.")


def ejemplo_6_ejercicio_interactivo():
    """
    EJEMPLO 6: Ejercicio Interactivo
    
    Contexto: Analiza tus propios datos.
    """
    imprimir_separador("EJEMPLO 6: Tu Turno - Ejercicio Interactivo")
    
    print("\n📝 EJERCICIO: Analiza estos datos")
    print("\n  Tienes las calificaciones de un examen:")
    
    calificaciones = [45, 67, 89, 72, 95, 58, 76, 82, 91, 64]
    print(f"  {calificaciones}")
    
    print("\n  PREGUNTAS:")
    print("  1. ¿Cuál es la nota promedio?")
    print("  2. ¿Cuál es la nota mediana?")
    print("  3. ¿Cuál es el percentil 75? (nota que supera el 75% de estudiantes)")
    print("  4. ¿Las notas son muy variables o bastante uniformes?")
    
    print("\n  Piensa tus respuestas antes de continuar...")
    input("\n  Presiona ENTER para ver las respuestas →")
    
    # Calcular
    media = calcular_media(calificaciones)
    mediana = calcular_mediana(calificaciones)
    percentiles = calcular_percentiles(calificaciones, [75])
    desv = calcular_desviacion_estandar(calificaciones)
    
    print("\n  📊 RESPUESTAS:")
    print(f"  1. Nota promedio: {media:.1f} puntos")
    print(f"  2. Nota mediana: {mediana:.1f} puntos")
    print(f"  3. Percentil 75: {percentiles[75]:.1f} puntos")
    print(f"     (El 75% de estudiantes sacó menos de {percentiles[75]:.1f})")
    print(f"  4. Desviación estándar: {desv:.1f} puntos")
    
    if desv < 10:
        print(f"     → Notas UNIFORMES (todos rindieron similar)")
    elif desv < 15:
        print(f"     → Notas con VARIABILIDAD MEDIA")
    else:
        print(f"     → Notas MUY VARIABLES (gran dispersión de rendimiento)")


def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "EJEMPLOS PRÁCTICOS INTERACTIVOS" + " " * 22 + "║")
    print("║" + " " * 15 + "Calculadora de Estadísticas" + " " * 26 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\n🎯 Este programa ejecutará 6 ejemplos prácticos.")
    print("   Cada uno muestra un caso de uso REAL de las funciones.")
    print("   Lee con atención y observa los resultados.\n")
    
    input("Presiona ENTER para comenzar →")
    
    # Ejecutar ejemplos
    ejemplo_1_ventas_restaurante()
    input("\nPresiona ENTER para el siguiente ejemplo →")
    
    ejemplo_2_tiempos_api()
    input("\nPresiona ENTER para el siguiente ejemplo →")
    
    ejemplo_3_productos_mas_vendidos()
    input("\nPresiona ENTER para el siguiente ejemplo →")
    
    ejemplo_4_estabilidad_datos()
    input("\nPresiona ENTER para el siguiente ejemplo →")
    
    ejemplo_5_validacion_robusta()
    input("\nPresiona ENTER para el siguiente ejemplo →")
    
    ejemplo_6_ejercicio_interactivo()
    
    # Final
    imprimir_separador("FIN DE LOS EJEMPLOS")
    print("\n🎉 ¡Felicidades! Has completado todos los ejemplos.")
    print("\n📚 PRÓXIMOS PASOS:")
    print("  1. Experimenta modificando los datos en este archivo")
    print("  2. Crea tus propios casos de uso")
    print("  3. Lee GUIA_APRENDIZAJE.md para profundizar")
    print("  4. Revisa los tests en tests/test_estadisticas.py")
    print("\n💡 Recuerda: La mejor forma de aprender es PRACTICANDO.\n")


if __name__ == "__main__":
    main()


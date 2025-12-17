"""
Generador de Certificados PDF - Master en Ingeniería de Datos

Este módulo genera certificados PDF profesionales para estudiantes
que completan el programa de Data Engineering.

Dependencias:
    pip install reportlab

Uso:
    python generar_certificado.py --nombre "Juan García" --nota 8.5
"""

import hashlib
from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas
except ImportError:
    print("Error: reportlab no está instalado.")
    print("Instálalo con: pip install reportlab")
    exit(1)


# Configuración de módulos del programa
MODULOS_PROGRAMA = [
    "Fundamentos de Python y Estadística",
    "SQL",
    "ETL con Python",
    "APIs y Web Scraping",
    "Bases de Datos Avanzadas",
    "Apache Airflow",
    "Cloud (AWS/GCP)",
    "Data Warehousing",
    "Spark y Big Data",
    "ML para Data Engineers / MLOps",
]


def generar_codigo_verificacion(nombre: str, fecha: str, nota: float) -> str:
    """
    Genera un código único de verificación para el certificado.

    Args:
        nombre: Nombre completo del estudiante
        fecha: Fecha de emisión del certificado
        nota: Nota media final

    Returns:
        Código de verificación de 12 caracteres
    """
    datos = f"{nombre}-{fecha}-{nota}"
    hash_obj = hashlib.sha256(datos.encode())
    return hash_obj.hexdigest()[:12].upper()


def crear_certificado(
    nombre_estudiante: str,
    nota_media: float,
    fecha_completado: str | None = None,
    notas_modulos: list[float] | None = None,
    directorio_salida: str | None = None,
) -> str:
    """
    Genera un certificado PDF profesional.

    Args:
        nombre_estudiante: Nombre completo del estudiante
        nota_media: Nota media final (0-10)
        fecha_completado: Fecha de completado (formato: YYYY-MM-DD)
        notas_modulos: Lista de notas por módulo (opcional)
        directorio_salida: Directorio donde guardar el PDF

    Returns:
        Ruta del archivo PDF generado

    Raises:
        ValueError: Si la nota está fuera del rango válido
        ValueError: Si el nombre está vacío
    """
    # Validaciones
    if not nombre_estudiante or not nombre_estudiante.strip():
        raise ValueError("El nombre del estudiante no puede estar vacío")

    if not 0 <= nota_media <= 10:
        raise ValueError("La nota debe estar entre 0 y 10")

    if nota_media < 7.0:
        raise ValueError("Se requiere nota mínima de 7.0 para obtener certificado")

    # Configurar fecha
    if fecha_completado is None:
        fecha_completado = datetime.now().strftime("%Y-%m-%d")

    fecha_formateada = datetime.strptime(fecha_completado, "%Y-%m-%d").strftime(
        "%d de %B de %Y"
    )

    # Traducir mes al español
    meses_es = {
        "January": "enero",
        "February": "febrero",
        "March": "marzo",
        "April": "abril",
        "May": "mayo",
        "June": "junio",
        "July": "julio",
        "August": "agosto",
        "September": "septiembre",
        "October": "octubre",
        "November": "noviembre",
        "December": "diciembre",
    }
    for en, es in meses_es.items():
        fecha_formateada = fecha_formateada.replace(en, es)

    # Código de verificación
    codigo_verificacion = generar_codigo_verificacion(
        nombre_estudiante, fecha_completado, nota_media
    )

    # Determinar calificación
    if nota_media >= 9.5:
        calificacion = "MATRÍCULA DE HONOR"
        color_calificacion = colors.HexColor("#FFD700")  # Dorado
    elif nota_media >= 9.0:
        calificacion = "SOBRESALIENTE"
        color_calificacion = colors.HexColor("#4CAF50")  # Verde
    elif nota_media >= 7.0:
        calificacion = "NOTABLE"
        color_calificacion = colors.HexColor("#2196F3")  # Azul
    else:
        calificacion = "APROBADO"
        color_calificacion = colors.HexColor("#607D8B")  # Gris

    # Configurar directorio de salida
    if directorio_salida is None:
        directorio_salida = Path(__file__).parent / "certificados"
    else:
        directorio_salida = Path(directorio_salida)

    directorio_salida.mkdir(parents=True, exist_ok=True)

    # Nombre del archivo
    nombre_archivo = nombre_estudiante.lower().replace(" ", "_")
    nombre_archivo = "".join(c for c in nombre_archivo if c.isalnum() or c == "_")
    ruta_pdf = (
        directorio_salida / f"certificado_{nombre_archivo}_{fecha_completado}.pdf"
    )

    # Crear el PDF en formato apaisado
    c = canvas.Canvas(str(ruta_pdf), pagesize=landscape(A4))
    ancho, alto = landscape(A4)

    # Fondo con gradiente simulado (rectángulos)
    c.setFillColor(colors.HexColor("#1a1a2e"))
    c.rect(0, 0, ancho, alto, fill=1, stroke=0)

    # Borde decorativo
    c.setStrokeColor(colors.HexColor("#00d4ff"))
    c.setLineWidth(3)
    c.roundRect(20, 20, ancho - 40, alto - 40, 10)

    # Borde interno
    c.setStrokeColor(colors.HexColor("#0072ff"))
    c.setLineWidth(1)
    c.roundRect(30, 30, ancho - 60, alto - 60, 8)

    # Título principal
    c.setFillColor(colors.HexColor("#00d4ff"))
    c.setFont("Helvetica-Bold", 42)
    c.drawCentredString(ancho / 2, alto - 100, "CERTIFICADO DE FINALIZACIÓN")

    # Subtítulo
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 18)
    c.drawCentredString(ancho / 2, alto - 140, "Master en Ingeniería de Datos con IA")

    # Línea decorativa
    c.setStrokeColor(colors.HexColor("#00d4ff"))
    c.setLineWidth(2)
    c.line(ancho / 2 - 150, alto - 160, ancho / 2 + 150, alto - 160)

    # Texto certificación
    c.setFillColor(colors.HexColor("#b0b0b0"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(ancho / 2, alto - 200, "Se certifica que")

    # Nombre del estudiante
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(ancho / 2, alto - 250, nombre_estudiante.upper())

    # Línea bajo el nombre
    nombre_ancho = c.stringWidth(nombre_estudiante.upper(), "Helvetica-Bold", 36)
    c.setStrokeColor(colors.HexColor("#00d4ff"))
    c.setLineWidth(1)
    c.line(
        ancho / 2 - nombre_ancho / 2 - 20,
        alto - 265,
        ancho / 2 + nombre_ancho / 2 + 20,
        alto - 265,
    )

    # Texto completado
    c.setFillColor(colors.HexColor("#b0b0b0"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(
        ancho / 2, alto - 300, "ha completado satisfactoriamente el programa de"
    )

    # Programa
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(ancho / 2, alto - 330, "MASTER EN INGENIERÍA DE DATOS")

    # Calificación
    c.setFillColor(color_calificacion)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(ancho / 2, alto - 380, f"Calificación: {calificacion}")

    # Nota numérica
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 410, f"Nota Media: {nota_media:.2f}/10")

    # Módulos completados (en dos columnas)
    c.setFillColor(colors.HexColor("#888888"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(ancho / 2, alto - 450, "Módulos Completados:")

    y_modulos = alto - 470
    col1_x = ancho / 2 - 200
    col2_x = ancho / 2 + 50

    c.setFont("Helvetica", 9)
    for i, modulo in enumerate(MODULOS_PROGRAMA):
        x = col1_x if i < 5 else col2_x
        y = y_modulos - (i % 5) * 15
        nota_modulo = (
            notas_modulos[i] if notas_modulos and i < len(notas_modulos) else nota_media
        )
        c.setFillColor(colors.HexColor("#666666"))
        c.drawString(x, y, f"✓ {modulo}")
        if notas_modulos:
            c.setFillColor(colors.HexColor("#00d4ff"))
            c.drawString(x + 220, y, f"({nota_modulo:.1f})")

    # Fecha
    c.setFillColor(colors.HexColor("#b0b0b0"))
    c.setFont("Helvetica", 12)
    c.drawCentredString(ancho / 2, 100, f"Emitido el {fecha_formateada}")

    # Código de verificación
    c.setFillColor(colors.HexColor("#666666"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(ancho / 2, 70, f"Código de verificación: {codigo_verificacion}")

    # Firmas
    c.setStrokeColor(colors.HexColor("#444444"))
    c.setLineWidth(1)

    # Firma izquierda
    c.line(100, 130, 250, 130)
    c.setFillColor(colors.HexColor("#888888"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(175, 115, "Director del Programa")

    # Firma derecha
    c.line(ancho - 250, 130, ancho - 100, 130)
    c.drawCentredString(ancho - 175, 115, "Coordinador Académico")

    # Logo/Marca de agua (texto)
    c.setFillColor(colors.HexColor("#222233"))
    c.setFont("Helvetica-Bold", 100)
    c.saveState()
    c.translate(ancho / 2, alto / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, "DATA ENGINEER")
    c.restoreState()

    # Guardar PDF
    c.save()

    return str(ruta_pdf)


def verificar_certificado(codigo: str, nombre: str, fecha: str, nota: float) -> bool:
    """
    Verifica la autenticidad de un certificado.

    Args:
        codigo: Código de verificación del certificado
        nombre: Nombre del estudiante
        fecha: Fecha de emisión
        nota: Nota media

    Returns:
        True si el certificado es auténtico
    """
    codigo_esperado = generar_codigo_verificacion(nombre, fecha, nota)
    return codigo.upper() == codigo_esperado


def main():
    """Función principal para uso desde línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Genera certificados PDF para el Master en Ingeniería de Datos"
    )
    parser.add_argument("--nombre", required=True, help="Nombre del estudiante")
    parser.add_argument(
        "--nota", type=float, required=True, help="Nota media (7.0-10.0)"
    )
    parser.add_argument(
        "--fecha", default=None, help="Fecha de completado (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--notas-modulos",
        nargs=10,
        type=float,
        help="Notas de cada módulo (10 valores)",
    )
    parser.add_argument(
        "--verificar",
        nargs=4,
        metavar=("CODIGO", "NOMBRE", "FECHA", "NOTA"),
        help="Verificar un certificado existente",
    )

    args = parser.parse_args()

    if args.verificar:
        codigo, nombre, fecha, nota = args.verificar
        es_valido = verificar_certificado(codigo, nombre, fecha, float(nota))
        if es_valido:
            print("✅ Certificado VÁLIDO")
        else:
            print("❌ Certificado NO VÁLIDO")
        return

    try:
        ruta = crear_certificado(
            nombre_estudiante=args.nombre,
            nota_media=args.nota,
            fecha_completado=args.fecha,
            notas_modulos=args.notas_modulos,
        )
        print("✅ Certificado generado exitosamente:")
        print(f"   📄 {ruta}")
    except ValueError as e:
        print(f"❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

"""
Sistema de Tracking de Progreso - Master en Ingeniería de Datos

Este módulo gestiona el seguimiento del progreso de los estudiantes,
almacena resultados de exámenes y genera reportes de avance.

Uso:
    from tracking_progreso import ProgresoEstudiante

    progreso = ProgresoEstudiante("Juan García")
    progreso.registrar_examen(1, 85)
    progreso.mostrar_dashboard()
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict


class ResultadoExamen(TypedDict):
    """Estructura de un resultado de examen."""

    modulo: int
    puntuacion: float
    fecha: str
    aprobado: bool
    intentos: int


class DatosEstudiante(TypedDict):
    """Estructura de datos del estudiante."""

    nombre: str
    fecha_inicio: str
    examenes: dict[str, ResultadoExamen]
    xp_total: int
    nivel: int
    logros: list[str]


# Configuración de módulos
MODULOS = {
    1: "Fundamentos de Python y Estadística",
    2: "SQL",
    3: "ETL con Python",
    4: "APIs y Web Scraping",
    5: "Bases de Datos Avanzadas",
    6: "Apache Airflow",
    7: "Cloud (AWS/GCP)",
    8: "Data Warehousing",
    9: "Spark y Big Data",
    10: "ML para Data Engineers / MLOps",
}

NOTA_APROBADO = 70.0
XP_POR_MODULO = 100
XP_BONUS_EXCELENCIA = 50  # Si nota >= 90


def calcular_nivel(xp: int) -> int:
    """
    Calcula el nivel basado en XP total.

    Args:
        xp: Puntos de experiencia totales

    Returns:
        Nivel del estudiante (1-10)
    """
    if xp < 100:
        return 1
    elif xp < 300:
        return 2
    elif xp < 600:
        return 3
    elif xp < 1000:
        return 4
    elif xp < 1500:
        return 5
    elif xp < 2100:
        return 6
    elif xp < 2800:
        return 7
    elif xp < 3600:
        return 8
    elif xp < 4500:
        return 9
    else:
        return 10


def cargar_progreso(
    nombre_estudiante: str, directorio: Path | None = None
) -> DatosEstudiante:
    """
    Carga el progreso de un estudiante desde archivo JSON.

    Args:
        nombre_estudiante: Nombre del estudiante
        directorio: Directorio donde buscar el archivo

    Returns:
        Datos del estudiante cargados o nuevos
    """
    if directorio is None:
        directorio = Path(__file__).parent / "progreso"

    directorio.mkdir(parents=True, exist_ok=True)

    nombre_archivo = nombre_estudiante.lower().replace(" ", "_")
    nombre_archivo = "".join(c for c in nombre_archivo if c.isalnum() or c == "_")
    ruta_archivo = directorio / f"{nombre_archivo}.json"

    if ruta_archivo.exists():
        with open(ruta_archivo, encoding="utf-8") as f:
            return json.load(f)

    # Crear nuevo registro
    return {
        "nombre": nombre_estudiante,
        "fecha_inicio": datetime.now().isoformat(),
        "examenes": {},
        "xp_total": 0,
        "nivel": 1,
        "logros": [],
    }


def guardar_progreso(datos: DatosEstudiante, directorio: Path | None = None) -> str:
    """
    Guarda el progreso del estudiante en archivo JSON.

    Args:
        datos: Datos del estudiante a guardar
        directorio: Directorio donde guardar

    Returns:
        Ruta del archivo guardado
    """
    if directorio is None:
        directorio = Path(__file__).parent / "progreso"

    directorio.mkdir(parents=True, exist_ok=True)

    nombre_archivo = datos["nombre"].lower().replace(" ", "_")
    nombre_archivo = "".join(c for c in nombre_archivo if c.isalnum() or c == "_")
    ruta_archivo = directorio / f"{nombre_archivo}.json"

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

    return str(ruta_archivo)


def registrar_examen(
    datos: DatosEstudiante, modulo: int, puntuacion: float
) -> tuple[DatosEstudiante, list[str]]:
    """
    Registra el resultado de un examen.

    Args:
        datos: Datos actuales del estudiante
        modulo: Número del módulo (1-10)
        puntuacion: Puntuación obtenida (0-100)

    Returns:
        Tupla con datos actualizados y lista de nuevos logros

    Raises:
        ValueError: Si el módulo o puntuación son inválidos
    """
    if modulo not in MODULOS:
        raise ValueError(f"Módulo inválido: {modulo}. Debe ser 1-10")

    if not 0 <= puntuacion <= 100:
        raise ValueError(f"Puntuación inválida: {puntuacion}. Debe ser 0-100")

    modulo_key = str(modulo)
    aprobado = puntuacion >= NOTA_APROBADO
    nuevos_logros: list[str] = []

    # Actualizar o crear resultado
    intentos = 1
    if modulo_key in datos["examenes"]:
        intentos = datos["examenes"][modulo_key]["intentos"] + 1

    datos["examenes"][modulo_key] = {
        "modulo": modulo,
        "puntuacion": puntuacion,
        "fecha": datetime.now().isoformat(),
        "aprobado": aprobado,
        "intentos": intentos,
    }

    # Calcular XP
    if aprobado:
        xp_ganado = XP_POR_MODULO
        if puntuacion >= 90:
            xp_ganado += XP_BONUS_EXCELENCIA
            if f"excelencia_m{modulo}" not in datos["logros"]:
                datos["logros"].append(f"excelencia_m{modulo}")
                nuevos_logros.append(f"🌟 Excelencia en {MODULOS[modulo]}")

        # Solo dar XP si es primera vez que aprueba
        if intentos == 1 or (
            intentos > 1
            and not datos["examenes"].get(modulo_key, {}).get("aprobado", False)
        ):
            datos["xp_total"] += xp_ganado

    # Actualizar nivel
    nuevo_nivel = calcular_nivel(datos["xp_total"])
    if nuevo_nivel > datos["nivel"]:
        datos["nivel"] = nuevo_nivel
        nuevos_logros.append(f"🎯 ¡Nivel {nuevo_nivel} alcanzado!")

    # Verificar logros especiales
    modulos_aprobados = sum(1 for e in datos["examenes"].values() if e["aprobado"])

    if modulos_aprobados == 5 and "mitad_programa" not in datos["logros"]:
        datos["logros"].append("mitad_programa")
        nuevos_logros.append("🏆 ¡Mitad del programa completado!")

    if modulos_aprobados == 10 and "programa_completo" not in datos["logros"]:
        datos["logros"].append("programa_completo")
        nuevos_logros.append("🎓 ¡PROGRAMA COMPLETADO!")

    # Logro por aprobar a la primera
    if aprobado and intentos == 1:
        if f"primera_m{modulo}" not in datos["logros"]:
            datos["logros"].append(f"primera_m{modulo}")
            nuevos_logros.append(f"⚡ Aprobado a la primera: {MODULOS[modulo]}")

    return datos, nuevos_logros


def calcular_nota_media(datos: DatosEstudiante) -> float:
    """
    Calcula la nota media de los exámenes aprobados.

    Args:
        datos: Datos del estudiante

    Returns:
        Nota media sobre 10 (0 si no hay exámenes aprobados)
    """
    examenes_aprobados = [
        e["puntuacion"] for e in datos["examenes"].values() if e["aprobado"]
    ]

    if not examenes_aprobados:
        return 0.0

    # Convertir de 0-100 a 0-10
    return sum(examenes_aprobados) / len(examenes_aprobados) / 10


def generar_dashboard(datos: DatosEstudiante) -> str:
    """
    Genera un dashboard visual del progreso en formato texto.

    Args:
        datos: Datos del estudiante

    Returns:
        String con el dashboard formateado
    """
    linea = "═" * 60

    dashboard = f"""
╔{linea}╗
║{"DASHBOARD DE PROGRESO":^60}║
║{datos["nombre"]:^60}║
╠{linea}╣
"""

    # Estadísticas generales
    modulos_aprobados = sum(1 for e in datos["examenes"].values() if e["aprobado"])
    porcentaje_completado = (modulos_aprobados / 10) * 100
    nota_media = calcular_nota_media(datos)

    # Barra de progreso
    progreso_lleno = int(porcentaje_completado / 5)
    barra = "█" * progreso_lleno + "░" * (20 - progreso_lleno)

    dashboard += f"""║ Nivel: {datos["nivel"]:>2} │ XP: {datos["xp_total"]:>4} │ Progreso: {porcentaje_completado:>5.1f}%     ║
║ [{barra}] {modulos_aprobados}/10 módulos      ║
║ Nota Media: {nota_media:.2f}/10                                      ║
╠{linea}╣
║{"MÓDULOS":^60}║
╠{linea}╣
"""

    # Estado de cada módulo
    for num, nombre in MODULOS.items():
        modulo_key = str(num)
        if modulo_key in datos["examenes"]:
            examen = datos["examenes"][modulo_key]
            if examen["aprobado"]:
                estado = f"✅ {examen['puntuacion']:.0f}%"
            else:
                estado = f"❌ {examen['puntuacion']:.0f}%"
        else:
            estado = "⬚ Pendiente"

        nombre_corto = nombre[:35] + "..." if len(nombre) > 35 else nombre
        dashboard += f"║ {num:>2}. {nombre_corto:<38} {estado:>12} ║\n"

    dashboard += f"""╠{linea}╣
║{"LOGROS":^60}║
╠{linea}╣
"""

    # Logros
    logros_mostrar = [
        item
        for item in datos["logros"]
        if not item.startswith("excelencia_m") and not item.startswith("primera_m")
    ]

    if logros_mostrar:
        for logro in logros_mostrar[:5]:  # Mostrar máximo 5
            logro_texto = {
                "mitad_programa": "🏆 Mitad del programa completado",
                "programa_completo": "🎓 Programa completado",
            }.get(logro, logro)
            dashboard += f"║ {logro_texto:<58} ║\n"
    else:
        dashboard += f"║ {'(Sin logros especiales aún)':<58} ║\n"

    # Contar logros de excelencia y primera vez
    excelencias = sum(1 for item in datos["logros"] if item.startswith("excelencia_m"))
    primeras = sum(1 for item in datos["logros"] if item.startswith("primera_m"))

    if excelencias > 0 or primeras > 0:
        dashboard += (
            f"║ 🌟 Excelencias: {excelencias} │ ⚡ A la primera: {primeras:<19} ║\n"
        )

    dashboard += f"""╚{linea}╝
"""

    return dashboard


def puede_obtener_certificado(datos: DatosEstudiante) -> tuple[bool, str]:
    """
    Verifica si el estudiante puede obtener el certificado.

    Args:
        datos: Datos del estudiante

    Returns:
        Tupla (puede_obtener, mensaje)
    """
    modulos_aprobados = sum(1 for e in datos["examenes"].values() if e["aprobado"])

    if modulos_aprobados < 10:
        modulos_faltantes = 10 - modulos_aprobados
        return False, f"Faltan {modulos_faltantes} módulos por aprobar"

    nota_media = calcular_nota_media(datos)
    if nota_media < 7.0:
        return False, f"Nota media ({nota_media:.2f}) inferior al mínimo (7.0)"

    return True, "¡Felicidades! Puedes obtener tu certificado"


def main():
    """Función principal para uso interactivo."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Sistema de tracking de progreso para el Master"
    )
    parser.add_argument("--nombre", required=True, help="Nombre del estudiante")
    parser.add_argument(
        "--registrar",
        nargs=2,
        metavar=("MODULO", "PUNTUACION"),
        help="Registrar resultado de examen",
    )
    parser.add_argument(
        "--dashboard", action="store_true", help="Mostrar dashboard de progreso"
    )
    parser.add_argument(
        "--certificado",
        action="store_true",
        help="Verificar si puede obtener certificado",
    )

    args = parser.parse_args()

    # Cargar datos
    datos = cargar_progreso(args.nombre)

    # Registrar examen
    if args.registrar:
        modulo = int(args.registrar[0])
        puntuacion = float(args.registrar[1])
        datos, nuevos_logros = registrar_examen(datos, modulo, puntuacion)
        guardar_progreso(datos)

        if puntuacion >= NOTA_APROBADO:
            print(f"✅ Examen del Módulo {modulo} aprobado con {puntuacion}%")
        else:
            print(f"❌ Examen del Módulo {modulo} no aprobado ({puntuacion}%)")
            print(f"   Se requiere mínimo {NOTA_APROBADO}%")

        for logro in nuevos_logros:
            print(f"   {logro}")

    # Mostrar dashboard
    if args.dashboard or not args.registrar:
        print(generar_dashboard(datos))

    # Verificar certificado
    if args.certificado:
        puede, mensaje = puede_obtener_certificado(datos)
        if puede:
            print(f"✅ {mensaje}")
            nota_media = calcular_nota_media(datos)
            print(f"   Nota media: {nota_media:.2f}/10")
            print("\n   Genera tu certificado con:")
            print(
                f'   python generar_certificado.py --nombre "{datos["nombre"]}" --nota {nota_media:.2f}'
            )
        else:
            print(f"❌ {mensaje}")


if __name__ == "__main__":
    main()

"""
Interface de línea de comandos (CLI) para ejecutar el pipeline.
"""

import sys
from pathlib import Path

import click
from sqlalchemy import create_engine

from src.pipeline import ejecutar_pipeline_completo


@click.command()
@click.option(
    "--num-noticias", default=100, help="Número de noticias a generar", type=int
)
@click.option(
    "--db-url",
    default="sqlite:///noticias.db",
    help="URL de conexión a base de datos",
    type=str,
)
@click.option(
    "--output-dir",
    default="data",
    help="Directorio de salida para datos",
    type=click.Path(),
)
@click.option(
    "--guardar-intermedios/--no-guardar-intermedios",
    default=True,
    help="Guardar datos intermedios (Bronze, Silver)",
)
def main(num_noticias: int, db_url: str, output_dir: str, guardar_intermedios: bool):
    """
    Pipeline de análisis de noticias con arquitectura Bronze/Silver/Gold.

    Extrae noticias simuladas, las transforma, valida calidad y carga
    en Parquet y base de datos.

    Ejemplos:

        # Ejecutar con configuración por defecto
        python -m src.cli

        # Generar 500 noticias
        python -m src.cli --num-noticias 500

        # Usar PostgreSQL
        python -m src.cli --db-url postgresql://user:pass@localhost/dbname
    """
    click.echo("=" * 60)
    click.echo("Pipeline de Análisis de Noticias")
    click.echo("=" * 60)
    click.echo(f"Noticias: {num_noticias}")
    click.echo(f"Base de datos: {db_url}")
    click.echo(f"Directorio salida: {output_dir}")
    click.echo("=" * 60)

    try:
        # Crear engine
        engine = create_engine(db_url)
        directorio = Path(output_dir)

        # Ejecutar pipeline
        click.echo("\n▶ Ejecutando pipeline...")
        resultado = ejecutar_pipeline_completo(
            num_noticias=num_noticias,
            engine=engine,
            directorio_salida=directorio,
            guardar_intermedios=guardar_intermedios,
        )

        # Mostrar resultados
        if resultado["exito"]:
            click.echo("\n✅ Pipeline completado exitosamente\n")
            click.echo("📊 Métricas:")
            click.echo(f"  - Registros extraídos: {resultado['registros_extraidos']}")
            click.echo(f"  - Registros Silver: {resultado['registros_silver']}")
            click.echo(f"  - Registros Gold: {resultado['registros_gold']}")

            if "calidad" in resultado:
                click.echo("\n🔍 Calidad de datos:")
                calidad = resultado["calidad"]
                click.echo(
                    f"  - Esquema válido: {'✅' if calidad['esquema_valido'] else '❌'}"
                )
                click.echo(f"  - Duplicados: {calidad['duplicados']['total']}")

            click.echo(f"\n📁 Datos guardados en: {output_dir}")
            sys.exit(0)
        else:
            click.echo(f"\n❌ Error en pipeline: {resultado.get('error', 'Unknown')}")
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Módulo de conexión y operaciones de base de datos para Data Warehouse.

Este módulo provee la clase DatabaseConnection para conectar a SQLite
y realizar operaciones de carga y consulta del Data Warehouse.

Clases:
    DatabaseConnection: Maneja conexión y operaciones de BD (context manager)
"""

import sqlite3
from pathlib import Path

import pandas as pd


class DatabaseConnection:
    """
    Maneja conexión a base de datos SQLite con soporte para context manager.

    Características:
    - Context manager para manejo automático de conexión
    - Carga de schema desde archivo SQL
    - Inserción de datos desde DataFrames
    - Ejecución de queries con retorno de DataFrames
    - Transacciones automáticas

    Examples:
        >>> with DatabaseConnection("dwh.db") as db:
        ...     db.crear_tablas()
        ...     db.cargar_dimension("DimFecha", df_fecha)
        ...     resultado = db.ejecutar_query("SELECT * FROM DimFecha")
    """

    def __init__(self, db_path: str = ":memory:"):
        """
        Inicializa conexión a base de datos.

        Args:
            db_path: Ruta al archivo de BD o ":memory:" para BD en memoria
        """
        self.db_path = db_path
        self.connection: sqlite3.Connection | None = None

    def __enter__(self):
        """Abre conexión cuando se entra al context manager."""
        self.connection = sqlite3.connect(self.db_path)
        # Habilitar claves foráneas en SQLite
        self.connection.execute("PRAGMA foreign_keys = ON")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra conexión cuando se sale del context manager."""
        if self.connection:
            if exc_type is None:
                # No hubo error, hacer commit
                self.connection.commit()
            else:
                # Hubo error, hacer rollback
                self.connection.rollback()

            self.connection.close()
            self.connection = None

        # No suprimir excepciones
        return False

    def crear_tablas(self, schema_path: str = "schema.sql") -> None:
        """
        Crea tablas del Data Warehouse desde archivo SQL.

        Args:
            schema_path: Ruta al archivo SQL con el schema

        Raises:
            FileNotFoundError: Si no existe el archivo schema.sql
            sqlite3.Error: Si hay error ejecutando el SQL

        Examples:
            >>> with DatabaseConnection(":memory:") as db:
            ...     db.crear_tablas()  # Usa schema.sql por defecto
            ...     db.crear_tablas("custom_schema.sql")
        """
        if not self.connection:
            raise RuntimeError("No hay conexión activa. Use context manager.")

        # Buscar schema.sql en directorio actual o en raíz del proyecto
        schema_file = Path(schema_path)

        if not schema_file.exists():
            # Intentar buscar en el directorio del módulo
            module_dir = Path(__file__).parent.parent
            schema_file = module_dir / schema_path

        if not schema_file.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {schema_path}")

        # Leer y ejecutar el schema SQL
        with open(schema_file, encoding="utf-8") as f:
            schema_sql = f.read()

        # Ejecutar cada statement del schema
        self.connection.executescript(schema_sql)
        self.connection.commit()

    def cargar_dimension(self, tabla: str, df: pd.DataFrame) -> int:
        """
        Carga datos de un DataFrame a una tabla de dimensión.

        Args:
            tabla: Nombre de la tabla de dimensión
            df: DataFrame con los datos a cargar

        Returns:
            Número de registros insertados

        Examples:
            >>> df_fecha = pd.DataFrame([...])
            >>> with DatabaseConnection(":memory:") as db:
            ...     db.crear_tablas()
            ...     registros = db.cargar_dimension("DimFecha", df_fecha)
            ...     print(f"Insertados: {registros}")
        """
        if not self.connection:
            raise RuntimeError("No hay conexión activa. Use context manager.")

        if df.empty:
            return 0

        # Usar to_sql de pandas para insertar
        df.to_sql(
            tabla,
            self.connection,
            if_exists="append",  # Agregar a tabla existente
            index=False,  # No insertar el índice de pandas
        )

        self.connection.commit()

        # to_sql retorna None, así que contamos manualmente
        return len(df)

    def cargar_fact(self, tabla: str, df: pd.DataFrame) -> int:
        """
        Carga datos de un DataFrame a una tabla de hechos.

        Args:
            tabla: Nombre de la tabla de hechos
            df: DataFrame con los datos a cargar

        Returns:
            Número de registros insertados

        Examples:
            >>> df_ventas = pd.DataFrame([...])
            >>> with DatabaseConnection(":memory:") as db:
            ...     db.crear_tablas()
            ...     registros = db.cargar_fact("FactVentas", df_ventas)
            ...     print(f"Insertados: {registros}")
        """
        # La lógica es idéntica a cargar_dimension
        # Se mantiene como función separada por claridad semántica
        return self.cargar_dimension(tabla, df)

    def ejecutar_query(self, query: str, params: tuple | None = None) -> pd.DataFrame:
        """
        Ejecuta un query SQL y retorna resultado como DataFrame.

        Args:
            query: Query SQL a ejecutar (SELECT)
            params: Parámetros para query parametrizado (opcional)

        Returns:
            DataFrame con los resultados del query

        Raises:
            sqlite3.Error: Si hay error ejecutando el query

        Examples:
            >>> with DatabaseConnection(":memory:") as db:
            ...     db.crear_tablas()
            ...     resultado = db.ejecutar_query("SELECT * FROM DimFecha")
            ...     print(resultado.shape)

            >>> # Query de agregación
            >>> resultado = db.ejecutar_query('''
            ...     SELECT categoria, COUNT(*) as total
            ...     FROM DimProducto
            ...     GROUP BY categoria
            ... ''')

            >>> # Query parametrizado
            >>> resultado = db.ejecutar_query(
            ...     "SELECT * FROM DimFecha WHERE anio = ?",
            ...     params=(2024,)
            ... )
        """
        if not self.connection:
            raise RuntimeError("No hay conexión activa. Use context manager.")

        # Usar read_sql_query de pandas para ejecutar y retornar DataFrame
        df_resultado = pd.read_sql_query(query, self.connection, params=params)

        return df_resultado

    def ejecutar_comando(self, comando: str) -> None:
        """
        Ejecuta un comando SQL que no retorna resultados (INSERT, UPDATE, DELETE).

        Args:
            comando: Comando SQL a ejecutar

        Raises:
            sqlite3.Error: Si hay error ejecutando el comando

        Examples:
            >>> with DatabaseConnection(":memory:") as db:
            ...     db.crear_tablas()
            ...     db.ejecutar_comando("DELETE FROM DimFecha WHERE anio < 2020")
        """
        if not self.connection:
            raise RuntimeError("No hay conexión activa. Use context manager.")

        cursor = self.connection.cursor()
        cursor.execute(comando)
        self.connection.commit()

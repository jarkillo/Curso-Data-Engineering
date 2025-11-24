"""
Módulo de conexión a base de datos SQLite.

Este módulo contiene la clase ConexionSQLite que gestiona
la conexión a bases de datos SQLite de forma segura.
"""

import sqlite3
from typing import Any


class ConexionSQLite:
    """
    Gestiona conexión a base de datos SQLite.

    Esta es una excepción válida a la regla de "no usar clases"
    porque maneja un recurso externo (conexión a base de datos)
    e implementa context manager.

    Attributes:
        conexion: Conexión a la base de datos SQLite

    Examples:
        >>> # Uso básico
        >>> conn = ConexionSQLite("techstore.db")
        >>> resultados = conn.ejecutar_query("SELECT * FROM productos")
        >>> conn.cerrar()

        >>> # Uso con context manager (recomendado)
        >>> with ConexionSQLite("techstore.db") as conn:
        ...     resultados = conn.ejecutar_query("SELECT * FROM productos")
    """

    def __init__(self, ruta_db: str) -> None:
        """
        Inicializa la conexión a la base de datos.

        Args:
            ruta_db: Ruta al archivo .db o ":memory:" para DB en memoria

        Raises:
            sqlite3.Error: Si hay error al conectar a la base de datos
        """
        self.conexion = sqlite3.connect(ruta_db)
        # Configurar para retornar diccionarios en lugar de tuplas
        self.conexion.row_factory = sqlite3.Row

    def ejecutar_query(
        self, query: str, parametros: tuple[Any, ...] = ()
    ) -> list[dict]:
        """
        Ejecuta una query SQL y retorna los resultados como lista de diccionarios.

        Esta función usa parámetros para prevenir SQL injection.

        Args:
            query: Query SQL a ejecutar (usar ? para parámetros)
            parametros: Tupla de parámetros para la query

        Returns:
            Lista de diccionarios con los resultados
            (lista vacía si no hay resultados)

        Raises:
            sqlite3.Error: Si hay error al ejecutar la query

        Examples:
            >>> conn = ConexionSQLite(":memory:")
            >>> # Query sin parámetros
            >>> resultados = conn.ejecutar_query("SELECT * FROM productos")
            >>> # Query con parámetros (previene SQL injection)
            >>> resultados = conn.ejecutar_query(
            ...     "SELECT * FROM productos WHERE categoria = ?",
            ...     ("Accesorios",)
            ... )
        """
        cursor = self.conexion.cursor()
        cursor.execute(query, parametros)

        # Convertir resultados a lista de diccionarios
        columnas = (
            [descripcion[0] for descripcion in cursor.description]
            if cursor.description
            else []
        )
        resultados = []

        for fila in cursor.fetchall():
            # sqlite3.Row se puede convertir a dict
            resultado_dict = dict(zip(columnas, fila, strict=False))
            resultados.append(resultado_dict)

        return resultados

    def cerrar(self) -> None:
        """
        Cierra la conexión a la base de datos.

        Es seguro llamar este método múltiples veces.

        Examples:
            >>> conn = ConexionSQLite(":memory:")
            >>> conn.cerrar()
            >>> conn.cerrar()  # No lanza error
        """
        if self.conexion:
            try:
                self.conexion.close()
            except sqlite3.ProgrammingError:
                # La conexión ya estaba cerrada
                pass

    def __enter__(self):
        """
        Implementa context manager (entrada del with).

        Returns:
            self: La instancia de ConexionSQLite

        Examples:
            >>> with ConexionSQLite(":memory:") as conn:
            ...     resultados = conn.ejecutar_query("SELECT 1")
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Implementa context manager (salida del with).

        Cierra la conexión automáticamente al salir del bloque with.

        Args:
            exc_type: Tipo de excepción (si hubo)
            exc_val: Valor de excepción (si hubo)
            exc_tb: Traceback de excepción (si hubo)
        """
        self.cerrar()

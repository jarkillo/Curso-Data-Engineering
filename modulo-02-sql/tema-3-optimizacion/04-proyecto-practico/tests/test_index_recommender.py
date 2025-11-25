"""
Tests para index_recommender.py

Siguiendo TDD: Tests escritos ANTES de la implementación.
"""

from src.index_recommender import (
    calcular_prioridad_indice,
    generar_sql_create_index,
    recomendar_indices,
)


class TestRecomendarIndices:
    """Tests para recomendar_indices()."""

    def test_recomienda_indice_para_where_simple(self):
        """Debe recomendar índice en columna de WHERE."""
        query = "SELECT * FROM usuarios WHERE email = 'test@example.com'"
        recomendaciones = recomendar_indices(query)

        assert len(recomendaciones) > 0
        assert any(r["columna"] == "email" for r in recomendaciones)
        assert recomendaciones[0]["tabla"] == "usuarios"

    def test_recomienda_indices_para_join(self):
        """Debe recomendar índices en columnas de JOIN."""
        query = "SELECT * FROM usuarios u JOIN pedidos p ON u.id = p.usuario_id"
        recomendaciones = recomendar_indices(query)

        assert len(recomendaciones) >= 1
        # Debe recomendar índice en usuario_id (foreign key)
        assert any("usuario_id" in r["columna"] for r in recomendaciones)

    def test_recomienda_indice_compuesto_para_where_multiple(self):
        """Debe recomendar índice compuesto para múltiples columnas en WHERE."""
        query = "SELECT * FROM ventas WHERE fecha >= '2024-01-01' AND tienda_id = 5"
        recomendaciones = recomendar_indices(query)

        # Debe haber recomendación de índice compuesto
        assert len(recomendaciones) > 0
        compuesto = [r for r in recomendaciones if "," in r["columna"]]
        assert len(compuesto) > 0

    def test_no_recomienda_para_select_asterisco_sin_filtros(self):
        """No debe recomendar índices para SELECT * sin WHERE."""
        query = "SELECT * FROM usuarios"
        recomendaciones = recomendar_indices(query)

        assert len(recomendaciones) == 0

    def test_prioriza_indices_por_selectividad(self):
        """Debe priorizar recomendaciones por selectividad."""
        query = "SELECT * FROM usuarios WHERE id = 1 AND nombre = 'Juan'"
        recomendaciones = recomendar_indices(query)

        # id (probablemente PK) debe tener mayor prioridad que nombre
        if len(recomendaciones) >= 2:
            assert recomendaciones[0]["prioridad"] >= recomendaciones[1]["prioridad"]


class TestGenerarSqlCreateIndex:
    """Tests para generar_sql_create_index()."""

    def test_genera_sql_indice_simple(self):
        """Debe generar SQL para índice simple."""
        sql = generar_sql_create_index("usuarios", "email")
        assert "CREATE INDEX" in sql
        assert "usuarios" in sql
        assert "email" in sql
        assert sql.startswith("CREATE INDEX")

    def test_genera_sql_indice_compuesto(self):
        """Debe generar SQL para índice compuesto."""
        sql = generar_sql_create_index("ventas", "fecha, tienda_id")
        assert "CREATE INDEX" in sql
        assert "ventas" in sql
        assert "fecha" in sql
        assert "tienda_id" in sql

    def test_nombre_indice_es_descriptivo(self):
        """El nombre del índice debe ser descriptivo."""
        sql = generar_sql_create_index("usuarios", "email")
        # Debe contener idx_ + tabla + columna
        assert "idx_usuarios" in sql

    def test_sql_termina_con_punto_y_coma(self):
        """El SQL generado debe terminar con ;"""
        sql = generar_sql_create_index("productos", "categoria")
        assert sql.endswith(";")


class TestCalcularPrioridadIndice:
    """Tests para calcular_prioridad_indice()."""

    def test_columna_en_where_tiene_prioridad_alta(self):
        """Columnas en WHERE deben tener prioridad alta."""
        prioridad = calcular_prioridad_indice(
            columna="email", en_where=True, en_join=False, en_order_by=False
        )
        assert prioridad >= 80

    def test_columna_en_join_tiene_prioridad_alta(self):
        """Columnas en JOIN deben tener prioridad alta."""
        prioridad = calcular_prioridad_indice(
            columna="usuario_id", en_where=False, en_join=True, en_order_by=False
        )
        assert prioridad >= 70

    def test_columna_en_order_by_tiene_prioridad_media(self):
        """Columnas solo en ORDER BY deben tener prioridad media."""
        prioridad = calcular_prioridad_indice(
            columna="fecha", en_where=False, en_join=False, en_order_by=True
        )
        assert 40 <= prioridad < 70

    def test_columna_en_where_y_join_tiene_maxima_prioridad(self):
        """Columna en WHERE y JOIN debe tener máxima prioridad."""
        prioridad = calcular_prioridad_indice(
            columna="id", en_where=True, en_join=True, en_order_by=False
        )
        assert prioridad >= 90

    def test_columna_sin_uso_tiene_prioridad_cero(self):
        """Columna que no se usa en WHERE/JOIN/ORDER BY debe tener prioridad 0."""
        prioridad = calcular_prioridad_indice(
            columna="descripcion", en_where=False, en_join=False, en_order_by=False
        )
        assert prioridad == 0

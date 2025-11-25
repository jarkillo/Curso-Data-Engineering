"""
Tests para el módulo gestor de extracciones.

Tests exhaustivos para gestor_extracciones.py con mocking extensivo.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.gestor_extracciones import (
    extraer_desde_fuente,
    generar_reporte_extraccion,
    guardar_resultados,
    orquestar_extraccion_multiple,
    pipeline_completo,
)


class TestExtraerDesdeFuente:
    """Tests para extraer_desde_fuente."""

    @patch("src.gestor_extracciones.leer_csv_con_encoding_auto")
    def test_extrae_csv(self, mock_leer_csv):
        """Debe extraer datos de CSV correctamente."""
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]})
        mock_leer_csv.return_value = mock_df

        config = {"ruta": "datos.csv", "kwargs": {"delimiter": ";"}}
        resultado = extraer_desde_fuente("csv", config)

        assert resultado.equals(mock_df)
        mock_leer_csv.assert_called_once_with("datos.csv", delimiter=";")

    @patch("src.gestor_extracciones.leer_json_nested")
    def test_extrae_json(self, mock_leer_json):
        """Debe extraer datos de JSON correctamente."""
        mock_df = pd.DataFrame({"id": [1, 2], "nombre": ["Ana", "Luis"]})
        mock_leer_json.return_value = mock_df

        config = {"ruta": "datos.json"}
        resultado = extraer_desde_fuente("json", config)

        assert resultado.equals(mock_df)
        mock_leer_json.assert_called_once()

    @patch("src.gestor_extracciones.leer_excel_multiple_sheets")
    def test_extrae_excel_con_combinar_true(self, mock_leer_excel):
        """Debe extraer Excel y retornar DataFrame combinado."""
        mock_df = pd.DataFrame({"datos": [1, 2, 3]})
        mock_leer_excel.return_value = mock_df

        config = {"ruta": "datos.xlsx", "combinar": True}
        resultado = extraer_desde_fuente("excel", config)

        assert resultado.equals(mock_df)

    @patch("src.gestor_extracciones.leer_excel_multiple_sheets")
    def test_extrae_excel_con_dict_de_sheets(self, mock_leer_excel):
        """Debe combinar sheets cuando retorna dict."""
        mock_sheets = {
            "Sheet1": pd.DataFrame({"col": [1, 2]}),
            "Sheet2": pd.DataFrame({"col": [3, 4]}),
        }
        mock_leer_excel.return_value = mock_sheets

        config = {"ruta": "datos.xlsx", "combinar": False}
        resultado = extraer_desde_fuente("excel", config)

        # Debe concatenar los DataFrames del dict
        assert len(resultado) == 4  # 2 + 2 filas

    @patch("src.gestor_extracciones.extraer_api_completa")
    def test_extrae_api(self, mock_extraer_api):
        """Debe extraer datos de API correctamente."""
        mock_datos = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
        mock_extraer_api.return_value = mock_datos

        config = {"url": "https://api.ejemplo.com/usuarios"}
        resultado = extraer_desde_fuente("api", config)

        assert len(resultado) == 2
        assert "id" in resultado.columns
        mock_extraer_api.assert_called_once()

    @patch("src.gestor_extracciones.extraer_html")
    @patch("src.gestor_extracciones.parsear_con_beautifulsoup")
    @patch("src.gestor_extracciones.extraer_tabla_html")
    def test_extrae_web(self, mock_tabla, mock_parsear, mock_html):
        """Debe extraer datos web correctamente."""
        mock_html.return_value = "<html><table><tr><td>Datos</td></tr></table></html>"
        mock_soup = MagicMock()
        mock_parsear.return_value = mock_soup
        mock_tabla.return_value = [{"col": "Datos"}]

        config = {"url": "https://ejemplo.com/datos", "selector": "#tabla1"}
        resultado = extraer_desde_fuente("web", config)

        assert len(resultado) == 1
        mock_html.assert_called_once()
        mock_parsear.assert_called_once()
        mock_tabla.assert_called_once_with(mock_soup, "#tabla1")

    def test_csv_sin_ruta_lanza_error(self):
        """CSV sin ruta debe lanzar ValueError."""
        config = {}

        with pytest.raises(ValueError, match="requiere 'ruta'"):
            extraer_desde_fuente("csv", config)

    def test_json_sin_ruta_lanza_error(self):
        """JSON sin ruta debe lanzar ValueError."""
        config = {}

        with pytest.raises(ValueError, match="requiere 'ruta'"):
            extraer_desde_fuente("json", config)

    def test_api_sin_url_lanza_error(self):
        """API sin URL debe lanzar ValueError."""
        config = {}

        with pytest.raises(ValueError, match="requiere 'url'"):
            extraer_desde_fuente("api", config)

    def test_tipo_fuente_invalido_lanza_error(self):
        """Tipo de fuente no soportado debe lanzar ValueError."""
        config = {"ruta": "datos.txt"}

        with pytest.raises(ValueError, match="no soportado"):
            extraer_desde_fuente("txt", config)


class TestOrquestarExtraccionMultiple:
    """Tests para orquestar_extraccion_multiple."""

    @patch("src.gestor_extracciones.extraer_desde_fuente")
    def test_extrae_multiples_fuentes(self, mock_extraer):
        """Debe extraer de múltiples fuentes correctamente."""
        mock_df1 = pd.DataFrame({"col": [1, 2]})
        mock_df2 = pd.DataFrame({"col": [3, 4]})
        mock_extraer.side_effect = [mock_df1, mock_df2]

        fuentes = [
            {"tipo": "csv", "nombre": "ventas", "config": {"ruta": "ventas.csv"}},
            {"tipo": "json", "nombre": "usuarios", "config": {"ruta": "usuarios.json"}},
        ]

        resultados = orquestar_extraccion_multiple(fuentes, combinar=False)

        assert isinstance(resultados, dict)
        assert "ventas" in resultados
        assert "usuarios" in resultados
        assert len(resultados["ventas"]) == 2
        assert len(resultados["usuarios"]) == 2

    @patch("src.gestor_extracciones.extraer_desde_fuente")
    def test_combinar_dataframes(self, mock_extraer):
        """Cuando combinar=True, debe retornar DataFrame único."""
        mock_df1 = pd.DataFrame({"col": [1, 2]})
        mock_df2 = pd.DataFrame({"col": [3, 4]})
        mock_extraer.side_effect = [mock_df1, mock_df2]

        fuentes = [
            {"tipo": "csv", "nombre": "f1", "config": {"ruta": "f1.csv"}},
            {"tipo": "csv", "nombre": "f2", "config": {"ruta": "f2.csv"}},
        ]

        resultado = orquestar_extraccion_multiple(fuentes, combinar=True)

        assert isinstance(resultado, pd.DataFrame)
        assert len(resultado) == 4  # 2 + 2 filas

    @patch("src.gestor_extracciones.extraer_desde_fuente")
    def test_maneja_error_en_fuente(self, mock_extraer):
        """Debe manejar error en una fuente y continuar con las demás."""
        mock_df = pd.DataFrame({"col": [1, 2]})
        mock_extraer.side_effect = [Exception("Error de red"), mock_df]

        fuentes = [
            {"tipo": "api", "nombre": "api1", "config": {"url": "https://error.com"}},
            {"tipo": "csv", "nombre": "csv1", "config": {"ruta": "datos.csv"}},
        ]

        resultados = orquestar_extraccion_multiple(fuentes, combinar=False)

        assert "api1" in resultados
        assert "csv1" in resultados
        assert resultados["api1"].empty  # DataFrame vacío por error
        assert not resultados["csv1"].empty

    @patch("src.gestor_extracciones.extraer_desde_fuente")
    def test_nombre_por_defecto_si_no_especificado(self, mock_extraer):
        """Debe asignar nombre por defecto si no se especifica."""
        mock_df = pd.DataFrame({"col": [1]})
        mock_extraer.return_value = mock_df

        fuentes = [{"tipo": "csv", "config": {"ruta": "datos.csv"}}]  # Sin nombre

        resultados = orquestar_extraccion_multiple(fuentes, combinar=False)

        assert "fuente_0" in resultados

    @patch("src.gestor_extracciones.extraer_desde_fuente")
    def test_combinar_con_dataframes_vacios_los_omite(self, mock_extraer):
        """Al combinar, debe omitir DataFrames vacíos."""
        mock_df_vacio = pd.DataFrame()
        mock_df_valido = pd.DataFrame({"col": [1, 2]})
        mock_extraer.side_effect = [mock_df_vacio, mock_df_valido]

        fuentes = [
            {"tipo": "csv", "nombre": "f1", "config": {"ruta": "f1.csv"}},
            {"tipo": "csv", "nombre": "f2", "config": {"ruta": "f2.csv"}},
        ]

        resultado = orquestar_extraccion_multiple(fuentes, combinar=True)

        assert len(resultado) == 2  # Solo el válido

    @patch("src.gestor_extracciones.extraer_desde_fuente")
    def test_combinar_sin_dataframes_validos_retorna_vacio(self, mock_extraer):
        """Si no hay DataFrames válidos, debe retornar DataFrame vacío."""
        mock_extraer.return_value = pd.DataFrame()

        fuentes = [{"tipo": "csv", "nombre": "f1", "config": {"ruta": "f1.csv"}}]

        resultado = orquestar_extraccion_multiple(fuentes, combinar=True)

        assert isinstance(resultado, pd.DataFrame)
        assert resultado.empty


class TestGenerarReporteExtraccion:
    """Tests para generar_reporte_extraccion."""

    def test_genera_reporte_basico(self):
        """Debe generar reporte con estadísticas básicas."""
        resultados = {
            "ventas": pd.DataFrame({"producto": ["A", "B"], "cantidad": [10, 20]}),
            "clientes": pd.DataFrame({"nombre": ["Ana", "Luis", "Maria"]}),
        }

        reporte = generar_reporte_extraccion(resultados)

        assert reporte["num_fuentes"] == 2
        assert "ventas" in reporte["fuentes"]
        assert "clientes" in reporte["fuentes"]
        assert reporte["fuentes"]["ventas"]["filas"] == 2
        assert reporte["fuentes"]["clientes"]["filas"] == 3

    def test_calcula_totales_correctamente(self):
        """Debe calcular totales de filas y columnas únicas."""
        resultados = {
            "df1": pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
            "df2": pd.DataFrame({"col2": [5], "col3": [6]}),
        }

        reporte = generar_reporte_extraccion(resultados)

        assert reporte["totales"]["filas"] == 3  # 2 + 1
        assert set(reporte["totales"]["columnas_unicas"]) == {"col1", "col2", "col3"}

    def test_detecta_dataframes_vacios(self):
        """Debe marcar DataFrames vacíos."""
        resultados = {"vacio": pd.DataFrame(), "con_datos": pd.DataFrame({"col": [1]})}

        reporte = generar_reporte_extraccion(resultados)

        assert reporte["fuentes"]["vacio"]["vacio"] is True
        assert reporte["fuentes"]["con_datos"]["vacio"] is False

    def test_incluye_validaciones_si_provistas(self):
        """Debe incluir validaciones si se proporcionan."""
        resultados = {"df1": pd.DataFrame({"col": [1, 2]})}
        validaciones = {"df1": {"valido": True}}

        reporte = generar_reporte_extraccion(resultados, validaciones)

        assert "validaciones" in reporte
        assert reporte["validaciones"]["df1"]["valido"] is True

    def test_sin_validaciones_no_incluye_seccion(self):
        """Si no hay validaciones, no debe incluir sección."""
        resultados = {"df1": pd.DataFrame({"col": [1]})}

        reporte = generar_reporte_extraccion(resultados, validaciones=None)

        assert "validaciones" not in reporte

    def test_incluye_timestamp(self):
        """Debe incluir timestamp del reporte."""
        resultados = {"df1": pd.DataFrame({"col": [1]})}

        reporte = generar_reporte_extraccion(resultados)

        assert "timestamp" in reporte
        assert isinstance(reporte["timestamp"], str)


class TestGuardarResultados:
    """Tests para guardar_resultados."""

    def test_guarda_csv(self, tmp_path):
        """Debe guardar DataFrames como CSV."""
        resultados = {
            "ventas": pd.DataFrame({"producto": ["A", "B"], "cantidad": [10, 20]})
        }

        archivos = guardar_resultados(resultados, tmp_path, formato="csv")

        assert len(archivos) == 1
        assert archivos[0].suffix == ".csv"
        assert archivos[0].exists()

        # Verificar contenido
        df_leido = pd.read_csv(archivos[0])
        assert len(df_leido) == 2

    def test_guarda_json(self, tmp_path):
        """Debe guardar DataFrames como JSON."""
        resultados = {"datos": pd.DataFrame({"id": [1, 2], "nombre": ["Ana", "Luis"]})}

        archivos = guardar_resultados(resultados, tmp_path, formato="json")

        assert len(archivos) == 1
        assert archivos[0].suffix == ".json"
        assert archivos[0].exists()

    def test_guarda_excel(self, tmp_path):
        """Debe guardar DataFrames como Excel."""
        resultados = {"datos": pd.DataFrame({"col": [1, 2, 3]})}

        archivos = guardar_resultados(resultados, tmp_path, formato="excel")

        assert len(archivos) == 1
        assert archivos[0].suffix == ".xlsx"
        assert archivos[0].exists()

    def test_crea_directorio_si_no_existe(self, tmp_path):
        """Debe crear directorio de salida si no existe."""
        directorio_nuevo = tmp_path / "subdir" / "output"
        resultados = {"datos": pd.DataFrame({"col": [1]})}

        archivos = guardar_resultados(resultados, directorio_nuevo, formato="csv")

        assert directorio_nuevo.exists()
        assert len(archivos) == 1

    def test_omite_dataframes_vacios(self, tmp_path):
        """Debe omitir DataFrames vacíos."""
        resultados = {
            "vacio": pd.DataFrame(),
            "con_datos": pd.DataFrame({"col": [1, 2]}),
        }

        archivos = guardar_resultados(resultados, tmp_path, formato="csv")

        assert len(archivos) == 1  # Solo guardó el no vacío
        assert archivos[0].stem == "con_datos"

    def test_formato_invalido_lanza_error(self, tmp_path):
        """Formato no soportado debe lanzar ValueError."""
        resultados = {"datos": pd.DataFrame({"col": [1]})}

        with pytest.raises(ValueError, match="no soportado"):
            guardar_resultados(resultados, tmp_path, formato="xml")

    def test_guarda_multiples_resultados(self, tmp_path):
        """Debe guardar múltiples DataFrames."""
        resultados = {
            "ventas": pd.DataFrame({"col": [1]}),
            "clientes": pd.DataFrame({"col": [2]}),
            "productos": pd.DataFrame({"col": [3]}),
        }

        archivos = guardar_resultados(resultados, tmp_path, formato="csv")

        assert len(archivos) == 3
        nombres = {f.stem for f in archivos}
        assert nombres == {"ventas", "clientes", "productos"}


class TestPipelineCompleto:
    """Tests para pipeline_completo."""

    @patch("src.gestor_extracciones.orquestar_extraccion_multiple")
    @patch("src.gestor_extracciones.validar_no_vacio")
    def test_pipeline_sin_guardar(self, mock_validar, mock_orquestar):
        """Pipeline sin directorio de salida no debe guardar."""
        mock_resultados = {"df1": pd.DataFrame({"col": [1, 2]})}
        mock_orquestar.return_value = mock_resultados
        mock_validar.return_value = {"valido": True}

        fuentes = [{"tipo": "csv", "nombre": "f1", "config": {"ruta": "datos.csv"}}]

        reporte = pipeline_completo(fuentes, directorio_salida=None)

        assert "archivos_guardados" not in reporte
        assert reporte["num_fuentes"] == 1

    @patch("src.gestor_extracciones.orquestar_extraccion_multiple")
    @patch("src.gestor_extracciones.validar_no_vacio")
    @patch("src.gestor_extracciones.guardar_resultados")
    def test_pipeline_con_guardar(self, mock_guardar, mock_validar, mock_orquestar):
        """Pipeline con directorio debe guardar archivos."""
        mock_resultados = {"df1": pd.DataFrame({"col": [1]})}
        mock_orquestar.return_value = mock_resultados
        mock_validar.return_value = {"valido": True}
        mock_guardar.return_value = [Path("/output/df1.csv")]

        fuentes = [{"tipo": "csv", "nombre": "f1", "config": {"ruta": "datos.csv"}}]

        reporte = pipeline_completo(fuentes, directorio_salida="/output")

        assert "archivos_guardados" in reporte
        assert len(reporte["archivos_guardados"]) == 1
        mock_guardar.assert_called_once()

    @patch("src.gestor_extracciones.orquestar_extraccion_multiple")
    def test_pipeline_sin_validar(self, mock_orquestar):
        """Pipeline con validar=False no debe ejecutar validaciones."""
        mock_resultados = {"df1": pd.DataFrame({"col": [1]})}
        mock_orquestar.return_value = mock_resultados

        fuentes = [{"tipo": "csv", "nombre": "f1", "config": {"ruta": "datos.csv"}}]

        reporte = pipeline_completo(fuentes, validar=False)

        assert "validaciones" not in reporte

    @patch("src.gestor_extracciones.orquestar_extraccion_multiple")
    @patch("src.gestor_extracciones.validar_no_vacio")
    def test_pipeline_con_validar(self, mock_validar, mock_orquestar):
        """Pipeline con validar=True debe ejecutar validaciones."""
        mock_resultados = {"df1": pd.DataFrame({"col": [1]})}
        mock_orquestar.return_value = mock_resultados
        mock_validar.return_value = {"valido": True, "mensaje": "OK"}

        fuentes = [{"tipo": "csv", "nombre": "f1", "config": {"ruta": "datos.csv"}}]

        reporte = pipeline_completo(fuentes, validar=True)

        assert "validaciones" in reporte
        assert "df1" in reporte["validaciones"]
        mock_validar.assert_called_once()

    @patch("src.gestor_extracciones.orquestar_extraccion_multiple")
    @patch("src.gestor_extracciones.guardar_resultados")
    def test_pipeline_formato_salida_json(self, mock_guardar, mock_orquestar):
        """Debe poder usar formato JSON."""
        mock_resultados = {"df1": pd.DataFrame({"col": [1]})}
        mock_orquestar.return_value = mock_resultados
        mock_guardar.return_value = [Path("/output/df1.json")]

        fuentes = [{"tipo": "csv", "nombre": "f1", "config": {"ruta": "datos.csv"}}]

        pipeline_completo(fuentes, directorio_salida="/output", formato_salida="json")

        call_args = mock_guardar.call_args
        assert call_args[0][2] == "json"

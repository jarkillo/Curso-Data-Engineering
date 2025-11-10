"""
Proyecto Práctico: Data Warehouse Dimensional para E-commerce.

Este paquete implementa un data warehouse dimensional completo siguiendo
las mejores prácticas de modelado dimensional (Star Schema, SCD Tipo 2).

Módulos:
    - generador_dim_fecha: Generación de dimensión de fecha
    - generador_dim_producto: Generación de catálogo de productos
    - generador_dim_cliente: Generación de clientes
    - generador_dim_vendedor: Generación de vendedores
    - scd_tipo2: Implementación de Slowly Changing Dimensions Tipo 2
    - generador_fact_ventas: Generación de fact table de ventas
    - validaciones: Validación de integridad de datos
    - database: Conexión y esquema SQLite
    - queries_analiticos: Queries de negocio pre-diseñados
    - utilidades: Funciones auxiliares

Versión: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "DataFlow Industries"

"""
Constantes de error IDs para tracking en Sentry.

Cada error tiene un ID único que facilita:
- Búsqueda y filtrado en logs
- Métricas de frecuencia de errores
- Alertas configuradas por tipo de error
- Debugging y troubleshooting
"""


class ErrorIds:
    """IDs de error para categorización y tracking."""

    # Errores de Base de Datos (DB_*)
    DATABASE_CONNECTION_FAILED = "DB_CONN_001"
    DATABASE_CONNECTION_LOST = "DB_CONN_002"
    DATABASE_QUERY_FAILED = "DB_QUERY_003"
    DATABASE_OPERATION_FAILED = "DB_OP_004"
    DATABASE_TRANSACTION_FAILED = "DB_TX_005"

    # Errores de Checkpoint (CHECKPOINT_*)
    CHECKPOINT_CORRUPTED = "CHECKPOINT_001"
    CHECKPOINT_INVALID_TIMESTAMP = "CHECKPOINT_002"
    CHECKPOINT_READ_FAILED = "CHECKPOINT_003"
    CHECKPOINT_WRITE_FAILED = "CHECKPOINT_004"

    # Errores de Validación (VAL_*)
    VALIDATION_FAILED = "VAL_001"
    VALIDATION_MISSING_COLUMNS = "VAL_002"
    VALIDATION_NULL_VALUES = "VAL_003"
    VALIDATION_EMPTY_DATAFRAME = "VAL_004"

    # Errores de SQL Injection (SQL_*)
    SQL_INJECTION_ATTEMPT = "SQL_INJ_001"
    SQL_INVALID_IDENTIFIER = "SQL_INJ_002"

    # Errores de Configuración (CFG_*)
    CONFIG_MISSING_PARAMETER = "CFG_001"
    CONFIG_INVALID_VALUE = "CFG_002"
    CONFIG_STRATEGY_UNSUPPORTED = "CFG_003"

    # Errores Inesperados (UNEXPECTED_*)
    UNEXPECTED_ERROR = "UNEXPECTED_001"
    UNEXPECTED_TYPE_ERROR = "UNEXPECTED_002"

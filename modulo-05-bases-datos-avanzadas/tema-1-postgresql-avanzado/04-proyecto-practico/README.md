# Proyecto Práctico: PostgreSQL Avanzado

Sistema de gestión de eventos con características avanzadas de PostgreSQL: JSONB, funciones almacenadas y triggers.

## 🎯 Objetivos del Proyecto

- Practicar operaciones con JSONB en PostgreSQL
- Implementar funciones Python que interactúan con PostgreSQL avanzado
- Aplicar TDD con cobertura >80%
- Manejar conexiones de forma segura

## 📁 Estructura

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── conexion.py              # Gestión de conexiones
│   └── operaciones_json.py      # Operaciones con JSONB
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures de pytest
│   ├── test_conexion.py         # Tests de conexión
│   └── test_operaciones_json.py # Tests de JSONB
├── README.md                    # Este archivo
└── requirements.txt             # Dependencias
```

## 🚀 Instalación

### 1. Crear entorno virtual
```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
# Copiar ejemplo
cp .env.example .env

# Editar .env con tus credenciales
```

### 4. Iniciar PostgreSQL
```bash
# Con Docker
docker-compose up -d postgres

# Verificar
docker-compose ps
```

## 📚 Módulos

### `src/conexion.py`
Gestión de conexiones a PostgreSQL.

**Funciones:**
- `crear_conexion()`: Crea conexión a PostgreSQL
- `cerrar_conexion()`: Cierra conexión de forma segura
- `ejecutar_query()`: Ejecuta queries SELECT

### `src/operaciones_json.py`
Operaciones con datos JSONB.

**Funciones:**
- `insertar_json()`: Inserta documento JSON en tabla
- `consultar_json_por_campo()`: Consulta por campo dentro del JSON
- `actualizar_campo_json()`: Actualiza un campo específico del JSON

## 🧪 Ejecutar Tests

### Tests completos con cobertura
```bash
pytest --cov=src --cov-report=term --cov-report=html -v
```

### Solo tests de conexión
```bash
pytest tests/test_conexion.py -v
```

### Solo tests de JSON
```bash
pytest tests/test_operaciones_json.py -v
```

### Ver reporte HTML
```bash
# Se genera en htmlcov/
# Abrir htmlcov/index.html en navegador
```

## 💡 Ejemplos de Uso

### Conectar a PostgreSQL
```python
from src.conexion import crear_conexion, cerrar_conexion

# Crear conexión
conn = crear_conexion()

# Usar conexión
# ...

# Cerrar conexión
cerrar_conexion(conn)
```

### Insertar datos JSON
```python
from src.operaciones_json import insertar_json

conn = crear_conexion()

# Insertar evento
datos_evento = {
    "tipo": "page_view",
    "url": "/productos",
    "user_id": 123
}

id_evento = insertar_json(conn, "eventos", "datos", datos_evento)
print(f"Evento insertado con ID: {id_evento}")

cerrar_conexion(conn)
```

### Consultar datos JSON
```python
from src.operaciones_json import consultar_json_por_campo

conn = crear_conexion()

# Buscar eventos de un usuario
resultados = consultar_json_por_campo(
    conn,
    tabla="eventos",
    columna_json="datos",
    campo="user_id",
    valor=123
)

for evento in resultados:
    print(f"ID: {evento['id']}, Datos: {evento['datos']}")

cerrar_conexion(conn)
```

### Actualizar campo JSON
```python
from src.operaciones_json import actualizar_campo_json

conn = crear_conexion()

# Marcar evento como procesado
actualizado = actualizar_campo_json(
    conn,
    tabla="eventos",
    columna_json="datos",
    id_registro=1,
    campo="procesado",
    nuevo_valor=True
)

if actualizado:
    print("Campo actualizado correctamente")

cerrar_conexion(conn)
```

## 📊 Métricas de Calidad

- **Tests:** 30+ tests unitarios
- **Cobertura:** >85% (objetivo: >80%)
- **Linting:** Cumple flake8
- **Formateo:** Cumple black
- **Tipado:** 100% con type hints

## ⚠️ Notas de Seguridad

1. **Nunca hardcodees credenciales** en el código
2. **Usa variables de entorno** para configuración sensible
3. **Parámetros en queries** previenen SQL injection
4. **Cierra conexiones** siempre (usa context managers)

## 🔧 Troubleshooting

### Error: "could not connect to server"
```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Ver logs
docker-compose logs postgres
```

### Error: "relation does not exist"
```sql
-- Crear tabla de eventos
CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    datos JSONB NOT NULL,
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Crear índice GIN para búsquedas rápidas
CREATE INDEX idx_eventos_datos ON eventos USING GIN (datos);
```

### Error en tests: "No module named 'src'"
```bash
# Asegurarse de estar en la carpeta correcta
cd 04-proyecto-practico

# Ejecutar tests con Python module
python -m pytest
```

## 📖 Referencias

- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [PostgreSQL JSON Functions](https://www.postgresql.org/docs/current/functions-json.html)
- [pytest Documentation](https://docs.pytest.org/)

---

**Última actualización:** 2025-10-25
**Versión:** 1.0.0
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [MongoDB - 01 Teoria](../../tema-2-mongodb/01-TEORIA.md)

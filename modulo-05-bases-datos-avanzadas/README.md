# Módulo 5: Bases de Datos Avanzadas

Bienvenido al **Módulo 5** del Master en Ingeniería de Datos con IA.

## 🎯 Objetivos del Módulo

Al completar este módulo, serás capaz de:

- Trabajar con tipos de datos avanzados en PostgreSQL (JSON, Arrays, UUID)
- Crear funciones almacenadas y triggers con PL/pgSQL
- Comprender transacciones ACID en profundidad
- Diseñar y trabajar con bases de datos NoSQL (MongoDB)
- Realizar agregaciones complejas en MongoDB
- Aplicar técnicas de normalización (1NF, 2NF, 3NF, BCNF)
- Diseñar esquemas dimensionales (Star Schema, Snowflake)
- Tomar decisiones informadas entre SQL y NoSQL

## 📚 Estructura del Módulo

### Tema 1: PostgreSQL Avanzado
**Duración estimada:** 3-4 días

Explora características avanzadas de PostgreSQL que lo convierten en una base de datos extremadamente poderosa para Data Engineering.

- **01-TEORIA.md**: Tipos avanzados, funciones almacenadas, PL/pgSQL, transacciones
- **02-EJEMPLOS.md**: 5 ejemplos ejecutables con PostgreSQL
- **03-EJERCICIOS.md**: 15 ejercicios (básico → avanzado)
- **04-proyecto-practico/**: Sistema transaccional con funciones almacenadas

[📂 Ir al Tema 1](./tema-1-postgresql-avanzado/)

---

### Tema 2: NoSQL con MongoDB
**Duración estimada:** 3-4 días

Aprende a trabajar con bases de datos NoSQL orientadas a documentos y cuándo usarlas en lugar de SQL.

- **01-TEORIA.md**: Documentos, colecciones, queries, agregaciones
- **02-EJEMPLOS.md**: 5 ejemplos ejecutables con MongoDB
- **03-EJERCICIOS.md**: 15 ejercicios (básico → avanzado)
- **04-proyecto-practico/**: Sistema de logs con agregaciones complejas

[📂 Ir al Tema 2](./tema-2-mongodb/)

---

### Tema 3: Modelado de Datos
**Duración estimada:** 2-3 días

Domina el arte de diseñar modelos de datos eficientes y escalables, tanto para OLTP como OLAP.

- **01-TEORIA.md**: Normalización, diseño ER, Star Schema, Snowflake
- **02-EJEMPLOS.md**: 4 ejemplos de modelado con diagramas
- **03-EJERCICIOS.md**: 12 ejercicios de diseño
- **04-proyecto-practico/**: Diseño de Data Warehouse dimensional

[📂 Ir al Tema 3](./tema-3-modelado-datos/)

---

## 🛠️ Requisitos Previos

### Conocimientos
- SQL básico (SELECT, WHERE, JOIN, GROUP BY)
- Python básico
- Conceptos de bases de datos relacionales

### Software Necesario

#### Docker (Recomendado)
```bash
# Iniciar PostgreSQL y MongoDB
docker-compose up -d postgres mongodb

# Verificar que están corriendo
docker-compose ps
```

#### PostgreSQL 15+
```bash
# Verificar instalación
psql --version

# Conectar (si no usas Docker)
psql -U usuario -d base_datos
```

#### MongoDB 6+
```bash
# Verificar instalación
mongosh --version

# Conectar (si no usas Docker)
mongosh "mongodb://localhost:27017"
```

#### Python 3.11+
```bash
# Instalar dependencias por tema
cd tema-X-nombre/04-proyecto-practico
pip install -r requirements.txt
```

---

## 📊 Progreso del Módulo

### Tema 1: PostgreSQL Avanzado ✅ 100% COMPLETADO
- [x] Leer 01-TEORIA.md
- [x] Estudiar 02-EJEMPLOS.md
- [x] Resolver 03-EJERCICIOS.md
- [x] Completar proyecto práctico
- [x] Tests pasando (>80% cobertura)

### Tema 2: MongoDB ✅ 100% COMPLETADO
- [x] Leer 01-TEORIA.md
- [x] Estudiar 02-EJEMPLOS.md
- [x] Resolver 03-EJERCICIOS.md
- [x] Completar proyecto práctico
- [x] Tests pasando (99% cobertura - 56 tests)

### Tema 3: Modelado de Datos ✅ 100% COMPLETADO
- [x] Leer 01-TEORIA.md
- [x] Estudiar 02-EJEMPLOS.md
- [x] Resolver 03-EJERCICIOS.md
- [x] Completar proyecto práctico
- [x] Tests pasando (98% cobertura - 25 tests)

---

## 🎓 Metodología de Estudio

### 1. Teoría (30-45 min por tema)
Lee el archivo `01-TEORIA.md` de cada tema. No te apresures, asegúrate de entender cada concepto antes de continuar.

### 2. Ejemplos (45-60 min por tema)
Estudia los ejemplos en `02-EJEMPLOS.md`. **Ejecuta el código** y experimenta modificándolo.

### 3. Ejercicios (2-3 horas por tema)
Resuelve los ejercicios de `03-EJERCICIOS.md`. Intenta resolverlos sin mirar las soluciones primero.

### 4. Proyecto Práctico (4-6 horas por tema)
Implementa el proyecto práctico siguiendo TDD:
1. Lee el README del proyecto
2. Revisa los tests en `tests/`
3. Implementa las funciones en `src/`
4. Ejecuta `pytest` hasta que todo pase
5. Verifica cobertura con `pytest --cov`

---

## 🔧 Docker Compose - Guía Rápida

### Iniciar servicios
```bash
# PostgreSQL + MongoDB
docker-compose up -d postgres mongodb

# Ver logs
docker-compose logs -f postgres
docker-compose logs -f mongodb
```

### Conectar a PostgreSQL
```bash
# Desde terminal
docker exec -it master-postgres psql -U dataeng_user -d dataeng_db

# Desde Python
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="dataeng_user",
    password="DataEng2025!SecurePass",
    database="dataeng_db"
)
```

### Conectar a MongoDB
```bash
# Desde terminal
docker exec -it master-mongodb mongosh -u admin -p MongoAdmin2025!SecurePass

# Desde Python
from pymongo import MongoClient
client = MongoClient(
    "mongodb://admin:MongoAdmin2025!SecurePass@localhost:27017/"
)
db = client.dataeng_db
```

### Detener servicios
```bash
docker-compose down

# Eliminar datos (CUIDADO)
docker-compose down -v
```

---

## 📚 Recursos Adicionales

### PostgreSQL
- [Documentación Oficial](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [PL/pgSQL Guide](https://www.postgresql.org/docs/current/plpgsql.html)

### MongoDB
- [Documentación Oficial](https://www.mongodb.com/docs/)
- [MongoDB University](https://university.mongodb.com/) (Cursos gratuitos)
- [Aggregation Pipeline Builder](https://www.mongodb.com/docs/compass/current/agg-pipeline-builder/)

### Modelado de Datos
- Libro: "The Data Warehouse Toolkit" - Ralph Kimball
- [Database Design Tutorial](https://www.lucidchart.com/pages/database-diagram/database-design)
- [Star Schema vs Snowflake](https://www.holistics.io/blog/star-schema-vs-snowflake-schema/)

---

## ⚠️ Notas de Seguridad

### Docker Compose
Las contraseñas en `docker-compose.yml` son de **EJEMPLO**. En producción:

1. Usa un archivo `.env`:
   ```bash
   POSTGRES_PASSWORD=tu_password_seguro
   MONGO_ROOT_PASSWORD=otro_password_seguro
   ```

2. Añade `.env` al `.gitignore`

3. Usa contraseñas fuertes (mínimo 16 caracteres, con mayúsculas, minúsculas, números y símbolos)

4. Limita el acceso con firewalls

### Conexiones
Nunca hardcodees credenciales en el código. Usa variables de entorno:

```python
import os

# ✅ CORRECTO
password = os.getenv("DB_PASSWORD")

# ❌ INCORRECTO
password = "mi_password_secreto"
```

---

## 🤝 Contribuciones

¿Encontraste un error? ¿Tienes una sugerencia?

1. Abre un issue en GitHub
2. Describe el problema o mejora
3. Si es código, incluye cómo reproducirlo

---

## 📈 Métricas del Módulo

### Contenido
- **3/3 temas completados (100%)** ✅
- **~32,000 palabras** de teoría total
- **14 ejemplos** ejecutables
- **42 ejercicios** con soluciones completas

### Código
- **Tema 2**: 12 funciones, 56 tests, 99% cobertura
- **Tema 3**: 9 funciones, 25 tests, 98% cobertura
- **Total**: **81 tests** unitarios
- **98% cobertura promedio** (supera objetivo ≥80%)
- **100% tipado** (type hints completos)

### Progreso General
```
Tema 1: ████████████████████ 100% ✅ Completado
Tema 2: ████████████████████ 100% ✅ Completado (2025-11-12)
Tema 3: ████████████████████ 100% ✅ Completado (2025-11-12)
──────────────────────────────────────────────────────────
Total:  ████████████████████ 100% ✅ MÓDULO COMPLETO
```

---

**Última actualización:** 2025-11-12
**Versión:** 2.0.0
**Estado:** ✅ COMPLETADO 100% (3/3 temas completados)

¡Éxito en tu aprendizaje de Bases de Datos Avanzadas! 🚀

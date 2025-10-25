# Tema 1: PostgreSQL Avanzado

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

- Trabajar con tipos de datos avanzados (JSON, JSONB, Arrays, UUID, HSTORE)
- Crear funciones almacenadas con PL/pgSQL
- Implementar triggers para automatizar acciones
- Comprender y aplicar transacciones ACID
- Optimizar consultas con tipos de datos apropiados
- Decidir cuándo usar características avanzadas de PostgreSQL

## 📚 Contenido

### [01-TEORIA.md](./01-TEORIA.md)
**Duración:** 30-45 minutos

Conceptos fundamentales de PostgreSQL avanzado explicados desde cero con analogías del mundo real.

**Temas cubiertos:**
- Tipos de datos avanzados (JSON/JSONB, Arrays, UUID, HSTORE)
- Funciones almacenadas y PL/pgSQL
- Triggers y automatización
- Transacciones ACID en profundidad
- Cuándo y por qué usar cada característica

### [02-EJEMPLOS.md](./02-EJEMPLOS.md)
**Duración:** 45-60 minutos

5 ejemplos trabajados paso a paso con código ejecutable.

**Ejemplos incluidos:**
1. Almacenar y consultar datos JSON
2. Trabajar con Arrays de PostgreSQL
3. Crear funciones almacenadas
4. Implementar triggers
5. Transacciones complejas

### [03-EJERCICIOS.md](./03-EJERCICIOS.md)
**Duración:** 2-3 horas

15 ejercicios prácticos con soluciones completas.

**Distribución:**
- 6 ejercicios básicos ⭐
- 6 ejercicios intermedios ⭐⭐
- 3 ejercicios avanzados ⭐⭐⭐

### [04-proyecto-practico/](./04-proyecto-practico/)
**Duración:** 4-6 horas

Proyecto completo: Sistema de gestión de transacciones bancarias con funciones almacenadas, triggers y validaciones.

**Funcionalidades:**
- Gestión de cuentas bancarias
- Transferencias con validaciones
- Triggers para auditoría
- Funciones almacenadas para lógica de negocio
- Tests completos (>80% cobertura)

## 🚀 Cómo Estudiar Este Tema

### Paso 1: Preparar el entorno (15 min)
```bash
# Iniciar PostgreSQL con Docker
docker-compose up -d postgres

# Verificar conexión
docker exec -it master-postgres psql -U dataeng_user -d dataeng_db

# Dentro de psql, verificar
\conninfo
```

### Paso 2: Leer teoría (30-45 min)
- Lee `01-TEORIA.md` completo
- No te saltes las analogías, te ayudarán a entender conceptos complejos
- Marca los conceptos que no entiendes para revisarlos

### Paso 3: Estudiar ejemplos (45-60 min)
- Abre `02-EJEMPLOS.md`
- **Ejecuta cada ejemplo** en tu PostgreSQL local
- Modifica los ejemplos para experimentar
- Observa los resultados

### Paso 4: Resolver ejercicios (2-3 horas)
- Intenta cada ejercicio sin ver la solución
- Si te atascas más de 15 minutos, mira la ayuda
- Solo mira la solución después de intentarlo seriamente
- Verifica tu solución contra la oficial

### Paso 5: Proyecto práctico (4-6 horas)
```bash
cd 04-proyecto-practico

# Instalar dependencias
pip install -r requirements.txt

# Revisar tests
pytest -v

# Implementar funciones
# (Edita archivos en src/)

# Verificar cobertura
pytest --cov=src --cov-report=html
```

## 📊 Checklist de Progreso

- [ ] PostgreSQL corriendo en Docker
- [ ] 01-TEORIA.md leído y comprendido
- [ ] 02-EJEMPLOS.md estudiado y ejemplos ejecutados
- [ ] Ejercicios 1-6 (básicos) resueltos
- [ ] Ejercicios 7-12 (intermedios) resueltos
- [ ] Ejercicios 13-15 (avanzados) resueltos
- [ ] Proyecto práctico completado
- [ ] Tests del proyecto pasando (>80% cobertura)

## 🔧 Requisitos Técnicos

### Software
- PostgreSQL 15+ (via Docker o instalación local)
- Python 3.11+
- psycopg2 (para conectar Python a PostgreSQL)

### Conocimientos Previos
- SQL básico (SELECT, INSERT, UPDATE, DELETE)
- Python básico
- Conceptos de bases de datos relacionales

## 💡 Tips para el Éxito

1. **Ejecuta TODO el código**: No solo leas, ¡practica!
2. **Experimenta**: Modifica los ejemplos para ver qué pasa
3. **Lee los errores**: PostgreSQL tiene mensajes de error muy descriptivos
4. **Usa \d en psql**: Para ver la estructura de tablas y funciones
5. **Documenta tu aprendizaje**: Escribe notas sobre lo que aprendes

## 🆘 Ayuda y Recursos

### Comandos útiles de psql
```sql
\l                    -- Listar bases de datos
\c database_name      -- Conectar a una BD
\dt                   -- Listar tablas
\df                   -- Listar funciones
\d+ table_name        -- Describir tabla
\q                    -- Salir
```

### Documentación Oficial
- [PostgreSQL 15 Docs](https://www.postgresql.org/docs/15/)
- [JSON Types](https://www.postgresql.org/docs/15/datatype-json.html)
- [PL/pgSQL](https://www.postgresql.org/docs/15/plpgsql.html)
- [Triggers](https://www.postgresql.org/docs/15/triggers.html)

### Recursos Adicionales
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [PL/pgSQL by Example](https://www.postgresql.org/docs/15/plpgsql-examples.html)

## ⚠️ Errores Comunes

### 1. "could not connect to server"
```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Si no está, iniciarlo
docker-compose up -d postgres
```

### 2. "permission denied for table"
```sql
-- Verificar permisos
SELECT current_user;

-- En psql como superuser, otorgar permisos
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dataeng_user;
```

### 3. "syntax error at or near..."
- Verifica punto y coma (;) al final de cada statement
- Revisa comillas: '' para strings, "" para identificadores
- PL/pgSQL requiere $$...$$  o 'BEGIN...END'

---

**Siguiente:** [Tema 2: MongoDB →](../tema-2-mongodb/)

**Última actualización:** 2025-10-25

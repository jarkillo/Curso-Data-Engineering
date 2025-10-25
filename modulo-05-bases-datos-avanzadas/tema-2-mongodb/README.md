# Tema 2: NoSQL con MongoDB

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

- Comprender el paradigma NoSQL y cuándo usarlo
- Trabajar con documentos y colecciones en MongoDB
- Realizar queries complejas con operadores de MongoDB
- Implementar pipelines de agregación para análisis avanzados
- Diseñar esquemas flexibles y eficientes
- Decidir cuándo usar MongoDB vs PostgreSQL
- Conectar MongoDB con Python usando pymongo

## 📚 Contenido

### [01-TEORIA.md](./01-TEORIA.md)
**Duración:** 30-45 minutos

Conceptos fundamentales de MongoDB y NoSQL explicados desde cero.

**Temas cubiertos:**
- Paradigma NoSQL vs SQL
- Documentos y colecciones
- Queries y operadores
- Pipeline de agregación
- Índices en MongoDB
- Cuándo usar MongoDB

### [02-EJEMPLOS.md](./02-EJEMPLOS.md)
**Duración:** 45-60 minutos

5 ejemplos trabajados paso a paso con código ejecutable.

**Ejemplos incluidos:**
1. CRUD básico con MongoDB
2. Queries con operadores ($gt, $in, $regex)
3. Actualizar documentos embebidos
4. Agregaciones simples
5. Pipeline de agregación complejo

### [03-EJERCICIOS.md](./03-EJERCICIOS.md)
**Duración:** 2-3 horas

15 ejercicios prácticos con soluciones completas.

**Distribución:**
- 6 ejercicios básicos ⭐
- 6 ejercicios intermedios ⭐⭐
- 3 ejercicios avanzados ⭐⭐⭐

### [04-proyecto-practico/](./04-proyecto-practico/)
**Duración:** 4-6 horas

Proyecto completo: Sistema de logs con análisis mediante agregaciones.

**Funcionalidades:**
- Inserción masiva de logs
- Queries complejas con múltiples filtros
- Agregaciones por nivel, fecha, servicio
- Análisis de errores y patrones
- Tests completos (>80% cobertura)

## 🚀 Cómo Estudiar Este Tema

### Paso 1: Preparar el entorno (15 min)
```bash
# Iniciar MongoDB con Docker
docker-compose up -d mongodb

# Verificar conexión
docker exec -it master-mongodb mongosh -u admin -p MongoAdmin2025!SecurePass

# Dentro de mongosh, verificar
show dbs
use dataeng_db
```

### Paso 2: Leer teoría (30-45 min)
- Lee `01-TEORIA.md` completo
- Compara constantemente con SQL que ya conoces
- Entiende CUÁNDO usar MongoDB vs PostgreSQL

### Paso 3: Estudiar ejemplos (45-60 min)
- Abre `02-EJEMPLOS.md`
- **Ejecuta cada ejemplo** en tu MongoDB local
- Experimenta modificando las queries
- Observa cómo cambian los resultados

### Paso 4: Resolver ejercicios (2-3 horas)
- Intenta cada ejercicio sin ver la solución
- MongoDB tiene una curva de aprendizaje, es normal atascarse
- Si llevas >15 minutos, mira la ayuda
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

- [ ] MongoDB corriendo en Docker
- [ ] 01-TEORIA.md leído y comprendido
- [ ] Diferencias SQL vs NoSQL claras
- [ ] 02-EJEMPLOS.md estudiado y ejemplos ejecutados
- [ ] Ejercicios 1-6 (básicos) resueltos
- [ ] Ejercicios 7-12 (intermedios) resueltos
- [ ] Ejercicios 13-15 (avanzados) resueltos
- [ ] Proyecto práctico completado
- [ ] Tests del proyecto pasando (>80% cobertura)

## 🔧 Requisitos Técnicos

### Software
- MongoDB 6+ (via Docker o instalación local)
- Python 3.11+
- pymongo (driver de MongoDB para Python)

### Conocimientos Previos
- SQL básico (para comparar)
- Python básico
- JSON (fundamental para MongoDB)

## 💡 Tips para el Éxito

1. **Piensa en documentos, no en tablas**: MongoDB es diferente
2. **JSON es tu aliado**: Todo en MongoDB es JSON
3. **Experimenta sin miedo**: MongoDB es muy flexible
4. **Usa MongoDB Compass**: GUI oficial muy útil para visualizar
5. **Lee los errores**: MongoDB te dice exactamente qué está mal

## 🆘 Ayuda y Recursos

### Comandos útiles de mongosh
```javascript
show dbs                    // Listar bases de datos
use nombre_db               // Usar una BD
show collections            // Listar colecciones
db.coleccion.find()         // Ver documentos
db.coleccion.find().pretty() // Ver formateado
db.coleccion.countDocuments() // Contar
exit                        // Salir
```

### Documentación Oficial
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query/)
- [Aggregation Pipeline](https://www.mongodb.com/docs/manual/aggregation/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)

### Recursos Adicionales
- [MongoDB University](https://university.mongodb.com/) - Cursos gratuitos
- [MongoDB Compass](https://www.mongodb.com/products/compass) - GUI oficial
- [Studio 3T](https://studio3t.com/) - IDE alternativo

## ⚠️ Errores Comunes

### 1. "connection refused"
```bash
# Verificar que MongoDB está corriendo
docker-compose ps

# Si no está, iniciarlo
docker-compose up -d mongodb

# Ver logs
docker-compose logs -f mongodb
```

### 2. "authentication failed"
```javascript
// Verificar credenciales en docker-compose.yml
// Usuario: admin
// Password: MongoAdmin2025!SecurePass

// Conectar con:
mongosh "mongodb://admin:MongoAdmin2025!SecurePass@localhost:27017/"
```

### 3. "database doesn't exist"
```javascript
// MongoDB crea la BD al insertar el primer documento
use mi_base_datos
db.mi_coleccion.insertOne({nombre: "test"})
// ¡Ahora existe!
```

### 4. Confundir find() con findOne()
```javascript
// find() retorna cursor (múltiples documentos)
db.usuarios.find({edad: {$gt: 18}})

// findOne() retorna UN documento
db.usuarios.findOne({email: "ana@example.com"})
```

## 🔄 SQL vs MongoDB - Cheat Sheet

| SQL         | MongoDB              |
| ----------- | -------------------- |
| Database    | Database             |
| Table       | Collection           |
| Row         | Document             |
| Column      | Field                |
| Primary Key | _id (automático)     |
| JOIN        | $lookup (o embeber)  |
| WHERE       | find({condiciones})  |
| SELECT      | projection           |
| INSERT      | insertOne/insertMany |
| UPDATE      | updateOne/updateMany |
| DELETE      | deleteOne/deleteMany |
| GROUP BY    | $group               |
| ORDER BY    | sort()               |
| LIMIT       | limit()              |

## 📈 Cuando Usar MongoDB vs PostgreSQL

### ✅ Usa MongoDB cuando:
- Datos semi-estructurados o esquema cambiante
- Escalabilidad horizontal crítica
- Documentos con estructuras muy diferentes
- Logs, eventos, métricas
- Prototipado rápido
- Catálogos de productos con atributos variables

### ✅ Usa PostgreSQL cuando:
- Datos altamente estructurados
- Integridad relacional importante
- Transacciones complejas ACID
- Queries con múltiples JOINs
- Reportes financieros
- Datos tabulares tradicionales

### 🤝 Usa ambos cuando:
- PostgreSQL para transacciones
- MongoDB para logs y analytics
- Arquitectura polyglot persistence

---

**Siguiente:** [Tema 3: Modelado de Datos →](../tema-3-modelado-datos/)

**Última actualización:** 2025-10-25

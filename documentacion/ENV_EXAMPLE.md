# 🔐 Variables de Entorno - Plantilla

Este archivo contiene un ejemplo de las variables de entorno necesarias para el proyecto.

---

## 📋 Instrucciones de Uso

1. **Crea un archivo `.env` en la raíz del proyecto**:
   ```bash
   # En la raíz del proyecto
   touch .env  # Linux/Mac
   # O créalo manualmente en Windows
   ```

2. **Copia el contenido de abajo al archivo `.env`**

3. **Reemplaza los valores de ejemplo con valores reales**

4. **NUNCA commitees el archivo `.env` al repositorio**
   - El `.gitignore` ya está configurado para ignorar `.env`

---

## 🔒 Contenido de `.env`

```bash
# ===============================================
# BASES DE DATOS
# ===============================================

# PostgreSQL (Principal)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=dataeng_user
POSTGRES_PASSWORD=TuContraseñaSegura123!
POSTGRES_DB=dataeng_db

# PostgreSQL (Airflow)
AIRFLOW_POSTGRES_HOST=localhost
AIRFLOW_POSTGRES_PORT=5433
AIRFLOW_POSTGRES_USER=airflow
AIRFLOW_POSTGRES_PASSWORD=OtraContraseñaSegura456!
AIRFLOW_POSTGRES_DB=airflow

# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=MongoContraseñaSegura789!
MONGO_DB=dataeng_db
MONGO_AUTH_SOURCE=admin

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=RedisContraseñaSegura012!

# ===============================================
# APACHE AIRFLOW
# ===============================================
AIRFLOW_HOME=./airflow
AIRFLOW_WEB_USER=admin
AIRFLOW_WEB_PASSWORD=AirflowAdmin345!
AIRFLOW_EXECUTOR=LocalExecutor

# Fernet Key para cifrado de credenciales (CRÍTICO)
# Genera una nueva con: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# IMPORTANTE: Usa la MISMA clave en todos los servicios de Airflow
AIRFLOW_FERNET_KEY=n3ZWLdC8o4d4n2FmztvqiggQ6d-R3CWNlMvpcqVgDu8=

# ===============================================
# AWS
# ===============================================
AWS_ACCESS_KEY_ID=tu_access_key_aqui
AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET=mi-bucket-dataeng

# ===============================================
# GOOGLE CLOUD PLATFORM
# ===============================================
GCP_PROJECT_ID=tu-proyecto-gcp
GCP_CREDENTIALS_PATH=./credentials/gcp-service-account.json
GCP_BUCKET=mi-bucket-gcp

# ===============================================
# AZURE (Opcional)
# ===============================================
AZURE_STORAGE_CONNECTION_STRING=tu_connection_string_aqui
AZURE_STORAGE_ACCOUNT=tu_cuenta_storage
AZURE_CONTAINER_NAME=tu_contenedor

# ===============================================
# APIS EXTERNAS
# ===============================================
API_BASE_URL=https://api.example.com
API_KEY=tu_api_key_aqui
API_SECRET=tu_api_secret_aqui

# ===============================================
# SEGURIDAD
# ===============================================
SECRET_KEY=tu_secret_key_super_segura_y_larga
JWT_SECRET_KEY=tu_jwt_secret_key_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
ENCRYPTION_KEY=tu_encryption_key_aqui

# ===============================================
# LOGGING Y MONITOREO
# ===============================================
LOG_LEVEL=INFO
LOG_FILE_PATH=./logs/app.log
SENTRY_DSN=https://tu_sentry_dsn_aqui

# ===============================================
# ENTORNO
# ===============================================
ENVIRONMENT=development
DEBUG=True

# ===============================================
# SPARK (Módulo 9)
# ===============================================
SPARK_HOME=/path/to/spark
SPARK_MASTER=local[*]
SPARK_DRIVER_MEMORY=4g
SPARK_EXECUTOR_MEMORY=4g

# ===============================================
# KAFKA (Módulo 9)
# ===============================================
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_PREFIX=dataeng

# ===============================================
# MLFLOW (Módulo 10)
# ===============================================
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_ARTIFACT_ROOT=s3://mi-bucket/mlflow-artifacts

# ===============================================
# CONFIGURACIÓN DE APLICACIÓN
# ===============================================
APP_NAME=Master Data Engineering
APP_VERSION=1.0.0
APP_HOST=0.0.0.0
APP_PORT=8000

# ===============================================
# TIMEOUTS Y LÍMITES
# ===============================================
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RATE_LIMIT_PER_MINUTE=60
MAX_CONCURRENT_TASKS=10

# ===============================================
# EMAILS (Opcional)
# ===============================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_app
SMTP_FROM_EMAIL=noreply@dataeng.com

# ===============================================
# TESTING
# ===============================================
TEST_DATABASE_URL=postgresql://test_user:test_pass@localhost:5432/test_db
TEST_MODE=False
```

---

## 🔑 Generación de Claves Seguras

### Secret Keys Generales

```python
import secrets
print(secrets.token_urlsafe(32))
```

### Fernet Key (para Airflow)

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### UUID (para IDs únicos)

```python
import uuid
print(str(uuid.uuid4()))
```

---

## 🛡️ Mejores Prácticas de Seguridad

1. **Contraseñas Fuertes**:
   - Mínimo 12 caracteres
   - Mezcla de mayúsculas, minúsculas, números y símbolos
   - No usar palabras del diccionario
   - No reutilizar contraseñas

2. **Rotación de Credenciales**:
   - Cambia las contraseñas cada 3-6 meses
   - Rota API keys regularmente
   - Documenta cuándo se cambió cada credencial

3. **Separación de Entornos**:
   - Usa diferentes credenciales para development, staging y production
   - Nunca uses credenciales de producción en desarrollo

4. **Backup Seguro**:
   - Guarda las credenciales en un gestor de contraseñas
   - No las envíes por email o chat
   - No las almacenes en texto plano

5. **Permisos Mínimos**:
   - Otorga solo los permisos necesarios
   - Usa cuentas de servicio separadas para cada aplicación
   - Limita el acceso por IP cuando sea posible

---

## 🚨 Qué NO Hacer

❌ No commitees el archivo `.env` al repositorio
❌ No compartas credenciales por email/chat
❌ No uses contraseñas simples como `123456` o `password`
❌ No reutilices la misma contraseña en múltiples servicios
❌ No incluyas credenciales en logs o mensajes de error
❌ No uses credenciales de producción en desarrollo

---

## ✅ Checklist de Seguridad

- [ ] Archivo `.env` creado en la raíz del proyecto
- [ ] Todas las contraseñas son fuertes (12+ caracteres)
- [ ] `.env` está en el `.gitignore`
- [ ] No hay credenciales en el código fuente
- [ ] Las credenciales están documentadas en un gestor de contraseñas
- [ ] Se han generado claves únicas (no usar las de ejemplo)
- [ ] Se configuró el acceso por IP cuando sea posible
- [ ] Se probó la conexión con las credenciales configuradas

---

## 📚 Referencias

- [12 Factor App - Config](https://12factor.net/config)
- [OWASP - Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Secrets Management Best Practices](https://www.doppler.com/blog/secrets-management-best-practices)

---

*Última actualización: 2025-10-18*


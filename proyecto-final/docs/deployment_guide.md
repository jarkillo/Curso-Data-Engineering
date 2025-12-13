# Guía de Despliegue - TechMart Analytics Pipeline

## Requisitos Previos

### Software

| Componente | Versión Mínima | Recomendada |
|------------|----------------|-------------|
| Python | 3.11 | 3.12 |
| Docker | 20.10 | 24.0+ |
| Docker Compose | 2.0 | 2.20+ |
| PostgreSQL | 14 | 15 |
| Apache Airflow | 2.7 | 2.8+ |

### Hardware (Producción)

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disco | 50 GB SSD | 100 GB SSD |

## Instalación Local (Desarrollo)

### 1. Clonar Repositorio

```bash
git clone https://github.com/org/techmart-etl.git
cd techmart-etl/proyecto-final
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=techmart
DB_USER=etl_user
DB_PASSWORD=your_secure_password

# API
API_URL=http://localhost:8000
API_KEY=your_api_key

# Rutas
WAREHOUSE_PATH=./data/warehouse
RAW_DATA_PATH=./data/raw

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 5. Ejecutar Tests

```bash
# Tests unitarios
pytest tests/ -v

# Con cobertura
pytest --cov=src --cov-report=html --cov-report=term-missing

# Solo tests rápidos
pytest tests/ -m "not integration"
```

## Despliegue con Docker

### 1. Estructura de Docker

```
docker/
├── Dockerfile
├── docker-compose.yml
└── airflow/
    └── Dockerfile.airflow
```

### 2. Dockerfile Principal

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY dags/ ./dags/

# Usuario no-root
RUN useradd -m etl_user
USER etl_user

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s \
    CMD python -c "import src; print('OK')" || exit 1

ENTRYPOINT ["python"]
```

### 3. Docker Compose

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  # Base de datos PostgreSQL
  postgres:
    image: postgres:15
    container_name: techmart-postgres
    environment:
      POSTGRES_USER: etl_user
      POSTGRES_PASSWORD: ${DB_PASSWORD:-securepass123}
      POSTGRES_DB: techmart
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U etl_user -d techmart"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis (para Airflow Celery)
  redis:
    image: redis:7
    container_name: techmart-redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Airflow Webserver
  airflow-webserver:
    build:
      context: .
      dockerfile: airflow/Dockerfile.airflow
    container_name: techmart-airflow-webserver
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://etl_user:${DB_PASSWORD:-securepass123}@postgres/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
      - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://etl_user:${DB_PASSWORD:-securepass123}@postgres/airflow
      - AIRFLOW__WEBSERVER__SECRET_KEY=${AIRFLOW_SECRET_KEY:-your_secret_key}
    ports:
      - "8080:8080"
    volumes:
      - ../dags:/opt/airflow/dags
      - ../src:/opt/airflow/src
      - airflow_logs:/opt/airflow/logs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: webserver
    restart: unless-stopped

  # Airflow Scheduler
  airflow-scheduler:
    build:
      context: .
      dockerfile: airflow/Dockerfile.airflow
    container_name: techmart-airflow-scheduler
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://etl_user:${DB_PASSWORD:-securepass123}@postgres/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
    volumes:
      - ../dags:/opt/airflow/dags
      - ../src:/opt/airflow/src
      - airflow_logs:/opt/airflow/logs
    depends_on:
      - airflow-webserver
    command: scheduler
    restart: unless-stopped

  # Airflow Worker
  airflow-worker:
    build:
      context: .
      dockerfile: airflow/Dockerfile.airflow
    container_name: techmart-airflow-worker
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://etl_user:${DB_PASSWORD:-securepass123}@postgres/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
    volumes:
      - ../dags:/opt/airflow/dags
      - ../src:/opt/airflow/src
      - airflow_logs:/opt/airflow/logs
      - warehouse_data:/data/warehouse
    depends_on:
      - airflow-scheduler
    command: celery worker
    restart: unless-stopped

volumes:
  postgres_data:
  airflow_logs:
  warehouse_data:

networks:
  default:
    name: techmart-network
```

### 4. Levantar Servicios

```bash
cd docker

# Construir imágenes
docker-compose build

# Inicializar base de datos de Airflow
docker-compose run --rm airflow-webserver airflow db init

# Crear usuario admin de Airflow
docker-compose run --rm airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@techmart.local \
    --password admin123

# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 5. Verificar Despliegue

```bash
# Estado de contenedores
docker-compose ps

# Verificar Airflow
curl http://localhost:8080/health

# Verificar PostgreSQL
docker-compose exec postgres psql -U etl_user -d techmart -c "SELECT 1;"
```

## Despliegue en AWS

### Arquitectura en AWS

```
┌─────────────────────────────────────────────────────────────────┐
│                          VPC                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Private Subnet                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │    ECS      │  │    RDS      │  │   ElastiCache   │  │   │
│  │  │  Fargate    │  │  PostgreSQL │  │     Redis       │  │   │
│  │  │  (Airflow)  │  │             │  │                 │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │                    S3                            │    │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │    │   │
│  │  │  │  raw/    │  │ staging/ │  │  warehouse/  │  │    │   │
│  │  │  └──────────┘  └──────────┘  └──────────────┘  │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Public Subnet                          │   │
│  │  ┌─────────────┐                                        │   │
│  │  │     ALB     │                                        │   │
│  │  │ (Airflow UI)│                                        │   │
│  │  └─────────────┘                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Terraform (Ejemplo Simplificado)

```hcl
# main.tf
provider "aws" {
  region = "eu-west-1"
}

# RDS PostgreSQL
resource "aws_db_instance" "techmart_db" {
  identifier           = "techmart-postgres"
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.medium"
  allocated_storage    = 100
  storage_encrypted    = true

  db_name              = "techmart"
  username             = "etl_user"
  password             = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  skip_final_snapshot     = false
}

# S3 Bucket para Data Warehouse
resource "aws_s3_bucket" "warehouse" {
  bucket = "techmart-data-warehouse"
}

resource "aws_s3_bucket_versioning" "warehouse" {
  bucket = aws_s3_bucket.warehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

# ECS Cluster para Airflow
resource "aws_ecs_cluster" "airflow" {
  name = "techmart-airflow"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}
```

## Configuración de Airflow

### Variables

Configurar en Airflow UI (`Admin > Variables`):

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `techmart_api_url` | `https://api.techmart.com` | URL de la API |
| `warehouse_path` | `s3://techmart-warehouse` | Ruta del warehouse |

### Conexiones

Configurar en Airflow UI (`Admin > Connections`):

| Conn ID | Type | Host | Schema | Login | Password |
|---------|------|------|--------|-------|----------|
| `techmart_postgres` | Postgres | `rds-endpoint` | `techmart` | `etl_user` | `***` |
| `techmart_s3` | Amazon S3 | - | - | - | - (usar IAM Role) |

## Monitoreo

### Métricas Clave

| Métrica | Descripción | Umbral Alerta |
|---------|-------------|---------------|
| `dag_duration` | Duración total del DAG | > 30 min |
| `task_failures` | Tareas fallidas | > 0 |
| `records_processed` | Registros procesados | < 100 |
| `data_freshness` | Antigüedad de datos | > 24h |

### CloudWatch Dashboards

```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "title": "ETL Pipeline Duration",
        "metrics": [
          ["Airflow", "dag_duration", "dag_id", "daily_etl_techmart"]
        ]
      }
    },
    {
      "type": "metric",
      "properties": {
        "title": "Records Processed",
        "metrics": [
          ["TechMart", "records_processed", "pipeline", "etl"]
        ]
      }
    }
  ]
}
```

### Alertas

Configurar en CloudWatch Alarms o Airflow:

```python
# En el DAG
default_args = {
    'email': ['data-team@techmart.com'],
    'email_on_failure': True,
    'email_on_retry': True,
}
```

## Troubleshooting

### Problemas Comunes

#### 1. Fallo de Conexión a Base de Datos

**Síntoma**: `ConnectionError: Failed to connect to database`

**Solución**:
```bash
# Verificar conectividad
docker-compose exec airflow-worker nc -zv postgres 5432

# Verificar credenciales
docker-compose exec postgres psql -U etl_user -d techmart
```

#### 2. Timeout en API

**Síntoma**: `ConnectionError: API request timeout`

**Solución**:
- Aumentar timeout en configuración
- Verificar rate limiting
- Revisar logs de la API

#### 3. Memoria Insuficiente

**Síntoma**: `MemoryError` o contenedor OOMKilled

**Solución**:
```yaml
# docker-compose.yml
services:
  airflow-worker:
    deploy:
      resources:
        limits:
          memory: 4G
```

#### 4. DAG No Aparece

**Síntoma**: DAG no visible en Airflow UI

**Solución**:
```bash
# Verificar sintaxis
python dags/daily_etl_dag.py

# Verificar logs de parsing
docker-compose logs airflow-scheduler | grep "daily_etl"
```

### Logs Útiles

```bash
# Logs de Airflow
docker-compose logs -f airflow-scheduler
docker-compose logs -f airflow-worker

# Logs específicos de tarea
airflow tasks logs daily_etl_techmart extract_orders 2024-01-15
```

## Rollback

### Procedimiento

1. **Pausar DAG**:
   ```bash
   airflow dags pause daily_etl_techmart
   ```

2. **Restaurar versión anterior**:
   ```bash
   git checkout v1.0.0
   docker-compose build
   docker-compose up -d
   ```

3. **Restaurar datos si necesario**:
   ```bash
   # Desde backup de S3
   aws s3 cp s3://backups/warehouse/ ./data/warehouse/ --recursive
   ```

4. **Reactivar DAG**:
   ```bash
   airflow dags unpause daily_etl_techmart
   ```

## Contacto y Soporte

- **Equipo**: Data Engineering
- **Email**: data-team@techmart.local
- **Slack**: #data-engineering
- **On-call**: Rotación semanal (ver PagerDuty)

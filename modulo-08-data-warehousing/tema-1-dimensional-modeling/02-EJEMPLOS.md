# Ejemplos Prácticos: Modelado Dimensional

En este documento encontrarás ejemplos completos de modelado dimensional aplicados a casos de negocio reales. Cada ejemplo está trabajado paso a paso, desde el análisis de requisitos hasta el diseño final del modelo.

---

## Ejemplo 1: Star Schema para Restaurante - Nivel: Básico

### Contexto

Trabajas para **DataFlow Industries** y tu nuevo cliente es **RestaurantData Co.**, una cadena de 15 restaurantes en diferentes ciudades. El director de analytics necesita un data warehouse para responder preguntas como:

- ¿Cuáles son los platos más vendidos por restaurante?
- ¿Cuántas ventas se hicieron cada día de la semana?
- ¿Qué meseros tienen mejor desempeño en ventas?
- ¿Cuál es el ticket promedio por hora del día?

Actualmente, los datos vienen de una aplicación transaccional (PostgreSQL) con múltiples tablas normalizadas. Las consultas son lentas y complejas.

### Datos de Entrada (Sistema OLTP)

El sistema actual tiene estas tablas normalizadas:

```sql
-- Sistema transaccional actual
Ordenes (
    orden_id,
    fecha_hora,
    mesero_id,
    restaurante_id,
    mesa_num,
    total
)

DetalleOrden (
    detalle_id,
    orden_id,
    plato_id,
    cantidad,
    precio_unitario
)

Platos (
    plato_id,
    nombre,
    categoria_id,
    precio
)

Categorias (
    categoria_id,
    nombre_categoria
)

Restaurantes (
    restaurante_id,
    nombre,
    ciudad,
    region
)

Meseros (
    mesero_id,
    nombre,
    fecha_contratacion
)
```

**Problema**: Para saber las ventas totales por categoría de plato, necesitas hacer 4 joins:

```sql
SELECT
    c.nombre_categoria,
    SUM(d.cantidad * d.precio_unitario) as ventas_totales
FROM Ordenes o
JOIN DetalleOrden d ON o.orden_id = d.orden_id
JOIN Platos p ON d.plato_id = p.plato_id
JOIN Categorias c ON p.categoria_id = c.categoria_id
GROUP BY c.nombre_categoria;
```

Este query tarda 8-10 segundos con 500,000 órdenes.

### Paso 1: Identificar el Proceso de Negocio y el Grano

**Proceso de negocio**: Venta de platos en restaurantes

**Grano (granularidad)**: Cada fila representa **una línea de una orden** (un plato vendido en un ticket específico)

**Por qué este grano**: Necesitamos detalle al nivel de plato individual para responder todas las preguntas de negocio. Si guardamos solo totales por orden, perdemos la capacidad de analizar por plato.

### Paso 2: Identificar Dimensiones (Contexto)

**Preguntas del negocio nos dan las pistas**:
- ¿Cuáles son los platos más vendidos por **restaurante**? → DimRestaurante
- ¿Cuántas ventas se hicieron cada **día de la semana**? → DimFecha
- ¿**Qué** platos? → DimPlato
- ¿**Qué meseros**? → DimMesero

**Dimensiones identificadas**:
1. DimFecha (cuándo)
2. DimPlato (qué plato)
3. DimRestaurante (dónde)
4. DimMesero (quién vendió)

### Paso 3: Identificar Medidas (Métricas)

**¿Qué queremos sumar, promediar, contar?**
- Cantidad de platos vendidos
- Monto de la venta
- Costo del plato (para calcular margen)

**Medidas identificadas**:
- `cantidad`
- `monto_linea` (cantidad × precio)
- `costo_plato`
- `propina` (si se registra)

### Paso 4: Diseñar el Star Schema

```
                DimFecha
                    │
                    │
DimMesero ───┬─── FactVentas ───┬─── DimPlato
              │                  │
              │                  │
         DimRestaurante          │
                                 │
                            (opcional)
```

**Estructura detallada**:

#### FactVentas (Fact Table)

```sql
CREATE TABLE FactVentas (
    venta_id BIGINT PRIMARY KEY,
    fecha_id INT NOT NULL,             -- FK → DimFecha
    plato_id INT NOT NULL,             -- FK → DimPlato
    restaurante_id INT NOT NULL,       -- FK → DimRestaurante
    mesero_id INT NOT NULL,            -- FK → DimMesero

    -- Medidas (métricas)
    cantidad SMALLINT NOT NULL,
    monto_linea DECIMAL(10,2) NOT NULL,
    costo_plato DECIMAL(10,2),
    propina DECIMAL(10,2) DEFAULT 0,

    FOREIGN KEY (fecha_id) REFERENCES DimFecha(fecha_id),
    FOREIGN KEY (plato_id) REFERENCES DimPlato(plato_id),
    FOREIGN KEY (restaurante_id) REFERENCES DimRestaurante(restaurante_id),
    FOREIGN KEY (mesero_id) REFERENCES DimMesero(mesero_id)
);
```

#### DimFecha (Dimension)

```sql
CREATE TABLE DimFecha (
    fecha_id INT PRIMARY KEY,           -- Formato: 20240315
    fecha_completa DATE NOT NULL,
    dia INT NOT NULL,
    mes INT NOT NULL,
    mes_nombre VARCHAR(20),
    trimestre INT,
    anio INT NOT NULL,
    dia_semana VARCHAR(20),
    numero_dia_semana INT,              -- 1=Lunes, 7=Domingo
    numero_semana INT,
    es_fin_de_semana BOOLEAN,
    es_dia_festivo BOOLEAN,
    nombre_festivo VARCHAR(50)
);
```

#### DimPlato (Dimension)

```sql
CREATE TABLE DimPlato (
    plato_id INT PRIMARY KEY,
    nombre_plato VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),              -- Denormalizado: NO FK
    descripcion TEXT,
    precio_catalogo DECIMAL(10,2),
    es_vegetariano BOOLEAN,
    tiempo_preparacion_min INT,
    calorias INT
);
```

**Nota**: La categoría está denormalizada (incluida directamente en DimPlato), NO como FK a otra tabla. Esto es característico del star schema.

#### DimRestaurante (Dimension)

```sql
CREATE TABLE DimRestaurante (
    restaurante_id INT PRIMARY KEY,
    nombre_restaurante VARCHAR(100),
    direccion VARCHAR(200),
    ciudad VARCHAR(50),
    region VARCHAR(50),                 -- Centro, Norte, Sur
    codigo_postal VARCHAR(10),
    telefono VARCHAR(15),
    fecha_apertura DATE,
    capacidad_mesas INT,
    tiene_terraza BOOLEAN
);
```

#### DimMesero (Dimension - SCD Tipo 2)

```sql
CREATE TABLE DimMesero (
    mesero_id INT PRIMARY KEY,          -- Surrogate key
    mesero_key VARCHAR(20),             -- Natural key (ID de nómina)
    nombre_completo VARCHAR(100),
    nivel VARCHAR(20),                  -- Junior/Senior (puede cambiar)
    restaurante_asignado INT,           -- Puede cambiar
    fecha_contratacion DATE,

    -- Campos de SCD Tipo 2
    fecha_inicio_vigencia DATE NOT NULL,
    fecha_fin_vigencia DATE NOT NULL,   -- 9999-12-31 si es actual
    es_actual BOOLEAN NOT NULL,

    FOREIGN KEY (restaurante_asignado) REFERENCES DimRestaurante(restaurante_id)
);
```

**Por qué SCD Tipo 2 en DimMesero**: Si un mesero cambia de nivel (Junior → Senior) o es transferido a otro restaurante, queremos mantener historial para analizar su desempeño en cada etapa.

### Paso 5: Código Python para Generar Dimensión de Fecha

```python
"""
Generador de DimFecha para Data Warehouse.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict


def generar_dim_fecha(
    fecha_inicio: str,
    fecha_fin: str,
    festivos: List[Dict[str, str]] = None
) -> pd.DataFrame:
    """
    Genera tabla de dimensión de fecha pre-calculada.

    Args:
        fecha_inicio: Fecha inicial en formato 'YYYY-MM-DD'
        fecha_fin: Fecha final en formato 'YYYY-MM-DD'
        festivos: Lista de diccionarios con festivos
                  [{'fecha': '2024-01-01', 'nombre': 'Año Nuevo'}, ...]

    Returns:
        DataFrame con dimensión de fecha completa

    Examples:
        >>> dim_fecha = generar_dim_fecha('2024-01-01', '2024-12-31')
        >>> print(dim_fecha.head())
    """
    # Convertir fechas
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')

    # Generar rango de fechas
    fechas = pd.date_range(start=fecha_inicio_dt, end=fecha_fin_dt, freq='D')

    # Crear DataFrame base
    dim_fecha = pd.DataFrame({
        'fecha_completa': fechas
    })

    # Generar fecha_id (formato: YYYYMMDD)
    dim_fecha['fecha_id'] = dim_fecha['fecha_completa'].dt.strftime('%Y%m%d').astype(int)

    # Extraer componentes de fecha
    dim_fecha['dia'] = dim_fecha['fecha_completa'].dt.day
    dim_fecha['mes'] = dim_fecha['fecha_completa'].dt.month
    dim_fecha['anio'] = dim_fecha['fecha_completa'].dt.year

    # Nombres de mes en español
    meses_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    dim_fecha['mes_nombre'] = dim_fecha['mes'].map(meses_es)

    # Trimestre
    dim_fecha['trimestre'] = dim_fecha['fecha_completa'].dt.quarter

    # Día de semana
    dias_semana_es = {
        0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
        4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
    }
    dim_fecha['numero_dia_semana'] = dim_fecha['fecha_completa'].dt.dayofweek
    dim_fecha['dia_semana'] = dim_fecha['numero_dia_semana'].map(dias_semana_es)

    # Número de semana del año
    dim_fecha['numero_semana'] = dim_fecha['fecha_completa'].dt.isocalendar().week

    # Es fin de semana (Sábado=5, Domingo=6)
    dim_fecha['es_fin_de_semana'] = dim_fecha['numero_dia_semana'].isin([5, 6])

    # Días festivos
    dim_fecha['es_dia_festivo'] = False
    dim_fecha['nombre_festivo'] = None

    if festivos:
        for festivo in festivos:
            fecha_festivo = datetime.strptime(festivo['fecha'], '%Y-%m-%d')
            mask = dim_fecha['fecha_completa'] == fecha_festivo
            dim_fecha.loc[mask, 'es_dia_festivo'] = True
            dim_fecha.loc[mask, 'nombre_festivo'] = festivo['nombre']

    # Ordenar columnas
    dim_fecha = dim_fecha[[
        'fecha_id', 'fecha_completa', 'dia', 'mes', 'mes_nombre',
        'trimestre', 'anio', 'dia_semana', 'numero_dia_semana',
        'numero_semana', 'es_fin_de_semana', 'es_dia_festivo',
        'nombre_festivo'
    ]]

    return dim_fecha


# Ejemplo de uso
if __name__ == '__main__':
    # Definir festivos de México 2024
    festivos_2024 = [
        {'fecha': '2024-01-01', 'nombre': 'Año Nuevo'},
        {'fecha': '2024-02-05', 'nombre': 'Día de la Constitución'},
        {'fecha': '2024-03-18', 'nombre': 'Natalicio de Benito Juárez'},
        {'fecha': '2024-05-01', 'nombre': 'Día del Trabajo'},
        {'fecha': '2024-09-16', 'nombre': 'Independencia de México'},
        {'fecha': '2024-11-18', 'nombre': 'Revolución Mexicana'},
        {'fecha': '2024-12-25', 'nombre': 'Navidad'}
    ]

    # Generar dimensión de fecha para todo 2024
    dim_fecha = generar_dim_fecha('2024-01-01', '2024-12-31', festivos_2024)

    print("Dimensión de Fecha Generada:")
    print(f"Total de fechas: {len(dim_fecha)}")
    print("\nPrimeras 5 filas:")
    print(dim_fecha.head())
    print("\nDías festivos:")
    print(dim_fecha[dim_fecha['es_dia_festivo']][['fecha_completa', 'nombre_festivo']])

    # Guardar a CSV
    dim_fecha.to_csv('DimFecha_2024.csv', index=False, encoding='utf-8')
    print("\n✅ Archivo guardado: DimFecha_2024.csv")
```

### Resultado

```
Dimensión de Fecha Generada:
Total de fechas: 366

Primeras 5 filas:
   fecha_id fecha_completa  dia  mes mes_nombre  trimestre  anio dia_semana  \
0  20240101     2024-01-01    1    1      Enero          1  2024      Lunes
1  20240102     2024-01-02    2    1      Enero          1  2024     Martes
2  20240103     2024-01-03    3    1      Enero          1  2024  Miércoles
3  20240104     2024-01-04    4    1      Enero          1  2024     Jueves
4  20240105     2024-01-05    5    1      Enero          1  2024    Viernes

   numero_dia_semana  numero_semana  es_fin_de_semana  es_dia_festivo  \
0                  0              1             False            True
1                  1              1             False           False
2                  2              1             False           False
3                  3              1             False           False
4                  4              1             False           False

  nombre_festivo
0     Año Nuevo
1           None
2           None
3           None
4           None

Días festivos:
    fecha_completa    nombre_festivo
0       2024-01-01        Año Nuevo
36      2024-02-05  Día de la Constitución
77      2024-03-18  Natalicio de Benito Juárez
121     2024-05-01    Día del Trabajo
259     2024-09-16  Independencia de México
322     2024-11-18  Revolución Mexicana
359     2024-12-25          Navidad

✅ Archivo guardado: DimFecha_2024.csv
```

### Interpretación

**¿Qué logramos con este diseño?**

1. **Simplicidad de Queries**: Las consultas ahora requieren solo 1-2 joins en lugar de 4-5.

```sql
-- Query simplificado: Ventas por categoría
SELECT
    p.categoria,
    SUM(v.monto_linea) as ventas_totales,
    SUM(v.cantidad) as platos_vendidos
FROM FactVentas v
INNER JOIN DimPlato p ON v.plato_id = p.plato_id
GROUP BY p.categoria
ORDER BY ventas_totales DESC;
```

2. **Performance**: El query que antes tardaba 8-10 segundos ahora toma menos de 1 segundo.

3. **Análisis temporal fácil**: Con DimFecha pre-calculada, no necesitamos funciones complejas.

```sql
-- Ventas por día de semana (inmediato)
SELECT
    f.dia_semana,
    COUNT(DISTINCT v.venta_id) as num_ventas,
    SUM(v.monto_linea) as total_ventas
FROM FactVentas v
INNER JOIN DimFecha f ON v.fecha_id = f.fecha_id
WHERE f.anio = 2024 AND f.mes = 3
GROUP BY f.dia_semana, f.numero_dia_semana
ORDER BY f.numero_dia_semana;
```

4. **Histórico de meseros**: Con SCD Tipo 2, podemos analizar cómo cambia el desempeño cuando un mesero es promovido.

---

## Ejemplo 2: Implementar SCD Tipo 2 - Nivel: Intermedio

### Contexto

Trabajas para **FinTech Analytics**, una empresa que procesa pagos digitales. Tienen una dimensión de clientes donde la categoría del cliente cambia según su volumen de transacciones:

- **Bronce**: < $10,000 mensuales
- **Plata**: $10,000 - $50,000 mensuales
- **Oro**: > $50,000 mensuales

El director de riesgos quiere analizar:
- ¿Cómo cambia el comportamiento de compra cuando un cliente sube de categoría?
- ¿Cuántos clientes pasaron de Bronce a Oro en el último año?
- ¿Las transacciones históricas se deben ver con la categoría que tenían EN ESE MOMENTO?

**Solución**: Implementar SCD Tipo 2 en DimCliente para mantener historial de cambios de categoría.

### Datos Iniciales

**DimCliente (versión inicial - SCD Tipo 1)**:

```
cliente_id | nombre      | email              | categoria | fecha_registro
1          | Ana López   | ana@email.com      | Oro       | 2023-01-15
2          | Luis Pérez  | luis@email.com     | Plata     | 2023-03-20
3          | Carmen Ruiz | carmen@email.com   | Bronce    | 2023-05-10
```

**Problema**: Si Ana era "Bronce" en 2023 y ahora es "Oro", hemos perdido ese historial.

### Paso 1: Rediseñar DimCliente con SCD Tipo 2

**Nueva estructura**:

```sql
CREATE TABLE DimCliente (
    cliente_id INT PRIMARY KEY,          -- Surrogate key (autoincremental)
    cliente_key VARCHAR(50) NOT NULL,    -- Natural key (no cambia, ej: RFC o email)
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    categoria VARCHAR(20) NOT NULL,      -- El atributo que cambia
    limite_credito DECIMAL(10,2),

    -- Campos de SCD Tipo 2
    fecha_inicio_vigencia DATE NOT NULL,
    fecha_fin_vigencia DATE NOT NULL,    -- 9999-12-31 indica versión actual
    es_actual BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_cliente_key ON DimCliente(cliente_key, es_actual);
CREATE INDEX idx_vigencia ON DimCliente(fecha_inicio_vigencia, fecha_fin_vigencia);
```

### Paso 2: Cargar Datos Históricos

```python
"""
Implementación de SCD Tipo 2 para DimCliente.
"""
import pandas as pd
from datetime import datetime, date
from typing import Dict, List


class SCDTipo2Manager:
    """Gestiona actualizaciones de dimensiones con SCD Tipo 2."""

    def __init__(self):
        self.dim_cliente = pd.DataFrame(columns=[
            'cliente_id', 'cliente_key', 'nombre', 'email', 'categoria',
            'limite_credito', 'fecha_inicio_vigencia', 'fecha_fin_vigencia',
            'es_actual'
        ])
        self.next_id = 1

    def insertar_nuevo_cliente(
        self,
        cliente_key: str,
        nombre: str,
        email: str,
        categoria: str,
        limite_credito: float,
        fecha_vigencia: date
    ) -> int:
        """
        Inserta un nuevo cliente en la dimensión.

        Args:
            cliente_key: Identificador único del cliente (natural key)
            nombre: Nombre completo
            email: Email
            categoria: Bronce/Plata/Oro
            limite_credito: Límite de crédito asignado
            fecha_vigencia: Fecha desde la cual es vigente

        Returns:
            cliente_id generado (surrogate key)
        """
        nuevo_registro = {
            'cliente_id': self.next_id,
            'cliente_key': cliente_key,
            'nombre': nombre,
            'email': email,
            'categoria': categoria,
            'limite_credito': limite_credito,
            'fecha_inicio_vigencia': fecha_vigencia,
            'fecha_fin_vigencia': date(9999, 12, 31),  # Versión actual
            'es_actual': True
        }

        self.dim_cliente = pd.concat([
            self.dim_cliente,
            pd.DataFrame([nuevo_registro])
        ], ignore_index=True)

        cliente_id = self.next_id
        self.next_id += 1

        print(f"✅ Cliente nuevo insertado: {nombre} (ID: {cliente_id})")
        return cliente_id

    def actualizar_categoria(
        self,
        cliente_key: str,
        nueva_categoria: str,
        nuevo_limite: float,
        fecha_cambio: date
    ) -> None:
        """
        Actualiza la categoría de un cliente usando SCD Tipo 2.

        Proceso:
        1. Buscar la versión actual del cliente
        2. Cerrar esa versión (fecha_fin_vigencia = fecha_cambio - 1 día)
        3. Insertar nueva versión con nueva categoría

        Args:
            cliente_key: Natural key del cliente
            nueva_categoria: Nueva categoría (Bronce/Plata/Oro)
            nuevo_limite: Nuevo límite de crédito
            fecha_cambio: Fecha desde la cual aplica el cambio
        """
        # 1. Buscar versión actual
        mask_actual = (
            (self.dim_cliente['cliente_key'] == cliente_key) &
            (self.dim_cliente['es_actual'] == True)
        )

        if not mask_actual.any():
            raise ValueError(f"Cliente {cliente_key} no encontrado")

        # Obtener datos actuales
        cliente_actual = self.dim_cliente[mask_actual].iloc[0]

        # Verificar si realmente cambió la categoría
        if cliente_actual['categoria'] == nueva_categoria:
            print(f"⚠️  La categoría no cambió, no se genera nueva versión")
            return

        # 2. Cerrar versión actual
        fecha_fin = fecha_cambio - pd.Timedelta(days=1)
        self.dim_cliente.loc[mask_actual, 'fecha_fin_vigencia'] = fecha_fin.date()
        self.dim_cliente.loc[mask_actual, 'es_actual'] = False

        print(f"📝 Versión anterior cerrada (vigente hasta {fecha_fin.date()})")

        # 3. Insertar nueva versión
        nueva_version = {
            'cliente_id': self.next_id,
            'cliente_key': cliente_key,
            'nombre': cliente_actual['nombre'],
            'email': cliente_actual['email'],
            'categoria': nueva_categoria,
            'limite_credito': nuevo_limite,
            'fecha_inicio_vigencia': fecha_cambio,
            'fecha_fin_vigencia': date(9999, 12, 31),
            'es_actual': True
        }

        self.dim_cliente = pd.concat([
            self.dim_cliente,
            pd.DataFrame([nueva_version])
        ], ignore_index=True)

        self.next_id += 1

        print(f"✅ Nueva versión creada: {cliente_actual['categoria']} → {nueva_categoria}")

    def obtener_cliente_actual(self, cliente_key: str) -> pd.Series:
        """Obtiene la versión actual de un cliente."""
        mask = (
            (self.dim_cliente['cliente_key'] == cliente_key) &
            (self.dim_cliente['es_actual'] == True)
        )
        return self.dim_cliente[mask].iloc[0]

    def obtener_historial(self, cliente_key: str) -> pd.DataFrame:
        """Obtiene todo el historial de un cliente."""
        return self.dim_cliente[
            self.dim_cliente['cliente_key'] == cliente_key
        ].sort_values('fecha_inicio_vigencia')


# Ejemplo de uso: Simular evolución de un cliente
if __name__ == '__main__':
    scd = SCDTipo2Manager()

    # --- Enero 2023: Cliente nuevo ---
    print("\n=== ENERO 2023: Cliente nuevo ===")
    scd.insertar_nuevo_cliente(
        cliente_key='CLI001',
        nombre='Ana López Martínez',
        email='ana.lopez@email.com',
        categoria='Bronce',
        limite_credito=5000.00,
        fecha_vigencia=date(2023, 1, 15)
    )

    # --- Junio 2023: Sube a Plata ---
    print("\n=== JUNIO 2023: Cliente sube a Plata ===")
    scd.actualizar_categoria(
        cliente_key='CLI001',
        nueva_categoria='Plata',
        nuevo_limite=25000.00,
        fecha_cambio=date(2023, 6, 1)
    )

    # --- Enero 2024: Sube a Oro ---
    print("\n=== ENERO 2024: Cliente sube a Oro ===")
    scd.actualizar_categoria(
        cliente_key='CLI001',
        nueva_categoria='Oro',
        nuevo_limite=100000.00,
        fecha_cambio=date(2024, 1, 1)
    )

    # Mostrar historial completo
    print("\n=== HISTORIAL COMPLETO DE CLI001 ===")
    historial = scd.obtener_historial('CLI001')
    print(historial.to_string(index=False))

    # Verificación: ¿Qué categoría tenía el cliente el 15 de agosto de 2023?
    print("\n=== CONSULTA HISTÓRICA: ¿Categoría el 15 de agosto de 2023? ===")
    fecha_consulta = date(2023, 8, 15)

    mask_vigente = (
        (historial['cliente_key'] == 'CLI001') &
        (historial['fecha_inicio_vigencia'] <= fecha_consulta) &
        (historial['fecha_fin_vigencia'] >= fecha_consulta)
    )

    version_vigente = historial[mask_vigente].iloc[0]
    print(f"En {fecha_consulta}, Ana López era: {version_vigente['categoria']}")
    print(f"Con límite de crédito: ${version_vigente['limite_credito']:,.2f}")
```

### Resultado

```
=== ENERO 2023: Cliente nuevo ===
✅ Cliente nuevo insertado: Ana López Martínez (ID: 1)

=== JUNIO 2023: Cliente sube a Plata ===
📝 Versión anterior cerrada (vigente hasta 2023-05-31)
✅ Nueva versión creada: Bronce → Plata

=== ENERO 2024: Cliente sube a Oro ===
📝 Versión anterior cerrada (vigente hasta 2023-12-31)
✅ Nueva versión creada: Plata → Oro

=== HISTORIAL COMPLETO DE CLI001 ===
 cliente_id cliente_key                nombre                email categoria  limite_credito fecha_inicio_vigencia fecha_fin_vigencia  es_actual
          1      CLI001  Ana López Martínez  ana.lopez@email.com    Bronce          5000.0            2023-01-15         2023-05-31      False
          2      CLI001  Ana López Martínez  ana.lopez@email.com     Plata         25000.0            2023-06-01         2023-12-31      False
          3      CLI001  Ana López Martínez  ana.lopez@email.com       Oro        100000.0            2024-01-01         9999-12-31       True

=== CONSULTA HISTÓRICA: ¿Categoría el 15 de agosto de 2023? ===
En 2023-08-15, Ana López era: Plata
Con límite de crédito: $25,000.00
```

### Interpretación

**¿Qué logramos con SCD Tipo 2?**

1. **Historial completo**: Tenemos 3 versiones del mismo cliente, cada una con fechas de vigencia claras.

2. **Consultas históricas precisas**: Podemos saber EXACTAMENTE qué categoría tenía el cliente en cualquier fecha pasada.

3. **Análisis de tendencias**:

```sql
-- ¿Cuántos clientes pasaron de Bronce a Oro directamente?
SELECT COUNT(DISTINCT cliente_key)
FROM DimCliente
WHERE cliente_key IN (
    SELECT cliente_key
    FROM DimCliente
    WHERE categoria = 'Bronce'
)
AND cliente_key IN (
    SELECT cliente_key
    FROM DimCliente
    WHERE categoria = 'Oro'
)
AND cliente_key NOT IN (
    SELECT cliente_key
    FROM DimCliente
    WHERE categoria = 'Plata'
);
```

4. **Join correcto con FactTransacciones**:

```sql
-- Ventas con la categoría que tenía el cliente EN ESE MOMENTO
SELECT
    c.categoria,
    SUM(t.monto) as ventas_totales
FROM FactTransacciones t
INNER JOIN DimCliente c ON t.cliente_id = c.cliente_id
INNER JOIN DimFecha f ON t.fecha_id = f.fecha_id
WHERE f.fecha_completa BETWEEN c.fecha_inicio_vigencia AND c.fecha_fin_vigencia
GROUP BY c.categoria;
```

**Trade-off**: La tabla DimCliente crece con el tiempo. Si tienes 100,000 clientes y cada uno cambia de categoría 2 veces, tendrás 300,000 filas. Esto es ACEPTABLE en data warehousing si necesitas historial.

---

## Ejemplo 3: Star vs. Snowflake Schema - Nivel: Intermedio

### Contexto

Trabajas para **LogisticFlow**, una empresa de envíos. El director de operaciones quiere analizar eficiencia de rutas, pero la estructura geográfica es compleja:

```
País → Estado → Ciudad → Zona
```

**Pregunta de diseño**: ¿Usamos Star Schema (denormalizado) o Snowflake Schema (normalizado)?

### Opción 1: Star Schema (Denormalizado)

```sql
CREATE TABLE DimUbicacion (
    ubicacion_id INT PRIMARY KEY,
    nombre_zona VARCHAR(100),
    codigo_postal VARCHAR(10),
    ciudad VARCHAR(50),
    estado VARCHAR(50),
    region VARCHAR(50),           -- Norte, Centro, Sur
    pais VARCHAR(50),
    latitud DECIMAL(10, 7),
    longitud DECIMAL(10, 7)
);
```

**Características**:
- TODO en una tabla
- Mucha redundancia (el mismo estado/país se repite miles de veces)
- Queries MUY rápidos (1 solo join)

**Ejemplo de datos**:

```
ubicacion_id | nombre_zona    | ciudad           | estado      | region | pais
1            | Centro CDMX    | Ciudad de México | CDMX        | Centro | México
2            | Polanco        | Ciudad de México | CDMX        | Centro | México
3            | Roma Norte     | Ciudad de México | CDMX        | Centro | México
4            | Monterrey Ctr  | Monterrey        | Nuevo León  | Norte  | México
```

**Nota**: "Centro" y "México" se repiten en cada fila.

**Query ejemplo**:

```sql
-- Entregas por región (1 JOIN)
SELECT
    u.region,
    COUNT(e.entrega_id) as total_entregas,
    AVG(e.tiempo_entrega_min) as tiempo_promedio
FROM FactEntregas e
INNER JOIN DimUbicacion u ON e.ubicacion_destino_id = u.ubicacion_id
GROUP BY u.region;
```

### Opción 2: Snowflake Schema (Normalizado)

```sql
-- Nivel 1: Zona
CREATE TABLE DimZona (
    zona_id INT PRIMARY KEY,
    nombre_zona VARCHAR(100),
    codigo_postal VARCHAR(10),
    ciudad_id INT NOT NULL,
    FOREIGN KEY (ciudad_id) REFERENCES DimCiudad(ciudad_id)
);

-- Nivel 2: Ciudad
CREATE TABLE DimCiudad (
    ciudad_id INT PRIMARY KEY,
    nombre_ciudad VARCHAR(50),
    estado_id INT NOT NULL,
    FOREIGN KEY (estado_id) REFERENCES DimEstado(estado_id)
);

-- Nivel 3: Estado
CREATE TABLE DimEstado (
    estado_id INT PRIMARY KEY,
    nombre_estado VARCHAR(50),
    region VARCHAR(50),
    pais_id INT NOT NULL,
    FOREIGN KEY (pais_id) REFERENCES DimPais(pais_id)
);

-- Nivel 4: País
CREATE TABLE DimPais (
    pais_id INT PRIMARY KEY,
    nombre_pais VARCHAR(50),
    codigo_iso VARCHAR(3)
);
```

**Características**:
- Jerarquía normalizada en 4 tablas
- SIN redundancia
- Queries más complejos (4 joins)

**Query ejemplo**:

```sql
-- Entregas por región (4 JOINS)
SELECT
    es.region,
    COUNT(e.entrega_id) as total_entregas,
    AVG(e.tiempo_entrega_min) as tiempo_promedio
FROM FactEntregas e
INNER JOIN DimZona z ON e.ubicacion_destino_id = z.zona_id
INNER JOIN DimCiudad c ON z.ciudad_id = c.ciudad_id
INNER JOIN DimEstado es ON c.estado_id = es.estado_id
INNER JOIN DimPais p ON es.pais_id = p.pais_id
GROUP BY es.region;
```

### Comparación con Datos Reales

**Escenario**: 50,000 zonas de entrega en México

#### Star Schema

```python
# Calcular tamaño de Star Schema
zonas = 50000
bytes_por_fila = (
    100 +  # nombre_zona
    10 +   # codigo_postal
    50 +   # ciudad
    50 +   # estado
    50 +   # region (REPETIDO miles de veces)
    50 +   # pais (REPETIDO 50,000 veces = "México")
    8 +    # latitud
    8      # longitud
)

tamaño_mb = (zonas * bytes_por_fila) / (1024 * 1024)
print(f"Star Schema: {tamaño_mb:.2f} MB")
# Output: Star Schema: 15.56 MB
```

#### Snowflake Schema

```python
# Snowflake Schema
zonas = 50000          # DimZona
ciudades = 2500        # DimCiudad (México tiene ~2,500 ciudades)
estados = 32           # DimEstado (México tiene 32 estados)
paises = 1             # DimPais (solo México)

bytes_zona = 100 + 10 + 4  # nombre, codigo, ciudad_id
bytes_ciudad = 50 + 4      # nombre, estado_id
bytes_estado = 50 + 50 + 4 # nombre, region, pais_id
bytes_pais = 50 + 3        # nombre, iso

tamaño_mb = (
    (zonas * bytes_zona) +
    (ciudades * bytes_ciudad) +
    (estados * bytes_estado) +
    (paises * bytes_pais)
) / (1024 * 1024)

print(f"Snowflake Schema: {tamaño_mb:.2f} MB")
# Output: Snowflake Schema: 5.48 MB
```

**Ahorro de espacio**: Snowflake usa ~65% menos espacio.

### Benchmark de Performance

```python
import time
import psycopg2

# Simular queries en ambos esquemas
def benchmark_star_schema(conn):
    """Medir tiempo en Star Schema."""
    start = time.time()

    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            u.region,
            COUNT(e.entrega_id) as total_entregas
        FROM FactEntregas e
        INNER JOIN DimUbicacion u ON e.ubicacion_destino_id = u.ubicacion_id
        GROUP BY u.region
    """)
    result = cursor.fetchall()

    elapsed = time.time() - start
    return elapsed

def benchmark_snowflake_schema(conn):
    """Medir tiempo en Snowflake Schema."""
    start = time.time()

    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            es.region,
            COUNT(e.entrega_id) as total_entregas
        FROM FactEntregas e
        INNER JOIN DimZona z ON e.ubicacion_destino_id = z.zona_id
        INNER JOIN DimCiudad c ON z.ciudad_id = c.ciudad_id
        INNER JOIN DimEstado es ON c.estado_id = es.estado_id
        GROUP BY es.region
    """)
    result = cursor.fetchall()

    elapsed = time.time() - start
    return elapsed

# Resultados con 1 millón de entregas
"""
Star Schema:     0.23 segundos
Snowflake:       0.41 segundos

Diferencia: Snowflake es ~78% más lento
"""
```

### Interpretación: ¿Cuál usar?

| Criterio | Star Schema | Snowflake Schema |
|----------|-------------|------------------|
| **Performance** | ⭐⭐⭐⭐⭐ 0.23s | ⭐⭐⭐ 0.41s |
| **Espacio** | ⭐⭐⭐ 15.56 MB | ⭐⭐⭐⭐⭐ 5.48 MB (65% menos) |
| **Simplicidad queries** | ⭐⭐⭐⭐⭐ 1 join | ⭐⭐ 4 joins |
| **Mantenibilidad** | ⭐⭐⭐ Cambios en toda la tabla | ⭐⭐⭐⭐⭐ Cambios localizados |
| **Integridad** | ⭐⭐⭐ Puede haber inconsistencias | ⭐⭐⭐⭐⭐ Garantizada por FKs |

**Recomendación para LogisticFlow**:

**Usar Star Schema** porque:
- El ahorro de espacio (10 MB) es trivial en 2024
- La diferencia de performance (0.18s) se multiplica en dashboards con 50 queries/minuto
- Analistas de negocio pueden escribir queries sin ayuda de IT
- Cloud storage es barato (S3, Blob Storage)

**Usar Snowflake solo si**:
- Restricciones severas de almacenamiento
- Jerarquías cambian constantemente (nuevos estados, regiones)
- Necesitas integridad referencial estricta por regulación

---

## Ejemplo 4: Data Warehouse Completo para E-commerce - Nivel: Avanzado

### Contexto

Has sido contratado por **MercadoDigital**, un e-commerce que vende productos de múltiples vendedores (tipo Mercado Libre). Necesitan un data warehouse completo para:

- Análisis de ventas
- Comportamiento de clientes
- Desempeño de vendedores
- Logística y entregas
- Devoluciones y calidad

**Complejidad**: Múltiples procesos de negocio = múltiples fact tables.

### Paso 1: Identificar Procesos de Negocio

**Procesos principales**:
1. **Ventas**: Compras de productos
2. **Inventario**: Stock de productos por bodega
3. **Envíos**: Entregas y logística
4. **Devoluciones**: Productos devueltos

Cada proceso tendrá su propia fact table.

### Paso 2: Diseñar el Modelo Dimensional

#### Dimensiones Conformadas (shared)

Estas dimensiones se comparten entre múltiples fact tables:

```sql
-- DimFecha (compartida entre todas las facts)
CREATE TABLE DimFecha (
    fecha_id INT PRIMARY KEY,
    fecha_completa DATE,
    dia INT,
    mes INT,
    anio INT,
    trimestre INT,
    dia_semana VARCHAR(20),
    es_fin_de_semana BOOLEAN,
    es_dia_festivo BOOLEAN
);

-- DimProducto (compartida)
CREATE TABLE DimProducto (
    producto_id INT PRIMARY KEY,
    sku VARCHAR(50),
    nombre_producto VARCHAR(200),
    marca VARCHAR(100),
    categoria VARCHAR(50),
    subcategoria VARCHAR(50),
    precio_catalogo DECIMAL(10,2),
    peso_kg DECIMAL(6,2),
    requiere_refrigeracion BOOLEAN
);

-- DimCliente (compartida, SCD Tipo 2)
CREATE TABLE DimCliente (
    cliente_id INT PRIMARY KEY,
    cliente_key VARCHAR(50),
    nombre VARCHAR(100),
    email VARCHAR(100),
    segmento VARCHAR(20),          -- Básico/Premium/VIP (puede cambiar)
    ciudad VARCHAR(50),
    estado VARCHAR(50),
    fecha_inicio_vigencia DATE,
    fecha_fin_vigencia DATE,
    es_actual BOOLEAN
);

-- DimVendedor (compartida, SCD Tipo 2)
CREATE TABLE DimVendedor (
    vendedor_id INT PRIMARY KEY,
    vendedor_key VARCHAR(50),
    nombre_vendedor VARCHAR(100),
    tipo VARCHAR(20),              -- Individual/Empresa
    calificacion_promedio DECIMAL(3,2),
    fecha_inicio_vigencia DATE,
    fecha_fin_vigencia DATE,
    es_actual BOOLEAN
);
```

#### Fact Table 1: FactVentas

```sql
CREATE TABLE FactVentas (
    venta_id BIGINT PRIMARY KEY,
    fecha_orden_id INT NOT NULL,
    fecha_pago_id INT,
    producto_id INT NOT NULL,
    cliente_id INT NOT NULL,
    vendedor_id INT NOT NULL,

    -- Medidas
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2),
    descuento DECIMAL(10,2) DEFAULT 0,
    impuestos DECIMAL(10,2),
    monto_total DECIMAL(10,2),
    comision_vendedor DECIMAL(10,2),
    costo_producto DECIMAL(10,2),

    -- Métricas derivadas (se pueden calcular)
    margen_bruto DECIMAL(10,2),

    FOREIGN KEY (fecha_orden_id) REFERENCES DimFecha(fecha_id),
    FOREIGN KEY (producto_id) REFERENCES DimProducto(producto_id),
    FOREIGN KEY (cliente_id) REFERENCES DimCliente(cliente_id),
    FOREIGN KEY (vendedor_id) REFERENCES DimVendedor(vendedor_id)
);
```

#### Fact Table 2: FactInventario (Snapshot Fact)

```sql
CREATE TABLE FactInventario (
    inventario_id BIGINT PRIMARY KEY,
    fecha_snapshot_id INT NOT NULL,    -- Foto diaria del inventario
    producto_id INT NOT NULL,
    bodega_id INT NOT NULL,

    -- Medidas
    cantidad_disponible INT,
    cantidad_reservada INT,
    cantidad_en_transito INT,
    costo_unitario_promedio DECIMAL(10,2),
    valor_total_inventario DECIMAL(12,2),

    FOREIGN KEY (fecha_snapshot_id) REFERENCES DimFecha(fecha_id),
    FOREIGN KEY (producto_id) REFERENCES DimProducto(producto_id),
    FOREIGN KEY (bodega_id) REFERENCES DimBodega(bodega_id)
);
```

**Nota**: Esta es una **snapshot fact table** porque registra el ESTADO del inventario en un momento específico (diario), no transacciones individuales.

#### Fact Table 3: FactEnvios

```sql
CREATE TABLE FactEnvios (
    envio_id BIGINT PRIMARY KEY,
    venta_id BIGINT NOT NULL,          -- FK a FactVentas
    fecha_envio_id INT,
    fecha_entrega_id INT,
    producto_id INT NOT NULL,
    transportista_id INT,
    ubicacion_origen_id INT,
    ubicacion_destino_id INT,

    -- Medidas
    peso_kg DECIMAL(6,2),
    distancia_km INT,
    costo_envio DECIMAL(10,2),
    tiempo_entrega_dias INT,
    fue_entregado_a_tiempo BOOLEAN,
    calificacion_entrega SMALLINT,     -- 1-5 estrellas

    FOREIGN KEY (venta_id) REFERENCES FactVentas(venta_id),
    FOREIGN KEY (producto_id) REFERENCES DimProducto(producto_id)
);
```

#### Fact Table 4: FactDevoluciones

```sql
CREATE TABLE FactDevoluciones (
    devolucion_id BIGINT PRIMARY KEY,
    venta_id BIGINT NOT NULL,          -- FK a FactVentas
    fecha_solicitud_id INT,
    fecha_aprobacion_id INT,
    producto_id INT NOT NULL,
    motivo_id INT,

    -- Medidas
    cantidad_devuelta INT,
    monto_reembolsado DECIMAL(10,2),
    costo_procesamiento DECIMAL(10,2),
    fue_aprobada BOOLEAN,
    tiempo_procesamiento_dias INT,

    FOREIGN KEY (venta_id) REFERENCES FactVentas(venta_id),
    FOREIGN KEY (producto_id) REFERENCES DimProducto(producto_id),
    FOREIGN KEY (motivo_id) REFERENCES DimMotivoDevolucion(motivo_id)
);
```

### Paso 3: Diagrama del Modelo Completo

```
                    DimFecha
                       │
          ┌────────────┼────────────┐
          │            │            │
      FactVentas   FactInventario FactEnvios
          │            │            │
     ┌────┼────┐       │       ┌────┼────┐
     │    │    │       │       │    │    │
DimCliente │ DimVendedor │  DimBodega  DimTransportista
     DimProducto ────────┼────────┼──────────┘
                         │        │
                    FactDevoluciones
```

### Paso 4: Queries Analíticos Complejos

```sql
-- 1. Análisis de ventas cruzado con devoluciones
SELECT
    p.categoria,
    COUNT(DISTINCT v.venta_id) as total_ventas,
    COUNT(DISTINCT d.devolucion_id) as total_devoluciones,
    ROUND(100.0 * COUNT(DISTINCT d.devolucion_id) / COUNT(DISTINCT v.venta_id), 2) as tasa_devolucion_pct,
    SUM(v.monto_total) as ingresos,
    SUM(d.monto_reembolsado) as reembolsos,
    SUM(v.monto_total) - COALESCE(SUM(d.monto_reembolsado), 0) as ingresos_netos
FROM FactVentas v
LEFT JOIN FactDevoluciones d ON v.venta_id = d.venta_id AND d.fue_aprobada = TRUE
INNER JOIN DimProducto p ON v.producto_id = p.producto_id
INNER JOIN DimFecha f ON v.fecha_orden_id = f.fecha_id
WHERE f.anio = 2024 AND f.trimestre = 1
GROUP BY p.categoria
ORDER BY tasa_devolucion_pct DESC;

-- 2. Análisis de eficiencia logística por vendedor
SELECT
    vend.nombre_vendedor,
    COUNT(e.envio_id) as total_envios,
    AVG(e.tiempo_entrega_dias) as tiempo_promedio_dias,
    SUM(CASE WHEN e.fue_entregado_a_tiempo THEN 1 ELSE 0 END) * 100.0 / COUNT(e.envio_id) as pct_a_tiempo,
    AVG(e.calificacion_entrega) as calificacion_promedio,
    SUM(e.costo_envio) as costo_total_logistica
FROM FactEnvios e
INNER JOIN FactVentas v ON e.venta_id = v.venta_id
INNER JOIN DimVendedor vend ON v.vendedor_id = vend.vendedor_id
WHERE vend.es_actual = TRUE
GROUP BY vend.nombre_vendedor
HAVING COUNT(e.envio_id) > 100
ORDER BY pct_a_tiempo DESC, calificacion_promedio DESC
LIMIT 10;

-- 3. Análisis de rotación de inventario
WITH ventas_por_producto AS (
    SELECT
        producto_id,
        SUM(cantidad) as unidades_vendidas
    FROM FactVentas
    WHERE fecha_orden_id BETWEEN 20240101 AND 20240131
    GROUP BY producto_id
),
inventario_promedio AS (
    SELECT
        producto_id,
        AVG(cantidad_disponible) as stock_promedio
    FROM FactInventario
    WHERE fecha_snapshot_id BETWEEN 20240101 AND 20240131
    GROUP BY producto_id
)
SELECT
    p.nombre_producto,
    p.categoria,
    v.unidades_vendidas,
    i.stock_promedio,
    ROUND(v.unidades_vendidas / NULLIF(i.stock_promedio, 0), 2) as rotacion_inventario
FROM ventas_por_producto v
INNER JOIN inventario_promedio i ON v.producto_id = i.producto_id
INNER JOIN DimProducto p ON v.producto_id = p.producto_id
WHERE i.stock_promedio > 0
ORDER BY rotacion_inventario DESC
LIMIT 20;
```

### Interpretación

**¿Qué logramos con este diseño de constelación de facts?**

1. **Separación de procesos**: Cada proceso de negocio tiene su fact table dedicada, con su propio grano.

2. **Dimensiones conformadas**: DimProducto, DimFecha, DimCliente se comparten entre facts, permitiendo análisis cruzados.

3. **Drill-across queries**: Podemos combinar métricas de diferentes facts (ventas + devoluciones + inventario) usando las dimensiones conformadas.

4. **Escalabilidad**: Cada fact table crece independientemente según su proceso.

5. **Flexibilidad analítica**: Podemos responder preguntas complejas que cruzan múltiples áreas del negocio.

---

## Resumen de Ejemplos

| Ejemplo | Concepto Principal | Nivel | Empresa Ficticia |
|---------|-------------------|-------|------------------|
| 1 | Star Schema básico | Básico | RestaurantData Co. |
| 2 | SCD Tipo 2 | Intermedio | FinTech Analytics |
| 3 | Star vs. Snowflake | Intermedio | LogisticFlow |
| 4 | Constelación de Facts | Avanzado | MercadoDigital |

**Próximos pasos**: En el documento de ejercicios (03-EJERCICIOS.md), aplicarás estos conceptos diseñando tus propios modelos dimensionales desde cero.

---

**Tiempo estimado**: 50-60 minutos de lectura y práctica
**Prerequisitos**: Haber leído 01-TEORIA.md, conocimientos de SQL
**Herramientas**: Python 3.11+, pandas, SQL (PostgreSQL/MySQL)

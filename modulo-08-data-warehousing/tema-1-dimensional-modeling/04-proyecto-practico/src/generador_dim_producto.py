"""
Generador de Dimensión de Producto (DimProducto).

Este módulo genera un catálogo de productos sintéticos con atributos
denormalizados siguiendo el patrón Star Schema.

Funciones:
    generar_dim_producto: Genera catálogo de productos
    asignar_categoria: Asigna categoría/subcategoría según nombre
"""

import random

import pandas as pd
from faker import Faker


def asignar_categoria(nombre_producto: str) -> tuple[str, str]:
    """
    Asigna categoría y subcategoría según el nombre del producto.

    Args:
        nombre_producto: Nombre del producto

    Returns:
        Tupla (categoria, subcategoria)

    Examples:
        >>> asignar_categoria("Laptop Dell Inspiron 15")
        ('Electrónica', 'Computadoras')

        >>> asignar_categoria("Camisa Polo Azul")
        ('Ropa', ...)
    """
    nombre_lower = nombre_producto.lower()

    # Electrónica
    if any(
        keyword in nombre_lower
        for keyword in ["laptop", "computadora", "pc", "macbook"]
    ):
        return ("Electrónica", "Computadoras")
    elif any(
        keyword in nombre_lower
        for keyword in ["iphone", "samsung", "celular", "teléfono", "smartphone"]
    ):
        return ("Electrónica", "Celulares")
    elif any(
        keyword in nombre_lower
        for keyword in ["audífonos", "mouse", "teclado", "monitor", "cable"]
    ):
        return ("Electrónica", "Accesorios")

    # Ropa
    elif any(
        keyword in nombre_lower
        for keyword in ["camisa", "polo", "playera", "blusa", "pantalón", "jeans"]
    ):
        return ("Ropa", "Casual")
    elif any(keyword in nombre_lower for keyword in ["zapatos", "tenis", "botas"]):
        return ("Ropa", "Calzado")

    # Hogar
    elif any(
        keyword in nombre_lower
        for keyword in ["sartén", "olla", "licuadora", "cafetera"]
    ):
        return ("Hogar", "Cocina")
    elif any(keyword in nombre_lower for keyword in ["lámpara", "espejo", "cuadro"]):
        return ("Hogar", "Decoración")

    # Deportes
    elif any(
        keyword in nombre_lower for keyword in ["balón", "pelota", "raqueta", "pesas"]
    ):
        return ("Deportes", "Equipamiento")

    # Libros
    elif any(
        keyword in nombre_lower
        for keyword in [
            "libro",
            "novela",
            "cien años",
            "harry potter",
            "señor de los anillos",
        ]
    ):
        return ("Libros", "Ficción")

    # Default
    else:
        return ("General", "Otros")


def generar_dim_producto(num_productos: int) -> pd.DataFrame:  # noqa: C901
    """
    Genera catálogo de productos sintéticos.

    Args:
        num_productos: Cantidad de productos a generar

    Returns:
        DataFrame con DimProducto con columnas:
            - producto_id (int): ID único
            - sku (str): Stock Keeping Unit único
            - nombre_producto (str): Nombre del producto
            - marca (str): Marca del producto
            - categoria (str): Categoría (denormalizada)
            - subcategoria (str): Subcategoría (denormalizada)
            - precio_catalogo (float): Precio de catálogo
            - peso_kg (float): Peso en kilogramos
            - requiere_refrigeracion (bool): Si requiere refrigeración

    Raises:
        ValueError: Si num_productos <= 0

    Examples:
        >>> productos = generar_dim_producto(100)
        >>> print(productos.shape)
        (100, 9)

        >>> print(productos['categoria'].unique())
        ['Electrónica' 'Ropa' 'Hogar' 'Deportes' 'Libros']
    """
    if num_productos <= 0:
        raise ValueError(
            f"num_productos debe ser mayor que 0. Recibido: {num_productos}"
        )

    Faker("es_MX")
    Faker.seed(42)  # Para reproducibilidad

    productos = []

    # Plantillas de productos por categoría
    plantillas = {
        "Electrónica": {
            "Computadoras": [
                "Laptop {marca} {modelo}",
                "PC Desktop {marca} {modelo}",
                "MacBook {modelo}",
            ],
            "Celulares": [
                "iPhone {modelo}",
                "Samsung Galaxy {modelo}",
                "Xiaomi {modelo}",
            ],
            "Accesorios": [
                "Audífonos {marca}",
                "Mouse {marca}",
                "Teclado {marca}",
                "Monitor {marca} {modelo}",
            ],
        },
        "Ropa": {
            "Casual": [
                "Camisa {marca} {color}",
                "Playera {marca} {color}",
                "Pantalón {marca} {color}",
            ],
            "Calzado": ["Tenis {marca} {modelo}", "Zapatos {marca} {color}"],
        },
        "Hogar": {
            "Cocina": [
                "Licuadora {marca}",
                "Cafetera {marca}",
                "Sartén {marca}",
            ],
            "Decoración": ["Lámpara {marca}", "Espejo {marca}", "Cuadro {tipo}"],
        },
        "Deportes": {
            "Equipamiento": [
                "Balón de {deporte}",
                "Pesas {peso}kg",
                "Raqueta de {deporte}",
            ]
        },
        "Libros": {
            "Ficción": [
                "Cien Años de Soledad",
                "Harry Potter y {titulo}",
                "El Señor de los Anillos",
            ]
        },
    }

    marcas = [
        "Nike",
        "Adidas",
        "Samsung",
        "Apple",
        "Sony",
        "LG",
        "HP",
        "Dell",
        "Lenovo",
    ]
    colores = ["Azul", "Rojo", "Negro", "Blanco", "Gris"]
    modelos = ["Pro", "Air", "Max", "Plus", "Ultra", "Lite"]

    producto_id = 1

    for _ in range(num_productos):
        # Elegir categoría y subcategoría aleatoria
        categoria = random.choice(list(plantillas.keys()))
        subcategoria = random.choice(list(plantillas[categoria].keys()))
        plantilla = random.choice(plantillas[categoria][subcategoria])

        # Generar nombre
        nombre = plantilla.format(
            marca=random.choice(marcas),
            modelo=random.choice(modelos),
            color=random.choice(colores),
            deporte=random.choice(["Fútbol", "Basketball", "Tenis"]),
            peso=random.choice([5, 10, 15, 20]),
            tipo=random.choice(["Abstracto", "Paisaje", "Retrato"]),
            titulo=random.choice(["la Piedra Filosofal", "el Prisionero de Azkaban"]),
        )

        # Asignar categoría/subcategoría (valida la lógica)
        cat_asignada, subcat_asignada = asignar_categoria(nombre)

        # Generar SKU único
        sku = f"SKU-{producto_id:06d}"

        # Precio según categoría
        if categoria == "Electrónica":
            precio = round(random.uniform(500, 25000), 2)
        elif categoria == "Ropa":
            precio = round(random.uniform(150, 2000), 2)
        elif categoria == "Hogar":
            precio = round(random.uniform(200, 5000), 2)
        elif categoria == "Deportes":
            precio = round(random.uniform(100, 3000), 2)
        elif categoria == "Libros":
            precio = round(random.uniform(100, 800), 2)
        else:
            precio = round(random.uniform(50, 1000), 2)

        # Peso según categoría
        if categoria == "Electrónica":
            peso = round(random.uniform(0.1, 5.0), 2)
        elif categoria == "Ropa":
            peso = round(random.uniform(0.1, 1.0), 2)
        elif categoria == "Hogar":
            peso = round(random.uniform(0.5, 10.0), 2)
        elif categoria == "Deportes":
            peso = round(random.uniform(0.2, 15.0), 2)
        elif categoria == "Libros":
            peso = round(random.uniform(0.2, 2.0), 2)
        else:
            peso = round(random.uniform(0.1, 5.0), 2)

        # Refrigeración (solo ciertos productos)
        requiere_refrigeracion = False  # Por defecto no

        productos.append(
            {
                "producto_id": producto_id,
                "sku": sku,
                "nombre_producto": nombre,
                "marca": random.choice(marcas),
                "categoria": cat_asignada,  # Usar categoría asignada
                "subcategoria": subcat_asignada,  # Usar subcategoría asignada
                "precio_catalogo": precio,
                "peso_kg": peso,
                "requiere_refrigeracion": requiere_refrigeracion,
            }
        )

        producto_id += 1

    return pd.DataFrame(productos)

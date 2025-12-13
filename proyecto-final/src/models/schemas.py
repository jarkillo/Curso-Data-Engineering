"""Schemas y modelos de datos para el pipeline ETL."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Order:
    """Modelo de un pedido."""

    order_id: str
    customer_id: str
    product_id: str
    quantity: int
    unit_price: float
    order_date: datetime
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Convierte a diccionario."""
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "order_date": self.order_date.isoformat(),
            "status": self.status,
        }


@dataclass
class Product:
    """Modelo de un producto."""

    product_id: str
    name: str
    category: str
    price: float
    stock: int

    def to_dict(self) -> dict[str, Any]:
        """Convierte a diccionario."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
        }


@dataclass
class Customer:
    """Modelo de un cliente."""

    customer_id: str
    name: str
    email: str
    region: str
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convierte a diccionario."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "region": self.region,
            "created_at": self.created_at.isoformat(),
        }


# Schemas de validación para DataFrames
ORDER_SCHEMA = {
    "required_columns": [
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "order_date",
        "status",
    ],
    "column_types": {
        "quantity": "int64",
        "unit_price": "float64",
    },
}

PRODUCT_SCHEMA = {
    "required_columns": [
        "product_id",
        "name",
        "category",
        "price",
        "stock",
    ],
    "column_types": {
        "price": "float64",
        "stock": "int64",
    },
}

CUSTOMER_SCHEMA = {
    "required_columns": [
        "customer_id",
        "name",
        "email",
        "region",
        "created_at",
    ],
}

FACT_SALES_SCHEMA = {
    "foreign_keys": ["product_id", "customer_id", "date_id"],
    "measures": ["quantity", "unit_price", "order_total", "discount_amount"],
}

DIM_DATE_SCHEMA = {
    "required_columns": [
        "date_id",
        "date",
        "year",
        "month",
        "day",
        "quarter",
        "day_of_week",
        "is_weekend",
    ],
}

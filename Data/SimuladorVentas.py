"""
simuladorVentas.py
------------------
Módulo de simulación de ventas para "Mis Creaciones".
Incluye inyección intencional de errores de calidad de datos.
Se importa desde main.py usando: from simuladorVentas import generar_ventas
"""

import random
from datetime import datetime, timedelta

# ── LISTAS BASE ────────────────────────────────────────────────────────────

PRODUCTOS = [
    {"nombre": "Vestido de ceremonia",  "precio": 215000, "descuento": False},
    {"nombre": "Traje elegante niño",   "precio": 189900, "descuento": True },
    {"nombre": "Conjunto formal mixto", "precio": 175000, "descuento": False},
    {"nombre": "Vestido bautizo",       "precio": 145000, "descuento": True },
    {"nombre": "Camisa formal niño",    "precio":  89900, "descuento": False},
    {"nombre": "Falda plisada niña",    "precio":  95000, "descuento": True },
    {"nombre": "Pantalón sastre niño",  "precio": 110000, "descuento": False},
    {"nombre": "Vestido quinceañera",   "precio": 320000, "descuento": True },
    {"nombre": "Blazer niño",           "precio": 135000, "descuento": False},
    {"nombre": "Vestido cóctel niña",   "precio": 180000, "descuento": True },
    {"nombre": "Corbatín niño",         "precio":  35000, "descuento": False},
    {"nombre": "Diadema elegante",      "precio":  28000, "descuento": True },
    {"nombre": "Zapatos charol niño",   "precio": 125000, "descuento": False},
    {"nombre": "Zapatos charol niña",   "precio": 120000, "descuento": True },
    {"nombre": "Cinturón formal",       "precio":  45000, "descuento": False},
    {"nombre": "Conjunto bautizo niño", "precio": 160000, "descuento": True },
]

TALLAS = ["XS", "S", "M", "L", "XL", "XXXL"]

ASESORES = [
    "Laura Gómez",
    "Carlos Mesa",
    "Valentina Ríos",
    "Andrés Parra",
    "Sofía Vélez",
    "Miguel Torres",
]

# ── FUNCIÓN PRINCIPAL ──────────────────────────────────────────────────────

def generar_ventas(numeroVentas: int) -> list:
    """
    Genera numeroVentas ventas simuladas con errores intencionales.

    Errores inyectados:
      < 0.15 → espacios extra en producto
      < 0.30 → vendedor en mayúsculas
      < 0.40 → talla inválida ("medio")
      < 0.50 → cantidad inválida (0, -1 o None)
      < 0.60 → precio_unitario None
      < 0.70 → fecha en formato incorrecto (dd/mm/YYYY)
      < 0.80 → total con valor basura
      < 0.90 → producto en minúsculas
      duplicados → 10% de las ventas se duplican al final
    """
    ventas = []

    # Fecha de inicio para el simulador
    fechaInicio = datetime(2025, 1, 2)

    for _ in range(numeroVentas):
        producto = random.choice(PRODUCTOS)
        cantidad = random.randint(1, 5)
        fecha    = fechaInicio + timedelta(days=random.randint(0, 60))

        venta = {
            "producto":        producto["nombre"],
            "precioUnitario":  producto["precio"],
            "descuento":       producto["descuento"],
            "talla":           random.choice(TALLAS),
            "cantidad":        cantidad,
            "vendedor":        random.choice(ASESORES),
            "fecha":           fecha.strftime("%Y-%m-%d"),
            "total":           cantidad * producto["precio"],
        }

        # ── INYECCIÓN DE ERRORES DE CALIDAD ───────────────────────────────
        probabilidadError = random.random()

        if probabilidadError < 0.15:
            venta["producto"] = " " + venta["producto"] + " "

        elif probabilidadError < 0.30:
            venta["vendedor"] = venta["vendedor"].upper()

        elif probabilidadError < 0.40:
            venta["talla"] = "medio"

        elif probabilidadError < 0.50:
            venta["cantidad"] = random.choice([0, -1, None])

        elif probabilidadError < 0.60:
            venta["precioUnitario"] = None

        elif probabilidadError < 0.70:
            fecha_obj = datetime.strptime(venta["fecha"], "%Y-%m-%d")
            venta["fecha"] = fecha_obj.strftime("%d/%m/%Y")

        elif probabilidadError < 0.80:
            venta["total"] = random.randint(1000, 5000)

        elif probabilidadError < 0.90:
            venta["producto"] = venta["producto"].lower()

        ventas.append(venta)

    # ── INYECCIÓN DE DUPLICADOS ────────────────────────────────────────────
    cantidadDuplicados = int(len(ventas) * 0.20)
    duplicados = random.sample(ventas, cantidadDuplicados)
    ventas.extend(duplicados)

    return ventas
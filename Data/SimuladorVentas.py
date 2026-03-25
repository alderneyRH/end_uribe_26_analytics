import numpy as np
from datetime import datetime, timedelta
 
# ── SEMILLA ────────────────────────────────────────────────────────────────
np.random.seed(42)
 
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
 
# ── FUNCIONES ──────────────────────────────────────────────────────────────
 
def simular_fecha(inicio="2025-01-01", fin="2025-03-31") -> str:
    """Retorna una fecha aleatoria entre inicio y fin."""
    fecha_inicio = datetime.strptime(inicio, "%Y-%m-%d")
    fecha_fin    = datetime.strptime(fin,    "%Y-%m-%d")
    dias_rango   = (fecha_fin - fecha_inicio).days
    fecha        = fecha_inicio + timedelta(days=int(np.random.randint(0, dias_rango)))
    return fecha.strftime("%Y-%m-%d")
 
 
def generar_ventas(n: int) -> list:
    """
    Genera n ventas simuladas.
    Retorna una lista de diccionarios lista para convertir a DataFrame.
 
    Cada venta contiene:
      id_venta, producto, precio_unitario, descuento, talla, cantidad, vendedor, fecha, total
    """
    ventas = []
 
    for i in range(1, n + 1):
        producto  = PRODUCTOS[np.random.randint(0, len(PRODUCTOS))]
        talla     = TALLAS[np.random.randint(0, len(TALLAS))]
        cantidad  = int(np.random.choice([1, 1, 1, 2, 2, 3]))
        vendedor  = ASESORES[np.random.randint(0, len(ASESORES))]
        fecha     = simular_fecha()
        total     = producto["precio"] * cantidad
 
        ventas.append({
            "id_venta":        i,
            "producto":        producto["nombre"],
            "precio_unitario": producto["precio"],
            "descuento":       producto["descuento"],
            "talla":           talla,
            "cantidad":        cantidad,
            "vendedor":        vendedor,
            "fecha":           fecha,
            "total":           total,
        })
 
    return ventas
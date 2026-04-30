"""
LimpiezaNegocio.py
------------------
Módulo de limpieza según reglas de negocio para "Mis Creaciones".
Contiene funciones específicas por dataset.
Se importa desde main.py usando: from utils.LimpiezaNegocio import limpiar_negocio_ventas
"""

import pandas as pd


# ── VENTAS ─────────────────────────────────────────────────────────────────

def limpiar_negocio_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica reglas de negocio específicas para el dataset de ventas.

    Reglas aplicadas:
      1. Cantidad debe ser mayor a 0
      2. Precio unitario debe ser mayor a 5000
      3. Talla debe pertenecer a la lista oficial
      4. Recalcula el total con los datos ya limpios
    """

    dataFrameCopia = df.copy()

    # ── REGLA 1: Cantidad válida (mayor a 0) ──────────────────────────────
    dataFrameCopia = dataFrameCopia[dataFrameCopia["cantidad"] > 0]

    # ── REGLA 2: Precio unitario válido (mayor a 5000) ────────────────────
    dataFrameCopia = dataFrameCopia[dataFrameCopia["precioUnitario"] > 5000]

    # ── REGLA 3: Talla dentro de los valores oficiales ────────────────────
    tallasValidas = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
    dataFrameCopia = dataFrameCopia[dataFrameCopia["talla"].isin(tallasValidas)]

    # ── REGLA 4: Recalcular total con datos ya limpios ────────────────────
    dataFrameCopia["total"] = dataFrameCopia["cantidad"] * dataFrameCopia["precioUnitario"]

    return dataFrameCopia


# ── EMPLEADOS ──────────────────────────────────────────────────────────────

def limpiar_negocio_empleados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica reglas de negocio específicas para el dataset de empleados.

    Reglas aplicadas:
      1. Salario base debe ser mayor o igual al salario mínimo colombiano (2025)
      2. Documento debe tener exactamente 10 dígitos numéricos
      3. Fecha de ingreso no puede ser futura
    """

    dataFrameCopia = df.copy()

    # ── REGLA 1: Salario mínimo Colombia 2025 = $1.423.500 ────────────────
    dataFrameCopia = dataFrameCopia[dataFrameCopia["salario_base"] >= 1423500]

    # ── REGLA 2: Documento debe ser numérico y tener 10 dígitos ──────────
    dataFrameCopia = dataFrameCopia[
        dataFrameCopia["documento"].astype(str).str.match(r"^\d{10}$")
    ]

    # ── REGLA 3: Fecha de ingreso no puede ser futura ─────────────────────
    dataFrameCopia = dataFrameCopia[
        dataFrameCopia["fecha_ingreso"] <= pd.Timestamp.today()
    ]

    return dataFrameCopia
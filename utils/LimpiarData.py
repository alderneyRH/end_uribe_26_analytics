"""
LimpiarData.py
--------------
Módulo genérico de limpieza de datos para "Mis Creaciones".
Funciona con cualquier DataFrame sin importar el generador.
Se importa desde main.py usando: from utils.LimpiarData import limpiar_data
"""

import pandas as pd


def limpiar_data(df: pd.DataFrame, columnas_texto: list, columnas_numericas: list, columnas_fecha: list, subset_dropna: list) -> pd.DataFrame:
    """
    Limpia un DataFrame aplicando las siguientes rutinas:

    1. Copia el DataFrame original para no modificarlo
    2. Limpia espacios extra en nombres de columnas
    3. Limpia espacios extra en columnas de texto y estandariza formato
    4. Reemplaza valores inválidos por NaN
    5. Convierte columnas numéricas al tipo correcto
    6. Convierte columnas de fecha al tipo correcto
    7. Elimina duplicados
    8. Elimina filas con nulos en columnas críticas

    Parámetros:
      df                → DataFrame sucio a limpiar
      columnas_texto    → columnas de tipo texto a limpiar (ej: ["producto", "talla", "vendedor"])
      columnas_numericas→ columnas numéricas a convertir  (ej: ["precioUnitario", "cantidad", "total"])
      columnas_fecha    → columnas de fecha a convertir   (ej: ["fecha"])
      subset_dropna     → columnas críticas para eliminar nulos (ej: ["producto", "precioUnitario", "cantidad", "fecha"])
    """

    # ── 1. COPIA PARA NO MODIFICAR EL ORIGINAL ────────────────────────────
    dataFrameCopia = df.copy()

    # ── 2. LIMPIAR ESPACIOS EN NOMBRES DE COLUMNAS ────────────────────────
    dataFrameCopia.columns = dataFrameCopia.columns.str.strip()

    # ── 3. LIMPIAR Y ESTANDARIZAR COLUMNAS DE TEXTO ───────────────────────
    for columna in columnas_texto:
        # Quitar espacios extra al inicio y al final
        dataFrameCopia[columna] = dataFrameCopia[columna].astype(str).str.strip()

    # Estandarizar formatos específicos si existen en el DataFrame
    if "producto" in dataFrameCopia.columns:
        dataFrameCopia["producto"] = dataFrameCopia["producto"].str.title()

    if "vendedor" in dataFrameCopia.columns:
        dataFrameCopia["vendedor"] = dataFrameCopia["vendedor"].str.title()

    if "talla" in dataFrameCopia.columns:
        dataFrameCopia["talla"] = dataFrameCopia["talla"].str.upper()

    if "nombre" in dataFrameCopia.columns:
        dataFrameCopia["nombre"] = dataFrameCopia["nombre"].str.title()

    if "apellido" in dataFrameCopia.columns:
        dataFrameCopia["apellido"] = dataFrameCopia["apellido"].str.title()

    # ── 4. REEMPLAZAR VALORES INVÁLIDOS POR NaN ───────────────────────────
    dataFrameCopia.replace(["", "None", "nan", "-"], pd.NA, inplace=True)

    # ── 5. CONVERTIR COLUMNAS NUMÉRICAS ───────────────────────────────────
    for columna in columnas_numericas:
        dataFrameCopia[columna] = pd.to_numeric(dataFrameCopia[columna], errors="coerce")

    # ── 6. CONVERTIR COLUMNAS DE FECHA ────────────────────────────────────
    for columna in columnas_fecha:
        dataFrameCopia[columna] = pd.to_datetime(dataFrameCopia[columna], errors="coerce", dayfirst=False)

    # ── 7. ELIMINAR DUPLICADOS ────────────────────────────────────────────
    dataFrameCopia = dataFrameCopia.drop_duplicates()

    # ── 8. ELIMINAR FILAS CON NULOS EN COLUMNAS CRÍTICAS ──────────────────
    dataFrameCopia = dataFrameCopia.dropna(subset=subset_dropna)

    return dataFrameCopia
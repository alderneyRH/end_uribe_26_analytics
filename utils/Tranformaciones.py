"""
Transformaciones.py
-------------------
Módulo de transformaciones y agrupaciones para "Mis Creaciones".
Genera los datos listos para alimentar las gráficas del Dashboard.
Funciona de forma independiente según el dataset recibido.

Importar desde main.py:
  from utils.Transformaciones import transformar_ventas, transformar_empleados
"""

import pandas as pd


# ══════════════════════════════════════════════════════════════════════════
#  VENTAS
# ══════════════════════════════════════════════════════════════════════════

def transformar_ventas(df: pd.DataFrame) -> dict:
    """
    Recibe el DataFrame de ventas ya limpio y retorna un diccionario
    con todas las agrupaciones necesarias para el Dashboard.

    Retorna:
      {
        kpis             → tarjetas KPI del Dashboard
        ventas_por_dia   → gráfica de barras por día
        ventas_por_mes   → gráfica de barras por mes
        ranking_asesores → tabla de ranking de asesores
        top_productos    → productos más vendidos
        resumen          → resumen general del período
      }
    """

    # ── Asegurar que fecha sea datetime ───────────────────────────────────
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", dayfirst=False)

    # Extraer columnas de tiempo útiles
    df["dia"]        = df["fecha"].dt.day
    df["mes"]        = df["fecha"].dt.month
    df["nombreDia"]  = df["fecha"].dt.day_name()
    df["año"]        = df["fecha"].dt.year

    # ── 1. KPIs generales ─────────────────────────────────────────────────
    kpis = {
        "total_ventas":      int(df["total"].sum()),
        "total_transacc":    len(df),
        "ticket_promedio":   round(df["total"].mean(), 2),
        "unidades_vendidas": int(df["cantidad"].sum()),
        "mejor_asesor":      df.groupby("vendedor")["total"].sum().idxmax(),
        "producto_estrella": df.groupby("producto")["cantidad"].sum().idxmax(),
    }

    # ── 2. Ventas por día (para gráfica de barras — filtro Día) ───────────
    ventas_por_dia = (
        df.groupby("nombreDia")["total"]
        .sum()
        .reset_index()
        .rename(columns={"nombreDia": "dia", "total": "total_ventas"})
        .sort_values("total_ventas", ascending=False)
    )

    # ── 3. Ventas por mes (para gráfica de barras — filtro Mes) ──────────
    ventas_por_mes = (
        df.groupby("mes")["total"]
        .sum()
        .reset_index()
        .rename(columns={"mes": "mes", "total": "total_ventas"})
        .sort_values("mes")
    )

    # ── 4. Ranking de asesores (para tabla del Dashboard) ─────────────────
    ranking_asesores = (
        df.groupby("vendedor")
        .agg(
            num_ventas  = ("total", "count"),
            total_ventas= ("total", "sum"),
        )
        .reset_index()
        .sort_values("total_ventas", ascending=False)
        .reset_index(drop=True)
    )
    # Agregar columna de porcentaje relativo al mejor asesor
    max_total = ranking_asesores["total_ventas"].max()
    ranking_asesores["pct"] = (ranking_asesores["total_ventas"] / max_total * 100).round(1)

    # ── 5. Top productos (para sección productos más vendidos) ────────────
    top_productos = (
        df.groupby("producto")
        .agg(
            unidades = ("cantidad", "sum"),
            ingresos = ("total",    "sum"),
        )
        .reset_index()
        .sort_values("ingresos", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    # ── 6. Ventas por talla (query específica de negocio) ─────────────────
    ventas_por_talla = (
        df.groupby("talla")["cantidad"]
        .sum()
        .reset_index()
        .sort_values("cantidad", ascending=False)
    )

    # ── 7. Queries útiles para reportes ───────────────────────────────────
    # Ventas superiores a 300.000
    ventas_altas = df.query("total > 300000")[["vendedor", "producto", "talla", "total"]]

    # Ventas del mes más reciente
    mes_reciente  = df["mes"].max()
    ventas_mes    = df.query("mes == @mes_reciente")

    # ── 8. Resumen del período ─────────────────────────────────────────────
    resumen = {
        "fecha_inicio":    str(df["fecha"].min().date()),
        "fecha_fin":       str(df["fecha"].max().date()),
        "asesores_activos": df["vendedor"].nunique(),
        "productos_distintos": df["producto"].nunique(),
        "mes_mayor_venta": int(ventas_por_mes.loc[ventas_por_mes["total_ventas"].idxmax(), "mes"]),
    }

    return {
        "kpis":             kpis,
        "ventas_por_dia":   ventas_por_dia,
        "ventas_por_mes":   ventas_por_mes,
        "ranking_asesores": ranking_asesores,
        "top_productos":    top_productos,
        "ventas_por_talla": ventas_por_talla,
        "ventas_altas":     ventas_altas,
        "ventas_mes":       ventas_mes,
        "resumen":          resumen,
    }


# ══════════════════════════════════════════════════════════════════════════
#  EMPLEADOS
# ══════════════════════════════════════════════════════════════════════════

def transformar_empleados(df: pd.DataFrame) -> dict:
    """
    Recibe el DataFrame de empleados ya limpio y retorna agrupaciones útiles.

    Retorna:
      {
        resumen          → totales generales
        por_turno        → conteo de empleados por turno
        salario_promedio → salario promedio general
        top_salarios     → empleados con mayor salario
      }
    """

    df = df.copy()
    df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"], errors="coerce", dayfirst=False)

    # ── 1. Resumen general ────────────────────────────────────────────────
    resumen = {
        "total_empleados":   len(df),
        "salario_promedio":  round(df["salario_base"].mean(), 2),
        "salario_minimo":    int(df["salario_base"].min()),
        "salario_maximo":    int(df["salario_base"].max()),
    }

    # ── 2. Empleados por turno ────────────────────────────────────────────
    por_turno = (
        df.groupby("turno" if "turno" in df.columns else "nombre")
        .size()
        .reset_index(name="cantidad")
    ) if "turno" in df.columns else pd.DataFrame()

    # ── 3. Top salarios ───────────────────────────────────────────────────
    top_salarios = (
        df[["nombre", "apellido", "salario_base"]]
        .sort_values("salario_base", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    # ── 4. Antigüedad (años en la empresa) ────────────────────────────────
    hoy = pd.Timestamp.today()
    df["antiguedad_años"] = ((hoy - df["fecha_ingreso"]).dt.days / 365).round(1)

    antiguedad = (
        df[["nombre", "apellido", "fecha_ingreso", "antiguedad_años"]]
        .sort_values("antiguedad_años", ascending=False)
        .reset_index(drop=True)
    )

    return {
        "resumen":     resumen,
        "por_turno":   por_turno,
        "top_salarios": top_salarios,
        "antiguedad":  antiguedad,
    }
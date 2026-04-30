"""
Reportes.py
-----------
Módulo de generación de reportes para "Mis Creaciones".
Toma las transformaciones y las exporta en JSON listos
para ser consumidos por el Dashboard del front-end.

Importar desde main.py:
  from utils.Reportes import generar_reporte_ventas, generar_reporte_empleados
"""

import json
import os
import pandas as pd
from .Tranformaciones import transformar_ventas, transformar_empleados


# ── UTILIDAD INTERNA ───────────────────────────────────────────────────────

def _guardar_json(datos: dict, nombre_archivo: str):
    """Guarda un diccionario como archivo JSON en la carpeta /reportes."""
    os.makedirs("reportes", exist_ok=True)
    ruta = f"reportes/{nombre_archivo}.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅ Reporte guardado: {ruta}")


def _df_a_lista(df: pd.DataFrame) -> list:
    """Convierte un DataFrame a lista de diccionarios para serializar a JSON."""
    return df.to_dict(orient="records")


# ══════════════════════════════════════════════════════════════════════════
#  REPORTE VENTAS
# ══════════════════════════════════════════════════════════════════════════

def generar_reporte_ventas(df: pd.DataFrame, guardar: bool = True) -> dict:
    """
    Genera el reporte completo de ventas listo para el Dashboard.

    Parámetros:
      df      → DataFrame de ventas ya limpio
      guardar → si True, exporta el JSON a /reportes/reporte_ventas.json

    Retorna un diccionario con la estructura que consume el front-end:
      {
        kpis             → tarjetas KPI
        graficaDia       → gráfica de barras filtro Día
        graficaMes       → gráfica de barras filtro Mes
        rankingAsesores  → tabla de ranking
        topProductos     → productos más vendidos
        resumen          → resumen del período
      }
    """

    t = transformar_ventas(df)

    reporte = {

        # ── Tarjetas KPI ──────────────────────────────────────────────────
        "kpis": {
            "totalVentas":      t["kpis"]["total_ventas"],
            "totalTransacc":    t["kpis"]["total_transacc"],
            "ticketPromedio":   t["kpis"]["ticket_promedio"],
            "unidadesVendidas": t["kpis"]["unidades_vendidas"],
            "mejorAsesor":      t["kpis"]["mejor_asesor"],
            "productoEstrella": t["kpis"]["producto_estrella"],
        },

        # ── Gráfica de barras por día ──────────────────────────────────────
        # Formato: [{ "dia": "Lunes", "total_ventas": 1200000 }, ...]
        "graficaDia": _df_a_lista(t["ventas_por_dia"]),

        # ── Gráfica de barras por mes ──────────────────────────────────────
        # Formato: [{ "mes": 1, "total_ventas": 18400000 }, ...]
        "graficaMes": _df_a_lista(t["ventas_por_mes"]),

        # ── Ranking de asesores ───────────────────────────────────────────
        # Formato: [{ "vendedor": "Laura Gómez", "num_ventas": 34, "total_ventas": 5800000, "pct": 100 }, ...]
        "rankingAsesores": _df_a_lista(t["ranking_asesores"]),

        # ── Top productos ─────────────────────────────────────────────────
        # Formato: [{ "producto": "Vestido de ceremonia", "unidades": 43, "ingresos": 9200000 }, ...]
        "topProductos": _df_a_lista(t["top_productos"]),

        # ── Ventas por talla ──────────────────────────────────────────────
        "ventasPorTalla": _df_a_lista(t["ventas_por_talla"]),

        # ── Resumen del período ───────────────────────────────────────────
        "resumen": t["resumen"],
    }

    if guardar:
        _guardar_json(reporte, "reporte_ventas")

    return reporte


# ══════════════════════════════════════════════════════════════════════════
#  REPORTE EMPLEADOS
# ══════════════════════════════════════════════════════════════════════════

def generar_reporte_empleados(df: pd.DataFrame, guardar: bool = True) -> dict:
    """
    Genera el reporte completo de empleados listo para el Dashboard.

    Parámetros:
      df      → DataFrame de empleados ya limpio
      guardar → si True, exporta el JSON a /reportes/reporte_empleados.json

    Retorna:
      {
        resumen      → totales generales
        porTurno     → distribución por turno
        topSalarios  → empleados con mayor salario
        antiguedad   → antigüedad de cada empleado
      }
    """

    t = transformar_empleados(df)

    reporte = {

        # ── Resumen general ───────────────────────────────────────────────
        "resumen": {
            "totalEmpleados":  t["resumen"]["total_empleados"],
            "salarioPromedio": t["resumen"]["salario_promedio"],
            "salarioMinimo":   t["resumen"]["salario_minimo"],
            "salarioMaximo":   t["resumen"]["salario_maximo"],
        },

        # ── Distribución por turno ────────────────────────────────────────
        "porTurno": _df_a_lista(t["por_turno"]) if not t["por_turno"].empty else [],

        # ── Top salarios ──────────────────────────────────────────────────
        "topSalarios": _df_a_lista(t["top_salarios"]),

        # ── Antigüedad ────────────────────────────────────────────────────
        "antiguedad": _df_a_lista(t["antiguedad"]),
    }

    if guardar:
        _guardar_json(reporte, "reporte_empleados")

    return reporte
import pandas as pd
from Data.SimuladorVentas    import generar_ventas
from Data.SimuladorEmpleados import generar_empleados
from utils.LimpiarData       import limpiar_data
from utils.LimpiezaNegocio   import limpiar_negocio_ventas, limpiar_negocio_empleados
from utils.Reportes          import generar_reporte_ventas, generar_reporte_empleados

# 1 — Generar datos sucios
df_ventas    = pd.DataFrame(generar_ventas(2000))
df_empleados = pd.DataFrame(generar_empleados(15))

# 2 — Limpieza técnica
df_ventas_limpio    = limpiar_data(df_ventas,    ["producto","talla","vendedor"], ["precioUnitario","cantidad","total"], ["fecha"],        ["producto","precioUnitario","cantidad","fecha"])
df_empleados_limpio = limpiar_data(df_empleados, ["nombre","apellido"],           ["salario_base"],                     ["fecha_ingreso"], ["documento","nombre","salario_base"])

# 3 — Limpieza de negocio
df_ventas_final    = limpiar_negocio_ventas(df_ventas_limpio)
df_empleados_final = limpiar_negocio_empleados(df_empleados_limpio)

# 4 — Generar reportes JSON para el Dashboard
reporte_ventas    = generar_reporte_ventas(df_ventas_final)
reporte_empleados = generar_reporte_empleados(df_empleados_final)

print(reporte_ventas["kpis"])


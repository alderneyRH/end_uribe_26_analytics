import numpy as np
from datetime import datetime, timedelta
 
np.random.seed(42)
 
 
NOMBRES = [
    {"nombre": "Laura",     "apellido": "Gómez"},
    {"nombre": "Carlos",    "apellido": "Mesa"},
    {"nombre": "Valentina", "apellido": "Ríos"},
    {"nombre": "Andrés",    "apellido": "Parra"},
    {"nombre": "Sofía",     "apellido": "Vélez"},
    {"nombre": "Miguel",    "apellido": "Torres"},
]
 
SALARIOS = [1800000, 2000000, 2200000, 2500000, 2800000]
 
 
def simular_documento() -> str:
    return str(np.random.randint(1000000000, 9999999999))
 
 
def simular_fecha_ingreso(inicio="2020-01-01", fin="2024-12-31") -> str:
    fecha_inicio = datetime.strptime(inicio, "%Y-%m-%d")
    fecha_fin    = datetime.strptime(fin,    "%Y-%m-%d")
    dias_rango   = (fecha_fin - fecha_inicio).days
    fecha        = fecha_inicio + timedelta(days=int(np.random.randint(0, dias_rango)))
    return fecha.strftime("%Y-%m-%d")
 
 
def generar_empleados() -> list:
    
    empleados = []
 
    for i, persona in enumerate(NOMBRES, start=101):
        empleados.append({
            "id_empleado":   i,
            "nombre":        persona["nombre"],
            "apellido":      persona["apellido"],
            "documento":     simular_documento(),
            "salario_base":  int(np.random.choice(SALARIOS)),
            "fecha_ingreso": simular_fecha_ingreso(),
        })
 
    return empleados
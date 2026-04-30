"""
simuladorEmpleados.py
---------------------
Módulo de simulación de empleados para "Mis Creaciones".
Incluye inyección intencional de errores de calidad de datos.
Se importa desde main.py usando: from simuladorEmpleados import generar_empleados
"""

import random
from datetime import datetime, timedelta

# ── LISTAS BASE ────────────────────────────────────────────────────────────

NOMBRES = [
    {"nombre": "Laura",     "apellido": "Gómez"},
    {"nombre": "Carlos",    "apellido": "Mesa"},
    {"nombre": "Valentina", "apellido": "Ríos"},
    {"nombre": "Andrés",    "apellido": "Parra"},
    {"nombre": "Sofía",     "apellido": "Vélez"},
    {"nombre": "Miguel",    "apellido": "Torres"},
]

SALARIOS = [1800000, 2000000, 2200000, 2500000, 2800000]

# ── FUNCIÓN PRINCIPAL ──────────────────────────────────────────────────────

def generar_empleados(numeroEmpleados: int) -> list:
    """
    Genera numeroEmpleados empleados simulados con errores intencionales.

    Errores inyectados:
      < 0.15 → documento con letras (inválido)
      < 0.30 → nombre en mayúsculas (inconsistencia de formato)
      < 0.40 → salario negativo o cero (valor inválido)
      < 0.50 → fecha en formato incorrecto (dd/mm/YYYY)
      < 0.60 → apellido con espacios extra
      < 0.70 → documento None (dato faltante)
      duplicados → 10% de los empleados se duplican al final
    """
    empleados = []

    fechaInicio = datetime(2020, 1, 1)

    for i in range(numeroEmpleados):
        persona = random.choice(NOMBRES)
        fecha   = fechaInicio + timedelta(days=random.randint(0, 1825))

        empleado = {
            "id_empleado":   101 + i,
            "nombre":        persona["nombre"],
            "apellido":      persona["apellido"],
            "documento":     str(random.randint(1000000000, 9999999999)),
            "salario_base":  random.choice(SALARIOS),
            "fecha_ingreso": fecha.strftime("%Y-%m-%d"),
        }

        # ── INYECCIÓN DE ERRORES DE CALIDAD ───────────────────────────────
        probabilidadError = random.random()

        if probabilidadError < 0.15:
            empleado["documento"] = "ABC" + str(random.randint(100000, 999999))

        elif probabilidadError < 0.30:
            empleado["nombre"] = empleado["nombre"].upper()

        elif probabilidadError < 0.40:
            empleado["salario_base"] = random.choice([0, -500000, -1000000])

        elif probabilidadError < 0.50:
            fecha_obj = datetime.strptime(empleado["fecha_ingreso"], "%Y-%m-%d")
            empleado["fecha_ingreso"] = fecha_obj.strftime("%d/%m/%Y")

        elif probabilidadError < 0.60:
            empleado["apellido"] = " " + empleado["apellido"] + " "

        elif probabilidadError < 0.70:
            empleado["documento"] = None

        empleados.append(empleado)

    # ── INYECCIÓN DE DUPLICADOS ────────────────────────────────────────────
    cantidadDuplicados = int(len(empleados) * 0.10)
    if cantidadDuplicados > 0:
        duplicados = random.sample(empleados, cantidadDuplicados)
        empleados.extend(duplicados)

    return empleados
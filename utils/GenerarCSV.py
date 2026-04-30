import pandas as pd
import os 

def generar_archivo_csv(data, nombre_archivo):
    df = pd.DataFrame(data)
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")
    print("Se creó el archivo CSV con éxito")



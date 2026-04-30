import pandas as pd 
import os 

def generar_archivo_json(data, nombre_archivo):
    df = pd.DataFrame(data)
    df.to_json(nombre_archivo, orient="records", indent=4)
    print("Se creó el archivo JSON con éxito")
import pandas as pd

from Data.SimuladorVentas import generar_ventas


DataFrameVentas = pd.DataFrame(generar_ventas(10))

 
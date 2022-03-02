import pandas as pd
from tqdm import tqdm
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(
    r'C:\Users\Lenovo\Documents\CURSO DATA SCIENCE - NEBULOVA\Archivos\PROYECTO AIRBNB\var.env')

KEY_MONGO = os.environ.get('KEY_MONGO')
client = MongoClient(
    f"mongodb+srv://admin:{KEY_MONGO}@clusterairbnb.hkqbr.mongodb.net/")


col_dataset = client["proyectoairbnb"]["dataset_limpio1"]
col_conteoclas = client["proyectoairbnb"]["conteo_clases"]
dataset = pd.DataFrame(list(col_dataset.find()))
conteoclas = pd.DataFrame(list(col_conteoclas.find()))
dataset.drop(columns=["_id", ""], inplace=True)
conteoclas.drop(columns=["_id", ""], inplace=True)

dataset.dropna(inplace=True)

# COGEMOS LOS DATOS NECESARIOS DE LA OTRA TABLA:

df_final1 = dataset[["ID", "Beds", "Bedrooms", "Bathrooms",
                     "Accommodates", "Room Type", "City", "Price"]]
conteoclas["ID"] = conteoclas["id_listing"]
conteoclas.drop(columns="id_listing", inplace=True)
df_final_def = df_final1.merge(conteoclas, on="ID", how="left")

# EXTRAEMOS INFO DE LA COLUMNA AMENITIES:

dataset.reset_index(inplace=True)
amenities = ["TV", "Internet", "Kitchen", "Heating",
             "Elevator", "Washer", "Air conditioning", "parking"]
conteoameties = pd.DataFrame(columns=["ID"])
for ame in amenities:
    print(f"{amenities.index(ame) + 1} / {len(amenities)} -- Buscando el elemento: {ame}")
    for row in tqdm(range(dataset.shape[0])):
        conteoameties.loc[row, "ID"] = dataset.ID[row]
        conteoameties.loc[row, ame] = dataset.Amenities[row].count(ame)
    print(
        f"{conteoameties[ame].sum()} coincidencias encontradas para el elemento {ame}")


# COMPROBAMOS QUE HAY COLUMNAS QUE NO TOMAN 0 Y 1. SINO QUE SE CUELAN ALGUNOS 2.
conteoameties.describe()

# CORREGIMOS LO ANTERIOR:
conteoameties_copy = conteoameties.copy()
for i in tqdm(["TV", "Internet", "Washer", "parking"]):
    for row in range(conteoameties.shape[0]):
        if conteoameties.loc[row, i] != 0:
            conteoameties.loc[row, i] = 1

# COMPROBAMOS QUE SE HA CORREGIDO:
conteoameties.describe()

df_final_def = df_final_def.merge(conteoameties, on="id_listing", how="right")

# RELLENAMOS LOS NAN CON CEROS:
df_final_def.fillna(0, inplace=True)

# HACEMOS LABEL ENCODER A LAS COLUMNAS OBJECT:


def mapeaColumna(columna):
    mapeo = dict()
    i = 0
    for cat in columna.unique():
        mapeo[cat] = i
        i += 1
    columna.replace(mapeo, inplace=True)
    return columna, mapeo


# mapeos_columnas = dict()
for col in df_final1.columns:
    if df_final1.loc[:, col].dtype == object:
        nueva_columna, mapeo = mapeaColumna(df_final1.loc[:, col])
        df_final1.loc[:, col] = nueva_columna
        mapeos_columnas[col] = mapeo

# Eliminamos la columna Unnamed: 0:
df_final_def.drop(columns="Unnamed: 0", inplace=True)

# SACAMOS LA TABLA EN CSV COMPLETA:
df_final_def.to_csv("TABLA_FULL.csv")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import string
from IPython.display import Image
from tqdm import tqdm
import requests
import json
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import math as m
import folium
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(
    r'C:\Users\Lenovo\Documents\CURSO DATA SCIENCE - NEBULOVA\Archivos\PROYECTO AIRBNB\var.env')

KEY_MONGO = os.environ.get('KEY_MONGO')
client = MongoClient(
    f"mongodb+srv://admin:{KEY_MONGO}@clusterairbnb.hkqbr.mongodb.net/")

col = client["proyectoairbnb"]["dataset_limpio1"]
dataset = pd.DataFrame(list(col.find()))
dataset.drop(columns="_id", inplace=True)
dataset.drop(columns="", inplace=True)
# path = r"C:\Users\Lenovo\Documents\CURSO DATA SCIENCE - NEBULOVA\Archivos\PROYECTO AIRBNB\PROYECTO EDU\dataset_limpio.csv"
# dataset = pd.read_csv(path)

# DESCARGAR DATOS DE OPENTRIPMAPS DE TODAS LAS GEOLOCATIONS PARA PUNTOS DE INTERES (POI)
# QUE ESTÉN A MENOS DE 500 METROS DE CADA UNO DE LOS LISTINGS:

list_closest = list()
for i in tqdm(range(5000)):
    i = i + 22701
    lat = dataset.Geolocation[i].split(",")[0]
    lon = dataset.Geolocation[i].split(",")[1]
    distancia = 500
    API_KEY = os.environ.get('API_KEY')
    url = f"https://api.opentripmap.com/0.1/en/places/radius?radius={distancia}&lon={lon}&lat={lat}&format=json&apikey={API_KEY}"
    prueba = requests.get(url)
    prueba1 = json.loads(prueba.text)
    for it in range(len(prueba1)):
        id_listing = dataset.ID[i]
        id_poi = prueba1[it]["xid"]
        name_poi = prueba1[it]["name"]
        dist_poi = prueba1[it]["dist"]
        kinds_poi = prueba1[it]["kinds"]
        dict_listing = {"id_listing": id_listing,
                        "id_poi": id_poi,
                        "dist_poi": dist_poi,
                        "kinds_poi": kinds_poi.split(",")}
        list_closest.append(dict_listing)
list_close = pd.DataFrame(list_closest)

kinds_global = list_close.copy()

kinds_global.reset_index(inplace=True)

kinds_global_agrupada = kinds_global.groupby(
    'id_listing').agg({"kinds_poi": "sum"}).reset_index()

# SCRAPEAMOS LAS CATEGORÍAS

url = "https://opentripmap.io/catalog.en.json"
cat = requests.get(url)
cat = json.loads(cat.text)
listcat = []
for i in cat["children"]:
    for e in i["children"]:
        listcat.append(e["id"])
        if "children" in e.keys():
            for a in e["children"]:
                listcat.append(a["id"])

listcat = ["beaches",
           "geological_formations",
           "nature_reserves",
           "water",
           "view_points",
           "buddhist_temples",
           "cathedrals",
           "synagogues",
           "churches",
           "climbing",
           "stadiums",
           "banks",
           "foods",
           "shops",
           "archaeology",
           "fortifications",
           "historical_places",
           "monuments_and_memorials",
           "museums",
           "theatres_and_entertainments",
           "bridges",
           "historic_architecture",
           "towers",
           "skyscrapers"]

conteoclas = pd.DataFrame(columns=["id_listing"])
# prueba_monuments = kinds_global["kinds_poi"].astype(str).str.count("monuments")
for clas in listcat:
    print(f"{listcat.index(clas) + 1} / {len(listcat)} -- Buscando el elemento: {clas}")
    for row in tqdm(range(kinds_global_agrupada.shape[0])):
        conteoclas.loc[row,
                       "id_listing"] = kinds_global_agrupada.id_listing[row]
        conteoclas.loc[row,
                       clas] = kinds_global_agrupada.kinds_poi[row].count(clas)
    print(
        f"{conteoclas[clas].sum()} coincidencias encontradas para el elemento {clas}")

conteoclas.to_csv("conteo_de_clases10_02_2022.csv")

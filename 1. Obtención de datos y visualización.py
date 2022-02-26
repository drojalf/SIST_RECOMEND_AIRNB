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

col = client["proyectoairbnb"]["airbnb_listings"]
dataset = pd.DataFrame(list(col.find()),index=None)

# IMPORTAMOS EL DATASET:

path = r"C:\Users\Lenovo\Documents\CURSO DATA SCIENCE - NEBULOVA\Archivos\PROYECTO AIRBNB\airbnb-listings.csv"
dataset = pd.read_csv(path, sep=";")

dataset_new = dataset.loc[:, ["ID",
                              "Name",
                              "Summary",
                              "Description",
                              "Space",
                              "Minimum Nights",
                              "Maximum Nights",
                              "Guests Included",
                              "Amenities",
                              "Beds",
                              "Bedrooms",
                              "Bathrooms",
                              "Accommodates",
                              "Room Type",
                              "Property Type",
                              "City",
                              "Country",
                              "Price",
                              "Review Scores Value",
                              "Number of Reviews",
                              "Geolocation",
                              "Listing Url"
                              ]]

# FILTRAMOS PARA QUEDARNOS SOLO CON ESPAÑA:

dataset_new = dataset_new[dataset_new['Country'] == "Spain"]
filtro = ["Madrid", "Barcelona"]
dataset_new1 = dataset_new[dataset_new.City.isin(filtro)]

dataset = dataset_new1

dataset.info()

dataset.describe()

# LIMPIEZA DE VALORES NULOS PARA COLUMNAS OBJECT:

for i in range(dataset.shape[1]):
    if dataset.iloc[:,i].dtype == 'O':
        dataset.iloc[:, i].fillna("N.A", inplace=True)

# LIMPIEZA DE VALORES NULOS PARA LOS RATINGS    :

dataset.iloc[:, 18].fillna(dataset.iloc[:,18].mean(), inplace=True)

# AL HABER POCOS VALORES NULOS, DESCARTAMOS LAS FILAS QUE TENGAN ALGÚN VALOR NULO:
dataset.dropna(inplace=True)

# DISTRIBUCIÓN DE PUNTUACIONES:
f, ax = plt.subplots(figsize=(20, 8))
sns.countplot(x="Review Scores Value", data=dataset)

# # DISTRIBUCIÓN DE LOS PRECIOS EN UNA MUESTRA DE LOS 1000 PRIMEROS:
x = dataset["ID"].head(1000)
y = dataset["Price"].head(1000)
plt.scatter(x, y)
plt.show()

# # PRECIOS EN FUNCIÓN DEL TIPO DE PROPIEDAD:
f, ax = plt.subplots(figsize=(20, 8))
sns.barplot(dataset["Price"], dataset["Property Type"], color="b")
ax.legend(ncol=2, loc="lower right", frameon=True)

# AFECTACIÓN DEL PRECIO

f, axs = plt.subplots(1, 2, figsize=(
    15, 6), gridspec_kw=dict(width_ratios=[6, 6]))
sns.lineplot(data=dataset, x="Bedrooms", y="Review Scores Value",
             ax=axs[0], color="r").set_xlabel("Bathrooms & Bedrooms * Scores")
sns.lineplot(data=dataset, x="Bathrooms",
             y="Review Scores Value", ax=axs[0], color="b")
sns.lineplot(data=dataset, x="Bedrooms", y="Price",
             ax=axs[1], color="r").set_xlabel("Bathrooms & Bedrooms * Prices")
sns.lineplot(data=dataset, x="Bathrooms", y="Price", ax=axs[1], color="b")
plt.legend(["Bedrooms", "Bathrooms"], loc="lower right")

# CORRELACIONES:
dataset[["Bathrooms", "Bedrooms", "Accommodates",
         "Price", "Review Scores Value"]].corr()

# MAPA DE CALOR:
f, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(dataset.corr())
# Observamos que las columnas Maximum Nights y Minimum Nights no parecen tener demasiada correlación con las demás. Sin embargo, existem columnas muy correlacionadas,
# como aquellas que hacen referencia a los Accommodates y las camas, las habitaciones, los baños...

dataset.to_csv("dataset_limpio.csv")
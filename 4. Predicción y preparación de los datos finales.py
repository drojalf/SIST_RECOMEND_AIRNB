from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import pymongo
from dotenv import load_dotenv
import os

load_dotenv(
    r'C:\Users\Lenovo\Documents\CURSO DATA SCIENCE - NEBULOVA\Archivos\PROYECTO AIRBNB\var.env')
key = os.environ.get('KEY_MONGO')


client = pymongo.MongoClient(
    f"mongodb+srv://admin:{key}@clusterairbnb.hkqbr.mongodb.net/")

col = client["proyectoairbnb"]["airbnb"]
Data = pd.DataFrame(list(col.find()))


# CÓDIGOS
#   1- EXTRACCIÓN DE DATOS PRIMERA TABLA, visualizaciones etc...
#   2- LLAMADA A LA API.
#   3- Ya tengo las tablas, junto toda la anterior, tratamiento de ammenities.
#   4- Codo y KMEANS, tabla final.
#   5- Código que lee la tabla de mongo y ejecuta el código y el pronóstico.

# AUTOMATIZADO
col = client["proyectoairbnb"]["airbnb"]
Data = pd.DataFrame(list(col.find()))
Data_ID = Data.copy()


# OPERAREMOS EL KMEANS 1 CON :
# Para este método, le daremos toda información que tenemos al KMEANS para clusterizar.

Data.drop(columns=["Unnamed: 0", "ID", "", "_id"],
          errors="ignore", inplace=True)
Data.drop(columns=["_id", ""], inplace=True, errors="ignore")

# OPERAREMOS EL KMEANS 2 CON:
# En este caso, únicamente dejamos aquellas columnas que nos sirvan para modelar un KMEANS enfocado en los sitios de interés cercanos.

Data2 = Data.drop(
    columns=[
        "Beds",
        "Bedrooms",
        "Bathrooms",
        "Accommodates",
        "Room Type",
        "City",
        "Price",
        "Internet",
        "Kitchen",
        "TV",
        "Heating",
        "Elevator",
        "Washer",
        "Air conditioning",
        "parking",
        "buddhist_temples",
        "cathedrals",
        "synagogues",
        "banks",
        "fortifications",
        "bridges",
        "skyscrapers",
        "towers",
        "historic_architecture",
        "stadiums",
        "climbing",
        "archaeology",
        "view_points",
        "historical_places",
    ]
)


# NORMALIZAMOS EL DATASET

norm = MinMaxScaler().fit(Data)
Data_norm = norm.transform(Data)

norm2 = MinMaxScaler().fit(Data2)
data_norm_2 = norm2.transform(Data2)


# CON LA LIBRERIA ELBOW, PODEMOS HACER PRUEBAS Y ESTUDIAR EL Nº DE CLÚSTER ÓPTIMOS PARA CADA ESTUDIO KMEANS.

kmeans = KMeans()
elbow = KElbowVisualizer(kmeans, k=(2, 15))
elbow.fit(Data_norm)
elbow.show()

kmeans = KMeans()
elbow = KElbowVisualizer(kmeans, k=(2, 15))
elbow.fit(data_norm_2)
elbow.show()


# 1-- PROCEDEMOS A REALIZAR EL PRIMER KMEANS SOBRE EL DATASET QUE CONTIENE TODA LA INFORMACIÓN ACERCA DE LOS APARTAMENTOS POSIBLE,

kmeans = KMeans(n_clusters=6, random_state=0).fit(Data_norm)
kmeans_cat = kmeans.fit_predict(Data_norm)

centers = kmeans.cluster_centers_

distancia_vectores = kmeans.transform(Data_norm)
cluster = kmeans.labels_

# 1.1- Montamos la tabla de datos originales e insertamos los cúster del KMEANS 1.
datos_kmeans = Data.copy()
datos_kmeans["ID"] = Data_ID.loc[:, "ID"]
datos_kmeans["Cluster_1"] = cluster
datos_kmeans.loc[:, "Cluster_1"].value_counts()

# 1.2- Montamos la tabla de distancias con los vectores con la que trabajaremos el Kmeans 1.
tabla_distancias_1 = pd.DataFrame(distancia_vectores)
tabla_distancias_1.reset_index(inplace=True, drop=True)
datos_kmeans.reset_index(inplace=True, drop=True)

# 1.3- Busco una tabla con los datos normalizados para hacer una asignación eficiente.
data_norm_pd = pd.DataFrame(Data_norm)
data_norm_pd["Cluster_1"] = cluster
data_norm_pd.describe()

# 1.4- Inserto las distancias a los clústers en la tabla completa.
for i in range(tabla_distancias_1.shape[0]):
    datos_kmeans.loc[i,
                     "dist_cluster_1"] = tabla_distancias_1.iloc[i, cluster[i]]


# 2-- PROCEDEMOS A REALIZAR EL SEGUNDO KMEANS SOBRE EL DATASET QUE CONTIENE TODA LA INFORMACIÓN ACERCA DE LOS APARTAMENTOS POSIBLE,

kmeans_2 = KMeans(n_clusters=4, random_state=0).fit(data_norm_2)
kmeans_cat_2 = kmeans_2.fit_predict(data_norm_2)

centers_2 = kmeans.cluster_centers_

distancia_vectores_2 = kmeans_2.transform(data_norm_2)
cluster_2 = kmeans_2.labels_

# 2.1- Insertamos los clústers del Kmeans 2.

datos_kmeans["Cluster_2"] = cluster_2
datos_kmeans.loc[:, "Cluster_2"].value_counts()

# 1.2- Montamos la tabla de distancias con los vectores con la que trabajaremos el Kmeans 1.

tabla_distancias_2 = pd.DataFrame(distancia_vectores_2)
tabla_distancias_2.reset_index(inplace=True, drop=True)

# 1.3- Busco una tabla con los datos normalizados (debe ser los datos normalizados de la tabla completa) para hacer una asignación eficiente.
data_norm_pd["Cluster_2"] = cluster_2
data_norm_pd["ID"] = Data_ID.loc[:, "ID"]
data_norm_pd.describe()

# 1.4
for i in range(tabla_distancias_2.shape[0]):
    datos_kmeans.loc[i,
                     "dist_cluster_2"] = tabla_distancias_2.iloc[i, cluster_2[i]]


datos_kmeans.to_csv('Tabla_Mongo.csv')


# EMPEZAMOS CON LA DESCRIPCIÓN DE CADA UNO DE LOS CLÚSTER EN CADA UNO DE LOS DOS MÉTODOS DE KMEANS
# Utilizamos los 100 más cercanos al clúster con el objetivo de ver los más representativos.

# CLÚSTERS DEL KMEANS 1

Cluster1_0 = Data.iloc[(tabla_distancias_1.sort_values(
    by=0).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster1_1 = Data.iloc[(tabla_distancias_1.sort_values(
    by=1).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster1_2 = Data.iloc[(tabla_distancias_1.sort_values(
    by=2).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster1_3 = Data.iloc[(tabla_distancias_1.sort_values(
    by=3).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster1_4 = Data.iloc[(tabla_distancias_1.sort_values(
    by=4).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster1_5 = Data.iloc[(tabla_distancias_1.sort_values(
    by=5).iloc[:100, 0].index.tolist()), :].copy().describe()


# CLÚSTERS DEL KMEANS 2

Cluster2_0 = Data2.iloc[(tabla_distancias_1.sort_values(
    by=0).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster2_1 = Data2.iloc[(tabla_distancias_1.sort_values(
    by=1).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster2_2 = Data2.iloc[(tabla_distancias_1.sort_values(
    by=2).iloc[:100, 0].index.tolist()), :].copy().describe()

Cluster2_3 = Data2.iloc[(tabla_distancias_1.sort_values(
    by=3).iloc[:100, 0].index.tolist()), :].copy().describe()

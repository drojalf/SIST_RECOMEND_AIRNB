              
              
              
              
              
              
              
              
              
              
              
              
              
              
              #################################### CÓDIGO 5 ########################################
import folium
from h11 import Data
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from operator import itemgetter
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pymongo
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(
    r'C:\Users\Lenovo\Documents\CURSO DATA SCIENCE - NEBULOVA\Archivos\PROYECTO AIRBNB\var.env')
key = os.environ.get('KEY_MONGO')

client = pymongo.MongoClient(
    f"mongodb+srv://admin:{key}@clusterairbnb.hkqbr.mongodb.net/")


# IMPORT DE TABLAS CON MONGO DB
col = client["proyectoairbnb"]["dataset_limpio1"]
dataset = pd.DataFrame(list(col.find()))

col = client["proyectoairbnb"]["airbnb2"]
datos_kmeans = pd.DataFrame(list(col.find()))

dataset.drop(columns=["_id", ""], inplace=True, errors="ignore")
datos_kmeans.drop(columns=["_id", ""], inplace=True, errors="ignore")

# #IMPORT DE TABLAS MANUAL
# dataset = pd.read_csv(r"C:\Users\eduar\Desktop\Curso DATA\trabajo final\dataset_new_proyecto_geo.csv")
# datos_kmeans = pd.read_csv(r"C:\Users\eduar\Desktop\Curso DATA\trabajo final\Tabla_Mongo.csv")


# LO USAMOS PARA SACAR LAS PONDERACIONES PARA REALIZAR ASIGNACIONES CON CIERTO PESO
norm = MinMaxScaler().fit(datos_kmeans)
data_norm_pd = pd.DataFrame(norm.transform(datos_kmeans))


# FUNCIONES QUE USAMOS
def selector_clúsuer():

    while True:
        q1_ciudad = input(
            "Elige una ciudad: \n1-MADRID, \n2-BARCELONA, \n3-No lo tengo claro. SELECCIONA UN NÚMERO."
        )

        if q1_ciudad == "1":  # MADRID

            while True:
                q1_personas = input(
                    "¿Cómo planeas viajar? \n1- Sólo / En pareja  \n2- En grupo "
                )

                if q1_personas == "1":
                    CLUSTER = 3
                    break
                elif q1_personas == "2":
                    CLUSTER = 4
                    break
                else:
                    print("Por favor, seleccione un valor válido")

            break

        elif q1_ciudad == "2":  # BARCELONA

            while True:
                q2_personas = input(
                    "¿Cómo planeas viajar? \n1- Sólo / En pareja  \n2- En grupo "
                )

                if q2_personas == "1":  # SOLO / EN PAREJA

                    while True:
                        q2_centro_afueras = input(
                            "Dónde le gustaría estar situado? \n1- Centro de la ciudad \n2- En las afueras \n3-Indiferente"
                        )
                        if q2_centro_afueras == "1":
                            CLUSTER = 2
                            break
                        elif q2_centro_afueras == "2":
                            CLUSTER = 1
                            break
                        elif q2_centro_afueras == "3":

                            while True:
                                q2_facilidades = input(
                                    "¿Las facilidades/equipamiento del apartamento son importantes para ti? \n1- Sí \n2-Me es indiferente"
                                )
                                if q2_facilidades == "1":
                                    CLUSTER = 1
                                    break
                                elif q2_facilidades == "2":
                                    CLUSTER = 2
                                    break
                                else:
                                    print("Por favor, elige una opción válida")

                            break

                        else:
                            print("Por favor, seleccione un valor válido")

                    break

                elif q2_personas == "2":  # EN GRUPO
                    while True:
                        q2_centro_afueras_2 = input(
                            "Dónde le gustaría estar situado? \n1- Centro de la ciudad \n2- En las afueras "
                        )  # \n3-Indiferente

                        if q2_centro_afueras_2 == "1":
                            CLUSTER = 5
                            break
                        elif q2_centro_afueras_2 == "2":
                            CLUSTER = 0
                            break
                        # elif q2_centro_afueras =="3":
                        else:
                            print("Por favor, seleccione una opción válida")
                    break

                else:
                    print("Por favor, seleccione un valor válido")

            break

        elif q1_ciudad == "3":

            q3_recom = input(
                "Por favor, deja que le asesoremos: \n¿Qué es lo que busca en el viaje? \nSelecciona tres de las siguientes actividades que le gustaría realizar, de mayor a menor importancia"
                " 1- Turismo gastronómico"
                " 2- Playa y sus alrededores"
                " 3- Excursiones en la naturaleza"
                " 4- Conocer una ciudad en profundidad"
                " 5- Hacer turismo y buenas compras"
                " 6- Ocio cultural"
                " 7- Hacer turismo sin los agobios del centro de una ciudad"
            )

            CLUSTER = q3_recom.replace(",", "").replace(
                "-", "").replace(" ", "").replace("  ", "")

            break

        else:
            print("Valor incorrecto, no ha elegido una opción válida")

    return CLUSTER


def filtrado(clúster_asignado):
    datos_kmeans_filtrado = datos_kmeans.loc[(
        datos_kmeans.loc[:, "Cluster_1"] == int(clúster_asignado)), :].copy()

    while True:
        q3 = input(
            f"¿Qué tipo de alojamiento te gustaría? 1-HABITACION PRIVADA ({datos_kmeans_filtrado.loc[datos_kmeans_filtrado['Room Type'] == 0].shape[0]} resultados), 2-CASA ENTERA({datos_kmeans_filtrado.loc[datos_kmeans_filtrado['Room Type'] == 1].shape[0]} resultados)")

        if q3 != "1" and q3 != "2":
            print("Valor incorrecto")
        else:
            break
    while True:
        q4 = input(f"Los precios se encuentran entre " + str(min(datos_kmeans_filtrado["Price"])) + " y "+str(
            max(datos_kmeans_filtrado["Price"]))+" euros. Elija un precio mínimo: ")
        q5 = input("Elija un precio máximo: ")

        if type(clúster_asignado) == str:
            q6 = input("Introduce el número de huéspedes: ")
            filtro = datos_kmeans_filtrado.loc[((datos_kmeans_filtrado.loc[:, "Price"] >= int(q4)) & (datos_kmeans_filtrado.loc[:, "Price"] <= int(
                q5)) & (datos_kmeans_filtrado["Room Type"] == int(q3)-1) & (datos_kmeans_filtrado.loc[:, "Accommodates"] == int(q6))), :].index.tolist()

        else:
            filtro = datos_kmeans_filtrado.loc[((datos_kmeans_filtrado.loc[:, "Price"] >= int(q4)) & (
                datos_kmeans_filtrado.loc[:, "Price"] <= int(q5)) & (datos_kmeans_filtrado["Room Type"] == int(q3)-1)), :].index.tolist()

        if len(filtro) != 0:

            break
        else:
            print(
                "No se han encontrado apartamentos para ese rango de precio, por favor marque una nueva cifra")

    filtrado_norm = data_norm_pd.loc[filtro, :].copy()

    return filtrado_norm


def selector_gustos(clúster_asignado, filtrado_data_normalizado):

    if type(clúster_asignado) == int:

        while True:
            pref = input("En su viaje le gustaría: 0 - Permanecer en el alojamiento "
                         " 1 - Conocer la historia y cultura ciudad "
                         " 2 - Ocio y entretenimiento "
                         " 3 - Disfrutar de buenos restaurantes y tiendas "
                         " 4 - Realizar deporte "
                         " 5 - Conocer los edificios religiosos de la zona "
                         " 6 - Estar cerca de la naturaleza ")
            listilla = []

            if pref == "0":

                for i in range(filtrado_data_normalizado.shape[0]):
                    a = []
                    a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("Internet")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("Kitchen")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("TV")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("Heating")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("Washer")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("Air conditioning")]), filtrado_data_normalizado.index.tolist()[i]]
                    listilla.append(a)
                LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                LISTILLA_INDEX = []

                for i in range(len(LISTILLA_ORDENADA[-20:])):
                    LISTILLA_INDEX.append(LISTILLA_ORDENADA[-20:][i][1])

                RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                    by="dist_cluster_1").copy()
                break

            if pref == "1":

                for i in range(filtrado_data_normalizado.shape[0]):
                    a = []
                    a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("historical_places")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("monuments_and_memorials")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("museums")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("fortifications")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("archaeology")]), filtrado_data_normalizado.index.tolist()[i]]
                    listilla.append(a)
                LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                LISTILLA_INDEX = []

                for i in range(len(LISTILLA_ORDENADA[-20:])):
                    LISTILLA_INDEX.append(LISTILLA_ORDENADA[-20:][i][1])

                RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                    by="dist_cluster_1").copy()
                break

            if pref == "2":

                for i in range(filtrado_data_normalizado.shape[0]):
                    a = []
                    a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("theatres_and_entertainments")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("museums")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("shops")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("stadiums")]), filtrado_data_normalizado.index.tolist()[i]]
                    listilla.append(a)
                LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                LISTILLA_INDEX = []

                for i in range(len(LISTILLA_ORDENADA[-20:])):
                    LISTILLA_INDEX.append(LISTILLA_ORDENADA[-20:][i][1])

                RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                    by="dist_cluster_1").copy()
                break

            if pref == "3":

                for i in range(filtrado_data_normalizado.shape[0]):
                    a = []
                    a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("shops")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("foods")]), filtrado_data_normalizado.index.tolist()[i]]
                    listilla.append(a)
                LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                LISTILLA_INDEX = []

                for i in range(len(LISTILLA_ORDENADA[-20:])):
                    LISTILLA_INDEX.append(LISTILLA_ORDENADA[-20:][i][1])

                RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                    by="dist_cluster_1").copy()
                break

            if pref == "4":

                for i in range(filtrado_data_normalizado.shape[0]):
                    a = []
                    a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("nature_reserves")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("stadiums")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("climbing")]), filtrado_data_normalizado.index.tolist()[i]]
                    listilla.append(a)
                LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                LISTILLA_INDEX = []

                for i in range(len(LISTILLA_ORDENADA[-20:])):
                    LISTILLA_INDEX.append(LISTILLA_ORDENADA[-20:][i][1])

                RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                    by="dist_cluster_1").copy()
                break

            if pref == "5":

                for i in range(filtrado_data_normalizado.shape[0]):
                    a = []
                    a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("buddhist_temples")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("cathedrals")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("churches")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("synagogues")]), filtrado_data_normalizado.index.tolist()[i]]
                    listilla.append(a)
                LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                LISTILLA_INDEX = []

                for i in range(len(LISTILLA_ORDENADA[-20:])):
                    LISTILLA_INDEX.append(LISTILLA_ORDENADA[-20:][i][1])

                RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                    by="dist_cluster_1").copy()
                break

            if pref == "6":

                for i in range(filtrado_data_normalizado.shape[0]):
                    a = []
                    a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("beaches")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("geological_formations")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("nature_reserves")] +
                          filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("water")]), filtrado_data_normalizado.index.tolist()[i]]
                    listilla.append(a)
                LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                LISTILLA_INDEX = []

                for i in range(len(LISTILLA_ORDENADA[-20:])):
                    LISTILLA_INDEX.append(LISTILLA_ORDENADA[-20:][i][1])

                RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                    by="dist_cluster_1").copy()

                break

    elif type(clúster_asignado) == str:

        for i in range(len(clúster_asignado)):

            listilla = []

            if i == 1:

                filtrado_data_normalizado = RECOMENDACIÓN
                n = 3

                if clúster_asignado[i] == "0":
                    n = 20
                    for i in range(filtrado_data_normalizado.shape[0]):
                        a = []
                        a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("beaches")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("nature_reserves")]),
                             filtrado_data_normalizado.index.tolist()[i]]
                        listilla.append(a)
                    LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                    LISTILLA_INDEX = []

                    for i in range(len(LISTILLA_ORDENADA[-n:])):
                        LISTILLA_INDEX.append(LISTILLA_ORDENADA[-n:][i][1])

                    RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                        by="dist_cluster_2").copy()
                    break

                if clúster_asignado[i] == "1":

                    RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                        by="dist_cluster_2").copy()
                    break

                if clúster_asignado[i] == "2":

                    for i in range(filtrado_data_normalizado.shape[0]):
                        a = []
                        a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("monuments_and_memorials")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("museums")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("theatres_and_entertainments")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index(
                                  "churches")]
                              ),
                             filtrado_data_normalizado.index.tolist()[i]]
                        listilla.append(a)
                    LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                    LISTILLA_INDEX = []

                    for i in range(len(LISTILLA_ORDENADA[-n:])):
                        LISTILLA_INDEX.append(LISTILLA_ORDENADA[-n:][i][1])

                    RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                        by="dist_cluster_2").copy()
                    break

                if clúster_asignado[i] == "3":

                    for i in range(filtrado_data_normalizado.shape[0]):
                        a = []
                        a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("foods")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index(
                                  "shops")]
                              ),
                             filtrado_data_normalizado.index.tolist()[i]]
                        listilla.append(a)
                    LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                    LISTILLA_INDEX = []

                    for i in range(len(LISTILLA_ORDENADA[-n:])):
                        LISTILLA_INDEX.append(LISTILLA_ORDENADA[-n:][i][1])

                    RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                        by="dist_cluster_2").copy()

            else:

                n = 20

                if clúster_asignado[i] == "0":

                    for i in range(filtrado_data_normalizado.shape[0]):
                        a = []
                        a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("beaches")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("nature_reserves")]),
                             filtrado_data_normalizado.index.tolist()[i]]
                        listilla.append(a)
                    LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                    LISTILLA_INDEX = []

                    for i in range(len(LISTILLA_ORDENADA[-n:])):
                        LISTILLA_INDEX.append(LISTILLA_ORDENADA[-n:][i][1])

                    RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                        by="dist_cluster_2").copy()
                    break

                if clúster_asignado[i] == "1":

                    a = filtrado_data_normalizado.index.tolist()
                    RECOMENDACIÓN = datos_kmeans.loc[a, :].sort_values(
                        by="dist_cluster_2").copy()
                    break

                if clúster_asignado[i] == "2":

                    for i in range(filtrado_data_normalizado.shape[0]):
                        a = []
                        a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("monuments_and_memorials")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("museums")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("theatres_and_entertainments")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index(
                                  "churches")]
                              ),
                             filtrado_data_normalizado.index.tolist()[i]]
                        listilla.append(a)
                    LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                    LISTILLA_INDEX = []

                    for i in range(len(LISTILLA_ORDENADA[-n:])):
                        LISTILLA_INDEX.append(LISTILLA_ORDENADA[-n:][i][1])

                    RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                        by="dist_cluster_2").copy()
                    break

                if clúster_asignado[i] == "3":

                    for i in range(filtrado_data_normalizado.shape[0]):
                        a = []
                        a = [(filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index("foods")] +
                              filtrado_data_normalizado.iloc[i, datos_kmeans.columns.tolist().index(
                                  "shops")]
                              ),
                             filtrado_data_normalizado.index.tolist()[i]]
                        listilla.append(a)
                    LISTILLA_ORDENADA = sorted(listilla, key=itemgetter(0))
                    LISTILLA_INDEX = []

                    for i in range(len(LISTILLA_ORDENADA[-n:])):
                        LISTILLA_INDEX.append(LISTILLA_ORDENADA[-n:][i][1])

                    RECOMENDACIÓN = datos_kmeans.loc[LISTILLA_INDEX, :].sort_values(
                        by="dist_cluster_2").copy()

                    break

    return RECOMENDACIÓN


# CÓDIGO DE RECOMENDACIÓN

# ASIGNAMOS EL CÚSTER

clúster_asignado = selector_clúsuer()

filtrado_data_normalizado = filtrado(clúster_asignado)

RECOMENDACIÓN = selector_gustos(clúster_asignado, filtrado_data_normalizado)


# Listado de cosas cercanas###

def elec(listing_id, columna):

    return datos_kmeans.loc[datos_kmeans['ID'] == listing_id, columna].iloc[0]


def cercano(listing_id):

    lista_cercanos = []

    for i in range(7, 31):

        if int(float(elec(primer_resultado, datos_kmeans.columns[i]))) >= 1:

            lista_cercanos.append(datos_kmeans.columns[i])

    return lista_cercanos


##################

# CÓDIGO DE VISUALIZACIÓN DEL AIRBNB RECOMENDADO

primer_resultado = RECOMENDACIÓN.iloc[0, -5]
RECOMENDACIÓN.columns
dataset.Namecoord = dataset.loc[dataset["ID"] ==
                                primer_resultado, "Geolocation"].iloc[0].split(",")

print(f"""ID : {primer_resultado}
Nombre : {dataset.loc[dataset["ID"] == primer_resultado,"Name"].iloc[0]}
Precio : {dataset.loc[dataset["ID"] == primer_resultado,"Price"].iloc[0]}
Ciudad: {dataset.loc[dataset["ID"] == primer_resultado,"City"].iloc[0]}
Tipo de alojamiento: {dataset.loc[dataset["ID"] == primer_resultado, "Room Type"].iloc[0]}
Equipado con: {dataset.loc[dataset["ID"] == primer_resultado, "Amenities"].iloc[0]}
Camas: {dataset.loc[dataset["ID"] == primer_resultado,"Beds"].iloc[0]}
Habitaciones: {dataset.loc[dataset["ID"] == primer_resultado,"Bedrooms"].iloc[0]}
Baños: {dataset.loc[dataset["ID"] == primer_resultado,"Bathrooms"].iloc[0]}
Equipado con: {dataset.loc[dataset["ID"] == primer_resultado, "Amenities"].iloc[0]}
Descripción: {dataset.loc[dataset["ID"] == primer_resultado, "Description"].iloc[0]}
Cercano a: {', '.join([str(item) for item in cercano(primer_resultado)])}
Puntuación opiniones: {dataset.loc[dataset["ID"] == primer_resultado, "Review Scores Value"].iloc[0]}
URL: {dataset.loc[dataset["ID"] == primer_resultado, "Listing Url"].iloc[0]}
""")

lat = float(dataset.Namecoord[0])
lon = float(dataset.Namecoord[1])
coord = [lat, lon]
mapi = folium.Map(
    location=coord,
    zoom_start=18,
    tiles='Stamen Terrain'
)

tooltip = 'mapa'

folium.Marker(coord, popup=folium.Popup(
    max_width=20), tooltip=tooltip).add_to(mapi)

mapi
# PROYECTO DE CREACIÓN DE UN SISTEMA DE RECOMENDACIÓN DE ALOJAMIENTO DE AIRBNB EN FUNCIÓN DE LOS GUSTOS DEL USUARIO
El proyecto que hemos llevado a cabo se trata de una aplicación que nos recomienda un alojamiento de la web AirBNB en función de nuestros gustos o preferencias de viaje. Esta recomendación irá en base a varios factores, pero principalmente analiza la afinidad del alojamiento a las características de lo que busca el cliente, como el destino del viaje, tipo de alojamiento, habitaciones, etc... pero principalmente se sirve de datos de puntos de interés cercanos al mismo, tomando como referencia un radio de 500 metros a la redonda, pero que podría ampliarse de manera sencilla según los requerimientos.
En esta primera versión, hemos utilizado solo las ciudades de Madrid y Barcelona.

## FUENTES DE DATOS:

Para la obtención de los datos hemos utilizado varias fuentes de datos que detallamos a continuación:

1. La primera fuente de información utilizada fue la base de datos de OpenDataSoft: https://public.opendatasoft.com/explore/dataset/airbnb-listings/table/?disjunctive.host_verifications&disjunctive.amenities&disjunctive.features
de la cual se puede descargar la información de listings AirBNB de numerosos países del mundo. En este caso nos interesaba quedarnos solo con España, y dentro de esta, con las ciudades de Madrid y Barcelona. De las columnas que lleva el dataset, nos hemos quedado con 22 columnas, que son las siguientes:

        - "ID"
        - "Name"
        - "Summary"
        - "Description",
        - "Space",
        - "Minimum Nights",
        - "Maximum Nights",
        - "Guests Included",
        - "Amenities",
        - "Beds",
        - "Bedrooms",
        - "Bathrooms",
        - "Accommodates",
        - "Room Type",
        - "Property Type",
        - "City",
        - "Country",
        - "Price",
        - "Review Scores Value",
        - "Number of Reviews",
        - "Geolocation",
        - "Listing Url"

2. La segunda fuente de datos utilizada, ha sido la web de OpenTripMaps. 
https://opentripmap.io/ Aprovechando la columna "Geolocation" de la información obtenida en OpenDataSoft, hemos analizado la cercanía de cada alojamiento a los diferentes puntos de interes de cada ciudad, catalogando cada uno en función de los POI's cercanos. 
Para ello, este código hace uso de la API de esta web con el objetivo de hacer una exploración de los diferentes puntos de interes, distinguiéndolos por su diversa tipología (historia, deportes, museos, restaurantes, monumentos...) en un radio de 500 metros a la redonda de cada uno de los alojamientos. 
Este radio se ha establecido por cuestión de equilibrio entre funcionalidad y economizar recursos, pero es ampliable.

## Paso 1: Obtención de información y limpieza de datos:

Al comienzo del proyecto, se recoge la tabla obtenida directamente desde OpenDataSoft y se extrae la información que necesitamos. Nos quedamos con las ciudades de Madrid y Barcelona, así como también nos quedamos solo con las columnas enumeradas en el punto anterior.

Luego se efectúa una limpieza de los valores nulos para las columnas objeto, así como para la columna de ratings. Una vez hecho, al quedar pocos valores nulos, desecharíamos las filas que tengan algún valor nulo.

Como resultado de esto, es obtienen 30.425 filas.

## Paso 2: Análisis de la información y visualización:
En este paso, visualizamos la información a través de distintos gráficos de visualización con las librerías Plotly y Matplotlib:
    - Distribución de puntuaciones: Observamos que las calificaciones predominantes, con diferencia, son aquellas que rondan el 9.
    - La distribución de precios en una muestra de los 1000 primeros: Observamos que la gran mayoría se ubica en menos de 100 Euros la noche, luego hay muchos que superan esta cantidad, y algunos aislados con valores muy altos.
    - Precios en funcion del tipo de propiedad: En este caso, observamos que aquellas propiedades "no usuales" son las más caras, como las villas, los barcos, o las cuevas.
    - Mapa de calor: Observamos mucha correlación entre las columnas de Accommodates, Bedrooms, Bathrooms...

## Paso 3: Obtención de los puntos de interés:
A través de la API de Opentripmaps, y valiéndonos de la columna Geolocation, hacemos una iteración de todos los alojamientos para que nos informe de aquellos POI's existentes a su alrededor. Estos pois quedan almacenados en un .json de cada listing, recogiendo su ID, tipo, nombre...

Posteriormente se scrapean las distintas categorías de POI's. Para ello se utiliza el arbol de categorías de OpenTripMaps: https://opentripmap.io/catalog. 

Para descargar la información es necesaria una API Key que se puede conseguir gratuitamente registrándose en el siguiente enlace:

https://opentripmap.io/product

Nos quedamos con las categorías que tienen resultados:

                "beaches", 
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
                "skyscrapers"

Luego se contea la aparición de cada categoría en cada listing, obteniendo una tabla en la que, para cada ID de listing, se nos muestra la aparición de cada categoría, una por cada columna.

## Paso 4: Tratamiento de la columna Amenities:

La columna Amenities requiere un tratamiento para poder hacer un análisis de su contenido, ya que los datos vienen recogidos en lista dentro de cada celda. Se realiza un proceso para recoger cada uno de sus elementos (TV, Internet, Kitchen, Washer, etc...) en cada columna. Nos genera una tercera tabla, que unimos a la tabla principal. 
En este caso, a diferencia de lo anterior, más que un conteo, se trata de un sistema binario en el que 0 significa que lo tiene, y 1 significa que no lo tiene.

## Paso 5: Label Encoder

Hacemos LabelEncoder a las columnas objeto, como por ejemplo la columna ciudad. Siendo tal que:

            0. Madrid
            1. Barcelona

## Paso 6: Predicción KMeans:

El código efectúa una predicción KMeans para discriminar entre diversos tipos de alojamiento en función de diversos valores que determina el propio modelo.

Para este modelo se trabaja con las columnas de POI's, Amenities y columnas cuantitativas del primer dataset, como Habitaciones, Huéspedes, Baños, Huéspedes, Tipo de Habitación, Ciudad y Precio.

Esos datos servirán de input para que el modelo aprenda a diferenciar los registros en 6 clusters diferentes.

Se trabaja además con una segunda tabla secundaria en la que solamente figuran columnas POI's. Esta tabla se utilizará para hacer una predicción en la que el usuario no esta seguro de lo que quiere, y solamente se le pregunta por sus gustos.

Una vez realizada la predicción KMeans, se añade a la tabla principal la columna "cluster" en el que figura el número de cluster asignado al registro.

En paralelo, obtenemos una tabla de distancias al cluster. Con esta tabla, de los registros finales que obtengamos, nos quedaremos con el más cercano al cluster.

## Paso 7: Análisis de clusters:

A través del análisis de clusters, sacaremos la información relevante de cada uno de los clusters para intentar interpretar de qué manera ha realizado el algoritmo Kmeans la clasificación.

Este análisis lo usaremos como primer paso a la hora de preguntar al usuario. Haciendo dos o tres preguntas básicas, asignaremos un cluster al usuario en función de su perfil de alternativas.

        • Grupo 0 :
            ○ Por encima de la media en el número de camas (3 vs 2 ), así como de huéspedes ( 4,5 vs 3,3 ) y número de habitaciones ( 1,93 vs 1,4 )
            ○ El tipo de habitación es 1 , Casa entera.
            ○ La ciudad es Barcelona.
            ○ El precio es superior a la media (106 vs 78 )
            ○ No hay muchos sitios de interés cercanos, tan solo se encuentra cerca de la media en arquitectura histórica (10,85 vs 12.93)
            ○ Totas cuentan con TV, internet, cocina, calefacción, ascensor, ducha, aire acondicionado...
        
        (Primeras conclusiones de este tipo de grupo: Piso situado en una zona no céntrica de barcelona, apartamento completo que cuenta con bastante espacio y todas las comodidades posibles en el piso.
        
        VIAJE EN FAMILIA A BARCELONA, CASA ENTERA 


        	• Grupo 1:
		○ Por debajo de la media en el número de camas (1 vs 2), así como de huéspedes (2 vs 3,3) y número de habitaciones (1 vs 1,4)
		○ El tipo de habitación es el 0, Habitación privada.
		○ La ciudad es Barcelona.
		○ El precio es inferior a la media ( 42,44 vs 78)
		○ No hay sitios de interés cercanos, tan solo se encuentra cerca de la media en arquitectura histórica (9,94 vs 12.93)
		○ Todos los apartamentos cuentan con todas las facilidades posibles excepto de aire acondicionado.
	
	(Primeras conclusiones de este tipo de grupo: Habitaciones situadas en una zona no céntrica de Barcelona, barato, viajeros individuales o en pareja )
	
	
	
	• Grupo 2:
		○ Por debajo de la media en el número de camas (1 vs 2), así como de huéspedes (1,91 vs 3,3) y número de habitaciones (1 vs 1,4)
		○ El tipo de habitación es el 0, Habitación privada.
		○ La ciudad es Barcelona.
		○ El precio es muy inferior a la media ( 34,79 vs 78)
		○ Hay algunos sitios de interés cercanos (por debajo de la media)
		○ Los apartamentos no cuentan con ningún tipo de facilidad, ni tv, ni calefacción, ni ascensor, ni ducha, ni aire acondicionado... 
	
	(Primeras conclusiones de este tipo de grupo: Habitaciones muy baratas situadas en una zona un poco más céntrica de Barcelona, barato, pero habitaciones de pisos muy poco equipadas )
	

	• Grupo 3:
		○ En la media en el número de camas (1,98 vs 2), así como de huéspedes (3,77 vs 3,3) y número de habitaciones (1,19 vs 1,4)
		○ El tipo de habitación es el 1, casa entera.
		○ La ciudad es Madrid.
		○ El precio está en la media (74.89 vs 78)
		○ Entre sus sitios de interés cercanos se encuentran los miradores, las iglesias (12,78 vs 10), los restaurantes (1.3 vs 1), hay tiendas ( 0,12 vs 0,3 ), hay muchos monumentos ( 36.82 vs 18 ) ,museos ( 8.12 vs 6.5), teatros ( 11,95 vs 10 ), algo de rascacielos, 
		○ Los apartamentos cuentan con todo tipo de facilidades (excepto parkings)
	
	(Primeras conclusiones de este tipo de grupo: casa entera situadas en el centro de madrid o de sus barrios, no en las afueras, y habitaciones de pisos muy equipadas ).
	

	• Grupo 4:
		○ Por debajo de la media en el número de camas (1,21 vs 2), así como de huéspedes (1,88 vs 3,3) y número de habitaciones (1,19 vs 1,4)
		○ El tipo de habitación es el 0, Habitación privada.
		○ La ciudad es Madrid.
		○ El precio está por debajo de la media ( 34,64  vs 78 )
		○ No hay muchos sitios de interés cercanos
		○ Los apartamentos cuentan con todo tipo de facilidades (excepto parking y aire acondicionado)

	 (Primeras conclusiones:  barato pero no céntrico, situado en algún barrio con poca densidad de sitios de interés a un precio barato.
	
	
	• Grupo 5:
		○ Por encima de la media en el número de camas (2,47 vs 2), así como de huéspedes (4 vs 3,3) y número de habitaciones (1,7 vs 1,4)
		○ El tipo de habitación es el 1, casa entera.
		○ La ciudad es Barcelona.
		○ El precio está por encima de la media ( 96  vs 78 )
		○ Hay algo de sitios de interés cercanos bastantes cosas pero por debajo de la media. 
		○ Los apartamentos cuentan con todo tipo de facilidades (excepto parking y elevator ????)
	
        (Primeras conclusiones: Habitación privada en barcelona, por encima de la media en precio pero no mucho)

## Paso 8: Preguntas al usuario:

### Obtención del cluster:

A través de variables input, vamos preguntando al usuario diversas cuestiones para, en primer lugar, asignarle un cluster, y en segundo lugar, filtrar los datos que no necesitemos. El resultado final vendrá determinado por el registro más cercano al cluster de aquellos que resten.

        DESTINO? --> MADRID ----> PERSONAS? -----> <2 ---> CLUSTER 3
        |                           |
        |                           -------------> >=2 --> CLUSTER 4
        |
        |--------> BARCELONA ---> PERSONAS? -----> <2 ---> CENTRO? ----> CLUSTER 2
                                     |                  |
                                     |                  --> AFUERAS? --> CLUSTER 1
                                     |
                                     ------------> >=2 --> CENTRO? ---> CLUSTER 5
                                                        |
                                                        --> AFUERAS? --> CLUSTER0   

Una vez realizada esta clusterización, pasamos a la etapa de filtrado.

### Filtrado por gustos y preferencias:

Una vez seleccionado el cluster, pasamos a la selección por gustos. En este proceso, filtramos los valores en función de las respuestas que nos devuelve el usuario en relación al número de huéspedes, equipamiento, habitaciones...

## Paso 9: Recomendación final:

Al final de la función, el sistema nos devuelve un print con la recomendación que nos hace. En este print observamos nombre, descripción, url de Airbnb y diversos datos.
Además, se ha incorporado un mapa de geolocalización a través de la librería folium que nos permite corroborar que la recomendación se ajusta a lo que buscamos.


# Próximas actualizaciones en previsión:

1. Ampliación a más ciudades de España, como Valencia, Sevilla, Zaragoza... y posteriormente ir incluyendo mayor número de paises.
2. Inclusión de más información que afine mejor la clusterización.
3. Interfaz gráfica web para mejorar la experiencia del usuario.
4. Al ampliar el ámbito geográfico, incluir mayor número de tipos de POI's que no se encuentran presentes en la versión actual.
5. Nuevos algoritmos de aprendizaje para la diferenciación de tipos, como DBSCAN.
6. Incluir más preguntas para afinar más en lo que desea el usuario.
7. Nuevas fuentes de datos, como reseñas individuales de usuarios de AirBNB que permitan una mayor precisión.
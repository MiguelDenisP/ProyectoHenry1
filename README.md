
## README

<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

 <h2 align=center>Miguel Denis</h2>




Este es el Proyecto Individual N°1 para Henry (API del Dataset de Películas), cohorte DataFT-23 a fecha Julio 2024. 

<hr>  

## Descripción
Este proyecto consta de una API a través de Render que contiene 6 funciones de consulta + 1 modelo de ML para Recomendación respecto a un dataset de películas para un cliente de servicio de Streaming

## Tabla de Contenido
1. [Introducción](#descripción)
2. [Librerias y Servicios](#librerías-y-servicios-utilizados)
3. [Fuente de datos](#fuente-de-datos)
4. [Estructura del Repositorio](#estructura-del-repositorio)
5. [Uso y Ejecución](#uso-y-ejecución)
6. [Metodología](#metodología)
7. [Funciones del API](#funciones-del-api)
8. [Mejoras a Proceder](#mejoras-a-proceder)
9. [Autor](#autor)




## Librerías y Servicios utilizados:
- Python 3.7 o superior
- pandas
- numpy
- nltk
- scikit-learn
- FastAPI
- Render

<br>

**Pasos de instalación:**

No es necesario instalar nada, sino acceder a [https://proyectohenry1.onrender.com/docs](https://proyectohenry1.onrender.com/docs) donde estará deployada la API o en su defecto hacer el deploy de este repositorio en Render

## **Fuente de Datos**

- Los 2 dataset originales (credit y movies_dataset) utilizados en este proyecto provienen de un drive aportado por Henry en [Dataset Original](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5?usp=drive_link)


Los cuales fueron procesados y guardados (ver notebooks) en una carpeta dentro de este repositorio



## Estructura del Repositorio

- `Main.py`: Archivo principal que contiene la FastAPI y y ejecuta las Funciones de Consulta y el Modelo través de Render

- `Requirements.txt`: texto que contiene los requerimientos de la API para Render


- `Data/`: Contiene los archivos de datos procesados a partir del dataset original que serán consumidos por la API

- `Notebooks/`: Incluye los notebooks de Jupyter con el ETL, EDA, tokenización para el Modelo y un beta del Modelo

- `README.md`: Archivo de documentación del proyecto.

## Uso y Ejecución
1. Ingrese a [https://proyectohenry1.onrender.com/docs](https://proyectohenry1.onrender.com/docs) en Render donde estará alojada la API y realice sus consultas.
2. Si esto no funciona, ingresar al Dashboard de Render y realizar un Deploy de este repositorio

## Metodología
De los datos originales luego de sus respectivos procesos de ETL y EDA correspondiente (ver notebooks) se construyen las 6 funciones de consulta del dataset, y se procede a tokenizar la data en lenguaje natural y se entrena un modelo vectorizado de similitud del coseno para construir la funcion de Recomendación

## Funciones del API

Las 7 funciones de la API son:
- `Score`: Se ingresa el título de una película. La API devolverá el año de estreño y su score de popularidad

- `Votos`: Se ingresa un título. Devolverá el año de estreno, y en caso de tener más de 2000 valoraciones, el promedio de ellas

- `Mes`: Se ingresa un mes en español (ej: Abril). Devuelve la cantidad de películas que fueron estrenadas en aquel mes

- `Actor`: Se ingresa un actor/actriz. La API retorna la cantidad de películas en las que ha participado, su retorno total y retorno promedio por película

- `Día`: Se ingresa un día de la semana(ej:Viernes). Retorna la cantidad de películas que han sido estrenadas ese día

- `Director`: Se ingresa el nombre de un Director(ej: Steven Spielberg). La API devolverá el retorno total del director. Además, retorna cada película que dirigió junto a su fecha de estreno, retorno, costo, y ganancia

- `Recomendación`: Se ingresa el título original de una película. El modelo otorgará una lista de las mejores 5 similitudes al título ingresado


## Mejoras a Proceder
- Mejorar el general layout, apariencia y descripciones de la API
- Foolproof los input de las funciones
- Incluir más data en el modelo y mejorar su rendimiento
- Tener menos crisis intentando hacer un proyecto

## Autor:
Este proyecto fue realizado por Miguel Denis Pagliero, cohorte DataFT-23 para Henry, y cuya única licencia es la de conducir.
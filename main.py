from fastapi import FastAPI
import pandas as pd
import numpy as np
from nltk import word_tokenize
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk


app = FastAPI(
    title= 'Consultas sobre database de Peliculas',
    description='API para realizar consultas sobre el movies_dataset')

#http://127.0.0.1:8000

#se lee el df limpio de la carpeta Data
df = pd.read_csv(r"./Data/limpio1.csv")


# funcion de entrada y testeo
@app.get("/")
def index():
    return "Hola Miguel. Esta es una API de Peliculas"


# funcion que recibe un titulo y entrega el año y la popularidad
@app.get("/score/")
def score_titulo(titulo):
    df_titulo = df[df['title']==titulo]
    anio = df_titulo['release_year'].values[0]
    score = df_titulo['popularity'].values[0]

    return (f'La pelicula {titulo} fue estrenada en el año {anio} con un score/popularidad de {round(score,2)}')



# funcion que recibe un titulo y entrega la valoraciones
@app.get('/votos/')
def votos_titulo(titulo):
    df_titulo= df[df['title']==titulo]
    conteo = df_titulo['vote_count'].values[0]
    if int(conteo)<2000:
        return ('La pelicula tiene menos de 2000 valoraciones. No se devuelve votos')
    else:
        anio = df_titulo['release_year'].values[0]
        puntaje = df_titulo['vote_average'].values[0]
        return (f'La pelicula {titulo} fue estrenada en el año {anio}. La misma cuenta con {conteo} valoraciones, con un promedio de {round(puntaje,2)}')
    

# funcion que entrega cantidad de peliculas estrenadas estrenadas en cierto mes
@app.get('/mes/')
def cantidad_filmaciones_mes(mes):
    if mes == 'Enero':
        mes1 = 1
    elif mes == 'Febrero':
        mes1 = 2
    elif mes == 'Marzo':
        mes1 = 3
    elif mes == 'Abril':
        mes1 = 4
    elif mes == 'Mayo':
        mes1 = 5
    elif mes == 'Junio':
        mes1 = 6
    elif mes == 'Julio':
        mes1 = 7
    elif mes == 'Agosto':
        mes1 = 8
    elif mes == 'Septiembre':
        mes1 = 9
    elif mes == 'Octubre':
        mes1 = 10
    elif mes == 'Noviembre':
        mes1 = 11
    elif mes == 'Diciembre':
        mes1 = 12
    else:
        return ('debe colocar un mes correcto en español con mayuscula al inicio y sin tilde')

    df['release_date']=pd.to_datetime(df['release_date'])
    df["mes"] = df["release_date"].dt.month
    peliculas_mes = df[df["mes"] == mes1]
    numero_peliculas = peliculas_mes.shape[0]

    return (f'{numero_peliculas} cantidad de peliculas fueron estrenadas en el mes {mes}')

# funcion que recibe un actor y devuelve cantidad de peliculas y retorno total
@app.get("/actor/")
def get_actor(actor):

    df_filtrado = df[df['cast_names'].apply(lambda x: actor in x)]
    conteo = df_filtrado.shape[0]
    retorno_total = df_filtrado['return'].sum()
    if float(conteo)==0:
        return (f'El nombre ingresado {actor} no ha participado en ninguna de estas peliculas')
    else:
        retorno_promedio = float(retorno_total)/float(conteo)
        return (f'El actor {actor} ha participado de {conteo} cantidad de filmaciones, ha conseguido un retorno de {round(retorno_total,2)} con un promedio de {round(retorno_promedio,2)} por filmacion')


# funcion que recibe dia de la semana y entrega cantidad de peliculas estrenadas ese dia
@app.get("/dia/")  
def cantidad_filmaciones_dia(dia):
    if dia=='Lunes':
        dia1 = 'Monday'
    elif dia =='Martes':
        dia1= 'Tuesday'
    elif dia =='Miercoles':
        dia1= 'Wednesday'
    elif dia =='Jueves':
        dia1= 'Thursday'
    elif dia =='Viernes':
        dia1= 'Friday'
    elif dia =='Sabado':
        dia1= 'Saturday'
    elif dia =='Domingo':
        dia1= 'Sunday'
    else: 
        return('debe colocar un dia de la semana en español con mayuscula al comienzo y sin tilde')
    
    df_dia = df[df['release_day']==dia1]
    cantidad_peliculas = df_dia.shape[0]

    return(f'{cantidad_peliculas} cantidad de peliculas fueron estrenadas en los días {dia}')



# funcion que entrega informacion sobre peliculas dirigias por un director
@app.get("/director/")
def get_director(director):
    df_filtrado = df[df['director_name']==director]
    retorno_total = df_filtrado['return'].sum()
    conteo = df_filtrado.shape[0]
    result = f'El/la Director/a {director} ha tenido un retorno total de {round(retorno_total,2)} dolares'
    for i in range(0,conteo):
        result = result + f'dirigio {df_filtrado.iloc[i,10]}, estrenada el {df_filtrado.iloc[i,5]} que tuvo un retorno de {df_filtrado.iloc[i,13]} con un costo de {df_filtrado.iloc[i,0]} y una ganancia de {df_filtrado.iloc[i,6]}'
    return (result)



# MODELO DE RECOMENDACION

""" Por razones de memoria y Render, el tokenizado previo de la data fue realizado en el notebook 'ml.ipynb'
    Y el modelo entrenado aqui a partir del dataset preparado 'data_modelo.csv'  
    Tambien, para este prototipo de modelo solo usaremos algunas columnas de las previamente    """

@app.get("/recomendacion/")
def recomendacion(titulo):
    return recomendador(titulo, df2)





df2 = pd.read_csv(r'../Data/data_modelo.csv')
df2 = df2.fillna("")

lista_columnas = ['tokenizada_overview', 'tokenizada_title', 'tokenizada_director_name', 'tokenizada_production_companies_names']

lista_matrices= []
dic_vectores = {}

for column in lista_columnas:
    vectorizer = TfidfVectorizer()
    matriz = vectorizer.fit_transform(df[column])
    dic_vectores[column]=vectorizer
    lista_matrices.append(matriz)

combinacion_matrices = hstack(lista_matrices).tocsr() if len(lista_matrices) > 1 else lista_matrices[0]

def similitud_coseno(idx, matriz):
    return cosine_similarity(matriz[idx], matriz).flatten()

def recomendador(title, data, num=5):
    if title not in df['title'].values:
        return f'La película {title} aun no se ha realizado o usted no sabe escribir'

    idx = data[data['title']==title].index[0]
    puntaje = similitud_coseno(idx, combinacion_matrices)

    lista_pelis = list(enumerate(puntaje))
    lista_pelis = sorted(lista_pelis, key=lambda x: x[1], reverse=True)

    lista_pelis= lista_pelis[1:num+1]

    indices = [i[0] for i in lista_pelis]

    lista_vacia = []

    return data['title'].iloc[indices].tolist()
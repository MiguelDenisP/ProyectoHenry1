from fastapi import FastAPI
import pandas as pd


app = FastAPI(
    title= 'Consultas sobre database de Peliculas',
    description='API para realizar consultas sobre el movies_dataset')

#http://127.0.0.1:8000

#se lee el df limpio de la carpeta Data
df = pd.read_csv(r"./Data/limpio1.csv")


# funcion de entrada y testeo
@app.get("/")
def index():
    return "Hola Miguel"


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
    if df['vote_count'].values[0]<2000:
        return ('La pelicula tiene menos de 2000 valoraciones. No se devuelve votos')
    else:
        df_titulo= df[df['title']==titulo]
        anio = df_titulo['release_year'].values[0]
        conteo = df_titulo['vote_count'].values[0]
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
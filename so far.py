import pandas as pd
import numpy as np
import ast
import json
import re
import datetime

# cargo el archivo para su lectura
eda = pd.read_csv(r"C:\Users\migue\OneDrive\Escritorio\movies_dataset.csv")

# Eliminación primeras columnas que no serán utilizadas
columnas_eliminar = ['video', "imdb_id", "adult", "original_title", "poster_path", "homepage"]
eda.drop(columns=columnas_eliminar, inplace=True)

# Se eliminan 87 entradas que no tienen release_date
eda.dropna(subset=['release_date'], inplace=True)

#Se deciden eliminar las 3 entradas de revenue 0 por data insuficiente
eda.dropna(subset=['revenue'], inplace=True)


# Creamos columa return (revenue/budget) que dará 0 en caso de no poder realizar la división
#primero creamos la función que calculará el return
def cal_return(revenue, budget):
    if float(budget) == 0:
        return 0
    else:
        return float(revenue)/float(budget)
    
#creamos nueva columa return
eda['return']=eda.apply(lambda row: cal_return(row['revenue'], row['budget']), axis=1)


# transformamos las fechas de release_date a datetime
eda['release_date']=pd.to_datetime(eda['release_date'])
eda['release_date']=eda['release_date'].dt.strftime('%Y-%m-%d')  #Esto es para volverlo str con formato AAAA-mm-dd

# se crea columna 'release_year' donde se alberga solo el año de estreno
eda['release_year']=eda['release_date'].dt.year



                # DESANIDADO


# Se crea una función que reemplaza las comillas ' por " para manejar json
def reemplazar_comillas(cadena):
  return re.sub(r"'", '"', cadena)

# Se cambian comillas de columna genres
eda['genres'] = eda['genres'].apply(reemplazar_comillas)

# Se transforma los datos de str a listas
eda['genres'] = eda['genres'].apply(lambda x: json.loads(x))

# Se desanidan id y los nombres de la columna genres
eda['genres_ids'] = eda['genres'].apply(lambda x: [d['id'] for d in x])
eda['genres_names'] = eda['genres'].apply(lambda x: [d['name'] for d in x])


# funcion para formatear las conlumnas con listas de diccionarios
def convert_to_list_of_dicts(value):
    try:
        value = value.strip()
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return [] 

# Se transforma la columna production_companies y se desanida en id y names
eda['production_companies'] = eda['production_companies'].apply(convert_to_list_of_dicts)
eda['production_companies_id'] = eda['production_companies'].apply(lambda x: [d['id'] for d in x])
eda['production_companies_names'] = eda['production_companies'].apply(lambda x: [d['name'] for d in x])


# de la columna production_countries se desanida el codigo iso
eda['production_countries'] = eda['production_countries'].apply(convert_to_list_of_dicts)
eda['production_countries_iso'] = eda['production_countries'].apply(lambda x: [d['iso_3166_1'] for d in x])
eda['production_countries_names'] = eda['production_countries'].apply(lambda x: [d['name'] for d in x])

# se transforma la columna spoken_languages a lista de dicc y se desanidan
eda['spoken_languages'] = eda['spoken_languages'].apply(convert_to_list_of_dicts)
eda['spoken_languages_iso'] = eda['spoken_languages'].apply(lambda x: [d['iso_639_1'] for d in x])
eda['spoken_languages_name'] = eda['spoken_languages'].apply(lambda x: [d['name'] for d in x])


# Se reemplazan los Nan de belongs_to_collection por dicc vacios
#eda['belongs_to_collection']=eda['belongs_to_collection'].fillna('{}') #opcion 1 funciona pero son str y falla luego
eda['belongs_to_collection']=eda['belongs_to_collection'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {})

# se crean funciones para extraer id y name de los diccionarios
def extract_id(row):
    try:
        return row['id']
    except:
        return None

def extract_name(row):
    try:
        return row['name']
    except:
        return None
    
# se crean nuevas columnas con los id y name extraidos
eda['belongs_to_collection_id']=eda['belongs_to_collection'].apply(extract_id)
eda['belongs_to_collection_name']=eda['belongs_to_collection'].apply(extract_name)


# Eliminación columnas desanidadas
columnas_eliminar = ['belongs_to_collection', "genres", "production_countries", "production_companies", "spoken_languages"]
eda.drop(columns=columnas_eliminar, inplace=True)



        # SEGUNDO ARCHIVO


# Se carga el segundo archivo
eda2 = pd.read_csv(r"C:\Users\migue\OneDrive\Escritorio\credits.csv")

# se formatea columna cast y se desanida en los actores/actrices
eda2['cast'] = eda2['cast'].apply(convert_to_list_of_dicts)
eda2['cast_names'] = eda2['cast'].apply(lambda x: [d['name'] for d in x])

# se crea una función para extraer director de la columna crew
def extraer_nombre_director(lista_diccionarios):
  for diccionario in lista_diccionarios:
    if diccionario['job'] == 'Director':
      return diccionario['name']
  return None

# Se transforma crew a lista de dicc y se le aplica el extractor de director para crear nueva columna
eda2['crew'] = eda2['crew'].apply(convert_to_list_of_dicts)
eda2['director_name']=eda2['crew'].apply(extraer_nombre_director)

# se eliminan columnas cast y crew originales
columnas_eliminar = ['crew', 'cast']
eda2.drop(columns=columnas_eliminar, inplace=True)

# transformamos el dtype de columna 'id' a int64 para poder hacer merge
eda['id'] = eda['id'].astype('int64')

# Merge de eda y eda2 en un solo df
df = eda.merge(eda2, on='id', how='inner')



# funcion para obtener el día de la semana dada una fecha AAAA-mm-dd
def obtener_dia_semana(fecha):
    # Convertir la cadena de fecha en un objeto datetime
    fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    # Obtener el día de la semana como una cadena
    dia_semana = fecha_obj.strftime('%A')
    return dia_semana

# creo columna con los días de estreno
df['release_day']=df['release_date'].apply(obtener_dia_semana)




                    # Funciones


# definimos funcion que entrega cantidad de peliculas estrenadas en cierto dia
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
    
    df_dia = df[df['release_day']==dia1]
    cantidad_peliculas = df_dia.shape[0]

    print(f'{cantidad_peliculas} cantidad de peliculas fueron estrenadas en los días {dia}')


# funcion que calcula la cantidad de peliculas estrenadas en cierto mes
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
        print('debe colocar un mes correcto en español con mayuscula y sin tilde')

    df['release_date']=pd.to_datetime(df['release_date'])
    df["mes"] = df["release_date"].dt.month
    peliculas_mes = df[df["mes"] == mes1]
    numero_peliculas = peliculas_mes.shape[0]

    print(f'{numero_peliculas} cantidad de peliculas fueron estrenadas en el mes {mes}')


# Funcion que toma titulo y entrega titulo, fecha y score(popularity)
def score_titulo(titulo):
    df_titulo = df[df['title']==titulo]
    anio = df_titulo['release_year'].values[0]
    score = df_titulo['popularity'].values[0]

    print(f'La pelicula {titulo} fue estrenada en el año {anio} con un score/popularidad de {score}')


# Funcion que recibe titulo y entrega titulo, anio estreno, conteo de votaciones y promedio votaciones
def votos_titulo(titulo):
    if df['vote_count'].values[0]<2000:
        print ('La pelicula tiene menos de 2000 valoraciones. No se devuelve votos')
    else:
        df_titulo= df[df['title']==titulo]
        anio = df_titulo['release_year'].values[0]
        conteo = df_titulo['vote_count'].values[0]
        puntaje = df_titulo['vote_average'].values[0]
        print(f'La pelicula {titulo} fue estrenada en el año {anio}. La misma cuenta con {conteo} valoraciones, con un promedio de {puntaje}')



# funcion que recibe un actor y entrega cantidad de filmaciones y retorno
def get_actor(actor):

    df_filtrado = df[df['cast_names'].apply(lambda x: actor in x)]
    conteo = df_filtrado.shape[0]
    retorno_total = df_filtrado['return'].sum()
    if float(conteo)==0:
        print(f'El actor o actriz {actor} no ha participado en ninguna de estas peliculas')
    else:
        retorno_promedio = float(retorno_total)/float(conteo)
        print(f'El actor {actor} ha participado de {conteo} cantidad de filmaciones, el/la mismo/a ha conseguido un retorno de {retorno_total} con un promedio de {retorno_promedio} por filmacion')



# Funcion que recibe un director y da harta info
def get_director(director):
    df_filtrado = df[df['director_name']==director]
    retorno_total = df_filtrado['return'].sum()
    conteo = df_filtrado.shape[0]

    print(f'El/la Director/a {director} ha tenido un retorno total de {retorno_total} dolares')
    for i in range(0,conteo):
        print(f'dirigio {df_filtrado.iloc[i,10]}, estrenada el {df_filtrado.iloc[i,5]} que tuvo un retorno de {df_filtrado.iloc[i,13]} con un costo de {df_filtrado.iloc[i,0]} y una ganancia de {df_filtrado.iloc[i,6]}')
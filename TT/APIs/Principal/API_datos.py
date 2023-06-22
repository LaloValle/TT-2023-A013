import csv
import json
import numpy as np
from typing import List
from fastapi import FastAPI
from functools import reduce
from datetime import datetime
from pydantic import BaseModel
from rich.console import Console
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware

from LLibraries.ConsolaAPI import *

"""
    API Creación de conjunto de datos
    ---------------------------------
    La API proveé de 6 endpoints útiles para la prueba, recepción y conformación de las repeticiones de un gesto comunicadas
    desde el dispositivo sensor para la creación de un conjunto de datos.

    Esta API en particular es stateful, conserva el progreso durante la conformación de un conjunto de datos y finalmente
    almacena los resultados una vez se identifica que se han cumplido con el número de repeticiones para todos los gestos
    convirtiendo las mediciones en un archivo csv.
    
    ** La API no es capaz de identificar de manera única cada dispositivo sensor que la alimente, esto implica que se debe
    de tener precaución al consultar la API pues se estará agregando repeticiones al conjunto de datos en progreso actualmente,
    independiente de el número o consumidor que la utilice.

"""

##
## Variables globales
##
console = Console()
conjunto_datos_api = FastAPI()
monitor_sid = None
socket_manager = SocketManager(app=conjunto_datos_api)
# Configuraciones realacionadas a la creación del dataset
nombre_dataset = ''
MAXIMO_REPETICIONES = 20
numero_gesto = 0 # Gesto actual que se graba
repeticiones = 0 # Repeticiones del gesto actual realizadas
series_tiempo = dict()
with open('./LLibraries/Gestos.json') as file:
    gestos_cat = json.load(file)
RUTA_BASE = './Datasets'

## Configuración CORS
conjunto_datos_api.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost','http://192.168.1.66','http://192.168.1.67','http://192.168.1.68','http://192.168.1.142'],
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*']
)

##
##  Modelos JSON
##
class Serie(BaseModel):
    x : List[int]
    y : List[int]
    z : List[int]


##
##  Funciones auxiliares
##
def series_a_csv(agregar_fecha:bool=False):
    global series_tiempo, nombre_dataset, RUTA_BASE

    for eje in series_tiempo.keys():
        ruta = f'{RUTA_BASE}/{eje.upper()}-{nombre_dataset}'

        if agregar_fecha:
            fecha = datetime.now()
            fecha = f'_{fecha.day}-{fecha.month}-{fecha.year}_{fecha.hour}-{fecha.minute}'
            ruta +=  fecha
        ruta += '.csv'
        print(ruta)

        with open(ruta, 'w+') as archivo:
            escritura = csv.writer(archivo)
            escritura.writerows(series_tiempo[eje])

        mensaje_consola(f'Mediciones guardadas en [bold]\'{ruta}\'[/]')
def nombre_por_clase(clase):
    global gestos_cat
    for fonema in gestos_cat.keys():
        if gestos_cat[fonema]['clase'] == clase:
            return gestos_cat[fonema]['nombre']
def fonema_por_clase(clase):
    global gestos_cat
    for fonema in gestos_cat.keys():
        if gestos_cat[fonema]['clase'] == clase:
            return fonema
def configuracion_actual_conjunto(nueva_medicion:bool=False):
    global nombre_dataset, gestos_cat
    global numero_gesto, repeticiones, MAXIMO_REPETICIONES
    return {
        'name' : nombre_dataset,
        'phoneme' : fonema_por_clase(numero_gesto),
        'gesture' : numero_gesto,
        'repetitions' : repeticiones,
        'totalGestures' : len(list(gestos_cat.keys())),
        'totalRepetitions' : MAXIMO_REPETICIONES,
        'newSample' : nueva_medicion
    }

##
## Endpoint socket
##
# Recuperado:
#   https://stackoverflow.com/questions/67982780/bidirectional-communication-with-fastapi-fastapi-socketio-and-javascript-socket
#
async def socket_microbit_conectado():
    await conjunto_datos_api.sio.emit('microbit-connected',{})
    await socket_enviar_configuracion()
async def socket_enviar_configuracion(nueva_medicion:bool=False):
    await conjunto_datos_api.sio.emit('receive-configuration',configuracion_actual_conjunto(nueva_medicion))
async def socket_terminar_conexion():
    monitor_sid = None
    await conjunto_datos_api.sio.emit('sampling-ended',{})

@conjunto_datos_api.sio.on('current-configuration')
async def socket_obtener_configuracion(sid,peticion={'new':''}):
    global monitor_sid
    monitor_sid = sid
    if peticion['new']: await nuevo_dataset(peticion['new'])
    else: await retomar_dataset(True)
    await socket_enviar_configuracion()

##
##  Endpoints Dataset
##
@conjunto_datos_api.put('/datos-api/configuracion')
def configuracion_conjunto():
    global numero_gesto, repeticiones, nombre_dataset, series_tiempo
    mensaje_consola('Ingresa el nombre del conjunto')
    nombre_dataset = input('>>')
    mensaje_consola('Ingresa el número de gesto desde el que deseas iniciar')
    numero_gesto = int(input('>>'))
    mensaje_consola('Ingresa el número de repeticiones de este gesto desde el cual te gustaría iniciar la recolección')
    repeticiones = int(input('>>'))

    series_tiempo = {
        'x' : [],
        'y' : [],
        'z' : []
    }

@conjunto_datos_api.get('/datos-api/dataset')
async def nuevo_dataset(nombre : str = ''):
    """Indica la creación de un nuevo conjunto de datos y permite la configuración
    de las variables relacionadas al proceso y descripción del nuevo conjunto de
    datos.
    Realizada la solicitud a este método se interpreta como el inicio de la
    recopilación de los gestos realizados por una persona.

    Query
    =====
    nombre : str
        Nombre del conjunto de datos en conformación

    Return
    ======
    numero_gesto : str
        El número del siguiente tipo de gesto que debería ser ingresado
    """
    global monitor_sid
    global numero_gesto, repeticiones, nombre_dataset, series_tiempo
    numero_gesto = 1
    repeticiones = 0
    nombre_dataset = ''
    series_tiempo = {
        'x' : [],
        'y' : [],
        'z' : []
    }

    mensaje_consola('Reinicio para nueva configuración.')
    
    global console
    console.print('[bold] Nombre del nuevo dataset.')
    nombre_dataset = nombre if nombre else input('API >> ')
    mensaje_consola(f'[bold]{nombre}[/]')
    console.print('[bold] <--- Nuevo nombre asignado ---> [/]')

    if monitor_sid: await socket_obtener_configuracion(monitor_sid)
    return f'{str(numero_gesto)}:resp'

@conjunto_datos_api.post('/datos-api/dataset')
async def nueva_medicion(serie: Serie):
    """Método que registra las mediciones transmitidas desde el dispositivo sensor
    manteniendo un estado del número de repeticiones realizadas y el gesto actual
    que se esta grabando.
    Cuando el número de grabaciones por cada tipo de gesto se acompleta se reinicia
    el contador de gestos y se cambia el estado al tipo de gesto siguiente.

    Query
    =====
    serie : Serie
        Objeto JSON con llaves "x", "y" y "z" que tienen como valor un arreglo de
        enteros que son las mediciones muestreadas del gesto en cada eje

    Return
    ======
    gesto_siguiente : str
        Retorna el número del tipo de gesto siguiente que se debe grabar
    """
    global series_tiempo, nombre_dataset, monitor_sid
    global MAXIMO_REPETICIONES, repeticiones, numero_gesto, gestos_cat
    
    if not numero_gesto: return str(numero_gesto)
    serie = serie.dict()
    
    # Se agrega como primer valor la clase del gesto
    serie = {eje:[numero_gesto]+serie[eje] for eje in serie.keys()}
    mensaje_consola(f'[green italic]Número de mediciones: {len(serie["x"])-1}')

    repeticiones += 1
    mensaje_consola(f'[bold gold1]Gesto {numero_gesto}[/]: Recibida la [bold purple]repetición {repeticiones}[/].')

    # Se añade la serie de tiempo a cada lista según el eje
    series_tiempo = {eje:series+[serie[eje]] for eje,series in series_tiempo.items()}

    if repeticiones == MAXIMO_REPETICIONES:
        repeticiones = 0
        numero_gesto += 1 if numero_gesto<len(list(gestos_cat.keys())) else -numero_gesto

        # Se han grabado todos los gestos
        if numero_gesto == 0:
            # Los gestos se guardan en un archivo
            series_a_csv(True)
            # Se limpian las variables
            numero_gesto = 1
            repeticiones = 0
            nombre_dataset = ''
            series_tiempo = {
                'x' : [],
                'y' : [],
                'z' : []
            }
            if monitor_sid: await socket_terminar_conexion()
            return '0:resp'

        else: advertencia_consola(f'A continuación se inicia la grabación del gesto siguiente [blue bold]{nombre_por_clase(numero_gesto)}[/]')

    if monitor_sid: await socket_enviar_configuracion(True)
    return f'{str(numero_gesto)}:resp'

@conjunto_datos_api.put('/datos-api/dataset/guardar')
def guardar_conjunto_actual():
    series_a_csv(True)

@conjunto_datos_api.delete('/datos-api/dataset')
async def eliminar_ultima_medicion():
    """Elimina la última medición almacenada en el conjunto de datos
    """
    global repeticiones, numero_gesto, MAXIMO_REPETICIONES, series_tiempo

    series_tiempo = {eje:series[:-1] for eje,series in series_tiempo.items()}

    repeticiones -= 1
    if repeticiones == -1: 
        numero_gesto -= 1 if numero_gesto > 1 else 0
        repeticiones = MAXIMO_REPETICIONES - 1

    mensaje_consola(f'La ultima repetición registrada es la [bold purple]#{repeticiones}[/] para el [bold gold1]gesto {numero_gesto}[/].')
    if monitor_sid: await socket_obtener_configuracion(monitor_sid)

@conjunto_datos_api.post('/datos-api/dataset/prueba')
def probar_mediciones(serie: Serie):
    """Función utilizada para probar la correcta recepción de las series de tiempo

    Query
    =====
    serie : Serie
        Objeto JSON con llaves "x", "y" y "z" que tienen como valor un arreglo de
        enteros que son las mediciones muestreadas del gesto en cada eje

    Return
    ======
    exito_prueba : str
        Retorna si la prueba fue exitosa o ha fallado
    """
    try:
        mensaje_consola(''.join(serie['x']))
        mensaje_consola(''.join(serie['y']))
        mensaje_consola(''.join(serie['z']))
    except:
        error_consola('Falló en recibir correctamente la prueba')
    else:
        mensaje_consola('[green]Recepción correcta de prueba[/]')
    return f'1:resp'

@conjunto_datos_api.get('/datos-api/dataset/retomar')
async def retomar_dataset(socket:bool=False):
    """Permite retomar la grabación del conjunto de datos a partir del progreso
    actual de este.
    En ocasiones pueden ocurrir errores que interrumpan la grabación de los
    gestos de un sujeto durante la creación de un dataset, esta función permite
    indicar que se quiere retomar la grabación desde la penúltima grabación.

    Return
    ======
    gesto_siguiente : str
        Retorna el número del tipo de gesto siguiente que se debe grabar
    """
    global numero_gesto, repeticiones, nombre_dataset

    ## Se ha elegido retormar un dataset que sin embargo no había sido iniciali-
    ## zado o había terminado de grabarse correctamente
    if numero_gesto <= 1 and repeticiones == 0 and nombre_dataset == '':
        advertencia_consola('No existe un dataset en grabación.')
        return await nuevo_dataset()

    # Remueve la última medición registrada
    if not socket: eliminar_ultima_medicion()

    mensaje_consola(f'Se retoma el [bold gold1]gesto {numero_gesto}({nombre_por_clase(numero_gesto)})[/] en su última repetición [bold purple]#{repeticiones}[/]')
    
    if not socket and monitor_sid: await socket_microbit_conectado()
    return f'{str(numero_gesto)}:resp'

@conjunto_datos_api.get('/datos-api/dataset/grabado')
def mostrar_dataset():
    """ADMINISTRACIÓN - Realiza una impresión del estado actual de la API y el conjunto de datos
    en progreso
    """
    global nombre_dataset, series_tiempo
    if nombre_dataset: mensaje_consola(f'Nombre del Dataset: [bold green] {nombre_dataset} [/]')
    mensaje_consola('[bold]Mediciones X:[/]' + reduce(lambda acc,serie: acc + str(serie), series_tiempo['x'], ''))
    mensaje_consola('[bold]Mediciones X:[/]' + reduce(lambda acc,serie: acc + str(serie), series_tiempo['y'], ''))
    mensaje_consola('[bold]Mediciones X:[/]' + reduce(lambda acc,serie: acc + str(serie), series_tiempo['z'], ''))
import csv
from distutils.log import error
import numpy as np
from fastapi import FastAPI
from datetime import datetime
from rich.console import Console

##
## Variables globales
##
console = Console()
raspi_api = FastAPI()
# numero_palabras = 10
# niveles_discretizacion = 5
nombres_gestos = ('hh', 'hu', 'hud', 'hh2', 'hu2', 'ud')
# Configuraciones realacionadas a la creación del dataset
MAXIMO_REPETICIONES = 10
numero_gesto = 0 # Gesto actual que se graba
repeticiones = 0 # Repeticiones del gesto actual realizadas
mediciones_x, mediciones_y, mediciones_z = [], [], []


##
## Funciones auxiliares
##
def mensaje_consola(mensaje):
    global console
    console.print(f'[bold cyan]API:[/]      {mensaje}')
def error_consola(mensaje):
    global console
    console.print(f'[bold red]ERROR:[/]     {mensaje}')
def advertencia_consola(mensaje):
    global console
    console.print(f'[bold gold1]ADVERTENCIA:        {mensaje}')
def cadena_a_lista(cadena, enteros:bool=True):
    return list(map(int if enteros else str, cadena[1:-1].split(',')))
def lista_a_csv(lista, ruta, agregar_fecha:bool=False):
    if agregar_fecha:
        fecha = datetime.now()
        fecha = f'_{fecha.day}-{fecha.month}-{fecha.year}_{fecha.hour}-{fecha.minute}'
        ruta +=  fecha
    ruta += '.csv'

    with open(ruta, 'w+') as archivo:
        escritura = csv.writer(archivo)
        escritura.writerows(lista)

    mensaje_consola(f'Mediciones guardas en [bold]\'{ruta}\'[/]')


##
## Endpoints Dataset
##
@raspi_api.get('/raspi-api/dataset/grabado')
def mostrar_dataset():
    mensaje_consola('[bold]Mediciones X:[/]' + str(mediciones_x))
    mensaje_consola('[bold]Mediciones Y:[/]' + str(mediciones_y))
    mensaje_consola('[bold]Mediciones Z:[/]' + str(mediciones_z))

@raspi_api.post('/raspi-api/dataset/prueba')
def probar_mediciones(x: str, y: str, z: str):
    """Función utilizada para probar la correcta recepción de las series de tiempo

    Query
    =====
    x : str
        Representación en una cadena de los valores de la medición del aceleró-
        metro en el eje X
    y : str
        Representación en una cadena de los valores de la medición del aceleró-
        metro en el eje Y
    Z : str
        Representación en una cadena de los valores de la medición del aceleró-
        metro en el eje Z

    Return
    ======
    exito_prueba : str
        Retorna si la prueba fue exitosa o ha fallado
    """
    try:
        mensaje_consola(''.join(cadena_a_lista(x,enteros=False)))
        mensaje_consola(''.join(cadena_a_lista(y,enteros=False)))
        mensaje_consola(''.join(cadena_a_lista(z,enteros=False)))
    except:
        error_consola('Falló en recibir correctamente la prueba')
        return str(0)
    else:
        mensaje_consola('[green]Recepción correcta de prueba[/]')
    return str(1)
        

@raspi_api.get('/raspi-api/dataset/retomar')
def retomar_dataset():
    """En ocasiones pueden ocurrir errores que interrumpan la grabación de los
    gestos de un sujeto durante la creación de un dataset, esta función permite
    indicar que se quiere retomar la grabación desde la penúltima grabación.
    """
    global numero_gesto, repeticiones
    global mediciones_x, mediciones_y, mediciones_z

    ## Se ha elegido retormar un dataset que sin embargo no había sido iniciali-
    ## zado o había terminado de grabarse correctamente
    if numero_gesto == 0 and repeticiones == 0:
        advertencia_consola('No existe un dataset en grabación.')
        return nuevo_dataset()

    mediciones_x.pop()
    mediciones_y.pop()
    mediciones_z.pop()

    if repeticiones == 0:
        numero_gesto -= 1
        repeticiones = MAXIMO_REPETICIONES - 1
    else: repeticiones -= 1

    return str(numero_gesto)
@raspi_api.get('/raspi-api/dataset')
def nuevo_dataset():
    """Cuando el microbit realice la solicitud a este método entonces se entien-
    de como el inicio de la recopilación de los gestos realizados por una persona.
    Cabe mencionar que el proceso de recopilación es 'Stateful' y este método
    funciona para configurar las variables en estado inicial.
    """
    global numero_gesto, repeticiones
    numero_gesto = 1
    repeticiones = 0
    mediciones_x.clear()
    mediciones_y.clear()
    mediciones_z.clear()

    mensaje_consola('Reinicio para nueva configuración.')

    return str(numero_gesto)

@raspi_api.post('/raspi-api/dataset')
def nueva_medicion(x: str, y: str, z: str):
    """Método que registra las mediciones transmitidas desde el microbit, mante-
    niendo un estado del número de repeticiones realizadas y el gesto actual que
    se esta grabando.
    Cuando el número de grabaciones por cada tipo de gesto se acompleta se reini-
    cia el contador de gestos y se cambia el estado al tipo de gesto siguiente.

    Query
    =====
    x : str
        Representación en una cadena de los valores de la medición del aceleró-
        metro en el eje X
    y : str
        Representación en una cadena de los valores de la medición del aceleró-
        metro en el eje Y
    Z : str
        Representación en una cadena de los valores de la medición del aceleró-
        metro en el eje Z

    Return
    ======
    gesto_siguiente : str
        Retorna el número del tipo de gesto siguiente que se debe grabar
    """
    global mediciones_x, mediciones_y, mediciones_z
    global MAXIMO_REPETICIONES,repeticiones, numero_gesto, nombres_gestos
    
    if not numero_gesto: return str(numero_gesto)
    
    # Se convierte la cadena a una lista de valores enteros y se agrega como
    # primer elemento la clase de la serie de tiempo
    mediciones_x.append([numero_gesto] + cadena_a_lista(x))
    mediciones_y.append([numero_gesto] + cadena_a_lista(y))
    mediciones_z.append([numero_gesto] + cadena_a_lista(z))
    mensaje_consola(f'[green italic]Número de mediciones: {len(mediciones_x[-1])}')

    repeticiones += 1
    mensaje_consola(f'[bold gold1]Gesto {numero_gesto}[/]: Recibida la [bold purple]repetición {repeticiones}[/].')

    if repeticiones == MAXIMO_REPETICIONES:
        repeticiones = 0
        numero_gesto += 1 if numero_gesto<len(nombres_gestos) else -numero_gesto

        # Se han grabado todos los gestos
        if numero_gesto == 0:
            # Los gestos se guardan en un archivo
            lista_a_csv(mediciones_x, './Dataset/mediciones_x', True)
            lista_a_csv(mediciones_y, './Dataset/mediciones_y', True)
            lista_a_csv(mediciones_z, './Dataset/mediciones_z', True)

    return str(numero_gesto)

@raspi_api.delete('/raspi-api/dataset')
def eliminar_ultima_medicion():
    """Permite eliminar la última medición guardada en el dataset
    """
    mediciones_x.pop()
    mediciones_y.pop()
    mediciones_z.pop()

    mensaje_consola('Ultima medición elminada')

# @raspi_api.patch('/raspi-api/dataset')
# def concatenar_muestreos(x: str, y: str, z: str):
#     """Método utilizado para agregar muestreos pertenecientes a la última serie
#     de tiempo multivariable, de forma que estas se concatenan y no se crea una
#     nueva serie.

#     Query
#     =====
#     x : str
#         Representación en una cadena de los valores de la medición del aceleró-
#         metro en el eje X
#     y : str
#         Representación en una cadena de los valores de la medición del aceleró-
#         metro en el eje Y
#     Z : str
#         Representación en una cadena de los valores de la medición del aceleró-
#         metro en el eje Z

#     Return
#     ======
#     gesto_actual : str
#         Retorna el número del tipo de gesto actual que se graba
#     """
#     global numero_gesto
#     global mediciones_x, mediciones_y, mediciones_z

#     mediciones_x[-1] += cadena_a_lista_enteros(x)
#     mediciones_y[-1] += cadena_a_lista_enteros(y)
#     mediciones_z[-1] += cadena_a_lista_enteros(z)

#     mensaje_consola(f'[green italic]Número de mediciones: {len(mediciones_x[-1])}')

#     return str(numero_gesto)


##
## Endpoints método SAX-DTW-Features
##

##
## Endpoints antiguos
##
""" @raspi_api.get('/raspberry/{ip}', response_model=ParametrosSAX)
def configuracion_inicial(ip:str):
    global ip_microbit

    if not re.findall('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',ip):
        raise HTTPException(status_code=400, detail='El formato de la IP es incorrecta')
    
    ip_microbit = ip
    return ParametrosSAX()

@raspi_api.post('/raspberry')
def parametros_post(x: str, y: str, z: str):
    series_tiempo = pd.DataFrame()
    series_tiempo['x'] = x[1:-1].split(',')
    series_tiempo['y'] = y[1:-1].split(',')
    series_tiempo['z'] = z[1:-1].split(',')
    print(series_tiempo)
    return 'A'

@raspi_api.get('/raspberry/traduccion/texto')
def traducir_a_texto(vector_x: str, vector_y: str, vector_z: str):
    return f'Recibidos:{vector_x},{vector_y},{vector_z}' """
import time
import json
import socket
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware

from LLibraries.SAXDTWF import *
from LLibraries.ConsolaAPI import *
from LLibraries.Ortografia import palabra_correcta
from LLibraries.Phonemes import phonemes_to_gestures

##
## Variables globales
##
traduccion_gestos_api = FastAPI()
with open('./LLibraries/Gestos.json') as file:
    gestos_cat = json.load(file)
# Servidor
PUERTO = 3276
IP_SERVIDOR = 'localhost'
PUERTO_RASPBERRY = 9327
IP_RASPBERRY = '192.168.1.76'

speaker = ''
monitor_sid = None
microbit_conectado = False
raspberry_conectado = False
traduciendo = 'phoneme' # Por defecto el gesto representa un fonema pero puede cambiarse a 'palabra' para representar a una palabra asociada al gesto
socket_manager = SocketManager(app=traduccion_gestos_api)



##
##  Funciones auxiliares
##
RUTA_MODELO = './Traductor/Modelo'
traductor = None
def recuperar_modelo(configuracion:str=''):
    global traductor
    traductor = SAXDTWF(configuracion)
    traductor.autoconfigure()
def enviar_servidor(mensaje):
    global IP_SERVIDOR, PUERTO
    tcp_socket = socket.create_connection((IP_SERVIDOR, PUERTO))
    response = ''
    
    try:
        data = str.encode(mensaje)
        tcp_socket.sendall(data)
        response = tcp_socket.recv(1024).decode('utf8')
    except:
        error_consola('Falló la conexión o el envío del mensaje')
    finally:
        mensaje_consola('Mensaje enviado exitosamente')
        tcp_socket.close()
    return response
def enviar_raspberry(mensaje):
    global IP_RASPBERRY, PUERTO_RASPBERRY
    tcp_socket = socket.create_connection((IP_RASPBERRY, PUERTO_RASPBERRY))
    response = ''
    
    try:
        data = str.encode(mensaje)
        tcp_socket.sendall(data)
        response = tcp_socket.recv(1024).decode('utf8')
    except:
        error_consola('Falló la conexión o el envío del mensaje')
    finally:
        mensaje_consola('Mensaje enviado exitosamente')
        tcp_socket.close()
    return response
def fonema_por_clase(clase):
    global gestos_cat
    for fonema in gestos_cat.keys():
        if gestos_cat[fonema]['clase'] == clase:
            return fonema

## Configuración CORS
traduccion_gestos_api.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost','http://192.168.1.66','http://192.168.1.64','http://192.168.1.67','http://192.168.1.68','http://192.168.1.142'],
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
## Endpoints socket
##
async def socket_cadena_fonemas(fonemas,onlyPhoneme=False):
    if not onlyPhoneme: palabra,correcta = palabra_correcta_fonemas(fonemas)
    if onlyPhoneme: 
        respuesta = {'phonemes':fonemas}
    else:
        respuesta = {
            'phonemes' : fonemas,
            'word' : '' if onlyPhoneme else palabra.capitalize() if type(palabra) == 'str' else ''.join(palabra).capitalize(),
            'correct' : correcta
        }
    await traduccion_gestos_api.sio.emit('predicted-phonemes',respuesta)
async def socket_microbit_conectado():
    await traduccion_gestos_api.sio.emit('microbit-connected',{})
async def socket_raspberry_conectado():
    await traduccion_gestos_api.sio.emit('raspberry-connected',{})
async def socket_reproduccion_finalizada():
    time.sleep(3)
    await traduccion_gestos_api.sio.emit('playback-finished',{})
async def socket_palabra_correcta(correccion):
    await traduccion_gestos_api.sio.emit('correct-word',correccion)

@traduccion_gestos_api.sio.on('current-configuration')
async def socket_configuracion_actual(sid,peticion={'path' : 'd'}):
    global monitor_sid, microbit_conectado, speaker
    monitor_sid = sid
    await definir_configuracion(peticion['path'],True)
    if 'speaker' in peticion.keys(): speaker = peticion['speaker']
    if microbit_conectado: await socket_microbit_conectado()
    if raspberry_conectado: await socket_raspberry_conectado()
@traduccion_gestos_api.sio.on('playback-voice')
async def socket_reproducir_voz(sid,peticion):
    try:
        palabra,correcta = palabra_correcta(peticion['phonemes'])
        respuesta = enviar_raspberry(
            json.dumps(
                {
                    'word': palabra
                },
                default=int
            )
        )
        await socket_reproduccion_finalizada()
    except:
        error_consola('Falló al mandar la reproducción a Raspberry')
@traduccion_gestos_api.sio.on('phonemes-word')
async def socket_palabra_fonemas(sid,peticion):
    palabra,correcta = palabra_correcta_fonemas(peticion['phonemes'])
    await socket_palabra_correcta({'word':palabra.capitalize(), 'correct':correcta})
@traduccion_gestos_api.sio.on('set-speaker')
def socket_set_speaker(sid,peticion):
    global speaker
    if peticion['speaker'] != speaker:
        speaker = peticion['speaker']
        mensaje_consola(f'Sintetizador de voz actualizado - [bold]{speaker}[/]')
@traduccion_gestos_api.sio.on('set-translating-type')
def socket_set_translating_type(sid,peticion):
    global traduciendo
    traduciendo = peticion['translating']
    mensaje_consola(f'Traducción cambiada a >>{traduciendo}')

##
## Endpoints Dataset
##
# Endpoints configuración
@traduccion_gestos_api.put('/configuracion')
async def definir_configuracion(ruta_configuracion:str='',socket:bool=False):
    global traductor, microbit_conectado
    if traductor != None:
        # Se trata de la conexión del micro:bit
        if not socket:
            mensaje_consola(f'[bold]micro:bit[/] conectado ...')
            microbit_conectado = True
            if monitor_sid: await socket_microbit_conectado()
            return '1:resp'
    # Ruta para el archivo de configuración del método de reconocimiento de gestos
    if not ruta_configuracion:
        mensaje_consola('Ingresa la ruta del archivo de configuración para el método SAX-DTW [purple]([bold]d[/] para el modelo por defecto, [bold]x[/] para salir)[/]')
        ruta_configuracion = input('>> ')

    if ruta_configuracion == 'x': return False
    if ruta_configuracion == 'd': ruta_configuracion = f'{RUTA_MODELO}/Configuracion.json'

    try:
        recuperar_modelo(ruta_configuracion)
        mensaje_consola(f'[bold] <--- Se ha recuperado el modelo con la configuración ingresada ---> [/]')
        
        if monitor_sid: await traduccion_gestos_api.sio.emit('configured',{})
        return '1:resp'
    except:
        error_consola('Fallo al recuperar el modelo')
        return '0:resp'

# Endpoints traducción
@traduccion_gestos_api.post('/traducir/gesto')
async def traducir_gesto(serie : Serie,fonema:str='',palabra:str=''):
    global traductor, gestos_cat, monitor_sid, speaker

    serie = serie.dict()
    if len(serie['x']) < 18: 
        advertencia_consola('El muestreo fue demasiado corto para ser identificado')
        enviar_servidor(json.dumps({'failed':True}))
        return '-:resp'

    gesto = traductor.ready_time_series(serie)
    clase = traductor.predict_label(gesto,has_label=False,verbose=False)[0]
    traducido = fonema_por_clase(clase)
    mensaje_consola(f'Gesto identificado ({clase})\'[bold cyan]{gestos_cat[traducido]["nombre"]}[/]\'')
    
    # Si lo que se traduce es una palabra en vez de solo un fonema
    if traduciendo == 'word': 
        fonema = traducido
        traducido = gestos_cat[fonema]['palabra']['escritura']
        print('Palabra >> ',traducido)
        await socket_palabra_correcta({'word':traducido.capitalize(), 'correct':True})

    peticion = {'speaker' : speaker}
    peticion[traduciendo] = traducido
    print('Peticion >>',peticion)

    respuesta = enviar_servidor(json.dumps( peticion,default=int))
    if monitor_sid: await socket_cadena_fonemas(respuesta,traduciendo == 'word')
    return f'{respuesta[-1]}:resp'
    # try:
    # except:
    #     error_consola('Comunicación con servidor falló')
    #     return '-:resp'

# Endpoints fonemas
@traduccion_gestos_api.head('/fonemas/gestos')
def gestos_fonemas(fonemas : str):
    
    lista_fonemas = [fonema for fonema in fonemas]
    print(lista_fonemas)
    gestos = phonemes_to_gestures(lista_fonemas)
    
    mensaje_consola(f'Gestos para los fonemas [cyan]{fonemas}[/]')
    mensaje_consola('\n -'+'\n -'.join(gestos))
@traduccion_gestos_api.get('/fonemas/palabra')
def palabra_correcta_fonemas(fonemas : str):
    retorno = palabra_correcta([f for f in fonemas])
    return retorno

# Endpoints reproducción
@traduccion_gestos_api.head('/reproducir/gesto')
def reproducir_gesto(serie : Serie):
    global traductor, gestos_cat, speaker

    gesto = traductor.ready_time_series(serie.dict())
    clase = traductor.predict_label(gesto,has_label=False,verbose=False)[0]
    fonema = fonema_por_clase(clase)

    mensaje_consola(f'Gesto identificado ({clase})\'[bold cyan]{gestos_cat[fonema]["nombre"]}[/]')

    try:
        enviar_servidor(
            json.dumps(
                {
                    'speak' : True,
                    'speaker' : speaker,
                    'phoneme': fonema
                },
                default=int
            )
        )
        return f'{fonema[-1]}:resp'
    except:
        error_consola('Comunicación con servidor falló')
        return f'-:resp'
@traduccion_gestos_api.head('/reproducir/texto')
def reproducir_texto(texto:str):
    global speaker
    try:
        enviar_servidor(
            json.dumps(
                {
                    'speak' : True,
                    'speaker' : speaker,
                    'text': texto
                },
                default=int
            )
        )
    except:
        error_consola('Comunicación con servidor falló')
@traduccion_gestos_api.put('/reproducir/palabra')
def reproducir_palabra_actual():
    global speaker
    try:
        enviar_servidor(
            json.dumps(
                {
                    'speak' : True,
                    'speaker' : speaker
                },
                default=int
            )
        )
    except:
        error_consola('Comunicación con servidor falló')
    return 'o:resp'

# Endpoints servidor raspberry
@traduccion_gestos_api.put('/raspberry/limpiar')
def limpiar_cadena_raspberry():
    enviar_servidor(
        json.dumps({
            'clear' : True
        })
    )
    return 'o:resp'
@traduccion_gestos_api.delete('/raspberry/ultimo')
async def eliminar_ultimo_phonema():
    try:
        respuesta = enviar_servidor(
            json.dumps({
                'remove_last' : True
            })
        )
        if monitor_sid: await socket_cadena_fonemas(respuesta)
    except:
        error_consola('Falló al eliminar el último fonema')
    finally:    
        return 'o:resp'
@traduccion_gestos_api.patch('/raspberry/modificar_espera')
def modificar_espera_raspberry(espera:int=5):
    enviar_servidor(
        json.dumps({
            'set_waiting' : espera
        })
    )
@traduccion_gestos_api.put('/raspberry/cerrar')
def terminar_raspberry():
    enviar_servidor(
        json.dumps({
            'close' : True
        })
    )
@traduccion_gestos_api.put('/raspberry/conexion')
async def conexion_raspberry():
    global raspberry_conectado
    mensaje_consola('[bold purple]Raspberry[/] conectada ...')
    raspberry_conectado = True
    await socket_raspberry_conectado()
    return 'correcto'
@traduccion_gestos_api.put('/raspberry/reproduccion-finalizada')
async def reproduccion_finalizada():
    await socket_reproduccion_finalizada()
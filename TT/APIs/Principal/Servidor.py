import os
import json
import time
import socket
import threading
from random import randint
from functools import reduce
from LLibraries.ConsolaAPI import *
from LLibraries.Ortografia import palabra_correcta

##
##  Constants and global variables
##
PORT = 3276
IP_ADDR = 'localhost'
IP_RASPBERRY = '192.168.1.76'
PUERTO_RASPBERRY = 9327
WAIT_TO_PLAY = 5 # Seconds before reproducing the word
speaker = ''
word = []

# Control variables with thread
time_elapsed = 0                # Time count for the thread timer
end_server = False              # Finishes the server
current_thread = None           # The current running thread
added_to_word = False           # Flag used to restart the time_elapsed while composing the word
composing_word = False          # Active while new phonemes and words can be added
start_word_composing = False    # Flag to create the thread in the main loop

##
## Auxiliar functions
##
def process_request(connection) -> dict:
    data_string = ''; data_dict = dict()

    # Receive bytes as long as the client is sending something
    while True:
        # Reception
        data = connection.recv(1024)
        data_string += data.decode('utf8')
        if not data: break
        # Processing
        if data_string:
            mensaje_consola_plano('[green]Datos recibidos correctamente[/]')
            data_dict = json.loads(data_string)
            response = process_message(data_dict)
            connection.sendall(word_to_text(response).encode() if response else '-'.encode())
            data_string = ''
    try:
        pass
    except:
        error_consola('Durante la recepción del mensaje desde el cliente')
    finally:
        connection.close()
        return data_dict
def start_word_compose() -> threading.Thread:
    global start_word_composing,composing_word

    start_word_composing = False
    composing_word = True

    return threading.Thread(target=compose_word)
def enviar_servidor_raspberry(mensaje,recibirRespuesta=False):
    global IP_RASPBERRY, PUERTO_RASPBERRY
    tcp_socket = socket.create_connection((IP_RASPBERRY, PUERTO_RASPBERRY))
    respuesta = None
    
    try:
        data = str.encode(mensaje)
        tcp_socket.sendall(data)
        if recibirRespuesta: respuesta = json.loads(tcp_socket.recv(1024).decode('utf8'))
    except:
        error_consola('Falló la conexión o el envío del mensaje')
    finally:
        tcp_socket.close()
        return respuesta
    

def conectar_raspberry():
    mensaje_consola('Solicitando la conexión con la [purple]Raspberry[/] ...')
    respuesta = None

    while True:
        respuesta = enviar_servidor_raspberry(
            json.dumps(
                { 'conexion' : False }
            ),
            True
        )
        if respuesta:
            print(respuesta)
            break

    mensaje_consola('Raspberry conectada')

##
##  Actions
##
def word_to_text(word):
    text = str(reduce(lambda text,w: text + (w if len(w) == 1 else f'{w} '),word,''))
    if text[-1] == ' ': text = text[:-1]
    return text
def clean_word():
    global word
    word = []
def remove_last():
    global word, time_elapsed
    removed = word.pop()
    if len(removed) <= 2: advertencia_consola(f'Removed last phoneme \'{removed}\'')
    else: advertencia_consola('Removed last text added')
    time_elapsed = time.time()
def reproduce(text):
    global speaker
    mensaje_consola(f'[bold]{text}[/]\n',programa='Raspberry')
    request = {'word':text,'speaker':speaker}
    if speaker != 'coqui':
        enviar_servidor_raspberry(json.dumps(request))
    else:
        # enviar_servidor_coqui(json.dumps(request))
        pass
def reproduce_word():
    global word
    correct_word,_ = palabra_correcta(word)
    mensaje_consola(f'[bold]{"".join(word)}[/]',programa='Fonemas')
    mensaje_consola(f'[bold]{"".join(correct_word)}[/]',programa='Palabra')
    request = {'word':correct_word,'speaker':speaker}
    if speaker != 'coqui':
        enviar_servidor_raspberry(json.dumps(request))
    else:
        # enviar_servidor_coqui(json.dumps(request))
        pass
    clean_word()
def add_phoneme(phoneme):
    global word, added_to_word
    global composing_word, start_word_composing
    word.append(phoneme)
    added_to_word = True
    # If there's no thread running then is requested
    if not composing_word: start_word_composing = True


def process_message(message:dict):
    '''The message received must be a dictionary, and in function of the keys found the following actions are performed:
        Data
        ====
            - phoneme : Response when predicting a gesture sampled by the sending node. The phoneme gets added to the in-composing-process word
            - text : A full text gets received. The text gets added to the in-composing-process word

        Flags
        -----
            - remove_last : Removes the last element added to the word. The phoneme or text string is received as value to be removed
            - speak : Added together with "phoneme" or "word". The phoneme or word gets reproduce
            - clear : Cleans the current word
            - set_waiting : Sets the time that must elapsed before reproducing the composing word
            - close : Finishes the server
    '''
    global WAIT_TO_PLAY, time_elapsed
    global end_server
    global word, speaker

    list_keys = list(message.keys())
    if 'speaker' in list_keys:
        if message['speaker'] != speaker:
            speaker = message['speaker']
            mensaje_consola(f'Speaker updated : [bold]{speaker}[/]')

    if 'failed' in list_keys:
        time_elapsed = time.time()
        return []
    if 'close' in list_keys: 
        end_server = True
        advertencia_consola('Finishing server')
        return ['Server finished']
    elif 'remove_last' in list_keys: 
        if word: remove_last()
        return list(word)
    elif 'set_waiting' in list_keys: 
        WAIT_TO_PLAY = message['set_waiting']
        mensaje_consola(f'<--- Changed waiting time while composing word to {message["set_waiting"]}sec --->',programa='Raspberry')
        return ['Waiting changed']
    elif 'clear' in list_keys: 
        clean_word()
        return ['Cleared']
    elif 'speak' in list_keys: 
        if 'phoneme' in list_keys: reproduce(message['phoneme'])
        elif 'word' in list_keys: reproduce(message['word'])
        else: time_elapsed = time.time() - (WAIT_TO_PLAY*2) # Makes the current word being composed to be reproduce
        return ['Reproduced']
    elif 'word' in list_keys:
        add_phoneme(message["word"])
        return list(word)
    elif 'phoneme' in list_keys: 
        add_phoneme(message['phoneme'])
        return list(word)

##
##  Tread function
##
def compose_word():
    global added_to_word,composing_word
    global WAIT_TO_PLAY,word
    global time_elapsed

    time_elapsed = time.time()
    while time.time()-time_elapsed <= WAIT_TO_PLAY:
        if added_to_word:
            added_to_word = False
            mensaje_consola_plano(f'[cyan]Tiempo reiniciado ...[/]')
            time_elapsed = time.time()

    if len(word) > 0 :
        if max(list(reduce(lambda acc,w: acc+[len(w)],word,[]))) == 1:
            # Reproduce palabra de fonemas
            reproduce_word()
        else:
            reproduce(word_to_text(word))
            word = []
    composing_word = False

def main():
    global word
    global end_server
    global IP_ADDR, PORT
    global composing_word, current_thread, start_word_composing

    #enviar_servidor_raspberry(json.dumps({'word':'Raspberry conectada','speaker':'piper'}))
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to server address and port
    server_address = (IP_ADDR, PORT)
    tcp_socket.bind(server_address)
    # Listen on port
    tcp_socket.listen(1)
    mensaje_consola(f'<--- Servidor iniciado en [bold]{IP_ADDR}:{PORT}[/] --->\n',programa='Servidor')

    # Intentando la conexión con la Raspberry
    #conectar_raspberry()

    while True:
        mensaje_consola_plano('\n[purple]Esperando nueva conexión ...[/]')
        connection,_ = tcp_socket.accept()
        
        process_request(connection)

        if start_word_composing:
            current_thread = start_word_compose()
            current_thread.start()
            advertencia_consola('Iniciada la ejecución de un nuevo hilo')
        if not composing_word and current_thread != None:
            current_thread.join()
            current_thread = None
        if end_server: break
    
    if current_thread != None: current_thread.join()

if __name__ == '__main__': main()
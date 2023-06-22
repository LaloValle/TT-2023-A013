import os
import json
import socket
import requests
import subprocess
from random import randint

## Variables globales
PORT = 9327
IP_ADDR = '192.168.1.76'

PORT_API = 6614
IP_API = '192.168.1.74'


##
## Auxiliar functions
##
def play(audio_path):
    os.system(f'mpg321 {audio_path}.mp3')

## Message reception y processing
def recover_message(connection) -> dict:
    data_string = ''; data_dict = dict()
    try:
        # Receive bytes as long as the client is sending something
        while True:
            data = connection.recv(256)
            data_string += data.decode('utf8')
            if not data: break
            if data_string: connection.sendall('received'.encode())
        data_dict = json.loads(data_string)
    except:
        print('Error >>  Durante la recepción del mensaje desde el cliente')
    finally:
        connection.close()
        return data_dict
def procesar_fonemas_audio(palabra,speaker):
    palabra = palabra.replace(' ','_')
    nombre_audio = f'./Audios/{palabra}'

    if speaker == 'piper':
        audios_existentes = subprocess.check_output(['ls','./Audios']).decode().split('\n')
        # Verifica si la palabra ya existe
        if f'{palabra}.mp3' in audios_existentes:
            play(nombre_audio)
        # Se genera el audio de la palabra
        else:
            os.system(f"echo '{palabra}' | ./piper/piper --model ./Voces/es-carlfm-x-low.onnx --output_file {nombre_audio}.wav")
            os.system(f'ffmpeg -i {nombre_audio}.wav -acodec mp3 {nombre_audio}.mp3')
            os.system(f'rm {nombre_audio}.wav')
            play(nombre_audio)

## Raspberry Conection
def anunciar_conexion():
    global IP_API, PORT_API
    print('Anunciando conexión ...')
    respuesta = requests.put(f'http://{IP_API}:{PORT_API}/raspberry/conexion')
    while respuesta.text != '"correcto"': pass
    print('<--- Conexión correcta --->\n')
    play('./Audios/conectada')
def anunciar_finalizada_reproduccion():
    global IP_API, PORT_API
    print('Anunciando conexión ...')
    respuesta = requests.put(f'http://{IP_API}:{PORT_API}/raspberry/reproduccion-finalizada')


def main():
    global PORT, IP_ADDR

    anunciar_conexion()
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to server address and port
    server_address = (IP_ADDR, PORT)
    tcp_socket.bind(server_address)
    # Listen on port
    tcp_socket.listen(1)
    print(f'<--- Servidor iniciado en {IP_ADDR}:{PORT} --->\n')

    while True:
        print('Raspberry >>  Esperando nueva conexión ...')
        connection,_ = tcp_socket.accept()
        
        message = recover_message(connection)
        print('Raspberry >>  Datos recibidos correctamente')
        print(message)

        procesar_fonemas_audio(message['word'],message['speaker'])

if __name__ == '__main__': main()

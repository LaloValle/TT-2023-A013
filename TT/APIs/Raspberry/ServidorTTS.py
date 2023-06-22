from TTS.api import TTS

INDEX_MODEL = 0

# List available 🐸TTS models and choose the first one
model_name = TTS.list_models()
spanish_models = [i for i,name in enumerate(model_name) if name.find('/es/') > 0]

tts = TTS(model_name[spanish_models[INDEX_MODEL]])
tts.tts_to_file(text="El zorro corrio hasta escurrirse debajo de la valla", file_path='./zorro2.wav')

import json
import socket
from random import randint

##
## Auxiliar functions
##
def recover_message(connection) -> dict:
    data_string = ''; data_dict = dict()
    try:
        # Receive bytes as long as the client is sending something
        while True:
            data = connection.recv(256)
            data_string += data.decode('utf8')
            if not data: break
        data_dict = json.loads(data_string)
    except:
        print('Error >>  Durante la recepción del mensaje desde el cliente')
    finally:
        connection.close()
        return data_dict



def main():
    global word
    global end_server
    global composing_word, current_thread, start_word_composing

    PORT = 7431
    IP_ADDR = '192.168.10.4'
    PORT_RASPBERRY = 9327
    RASPBERRY_PATH = '~/TT/Audios'


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

if __name__ == '__main__': main()
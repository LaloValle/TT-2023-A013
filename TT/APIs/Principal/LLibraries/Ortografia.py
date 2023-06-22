# Las funciones de sustitución ortográfica identifican un fonema en especial y según las reglas del español se sustituye por la grafía asociada correcta.
# Todas las funciones regresan 2 valores aunque algunas palabras de fonemas no requieren el último:
#   1. Palabra con la sustitución ortográfica
#   2. Requiere de una comparación de corrección ortográfica para asegurar la forma correcta de escritura en el español, esto debido a que existen más de 1 posible sustitución con las reglas del fonema.
#       Lista con tuplas con elementos:
#           0 : Índice de la palabra
#           1 : Lista de subsecuentes posibles grafías(con la que se retorna la palabra también debe verificarse)
import json
import numpy as np
from autocorrect import Speller
from functools import reduce

##  Globales
spell = Speller(lang='es')
VOCALES = ['a','e','i','o','u']
encontrar_indices = lambda fonema,palabra: [i for i,letra in enumerate(palabra) if letra == fonema ]
cat_fonemas = []
with open('./LLibraries/Gestos.json') as archivo:
    cat_fonemas = json.load(archivo)

##
##  Reglas del fonema 'b'
##
def b(palabra : list) -> list:
    indices = encontrar_indices('b',palabra)
    comparaciones_ortograficas = []

    for i in indices:
        # Terminaciones de 'b'
        if ''.join(palabra[i+1:]) in ['a','as','amos','ais','an']: palabra[i] = 'b'
        if i < (len(palabra)-1): 
            if palabra[i+1] in ['b','d','n']: palabra[i] = 'v'
        else: palabra[i] = 'b'; comparaciones_ortograficas.append((i,['v']))
    return palabra,comparaciones_ortograficas
##
##  Reglas del fonema 'g'
##
def g(palabra : list) -> list:
    indices = encontrar_indices('g',palabra)

    for i in indices:
        if i < (len(palabra)-1):
            if palabra[i+1] in ['e','i']: palabra[i] = 'gu'
        else: palabra[i] = 'g'
    return palabra,[]
##
##  Reglas del fonema 'k'
##
def k(palabra : list) -> list:
    indices = encontrar_indices('k',palabra)
    comparaciones_ortograficas = []

    for i in indices:
        if i == (len(palabra)-1) or ( # Cuando se encuentra al final de una palabra puede ser una 'c' o una extranjera con 'k'
            palabra[i+1] not in VOCALES) or ( # Cuando le precede una consonante
            palabra[i+1] in ['a','o','u']): # Cuando precede las 3 vocales
            palabra[i] = 'c'
            comparaciones_ortograficas.append((i,['k']))
        elif i < (len(palabra)-1):
            if palabra[i+1] in ['i','e']: palabra[i] = 'qu'; comparaciones_ortograficas.append((i,['k']))
        else: palabra[i] = 'k'; comparaciones_ortograficas.append((i,['c']))
    return palabra,comparaciones_ortograficas
##
##  Reglas del fonema 's'
##
def s(palabra : list) -> list:
    """
        c - con prefijos cidio- y cida-
        c - palabras que empiezan con cerc- y circ-
    """
    indices = encontrar_indices('s',palabra)
    comparaciones_ortograficas = []

    for i in indices:
        # Cuando se encuentra al final de la palabra solo puede ser 's' o 'z'
        if i == (len(palabra)-1): palabra[i] = 's'; comparaciones_ortograficas.append((i,['z']))
        elif i < (len(palabra)-1):
            if palabra[i+1] in ['b','d','g','l','m']: palabra[i] = 's'
        # Prefijos de inicio de la 's'
        elif ''.join(palabra[:i]) in ['sub','su','con','kon','tran']: palabra[i] = 's'
        # Prefijos que anteceden la 's'
        elif ''.join(palabra[i-2:i]) in ['de','di']: palabra[i] = 's'
        elif ''.join(palabra[i-3:i]) in ['tra']: palabra[i] = 's'
        # Terminaciones
        elif ''.join(palabra[i:]) == 'sis': palabra[i] = 's'
        # Vocales
        elif i < (len(palabra)-1):
            if palabra[i+1] in ['a','o','u']: palabra[i] = 's'; comparaciones_ortograficas.append((i,['z']))
        # Prefijos de inicio de la 'c'
        elif len(palabra) > 5 and i == 0:
            if ''.join(palabra[:4]) in ['sida','serk','sirk','cerc','circ']: palabra[i] = 'c'
            elif ''.join(palabra[:5]) == 'sidio': palabra[i] = 'c'
        else: palabra[i] = 's'; comparaciones_ortograficas.append((i,['c','sc','z']))
    return palabra, comparaciones_ortograficas
##
##  Reglas del fonema 'x'
##
def x(palabra : list) -> list:
    indices = encontrar_indices('x',palabra)
    comparaciones_ortograficas = []

    for i in indices:
        if i < (len(palabra)-1):
            # El fonema /x/ se puede asociar a la 'j' cuando la preceden todas las vocales
            palabra[i] == 'j'
            # El fonema /x/ se asocia a la 'g' solo con 'e' e 'i', si la vocal que precede es diferente a estas 2 es seguro asignar la 'j'
            # La escritura correcta de la palabra cuando precede la vocal 'e' o 'i' es tarea de un corrector otográfico pues depende de la forma aceptada como correcta por el español. No es posible realizar esta etapa en este instante pues no se asegura que la palabra ingresada sea únicamente incorrecta en este fonema y por esta razón se retorna el índice y las otra grafía a verificar como una bandera de 'correccion_ortográfica' para que al finalizar todas posibles sustituciones ortográficas se verifique la grafía correcta.
            if i < (len(palabra)-1):
                if palabra[i+1] in ['e','i']: comparaciones_ortograficas.append((i,['g']))
    return palabra, comparaciones_ortograficas
##
##  Reglas del fonema 'r'(sonido fuerte rr)
##
def r(palabra : list) -> list:
    indices = encontrar_indices('r',palabra)

    for i in indices:
        # Cuando inicia la palabra la grafía es 'r'
        if i == 0: palabra[0] = 'r'
        # Cuando se tiene el prefijo de negación in- a términos que inician con r
        elif i == 1 and palabra[0] == 'i': palabra[i] = 'rr'
        # Cuando se tiene el prefijo sub- la grafía es 'r'
        elif ''.join(palabra[:i]) == 'sub': palabra[i] = 'r'
        # Cuando le precede una 'l','n' o 's' la grafía es 'r'
        elif palabra[i-1] in ['l','n','s']: palabra[i] = 'r'
        # Cuando se encuentra entre vocales la grafía es 'rr'
        elif i < (len(palabra)-1) and palabra[i-1] in VOCALES and palabra[i+1] in VOCALES: palabra[i] = 'rr'
        else: palabra[i] = 'rr'
    return palabra,[] # Comparaciones ortográficas vacias
##
##  Reglas de vocales
##
def a(palabra : list) -> list:
    indices = encontrar_indices('a',palabra)
    return palabra, list(zip(indices, ['ha']*len(indices)))
def e(palabra : list) -> list:
    indices = encontrar_indices('e',palabra)
    return palabra, list(zip(indices, ['he']*len(indices)))
def i(palabra : list) -> list:
    indices = encontrar_indices('i',palabra)
    return palabra, list(zip(indices, ['hi']*len(indices)))
def o(palabra : list) -> list:
    indices = encontrar_indices('o',palabra)
    return palabra, list(zip(indices, ['ho']*len(indices)))
def u(palabra : list) -> list:
    indices = encontrar_indices('u',palabra)
    return palabra, list(zip(indices, ['hu']*len(indices)))

reemplazos_ortograficos = {
    'b' : b,
    'g' : g,
    'k' : k,
    's' : s,
    'x' : x,
    'r' : r,
    'a' : a, 'e' : e, 'i' : i, 'o' : o, 'u' : u
}

def igual_a_correccion(palabra):
    palabra_aux = ''.join(palabra)
    return palabra_aux == spell(palabra_aux)
def palabra_correcta(palabra : list):
    if len(palabra) == 1: return palabra[0],True

    correcta = False
    mas_grafias = []
    ## Paso 1
    ##  Sustitución de fonemas con grafía única
    for i in range(len(palabra)):
        fonema = palabra[i]
        # El fonema se corresponde con una sola grafía
        if len(cat_fonemas[fonema]['grafias']) == 1: palabra[i] = cat_fonemas[fonema]['grafias'][0]
        # El fonema tiene más de una grafía
        elif fonema not in mas_grafias: mas_grafias.append(fonema)

    ## Paso 2
    ##  Sustitución de fonemas con más de 1 grafía
    comparaciones = []
    for fonema_mas_grafias in list(mas_grafias):
        palabra,comparacion = reemplazos_ortograficos[fonema_mas_grafias](palabra)
        if comparacion: comparaciones += comparacion
    
    ## Paso 3
    ##  Comprueba que la corrección ortográfica del 'Speller' sea igual a la palabra obtenida
    # Primer comprobación
    if igual_a_correccion(palabra): correcta = True; palabra = ''.join(palabra)
    ## Paso 4
    ##  Verifica las incongruencias/diferencias entre la corrección y la palabra con sustituciones para retornar la palabra corregida
    else:
        try:
            correccion = spell(''.join(palabra))
            indices_comparaciones,grafias_comparaciones = zip(*comparaciones)
            ##
            ## Si la palabra sustituida es menor a la palabra corregida
            ##
            multiples_grafias = []
            if len(palabra) < len(correccion): 
                # Verifica si existen combinaciones de grafías mayores a 1 solo caracter para los fonemas
                #   ¡¡ Funciona solo si aparecen 1 sola vez !!
                for grafias_dobles in ['qu','gu','sc','rr','ha','he','hi','ho','hu']:
                    indice = correccion.find(grafias_dobles)
                    if indice >= 0: 
                        multiples_grafias.append((indice,grafias_dobles))
                        correccion = correccion[:indice]+correccion[indice+2:]
            # Se transforma la palabra corregida en lista
            correccion = [c for c in correccion]
            ##
            ## De identificarse grafias múltiples se agregan a la lista
            ##
            for i in range(len(multiples_grafias)):
                indice_correccion,grafia_correccion = multiples_grafias[(len(multiples_grafias)-1)-i] # Inicia obteniendo los últimos en ingresar
                correccion.insert(indice_correccion-i,grafia_correccion)
            print(palabra,correccion)
            # Identifica las grafias que no corresponden con la palabra auxiliar
            incongruencias = [i for i in range(len(palabra)) if palabra[i] != correccion[i]]
            # print('Palabra >>',palabra)
            # print('Correcta >>',correccion)
            # print('Incong >>',incongruencias)
            for incongruencia in incongruencias:
                # Cuando la corrección no se encuentra en alguna de las grafias que faltaban por ser comprobadas se marca como incorrecta y se retorna la palabra corregida
                if incongruencia not in indices_comparaciones: return ''.join(correccion), False
                # print('gRAFIAS >>',grafias_comparaciones[indices_comparaciones.index(incongruencia)])
                # Se verifica que la grafia en la corrección exista en las grafias que se busca comparar
                if correccion[incongruencia] not in grafias_comparaciones[indices_comparaciones.index(incongruencia)]: return ''.join(correccion), False
            
            correcta = True
            palabra = ''.join(correccion)
        except:
            print('Error durante la correción ortográfica')
            correcta = False
        finally:
            return palabra if type(palabra) == 'str' else ''.join(correccion), correcta
    
    return palabra,correcta






# def main():
#     palabras = [
        # 'konstansias',
        # 'kaɲabeɾal',
        # 'askaɾpado',
        # 'gera',
        # 'eskaɾpado',
        # 'adolesente',
        # 'fasista',
        # 'kasa',
        # 'koro',
        # 'koɾo',
        # 'kotoro',
        # 'peɾiko',
#         'aɾbol',
#         'ola',
#         'aoro',
#         'ueko',
#         'aser',
#         'ilo',
#         'aɾko'
#     ]

#     palabras = [[p for p in palabra] for palabra in palabras]

#     for palabra in palabras:
#         correccion,correcta = palabra_correcta(palabra)
#         if correcta: print(f'<< --- CORREGIDA : {correccion} --- >>')
#         else: print(f'<< !!! INCORRECTA : {correccion} --- >>')
#         print('----------------\n')

# if __name__ == '__main__': main()

## Palabras que fallan
##  - Arroz
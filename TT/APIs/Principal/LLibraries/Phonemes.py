import json
import random
from functools import reduce
from autocorrect import Speller

import google.cloud.texttospeech as tts
from typing import Sequence

##
## Global variables
##
#with open('./LLibraries/Gestos.json') as file:
with open('./LLibraries/Gestos.json') as file:
    phonemes_cat = json.load(file)
spell = Speller(lang='es')
# Words found to be corrected yet they interfere with the word that is really beign looked up
exceptions = [
    'gera', #guerra
    'azer', #hacer
    'ezquarpado', 'ecquarpado' #escarpado
]

##
##  Auxiliar functions
##
def recover_graphies(phoneme):
    if phoneme in list(phonemes_cat.keys()): return phonemes_cat[phoneme]['grafias']
    for _,valores in phonemes_cat.items():
        if phoneme in valores['grafias']:
            return valores['grafias']
def phonemes_to_gestures(phonemes):
    return [phonemes_cat[phoneme]['nombre'] for phoneme in phonemes]

##
##  Spelling correction
##
def correct(word):
    if word in exceptions:
        return ''
    return spell(word)
def same_as_correction(word):
    corrected = correct(word)
    if word == corrected: return True
    # Analizes if the corrected word has an h preceding vocals
    corrected = corrected.replace('ch',''); word = word.replace('ch','')
    if 'h' not in corrected: return False
    correct_match = True
    for i,c in enumerate(corrected):
        if c == 'h':
            if c[i:i+1] not in ['ha','he','hi','ho','hu']:
                correct_match = False
                break
    return correct_match
def phonemes_to_graphy(phonemes:list,as_text:bool=False):
    graphies = reduce(lambda acc,phoneme: acc + [phonemes_cat[phoneme]['grafias'][0]],phonemes,[])
    return ''.join(graphies) if as_text else graphies
def correct_spell(word):
    return correct(word)
def phonemes_to_correct_word(phonemes:list):
    '''
        Asignación de grados por corrección ortográfica:
            1. De primer grado en la que no existe otra grafía asociada
            2. De primer grado donde existe una segunda grafía asociada pero la forma ortográfica correcta debe ser provista por el corrector ortográfico o su forma correcta depende del contexto y es imposible hacer la corrección(para las limitaciones del algoritmo y aplicación)
            3. De segundo grado por su asociación con una segunda grafía
            4. De segundo grado por su asociación con mas de 2 grafías y de las que se agregan únicamente 2 extras(sin incluir el símbolo del phonema por defecto)

        1. Reemplazo de todos los fonemas en primer grado(fonemas con una única grafía asociada)
        2. Se verifica la corrección ortográfica y si no existe corrección la palabra ya es correcta
        3. De otra forma se procede hacer el reemplazo individual de la siguiente letra de nivel superior
        4. Se verifica la corrección ortográfica
        5. Se repite el paso 3 hasta todas las letras
    '''
    if len(phonemes) == 1: return phonemes[0]
    greater_grades = []
    word = ''
    ## Step 1
    for i in range(len(phonemes)):
        phoneme = phonemes[i]
        print(phonemes,phoneme)
        if len(phonemes_cat[phoneme]['grafias']) == 1: phonemes[i] = phonemes_cat[phoneme]['grafias'][0]
        else: greater_grades.append(i)
    word = ''.join(phonemes)

    ## Step 2
    # Al ready correct
    if same_as_correction(word): return correct(word)

    ## Step 3
    if greater_grades:
        def phonemes_next_grade(phonemes:list, index:list):
            phonemes_aux = list(phonemes)
            word = ''.join(phonemes)

            # 1° Stop condition
            if same_as_correction(word):
                return correct(word),True
            # 2° Stop condition
            if not index:
                return phonemes,False
            
            # Recovers the associated graphies
            graphies = recover_graphies(phonemes[index[0]])

            # Loops through the graphies
            for graphy in graphies:
                phonemes_aux[index[0]] = graphy
                phonemes_aux,matched = phonemes_next_grade(phonemes_aux, index[1:])
                # Breaks if match found
                if matched: return phonemes_aux,matched
            return phonemes, False

        phonemes,_ = phonemes_next_grade(phonemes, greater_grades)

    return phonemes if type(phonemes) == str else ''.join(phonemes)


##
##  Translation to voice
##
def phonemes_to_ssml(phonemes:str, word:str):
    return f'<phoneme alphabet="ipa" ph="{phonemes}">{word}</phoneme>'
def text_to_voice(ssml_text:str, outfile:str):
    global tts_config
    # Sets the text input to be synthesized
    synthesis_input = tts.SynthesisInput(ssml=ssml_text)
    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = tts.VoiceSelectionParams(
        language_code='es-US',
        name='es-US-Neural2-B'
    )
    # Selects the type of audio file to return
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    try:
        client = tts.TextToSpeechClient()
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
    except:
        print('Error in the tts request')
    else:
        try:
            # Writes the synthetic audio to the output file.
            with open(outfile, "wb") as out:
                out.write(response.audio_content)
            return True
        except:
            print('Error saving the mp3 file')
            return False
def translate_to_voice(phonemes:str, word:str):
    outfile_path = f'./Audios/{phonemes}-{random.randint(1000,10000)}.mp3'
    if text_to_voice(
        phonemes_to_ssml(phonemes, word),
        outfile_path
    ):
        return outfile_path
    return ''

        

# def main():
#     gestos = [
#         'kasa',
#         'alfombɾa',
#         'gera',
#         'rapas',
#         'senaɾ',
#         'pɾobaɾ'
#     ]

#     gestos = [[g for g in gesto] for gesto in gestos]
#     for gesto in gestos:
#         print(phonemes_to_correct_word(gesto))

# def main():
#     from playsound import playsound

#     phonemes = 'eskaɾpado'
#     word = phonemes_to_correct_word([p for p in phonemes])
#     print('Fonemas >>',phonemes,'\nPalabra >>',word)

#     voice_path = translate_to_voice(phonemes, word)
#     if voice_path: playsound(voice_path)

# if __name__ == '__main__': main()
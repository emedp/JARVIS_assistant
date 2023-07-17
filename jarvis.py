import os
import time
import datetime
import speech_recognition #https://pypi.org/project/SpeechRecognition/
import pyttsx3 #https://pypi.org/project/pyttsx3/
from gtts import gTTS #https://pypi.org/project/gTTS/

'''
JARVIS CORE
'''
# TODO loop
# TODO GUI

'''
TRANSCRIBIR VOZ - TEXTO
'''
# speech recognition
def speech_to_text ():
    audio = None
    stt = ""
    stt_google = None

    # obtain audio from microphone
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5) # listen for 0.5 second, the minimum, to calibrate the energy threshold for ambient noise levels
        print("Say something...")
        audio = recognizer.listen(source)

    # try recognize speech using Google Speech Recognition
    try:
        stt_google = recognizer.recognize_google(audio, language="es-ES")
        print("Google Speech Recognition thinks you said: " + stt_google)
    except speech_recognition.UnknownValueError:
        print("Google Speech Recognition could not understand audio. Try again")
    except speech_recognition.RequestError as e:
        print(f"Google Speech Recognition could not be available now. Request failed. Error: {e}")

    stt = str(stt_google)
    return stt

# text to speech
tts = pyttsx3.init()
def text_to_speech(text: str):
    tts.say(text)
    tts.runAndWait()

def tts_change_voice ():
    voices=tts.getProperty('voices')

    text_to_speech("Selecciona una nueva voz diciendo el número")
    print("Select the new voice saying its number:")

    # presenting all voice options
    for index, voice in enumerate(voices):
        print(f"0{index}. {voice.name}")
    
    # select the new voice
    voice_selected = speech_to_text()
    text_to_speech(f"He escuchado {voice_selected}")
    print("Voice selected:", voice_selected)

    # check selection is a number
    if voice_selected.isnumeric == False:
        text_to_speech("Tu respuesta no es un número. Vuelve a intentarlo")
        return
    
    # convert string to integer
    voice_selected = int(voice_selected)

    # check selection is a valid number
    if voice_selected < 0 or voice_selected >= len(voices):
        text_to_speech("Esa no es una opción válida. Vuelve a intentarlo")
        return
    
    # if checks are OK then make the change of voice
    tts.setProperty("voice", voices[voice_selected].id)
    text_to_speech(f"He cambiado mi voz a {voices[voice_selected].name}")
   
def tts_change_rate (new_rate: int):
    old_rate = tts.getProperty('rate')
    tts.setProperty("rate", new_rate)

    print("old speed rate:", old_rate)
    print("new speed rate:", new_rate)
    text_to_speech(f"Mi velocidad de voz ha cambiado de {old_rate} a {new_rate} puntos en palabras por minuto")

def tts_change_volume (new_volume: float):
    old_volume = tts.getProperty('volume')
    tts.setProperty("volume", new_volume)
    
    print("old volume:", old_volume)
    print("new volume:", new_volume)
    text_to_speech(f"Mi volumen ha cambiado del {int(old_volume*100)}% al {int(new_volume*100)}%")

def text_to_speech_google(text: str):
    tts = gTTS("Tu asistente de Google dice: " + text, lang="es",tld="es")
    
    # TODO pasar el siguiente bloque a reproduccion en tiempo real y no con un archivo mp3

    # save the audio in a file
    tts.save('tts.mp3')
    #open the audio file
    os.system("tts.mp3")
    # sleep main thread to give OS time to play file
    time.sleep(1)
    # delete the audio file
    os.remove("tts.mp3")

    return tts

'''
DATOS DE TIEMPO Y LUGAR
'''
# datos de día y hora
def date_time_data ():
    datetime_now = datetime.datetime.now()
    today_weekday = datetime_now.isoweekday()
    weekday = ""
    
    # literal of day of week
    if today_weekday == 1:
        weekday = "lunes"
    elif today_weekday == 2:
        weekday = "martes"
    elif today_weekday == 3:
        weekday = "miércoles"
    elif today_weekday == 4:
        weekday = "jueves"
    elif today_weekday == 5:
        weekday = "viernes"
    elif today_weekday == 6:
        weekday = "sábado"
    elif today_weekday == 7:
        weekday = "domingo"

    date_time = f"Hoy es {weekday}, {datetime_now.day} del {datetime_now.month} de {datetime_now.year} y son las {datetime_now.hour} y {datetime_now.minute}"
    print(date_time)
    text_to_speech(date_time)


# TODO datos de clima

'''
MONITORIZACIÓN Y CONTROL DEL EQUIPO
'''
# TODO datos del sistema como batería, RAM, ROM, CPU, GPU, etc
# TODO cambiar valores del sistema como volumen, etc
# TODO check internet velocity

'''
BUSCAR INFORMACIÓN
'''
# TODO buscar en google
# TODO buscar en wikipedia
# TODO hablar con ChatGPT

'''
text_from_speech = speech_to_text()
text_to_speech_google(text_from_speech)
text_to_speech(text_from_speech)
tts_change_voice()
tts_change_volume(0.5)
tts_change_rate(100)
date_time_data()
'''
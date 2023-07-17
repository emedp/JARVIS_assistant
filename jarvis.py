import speech_recognition #https://pypi.org/project/SpeechRecognition/

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

# TODO text to speech
# TODO escuchar con el micro

'''
DATOS DE TIEMPO Y LUGAR
'''
# TODO datos de día y hora
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

speech = speech_to_text()

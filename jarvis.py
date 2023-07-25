import os
import time
import datetime
import speech_recognition #https://pypi.org/project/SpeechRecognition/
import pyttsx3 #https://pypi.org/project/pyttsx3/
from gtts import gTTS #https://pypi.org/project/gTTS/
import wikipedia #https://pypi.org/project/wikipedia/
import psutil #https://pypi.org/project/psutil/
import platform # https://www.thepythoncode.com/article/get-hardware-system-information-python
# import python-weather #https://pypi.org/project/python-weather/

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
        print("Escuchando...")
        audio = recognizer.listen(source)

    # try recognize speech using Google Speech Recognition
    try:
        stt_google = recognizer.recognize_google(audio, language="es-ES")
        print("GSP: " + stt_google)
    except speech_recognition.UnknownValueError:
        print("Google Speech Recognition could not understand audio. Try again")
    except speech_recognition.RequestError as e:
        print(f"Google Speech Recognition could not be available now. Request failed. Error: {e}")

    stt = str(stt_google)
    return stt

# text to speech
tts = pyttsx3.init()
def text_to_speech(text: str):
    print("TTS:", text)
    tts.say(text)
    tts.runAndWait()

def tts_change_voice ():
    voices=tts.getProperty('voices')

    text_to_speech("Selecciona una nueva voz diciendo el número")

    # presenting all voice options
    for index, voice in enumerate(voices):
        print(f"0{index}. {voice.name}")
    
    # select the new voice
    voice_selected = speech_to_text()
    text_to_speech(f"He entendido {voice_selected}")

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
    text_to_speech(f"Mi velocidad de voz ha cambiado de {old_rate} a {new_rate} puntos en palabras por minuto")

def tts_change_volume (new_volume: float):
    old_volume = tts.getProperty('volume')
    tts.setProperty("volume", new_volume)
    text_to_speech(f"Mi volumen ha cambiado del {int(old_volume*100)}% al {int(new_volume*100)}%")

def text_to_speech_google(text: str):
    tts = gTTS(text, lang="es",tld="es")
    
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
    text_to_speech(date_time)

# TODO datos de clima

'''
BUSCAR INFORMACIÓN
'''
# TODO buscar en google
# buscar en wikipedia
wikipedia.set_lang("es")
def wikipedia_search (search):
    result = wikipedia.summary(search, sentences=1)
    text_to_speech(result)

'''
MONITORIZACIÓN Y CONTROL DEL EQUIPO
'''
# Monitorizar sistema
def scalated_bytes (bytes):
    factor = 1024
    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    for unit in units:
        if bytes < factor:
            return f"{bytes:.2f}{unit}"
        bytes = bytes / factor

def monitoring_system ():

    # SYSTEM INFORMATION
    system = "Sistema Operativo: " + platform.system() + " " + platform.release()
    release = "Versión del S.O.: " +  platform.version()
    node = "Nombre de equipo en la red: " +  platform.node()
    machine = "Arquitectura: " + platform.machine()
    processor = "Procesador: " + platform.processor()

    text_to_speech(system)
    text_to_speech(release)
    text_to_speech(node)
    text_to_speech(machine)
    text_to_speech(processor)

    # BOOT SYSTEM TIME
    boot_dt = datetime.datetime.fromtimestamp(psutil.boot_time())
    text_to_speech(f"El arranque se realizó el {boot_dt.day} del {boot_dt.month} del {boot_dt.year} a las {boot_dt.hour} y {boot_dt.minute}")

    # BATTERY INFORMATION

    battery = psutil.sensors_battery()
    if battery == None:
        text_to_speech(f"No hay batería conectada")
    

    # CPU INFORMATION

    # CPU cores number
    cores_total = psutil.cpu_count(logical=True)
    cores_physical = psutil.cpu_count(logical=False)
    cores_logical = cores_total - cores_physical
    text_to_speech("Número total de núcleos: " + str(cores_total))
    text_to_speech("Número de núcleos físicos: " + str(cores_physical))
    text_to_speech("Número de núcleos lógicos: " + str(cores_logical))

    # CPU frequencies
    cpu_freq = psutil.cpu_freq()
    text_to_speech(f"Frecuencia máxima: {cpu_freq.max:.0f} Mhz")
    text_to_speech(f"Frecuencia mínima: {cpu_freq.min:.0f} Mhz")
    text_to_speech(f"Frecuencia actual: {cpu_freq.current:.0f} Mhz")

    # CPU usage
    for index, percent in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        text_to_speech(f"Núcleo {index} al {percent:.0f}%")
    
    text_to_speech(f"Uso total de la CPU: {psutil.cpu_percent():.0f}%")

    
    # MEMORY INFORMATION

    svmem = psutil.virtual_memory()
    text_to_speech(f"Memoria RAM total: {scalated_bytes(svmem.total)}")
    text_to_speech(f"Memoria RAM disponible: {scalated_bytes(svmem.available)} un {100-svmem.percent:.0f}% libre")
    text_to_speech(f"Memoria RAM usada: {scalated_bytes(svmem.used)} un {svmem.percent:.0f}% ocupado")

    try:
        swap = psutil.swap_memory()
        text_to_speech(f"Memoria SWAP total: {scalated_bytes(swap.total)}")
        text_to_speech(f"Memoria SWAP disponible: {scalated_bytes(swap.available)} un {100-swap.percent:.0f}% libre")
        text_to_speech(f"Memoria SWAP usada: {scalated_bytes(swap.used)} un {swap.percent:.0f}% ocupado")
    except:
        text_to_speech("No ha sido posible leer la memoria SWAP")


    # DISK INFORMATION
    for partition in psutil.disk_partitions():
        text_to_speech(f"Disco: {partition.device}")
        text_to_speech(f"Punto de montaje: {partition.mountpoint}")
        text_to_speech(f"Sistema de archivos: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            text_to_speech(f"Partición espacio total: {scalated_bytes(partition_usage.total)}")
            text_to_speech(f"Partición espacio usado: {scalated_bytes(partition_usage.used)} un {100-partition_usage.percent:.0f}%")
            text_to_speech(f"Partición espacio libre: {scalated_bytes(partition_usage.free)} un {partition_usage.percent:.0f}%")
        except PermissionError:
            continue
    
    # IO statistics  since boot
    disk_io = psutil.disk_io_counters()
    text_to_speech(f"Total leído desde arranque: {scalated_bytes(disk_io.read_bytes)}")
    text_to_speech(f"Total escrito desde arranque: {scalated_bytes(disk_io.write_bytes)}")


    # NETWORK INFORMATION

    # network interfaces (virtual and physical)
    net_addrs = psutil.net_if_addrs()

    for interface_name, interface_addrs in net_addrs.items():
        text_to_speech(f"Interfaz: {interface_name}")
        for addr in interface_addrs:
            if str(addr.family) == "AddressFamily.AF_INET":
                text_to_speech(f"Dirección IP: {addr.address}")
                text_to_speech(f"Máscara: {addr.netmask}")
                text_to_speech(f"Transmisión IP: {addr.broadcast}")
            elif str(addr.family) == 'AddressFamily.AF_PACKET':
                text_to_speech(f"Dirección MAC: {addr.address}")
                text_to_speech(f"Máscara: {addr.netmask}")
                text_to_speech(f"Transmisión MAC: {addr.broadcast}")
    
    # IO statistics  since boot
    net_io = psutil.net_io_counters()
    text_to_speech(f"Total paquetes enviados desde arranque: {net_io.packets_sent}")
    text_to_speech(f"Total paquetes recibidos desde arranque: {net_io.packets_recv}")
    text_to_speech(f"Total datos enviados desde arranque: {scalated_bytes(net_io.bytes_sent)}")
    text_to_speech(f"Total datos recibidos desde arranque: {scalated_bytes(net_io.bytes_recv)}")
    text_to_speech(f"Total errores al enviar datos desde arranque: {net_io.errout}")
    text_to_speech(f"Total errores al recibir datos desde arranque: {net_io.errin}")

# TODO cambiar valores del sistema como volumen, etc
# TODO check internet velocity

'''
JARVIS CORE
'''
# TODO GUI

# start
# play highway to hell
os.system("ACDC-Highway_to_Hell.mp3")

# loop
running = True

# starting the program, the welcome
#text_to_speech("welcome back sir. all systems for gaming will be prepared in a few minutes. For now feel free to grab a cup of coffee and have a good day.")
text_to_speech("Bienvenido de nuevo señor, los sistemas están listos, ¿Qué puedo hacer por usted?")

while running:
    commands = speech_to_text()

    command_all_comands = "dime qué puedes hacer"
    command_power_off = "apágate"
    command_say = "di esto"
    command_google_say = "haz que Google diga"
    command_change_voice = "cambia tu voz"
    command_change_volume = "cambia el volumen a"
    command_change_rate = "cambia la velocidad a"
    command_say_datetime = "dime el día con hora de hoy"
    command_wikipedia = "busca en Wikipedia"
    command_system_info = "monitoriza el sistema"

    all_commands = [
        command_power_off,
        command_say,
        command_google_say,
        command_change_voice,
        command_change_volume,
        command_change_rate,
        command_say_datetime,
        command_wikipedia,
        command_system_info,
    ]

    # Split commands
    for command in commands.split(" y "):
        # analize command
        if command_power_off in command:
            text_to_speech("Hasta luego señor")
            running = False
            break
        elif command_all_comands in command:
            text_to_speech("Estos son todos los comandos que puedes realizar")
            for option in all_commands:
                text_to_speech(option)

        elif command_say in command:
            text_to_speech(command.split(command_say)[1])
        elif command_google_say in command:
            text_to_speech_google(command.split(command_google_say)[1])
        elif command_change_voice in command:
            tts_change_voice()
        elif command_change_volume in command:
            volume = command.split(command_change_volume)[1]
            volume = float(volume) / 100
            tts_change_volume(volume)
        elif command_change_rate in command:
            rate = command.split(command_change_rate)[1]
            rate = int(rate)
            tts_change_rate(rate)
        elif command_say_datetime in command:
            date_time_data()
        elif command_wikipedia in command:
            wikipedia_search(command.split(command_wikipedia)[1])
        elif command_system_info in command:
            monitoring_system()
        else:
            text_to_speech("Creo que no has dicho ningún comando existente")

# Clossing all back process
tts.stop()
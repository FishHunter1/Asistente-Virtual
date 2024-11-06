import random
import pyttsx3
import time
import pygame
import threading
from PIL import Image
import pyfiglet
import subprocess
import wolframalpha
import openai
import pyttsx3
import json
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import gradio as gr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys

API_TOKEN = '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'  # Reemplaza con tu token de API
MODEL_ID = 'openai/whisper-large-v2'  # Reemplaza con el ID del modelo que deseas usar

url = f'https://api-inference.huggingface.co/models/{MODEL_ID}'

headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
for voice in voices:
    if 'spanish' in voice.languages and 'male' in voice.name:
        engine.setProperty('voice', voice.id)
        break
wikipedia.set_lang("es")


pygame.init()
# Configura la ventana
ancho, alto = 1080, 720
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Asistente Alvaro')

# Carga las imágenes de boca abierta y cerrada
boca_abierta = pygame.image.load('/img/aea2.jpg')
boca_cerrada = pygame.image.load('img/aea.jpg')

def mostrar_boca(abierta):

    ventana.fill((255, 255, 255))  # Fondo blanco
    if abierta:
        ventana.blit(boca_abierta, (ancho // 2 - boca_abierta.get_width() // 2, alto // 2 - boca_abierta.get_height() // 2))
    else:
        ventana.blit(boca_cerrada, (ancho // 2 - boca_cerrada.get_width() // 2, alto // 2 - boca_cerrada.get_height() // 2))
    pygame.display.flip()


def animar_boca(intervalo, duracion):
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < duracion:
        tiempo_actual = time.time() - tiempo_inicio
        if int(tiempo_actual / intervalo) % 2 == 0:
            mostrar_boca(True)
        else:
            mostrar_boca(False)
        pygame.time.wait(50)
    mostrar_boca(False)

def speak(texto):
    
    def on_end():
        nonlocal hilo_animacion
        hilo_animacion.join()  # Espera a que el hilo de animación termine
        print("Pronunciación terminada")
    
    engine.connect('finished-utterance', on_end)
    
    # Calcula el tiempo estimado de pronunciación
    num_palabras = len(texto.split())
    tasa_palabras_por_minuto = 150
    tiempo_estimado_minutos = num_palabras / tasa_palabras_por_minuto
    tiempo_estimado_segundos = tiempo_estimado_minutos * 60

    # Inicia el hilo de animación
    hilo_animacion = threading.Thread(target=animar_boca, args=(0.3, tiempo_estimado_segundos))
    hilo_animacion.start()

    # Reproduce el texto
    engine .say(texto)
    engine .runAndWait()

def wishMe():
    global assname
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Buenos dias !")
  
    elif hour>= 12 and hour<18:
        speak("Buenas tardes")   
  
    else: 
        speak("Buenas Noches")  
  
    assname =("Alvaro")
    speak("Soy "+assname+" su asistente personal")
    #speak(assname)
    
 
def username():
    global uname
    speak("Cual es su nombre")
    uname = takeCommand()
    speak(uname+",Gracias por adquirirme")
    speak("Si dices alvaro, estaré listo para ayudarte")
 
def takeCommand():
     
    r = sr.Recognizer()     
    with sr.Microphone() as source:
         
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=4)
    try:
        print("Reconociendo...")    
        query = r.recognize_google(audio, language ='es-ES')
        print(f"dijiste : {query}\n")
  
    except Exception as e:
        print(e)    
        print("No entendi.")  
        return ""
     
    return query

def takeCommand2():
     
    r = sr.Recognizer()     
    with sr.Microphone() as source:
         
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=2)
    try:
        print("Reconociendo...")    
        activa = r.recognize_google(audio, language ='es-ES')
        print(f"dijiste : {activa}\n")
  
    except Exception as e:
        print(e)    
        print("No entendi.")  
        return ""
     
    return activa
  
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 465)
    server.ehlo()
    server.starttls()
     
    # Enable low security in gmail
    server.login('abetancourt889@unab.edu.co', 'Lucascoronel08')
    server.sendmail('abetancourt889@unab.edu.co', to, content)
    server.close()

def otra():
    time.sleep(2)

    
    speak("puedes continuar usando el asistente")

# Realiza la solicitud POST a la API
def chat_function(message, history, system_prompt, max_new_tokens, temperature):
    # Asegúrate de que la temperatura sea estrictamente positiva
    if temperature <= 0:
        return "La temperatura debe ser mayor que 0."

    data = {
        'inputs': message,
        'parameters': {
            'max_new_tokens': max_new_tokens,
            'temperature': temperature,
            'return_full_text': False
        }
    }

    # Añadir system_prompt si no es vacío
    if system_prompt:
        data['system_prompt'] = system_prompt

    response = requests.post(url, headers=headers, json=data)

    # Verifica el estado de la respuesta
    if response.status_code == 200:
        # Procesa la respuesta
        result = response.json()
        # Verifica si la respuesta contiene el texto generado
        if 'generated_text' in result:
            return result['generated_text']
        elif isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            return "No se pudo generar una respuesta adecuada."
    else:
        return f'Error: {response.status_code}, {response.text}'


def interaccion():
    i=0
    while True:
        if i==0:
            speak("En qué te puedo ayudar")
            i=1
            print("Escuchando...")
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Qué quieres buscar en Wikipedia...')
            query = takeCommand()
            try:
                results = wikipedia.summary(query, sentences = 1)
                speak("De acuerdo a Wikipedia")
                speak(results)
                speak('Puedes ir a la página de Wikipedia si quieres más información')
            except Exception as e:
                print(e)
                speak("No fué posible encontrar esa información en Wikipedia")
            otra()
            break

        elif 'abra youtube' in query or 'abrir youtube' in query or 'youtube' in query:
            speak("En esta página abrí Youtube\n")
            webbrowser.open("youtube.com")
            otra()
            break
        
        if 'discord' in query:
            speak("Abriendo Discord...")
            try:
                # Para Windows
                if sys.platform == "win32":
                    subprocess.run(["start", "discord"], shell=True)
                # Para macOS
                elif sys.platform == "darwin":
                    subprocess.run(["open", "-a", "Discord"])
                # Para Linux
                elif sys.platform == "linux":
                    subprocess.run(["discord"])
                else:
                    speak("No pude detectar el sistema operativo para abrir Discord.")
            except Exception as e:
                print(e)
                speak("Ocurrió un error al intentar abrir Discord.")

            otra()
            break
        
        elif 'escuchar música' in query or "canción" in query or "música" in query or "oir una canción" in query or "Música" in query:
            speak("¿Quieres escuchar una canción o una playlist?")
            choice = takeCommand().lower()

            if 'canción' in choice:
                while True:
                    speak("¿Cuál canción quieres escuchar?")
                    # Escuchar el nombre de la canción
                    song_name = takeCommand().lower()
                    speak("¿De qué artista?")
                    # Escuchar el nombre del artista
                    artist_name = takeCommand().lower()

                    CLIENT_ID = 'f1bfbdadf0d441c09062e50e8f40000c'
                    CLIENT_SECRET = 'b9944053c3b049a19cbb26e3b13c9848'
                    REDIRECT_URI = 'http://localhost:8888/callback'
                    SCOPE = "user-library-read user-read-playback-state user-modify-playback-state"

                    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE
                    ))

                    try:
                        # Buscar canción con el nombre y artista especificados
                        query = f"track:{song_name} artist:{artist_name}"
                        results = sp.search(q=query, limit=1, type='track')

                        # Verificar si encontró un resultado y reproducir la canción
                        if results['tracks']['items']:
                            song_uri = results['tracks']['items'][0]['uri']
                            sp.start_playback(uris=[song_uri])
                            speak(f"Estoy reproduciendo la canción {song_name} de {artist_name}.")
                            break  # Termina el ciclo si encontró la canción
                        else:
                            speak("No pude encontrar esa canción en Spotify. ¿Quieres intentar con otra?")
                            choice = takeCommand().lower()
                            if "no" in choice:
                                break  # Termina el ciclo si el usuario no quiere seguir buscando

                    except Exception as e:
                        print("Ocurrió un error al intentar reproducir la música:", e)
                        speak("No pude reproducir la música en este momento.")
                        break  # Termina el ciclo si ocurre un error

            elif 'playlist' in choice:
                while True:
                    speak("¿Qué playlist quieres escuchar?")
                    # Escuchar el nombre de la playlist
                    playlist_name = takeCommand().lower()
                    speak("¿De qué autor es la playlist?")
                    # Escuchar el autor de la playlist
                    playlist_author = takeCommand().lower()

                    CLIENT_ID = 'f1bfbdadf0d441c09062e50e8f40000c'
                    CLIENT_SECRET = 'b9944053c3b049a19cbb26e3b13c9848'
                    REDIRECT_URI = 'http://localhost:8888/callback'
                    SCOPE = "user-library-read user-read-playback-state user-modify-playback-state"

                    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE
                    ))

                    try:
                        # Buscar playlist con el nombre y autor especificados
                        query = f"playlist:{playlist_name} creator:{playlist_author}"
                        results = sp.search(q=query, limit=1, type='playlist')

                        # Verificar si encontró un resultado y reproducir la playlist
                        if results['playlists']['items']:
                            playlist_uri = results['playlists']['items'][0]['uri']
                            sp.start_playback(context_uri=playlist_uri)
                            speak(f"Estoy reproduciendo la playlist {playlist_name} de {playlist_author}.")
                            break  # Termina el ciclo si encontró la playlist
                        else:
                            speak("No pude encontrar esa playlist en Spotify. ¿Quieres intentar con otra?")
                            choice = takeCommand().lower()
                            if "no" in choice:
                                break  # Termina el ciclo si el usuario no quiere seguir buscando

                    except Exception as e:
                        print("Ocurrió un error al intentar reproducir la playlist:", e)
                        speak("No pude reproducir la playlist en este momento.")
                        break  # Termina el ciclo si ocurre un error

            otra()
            break

        elif 'abra google' in query or 'ir a google' in query or 'google' in query:
            speak("Quiere ir a Google, aquí tienes google\n")
            webbrowser.open("google.com")
            otra()
            break

        elif 'fecha' in query or 'deme la hora' in query or 'deme la fecha' in query or 'dime la fecha' in query or 'hora' in query:
            strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            # Obtener la fecha y hora actual
            speak(f"La fecha y hora son {strTime}")
            otra()
            break

        elif 'email al director' in query or 'correo al director' in query:
            try:
                speak("Qué quiere decirle?")
                content = takeCommand()
                to = "abetancourt889@unab.edu.co"   
                sendEmail(to, content)
                speak("El email fué enviado !")
            except Exception as e:
                print(e)
                speak("No fué posible enviar el email, intenta más tarde")
            otra()
            break

        elif 'enviar email' in query or 'email' in query or 'enviar un email' in query:
            try:
                speak("Qué quiere decir?")
                content = takeCommand()
                speak("A quién desea enviale, escribe usa tu teclado")
                to = input()    
                sendEmail(to, content)
                speak("El email fué enviado !")
            except Exception as e:
                print(e)
                speak("No fué posible enviar el email, intenta más tarde")
            otra()
            break

        elif 'Cómo estás' in query or 'cómo está'in query or 'Qué tal estás'in query  or  'qué tal'in query:
            speak("Yo muy bien, gracias")
            speak("Espero que usted tambien este disfrutando este asistente?")
            otra()
            break

        elif 'yo bien' in query or "muy bien" in query or "estoy bien" in query:
            speak("Es muy bueno saber que está usted bien")
            otra()
            break

        elif "cambiar tu nombre" in query or "cambia tu nombre" in query or "otro nombre para ti" in query:
            speak("Cual sería mi nuevo nombre")
            assname = takeCommand()
            speak("Gracias, ahora mis amigos me conocerán por"+assname)
            otra()
            break


        elif "cambiar nombre" in query or "cambia mi nombre" in query or "otro nombre" in query:
            speak("Cuál es tu nombre")
            uname = takeCommand()
            speak("A partir de ahora eres"+uname)
            otra()
            break

        elif "cuál es tu nombre" in query or "qué nombre tienes" in query:
            speak("Mis amigos me llaman Alvaro")
            otra()
            break

        elif 'salir' in query or 'chao' in query or 'adios' in query  :
            speak("Gracias por su tiempo")
            otra()
            break

        elif "quién te construyó" in query or "quién te creó" in query or "cómo naciste" in query or "de dónde saliste" in query or "quién te hizo" in query: 
            speak("yo fui creado por un furro llamado alvaro")
            otra()
            break                
        elif 'chiste' in query:
            speak("Mis chiste son muy de loquito del centro, pero te voy a contar uno:")
            speak(pyjokes.get_joke(language='es', category= 'all'))
            speak("meow y ojalá te haya gustado")
            otra()
            break
                
        elif "calcula" in query or "operación matemática" in query or "cuánto es" in query:           
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client("3527QJ-EYKJ9QYEQY")
            # Obtener la consulta para calcular
            if 'calcula' in query:
                indx = query.lower().split().index('calcula') 
            else:
                indx = query.lower().split().index('operación') + 1
            query = query.split()[indx + 1:] 
            
            try:
                # Consultar a Wolfram Alpha
                res = client.query(' '.join(query)) 
                answer = next(res.results).text
                print("La respuesta es:", answer) 
                speak("La respuesta es: " + answer)
            except Exception as e:
                print("Hubo un error al calcular la operación:", e)
            
            otra()
            break

        elif 'busca en internet' in query or 'encuentra en internet' in query:
                
            query = query.replace('busca en internet', "") 
            query = query.replace('encuentra en internet', "")          
            webbrowser.open(query) 
            
            otra()
            break


        elif "quién soy yo" in query or "quién soy" in query:
            speak("eres un furro como yo")
            otra()
            break

        elif "vino" in query or "viniste" in query  or "razón de ser" in query  or "para qué nació" in query  or "por qué nació" in query:
            speak("para ser el mayor furro de todos en el mundo")
            otra()
            break

        elif 'qué es amor' in query or 'que es amor' in query or 'Qué es amor' in query:
            speak("no lo se pq soy un ser amorfo que dice meow")
            otra()
            break

        elif "quién eres" in query or 'quién eres' in query or 'Quién eres' in query:
            speak("un furro")
            otra()
            break

        elif 'Para qué te crearon' in query or 'Por qué te crearon' in query or 'te crearon' in query:
            speak("Fuí creado para un experimento de trafico de niños taiwaneses")
            
            otra()
            break
        
        elif 'noticia' in query:
                
            try: 
                api_news='a3a77c24281644b5a598d70a6f1e887c'
                jsonObj = urlopen('''https://newsapi.org/v2/everything?q=colombia&from=2024-03-18&sortBy=publishedAt&apiKey=a3a77c24281644b5a598d70a6f1e887c''')
                data = json.load(jsonObj)
                i = 1
                    
                speak('Aquí hay algunas noticias de colombia.')
                print('''=============== NOTICIAS ============'''+ '\n')
                    
                for item in data['articles']:
                        
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                    
                print(str(e))      
            otra()
            break

            
        elif 'bloquea la pantalla' in query or 'bloquea windows' in query:
                speak("Bloquendo windows")
                ctypes.windll.user32.LockWorkStation()    
                otra()
                break

        elif 'bajar el sistema' in query or 'cerrar el sistema' in query:
                speak("Espera un segundo ! Su sistema está en camino de apagarse")
                subprocess.call('shutdown / p /f')
                
                otra()
                break
                    
        elif 'borra reciclaje' in query or 'limpia el reciclaje' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Reciclaje borrado")

        elif "no escuchar" in query or "pare de escuchar" in query:
            speak("¿Durante cuánto tiempo deseas que  deje de escuchar comandos?")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "dónde estamos" in query or "dónde está el laboratorio" in query or "dónde queda" in query :
            query = query.replace("donde estamos ubicados", "")
            location = query
            speak("El laboratorio queda en el edificio de Ingenieria de la Unab. Te voy ayudar a ubiqcarte en la Unab usando google map")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/search/unab/@7.1170986,-73.1060737,17z")

        elif "cámara" in query or "foto" in query:
            speak("Espera un 30 segundos mientras activo la camara, tomo una foto y cierra la imagen para continuar")
            ec.capture(0, "foto", "img.jpg")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
                
        elif "hibernar" in query or "sleep" in query:
            speak("Hibernando")
            subprocess.call("shutdown / h")

        elif "cerrar sesión" in query or "sign out" in query:
            speak("Asegúrese de que todas las aplicaciones estén cerradas antes de cerrar sesión.")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "escribe una nota" in query or "escribir nota" in query or "toma una nota" in query:
            speak("Qué quisiera que yo escribiera")
            note = takeCommand()
            file = open('nota.txt', 'w')
            speak("Puedo incluir la fecha")
            snfm = takeCommand()
            if 'si' in snfm or 'seguro' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
            
        elif "mostrar la nota" in query or "ver la nota" in query or "ver nota" in query or "muestre la nota" in query :
            speak("mostrando la nota")
            file = open("nota.txt", "r") 
            print(file.read())
            speak(file.read(6))

        elif "alvaro" in query:               
            wishMe()
            speak("Si señor ese soy yo... ")
            speak(assname + "pregunta lo que quieras")

        elif "clima" in query:
            api_key = "b175155b402c44d69e3a12377008afca"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak(" Dime la ciudad ")
            print("El clima de : ")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url) 
            x = response.json() 
            print(response.text)

            if x["cod"] != "404" and x["cod"] != "400": 
                y = x["main"] 
                current_temperature = str(round(float(y["temp"] - 273.15 ),0))
                current_pressure = y["pressure"] 
                current_humidity = y["humidity"] 
                z = x["weather"] 
                weather_description = z[0]["description"] 
                speak(" Temperatura es= " +str(current_temperature)+"grados centigrados"+"\n presión atmosférica="+str(current_pressure) +"hpa"+"\n la humedad es= " +str(current_humidity)+"porciento") 
            else:
                speak(" la ciudad no fué encontrada o no la entendí ")
            otra()
            break
                
        elif "alvaro es gey?" in query or "alvaro le gusta el pito?" in query or "alvaro que le gusta?" in query:
            speak("Aun no sabemos como se identifica mi creador, asi que porfavor dile que complete el siguiente cuestionario")
            webbrowser.open("https://www.idrlabs.com/es/orientacion-sexual/prueba.php")
            
        elif "abrir wikipedia" in query:
            webbrowser.open("wikipedia.com")    

        elif "hola" in query or  "que tal" in query or "buenas" in query:
            speak("" +query)
            speak("Espero te encuentre muy bien? Puedes iniciar preguntando")

        # most asked question from google Assistant
        elif "seré tu novio" in query or "seré tu novia" in query or "tu novio" in query or "tu novia" in query or "mi novia" in query:   
            speak("sere tu novio si me ladras o me dices meow")

        elif "te amo" in query:
            speak("Yo no puedo amar pero si fueras un helicoptero apache si")

        elif "busca" in query:           
            # Use the same API key 
            # that we have generated earlier
            client = wolframalpha.Client("3527QJ-EYKJ9QYEQY")
            res = client.query(query)
                
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No tengo resultados para esa pregunta")
                speak ("No encontré una respuesta, intenta otra vez")
        
        elif "Llama" in query or 'llama' in query:
            speak("¿Qué deseas preguntar?")
            # Captura la pregunta del usuario
            message = takeCommand()
            speak("Dame un segundo.")
            
            # Ajustamos el prompt del sistema para mejorar la consistencia en español y evitar respuestas regionales
            system_prompt = """
            Eres un asistente virtual que habla en español. Responde siempre en español. 
            Evita proporcionar información específica de España a menos que el usuario lo pida explícitamente. 
            Prefiere información general o de América Latina cuando sea relevante.
            No respondas en contexto espeficio
            """
            
            # Llamada a la función de chat con los ajustes sugeridos
            resultado = chat_function(message, history="", system_prompt=system_prompt, max_new_tokens=250, temperature=0.7)
            
            print(resultado)
            print(type(resultado))
            
            speak(resultado)
            otra()
            break

def print_message(mensaje):
    # Crear un objeto Figlet con el estilo deseado
    font = pyfiglet.Figlet(font='slant')
    
    # Generar el texto ASCII art
    ascii_art = font.renderText(mensaje)
    
    # Imprimir el texto ASCII art
    print(ascii_art)



if __name__ == '__main__':
    query=''
    clear = lambda: os.system('cls')    
    clear()
    print_message('Bienvenido')
    wishMe()
    username()

    while True:

        query = takeCommand2().lower()
        if 'Alvaro' in query or 'lvaro' in query  or 'varo' in query or 'al varo' in query or 'avaro' in query:
            interaccion()
            speak("Para activarme di alvaro")
        elif 'salir' in query or 'apagar' in query or 'quitar' in query or 'terminar' in query or'salga' in query:
            speak("Gracias por visitarnos")
            print_message('Gracias')
            break
pygame.quit()
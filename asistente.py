from cgitb import reset
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import requests
import pyautogui
import operator
import os
import webbrowser
from googletrans import Translator
from spanishconjugator import Conjugator
 
listener = sr.Recognizer()
engine = pyttsx3.init()
voiceRate = 142

voces = engine.getProperty('voices')
engine.setProperty('voice', voces[2].id)
engine.setProperty('rate',voiceRate)
nombre_asistente = 'pandita'
 
def bienvenida():
    engine.say(f"Hola me llamo {nombre_asistente}, y soy tu asistente virtual")
    engine.runAndWait()
 
def hablar(por_hablar):
    engine.say(por_hablar)
    engine.runAndWait()
 
def escuchar():
    while True:
        with sr.Microphone() as source:
            print('Escuchando...')
 
            audio = listener.listen(source, phrase_time_limit=5)
            text = ''
            try:
                print('Reconociendo...')
                text = listener.recognize_google(audio, language='es-US').lower()
                print(text)
                return text
            except Exception as e:
                print(e)
                if nombre_asistente in text:
                    hablar('No pude entenderlo bien, repítelo por favor')
                
 
def dar_hora():
    hablar(f"La hora es {datetime.datetime.now().strftime('%H:%M')}")
 
def dar_dia():
    hablar(f"La fecha actual es: {datetime.datetime.now().day} del {datetime.datetime.now().month}")
 
def busqueda_wikipedia(busca):
    wikipedia.set_lang('es')
    busca = busca.replace(f'{nombre_asistente} busca en wikipedia','')
    resultado = wikipedia.summary(busca, sentences=3)
    hablar(f'Esto es lo que dice wikipedia: {resultado}')
 
def busqueda_google(busca):
    busca = busca.replace(f'{nombre_asistente} busca en google','')
    hablar('Buscando en Google')
    pywhatkit.search(busca)
 
def busqueda_youtube(busca):
    busca = busca.replace(f'{nombre_asistente} busca en youtube','')
    hablar('Buscando en youtube')
    pywhatkit.playonyt(busca)

def busqueda_amazon(busca):
    busca = busca.replace(f'{nombre_asistente} busca en amazon','')
    hablar('Buscando en amazon')
    url = 'https://www.amazon.com.mx/s?k='+busca 
    webbrowser.open_new_tab(url)
    envia_whats(url)

def busqueda_linkedin(busca):
    busca = busca.replace(f'{nombre_asistente} busca en linkedin','')
    hablar('Buscando en linkedin')
    url = 'https://www.linkedin.com/search/results/all/?keywords='+busca 
    webbrowser.open_new_tab(url)

def traduce_a_en(busca):
    busca = busca.replace(f'{nombre_asistente} traduce al inglés','')
    hablar('Traduciendo al ingles')
    translator = Translator()
    result_en = translator.translate(busca, src='es', dest='en')
    hablar(result_en.text) 

def conjuga_verbo(busca):
    busca = busca.replace(f'{nombre_asistente} conjuga el verbo','')
    hablar(f'Conjugando el verbo {busca}' )
    present_indicative_conjugation = Conjugator().conjugate('hablar','present','indicative')
    hablar(present_indicative_conjugation) 

def envia_whats(url):
    try:
     pywhatkit.sendwhatmsg("+525538997875", "Checate esto esta increible", datetime.datetime.now().hour, datetime.datetime.now().minute + 1)
     print("Message Sent!") #Prints success message in console
 
    except: 
     print("Error in sending the message")
    
 
def no_entendi():
    hablar('no te estoy entendiendo nada!')

def detener():
    hablar('Adios!')
    quit()

 
bienvenida()
while True:
    comando = escuchar()
 
    if nombre_asistente in comando:
 
        if 'qué hora es' in comando:
            print('despues del texto')
            dar_hora()
 
        elif 'qué día es' in comando:
            dar_dia()
 
        elif 'busca en wikipedia' in comando:
            busqueda_wikipedia(comando)
 
        elif 'busca en google' in comando:
            busqueda_google(comando)
 
        elif 'busca en youtube' in comando:
            busqueda_youtube(comando)
        
        elif 'busca en amazon' in comando:
            busqueda_amazon(comando)

        elif 'busca en linkedin' in comando:
            busqueda_linkedin(comando)

        elif 'traduce al inglés' in comando:
            traduce_a_en(comando)

        elif 'conjuga el verbo' in comando:
            conjuga_verbo(comando)
 
        elif 'adiós' in comando:
            detener()
        else:
            no_entendi()

from cgitb import reset
import string
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

from tkinter import *
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np

 
listener = sr.Recognizer()
engine = pyttsx3.init()
voiceRate = 142
tempFile = 'temp.jpg'



voces = engine.getProperty('voices')
engine.setProperty('voice', voces[2].id)
engine.setProperty('rate',voiceRate)
nombre_asistente = 'pandita'
 
def bienvenida():
    engine.say(f"Soy {nombre_asistente}, tu asistente virtual")
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
     print("Mensaje enviado!")
 
    except: 
     print("Error enviando mensaje")
 
def no_entendi():
    hablar('no te estoy entendiendo nada!')

def detener():
    hablar('Adios!')
    quit()

def entrena_rostro(nombre_usuario):
    nombre_usuario = nombre_usuario.replace(f'{nombre_asistente} entrena rostro de ','')
    a,b = 'áéíóúü','aeiouu'
    trans = str.maketrans(a,b)
    nombre_usuario = nombre_usuario.translate(trans)
    print(nombre_usuario)
    hablar(f'Hola {nombre_usuario}, posiciona tu rostro enfrente de la cámara, y cuando estes listo presiona la tecla escape para capturarlo')
    
    cap = cv2.VideoCapture(0)              
    while(True):
        ret,frame = cap.read()              
        cv2.imshow('Entrenando Rostro',frame)         
        if cv2.waitKey(1) == 27:            
            break
    usuario_img = nombre_usuario
    cv2.imwrite(usuario_img+".jpg",frame)       
    cap.release()                               
    cv2.destroyAllWindows()

    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) 
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)
    hablar(f'{nombre_usuario}, tu rostro se entrenó correctamente')

def detecta_rostro():
    hablar('Hola, posiciona tu rostro enfrente de la cámara, y cuando estes listo presiona la tecla escape para capturarlo' )
    
    cap = cv2.VideoCapture(0)
    while(True):
        ret,frame = cap.read()
        cv2.imshow('Detectando Rostro',frame)
        if cv2.waitKey(1) == 27:           
            break
    cv2.imwrite(tempFile,frame)       
    cap.release()
    cv2.destroyAllWindows()

    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(tempFile,cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = tempFile
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    im_archivos = os.listdir()  
    detectado = False
    for i in range(len(im_archivos)):
        print(im_archivos[i])
        if(im_archivos[i].__contains__('.jpg') and im_archivos[i] != tempFile):
            print(f'validando contra {im_archivos[i]}')
            rostro_reg = cv2.imread(im_archivos[i])
            rostro_log = cv2.imread(tempFile)
            similitud = orb_sim(rostro_reg, rostro_log)
            print(similitud)
            if similitud >= 0.95:
                nombre_detectado = im_archivos[i].replace('.jpg','')
                hablar(f'Ya se quien eres, eres: {nombre_detectado}')
                detectado = True
                break
    if(detectado == False):
        hablar('No se quien eres!!, Debes entrenar tu rostro previamente!')

def orb_sim(img1,img2):
    orb = cv2.ORB_create()  

    kpa, descr_a = orb.detectAndCompute(img1, None)  
    kpb, descr_b = orb.detectAndCompute(img2, None)  

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 

    matches = comp.match(descr_a, descr_b)  

    regiones_similares = [i for i in matches if i.distance < 70] 
    if len(matches) == 0:
        return 0
    return len(regiones_similares)/len(matches)  
 
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
        
        elif 'entrena rostro de' in comando:
            entrena_rostro(comando)

        elif 'quién soy' in comando:
            detecta_rostro()

        else:
            no_entendi()

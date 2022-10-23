from chardet import detect
from cgitb import reset
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import torch
import os
import webbrowser
from googletrans import Translator
from tkinter import *
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np

#CONSTANTES
NOMBRE_ASISTENTE = 'pandita'
LENGUAJE = 'es-US'
VOICE_RATE = 142
TEMP_FILE_DETECTION = 'temp.jpg'
OS_VOICE_IDENTIFIER = 2
UMBRAL_IDENTIFICACION_ROSTRO = 0.93
PATH_PESOS_YOLO = 'C:/praxthon/model_pesos/best.pt'
EXTENSION_JPG = '.jpg'

#COMANDOS
COMANDO_QUE_HORA_ES = 'qué hora es'
COMANDO_QUE_DIA_ES = 'qué día es'
COMANDO_BUSCA_EN_WIKIPEDIA= 'busca en wikipedia'
COMANDO_BUSCA_EN_GOOGLE= 'busca en google'
COMANDO_BUSCA_EN_YOUTUBE='busca en youtube'
COMANDO_BUSCA_EN_AMAZON='busca en amazon'
COMANDO_BUSCA_EN_LINKEDIN = 'busca en linkedin'
COMANDO_TRADUCE_AL_INGLES = 'traduce al inglés'
COMANDO_ENTRENA_ROSTRO_DE = 'entrena rostro de'

COMANDO_QUIEN_SOY = 'quién soy'
COMANDO_DETECTA_OBJETOS = 'detecta objetos'
COMANDO_PARAR = 'parar'

engine = pyttsx3.init()
voces = engine.getProperty('voices')
engine.setProperty('voice', voces[OS_VOICE_IDENTIFIER].id)
engine.setProperty('rate',VOICE_RATE)
 
def hablar(por_hablar: str):
    """Método encargado de decir una frase
    Args:
        por_hablar (str): [sentencia a decir]
    """
    engine.say(por_hablar)
    engine.runAndWait()
 
def escuchar(lenguaje):
    """Metodo encargado de mantener el asistente a la escucha
    Args:
        lenguaje (str): [lenguaje en el cual escucha el asistente]
    """
    
    while True:
        with sr.Microphone() as source:
            print('Escuchando')
            listener = sr.Recognizer()
            listener.adjust_for_ambient_noise(source, duration = 0.5)
            audio = listener.listen(source, phrase_time_limit=5)
            text = ''
            try:
                text = listener.recognize_google(audio, language=LENGUAJE).lower()
                print(text)
                return text
            except Exception as e:
                print(e)
                if NOMBRE_ASISTENTE in text:
                    hablar('No pude entenderlo bien, repítelo por favor')

def dar_bienvenida():
    """Método encargado de dar la bienvenida del asistente virtual."""
    hablar(f"Soy {NOMBRE_ASISTENTE}, tu asistente virtual")
    engine.runAndWait()

def dar_hora():
    """Metodo del asistente que da la hora y minuto actual
       
       Se invoca con el comando: ¿NOMBRE_ASISTENTE COMANDO_QUE_HORA_ES?

       Ejemplo: Pandita qué hora es?
    """
    hablar(f"La hora es {datetime.datetime.now().strftime('%H:%M')}")
 
def dar_dia():
    """Metodo del asistente que da el día y mes actual
       
       Se invoca con el comando: ¿NOMBRE_ASISTENTE COMANDO_QUE_DIA_ES?

       Ejemplo: Pandita qué día es?
    """
    hablar(f"La fecha actual es: {datetime.datetime.now().day} del {datetime.datetime.now().month}")
 
def busqueda_wikipedia(busca):
    """Metodo encargado de buscar en wikipedia
       Args:
            busca (str): [comando recibido]
    
       Se invoca con el comando: NOMBRE_ASISTENTE COMANDO_BUSCA_EN_WIKIPEDIA Texto a buscar

       Ejemplo: Pandita busca en wikipedia zapato 
    """
    wikipedia.set_lang('es')
    busca = busca.replace(f'{NOMBRE_ASISTENTE} {COMANDO_BUSCA_EN_WIKIPEDIA}','')
    resultado = wikipedia.summary(busca, sentences=3)
    hablar(f'Esto es lo que encontré en wikipedia: {resultado}')
 
def busqueda_google(busca):
    """Metodo encargado de buscar en google
       Args:
            busca (str): [comando recibido]
   
       Se invoca con el comando: NOMBRE_ASISTENTE COMANDO_BUSCA_EN_GOOGLE Texto a buscar

       Ejemplo: Pandita busca en google dolar 
    """
    busca = busca.replace(f'{NOMBRE_ASISTENTE} {COMANDO_BUSCA_EN_GOOGLE}','')
    hablar(f'Buscando en Google: {busca}')
    pywhatkit.search(busca)
 
def busqueda_youtube(busca):
    """Metodo encargado de buscar en youtube
       Args:
            busca (str): [comando recibido]

       Se invoca con el comando: NOMBRE_ASISTENTE COMANDO_BUSCA_EN_YOUTUBE Texto a buscar

       Ejemplo: Pandita busca en youtube developers 
    """
    busca = busca.replace(f'{NOMBRE_ASISTENTE} {COMANDO_BUSCA_EN_YOUTUBE}','')
    hablar(f'Buscando en youtube: {busca}')
    pywhatkit.playonyt(busca)

def busqueda_amazon(busca):
    """Metodo encargado de buscar en amazon méxico, al finalizar la busqueda envia un whatsapp recomendando la busqueda del producto
       Args:
            busca (str): [comando recibido]

       Se invoca con el comando: NOMBRE_ASISTENTE COMANDO_BUSCA_EN_AMAZON Texto a buscar

       Ejemplo: Pandita busca en amazon motorola 
    """
    busca = busca.replace(f'{NOMBRE_ASISTENTE} {COMANDO_BUSCA_EN_AMAZON}','')
    hablar(f'Buscando en amazon: {busca}')
    url = 'https://www.amazon.com.mx/s?k='+busca 
    webbrowser.open_new_tab(url)
    envia_whats("+525538997875",url)

def busqueda_linkedin(busca):
    """Metodo encargado de buscar en linkedin
       Args:
            busca (str): [comando recibido]
    
       Se invoca con el comando: NOMBRE_ASISTENTE COMANDO_BUSCA_EN_LINKEDIN Texto a buscar

       Ejemplo: Pandita busca en linkedin praxis 
    """
    busca = busca.replace(f'{NOMBRE_ASISTENTE} {COMANDO_BUSCA_EN_LINKEDIN}','')
    hablar(f'Buscando en linkedin: {busca}')
    url = 'https://www.linkedin.com/search/results/all/?keywords='+busca 
    webbrowser.open_new_tab(url)

def traduce_a_en(busca):
    """Metodo encargado de traducir al idioma ingles
       Args:
            busca (str): [comando recibido]
    
       Se invoca con el comando: NOMBRE_ASISTENTE COMANDO_TRADUCE_AL_INGLES Texto a buscar

       Ejemplo: Pandita traduce al ingles Hola mundo 
    """
    busca = busca.replace(f'{NOMBRE_ASISTENTE} {COMANDO_TRADUCE_AL_INGLES}','')
    hablar(f'Traduciendo al ingles: {busca}')
    translator = Translator()
    result_en = translator.translate(busca, src='es', dest='en')
    hablar(result_en.text) 

def envia_whats(numero_whatsapp, url):
    """Metodo encargado de traducir al idioma ingles
       Args:
            numero_whatsapp (str): [el número de whatsapp destino]
            url (str): [la url a recomendar]
    """
    try:
        pywhatkit.sendwhatmsg(numero_whatsapp, f"Chécate esto esta increíble: {url}", datetime.datetime.now().hour, datetime.datetime.now().minute + 1)
        print("Mensaje enviado!")
    except: 
        print("Error enviando mensaje")

def no_entendi():
    """Metodo encargado de notificar que no se entendio el comando recibido
    """
    hablar('no te estoy entendiendo nada!')

def detener():
    """Metodo encargado de notificar que no se entendio el comando recibido
    """
    hablar('Nos vemos pronto!')
    quit()

def similitud_orb(img1,img2):
    """Metodo encargado de obtener la similitud por Fuerza bruta
       entre dos imagenes através de descriptores.
       Args:
            img1 (image): [Imagen a compar]
            img2 (image): [Imagen a compar]
    """
    orb = cv2.ORB_create()  
    kpa, descr_a = orb.detectAndCompute(img1, None)  
    kpb, descr_b = orb.detectAndCompute(img2, None)  
    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 
    matches = comp.match(descr_a, descr_b)  
    regiones_similares = [i for i in matches if i.distance < 70] 
    if len(matches) == 0:
        return 0
    return len(regiones_similares)/len(matches)  

def entrena_rostro(nombre_usuario):
    """Metodo encargado de entrenar un nuevo rostro
       Args:
            nombre_usuario (str): [Nombre del usuario]
    """
    nombre_usuario = nombre_usuario.replace(f'{NOMBRE_ASISTENTE} {COMANDO_ENTRENA_ROSTRO_DE} ','')
    a,b = 'áéíóúü','aeiouu' 
    trans = str.maketrans(a,b)
    nombre_usuario = nombre_usuario.translate(trans) #Se normaliza el nombre para eliminar acentos
    print(nombre_usuario)
    hablar(f'Hola {nombre_usuario}, posiciona tu rostro enfrente de la cámara, y cuando estes listo presiona la tecla escape para capturarlo')
    
    #Captura del frame de la camara
    cap = cv2.VideoCapture(0)              
    while(True):
        ret,frame = cap.read()              
        cv2.imshow('Entrenando Rostro',frame)         
        if cv2.waitKey(1) == 27:   #Al teclear ESC se toma el frame a guardar como image         
            break
    usuario_img = nombre_usuario
    cv2.imwrite(usuario_img + EXTENSION_JPG, frame) #Se guarda a disco el frame como imagen      
    cap.release()                               
    cv2.destroyAllWindows()

    def obtiene_rostro(img, lista_resultados):
        """Metodo encargado de extraer de la imagen capturada el rostro y normalizarlo a un tamaño estandar,
           se hace uso de la libreria MTCNN para la detección de rostros en la cara
            Args:
                img (str): [nombre imagen]
                lista_resultados (list): [lista de las caras detectadas en la image]  
        """
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Se obtiene unicamente la cara
            cv2.imwrite(usuario_img + EXTENSION_JPG ,cara_reg) #Se guarda a disco la imagen de la cara
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img + EXTENSION_JPG
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles) #Se obtienen la caras a través de Multi-task Cascaded Convolutional Networks
    obtiene_rostro(img, caras)
    hablar(f'{nombre_usuario}, tu rostro se entrenó correctamente')

def detecta_rostro():
    """Metodo encargado de detectar un rostro previamenten entrenado
    """
    hablar('Intentaré detectar tu rostro, posiciónate enfrente de la cámara, y cuando estes listo presiona la tecla escape para comenzar con la detección' )
    
    #Captura del frame de la camara
    cap = cv2.VideoCapture(0)
    while(True):
        ret,frame = cap.read()
        cv2.imshow('Detectando Rostro',frame)
        if cv2.waitKey(1) == 27:                #Al teclear ESC se toma el frame a guardar como image                  
            break
    cv2.imwrite(TEMP_FILE_DETECTION,frame)      #Se guarda a disco el frame como imagen  
    cap.release()
    cv2.destroyAllWindows()

    def obtener_rostro_temporal(img, lista_resultados):
        """Metodo encargado de extraer de la imagen capturada el rostro y normalizarlo a un tamaño estandar,
           se hace uso de la libreria MTCNN para la detección de rostros en la cara
            Args:
                img (str): [nombre imagen]
                lista_resultados (list): [lista de las caras detectadas en la image]  
        """
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Se obtiene unicamente la cara
            cv2.imwrite(TEMP_FILE_DETECTION,cara_reg)  #Se guarda a disco la imagen de la cara
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = TEMP_FILE_DETECTION
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles) #Se obtienen la caras a través de Multi-task Cascaded Convolutional Networks
    obtener_rostro_temporal(img, caras)

    im_archivos = os.listdir()  
    detectado = False
    for i in range(len(im_archivos)):
        print(im_archivos[i])
        if(im_archivos[i].__contains__(EXTENSION_JPG) and im_archivos[i] != TEMP_FILE_DETECTION): #Comparo la cara actual con las previamente entrenadas
            print(f'validando contra {im_archivos[i]}')
            rostro_reg = cv2.imread(im_archivos[i])
            rostro_log = cv2.imread(TEMP_FILE_DETECTION)
            similitud = similitud_orb(rostro_reg, rostro_log)
            print(similitud)
            if similitud >= UMBRAL_IDENTIFICACION_ROSTRO: # Si cumple con un valor mayot o igual al umbral lo considera como el mismo
                nombre_detectado = im_archivos[i].replace(EXTENSION_JPG,'')
                hablar(f'Ya se quien eres, eres: {nombre_detectado}')
                detectado = True
                break
    if(detectado == False):
        hablar('No se quien eres!!, Debes entrenar tu rostro previamente!')

def detecta_objeto():
    """Metodo encargado de la deteccion de objetos a haciendo uso de Yolo V5 para la detección de ibjetos en tiempo real a través de una red neuronal convlolucional.
    """
    hablar('Tengo implementada una red neuronal entrenada con YOLO v5, y fui entrenada para detectar objetos parecidos a carritos de juguete.')
    hablar('Coloca un carrito de juguete para su detección.')
    model = torch.hub.load('ultralytics/yolov5', 'custom', path = PATH_PESOS_YOLO) #Se carga el archivo de pesos previamente entrenado
    
    cap = cv2.VideoCapture(0)
    while(True):
        ret,frame = cap.read() #Se realiza la lectura de frames
        detect = model(frame)  #Detección usando el modelo
        info = detect.pandas().xyxy[0]
        print(info)
        cv2.imshow('Detector Carritos Praxthon', np.squeeze(detect.render()))
        if cv2.waitKey(1) == 27:           
            break
    cap.release()
    cv2.destroyAllWindows()
    for i in range (1,5):
        cv2.waitKey(1)

dar_bienvenida()

while True:
    comando = escuchar(LENGUAJE)
 
    if NOMBRE_ASISTENTE in comando:
 
        if COMANDO_QUE_HORA_ES in comando:
            dar_hora()
        elif COMANDO_QUE_DIA_ES in comando:
            dar_dia()
        elif COMANDO_BUSCA_EN_WIKIPEDIA in comando:
            busqueda_wikipedia(comando)
        elif COMANDO_BUSCA_EN_GOOGLE in comando:
            busqueda_google(comando)
        elif COMANDO_BUSCA_EN_YOUTUBE in comando:
            busqueda_youtube(comando)
        elif COMANDO_BUSCA_EN_AMAZON in comando:
            busqueda_amazon(comando)
        elif COMANDO_BUSCA_EN_LINKEDIN in comando:
            busqueda_linkedin(comando)
        elif COMANDO_TRADUCE_AL_INGLES in comando:
            traduce_a_en(comando)
        elif COMANDO_PARAR in comando:
            detener()
        elif COMANDO_ENTRENA_ROSTRO_DE in comando:
            entrena_rostro(comando)
        elif COMANDO_QUIEN_SOY in comando:
            detecta_rostro()
        elif COMANDO_DETECTA_OBJETOS in comando:
            detecta_objeto()    
        else:
            no_entendi()
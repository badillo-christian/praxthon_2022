## PRAXTHON 2022 - Asistente Virtual: **Pandita**

<p align="center">
  <img src="https://github.com/badillo-christian/praxthon_2022/blob/main/blob/master/panda.png?raw=true" alt="Asistente pandita"/>
</p>

### Resumen:

  * Asistente virtual elaborado para el praxthon 2022
  * Reto:

<p align="center">
  <img src="https://github.com/badillo-christian/praxthon_2022/blob/main/blob/master/requerimiento.jpeg?raw=true" alt="Reto"/>
</p>

### Consideraciones previas:
  * El nombre del asistente es **Pandita**
  * Es necesario establecer el valor correcto del identificador de idioma español de acuerdo tu Sistema Operativo, en mi caso el español corresponde al identificador #2
  * Proyectos utilizados: 

````
pip install pyttsx3
pip install SpeechRecognition
pip install pywhatkit
pip install wikipedia
pip install PyAutoGUI
pip install googletrans==4.0.0-rc1

pip install opencv-python
pip install matplotlib
pip install mtcnn
pip install tensorflow
pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
````

### Comandos soportados:

** Para cada uno de estos comandos el asistente establece una conversación con el usuario por medio de voz y atiende a la solicitud realizada: **

- [x] COMANDO_QUE_HORA_ES >>> 'qué hora es'
- [x] COMANDO_QUE_DIA_ES >>> 'qué día es'
- [x] COMANDO_BUSCA_EN_WIKIPEDIA >>> 'busca en wikipedia'
- [x] COMANDO_BUSCA_EN_GOOGLE >>> 'busca en google'
- [x] COMANDO_BUSCA_EN_YOUTUBE >>>'busca en youtube'
- [x] COMANDO_BUSCA_EN_AMAZON >>> 'busca en amazon'
- [x] COMANDO_BUSCA_EN_LINKEDIN >>> 'busca en linkedin'
- [x] COMANDO_TRADUCE_AL_INGLES >>> 'traduce al inglés'
- [x] COMANDO_ENTRENA_ROSTRO_DE >>> 'entrena rostro de'
- [x] COMANDO_QUIEN_SOY >>> 'quién soy'
- [x] COMANDO_DETECTA_OBJETOS >>> 'detecta objetos'
- [x] COMANDO_PARAR >>> 'parar'



### Ejecución del asistente:

````
python .\asistente.py
````

### Ejemplo de comando *Búsqueda en Amazon*:

# *Pandita busca en amazon zapatos*

### Resultado del comando *Búsqueda en Amazon*:

*El asistente abre un navegador con el resultado de la busqueda:*

<p align="center">
  <img src="https://github.com/badillo-christian/praxthon_2022/blob/main/blob/master/resultado_amazon.png?raw=true" alt="Resultado comando"/>
</p>

*De igual forma el asistente genera un intent para el envío de un mensaje de whatsapp con la recomendación resultante de la búsqueda.*

<p align="center">
  <img src="https://github.com/badillo-christian/praxthon_2022/blob/main/blob/master/whatsapp.png?raw=true" alt="Resultado comando"/>
</p>

### Ejemplo de comando *Entrenar rostro*:

# *Pandita entrena rostro de Cris*

### Resultado del comando *Entrenar rostro*:

*El asistente se comunica con la camara del sistema y despliega el widget de la misma para capturar el rostro y almacenarlo*

<p align="center">
  <img src="https://github.com/badillo-christian/praxthon_2022/blob/main/blob/master/entrena_rostro_1.png?raw=true" alt="Widget Camara"/>
</p>

### Notas de implementación comando *Entrenar rostro*:

1. El asistente hace uso del modulo MTCNN - Multi-task Cascaded Convolutional Networks, para realizar la detección del rostro en la imagen.
2. Se obtiene una imagen normalizada con el puro rostro resultante de la ejecución del método:

````
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles) #Se obtienen la caras a través de Multi-task Cascaded Convolutional Networks
````
3. Se almacena la imagen con el nombre del rostro recibido en el comando, en este caso **cris**

<p align="center">
  <img src="https://github.com/badillo-christian/praxthon_2022/blob/main/blob/master/cris.jpg?raw=true" alt="cris.jpg"/>
</p>





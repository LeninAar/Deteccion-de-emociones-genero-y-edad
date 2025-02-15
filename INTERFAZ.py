import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import threading
from deepface import DeepFace
import uuid
import os
import tkinter as tk

# Función para crear la conexión con la base de datos
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            database='prediccionesdb1'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return None

# Función para guardar los datos en la base de datos
def save_to_database(imagen_path, resultado, genero, emocion, precision_edad, precision_genero, precision_emocion):
    connection = create_connection()
    
    if connection:
        cursor = connection.cursor()
        
        # Convertir los valores de precisión a tipo float explícitamente
        precision_edad = float(precision_edad)
        precision_genero = float(precision_genero)
        precision_emocion = float(precision_emocion)
        
        # Consulta para insertar los datos en la tabla Predicciones
        query = '''
            INSERT INTO Predicciones (Imagen, Edad_rango, Genero, Emocion, Precision_Edad, Precision_Genero, Precision_Emocion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        values = (imagen_path, resultado, genero, emocion, precision_edad, precision_genero, precision_emocion)
        
        cursor.execute(query, values)
        
        # Confirmar la transacción
        connection.commit()
        
        print("Datos guardados correctamente.")
        
        cursor.close()
        connection.close()

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Variable para controlar si la cámara está activa
camera_active = True

# Función para realizar predicciones con DeepFace
def get_predictions(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    gender, age, emotion = "", 0, ""
    gender_precision, age_precision, emotion_precision = 0.0, 0.0, 0.0

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face = frame[y:y+h, x:x+w]
        
        # Usar DeepFace para obtener las predicciones
        result = DeepFace.analyze(face, actions=["age", "gender", "emotion"], detector_backend='mtcnn')
        
        # Obtener predicciones (accedemos a los valores específicos del diccionario)
        if isinstance(result, list) and len(result) > 0:
            gender_probabilities = result[0].get('gender', {})
            age = result[0].get('age', 0)
            emotion = result[0].get('dominant_emotion', "")
            emotion_probabilities = result[0].get('emotion', {})
            
            if isinstance(gender_probabilities, dict):
                gender = max(gender_probabilities, key=gender_probabilities.get)
                gender_precision = gender_probabilities[gender] / 100.0
            
            # Calcular la precisión de la edad 
            age_precision = 1.0
            
            # Calcular la precisión de la emoción
            if isinstance(emotion_probabilities, dict):
                emotion_precision = emotion_probabilities[emotion] / 100.0 
    
    return gender, age, emotion, gender_precision, age_precision, emotion_precision

# Variables globales para almacenar las predicciones y precisiones
gender_pred = ""
age_pred = 0
emotion_pred = ""
gender_precision = 0.0
age_precision = 0.0
emotion_precision = 0.0

# Ruta donde se guardarán las imágenes
image_save_path = r"C:\Users\lenin\Desktop\Proyecto final\Modelos\FINAL\DATAC12"

if not os.path.exists(image_save_path):
    os.makedirs(image_save_path)

# Función que actualiza el frame de la cámara
def update_frame():
    global camera_active
    
    if camera_active:
        ret, frame = cap.read()
        if ret:
            # Mostrar la imagen en el flujo de la cámara
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img)
            
            lbl_camera.img_tk = img_tk
            lbl_camera.config(image=img_tk)
    
    ventana.after(10, update_frame)

# Función para capturar la imagen, realizar las predicciones y mostrar los resultados
def capture_image():
    global camera_active, gender_pred, age_pred, emotion_pred, gender_precision, age_precision, emotion_precision
    
    if camera_active:
        ret, frame = cap.read()
        if ret:
            frame_resized = cv2.resize(frame, (640, 480))
            
            random_filename = f"{uuid.uuid4()}.jpg"
            imagen_path = os.path.join(image_save_path, random_filename)  
            
            cv2.imwrite(imagen_path, frame_resized)
            
            # Mostrar la imagen en la interfaz
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img)
            
            lbl_photo.img_tk = img_tk
            lbl_photo.config(image=img_tk)
            
            gender_pred, age_pred, emotion_pred, gender_precision, age_precision, emotion_precision = get_predictions(frame_resized)
            
            if isinstance(gender_pred, dict):
                gender_pred = str(gender_pred)
            if isinstance(age_pred, dict):
                age_pred = 0
            if isinstance(emotion_pred, dict):
                emotion_pred = str(emotion_pred)
            
            if age_pred <= 12:
                resultado = "Niño/a"
            elif age_pred < 19:
                resultado = "Adolescente"
            elif age_pred > 18 and age_pred <= 27:
                resultado = "Adulto joven"
            elif age_pred > 27 and age_pred <= 65:
                resultado = "Adulto de mediana edad"
            else:
                resultado = "Anciano"

            
            if gender_pred == "Man":
                GENERO="Hombre"
            else:
                GENERO="Mujer"
            

                     

            lbl_gender.config(text=f"Género: {GENERO}")
            lbl_age.config(text=f"Edad: {resultado}")
            lbl_emotion.config(text=f"Emoción: {emotion_pred}")
            
            prediction_text = f"Usando las redes neuronales VGG-Face, Facenet, OpenFace, DeepID y Dlib,\nse predice que usted es un/a {GENERO} y tiene la edad de un/a {resultado}."

            lbl_result_text = Label(ventana, text=prediction_text, font=("Arial", 13), bg="gray70", fg="black",width=100, height=4)
            lbl_result_text.place(x=450, y=30) 

            # Guardar los datos en la base de datos
            save_to_database(imagen_path, age_pred, gender_pred, emotion_pred, age_precision, gender_precision, emotion_precision)
# Configuración de la interfaz gráfica con Tkinter
ventana = Tk()
ventana.title("Cámara y Predicciones")
ventana.geometry("1602x1000+-2+0")
ventana.iconbitmap("ico.ico")
# fondo
ruta_imagen1 = r"C:\Users\lenin\Desktop\Proyecto final\Modelos\FINAL\fondo.jpeg"  

imagen1 = Image.open(ruta_imagen1)
imagen_redimensionada1 = imagen1.resize((1400, 1400))
imagen_tk1 = ImageTk.PhotoImage(imagen_redimensionada1)

lbl_imagen1 = tk.Label(ventana, image=imagen_tk1, borderwidth=0, highlightthickness=0)
lbl_imagen1.place(x=200, y=-350)

# Crear un marco para el rectángulo de 1/8 del ancho de la pantalla
frame_camera = Frame(ventana, bg="deep sky blue", width=1602//8, height=1000)
frame_camera.place(x=0, y=0)

# 1
ruta_imagen = r"C:\Users\lenin\Desktop\Proyecto final\Modelos\FINAL\Captura.JPG"  

imagen = Image.open(ruta_imagen)
imagen_redimensionada = imagen.resize((180, 210))
imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

lbl_imagen = tk.Label(ventana, image=imagen_tk, borderwidth=0, highlightthickness=0)
lbl_imagen.place(x=10, y=100)


# tec
ruta_imagen3 = r"C:\Users\lenin\Desktop\Proyecto final\Modelos\FINAL\Captura3.JPG"  

imagen3 = Image.open(ruta_imagen3)
imagen_redimensionada3 = imagen3.resize((180, 60))
imagen_tk3 = ImageTk.PhotoImage(imagen_redimensionada3)

lbl_imagen3 = tk.Label(ventana, image=imagen_tk3, borderwidth=0, highlightthickness=0)
lbl_imagen3.place(x=10, y=350)

# Label para mostrar el flujo de la cámara
lbl_camera = Label(ventana, bg="black", bd=5, relief="groove")
lbl_camera.place(x=250, y=150, width=600, height=490)

# Botón para capturar una imagen

btn_capture = Button(ventana, text="Tomar Foto", command=capture_image, 
                     bg="gray70", fg="black", font=("Arial", 13, "bold"), 
                     borderwidth=3, relief="raised")

btn_capture.place(x=480, y=700)
btn_capture.config(width=15, height=2)

# Label para mostrar la imagen capturada
lbl_photo = Label(ventana, bg="black", bd=5, relief="groove")
lbl_photo.place(x=870, y=150)


# Labels para mostrar los resultados de género, edad y emoción
lbl_gender = Label(ventana, text="Género: ", font=("Open Sans", 16, "bold"),borderwidth=3, relief="raised")
lbl_gender.place(x=1040, y=671)

lbl_age = Label(ventana, text="Edad: ", font=("Open Sans", 16, "bold"),borderwidth=3, relief="raised")
lbl_age.place(x=1040, y=701)

lbl_emotion = Label(ventana, text="Emoción: ", font=("Open Sans", 16, "bold"),borderwidth=3, relief="raised")
lbl_emotion.place(x=1040, y=731)

# Iniciar la actualización de la cámara en un hilo separado para no bloquear la interfaz
def capture_and_process_frame():
    threading.Thread(target=update_frame).start()

ventana.after(10, capture_and_process_frame)

ventana.mainloop()

cap.release()
cv2.destroyAllWindows()

import mediapipe as mp
import cv2
import numpy as np
import pyrealsense2 as rs
import random
import winsound
import sys
#============================================================================================
#                                   MEDIAPIPE-POSE
#============================================================================================
mp_drawing = mp.solutions.drawing_utils                                                                     #Esta funcion proporciona los puntos y lineas para el dibujo
mp_drawing_styles = mp.solutions.drawing_styles                                                             #Prorciona estilos de dibujo
mp_pose = mp.solutions.pose                                                                                 #Modulo empleado para el seguimiento de la pose humana
#============================================================================================
#                                    MARCADORES
#============================================================================================
x_0, y_0 , x_11, y_11, x_12, y_12 , x_15, y_15, x_17, y_17, x_18, y_18, x_19, y_19, x_20, y_20 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

#============================================================================================
#                                    VARIABLES
#============================================================================================
stream_res_x = 1280                                                                                         #Resolucion de la pantalla de streamming en X
stream_res_y = 720                                                                                          #Resolucion d ela pantalla de streamming en Y
stream_fps = 30                                                                                             #Frames por segundo
background_remove_color = 153                                                                               #Todo aquello superior a una distancia especifica sera pintado de color gris
min_distance = 1.00                                                                                         #Distancia minima al hombro del individuo
max_distance = 1.60                                                                                         #Distancia maxima al hombro del individuo
bandera_should = False                                                                                      #Bandera de hombro. En caso de estar a la distancia correcta arroja True
bandera_seleccion = False                                                                                   #Bandera utilizada en el while de seleccion. Se la inicializa en False
opcion_seleccionada = 0                                                                                     #Variable para guardar la opcion seleccionada. Por ejemplo =1 cuando trabajamos con brazo derecho
opcion = 0                                                                                                  #Guardamos la opcion ingresada por consola
msj_right = str ('Mensaje inicial')                                                                         #Inicializamos el string del brazo derecho
msj_left = str ('Mensaje inicial')                                                                          #Inicializamos el string del brazo izquierdo
circle_radius = 50                                                                                          #Radio del circulo que se dibuja en pantalla. Estos son los que se deben tocar
circle_color = (0, 0, 255)                                                                                  #Color del circulo a tocar
max_valor = 0                                                                                               #si max_valor = 5 (brazo derecho o izquierdo), max_valor = 10 ambos brazos
desplazamiento = 100                                                                                        #Valor que se usa para mover en X los centros del circulo a la derecha
desplazamiento_neg = 0                                                                                      #Valor que se usa para mover en X los centros del circulo a la izquierda
circle_center = (int(stream_res_x/2), int(stream_res_y/2))                                                  #Circulo inicial en el centro de la ventana de streamming

#==============================================================================================             #Sonidos con los que se trabaja
#                               SONIDOS
#==============================================================================================
music_coincidence = 'Speech Disambiguation.wav'                                                             #Sonido de coincidencia

#============================================================================================
#                           INICIALIZAMOS LA CAMARA RS
#============================================================================================
pipeline = rs.pipeline()
config = rs.config()
# config.enable_device(device)
config.enable_stream(rs.stream.depth, stream_res_x, stream_res_y, rs.format.z16, stream_fps)                #Configuramos las ventanas de stream con un resolucion determinada
config.enable_stream(rs.stream.color, stream_res_x, stream_res_y, rs.format.bgr8, stream_fps)               #Configuramos las ventanas de stream con un resolucion determinada

# pipeline = pipeline.start()
profile = pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

depth_sensor = profile.get_device().first_depth_sensor()                                                    #Necesito obtener la escala de profndidad para luego hacer que todo 
depth_scale = depth_sensor.get_depth_scale()                                                                #el fondo sea "borrado"
print(f"\tDepth Scale for Camera is: {depth_scale}")
#============================================================================================
#                                       CENTRAR
#============================================================================================
def Centrar(marcadores, image, w, h):

    x_11 = int(marcadores.landmark[11].x*w)
    y_11 = int(marcadores.landmark[11].y*h)
    x_12 = int(marcadores.landmark[12].x*w)
    y_12 = int(marcadores.landmark[12].y*h)

    #Verificamos que los valores de x_12 y_12 no esten fuera de "escala" (hombro derecho)
    if x_11 >= len(flipped_depth_image[0]*depth_scale):
        x_11 = int(len(flipped_depth_image[0])-1)
    if y_11 >= len(flipped_depth_image[1]*depth_scale):
        y_11 = int(len(flipped_depth_image[1]-1))

    if x_12 >= len(flipped_depth_image[0]*depth_scale):
        x_12 = int(len(flipped_depth_image[0])-1)
    if y_12 >= len(flipped_depth_image[1]*depth_scale):
        y_12 = int(len(flipped_depth_image[1]-1))


    distancia_derecha = round(flipped_depth_image[y_11, x_11]*depth_scale, 2)
    distancia_izquierda = round(flipped_depth_image[y_12, x_12]*depth_scale, 2)
    
    if min_distance <= distancia_derecha <= max_distance or min_distance <= distancia_izquierda <= max_distance:
        bandera_should = True
    else:
        bandera_should = False  
    msj_right = f'Distancia hombro der: {distancia_derecha}'
    msj_left = f'Distancia hombro izq: {distancia_izquierda}'
    
    x_0 = int(results.pose_landmarks.landmark[0].x*w)
    y_0 = int(results.pose_landmarks.landmark[0].y*h)
    
    return bandera_should, x_0, y_0, x_11, y_11, x_12, y_12, msj_right, msj_left
#============================================================================================
#                               RECORTE DEL FONDO ("BORRADO")
#============================================================================================
clipping_distance_in_meters = 2                                                                             #Distancia de recorte en metros. Todo a dos metros de profundidad se recorta 
clipping_distance = clipping_distance_in_meters / depth_scale                                               #La distancia de recorte sale de esta operacion (El valor esta en mm)
print(f"La distancia de recorte es de {clipping_distance/1000} metros")                                     #Imprimo la distancia en mm. Por encima de ese valor no se muestra nada
#============================================================================================
#                               VENTANA EMERGENTE
#============================================================================================
while bandera_seleccion == False:
    mensaje = 'nada'
    mensaje_1 = "Seleccione una de las siguientes opciones: "                                               #En esta ventana emergente se presenta un menu de seleccion.
    mensaje_2 = "(1) - Trabajo con brazo derecho"                                                           #Permite seleccionar si se trabaja con un brazo o ambos
    mensaje_3 = "(2) - Trabajo con brazo izquierdo"
    mensaje_4 = "(3) - Trabajo con ambos brazos"
    mensaje_5 = "(4) - Salir"
    mensaje_6 = "Ingrese opcion: "
    
    print(mensaje_1)
    print(mensaje_2)
    print(mensaje_3)
    print(mensaje_4)
    print(mensaje_5)
    print(mensaje_6)
    opcion=input()
    if opcion == '1':
        mensaje = 'bazo derecho'
        bandera_seleccion = True
        opcion_seleccionada = 1
    elif opcion == '2':
        mensaje = 'brazo izquierdo'
        bandera_seleccion = True
        opcion_seleccionada = 2
    elif opcion == '3':
        mensaje = 'ambos brazos'
        bandera_seleccion = True
        opcion_seleccionada = 3
    elif opcion == '4':
        sys.exit()
    else:
        print ("OPCION NO VALIDA")
        bandera_seleccion == False    
    
#============================================================================================
#                               MOSTRAMOS IMAGENES
#============================================================================================
with mp_pose.Pose( min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    cont_frames = 0
    relleno = 0
    contador = 0
    conteo = 0
    evento = False
    cont_eventos = 1
    while True:
        evento = False
        color_ok = (0, 255, 0)                                                                          #Cuando los hombros estan a la distancia adecuada se vera el marcador de color verde
        color_no_ok = (0, 0, 255)                                                                       #En caso de no estar a la distancia adecuada el marcador aparecera rojo
        cont_frames = cont_frames + 1
        # print (cont_frames)                                                                           #Cuando se utiliza una cámara RealSense, los sensores de profundidad y color están 
        frames = pipeline.wait_for_frames()                                                             #físicamente separados, lo que puede resultar en una disparidad espacial 
        aligned_frames = align.process(frames)                                                          #entre los frames capturados por ambos sensores
        aligned_depth_frames = aligned_frames.get_depth_frame()                                         #La función  align.process()  se utiliza para alinear los frames de 
        color_frames = aligned_frames.get_color_frame()                                                 #profundidad y color, de modo que correspondan espacialmente y se 
                                                                                                        #puedan utilizar juntos en aplicaciones que requieren información de ambos sensores
        if not aligned_depth_frames or not color_frames:
            continue

        #============================================================================================
        #                           PROCESAMIENTO DE LA IMAGEN
        #============================================================================================
        
        depth_image = np.asanyarray(aligned_depth_frames.get_data())                                       #Convertimos los datos de profundidad en un arreglo de array para aprovechar las ventajas de la biblioteca numpy
        flipped_depth_image = cv2.flip(depth_image, 1)                                                     #Al usar "flip" y "1" espejamos la imagen de manera vertical 
        color_image = np.asanyarray(color_frames.get_data())                                               #Convertimos los datos de color en un arreglo de array para aprovechar las ventajas de la biblioteca numpy

        depth_image_3d = np.dstack((depth_image, depth_image, depth_image))                                #Dado que estamos buscando que la imagen de profundidad coincida con la de color, y sabiendo
                                                                                                           # que la imagen de color es una matriz de RGB. Proponemos armar una matriz de profundidad en
                                                                                                           #en la que RGB se le asigne "depth_image
        background_remove = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0),  
                                    background_remove_color, color_image)                                  #Todo aquello a una distancia superior de 2 m se mostrara con un fondo gris en la imagen a color

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        images = cv2.flip(background_remove, 1)                                                             #Imagen de salida
        color_image = cv2.flip(color_image, 1)
        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)                                      #Imagen para la deteccion de marcadores


        #============================================================================================
        #                                MARCADORES 
        #============================================================================================
        results = pose.process(color_image_rgb)
        height, widith, _ = color_image_rgb.shape                                                           #Obtenemos los valores de ancho y alto de la imagen. 
        if results.pose_landmarks is not None:

            #=======================================================================================        #Medimos la distancia a los hombros. Buscamos que ambos hombros esten
            #                               CENTRAMOS AL INDIVIDUO                                          #a la misma distancia (aproximadamente 1.5 metros)
            #=======================================================================================
            bandera_should, x_0, y_0, x_11, y_11, x_12, y_12, msj_right, msj_left = Centrar(results.pose_landmarks, images, stream_res_x, stream_res_y)
            
            #====================================================================================           #En base a las selecciones del menu se sleccionan y dibujan los marcadores
            #                MANO: DERECHA - IZQUIERDA - AMBAS          
            #====================================================================================
            if opcion_seleccionada == 1 or opcion_seleccionada == 3:
                x_17 = int(results.pose_landmarks.landmark[17].x*stream_res_x)
                y_17 = int(results.pose_landmarks.landmark[17].y*stream_res_y)
                x_19 = int(results.pose_landmarks.landmark[19].x*stream_res_x)
                y_19 = int(results.pose_landmarks.landmark[19].y*stream_res_y)

                images = cv2.circle(images, (x_17, y_17), radius = 6, color = color_ok, thickness=6)
                images = cv2.circle(images, (x_19, y_19), radius = 6, color = color_ok, thickness=6)
            if opcion_seleccionada == 2 or opcion_seleccionada == 3:
                x_18 = int(results.pose_landmarks.landmark[18].x*stream_res_x)
                y_18 = int(results.pose_landmarks.landmark[18].y*stream_res_y)
                x_20 = int(results.pose_landmarks.landmark[20].x*stream_res_x)
                y_20 = int(results.pose_landmarks.landmark[20].y*stream_res_y)

                images = cv2.circle(images, (x_18, y_18), radius = 6, color = color_ok, thickness=6)
                images = cv2.circle(images, (x_20, y_20), radius = 6, color = color_ok, thickness=6)
        #=======================================================================================
        #                        LINEA PARA CNETRAR CON MARCADOR DE NARIZ
        #=======================================================================================
        cv2.line(images, (640, 0), (640, 720), color = (0, 255, 0), thickness = 1, lineType = 1)
        #=======================================================================================
        #                           DIBUJAMOS LOS CIRCULOS
        #=======================================================================================
        if bandera_should == True:
            if opcion_seleccionada == 1:
                max_valor = 5
            elif opcion_seleccionada == 2:
                max_valor = 5 
                desplazamiento = -100 
            else:
                max_valor = 10
                desplazamiento = 100
                desplazamiento_neg = -100

            if cont_frames % 30 == 0 or evento == True:                                                         #Cuando se tenga un valor de contador == 30 se genera un numero                                                                                         
                relleno = random.randint(1, max_valor)                                                          #random entre 1-5 que me rellenaran el circulo en pantalla
                cont_frames = 0
                cont_eventos = cont_eventos + 1
                evento == False
                circle_color = (0, 0, 255)
            if relleno == 1:
                circle_center = (640 + desplazamiento , 100)
            elif relleno == 2:
                circle_center = (640 + 2*desplazamiento, 150)
            elif relleno == 3:
                circle_center = (640 + 3*desplazamiento, 300)
            elif relleno == 4 :
                circle_center = (640 + 4*desplazamiento, 450)
            elif relleno == 5:
                circle_center = (640 +3*desplazamiento + desplazamiento, 500)
            elif relleno == 6 and opcion_seleccionada == 3:
                circle_center = (640 + desplazamiento_neg, 100)
            elif relleno == 7 and opcion_seleccionada == 3:
                circle_center = (640 + 2*desplazamiento_neg, 150)
            elif relleno == 8 and opcion_seleccionada == 3:
                circle_center = (640 + 3*desplazamiento_neg, 300)
            elif relleno == 9 and opcion_seleccionada == 3:
                circle_center = (640 + 4*desplazamiento_neg, 450)
            else:
                circle_center = (640 +3*desplazamiento_neg+ desplazamiento, 500)
            aux_relleno = relleno
            #=======================================================================================            #Contamos los eventos donde los marcadores de la mano coinciden
            #                           CONTAMOS COINCIDENCIAS                                                  #con el circulo dibujado en pantalla
            #=======================================================================================        
            if opcion_seleccionada == 1 or opcion_seleccionada == 3:                                        
                distance_17 = np.sqrt((x_17 - circle_center[0])**2 + (y_17 - circle_center[1])**2)
                distance_19 = np.sqrt((x_19 - circle_center[0])**2 + (y_19 - circle_center[1])**2)

                if distance_17 <= circle_radius and distance_19 <= circle_radius:                               #al coincidir los marcadores de la mano y el circulo dibujado, 
                    contador += 1                                                                               #se calcula la distancia del centro de la esfera al marcador
                                                                                                                #si la distancia del marcador al origen del circulo es menor que el 
                    if contador % 15 == 0:                                                                      #radio del circulo se concidera como coincidencia y se cuenta
                        evento = True
                        conteo +=1
                        winsound.PlaySound(music_coincidence, winsound.SND_FILENAME)
                        circle_color = (255, 0, 0)
                        # continue
            

            if opcion_seleccionada == 2 or opcion_seleccionada == 3:
                distance_18 = np.sqrt((x_18 - circle_center[0])**2 + (y_18 - circle_center[1])**2)
                distance_20 = np.sqrt((x_20 - circle_center[0])**2 + (y_20 - circle_center[1])**2)

                if distance_18 <= circle_radius and distance_20 <= circle_radius:
                    contador += 1
                    # print("¡Evento de conteo!")
                    if contador % 15 == 0:
                        evento = True
                        conteo +=1
                        winsound.PlaySound(music_coincidence, winsound.SND_FILENAME)
                        circle_color = (255, 0, 0)
        
        # print("Promedio: ", conteo/cont_eventos)                                                              #Este dato puedo usarlo mas adelante. En caso que el nivel de coincidencias sea bajo
                                                                                                                #voy a modificar la velocidad con la que aparecen las bolas en funcion de este valor
                                                                                                                #En caso de un nivel de coincidencias alto voy a poder trabajar aumentando los valores
        #===========================================================================================            #Mostramos todos los datos por pantalla en la ventana
        #                         MOSTRAMOS LOS DATOS EN LA VENTANA DE STREAMMING
        #===========================================================================================
        images = cv2.rectangle(images, (440, 500), (840, 700), (0, 0, 0), -1)
        images = cv2.putText(images, msj_right, (450, 520), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        images = cv2.putText(images, msj_left, (450, 540), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        images = cv2.circle(images, (x_0, y_0), radius = 6, color = color_ok, thickness=6)
        msj_conteo = (f'Capturas: ')
        msj_eventos = (f'Pelotas:')
        if bandera_should == True:
            images = cv2.circle(images, (x_11, y_11), radius = 6, color = color_ok, thickness=6)
            images = cv2.circle(images, (x_12, y_12), radius = 6, color = color_ok, thickness=6)
            images = cv2.putText(images, str('Distancia Perfecta'), (450, 560), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        
        if bandera_should == False:
            images = cv2.circle(images, (x_11, y_11), radius = 5, color = color_no_ok, thickness=6)
            images = cv2.circle(images, (x_12, y_12), radius = 5, color = color_no_ok, thickness=6)
            images = cv2.putText(images, str('Alejese mas de la camara'), (450, 560), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        images = cv2.putText(images, str(msj_conteo), (450, 600), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        images = cv2.putText(images, str(conteo), (490, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        images = cv2.putText(images, str(msj_eventos), (650, 600), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, 2)
        images = cv2.putText(images, str(cont_eventos), (690, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, 2)
        cv2.circle(images, circle_center, circle_radius, circle_color, -1)
        cv2.imshow(f"se trabaja con: {mensaje}. Precione ESC para salir", images)
        key = cv2.waitKey(1)

        if key == 27:
            break

    pipeline.stop()




    


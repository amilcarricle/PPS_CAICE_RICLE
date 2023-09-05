import mediapipe as mp
import cv2
import pyautogui
import numpy as np
import math
import ctypes
from time import sleep
import webbrowser
import winsound

#___________________________________________________________________________________________________________________
#-----------------------------------------FUNCION TAMANIO DE PANTALLA DE LA PC--------------------------------------
#___________________________________________________________________________________________________________________

def Tamanio_Pantalla_PC():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    widith, hight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # print(widith, hight)
    return (widith, hight) 
#___________________________________________________________________________________________________________________
#----------------------------------------AJUSTAMOS LA VENTANA DE TRABAJO------------------------------------
#___________________________________________________________________________________________________________________

widith_PC, hight_PC = Tamanio_Pantalla_PC()
X_INI = 0
Y_INI = 0
WIDTH_RESIZE = widith_PC 
HIGTH_RESIZE = hight_PC 
X_FIN = widith_PC
Y_FIN = hight_PC
# X_INI = widith_PC * 0.01
# Y_INI = hight_PC * 0.01
# WIDTH_RESIZE = widith_PC * 0.01
# HIGTH_RESIZE = hight_PC * 0.01
# X_FIN = widith_PC -2 * X_INI 
# Y_FIN = hight_PC -2 * Y_INI 
NAME = "https://wordwall.net"
music_click = 'Speech Disambiguation.wav'
music_drag = 'chimes.wav'
NAVIGATOR = "chrome"
# color = (0 ,0, 0)
X_Y_INI = 200
aspecto_ratio_screen = (X_FIN - X_INI)/(Y_FIN - Y_INI)
print(aspecto_ratio_screen)
#-----------------------------------------------------------------------------------------------------------
#___________________________________________________________________________________________________________________
#-----------------------------------------FUNCION PARA ABRIR LA PAGINA DE TRABAJO-----------------------------------
#___________________________________________________________________________________________________________________

def Open_page(navigator,name):
    
    try:
        webbrowser.get(using=None).open(name)

    except:
        print(f"""Hay problemas al momento de abrir la pagina. Esto se puede deber a:
                a - El navegador no {navigator} no se encuentra instalado en la PC.
                b- La pagina seleccionada de juegos no existe o esta caida.

            """)
    return True

#___________________________________________________________________________________________________________________
#------------------------------------------------FUNCION PARA CALCULAR PUNTOS---------------------------------------
#___________________________________________________________________________________________________________________

def Calculo_Punto(x, y):

    return  np.array([x, y])
#___________________________________________________________________________________________________________________
#-----------------------------------------FUNCION PARA MOVER PUNTERO -----------------------------------------------
#___________________________________________________________________________________________________________________
"""
Movemos el puntero mediante la extencion del indice y el dedo medio y la flexion del anular y el meñique. 
 
"""
def Mover_Puntero(hand_landmarks, height, widith):
    
    bandera = False
    #MARCADORES DE INTERES
    x_0 = int(hand_landmarks.landmark[0].x*widith)
    y_0 = int(hand_landmarks.landmark[0].y*height)
    
    x_6 = int(hand_landmarks.landmark[6].x*widith)
    y_6 = int(hand_landmarks.landmark[6].y*height)

    x_8 = int(hand_landmarks.landmark[8].x*widith)
    y_8 = int(hand_landmarks.landmark[8].y*height)

    x_10 = int(hand_landmarks.landmark[10].x*widith)
    y_10 = int(hand_landmarks.landmark[10].y*height)

    x_12 = int(hand_landmarks.landmark[12].x*widith)
    y_12 = int(hand_landmarks.landmark[12].y*height)

    x_14 = int(hand_landmarks.landmark[14].x*widith)
    y_14 = int(hand_landmarks.landmark[14].y*height)

    x_16 = int(hand_landmarks.landmark[16].x*widith)
    y_16 = int(hand_landmarks.landmark[16].y*height)

    x_18 = int(hand_landmarks.landmark[18].x*widith)
    y_18 = int(hand_landmarks.landmark[18].y*height)

    x_20 = int(hand_landmarks.landmark[20].x*widith)
    y_20 = int(hand_landmarks.landmark[20].y*height)

    dist_p0_p_6 = math.sqrt((x_6 - x_0)**2 + (y_6 - y_0)**2)
    dist_p0_p_8 = math.sqrt((x_8 - x_0)**2 + (y_8 - y_0)**2)
    dist_p0_p_10 = math.sqrt((x_10 - x_0)**2 + (y_10 - y_0)**2)
    dist_p0_p_12 = math.sqrt((x_12 - x_0)**2 + (y_12 - y_0)**2)
    dist_p0_p_14 = math.sqrt((x_14 - x_0)**2 + (y_14 - y_0)**2)
    dist_p0_p_16 = math.sqrt((x_16 - x_0)**2 + (y_16 - y_0)**2)
    dist_p0_p_18 = math.sqrt((x_18 - x_0)**2 + (y_18 - y_0)**2)
    dist_p0_p_20 = math.sqrt((x_20 - x_0)**2 + (y_20 - y_0)**2)

    if dist_p0_p_8 > dist_p0_p_6 and dist_p0_p_12 > dist_p0_p_10 and dist_p0_p_14 > dist_p0_p_16 and dist_p0_p_18 > dist_p0_p_20:
        bandera = True
        # print(f"distancia0-6 {dist_p0_p_6}, distancia0-8 {dist_p0_p_8}")
        # print(f"distancia0-10 {dist_p0_p_10}, distancia0-12 {dist_p0_p_12}")
    return bandera, x_6, y_6
#___________________________________________________________________________________________________________________
#---------------------------------------------FUNCION CLICK NORMAL--------------------------------------------------
#___________________________________________________________________________________________________________________
"""
El click normal funciona flexionando los cuatro dedos, desde el indice al meñique
"""
def Click_Normal(hand_landmarks, height, widith):
    
    bandera = False
    x = 0
    y = 0
    #MARCADORES DE INTERES
    x_0 = int(hand_landmarks.landmark[0].x*widith)
    y_0 = int(hand_landmarks.landmark[0].y*height)
    
    x_6 = int(hand_landmarks.landmark[6].x*widith)
    y_6 = int(hand_landmarks.landmark[6].y*height)

    x_5 = int(hand_landmarks.landmark[5].x*widith)
    y_5 = int(hand_landmarks.landmark[5].y*height)

    x_8 = int(hand_landmarks.landmark[8].x*widith)
    y_8 = int(hand_landmarks.landmark[8].y*height)

    x_12 = int(hand_landmarks.landmark[12].x*widith)
    y_12 = int(hand_landmarks.landmark[12].y*height)

    x_18 = int(hand_landmarks.landmark[18].x*widith)
    y_18 = int(hand_landmarks.landmark[18].y*height)

    x_20 = int(hand_landmarks.landmark[20].x*widith)
    y_20 = int(hand_landmarks.landmark[20].y*height)

    dist_p0_p_6 = math.sqrt((x_6 - x_0)**2 + (y_6 - y_0)**2)
    dist_p0_p_8 = math.sqrt((x_8 - x_0)**2 + (y_8 - y_0)**2)
    dist_p0_p_8 = math.sqrt((x_8 - x_0)**2 + (y_8 - y_0)**2)
    dist_p0_p_18 = math.sqrt((x_18 - x_0)**2 + (y_18 - y_0)**2)
    dist_p0_p_20 = math.sqrt((x_20 - x_0)**2 + (y_20 - y_0)**2)

    if dist_p0_p_6 > dist_p0_p_8 and dist_p0_p_18 > dist_p0_p_20:
        bandera = True
    return bandera , x_6, y_6
#___________________________________________________________________________________________________________________
#-----------------------------------------------FUNCION DE ARRASTRE-------------------------------------------------
#___________________________________________________________________________________________________________________

def Click_Arrastre(hand_landmarks, height, widith):
    
    bandera = False
    #MARCADORES DE INTERES
    x_0 = int(hand_landmarks.landmark[0].x*widith)
    y_0 = int(hand_landmarks.landmark[0].y*height)
    
    x_6 = int(hand_landmarks.landmark[6].x*widith)
    y_6 = int(hand_landmarks.landmark[6].y*height)

    x_8 = int(hand_landmarks.landmark[8].x*widith)
    y_8 = int(hand_landmarks.landmark[8].y*height)

    x_10 = int(hand_landmarks.landmark[10].x*widith)
    y_10 = int(hand_landmarks.landmark[10].y*height)

    x_12 = int(hand_landmarks.landmark[12].x*widith)
    y_12 = int(hand_landmarks.landmark[12].y*height)

    dist_p0_p_6 = math.sqrt((x_6 - x_0)**2 + (y_6 - y_0)**2)
    dist_p0_p_8 = math.sqrt((x_8 - x_0)**2 + (y_8 - y_0)**2)
    dist_p0_p_10 = math.sqrt((x_10 - x_0)**2 + (y_10 - y_0)**2)
    dist_p0_p_12 = math.sqrt((x_12 - x_0)**2 + (y_12 - y_0)**2) 

    if dist_p0_p_8 < dist_p0_p_6 and dist_p0_p_8 < dist_p0_p_12 and dist_p0_p_12 > dist_p0_p_10:
        bandera = True
    return bandera, x_6, y_6

#___________________________________________________________________________________________________________________
#--------------------------------------------------DOBLE CLICK------------------------------------------------------
#___________________________________________________________________________________________________________________
"""
Funcion que implementa el doble click. Se efectua cuando se flexionan los dedos indice y medio mientras se dejan 
extendidoss los dedos anular y meñique
"""
def Doble_Click(hand_landmarks, height, widith):
    
    bandera = False
    #MARCADORES DE INTERES
    x_0 = int(hand_landmarks.landmark[0].x*widith)
    y_0 = int(hand_landmarks.landmark[0].y*height)
    
    x_6 = int(hand_landmarks.landmark[6].x*widith)
    y_6 = int(hand_landmarks.landmark[6].y*height)

    x_8 = int(hand_landmarks.landmark[8].x*widith)
    y_8 = int(hand_landmarks.landmark[8].y*height)

    x_10 = int(hand_landmarks.landmark[10].x*widith)
    y_10 = int(hand_landmarks.landmark[10].y*height)

    x_12 = int(hand_landmarks.landmark[12].x*widith)
    y_12 = int(hand_landmarks.landmark[12].y*height)

    x_14 = int(hand_landmarks.landmark[14].x*widith)
    y_14 = int(hand_landmarks.landmark[14].y*height)

    x_16 = int(hand_landmarks.landmark[16].x*widith)
    y_16 = int(hand_landmarks.landmark[16].y*height)

    dist_p0_p_6 = math.sqrt((x_6 - x_0)**2 + (y_6 - y_0)**2)
    dist_p0_p_8 = math.sqrt((x_8 - x_0)**2 + (y_8 - y_0)**2)
    dist_p0_p_10 = math.sqrt((x_10 - x_0)**2 + (y_10 - y_0)**2)
    dist_p0_p_12 = math.sqrt((x_12 - x_0)**2 + (y_12 - y_0)**2) 
    dist_p0_p_14 = math.sqrt((x_14 - x_0)**2 + (y_14 - y_0)**2)
    dist_p0_p_16 = math.sqrt((x_16 - x_0)**2 + (y_16 - y_0)**2)

    if dist_p0_p_6 > dist_p0_p_8 and dist_p0_p_10 > dist_p0_p_12 and dist_p0_p_16 > dist_p0_p_14:
        bandera = True
    return bandera, x_6, y_6    

mpdraw = mp.solutions.drawing_utils
mphand = mp.solutions.hands

cap = cv2.VideoCapture(0)


# bandera_click = False
x_last_click = 0
y_last_click= 0
x_aux = 0
y_aux = 0
pos = f"xm = {0} ; ym = {0}"
delay = 2
cont = 0
aumento = 1.0
color_click = (0, 0, 0)
mensaje2 = f"Escala 1-1"
# with mphand.Hands(static_image_mode = False,
#                       max_num_hands = 1,
#                       min_detection_confidence = 0.5 
#                       ) as hand:
with mphand.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.5) as hand:    
    Open_page(NAVIGATOR, NAME)
    # succes, frame = cap.read()
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cam_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    mensaje = str('EL PUNTERO NO SE MUEVE')#Aca tengo que agregar un contador de tiempo
    click_cont = 0
    pos_arr = f"xm_a = {0} ; ym_a = {0}"
    pos_click = f"xm_c = {0}; ym_c = {0}"
    cont_click = 0
    while cap.isOpened():
        #comprobar entrada 
        exito, frame = cap.read()
        if not exito:
            # print("Frame de camara ignorado")
            continue
        # cont_click = 0

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_RGB2BGR)

        height, widith, _ = frame.shape
        factor_h = (hight_PC/cam_h)
        factor_w = (widith_PC/cam_w)
        height_m = int(height*(factor_h))
        widith_m = int(widith*(factor_w))

        # print(f"cam_h: {cam_h}; cam_w: {cam_w}")
        #print(f"factor_h: {factor_h}; factor_w:{factor_w}")
        # print(f"heigh_m:{height_m}; widith_m:{widith_m}")
        results = hand.process(frame)
        area_width = widith - X_Y_INI * 2
        area_height = int( area_width / aspecto_ratio_screen)
        
        if results.multi_hand_landmarks is not None:

            for hand_landmarks in results.multi_hand_landmarks:
                
                bandera_mov, x_p, y_p= Mover_Puntero(hand_landmarks, height, widith)

                bandera_click_normal, x_n, y_n = Click_Normal(hand_landmarks, height, widith)

                bandera_click_arrastre, x_c, y_c = Click_Arrastre(hand_landmarks, height, widith)

                bandera_doble_click, x_2c, y_2c =Doble_Click(hand_landmarks, height, widith)

                mpdraw.draw_landmarks(
                    frame, hand_landmarks, mphand.HAND_CONNECTIONS)
#===================================MOVIMIENTO DEL MOUSE=====================================================
                if bandera_mov == True and bandera_click_normal == False and bandera_click_arrastre == False and bandera_doble_click == False:

                    xm = int(np.interp(x_p, (X_Y_INI, X_Y_INI + area_width), (X_INI, X_FIN)))
                    ym = int(np.interp(y_p, (X_Y_INI, X_Y_INI + area_height), (Y_INI, Y_FIN)))
                    # print(f"Xm:{xm}; Ym:{ym}")
                    # print(f"Xm_m:{xm*factor_w}; Ym_m:{ym*factor_h}")
                    xm = int(xm*aumento)
                    ym = int(ym*aumento)
                    #if xm > 0 and xm < widith_PC and ym > 0 and ym < hight_PC:
                    if (0 < xm < widith_PC) and  (0 < ym < hight_PC):
                        pyautogui.moveTo(int(xm), int(ym))
                        # pyautogui.moveTo(xm*factor_w , ym*factor_h)
                        pos = f"xm = {int(xm)} ; ym = {int(ym)}"
                        mensaje = str('MOVIENDO PUNTERO')
#===================================CLICK NORMAL==========================================================
                if bandera_mov == False and bandera_click_normal == True and bandera_click_arrastre == False and bandera_doble_click == False:
                    cont = cont + 1
                    # print(f"CLICK N° {cont}")
                    winsound.PlaySound(music_click, winsound.SND_FILENAME)
                    # sleep(delay)
                    # xm_n = np.interp(x_n, (X_Y_INI, X_Y_INI + area_width), (X_INI, X_FIN))
                    # ym_n = np.interp(y_n, (X_Y_INI, X_Y_INI + area_width), (X_INI, X_FIN))
                    mensaje = str("CLICK")
                    pyautogui.click()
#===================================CLICK DE ARRASTRE=====================================================
                if bandera_click_arrastre == True and bandera_click_normal == False and bandera_mov == False and bandera_doble_click == False:
                    
                    if click_cont == 0:
                        pyautogui.click()
                        # print("Primer Click")
                        winsound.PlaySound(music_drag, winsound.SND_FILENAME)

                        # sleep(delay)

                        x_last_click ,y_last_click = pyautogui.position()
                        # print(x_last_click, y_last_click)
                        xm_c = np.interp(x_last_click, (X_Y_INI, X_Y_INI + area_width), (X_INI, X_FIN))
                        ym_c = np.interp(y_last_click, (X_Y_INI, X_Y_INI + area_height), (Y_INI, Y_FIN))
                        pos_click =  f"xm_c ={int(xm_c)} ; ym_c =  {int(ym_c)}"

                        mensaje = str('Click')
                        
                        # print(f"Contador = {click_cont}")
                        # print("________________________")
                        # print(f"x : {int(x_last_click)} ; y: {int(y_last_click)}")
                        # print(f"x : {int(x_aux)} ; y: {int(y_aux)}")                    
                        click_cont += 1
                        mensaje = str("PRIMER CLICK DE ARRASTRE")
                        color_click = (0, 0, 255)
                    else: 
                        pyautogui.click()
                        # print("Segundo Click")
                        winsound.PlaySound(music_drag, winsound.SND_FILENAME)

                        # sleep(delay)
                        x_aux = x_last_click
                        y_aux = y_last_click
                        x_last_click ,y_last_click = pyautogui.position()
                        # print(f"Contador = {click_cont}")
                        # print("________________________")
                        # print(f"x : {int(x_aux)} ; y: {int(y_aux)}") 
                        # print(f"x : {int(x_last_click)} ; y: {int(y_last_click)}")
                        click_cont = 0
                        # print("ARRASTRANDO")
                        color_click = (0, 255, 0)
                        # sleep(delay)
                        pyautogui.moveTo(x_aux, y_aux)
                        mensaje = str("SEGUNDO CLICK DE ARRASTRE")
                    pyautogui.dragTo(x_last_click, y_last_click, 0.5)
                    # print("FINALIZADO")

#======================================DOBLE CLICK===========================================================
            if bandera_click_arrastre == False and bandera_click_normal == False and bandera_mov == False and bandera_doble_click == True:
                pyautogui.doubleClick()

        #Dibujo un area proporcional a la del monitor
        aux_image = np.zeros(frame.shape, np.uint8)
        aux_image = cv2.rectangle (aux_image, (X_Y_INI , X_Y_INI),  
                                    (X_Y_INI  + area_width, X_Y_INI+ area_height),   
                                    (255, 250, 0), -1)            

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Captura",frame)
        output = cv2.addWeighted(frame, 1, aux_image, 0.3, 0)
        cv2.rectangle(output, (0, 0), (300, 90), (0, 0, 0), -1)
        
        cv2.putText(output,mensaje, (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(output,mensaje2, (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 1)
        cv2.circle(output, (10, 40), radius = 6, color = color_click, thickness=6)
        # cv2.putTextou(output, str(pos), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (125, 255, 0), 2)
        # cv2.putText(output, (pos_click), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (125, 255, 0), 2)
        # cv2.putText(output, str(pos_arr), (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.5, (125, 255, 0), 2)

        cv2.imshow("Captura", output)
        key = cv2.waitKey(1)
        if key == 43:
            print("PLUS")
            aumento = aumento + 0.5
            # print(f"Aumento:{aumento}")
            mensaje2 = f"Escala 1:{aumento}"
        if key == 45 and aumento > 0.5:
            print("MINUS")
            aumento = aumento - 0.5
            mensaje2 = f"Escala 1:{aumento}"
            # print(f"Decremento: {aumento}")
        if key == 27:
            break
cv2. destroyAllWindows()
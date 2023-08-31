import sys
from machine import I2C, Pin, ADC
from I2C_LCD import I2cLcd
import time
import utime
import sys
import _thread
from myservo import Servo

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
i2c_add = i2c.scan()[0]

ledVert = Pin(13, Pin.OUT)
ledRouge = Pin(16, Pin.OUT)

#Capteur Distances
trigger = Pin(19, Pin.OUT)
echo = Pin(18, Pin.IN)
distance = 0
velocite_son = 340

#Servomoteur
servo = Servo(15)
adc = ADC(26)
servo.ServoAngle(0)

ecranLCD = I2cLcd(i2c, i2c_add, 2, 16)

#Joystick
xAxis = ADC(Pin(28))
yAxis = ADC(Pin(27))
buttonJoystick = Pin(26,Pin.IN, Pin.PULL_UP)

terminateThread = False
typeCapture = ""

def lectureDistance():
    #Fonction qui calcule et retourne la distance détectée
	trigger.value(1)
	time.sleep_us(10)
	trigger.value(0)
 
	while not echo.value():
		pass
	ping_debut = time.ticks_us()
 
	while echo.value():
		pass
	ping_fin = time.ticks_us()
 
	distance_temps = time.ticks_diff(ping_fin, ping_debut) // 2
	distance = (velocite_son* distance_temps) // 10000
 
	return distance

def afficherMesureLCD(typeMesure, valeur):
    ecranLCD.clear()
    
    #Affichage différent selon le type de mesure
    if typeMesure == "distance":
        ecranLCD.putstr("Objet detecte a:\n" + str(valeur) + "cm")
    else:
        ecranLCD.putstr("Angle actuel:\n" + str(valeur) + " degrees")
        
    time.sleep(2)
    ecranLCD.clear()
    ecranLCD.putstr("Appuyer pour\nafficher mesure")
    

def demarrerSysteme():
    global terminateThread, distance, typeCapture
    global angleInt
    
    ledVert.on()
    ledRouge.off()
    
    #Affichage de démarrage. Indique le type de mesure
    if typeCapture == "distance":
        ecranLCD.putstr("DEMARRAGE\nDISTANCE")
    elif typeCapture == "angle":
        ecranLCD.putstr("DEMARRAGE\nANGLE")
    time.sleep(2)
    ecranLCD.clear()
    ecranLCD.putstr("Appuyer pour\nafficher mesure")
    
    angleInt = 0
    servo.ServoAngle(0)
    
    while not terminateThread:
        xValue = xAxis.read_u16()
        
        if xValue <= 32000:
            #Inclinaison du joystick à gauche
            if angleInt + 2 <= 180:
                angleInt = angleInt + 2
                servo.ServoAngle(angleInt)
        elif xValue >= 34000:
            #Inclinaison du joystick à droite
            if angleInt - 2 >= 0:
                angleInt = angleInt - 2
                servo.ServoAngle(angleInt)
        
        #Si le joystick est appuyé et on capture la distance
        if buttonJoystick.value() == 0 and typeCapture == "distance":
            time.sleep(0.5)
            distance = lectureDistance()
            afficherMesureLCD("distance", distance)
            time.sleep(0.5)
        
        #Si le joystick est appuyé et on capture l'angle
        if buttonJoystick.value() == 0 and typeCapture == "angle":
            time.sleep(0.5)
            afficherMesureLCD("angle", angleInt)
            time.sleep(0.5)
            
        utime.sleep(0.1)
  
	 
def arreterSysteme():
    global terminateThread, distance, angleInt, typeCapture
    terminateThread = True
    valeurRetournee = 0
    
    if typeCapture == "distance":
        distance = lectureDistance()
        ecranLCD.clear()
        ecranLCD.putstr("MESURE PRISE:\n" + str(distance) + "cm")
        valeurRetournee = distance
    elif typeCapture == "angle":
        ecranLCD.clear()
        ecranLCD.putstr("MESURE PRISE:\n" + str(angleInt) + " degrees")
        valeurRetournee = angleInt
    
    typeCapture = ""
        
    ledRouge.off()
    ledVert.off()

    for i in range(5):
        time.sleep(1)
        ledVert.toggle()
    
    ecranLCD.clear()

    #Retour vers l'hôte de la distance ou de l'angle
    print(valeurRetournee)
    
def afficherErreur():
    global terminateThread
    terminateThread = True
    
    ecranLCD.clear()
    ecranLCD.putstr("DESCRIPTION\nMANQUANTE")
    
    ledRouge.off()
    ledVert.off()
    
    for i in range(5):
        time.sleep(1)
        ledRouge.toggle()
    
    
    time.sleep(2)
    ecranLCD.clear()
    ecranLCD.putstr("ARRET")
    time.sleep(2)
    ecranLCD.clear()
    

while True:
    rep = sys.stdin.readline().strip()
    
    if rep.lower() == "demarrerdistance":
        terminateThread = False
        typeCapture = "distance"
        _thread.start_new_thread(demarrerSysteme, ())
    elif rep.lower() == "demarrerangle":
        typeCapture = "angle"
        terminateThread = False
        _thread.start_new_thread(demarrerSysteme, ())
    elif rep.lower() == "arreter":
        arreterSysteme()
    elif rep.lower() == "descriptionvide":
        afficherErreur()

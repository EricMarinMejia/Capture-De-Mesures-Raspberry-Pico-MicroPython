import tkinter as tk
from tkinter import ttk
import serial
import moduleMesure as module
import time
import datetime
import connexionBD as bd

serialPort = serial.Serial("COM3")

class Interface(tk.Tk):
    
    typeCapture = ""
    
    def setCapture(self, typeCapture):
        self.typeCapture = typeCapture
    
    def demarrerSysteme(self, labelStatus, textBoxDescription):
        labelStatus.config(text="ACTIVÉ", fg="green")
        textBoxDescription.config(state="normal")
        
        if self.typeCapture == "distance":
            serialPort.write(b"DEMARRERDISTANCE\n")
        elif self.typeCapture == "angle":
            serialPort.write(b"DEMARRERANGLE\n")
        
    
    def prendreMesure(self, labelStatus, textBoxDescription, listBoxMesures):
        
        #Si une description est rentrée
        if textBoxDescription.get("1.0", "end-1c") != "":
            labelStatus.config(text="DÉSACTIVÉ", fg="red")

            description = textBoxDescription.get("1.0", "end-1c")
            textBoxDescription.delete('1.0', tk.END)
            textBoxDescription.config(state="disabled")
            
            serialPort.write(b"ARRETER\n")
            data_in = serialPort.readline()
            donnees = data_in.decode("utf-8").strip()

            if self.typeCapture == "distance":
                self.creerMesure(donnees, listBoxMesures, description, "distance")
            elif self.typeCapture == "angle":
                self.creerMesure(donnees, listBoxMesures, description, "angle")
        else:
            labelStatus.config(text="DÉSACTIVÉ", fg="red")
            text = textBoxDescription.get("1.0", "end-1c")
            textBoxDescription.delete('1.0', tk.END)
            textBoxDescription.config(state="disabled")
            serialPort.write(b"DESCRIPTIONVIDE\n")
        
    def creerMesure(self, mesure, listBoxMesures, description, typeDeMesure):
        date = datetime.datetime.now()
        dateStr = date.strftime("%c")
        objetMesure = module.Mesure(dateStr, description, mesure, typeDeMesure)
        listBoxMesures.insert(tk.END, objetMesure)
        
        bd.connexionDB()
        
        if bd.verifierExisteTable("MESURES") == False:
            bd.creationBaseDeDonnées()
            
        bd.ajouterMesure(dateStr, description, mesure, typeDeMesure)
        
        bd.fermetureDB()
        print("-----------------------------------------------------")
        
    
    def __init__(self):
        super().__init__()
        self.title("TP4 Eric Marin")
        self.geometry("600x600")
        self.resizable(False, False)
        
        frame1 = ttk.Frame(self)
        frame1.pack(side=tk.TOP)

        frame2 = ttk.Frame(self)
        frame2.pack(side=tk.BOTTOM)
        
        labelLogo = tk.Label(frame1, text="SONAR STANCE\nTECHNOLOGIES", font=('Copperplate Gothic Bold', 10), borderwidth=1, relief="solid")
        labelLogo.config(bg="orange")
        labelLogo.pack()
        
        labelTitre = tk.Label(frame1, text="Logiciel de mesures", font=('Helvetica', 16))
        labelTitre.pack()
        
        labelMesures = tk.Label(frame1, text="Mesures:", font=('Helvetica', 12))
        labelMesures.pack(pady=(10,0))
        
        listBoxMesures = tk.Listbox(frame1, height=12, width=100)
        listBoxMesures.pack()
        
        ######### ECRIRE MÉTHODE POUR COMMANDE POUR SETCAPTURE SOIT DISTANCE OU ANGLE
        labelChoix = tk.Label(frame1, text="Que voulez-vous capturer?", font=('Helvetica', 12))
        labelChoix.pack()
        
        radioVar = tk.IntVar()
        
        radioDistance = tk.Radiobutton(frame1, text = "Distance", variable = radioVar, value = 1, command=lambda: self.setCapture("distance"))
        radioDistance.pack()
        
        radioAngle = tk.Radiobutton(frame1, text = "Angle du moteur", variable = radioVar, value = 2, command=lambda: self.setCapture("angle"))
        radioAngle.pack()
        
        radioDistance.select()
        ################
        
        labelDescription = tk.Label(frame1, text="Entrez une description:", font=('Helvetica', 12))
        labelDescription.pack(pady=(20,0))
        
        textBoxDescription = tk.Text(frame1, width=60, height=3, state="disabled")
        textBoxDescription.pack()
        
        
        labelStatus = tk.Label(frame1, text="DÉSACTIVÉ", font=('Helvetica', 12))
        labelStatus.pack(pady=(20,0))
        
        boutonDemarrer = tk.Button(frame2, text="Démarrer la capture", bg='#3CBA4C', command=lambda: self.demarrerSysteme(labelStatus, textBoxDescription))
        boutonDemarrer.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        boutonStop = tk.Button(frame2, text="Capturer la mesure", bg='#f44336', command=lambda: self.prendreMesure(labelStatus, textBoxDescription, listBoxMesures))
        boutonStop.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
    
if __name__ == "__main__":
    app = Interface()
    app.mainloop()
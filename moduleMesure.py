class Mesure:
    dateHeureMesure = ""
    description = ""
    dataMesure = []
    
    def __init__(self, dateHeureMesure, description, dataMesure):
        self.dateHeureMesure = dateHeureMesure
        self.description = description
        self.dataMesure.append(dataMesure)
        
    def __repr__(self):
        return "[" + self.dateHeureMesure + "] " + str(self.dataMesure[0]) + " cm - " + self.description
    
    def afficherMesure(self):
        return str(self.dateHeureMesure) + "\n" + self.description + "\n" + self.dataMesure
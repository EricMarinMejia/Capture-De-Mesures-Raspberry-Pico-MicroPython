class Mesure:
    dateHeureMesure = ""
    description = ""
    typeDeMesure = ""
    dataMesure = []
    
    def __init__(self, dateHeureMesure, description, dataMesure, typeDeMesure):
        self.dataMesure = []
        self.dateHeureMesure = dateHeureMesure
        self.description = description
        self.typeDeMesure = typeDeMesure
        self.dataMesure.append(dataMesure)
        
    def __repr__(self):
        if self.typeDeMesure == "angle":
            return "[" + self.dateHeureMesure + "] " + str(self.dataMesure[0]) + " degrées - " + self.description
            
        return "[" + self.dateHeureMesure + "] " + str(self.dataMesure[0]) + " cm - " + self.description
    
    def afficherMesure(self):
        return str(self.dateHeureMesure) + "\n" + self.description + "\n" + self.dataMesure
    
    def __eq__(self, other):
        #Compare la date/heure/seconde
        if not isinstance(other, Mesure):
            return NotImplemented

        return self.dateHeureMesure == other.dateHeureMesure
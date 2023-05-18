import sqlite3

connexion = ""
nomBD = "Tp-Synthese-DB.db"
table_mesures = "MESURES"
cle_no = "noMesure"
cle_date = "date"
cle_description = "description"
cle_mesure = "mesure"
cle_typeMesure = "typeMesure"

def connexionDB():
    global connexion
    try:
        connexion = sqlite3.connect(nomBD)
        print("[INFO] Connexion à la base de données réussite")
    except sqlite3.Error as error:
         print("[ERREUR] Connexion à la base de données échouée", error)
         
         
def fermetureDB():
    if connexion:
        connexion.close()
        print("[FIN] Fermeture de la connexion vers la base de données")
    else:
        print("[ERREUR] Connexion à la base de données échouée")
        
def verifierExisteTable(table):
    existe = False
    
    cur = connexion.cursor()
    
    sql_tableExiste = "SELECT count(name) "\
                      "FROM sqlite_master "\
                      "WHERE type='table' AND name='" + table + "'"
    
    try:
        cur.execute(sql_tableExiste)
        
        if cur.fetchone()[0]==1:
            existe = True
        else:
            existe = False
    
    except sqlite3.Error as error:
        print("[ERREUR] Vérification de l'existance de la table 'MESURES' échouée", error)
        
    return existe
        
        
def creationBaseDeDonnées():  
        
        tableDistances = """CREATE TABLE "MESURES" (
	                        "noMesure"	INTEGER,
	                        "date"	TEXT NOT NULL,
	                        "description"	TEXT NOT NULL,
	                        "mesure"	INTEGER NOT NULL,
	                        "typeMesure"	TEXT NOT NULL,
	                        PRIMARY KEY("noMesure" AUTOINCREMENT)
                            );"""
                                                        
        connexionDB()
        
        if verifierExisteTable(table_mesures):
            print("[INFO] La table 'MESURES' existe déjà")
        else:
            try:
                connexion.execute(tableDistances)
                print("[INFO] Création de la table 'DISTANCES' réussite")
            except:
                print("[ERREUR] Création de la table 'DISTANCES' échouée")
        
        fermetureDB()


def ajouterMesure(date, description, mesure, typeDeMesure):
    sql_insert = "INSERT INTO " + table_mesures + " (" + cle_date + ", " + cle_description + ", " + cle_mesure + ", " + cle_typeMesure + ") VALUES (?, ?, ?, ?);"
    
    connexionDB()
    
    try:        
        cur_insert = connexion.cursor()
        data_param = (date, description, mesure, typeDeMesure)
        cur_insert.execute(sql_insert, data_param)
        
        connexion.commit()
        print("[INFO] Insertion de données dans la table 'MESURES' réussite")
        
        cur_insert.close()
        
    except:
        print("[ERREUR] Insertion de données dans la table 'MESURES' échouée")
    finally:
        fermetureDB()
        
        

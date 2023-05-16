import sqlite3

connexion = ""
nomBD = "Tp-Synthese-DB.db"
table_distances = "DISTANCES"
cle_no = "noMesure"
cle_date = "date"
cle_description = "description"
cle_distance = "distance"

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
        print("[ERREUR] Vérification de l'existance de la table 'DISTANCES' échouée")
        
    return existe
        
        
def creationBaseDeDonnées():  
        
        tableDistances = """CREATE TABLE "DISTANCES" (
                            "noMesure"	INTEGER,
                            "date"	TEXT NOT NULL,
                            "description"	TEXT NOT NULL,
                            "distance"	INTEGER NOT NULL,
                            PRIMARY KEY("noMesure" AUTOINCREMENT)
                            );"""
                                                        
        connexionDB()
        
        if verifierExisteTable(table_distances):
            print("[INFO] La table 'DISTANCES' existe déjà")
        else:
            try:
                connexion.execute(tableDistances)
                print("[INFO] Création de la table 'DISTANCES' réussite")
            except:
                print("[ERREUR] Création de la table 'DISTANCES' échouée")
        
        fermetureDB()


def ajouterMesure(date, description, distance):
    sql_insert = "INSERT INTO " + table_distances + " (" + cle_date + ", " + cle_description + ", " + cle_distance + ") VALUES (?, ?, ?);"
    
    connexionDB()
    
    try:        
        cur_insert = connexion.cursor()
        data_param = (date, description, distance)
        cur_insert.execute(sql_insert, data_param)
        
        connexion.commit()
        print("[INFO] Insertion de données dans la table 'DISTANCES' réussite")
        
        cur_insert.close()
        
    except:
        print("[ERREUR] Insertion de données dans la table 'DISTANCES' échouée")
    finally:
        fermetureDB()
        
        

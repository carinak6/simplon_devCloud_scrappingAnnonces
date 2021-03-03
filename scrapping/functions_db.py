import requests
import pprint

import datetime

import mysql.connector

class ConnectionBDD:
    def __init__(self):
        #, dbName, user, passwd, host
        #"Établissement de la connexion - Création du curseur"
        try:
            self.cnx = mysql.connector.connect(user='root', password='sha', host='my_mysql', database='bd_scrapping', use_unicode=True, charset='utf8')
            print('connexion reussi') 
            #self.mycursor = self.cnx.cursor()
            self.echec =0

        except mysql.connector.Error as err:
            print("Something went wrong, La connexion avec la base de données a échoué : {}".format(err))       
            self.echec =1 
       
    
    def create_tables(self):
        mon_curseur = self.cnx.cursor()
        mon_curseur.execute("CREATE TABLE offer (offer_id INTEGER AUTO_INCREMENT PRIMARY KEY, titre VARCHAR(200) NOT NULL, description TEXT NOT NULL, date_offre TEXT, salaire VARCHAR(100), localisation VARCHAR(200), id_entreprise INT, date_current DATE, lien TEXT NULL)")
        mon_curseur.execute("CREATE TABLE entreprise (id_entreprise INTEGER AUTO_INCREMENT PRIMARY KEY, nom_entreprise VARCHAR(200) NOT NULL, adresse TEXT NULL, code_postal VARCHAR(10))")    
    
    def enregistrer_donnes(self,donnes):
        
        try:
            mon_cursor = self.cnx.cursor()
            #print(donnes)           

            #on cree la requete d'insertion
            sql_insert = ('INSERT INTO offer(titre, description,date_offre,salaire,localisation,id_entreprise, date_current, lien) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)')
            
            #on execute le methode pour inserer les donnes sur la BDD bd_scrapping)
            mon_cursor.executemany(sql_insert, donnes) #execute le curseur avec la methode executemany transmit la requete
            
            self.cnx.commit() #valide la transaction
                
            print(mon_cursor.rowcount, "record inserted.\n")           


        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err))

    def effacer_tous_annonces(self):
        
        try:
            mon_cursor = self.cnx.cursor()

            sql = "DELETE FROM offer"
            mon_cursor.execute(sql)

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err))


    def afficher_donnes(self):

        try:
            mon_cursor = self.cnx.cursor()

            mon_cursor.execute('SELECT * FROM offer')
            res = mon_cursor.fetchall()
            
            self.liste_donnes_offer=[]
            for line in res:
                #print(line)
                self.liste_donnes_offer.append(line)

            return self.liste_donnes_offer  

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err))
    
    def lastAnnonces(self):
        #il faudra verifier avec le dernier annonce en BDD si il y a eu des nouveaux
        try:
            mon_cursor = self.cnx.cursor()
            annonces_non_send=[]

            mon_cursor.execute('SELECT * FROM offer WHERE ISNULL(date_send_email)')
            annonces_non_send = mon_cursor.fetchall()
            
            """ self.liste_donnes_offer=[]
            for line in res:
                #print(line)
                self.liste_donnes_offer.append(line) """

            return annonces_non_send  

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err))

    def update_anonces_envoye(self, liste_annonces):
        try:
            mon_cursor = self.cnx.cursor()
            #print(liste_annonces)           

            for annonce in liste_annonces:
                #on cree la requete d'update
                #print(annonce)
                sql_update = f'UPDATE offer SET date_send_email = NOW() WHERE offer_id = {annonce[0]}'
                print(sql_update)

                #on execute le methode pour inserer les donnes sur la BDD bd_scrapping)
                mon_cursor.execute(sql_update) #execute le curseur avec la methode executemany transmit la requete
                print(mon_cursor.rowcount, "record updated.\n") 

            self.cnx.commit() #valide la transaction
                
                      
            print('Actualisation des données avec la date d envoie des annonces, END')
            return True

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err))

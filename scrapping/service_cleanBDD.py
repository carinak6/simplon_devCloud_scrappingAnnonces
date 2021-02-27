import requests
#import pprint

import datetime
import mysql.connector

from functions_db import *


class CleanBdd:
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

    def clean_bdd_etapeUn_href(self):
        print("Entra clean_bdd_etapeUn_href ")
        try:
            
            mon_cursor = self.cnx.cursor()            
            
            requete="""SELECT lien, COUNT(*) FROM offer GROUP BY lien HAVING COUNT(*)>1"""
            #print(requete)

            mon_cursor.execute(requete)
            
            res = mon_cursor.fetchall()

            print('type de reponse ',type(res),' cuantos ==> ', len(res))
            liste_lien_effacer=[]
            for num, annonce in enumerate(res):
                print('num ==>', num, ' annonce ', annonce, ' \n')                
                liste_lien_effacer.append(annonce[0])

                
            #liste des liens à effacer
            print(liste_lien_effacer)
            
            return liste_lien_effacer

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err)) 
    
    """ def clean_bdd_etapeUn_href(self):
        try:

            offres_bdd = ConnectionBDD()
            liste_offre = offres_bdd.afficher_donnes()
            self.liste_id_offer_effacer=[]

            mon_cursor = self.cnx.cursor()
            
            for line in liste_offre:
                liste_id_offer_effacer=[]
                #print('annonce:==> ',line)

                requete=SELECT offer_id FROM offer WHERE lien = %s ajouter apres les 3"
                #print(requete)

                mon_cursor.execute(requete, (line[8],))
                
                res = mon_cursor.fetchall()

                for num, annonce in enumerate(res):
                    #print('num ==>', num, ' annonce ', annonce, ' \n')
                    if num !=0: #on laisse le premier annonce
                        liste_id_offer_effacer.append(annonce[0])

                
                #continuer requete pour effacer les lignes trouvé en double
            print(liste_id_offer_effacer)
            
            return self.clear_annonces(liste_id_offer_effacer)

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err)) """
    

    def clear_annonces(self, liste_a):
        print("Entra clear_annonces ")
        print('liste des annonces à effacer ',liste_a)
        #delete_records = tuple(liste_a)
        #print('liste des annonces à effacer delete_records ',delete_records)

        try:
            print('clear_annonces')
            mon_cursor = self.cnx.cursor()

            for annonce in liste_a:
                print(annonce)
                sql = 'DELETE FROM offer WHERE offer_id = '+str(annonce)
                mon_cursor.execute(sql)
 
            # sql = """DELETE FROM offer WHERE offer_id = (%s)"""
            # mon_cursor.executemany(sql,liste_a)

            # sql = "delete from offer where offer_id in (%s)" % ','.join(['?'] * len(liste_a))
            # mon_cursor.execute(sql,liste_a)

            self.cnx.commit()
            print('number of rows deleted', mon_cursor.rowcount)
            return True

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err))
            return False
        """ finally:
            if self.cnx.is_connected():
                self.cnx.cursor.close()
                self.cnx.close()
                print("MySQL connection is closed") """
    
    def find_id_link(self, liste_clean):        
        try:
            print("Entra find_id_link \n")
            mon_cursor = self.cnx.cursor()
            list_annonces=[]

            for link in liste_clean: 
                print(link)
                requete= f"SELECT offer_id FROM offer WHERE lien = '{link}'"
                print(requete)    
                mon_cursor.execute(requete)            

                #print('results ==> ',results)
                
                res = mon_cursor.fetchall()

                print('type de reponse ',type(res), ' cuantos ==> ', len(res))
                
                for num, annonce in enumerate(res):
                    print('num ==>', num, ' annonce ', annonce, ' \n')
                    if num !=0: #on laisse le premier annonce
                        list_annonces.append(annonce[0])

                
            #liste des liens à effacer
            print(list_annonces)            
            
            return list_annonces

        except mysql.connector.Error as err:
            print("Something went wrong, un erreur se produit : {}".format(err)) 
    
    def clean_bdd(self):
        print("Entra clean_bdd")
        list_clearlien= self.clean_bdd_etapeUn_href()
        list_annonces_clean = self.find_id_link(list_clearlien)
        resp=self.clear_annonces(list_annonces_clean)
        return "BDD clean / netoyer / limpia ?" if resp else "No paso nada!!!"
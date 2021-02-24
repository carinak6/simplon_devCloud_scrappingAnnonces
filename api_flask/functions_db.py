import mysql.connector
import json

class conn_bd:
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
            

    def cherche_ville(self,ville):
        #sql_insert = ('INSERT INTO offer(titre, description,date_offre,salaire,localisation,id_entreprise, date_current) VALUES (%s,%s,%s,%s,%s,%s,%s)')
        
        try:       

            var_cursor = self.cnx.cursor()
            #self.requete='SELECT * FROM offer'
            self.requete=f'SELECT * FROM offer WHERE localisation LIKE "%{ville}%"; '

            var_cursor.execute(self.requete)
            res = var_cursor.fetchall()
            """ print('type de reponse res ', type(res))#<class 'list'>
            print('la reponse est: ', res) """
            reponse={}#[]

            if len(res) == 0:
                #conn.commit()
                #reponse = json.dumps({'erreur':'pas des lignes !!!'})
                reponse = {'erreur':'pas des lignes !!!'}
            else:
                for i, line in enumerate(res):
                    #je cree le dictionnaire
                    reponse[i+1]={
                        'id': line[0],                    
                        'titre' : line[1],
                        'description': line[2],
                        'date_offre': line[3],
                        'salaire': line[4],
                        'localisation' : line[5] ,
                        'date_creation': line[7],
                        'lien': line[8],      
                    }
        
            return reponse

        except Exception as err:
            # afficher la requête et le message d'erreur système :
            print ("Requête SQL incorrecte :\n%s\nErreur détectée :\n%s"\
                % (self.requete, err))
            return 0
        else:
            return 1  

    def cherche_cp(self, cp):

        #self.requete=f'SELECT * FROM offer WHERE localisation LIKE "%{cp}%"; '
        try:
            var_cursor = self.cnx.cursor()
            
            self.requete=f'SELECT * FROM offer WHERE localisation LIKE "%{cp}%"; '

            var_cursor.execute(self.requete)
            res = var_cursor.fetchall()
            """ print('type de reponse res ', type(res))#<class 'list'>
            print('la reponse est: ', res) """
            reponse={}

            if len(res) == 0:
                self.cnx.commit()
                #reponse = json.dumps({'erreur':'pas des lignes !!!'})
                reponse = {'erreur':'pas des annonces !!!'}
            else:
                for i, line in enumerate(res):
                    print('type description ==>',type(line[2]))
                    #descrip = line[2].encode('iso8859-1').decode('utf8')#'latin-1' codec can't encode character '\u2019' in position 646: ordinal not in range(256)
                    #descrip=descrip.decode('unicode_escape').encode('iso8859-1').decode('utf8')
                    
                    #descrip = descrip.decode("utf-8").encode("windows-1252").decode("utf-8")
                    #descrip = line[2].encode("windows-1252").decode("utf-8")
                    #descrip =str(line[2], 'utf-8')

                    #je cree le dictionnaire
                    reponse[i+1]={
                        'id': line[0],                    
                        'titre' : line[1],
                        'description': line[2],
                        'date_offre': line[3],
                        'salaire': line[4],
                        'localisation' : line[5] ,
                        'date_creation': line[7], 
                        'lien': line[8],      
                    }
        
            return reponse

        except Exception as err:
            # afficher la requête et le message d'erreur système :
            print ("Requête SQL incorrecte :\n%s\nErreur détectée :\n%s"\
                % (self.requete, err))
            return 0
        else:
            return 1  

        


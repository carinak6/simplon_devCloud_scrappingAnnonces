import logging
import requests
import pprint
from bs4 import BeautifulSoup
import datetime
import unicodedata
import lxml.html

import mysql.connector

class Indeed:
    def __init__(self):
        logging.info('on initialise la classe indeed - Start')
        
        #self.url= 'https://fr.indeed.com/emplois?q=alternance+cloud&l=%C3%8Ele-de-France'
        self.url= 'https://fr.indeed.com/emplois?q=alternance+d%C3%A9veloppeur&l=%C3%8Ele-de-France'
        
        #original
        #self.url='https://fr.indeed.com/emplois?q=alternance+developpeur+cloud&l=%C3%8Ele-de-France'
        
        logging.info('on recupere le contenur de l url passé comme parametre du methode get requests url :'+self.url)
        self.page = requests.get(self.url)
        reponse_get =self.page#200 
        print(reponse_get)
        logging.info('Connexion reussi ? reponse '+str(reponse_get))

        logging.info('on utilise la librerie BeautifulSoup pour recuperer le contenu de la page')        
        self.soup = BeautifulSoup(self.page.content, 'html.parser') 
        #un analyseur HTML; c est le parametre original; 'lxml') un analyseur XML

        logging.info('on prends la div avec tous les annonces, l\'id est resultsCol') 
        # taking the div with all results
        self.results = self.soup.find(id='resultsCol')
        #print('type de results ==>',type(self.results)) #<class 'bs4.element.Tag'>

        #je le genere ici parce que j'ai besoin dans 2 autres methodes
        logging.info('on recupere le lien de la balise a avec les classes jobtitle et turnstileLink') 
        self.a_links = self.results.findAll("a", {"class": ['jobtitle', 'turnstileLink']})
        #print('self.a_links ==>',self.a_links)
        #print('type self.a_links ==>',type(self.a_links)) #<class 'bs4.element.ResultSet'>

        logging.info('on initialise la classe indeed - End')

    def recuperationLien(self):
        logging.info('Execution de la methode recuperationLien(indeed) - Start')

        #self.liens = self.a_links
        self.href_list=[]

        for link in self.a_links:
            href= link.get('href').strip()
            title = link.get('title')
            #print(href, link)
            if title != None:
                href = "https://indeed.fr"+href
                self.href_list.append(href)

        #print(href_list)
        logging.info('Liste des liens trouvés : '+ str(self.href_list))

        logging.info('Execution de la methode recuperationLien(indeed) - End')

        return self.href_list


    def recuperationTitle(self):
        logging.info('Execution de la methode recuperationTitle(indeed) - Start')

        #self.title = self.a_links
        title_list = []

        for link in self.a_links:
            title = link.get('title')
            if title != None: #je verifie sinon il y a des erreurs
                title_list.append(title)
            """ print(f"Job title is: {title}")
            print('_______________') """
        
        #print(title_list)

        logging.info('Liste de title trouvé ' + str(title_list))

        logging.info('Execution de la methode recuperationTitle(indeed) - End')

        return title_list


    #TODO continuer avec les functions et faire avec les classes apres, ajouter les logs et testes unitaires

    

    """ def find_salary(self): #Maria  ça marche pas pour moi, il retourne la meme quantite des salaires 3
        salary_list = []
        logging.info("getting salaries: start")
        try:
            salaries = self.results.find_all('span', class_ = "salaryText")
            for salary in salaries:
                salary = salary.text.strip()#suprime les spaces les espaces du début et de la fin de chaque bit de texte:
                salary = unicodedata.normalize("NFKD", salary)

                # https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
                
                salary_list.append(salary)
        except:
            #salaries = " "
            salary_list.append('RIEN')
        
        print(salary_list)
        logging.info("getting salaries: end")
        return salary_list """
        

    def recupererLocalisations(self):
        logging.info('Execution de la methode recupererLocalisations(indeed) - Start')

        logging.info('On cherche dans le self.results un div,span ==> class : location ')
        self.locations_resultat = self.results.find_all(['div', 'span'], {'class' : 'location'})
        
        location_list=[]    
        for location in self.locations_resultat:
            location_list.append(location.text)
            """ print(location.text)
            print('_______________') """

        logging.info('liste de location des annonces : '+str(location_list))

        logging.info('Execution de la methode recupererLocalisations(indeed) - End')
        return location_list

    
    def recupereDate(self):
        logging.info('Execution de la methode recupereDate(indeed) - Start')
        
        logging.info('on recupere les date ')

        self.date_result = self.results.findAll('span', {'class': 'date'})
        date_list=[]
        # finds when annonce posted   
        for date in self.date_result:        
            date_list.append(date.text)
            """ print('\ndate.text ==>',date.text)
            print('********') """

        logging.info('liste des date pour les annonces : '+str(date_list))

        logging.info('Execution de la methode recupereDate(indeed) - End')
        return date_list

    def recupereSalaire(self, donnes):
        logging.info('Execution de la methode recupereSalaire(indeed) - Start')

        #traitement de text pour avoir le salaire avec les donnes envoye
        position= donnes.find('Salaire')#il commence à zero
        #print('position ==> ',position)

        a_partir=donnes[position:] #texte apres salaire
        position_salaire= a_partir.find(':')

        recupererSalaire=a_partir[(position_salaire + 1):]
        #on cherche les mots par an, par mois et €, pour avoir le montant du salaire propose
        position_an= recupererSalaire.find('par an')
        position_mois= recupererSalaire.find('par mois')
        position_euro= recupererSalaire.find('€')

        #check if we found "par an" / verifie si on a trouvé "par an"
        if position_an != -1:
            salaire=recupererSalaire[:position_an]+"par an"
        elif position_mois != -1:
            salaire=recupererSalaire[:position_mois] +"par mois"
        elif position_euro != -1:
            salaire=recupererSalaire[:position_euro]
        else:
            salaire='Il n\'y a pas'

        """ print('position_mois ==> ',position_mois)
        print('position_an ==> ',position_an)
        print('position_retour ==> ',position_euro)        
        print('a partir ==>',a_partir)
        print('salaire returné : ',salaire,'\n') """

        logging.info('salaire retourné : '+ salaire)

        logging.info('Execution de la methode recupereSalaire(indeed) - End')
        return salaire

    def recupererDescription(self): 
        logging.info('Execution de la methode recupererDescription(indeed) - Start')

        logging.info('on recuperera la liste des salaires et la liste des description')

        #declarer un attribute avec le salaire
        self.liste_salaire=[]
        description_list=[] 
        
        logging.info('on recuperera la liste des description en allant sur chaque lien des annonces et aussi les salaires')
        for lien in self.href_list:

            #comment c est effimere je cree des variables locales
            page = requests.get(lien) #je recupere la page de l'offre
            #print(page)#200 OK       
            soup = BeautifulSoup(page.content, 'html.parser') #''lxml')
            
            # taking the div with all results jobDescriptionText
            results = soup.find(id='jobDescriptionText') #soup.select('div>div#vjs-desc')
            #jobDescriptionText contenu 'html.parser' <div class="jobsearch-jobDescriptionText" id="jobDescriptionText"><div><div><h2 class="jobSectionHeader"><b>A propos de SQLI
            #print('jobDescriptionText contenu ',results, ' type: ',type(results))
            
            description=results.text
            #on verifie si le mot salaire c est trouve dans la decription
            if 'Salaire' in description: 
                self.liste_salaire.append(self.recupereSalaire(description))
            else:
                self.liste_salaire.append('Salaire inconnu')

            #print("results ==> ",results.text)
            # je recupere le text de chaque detail de l'offre 
            description_list.append(description)


        #print('*************************** \n len==>',len(description_list), '\nresultats description==>', description_list)
        logging.info('liste des salaires '+str(self.liste_salaire) +' et la liste des description :'+str(description_list))
        
        logging.info('Execution de la methode recupererDescription(indeed) - End')

        return description_list
    
    def generateur_tuples(self):
        logging.info('Execution de la methode generateur_tuples(indeed) - Start')

        logging.info('J\'execute les differentes methodes de la classe pour creer les tuples de chaque annonce')

        #TODO je pourrai pas faire de retur et utiliser les variables self
        resultat_href = self.recuperationLien() 
        resultat_titre = self.recuperationTitle()
        resultat_localisation = self.recupererLocalisations()
        resultat_date = self.recupereDate()
        resultat_description = self.recupererDescription()
        resultat_salaire = self.liste_salaire #comment des fois c est indiqué ou non, je le define dans recupererDescription()

        """ test_salaire =self.find_salary()
        print(test_salaire) """
        #print('href_list==> ',resultat_href,' \n title_list==>', resultat_titre,'\nlocation_list ==>',resultat_localisation,' \ndate_list ==> ',resultat_date)
        print('len resultat_href ==>', len(resultat_href),'\nlen(resultat_titre)==>',len(resultat_titre) ,'\nlen resultat_date ==>', len(resultat_date),'\nlen resultat_localisation==>', len(resultat_localisation))

        tailleLists = len(resultat_localisation) #len(resultat_titre) out of range
        
        listResultat = []
        date_actuel = datetime.date.today()#pour recuperer la date que j'ai lancé le script
        #print(date_actuel) #2021-02-20, en BDD egal

        #********* generation des touples ***********
        for x in range(tailleLists): 
            listResultat.append((resultat_titre[x],resultat_description[x], resultat_date[x],resultat_salaire[x],resultat_localisation[x],1, date_actuel, resultat_href[x]))

        logging.info('La liste des tuples : '+str(listResultat))

        logging.info('Execution de la methode generateur_tuples(indeed) - End')                
        return listResultat
    
    
import requests
import pprint
from bs4 import BeautifulSoup
import datetime

import mysql.connector

#https://fr.indeed.com/emplois?q=developpeur+web&l=Paris+%2875%29
#https://fr.indeed.com/Paris-(75)-Emplois-developpeur-web
URL = 'https://fr.indeed.com/emplois?q=alternance+d%C3%A9veloppeur&l=%C3%8Ele-de-France'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser') #"""'lxml')"""

# taking the div with all results
results = soup.find(id='resultsCol')
#print(results)
#a_links = results.find_all(name='a',attrs={"class":"jobtitle turnstileLink "})
a_links = results.findAll("a", {"class": ['jobtitle', 'turnstileLink']})


def recuperationLien(donnes):
    href_list=[]

    for link in donnes:
        href= link.get('href')
        #print(href, link)
        href = "https://indeed.fr"+href
        href_list.append(href)
    
    return href_list

def recuperationTitle(donnes):
    title_list = []

    for link in donnes:
        title = link.get('title')
        title_list.append(title)
        """ print(f"Job title is: {title}")
        print('_______________') """
    return title_list


#continuer avec les functions et faire avec les classes apres, ajouter les logs et testes unitaires

locations_resultat = results.find_all(['div', 'span'], {'class' : 'location'})
def recupererLocalisations(donnes):
    location_list=[]    
    for location in donnes:
        location_list.append(location.text)
        """ print(location.text)
        print('_______________') """
    return location_list

date_result = results.findAll('span', {'class': 'date'})
def recupereDate(donnes):
    date_list=[]
    # finds when annonce posted   
    for date in donnes:        
        date_list.append(date.text)
        """ print('\ndate.text ==>',date.text)
        print('********') """
    return date_list

resultat_href = recuperationLien(a_links) 
resultat_titre = recuperationTitle(a_links)
resultat_localisation = recupererLocalisations(locations_resultat)
resultat_date = recupereDate(date_result)

#print('href_list==> ',resultat_href,' \n title_list==>', resultat_titre,'\nlocation_list ==>',resultat_localisation,' \ndate_list ==> ',resultat_date)
#print('date_list ==> ',resultat_date)

try:
    cnx = mysql.connector.connect(user='root', password='sha', host='my_mysql', database='bd_scrapping', use_unicode=True, charset='utf8')
    print('connexion reussi')

    mycursor = cnx.cursor()

    #mycursor.execute("CREATE TABLE offer (offer_id INTEGER AUTO_INCREMENT PRIMARY KEY, titre VARCHAR(200) NOT NULL, description TEXT NOT NULL, date_offre TEXT, salaire INTEGER, localisation VARCHAR(200), id_entreprise INT)")
    tailleLists = len(resultat_localisation) #len(resultat_titre) out of range
    #probleme avec les indices le len de chaque resultats est different
    #print('len resultat_href', len(resultat_href),'\nlen(resultat_titre)',len(resultat_titre) ,'\nlen resultat_date', len(resultat_date),'\nlen resultat_localisation', len(resultat_localisation) ,'\ntailleList ==> ', tailleLists,'\n')
    listResultat = []

    #generation des touples
    #dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
    """ dt.strftime("%A, %d. %B %Y %I:%M%p")
    datetime.now()  """  
    #date_actuel = datetime.strftime(datetime.now(),"%d/%m/%y %H:%M:%S")
    date_actuel = datetime.date.today()
    print(date_actuel) #2021-02-20, en BDD egal
    for x in range(tailleLists): 
        if resultat_titre[x] != None: #je verifie sinon il y a des erreurs
            listResultat.append((resultat_titre[x],"pas encore recupere", resultat_date[x],1000,resultat_localisation[x],1, date_actuel))
        
    
    #print('\nlistResultat : ', listResultat, '\ntype ',type(listResultat))#liste des touples
    
    """ sql = "DELETE FROM offer"
    mycursor.execute(sql) """

    #on cree la requete d'insertion
    sql_insert = ('INSERT INTO offer(titre, description,date_offre,salaire,localisation,id_entreprise, date_current) VALUES (%s,%s,%s,%s,%s,%s,%s)')
    
    #on execute le methode pour inserer les donnes sur la BDD bd_scrapping)
    mycursor.executemany(sql_insert, listResultat) #execute le curseur avec la methode executemany transmit la requete
    
    cnx.commit() #valide la transaction
        
    print(mycursor.rowcount, "record inserted.")

    mycursor.execute('SELECT * FROM offer')
    res = mycursor.fetchall()

    for line in res:
        print(line)
   

except mysql.connector.Error as err:
    print("Something went wrong, un erreur se produit : {}".format(err))


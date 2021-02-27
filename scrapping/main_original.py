import requests
import pprint
from bs4 import BeautifulSoup

import mysql.connector



URL = 'https://fr.indeed.com/emplois?q=developpeur+web&l=Paris+%2875%29'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser') #"""'lxml')"""

# taking the div with all results
results = soup.find(id='resultsCol')
#print(results)
#a_links = results.find_all(name='a',attrs={"class":"jobtitle turnstileLink "})

a_links = results.findAll("a", {"class": ['jobtitle', 'turnstileLink']})
#a_links = results.find_all('a', class_ = 'jobtitle turnstileLink ')

#print(f"Printing links: {a_links}")


href_list = []
title_list = []
location_list=[]
date_list=[]



for link in a_links:
    href= link.get('href')
    #print(href, link)
    href = "https://indeed.fr"+href
    href_list.append(href)


    title = link.get('title')
    title_list.append(title)
    """ print(f"Job title is: {title}")
    print('_______________') """

locations = results.find_all(['div', 'span'], {'class' : 'location'})
for location in locations:
    location_list.append(location.text)
    """ print(location.text)
    print('_______________') """

# finds when annonce posted
date_result = results.findAll('span', {'class': 'date'})
for date in date_result:
    date_list.append(date.text)
    """ print(date.text)
    print('********') """

#print('href_list==> ',href_list,' \n title_list==>', title_list,'\nlocation_list ==>',location_list,' \ndate_list ==> ',date_list)

try:
    cnx = mysql.connector.connect(user='root', password='sha', host='my_mysql', database='bd_scrapping')
    print('connexion reussi')

    mycursor = cnx.cursor()

    #mycursor.execute("CREATE TABLE offer (offer_id INTEGER AUTO_INCREMENT PRIMARY KEY, titre VARCHAR(200) NOT NULL, description TEXT NOT NULL, date_offre TEXT, salaire INTEGER, localisation VARCHAR(200), id_entreprise INT)")
    tailleLists = len(href_list) - 1
    listResultat = []

    #generation des touples
    for x in range(tailleLists): 
        if title_list[x] != None:
            listResultat.append((title_list[x],"pas encore recupere", date_list[x],1000,location_list[x],1))
        
    
    #print('listResultat : ', listResultat, '\ntype ',type(listResultat))#liste des touples
    
    sql_insert = ('INSERT INTO offer(titre, description,date_offre,salaire,localisation,id_entreprise) VALUES (%s,%s,%s,%s,%s,%s)')
    
    mycursor.executemany(sql_insert, listResultat) #execute le curseur avec la methode executemany transmit la requete
    
    cnx.commit() #valide la transaction
        
    print(mycursor.rowcount, "record inserted.")

    mycursor.execute('SELECT * FROM offer')
    res = mycursor.fetchall()

    for line in res:
        print(line)

   

except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))


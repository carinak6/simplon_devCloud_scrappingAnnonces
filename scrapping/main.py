import logging
import requests
import pprint

from send_email import *
from scrapping_indeed import *
from functions_db import *
from service_cleanBDD import *

logging.basicConfig(filename='logging_scrapping.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def main():    
    logging.info('instace la classe indeed')
    """ var_indeed = indeed() #creation de l'instance de la classe indeed

    logging.info('on execute les processus pour obtenir les informations sur le site indeed')
    var_tuples = var_indeed.generateur_tuples()
    #print(var_tuples)

    logging.info('on cree une instance de la classe conn_bd que realise la connexion avec la BDD')
    var_donnes= ConnectionBDD()

    logging.info('on cree une instance de la classe conn_bd que realise la connexion avec la BDD')
    var_donnes.enregistrer_donnes(var_tuples)
    donnes = var_donnes.afficher_donnes() """
    #print(donnes)

    clean_bdd = CleanBdd()
    print(clean_bdd.clean_bdd())

    """ var_email = GestionEmail()
    var_email.send_email('kassiscarina@gmail.com')
    print('fin message envoye') """

if __name__ == '__main__':
    logging.info('%s - logged in successfully', "Appel du main pour la script de scrapping")
    main()


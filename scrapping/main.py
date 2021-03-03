import logging

from send_email import *
from scrapping_indeed import *
from functions_db import *
from service_cleanBDD import *

logging.basicConfig(filename='logging_scrapping.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def main(): 
    logging.info('Beginning of the script')   
    logging.info('creation de l\'instance de la classe indeed')
    var_indeed = Indeed()

    logging.info('on execute les processus pour obtenir les informations sur le site indeed - Start')
    var_tuples = var_indeed.generateur_tuples()
    #print(var_tuples)
    logging.info('Les donnes trouvés on genere les suivant touples : '+str(var_tuples))
    logging.info('on execute les processus pour obtenir les informations sur le site indeed - End')

    logging.info('on cree une instance de la classe conn_bd que realise la connexion avec la BDD - Start')
    var_donnes= ConnectionBDD()

    logging.info('J\'execute la methode enregistrer_donnes qui prends les tuples generé avant - Start')
    var_donnes.enregistrer_donnes(var_tuples)
    logging.info('je recupere les donnes pour enregistre dans la BDD - Start')
    donnes = var_donnes.afficher_donnes()
    #print(donnes)
    logging.info('je recupere les donnes pour enregistre dans la BDD : '+ str(donnes) +' - End')
    logging.info('J\'execute la methode enregistrer_donnes qui prends les tuples generé avant - End')
    logging.info('On cree une instance de la classe conn_bd que realise la connexion avec la BDD - End')

    logging.info('On cree une instance de la classe CleanBdd que realise le netoyage de la BDD - Start')    
    clean_bdd = CleanBdd()
    reponse =clean_bdd.clean_bdd()
    print(reponse)
    logging.info('On cree une instance de la classe CleanBdd que realise le netoyage de la BDD - Fin : '+reponse) 
    
    logging.info('On cree une instance de la classe GestionEmail que realise l\'envoye de l\'email - Start') 
    var_email = GestionEmail()
    email_target='kassiscarina@gmail.com'
    var_email.send_email(email_target)
    print('fin message envoye')
    logging.info('On cree une instance de la classe GestionEmail que realise l\'envoye de l\'email - End : '+email_target) 
    
    logging.info('Fin du main') 

if __name__ == '__main__':
    logging.info('%s - logged in successfully', "Appel du main pour la script de scrapping")
    main()


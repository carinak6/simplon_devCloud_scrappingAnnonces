import smtplib, ssl #se connecter à notre serveur SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from functions_db import *

import unidecode
import codecs
import unicodedata

class GestionEmail():

    def __init__ (self):
        self.server = smtplib.SMTP()

        # on rentre les renseignements pris sur le site du fournisseur
        self.smtp_adress = 'smtp.gmail.com'
        self.smtp_port = 465

        # on rentre les informations sur notre adresse e-mail
        self.email_address = 'mariacardelli996@gmail.com'
        self.email_password = 'kary93800ARG'

        # on rentre les informations sur le destinataire
        self.email_receiver = 'kassiscarina@gmail.com'
        print(self.smtp_adress)

    def send_email_html(self,email_target):        
        self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
        print(self.smtp_adress)

        # on crée la connexion
        # server.set_debuglevel(1) # Décommenter pour activer le debug
        self.server.connect(self.smtp_adress)

        self.server.helo() #??
        sujet="Les derniers annonces pour alternance"
        

        #********************** pour creer le contenu html ***********
        var_bdd = ConnectionBDD()
        list_new_annonces = var_bdd.lastAnnonces()
        print(list_new_annonces)
        contenu_email= self.create_contenu(list_new_annonces)
        body = "This is an email with attachment sent from Python"
        #********************  **********************

        #msg = MIMEMultipart('alternative')
        msg = MIMEMultipart()
        msg['Subject'] = sujet
        msg['From'] = self.email_address
        msg['To'] = self.email_receiver

        #part = MIMEText(contenu_email, 'html')
        part =MIMEText(body, "plain")
        msg.attach(part)

        try:
            self.server.sendmail(self.email_address, self.email_receiver, msg.as_string())
            print('message envoye')
            var_bdd.update_anonces_envoye(list_new_annonces)

        except smtplib.SMTPException as e:
            print('ERROR ==>SMTPException :',e)

        """ with smtplib.SMTP_SSL(self.smtp_adress, self.smtp_port, context=context) as server:
            # connexion au compte
            server.login(self.email_address, self.email_password)
            # envoi du mail
            server.sendmail(self.email_address, self.email_receiver, 'Test d envoie d email, VAMOS!!!') """
        
    
    def create_contenu(self, last_annonces):

        txt_page= u"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                </head>
                <body>
                <div>
                        <p class ="titre" >HOLA</p>
                        <p class="lien"> <a href="" target="_blank"> lien à l'annonce</a> </p>        
                    </div>
                </body>
                </html>"""


        return txt_page

    def send_email(self,email_target):
        var_bdd = ConnectionBDD()
        list_new_annonces = var_bdd.lastAnnonces()

        if len(list_new_annonces) !=0:        
            self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
            # on crée la connexion
            context = ssl.create_default_context()
            #print(self.smtp_adress)           

            print('taille des nouveau annonces ',len(list_new_annonces))
            #print('les nouveaux annonces ',list_new_annonces)

            message=""
            if len(list_new_annonces) == 1:
                message =str(list_new_annonces[0][1]).encode('utf-8', errors='ignore')
                message +=str(" \n "+list_new_annonces[0][8]).encode('utf-8', errors='ignore') 
            else:
                for detaille_annon in list_new_annonces:
                    message +="Annonce : "+detaille_annon[1] +"\n suivre le lien : "+detaille_annon[8]+"\n\n"
                       
                message= str(message).encode('utf-8', errors='ignore')
            
            print(message)
            

            with smtplib.SMTP_SSL(self.smtp_adress, self.smtp_port, context=context) as server:
                # connexion au compte
                server.login(self.email_address, self.email_password)
                # envoi du mail
                server.sendmail(self.email_address, self.email_receiver, message)
            print('message envoye')

            print('actualiser les annonces avec la date d\'envoye par email')
            var_bdd.update_anonces_envoye(list_new_annonces) #je l activerai apres
            
            return True
        else:
            print('Pas des nouveaux annonces')
            return False



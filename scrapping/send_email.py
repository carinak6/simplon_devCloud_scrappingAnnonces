import smtplib, ssl #se connecter à notre serveur SMTP

class GestionEmail():

    def __init__ (self):
        # on rentre les renseignements pris sur le site du fournisseur
        self.smtp_adress = 'smtp.gmail.com'
        self.smtp_port = 465

        # on rentre les informations sur notre adresse e-mail
        self.email_adress = 'kassiscarina@gmail.com'
        self.email_password = 'sha*CD25141675'

        # on rentre les informations sur le destinataire
        self.email_receiver = 'kassiscarina@gmail.com'
        print(self.smtp_address)

    def send_email(self,email_target):        
        self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
        # on crée la connexion
        context = ssl.create_default_context()
        print(self.smtp_address)

        with smtplib.SMTP_SSL(self.smtp_address, self.smtp_port, context=context) as server:
            # connexion au compte
            server.login(self.email_adress, self.email_password)
            # envoi du mail
            server.sendmail(self.email_address, self.email_receiver, 'Test d envoie d email, VAMOS!!!')
        print('message envoye')
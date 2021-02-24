import logging
import mysql.connector
from flask import Flask, request, render_template, jsonify

from functions_db import *

app = Flask(__name__)
logging.basicConfig(filename='logging_flask.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

conn_funct = conn_bd() #creation de l instance de la class connexion

@app.route('/')
def hello():
    #app.logger.info('Returning my hello function')
    app.logger.info('%s logged in successfully', "HOLA entra à logger")
    """ handler.setLevel("INFO")
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(threadName)s :: %(message)s') """
    return 'Hello, World!'

@app.route('/search/city/<string:ville>', methods=['GET'])
def search_city(ville):
    #return cherche_ville(ville)
    reponse = conn_funct.cherche_ville(ville)
    #reponse =cherche_ville(ville)

    print('le return de chercher_ville est ',reponse)
    #, 5: {'id': 135, 'titre': 'Développeur Intégrateur Web H/F', 'description': 'pas encore recupere', 'date_offre': 'il y a 3 jours', 'salaire': 1000, 'localisation': 'Paris (75)'},
    return jsonify(reponse)


    #Cette fonction encapsule: func: `dumps` pour ajouter quelques améliorations qui font la vie plus facile.
    #return jsonify(cherche_ville(ville))

    #return 'ma route /test'

    #type_req = request.args['type_offre']  #pour capter le requete GET avec ?type_offre=indeed
    #type_req = request.args.get("type_offre") 
    #return f'Le login entré est {type_req}'#""" """.format(type_offre)

    #return request.args.get("page_number") #http://localhost:4005/test?page_number=200 ==>return 200

@app.route('/search/cp/<int:cp>') #route requete GET avec endpoint avec le point: ?
def paramget(cp):
    """ pour definir des valeurs par defaut dans les url
    page = request.args.get('page', default = 1, type = int)
    filtro = request.args.get('filter', default = '*', type = str) """
   
    #return f'Le login entré est {type_offre}'#""" """.format(type_offre)
    #return f'Le login entré est {cp}'#""" """.format(type_offre)
    return jsonify(conn_funct.cherche_cp(cp))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 3005, debug=True)

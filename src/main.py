"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for, make_response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Tournament, TournamentMatch, Inscription

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/register/<username>', methods=['POST'])
def handle_register_user(username):

    headers = {
        "Content-Type": "application/json"
    }
    #Chequeando si el usuario 
    
    requesting_user = User.query.filter_by(username=username).first()
    if requesting_user:
        username_id = requesting_user.id
    else : 
        username_id = None 

           
    if request.method == 'POST':
        
        print("HELLO Creando Usuario POST")
                
        if username_id:
            
            response_body = {
                "status": "HTTP_400_BAD_REQUEST. Usuario ya existe..."
            }
            status_code = 400
        
        else:
            print("Creando usuario")
            user_pack = request.json
            new_user = User(username,user_pack["email"],user_pack["name"],user_pack["last_name"],
                user_pack["password"],user_pack["date_of_birth"],
                user_pack["country"],user_pack["state"],user_pack["city"],user_pack["description"])
            db.session.add(new_user)
            db.session.commit()
            response_body = {
                "status": "Ok"
            }
            status_code = 200
      
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

@app.route('/login/<username>', methods=['POST'])
def handle_log_in_user(username):

    headers = {
        "Content-Type": "application/json"
    }
    #Chequeando si el usuario existe
    user_pack = request.json
    
    if username.find("@") == -1:
       
        requesting_user = User.query.filter_by(username=username,password=user_pack["password"]).first()
        
        if requesting_user:
            username_id = requesting_user.id
        else : 
            username_id = None 

    else:
           
        requesting_user = User.query.filter_by(email=username,password=user_pack["password"]).first()
        if requesting_user:
            username_id = requesting_user.id
        else : 
            username_id = None

    if request.method == 'POST':
        
        print("HELLO Logeando Usuario POST")
                
        if username_id:

            user = User.get_by_id(username_id)
            user_diccionary = json.dumps(user.serialize())
            
            response_body = {
                "status": "OK",
                "user": user_diccionary
            }
            status_code = 200
        
        else:
            response_body = {
                "status": "400_CREDENCIALES_NO_CONCUERDAN"
            }
            status_code = 400
      
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

@app.route('/user/<user_id>/tournaments/', methods=['GET','POST'])
@app.route('/user/<user_id>/tournaments/<tournament_id>', methods=['GET','POST','PUT','DELETE'])
def handle_tournament(user_id,tournament_id = 0):

    headers = {
        "Content-Type": "application/json"
    }
    #Chequeando si el usuario existe
    
    if request.method == 'GET':
        
        print("HELLO Tournament GET")
        all_tournament = Tournament.query.all()
        all_tournament_serialize = []
        for tournament in all_tournament:
            all_tournament_serialize.append(tournament.serialize())
        all_tournament_serialize_json = json.dumps(all_tournament_serialize)

        response_body = {
                "status": "OK",
                "tournaments": all_tournament_serialize_json
            }
        status_code = 200
    
    if request.method == 'POST':

        print("HELLO Tournament POST")
        tournament_pack = request.json        
        if tournament_pack["action"] == "create":
            print("Creando torneo")
            new_tournament = Tournament(tournament_pack["tournament_name"],tournament_pack["password"],tournament_pack["game_title"],tournament_pack["game_plataform"],tournament_pack["deadline"], tournament_pack["start_date"], tournament_pack["country"],tournament_pack["state"], tournament_pack["city"],tournament_pack["participants"],tournament_pack["entrance_fee"],tournament_pack["prize"],tournament_pack["kind"],user_id)
            db.session.add(new_tournament)
            db.session.commit()
            response_body = {
                "status": "OK"
            }
            status_code = 200
        
        elif tournament_pack["action"] == "take part":
            print("Inscribiendo en torneo")
            inscriptions = Inscription.query.filter_by(tournament_id=tournament_id).all()
            tournament = Tournament.query.filter_by(id=tournament_id).first()
            limit_inscriptions = tournament.participants
            if len(inscriptions) < limit_inscriptions:
                new_inscription = Inscription(tournament_id,user_id,tournament_pack["status"],tournament_pack["date_inscription"])
                db.session.add(new_inscription)
                db.session.commit()
                response_body = {
                    "status": "OK"
                }
                status_code = 200
            else:
                response_body = {
                    "status": "400_BAD_REQUEST"
                }
                status_code = 400
            
        else:
            response_body = {
                "status": "400_ACCION_NO_REGISTRADA"
            }
            status_code = 400
      
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )


@app.route('/tournaments/<tournament_id>/match/', methods=['GET','POST','PUT','DELETE'])
@app.route('/tournaments/<tournament_id>/match/<match_id>', methods=['GET','POST','PUT','DELETE'])
def handle_match_tournament(tournament_id,match_id = 0):
    
    headers = {
        "Content-Type": "application/json"
    }

    if match_id == 0:
        if request.method == 'POST':
            registered_users = Inscription.query.filter_by(tournament_id=tournament_id).all()
            requesting_tournament = Tournament.query.filter_by(id=tournament_id).one_or_none()
            if requesting_tournament:
                
                did_create_matches = requesting_tournament.create_matches_mode_league(registered_users)
                
                if did_create_matches:
                    response_body = {
                            "status": "OK"
                        }
                    status_code = 200
                else:
                    response_body = {
                            "status": "400_BAD_REQUEST_LOS PARTIDOS YA ESTAN CREADOS"
                        }
                    status_code = 400
            
            else:
                response_body = {
                        "status": "400_BAD_REQUEST"
                    }
                status_code = 400
    
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

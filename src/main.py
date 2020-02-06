"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
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
    print(username)
    requesting_user = User.query.filter_by(username=username).all()
    if len(requesting_user) > 0:
        username_id = requesting_user[0].id
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
            new_user = User(user_pack["username"],user_pack["email"],user_pack["password"],user_pack["date_of_birth"],
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
       
        requesting_user = User.query.filter_by(username=username,password=user_pack[password]).all()
        if len(requesting_user) > 0:
            username_id = requesting_user[0].id
        else : 
            username_id = None 

    else:
           
        requesting_user = User.query.filter_by(email=username,password=user_pack[password]).all()
        if len(requesting_user) > 0:
            username_id = requesting_user[0].id
        else : 
            username_id = None

    if request.method == 'POST':
        
        print("HELLO Logeando Usuario POST")
                
        if username_id:
                        
            response_body = {
                "status": "OK"
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



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

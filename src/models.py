from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): #Usuario
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    date_of_birth = db.Column(db.Date,nullable=False)
    country = db.Column(db.String(120))
    state = db.Column(db.String(120))
    city = db.Column(db.String(120))
    description = db.Column(db.String(1200))
    tournament = db.relationship('Tournament', backref='user', lazy=True)
    inscription = db.relationship('Inscription', backref='user', lazy=True)

    def __init__(self,username,email,password,date_of_birth,country,state,city,description):
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.country = country
        self.state = state
        self.city = city
        self.description = description

    def __repr__(self):
        return f"User username: {self.username},e-mail: {self.email},date of birt: {self.date_of_birth},country: {self.country},state: {self.state},city: {self.city}"
            

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "country":self.country,
            "state":self.state,
            "city":self.city,
            "description":self.description
        }


class Tournament(db.Model): #Torneo
    id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120))
    game_title = db.Column(db.String(80), nullable=False)
    game_plataform = db.Column(db.String(80), nullable=False)
    deadline = db.Column(db.Date,nullable=False)
    start_date = db.Column(db.Date,nullable=False)
    country = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    city = db.Column(db.String(120),nullable=False)
    participants = db.Column(db.Integer,nullable=False)
    entrance_fee = db.Column(db.String(120),nullable=False)
    prize = db.Column(db.String(120),nullable=False)
    kind = db.Column(db.String(120),nullable=False)
    organizator_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    inscriptions = db.relationship('Inscription', backref='tournament', lazy=True) 
    matches = db.relationship('TournamentMatch', backref='tournament', lazy=True)

    def __init__(self,tournament_name,password,game_title,game_plataform,deadline,start_date,
        country,state,city,participants,entrance_fee,prize,kind,organizator_id):
        self.tournament_name = tournament_name
        self.password = password
        self.game_title = game_title
        self.game_plataform = game_plataform
        self.deadline = deadline
        self.start_date = start_date
        self.country = country
        self.state = state
        self.city = city
        self.participants = participants
        self.entrance_fee = entrance_fee
        self.prize = prize
        self.kind = kind
        self.organizator_id = organizator_id

    def __repr__(self):
        return f"Tournament tournament_name: {self.tournament_name},game_title: {self.game_title},game_plataform: {game.game_plataform},deadline: {self.deadline},start_date: {self.start_date},country: {self.country},state: {self.state},city: {self.city},participants: {self.participants},entrance fee: {self.entrance_fee},prize: {self.prize},kind: {self.prize}" 

    def serialize(self):
        return {
            "tournament_name" : self.tournament_name,
            "password" : self.password,
            "game_title" : self.game_title,
            "game_plataform" : self.game_plataform,
            "deadline" : self.deadline,
            "start_date" : self.start_date,
            "country" : self.country,
            "state" : self.state,
            "city" : self.city,
            "participants" : self.participants,
            "entrance_fee" : self.entrance_fee,
            "prize" : self.prize,
            "kind" : self.kind
        }

class Inscription(db.Model): #Inscripciones
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'),
        nullable=False)
    competitor_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    status = db.Column(db.String(20),nullable=False)
    date_inscription = db.Column(db.Date,nullable=False)
    
    def __init__(self,tournament_id,competitor_id,status,date_inscription):
        self.tournament_id = tournament_id
        self.competitor_id = competitor_id
        self.status = status
        self.date_inscription = date_inscription
    
    def __repr__(self):
        return '<Inscription %r>' % self.status

    def serialize(self):
        return {
            #status
            #nombredeusario a inscriibir
            #nombre de torneoa inscribir 
        }

class TournamentMatch(db.Model): #Encuentros
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'),
        nullable=False)
    competitor_one_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    competitor_two_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), nullable=False)
    match_result_one = db.Column(db.Integer, nullable=False)
    match_result_two = db.Column(db.Integer, nullable=False)
    # won_one = db.Column(db.Boolean,nullable=False)
    # won_two = db.Column(db.Boolean,nullable=False)
    round = db.Column(db.Integer,nullable=False)
    

    def __repr__(self):
        return '<Match %r>' % self.round

    def serialize(self):
        return {
            "hello" : "chao"
        }


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): #Usuario
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120),nullable=False)
    date_of_birth = db.Column(db.Date,nullable=False)
    country = db.Column(db.String(120))
    state = db.Column(db.String(120))
    city = db.Column(db.String(120))
    description = db.Column(db.String(1200))
    tournament = db.relationship('Tournament', backref='user', lazy=True)
    inscription = db.relationship('Inscription', backref='user', lazy=True)

    def __init__(self,username,email,name,last_name,password,date_of_birth,country,state,city,description):
        self.username = username
        self.email = email
        self.name = name 
        self.last_name = last_name
        self.password = password
        self.date_of_birth = date_of_birth
        self.country = country
        self.state = state
        self.city = city
        self.description = description

    def __repr__(self):
        return f"User username: {self.username},e-mail: {self.email},name : {self.name},last_name: {self.last_name},date of birt: {self.date_of_birth},country: {self.country},state: {self.state},city: {self.city}"
            

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "name" : self.name,
            "last_name" : self.last_name,
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
        return f"Tournament tournament_name: {self.tournament_name},game_title: {self.game_title},game_plataform: {self.game_plataform},deadline: {self.deadline},start_date: {self.start_date},country: {self.country},state: {self.state},city: {self.city},participants: {self.participants},entrance fee: {self.entrance_fee},prize: {self.prize},kind: {self.prize}" 

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
    match_result_one = db.Column(db.Integer)
    match_result_two = db.Column(db.Integer)
    # won_one = db.Column(db.Boolean,nullable=False)
    # won_two = db.Column(db.Boolean,nullable=False)
    round = db.Column(db.Integer,nullable=False)
    
    def __init__(self,tournament_id,competitor_one_id,competitor_two_id,status,round):
        self.tournament_id = tournament_id
        self.competitor_one_id = competitor_one_id
        self.competitor_two_id = competitor_two_id
        self.status = status
        self.round = round

    def __repr__(self):
        return '<Match %r>' % self.round

    def serialize(self):
        return {
            "hello" : "chao"
        }

    def create_matches_mode_league(self, registered_users):
        number_enrolled = len(registered_users)
        index_participants = 0
        odd = True if number_enrolled%2 != 0 else False

        if odd:
            number_enrolled += 1

        total_one_day_matches = number_enrolled/2 # total de partidos de una jornada
        journey = []
        inverse_index = number_enrolled-2

        for i in range(1,number_enrolled):
            list_equipos = {}
            for match_journey in range(0,total_one_day_matches):
                if index_participants > number_enrolled-2:
                    index_participants = 0

            if inverse_index < 0:
                inverse_index = number_enrolled-2

        #   if indiceP == 0: # seria el partido inicial de cada fecha
        #      if impar:
        #         equipos.append(clubes[index_clubes])
        #      else:
        #         if (i+1)%2 == 0:
        #            partido = [clubes[index_clubes], clubes[auxT-1]]
        #         else:
        #            partido = [clubes[auxT-1], clubes[index_clubes]]
        #         equipos.append(" vs ".join(partido))
        #     else:
        #     partido = [clubes[index_clubes], clubes[indiceInverso]]
        #     equipos.append(" vs ".join(partido))
        #     indiceInverso -= 1
        #     index_clubes += 1

        #     list_equipos = {
        #         'jornada': "Jornada Nro.: " + str(i),
        #         'equipos': equipos
        #     }
        #     jornada.append(list_equipos)

        #     print(jornada)


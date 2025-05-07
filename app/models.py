from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    teams = db.relationship('Team', backref='manager', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    players = db.relationship('Player', backref='team', lazy='dynamic')
    games = db.relationship('Game', backref='team', lazy='dynamic')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    number = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    batting_orders = db.relationship('BattingOrder', backref='player', lazy='dynamic')
    game_stats = db.relationship('GameStats', backref='player', lazy='dynamic')
    at_bats = db.relationship('AtBat', backref='batter', lazy='dynamic')
    outs = db.relationship('Out', foreign_keys='Out.player_id', backref='player', lazy='dynamic')
    fielded_outs = db.relationship('Out', foreign_keys='Out.fielder_id', backref='fielder', lazy='dynamic')
    steals = db.relationship('Steal', backref='player', lazy='dynamic')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    opponent = db.Column(db.String(64), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    innings = db.relationship('Inning', backref='game', lazy='dynamic')
    batting_orders = db.relationship('BattingOrder', backref='game', lazy='dynamic')
    game_stats = db.relationship('GameStats', backref='game', lazy='dynamic')

class Inning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    inning_number = db.Column(db.Integer, nullable=False)
    team_runs = db.Column(db.Integer, default=0)
    opponent_runs = db.Column(db.Integer, default=0)
    at_bats = db.relationship('AtBat', backref='inning', lazy='dynamic')

class BattingOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    order_number = db.Column(db.Integer, nullable=False)

class GameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    at_bats = db.Column(db.Integer, default=0)
    hits = db.Column(db.Integer, default=0)
    runs = db.Column(db.Integer, default=0)
    rbis = db.Column(db.Integer, default=0)
    strikeouts = db.Column(db.Integer, default=0)
    walks = db.Column(db.Integer, default=0)
    stolen_bases = db.Column(db.Integer, default=0)
    caught_stealing = db.Column(db.Integer, default=0)

class AtBat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inning_id = db.Column(db.Integer, db.ForeignKey('inning.id'))
    batter_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    result = db.Column(db.String(32), nullable=False)  # e.g., 'single', 'double', 'strikeout', 'walk'
    rbis = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    outs = db.relationship('Out', backref='at_bat', lazy='dynamic')
    steals = db.relationship('Steal', backref='at_bat', lazy='dynamic')
    
    # Track pitch count
    balls = db.Column(db.Integer, default=0)
    strikes = db.Column(db.Integer, default=0)
    
    # Track base advancements
    bases_advanced = db.Column(db.Integer, default=0)  # How many bases the batter advanced
    runners_advanced = db.Column(db.Integer, default=0)  # How many runners advanced

class Out(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    at_bat_id = db.Column(db.Integer, db.ForeignKey('at_bat.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    out_type = db.Column(db.String(32), nullable=False)  # e.g., 'strikeout', 'groundout', 'flyout', 'caught_stealing'
    base = db.Column(db.Integer)  # 1, 2, 3, or home for fielding outs, null for strikeouts
    fielder_id = db.Column(db.Integer, db.ForeignKey('player.id'))  # Player who made the out
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Steal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    at_bat_id = db.Column(db.Integer, db.ForeignKey('at_bat.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    from_base = db.Column(db.Integer, nullable=False)  # Base they're stealing from
    to_base = db.Column(db.Integer, nullable=False)    # Base they're stealing to
    success = db.Column(db.Boolean, nullable=False)    # Whether the steal was successful
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 
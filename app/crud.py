from app import db
from app.models import User, Team, Player, Game, GameStats, BattingOrder, Inning, AtBat, Out, Steal
from datetime import datetime
from typing import List, Optional, Dict, Any
from werkzeug.security import generate_password_hash

# User CRUD operations
def create_user(username: str, email: str, password: str) -> User:
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(user_id: int) -> Optional[User]:
    return db.session.get(User, user_id)

def get_user_by_username(username: str) -> Optional[User]:
    return User.query.filter_by(username=username).first()

def get_user_by_email(email: str) -> Optional[User]:
    return User.query.filter_by(email=email).first()

def update_user(user_id: int, data: Dict[str, Any]) -> Optional[User]:
    user = get_user_by_id(user_id)
    if user:
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
    return user

def delete_user(user_id: int) -> bool:
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

# Team CRUD operations
def create_team(name: str, user_id: int) -> Team:
    team = Team(name=name, user_id=user_id)
    db.session.add(team)
    db.session.commit()
    return team

def get_team_by_id(team_id: int) -> Optional[Team]:
    return db.session.get(Team, team_id)

def get_teams_by_user(user_id: int) -> List[Team]:
    return Team.query.filter_by(user_id=user_id).all()

def update_team(team_id: int, data: Dict[str, Any]) -> Optional[Team]:
    team = get_team_by_id(team_id)
    if team:
        if 'name' in data:
            team.name = data['name']
        db.session.commit()
    return team

def delete_team(team_id: int) -> bool:
    team = get_team_by_id(team_id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return True
    return False

# Player CRUD operations
def create_player(name: str, team_id: int, number: Optional[int] = None) -> Player:
    player = Player(name=name, team_id=team_id, number=number)
    db.session.add(player)
    db.session.commit()
    return player

def get_player_by_id(player_id: int) -> Optional[Player]:
    return db.session.get(Player, player_id)

def get_players_by_team(team_id: int) -> List[Player]:
    return Player.query.filter_by(team_id=team_id).all()

def update_player(player_id: int, data: Dict[str, Any]) -> Optional[Player]:
    player = get_player_by_id(player_id)
    if player:
        if 'name' in data:
            player.name = data['name']
        if 'number' in data:
            player.number = data['number']
        db.session.commit()
    return player

def delete_player(player_id: int) -> bool:
    player = get_player_by_id(player_id)
    if player:
        db.session.delete(player)
        db.session.commit()
        return True
    return False

# Game CRUD operations
def create_game(date: datetime, opponent: str, team_id: int) -> Game:
    game = Game(date=date, opponent=opponent, team_id=team_id)
    db.session.add(game)
    db.session.commit()
    return game

def get_game_by_id(game_id: int) -> Optional[Game]:
    return db.session.get(Game, game_id)

def get_games_by_team(team_id: int) -> List[Game]:
    return Game.query.filter_by(team_id=team_id).all()

def update_game(game_id: int, data: Dict[str, Any]) -> Optional[Game]:
    game = get_game_by_id(game_id)
    if game:
        if 'date' in data:
            game.date = data['date']
        if 'opponent' in data:
            game.opponent = data['opponent']
        db.session.commit()
    return game

def delete_game(game_id: int) -> bool:
    game = get_game_by_id(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
        return True
    return False

# Game Stats CRUD operations
def create_game_stats(game_id: int, player_id: int) -> GameStats:
    stats = GameStats(game_id=game_id, player_id=player_id)
    db.session.add(stats)
    db.session.commit()
    return stats

def get_game_stats(game_id: int, player_id: int) -> Optional[GameStats]:
    return GameStats.query.filter_by(game_id=game_id, player_id=player_id).first()

def update_game_stats(game_id: int, player_id: int, data: Dict[str, Any]) -> Optional[GameStats]:
    stats = get_game_stats(game_id, player_id)
    if stats:
        for key, value in data.items():
            if hasattr(stats, key):
                setattr(stats, key, value)
        db.session.commit()
    return stats

# Batting Order CRUD operations
def create_batting_order(game_id: int, player_id: int, order_number: int) -> BattingOrder:
    batting_order = BattingOrder(game_id=game_id, player_id=player_id, order_number=order_number)
    db.session.add(batting_order)
    db.session.commit()
    return batting_order

def get_batting_order(game_id: int) -> List[BattingOrder]:
    return BattingOrder.query.filter_by(game_id=game_id).order_by(BattingOrder.order_number).all()

def update_batting_order(batting_order_id: int, order_number: int) -> Optional[BattingOrder]:
    batting_order = db.session.get(BattingOrder, batting_order_id)
    if batting_order:
        batting_order.order_number = order_number
        db.session.commit()
    return batting_order

def delete_batting_order(batting_order_id: int) -> bool:
    batting_order = db.session.get(BattingOrder, batting_order_id)
    if batting_order:
        db.session.delete(batting_order)
        db.session.commit()
        return True
    return False 
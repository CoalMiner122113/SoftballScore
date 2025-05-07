import pytest
from app import create_app, db
from app.models import User, Team, Player, Game, GameStats, BattingOrder
from app.crud import (
    create_user, get_user_by_id, get_user_by_username, get_user_by_email,
    update_user, delete_user,
    create_team, get_team_by_id, get_teams_by_user, update_team, delete_team,
    create_player, get_player_by_id, get_players_by_team, update_player, delete_player,
    create_game, get_game_by_id, get_games_by_team, update_game, delete_game,
    create_game_stats, get_game_stats, update_game_stats,
    create_batting_order, get_batting_order, update_batting_order, delete_batting_order
)
from datetime import datetime

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] + '_test'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# User CRUD Tests
def test_user_crud(app):
    with app.app_context():
        # Create
        user = create_user('testuser', 'test@example.com', 'password123')
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('password123')

        # Read
        user_by_id = get_user_by_id(user.id)
        assert user_by_id == user

        user_by_username = get_user_by_username('testuser')
        assert user_by_username == user

        user_by_email = get_user_by_email('test@example.com')
        assert user_by_email == user

        # Update
        updated_user = update_user(user.id, {
            'username': 'newusername',
            'email': 'new@example.com',
            'password': 'newpassword'
        })
        assert updated_user.username == 'newusername'
        assert updated_user.email == 'new@example.com'
        assert updated_user.check_password('newpassword')

        # Delete
        assert delete_user(user.id)
        assert get_user_by_id(user.id) is None

# Team CRUD Tests
def test_team_crud(app):
    with app.app_context():
        # Create user first
        user = create_user('testuser', 'test@example.com', 'password123')
        
        # Create
        team = create_team('Test Team', user.id)
        assert team.id is not None
        assert team.name == 'Test Team'
        assert team.user_id == user.id

        # Read
        team_by_id = get_team_by_id(team.id)
        assert team_by_id == team

        teams_by_user = get_teams_by_user(user.id)
        assert len(teams_by_user) == 1
        assert teams_by_user[0] == team

        # Update
        updated_team = update_team(team.id, {'name': 'New Team Name'})
        assert updated_team.name == 'New Team Name'

        # Delete
        assert delete_team(team.id)
        assert get_team_by_id(team.id) is None

# Player CRUD Tests
def test_player_crud(app):
    with app.app_context():
        # Create user and team first
        user = create_user('testuser', 'test@example.com', 'password123')
        team = create_team('Test Team', user.id)
        
        # Create
        player = create_player('Test Player', team.id, 42)
        assert player.id is not None
        assert player.name == 'Test Player'
        assert player.number == 42
        assert player.team_id == team.id

        # Read
        player_by_id = get_player_by_id(player.id)
        assert player_by_id == player

        players_by_team = get_players_by_team(team.id)
        assert len(players_by_team) == 1
        assert players_by_team[0] == player

        # Update
        updated_player = update_player(player.id, {
            'name': 'New Player Name',
            'number': 99
        })
        assert updated_player.name == 'New Player Name'
        assert updated_player.number == 99

        # Delete
        assert delete_player(player.id)
        assert get_player_by_id(player.id) is None

# Game CRUD Tests
def test_game_crud(app):
    with app.app_context():
        # Create user and team first
        user = create_user('testuser', 'test@example.com', 'password123')
        team = create_team('Test Team', user.id)
        
        # Create
        game_date = datetime.utcnow().replace(microsecond=0)
        game = create_game(game_date, 'Opponent Team', team.id)
        assert game.id is not None
        assert game.date.replace(microsecond=0) == game_date
        assert game.opponent == 'Opponent Team'
        assert game.team_id == team.id

        # Read
        game_by_id = get_game_by_id(game.id)
        assert game_by_id == game

        games_by_team = get_games_by_team(team.id)
        assert len(games_by_team) == 1
        assert games_by_team[0] == game

        # Update
        new_date = datetime.utcnow().replace(microsecond=0)
        updated_game = update_game(game.id, {
            'date': new_date,
            'opponent': 'New Opponent'
        })
        assert updated_game.date.replace(microsecond=0) == new_date
        assert updated_game.opponent == 'New Opponent'

        # Delete
        assert delete_game(game.id)
        assert get_game_by_id(game.id) is None

# Game Stats CRUD Tests
def test_game_stats_crud(app):
    with app.app_context():
        # Create user, team, player, and game first
        user = create_user('testuser', 'test@example.com', 'password123')
        team = create_team('Test Team', user.id)
        player = create_player('Test Player', team.id)
        game = create_game(datetime.utcnow(), 'Opponent Team', team.id)
        
        # Create
        stats = create_game_stats(game.id, player.id)
        assert stats.id is not None
        assert stats.game_id == game.id
        assert stats.player_id == player.id

        # Read
        stats_by_game_player = get_game_stats(game.id, player.id)
        assert stats_by_game_player == stats

        # Update
        updated_stats = update_game_stats(game.id, player.id, {
            'at_bats': 3,
            'hits': 2,
            'runs': 1,
            'rbis': 2
        })
        assert updated_stats.at_bats == 3
        assert updated_stats.hits == 2
        assert updated_stats.runs == 1
        assert updated_stats.rbis == 2

# Batting Order CRUD Tests
def test_batting_order_crud(app):
    with app.app_context():
        # Create user, team, player, and game first
        user = create_user('testuser', 'test@example.com', 'password123')
        team = create_team('Test Team', user.id)
        player = create_player('Test Player', team.id)
        game = create_game(datetime.utcnow(), 'Opponent Team', team.id)
        
        # Create
        batting_order = create_batting_order(game.id, player.id, 1)
        assert batting_order.id is not None
        assert batting_order.game_id == game.id
        assert batting_order.player_id == player.id
        assert batting_order.order_number == 1

        # Read
        batting_orders = get_batting_order(game.id)
        assert len(batting_orders) == 1
        assert batting_orders[0] == batting_order

        # Update
        updated_order = update_batting_order(batting_order.id, 2)
        assert updated_order.order_number == 2

        # Delete
        assert delete_batting_order(batting_order.id)
        assert len(get_batting_order(game.id)) == 0 
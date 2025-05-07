import pytest
from app import create_app, db
from app.models import User, Team, Player, Game
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

def test_user_creation(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')

def test_team_creation(app):
    with app.app_context():
        # Create a test user and team
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        team = Team(name='Test Team', user_id=user.id)
        db.session.add(team)
        db.session.commit()
        
        # Verify team was created
        assert team.id is not None
        assert team.name == 'Test Team'
        assert team.user_id == user.id
        assert team.manager == user

def test_player_creation(app):
    with app.app_context():
        # Create test user, team, and player
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        team = Team(name='Test Team', user_id=user.id)
        db.session.add(team)
        db.session.commit()
        
        player = Player(name='Test Player', number=42, team_id=team.id)
        db.session.add(player)
        db.session.commit()
        
        # Verify player was created
        assert player.id is not None
        assert player.name == 'Test Player'
        assert player.number == 42
        assert player.team_id == team.id
        assert player.team == team

def test_game_creation(app):
    with app.app_context():
        # Create test user, team, and game
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        team = Team(name='Test Team', user_id=user.id)
        db.session.add(team)
        db.session.commit()
        
        game = Game(
            date=datetime.utcnow(),
            opponent='Opponent Team',
            team_id=team.id
        )
        db.session.add(game)
        db.session.commit()
        
        # Verify game was created
        assert game.id is not None
        assert game.opponent == 'Opponent Team'
        assert game.team_id == team.id
        assert game.team == team

def test_relationships(app):
    with app.app_context():
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Create test team
        team = Team(name='Test Team', user_id=user.id)
        db.session.add(team)
        db.session.commit()
        
        # Create test players
        player1 = Player(name='Player 1', number=1, team_id=team.id)
        player2 = Player(name='Player 2', number=2, team_id=team.id)
        db.session.add_all([player1, player2])
        db.session.commit()
        
        # Create test game
        game = Game(
            date=datetime.utcnow(),
            opponent='Opponent Team',
            team_id=team.id
        )
        db.session.add(game)
        db.session.commit()
        
        # Verify relationships
        assert user.teams.count() == 1
        assert team.players.count() == 2
        assert team.games.count() == 1
        assert player1.team == team
        assert game.team == team 
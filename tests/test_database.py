import pytest
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test that we can connect to the database"""
    # Get individual connection parameters
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_db = os.getenv('MYSQL_DB')
    mysql_port = os.getenv('MYSQL_PORT')

    # Print connection parameters (excluding password)
    print(f"\nConnection parameters:")
    print(f"User: {mysql_user}")
    print(f"Host: {mysql_host}")
    print(f"Port: {mysql_port}")
    print(f"Database: {mysql_db}")

    # Check if all required environment variables are set
    assert mysql_user is not None, "MYSQL_USER environment variable is not set"
    assert mysql_password is not None, "MYSQL_PASSWORD environment variable is not set"
    assert mysql_host is not None, "MYSQL_HOST environment variable is not set"
    assert mysql_db is not None, "MYSQL_DB environment variable is not set"
    assert mysql_port is not None, "MYSQL_PORT environment variable is not set"
    
    try:
        # Create connection URL from individual parameters
        db_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
        
        # Create engine
        engine = create_engine(db_url)
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1, "Database query failed"
            
    except Exception as e:
        pytest.fail(f"Failed to connect to database: {str(e)}") 
import os
from dotenv import load_dotenv
import pymysql
from config import Config

# Load environment variables
load_dotenv()

def create_database():
    # Get database connection details
    config = Config()
    
    # Print configuration (excluding password)
    print("\nConfiguration:")
    print(f"Host: {config.MYSQL_HOST}")
    print(f"User: {config.MYSQL_USER}")
    print(f"Database: {config.MYSQL_DB}")
    print(f"Port: {config.MYSQL_PORT}")
    
    # Connect to MySQL without specifying a database
    conn = pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        port=int(config.MYSQL_PORT)
    )
    
    try:
        with conn.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB}")
            print(f"Database '{config.MYSQL_DB}' created or already exists")
            
    finally:
        conn.close()

if __name__ == '__main__':
    create_database() 
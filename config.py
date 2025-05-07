import os
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector
import pymysql

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # MySQL connection details
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_DB = os.environ.get('MYSQL_DB')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_connector():
        connector = Connector()
        
        def getconn():
            conn = connector.connect(
                MYSQL_HOST,
                "pymysql",
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                db=MYSQL_DB,
            )
            return conn

        return getconn 
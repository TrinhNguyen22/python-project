import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    engine = os.environ.get('DB_ENGINE')
    host = os.environ.get('DB_HOST')
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    name = os.environ.get('DB_NAME')
    port = os.environ.get('DB_PORT')
    # return f'{engine}://{username}:{password}@{host}/{name}'
    return f'{engine}://{username}:{password}@{host}:{port}/{name}'


SQLALCHEMY_DB_URL = get_db_connection()
ADMIN_DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD')

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

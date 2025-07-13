import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'DB_USER': os.getenv('DB_USER', None),
    'DB_PASSWORD': os.getenv('DB_PASSWORD', None),
    'DB_HOST': os.getenv('DB_HOST', None),
    'DB_PORT': os.getenv('DB_PORT', None),
    'DB_NAME': os.getenv('DB_NAME', None),
    'TOKEN_KEY': os.getenv('TOKEN_KEY', 'mysecretkey'),
    'TOKEN_ALGORITHM': os.getenv('TOKEN_ALGORITHM', 'HS256'), # Lo tuve que hacer para que no me diera error
}

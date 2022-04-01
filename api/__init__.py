import os

from .base_client import ApiClient
from .user import User
from dotenv import load_dotenv

load_dotenv()


api = ApiClient(root_url=os.getenv('ROOT_PATH'))
user_methods = User(api=api)

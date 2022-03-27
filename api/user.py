from .base import ApiClient

class User:
    def __init__(self, api: ApiClient = None):
        self.api = api
    
    async def get_users(self):
        return await self.api.get('users')
    
    async def add_user(self, id, username, nickname=None):
        data = {
            'telegram_id': id,
            'username': username,
            'nickname': nickname
        }
        return await self.api.post('user', data=data)

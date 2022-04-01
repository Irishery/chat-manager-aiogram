from .base_client import ApiClient

class User:
    def __init__(self, api: ApiClient = None):
        self.api = api
    
    async def get_users(self):
        return await self.api.get('users')
    
    async def get_user(self, id, type):
        data = {
            'id': id,
            'type': type
        }
        return await self.api.get('user', data=data)

    
    async def add_user(self, id, username, nickname=None):
        data = {
            'telegram_id': id,
            'username': username,
            'nickname': nickname
        }
        return await self.api.post('user', data=data)
    
    async def send_message(self, id, text, nickname):
        data = {
            'telegram_id': id,
            'message_text': text,
            'nickname': nickname
        }
        return await self.api.post('message/user', data=data)

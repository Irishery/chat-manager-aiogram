from .base_client import ApiClient, ApiError

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
        print('getting user')
        if not (data['type'] == 'telegram' or data['type'] == 'pk'):
                raise ApiError(f'Type is incorrect. There are two types:\
                                telegram, pk. Got {data["type"]}')
        user = await self.api.get('user', params=data)
        print(user)
        print('got it')
        return user

    
    async def add_user(self, id, username, nickname=None, number=None):
        data = {
            'telegram_id': id,
            'username': username,
            'nickname': nickname
        }
        return await self.api.post('user', params=data)
    
    async def send_message(self, id, text, nickname, is_call, name=None, contact=None):
        data = {
            'telegram_id': id,
            'message_text': text,
            'nickname': nickname,
            'request_to_call': is_call,
            'name': name,
            'contact': contact
        }
        return await self.api.post('message/user', params=data)

    async def send_pic(self, pic, params):
        return await self.api.post('user/pic', picture=pic, params=params)

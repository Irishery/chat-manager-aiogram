from urllib.parse import urljoin
import json
import httpx

class ApiError(Exception):
    pass

class ApiClient:
    def __init__(self, root_url):
        self.root_url = root_url

    async def request(self, method, path, params=None, data=None, json=None,
                                                       picture=None):
        client = httpx.AsyncClient(timeout=None)
        try:
            if picture:
                resp = await client.request(
                    method, urljoin(self.root_url, path) + '/',
                    params=params,
                    data=picture,
                    headers={'content-type': 'application/json'}
                )
                
            else:
                resp = await client.request(
                    method, urljoin(self.root_url, path) + '/',
                    params=params,
                    headers={'content-type': 'application/json'}
                )

            resp_json = resp.json()

            if resp.status_code != 200:
                raise ApiError(
                    f"Error: {resp_json}."
                )
        except httpx.ConnectError:
                raise ApiError(f"Cannot connect to host {self.root_url}")
        except json.JSONDecodeError:
                raise ApiError(
                    f"Can't decode json, content: {resp.text}. "
                    f"Code: {resp.status_code}")
        finally:
            await client.aclose()

        return resp_json
    
    async def get(self, path, data=None, params=None):
        return await self.request('get', path, data=data, params=params)
    
    async def post(self, path, data=None, params=None, json=None, picture=None):
        return await self.request('post', path, data=data, json=json,
                                params=params, picture=picture)

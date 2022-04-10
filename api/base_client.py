import json

from urllib.parse import urljoin

import httpx

class ApiError(Exception):
    pass

class ApiClient:
    def __init__(self, root_url):
        self.root_url = root_url

    async def request(self, method, path, params=None, data=None):
        client = httpx.AsyncClient(timeout=None)

        try:
            resp = await client.request(
                method, urljoin(self.root_url, path) + '/',
                params=data,
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
        return await self.request('get', path, data=data)
    
    async def post(self, path, data, params=None):
        return await self.request('post', path, data=data)

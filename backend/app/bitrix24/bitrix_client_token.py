
import json
import time
from requests import post, adapters, exceptions

from .bitrix_client import InterfaceBitrixClient
from app.repositories.credentials import CredentialRepository


adapters.DEFAULT_RETRIES = 10


class BitrixClient(InterfaceBitrixClient):
    api_url = 'https://%s/rest/%s.json'
    oauth_url = 'https://oauth.bitrix.info/oauth/token/'
    timeout = 60

    def __init__(self, credential_repository: CredentialRepository):
        self.credential_id = 1
        self.credential_repository = credential_repository
        self.token_data = None

    async def load_token(self):
        self.token_data = await self.credential_repository.get(self.credential_id)

    async def refresh_tokens(self):
        await self.load_token()
        try:
            r = post(
                self.oauth_url,
                params={
                    'grant_type': 'refresh_token',
                    'client_id': self.token_data.client_id,
                    'client_secret': self.token_data.client_secret,
                    'refresh_token': self.token_data.refresh_token
                }
            )
            result = r.json()

            await self.credential_repository.edit_one(
                ident = 1,
                data = {
                    'auth_token': result['access_token'],
                    'refresh_token': result['refresh_token']
                }
            )
            return True
        except Exception as e:
            return {'error': f"Failed to refresh token: {e}"}

    async def call(self, method, params):
        await self.load_token()
        try:
            url = self.api_url % (self.token_data.domain, method)
            url += '?auth=' + self.token_data.auth_token
            headers = {
                'Content-Type': 'application/json',
            }
            r = post(url, data=json.dumps(params), headers=headers, timeout=self.timeout)
            result = r.json()
        except ValueError:
            result = dict(error='Error on decode api response [%s]' % r.text)
        except exceptions.ReadTimeout:
            result = dict(error='Timeout waiting expired [%s sec]' % str(self.timeout))
        except exceptions.ConnectionError:
            result = dict(error='Max retries exceeded [' + str(adapters.DEFAULT_RETRIES) + ']')

        if 'error' in result and result['error'] in ('NO_AUTH_FOUND', 'expired_token'):
            result_update_token = await self.refresh_tokens()
            if result_update_token is not True:
                return result
            result = await self.call(method, params)
        elif 'error' in result and result['error'] in ['QUERY_LIMIT_EXCEEDED', ]:
            time.sleep(2)
            return await self.call(method, params)

        return result

    async def batch(self, params):
        if 'halt' not in params or 'cmd' not in params:
            return dict(error='Invalid batch structure')

        return await self.call("batch", params)
    






















    # async def refresh_tokens(self):
    #     r = {}
    #     try:
    #         r = post(
    #             self.oauth_url,
    #             params={
    #                 'grant_type': 'refresh_token',
    #                 'client_id': self.token_data.client_id,
    #                 'client_secret': self.token_data.client_secret,
    #                 'refresh_token': self.token_data.refresh_token
    #             }
    #         )
    #         result = json.loads(r.text)
    #         self.auth_token = result['access_token']
    #         self.refresh_token = result['refresh_token']
    #         self.expires_in = result['expires_in']
    #         # bitrix_token.update_secrets(self.auth_token, self.expires_in, self.refresh_token)
    #         await self.credential_repository.edit_one(
    #             {
    #                 access_token
    #             }
    #             result['access_token'], result['refresh_token'], result['expires_in']
    #         )
    #         return True
    #     except (ValueError, KeyError):
    #         result = dict(error='Error on decode oauth response [%s]' % r.text)
    #         return result



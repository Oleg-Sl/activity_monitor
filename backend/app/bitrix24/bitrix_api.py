import json
import time
from requests import adapters, post, exceptions

from . import bitrix_token


adapters.DEFAULT_RETRIES = 10


class Bitrix24:
    api_url = 'https://%s/rest/%s.json'
    oauth_url = 'https://oauth.bitrix.info/oauth/token/'
    timeout = 60

    def __init__(self):
        token_data = bitrix_token.get_secrets_all()
        self.domain = token_data.get("domain", None)
        self.auth_token = token_data.get("auth_token", None)
        self.refresh_token = token_data.get("refresh_token", None)
        self.client_id = bitrix_token.get_secret("client_id")
        self.client_secret = bitrix_token.get_secret("client_secret")

    def refresh_tokens(self):
        r = {}
        try:
            r = post(
                self.oauth_url,
                params={'grant_type': 'refresh_token', 'client_id': self.client_id, 'client_secret': self.client_secret,
                        'refresh_token': self.refresh_token})
            print("refresh_token: ", r.text)
            result = json.loads(r.text)
            self.auth_token = result['access_token']
            self.refresh_token = result['refresh_token']
            self.expires_in = result['expires_in']
            bitrix_token.update_secrets(self.auth_token, self.expires_in, self.refresh_token)
            return True
        except (ValueError, KeyError):
            result = dict(error='Error on decode oauth response [%s]' % r.text)
            return result

    def call(self, method, params):
        try:
            url = self.api_url % (self.domain, method)
            url += '?auth=' + self.auth_token
            headers = {
                'Content-Type': 'application/json',
            }
            r = post(url, data=json.dumps(params), headers=headers, timeout=self.timeout)
            result = json.loads(r.text)
        except ValueError:
            pass
            result = dict(error='Error on decode api response [%s]' % r.text)
        except exceptions.ReadTimeout:
            result = dict(error='Timeout waiting expired [%s sec]' % str(self.timeout))
        except exceptions.ConnectionError:
            result = dict(error='Max retries exceeded [' + str(adapters.DEFAULT_RETRIES) + ']')

        if 'error' in result and result['error'] in ('NO_AUTH_FOUND', 'expired_token'):
            result_update_token = self.refresh_tokens()
            if result_update_token is not True:
                return result
            result = self.call(method, params)
        elif 'error' in result and result['error'] in ['QUERY_LIMIT_EXCEEDED', ]:
            time.sleep(2)
            return self.call(method, params)

        return result

    def batch(self, params):
        if 'halt' not in params or 'cmd' not in params:
            return dict(error='Invalid batch structure')

        return self.call("batch", params)
    
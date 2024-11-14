import os
import json


path_secret_file = os.path.join(settings.BASE_DIR, 'bitrix24', 'secrets_bx24.json')


def save_secrets(data):
    data_old = {}
    with open(path_secret_file) as secrets_file:
        data_old = json.load(secrets_file)

    with open(path_secret_file, 'w') as secrets_file:
        data_old.update(data)
        json.dump(data_old, secrets_file)


def update_secrets(auth_token, expires_in, refresh_token):
    with open(path_secret_file) as secrets_file:
        data = json.load(secrets_file)

    data["auth_token"] = auth_token
    data["expires_in"] = expires_in
    data["refresh_token"] = refresh_token

    with open(path_secret_file, 'w') as secrets_file:
        json.dump(data, secrets_file)


def get_secret(key):
    with open(path_secret_file) as secrets_file:
        data = json.load(secrets_file)

    return data.get(key)


def get_secrets_all():
    with open(path_secret_file) as secrets_file:
        data = json.load(secrets_file)

    return data

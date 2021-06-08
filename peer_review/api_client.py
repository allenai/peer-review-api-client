import requests
import json
import config

class ApiClient():
    def __init__(self, base_url, key):
        self.headers = {"x-api-key": key}
        self.base_url = base_url

    def get(self, url: str):
        resp = requests.get(f'{self.base_url}/{url}', headers=self.headers)
        if resp.status_code != 200:
            raise Exception(
                f'Returned status code {resp.status_code} from GET {self.base_url}/{url}: {resp.text}')
        return json.loads(resp.text)

    def post(self, url: str, body):
        resp = requests.post(f'{self.base_url}/{url}', json=body, headers=self.headers)
        if resp.status_code != 200:
            raise Exception(
                f'Returned status code {resp.status_code} from POST {self.base_url}/{url}: {resp.text}')
        return json.loads(resp.text)


def client():
    return ApiClient(f"{config.get('url')}", config.get('api_key'))

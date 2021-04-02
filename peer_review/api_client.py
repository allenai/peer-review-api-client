import requests
import json
import os


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


api_key = None
settings_file = os.path.join(os.path.dirname(__file__), '.api_client')
if os.path.isfile(settings_file):
    with open(settings_file) as f:
        settings = json.load(f)
        api_key = settings.get('api_key')

if not api_key:
    api_key = input("Enter API Key:")
    settings = {'api_key': api_key}
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

client = ApiClient("http://conference-api.prod.s2.allenai.org/peer-review", api_key)

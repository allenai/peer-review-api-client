import json
import csv
from api_client import client

def create(pool_name, file):
    pool_id = client.post('submission-pool',{'name':pool_name})['id']
    with open(file) as f:
        for row in csv.DictReader(f):
            row['authors'] = json.loads(row['authors'])
            client.post(f'submission-pool/{pool_id}/submission', row)
    return pool_id

def list():
    return client.get(f'submission-pool')

def list_submissions(pool_id):
    return client.get(f'submission-pool/{pool_id}/submission')




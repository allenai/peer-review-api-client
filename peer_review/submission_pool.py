import json
import csv
import sys
from api_client import client

def create(pool_name, file):
    pool_id = client().post('submission-pool',{'name':pool_name})['id']
    with open(file) as f:
        for row in csv.DictReader(f):
            row['authors'] = json.loads(row['authors'])
            client().post(f'submission-pool/{pool_id}/submission', row)
    return pool_id

def list():
    return client().get(f'submission-pool')

def list_submissions(pool_id):
    return client().get(f'submission-pool/{pool_id}/submission')

def print_pools():
    pools = list()
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'name', 'size'])
    writer.writeheader()
    for r in pools:
        r['size'] = client().get(f'submission-pool/{r["id"]}/size')
        writer.writerow(r)

def print_submissions(pool_id):
    submissions = list_submissions(pool_id)
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'externalId', 'title', 'abstract', 'authors'])
    writer.writeheader()
    for r in submissions:
        r['authors'] = json.dumps(r['authors'])
        writer.writerow(r)



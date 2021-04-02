import csv
import sys
from api_client import client

def create(pool_name, file):
    pool_id = client().post('reviewer-pool',{'name':pool_name})['id']
    with open(file) as f:
        for row in csv.DictReader(f):
            row['semanticScholarId'] = int(row['semanticScholarId'])
            client().post(f'reviewer-pool/{pool_id}/reviewer', row)
    return pool_id

def list():
    return client().get('reviewer-pool')

def list_reviewers(pool_id):
    return client().get(f'reviewer-pool/{pool_id}/reviewer')

def print_pools():
    pools = list()
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'name'])
    writer.writeheader()
    for r in pools:
        writer.writerow(r)

def print_reviewers(pool_id):
    reviewers = list_reviewers(pool_id)
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'name', 'semanticScholarId', 'externalId'])
    writer.writeheader()
    for r in reviewers:
        writer.writerow(r)





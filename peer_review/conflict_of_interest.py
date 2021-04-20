import csv
import sys
from api_client import client

def submit_request(reviewer_pool_id, submission_pool_id):
    req = {'reviewerPoolId':reviewer_pool_id, 'submissionPoolId':submission_pool_id}
    return client().post('conflict-of-interest',req)['id']

def list_requests():
    return client().get('conflict-of-interest')

def print_requests():
    requests = list_requests()
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['id', 'status', 'reviewerPoolId', 'submissionPoolId',
                                        'configuration', 'submitted'])
    writer.writeheader()
    for r in requests:
        writer.writerow(r)


def download_result(request_id):
    return client().get(f'conflict-of-interest/{request_id}/result')

def print_result(request_id):
    results = download_result(request_id)
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['reviewerId', 'reviewerExternalId', 'submissionId', 'submissionExternalId', 'score', 'reason'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

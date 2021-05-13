import csv
import sys
from api_client import client


def submit_request(reviewer_pool_id, submission_pool_id):
    req = {'reviewerPoolId': reviewer_pool_id, 'submissionPoolId': submission_pool_id}
    return client().post('conflict-of-interest', req)['id']


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


def fetch_batch(request_id, start):
    return client().get(f'conflict-of-interest/{request_id}/result?start={start}')


def download_result(request_id, output_file):
    with open(output_file, 'w') as f:
        writer = csv.DictWriter(f,
                                fieldnames=['reviewerId', 'reviewerExternalId', 'submissionId',
                                            'submissionExternalId', 'score', 'reason'])
        writer.writeheader()
        next = 0
        total = 0
        print("Downloading", end="", flush=True)
        while next is not None:
            print("...", end="", flush=True)
            batch = fetch_batch(request_id, next)
            for row in batch['rows']:
                writer.writerow(row)
            total += len(batch['rows'])
            print(total, end="", flush=True)
            next = batch.get('next')
        print("\nDone!")

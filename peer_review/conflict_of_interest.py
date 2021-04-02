from api_client import client

def request(reviewer_pool_id, submission_pool_id):
    req = {'reviewerPoolId':reviewer_pool_id, 'submissionPoolId':submission_pool_id}
    return client.post('conflict-of-interest',req)['id']

def list():
    return client.get('conflict-of-interest')

def download(request_id):
    return client.get(f'conflict-of-interest/{request_id}/result')
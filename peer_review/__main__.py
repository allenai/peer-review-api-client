import click
import reviewer_pool as rp
import submission_pool as sp
import conflict_of_interest as coi
import reviewer_match as rm
import csv
import json
import sys


@click.group()
def app():
    """Command-line client to AI2's peer-review API"""
    pass


@app.group()
def reviewer_pool():
    """Manage Reviewers"""
    pass


@app.group()
def submission_pool():
    """Manage Submissions"""
    pass


@app.group()
def conflict_of_interest():
    """Manage conflict-of-interest calculations"""
    pass


@app.group()
def reviewer_match():
    """Manage reviewer-match calculations"""
    pass


@reviewer_pool.command()
@click.option("--name", help="Name for the reviewer pool", required=True)
@click.option("--file", help="CSV file of reviewer data. Columns [name, semanticScholarId, externalId]",
              required=True)
def create(name, file):
    """Upload reviewer data to a new reviewer pool"""
    id = rp.create(name, file)
    print(f"Created reviewer pool '{name}' with ID={id}")
    pass


@reviewer_pool.command()
@click.option("--id", help="ID of the reviewer pool")
def list_reviewers(id):
    reviewers = rp.list_reviewers(id)
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'name', 'semanticScholarId', 'externalId'])
    writer.writeheader()
    for r in reviewers:
        writer.writerow(r)


@reviewer_pool.command()
def list():
    pools = rp.list()
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'name'])
    writer.writeheader()
    for r in pools:
        writer.writerow(r)


@submission_pool.command()
@click.option("--name", help="Name for the submission pool", required=True)
@click.option("--file",
              help="CSV file of submission data. Columns [externalId,title,abstract,authors] where authors is a JSON-formatted list of objects with fields [name,semanticScholarId]",
              required=True)
def create(name, file):
    """Upload submission data to a new submission pool"""
    id = sp.create(name, file)
    print(f"Created submission pool '{name}' with ID={id}")
    pass


@submission_pool.command()
@click.option("--id", help="ID of the submission pool", required=True)
def list_submissions(id):
    submissions = sp.list_submissions(id)
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'externalId', 'title', 'abstract', 'authors'])
    writer.writeheader()
    for r in submissions:
        r['authors'] = json.dumps(r['authors'])
        writer.writerow(r)


@submission_pool.command()
def list():
    pools = sp.list()
    writer = csv.DictWriter(sys.stdout, fieldnames=['id', 'name'])
    writer.writeheader()
    for r in pools:
        writer.writerow(r)


@conflict_of_interest.command()
@click.option("--reviewer-pool-id", help="ID of the reviewer pool", required=True, type=int)
@click.option("--submission-pool-id", help="ID of the submission pool", required=True, type=int)
def request(reviewer_pool_id, submission_pool_id):
    request_id = coi.request(reviewer_pool_id, submission_pool_id)
    print(f'Submitted conflict-of-interest request with ID={request_id}')


@conflict_of_interest.command()
def list():
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['id', 'status', 'reviewerPoolId', 'submissionPoolId',
                                        'configuration', 'submitted'])
    writer.writeheader()
    for r in coi.list():
        writer.writerow(r)


@conflict_of_interest.command()
@click.option("--request-id", help="ID of the request", required=True, type=int)
def download(request_id):
    results = coi.download(request_id)
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['reviewerId', 'reviewerExternalId', 'submissionId', 'submissionExternalId', 'score', 'reason'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)


@reviewer_match.command()
@click.option("--reviewer-pool-id", help="ID of the reviewer pool", required=True, type=int)
@click.option("--submission-pool-id", help="ID of the submission pool", required=True, type=int)
def request(reviewer_pool_id, submission_pool_id):
    request_id = rm.request(reviewer_pool_id, submission_pool_id)
    print(f'Submitted reviewer-match request with ID={request_id}')


@reviewer_match.command()
def list():
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['id', 'status', 'reviewerPoolId', 'submissionPoolId',
                                        'configuration', 'submitted'])
    writer.writeheader()
    for r in rm.list():
        writer.writerow(r)


@reviewer_match.command()
@click.option("--request-id", help="ID of the request", required=True, type=int)
def download(request_id):
    results = rm.download(request_id)
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['reviewerId', 'reviewerExternalId', 'submissionId', 'submissionExternalId', 'score', 'reason'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)


if __name__ == "__main__":
    app()

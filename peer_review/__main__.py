import click
import reviewer_pool as rp
import submission_pool as sp
import conflict_of_interest as coi
import reviewer_match as rm
import csv
import json
import sys
import config


@click.group()
def app():
    """Command-line client to AI2's peer-review API"""
    pass

@app.command()
def configure():
    """Configure options"""
    config.configure()


@app.group()
def reviewer_pool():
    """Manage reviewers"""
    pass


@app.group()
def submission_pool():
    """Manage submissions"""
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

@reviewer_pool.command()
@click.option("--id", help="ID of the reviewer pool")
def list_reviewers(id):
    rp.print_reviewers(id)

@reviewer_pool.command()
def list():
    rp.print_pools()

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
    sp.print_submissions(id)


@submission_pool.command()
def list():
    sp.print_pools()

@conflict_of_interest.command()
@click.option("--reviewer-pool-id", help="ID of the reviewer pool", required=True, type=int)
@click.option("--submission-pool-id", help="ID of the submission pool", required=True, type=int)
def request(reviewer_pool_id, submission_pool_id):
    request_id = coi.submit_request(reviewer_pool_id, submission_pool_id)
    print(f'Submitted conflict-of-interest request with ID={request_id}')

@conflict_of_interest.command()
def list():
    coi.print_requests()

@conflict_of_interest.command()
@click.option("--request-id", help="ID of the request", required=True, type=int)
@click.option("--output", help="Output file for downloaded results", required=True)
def download(request_id,output):
    coi.download_result(request_id,output)

@reviewer_match.command()
@click.option("--reviewer-pool-id", help="ID of the reviewer pool", required=True, type=int)
@click.option("--submission-pool-id", help="ID of the submission pool", required=True, type=int)
def request(reviewer_pool_id, submission_pool_id):
    request_id = rm.submit_request(reviewer_pool_id, submission_pool_id)
    print(f'Submitted reviewer-match request with ID={request_id}')

@reviewer_match.command()
def list():
    rm.print_requests()

@reviewer_match.command()
@click.option("--request-id", help="ID of the request", required=True, type=int)
@click.option("--output", help="Output file for downloaded results", required=True)
def download(request_id, output):
    rm.download_result(request_id, output)

if __name__ == "__main__":
    app(prog_name="peer-review")

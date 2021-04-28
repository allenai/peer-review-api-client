# AI2 API for Peer Review Management

The [Allen Institute for AI](http://allenai.org) offers an API to aid conference chairs with matching conference submissions with potential reviewers.

The full API documentation can be found [here](https://partner.semanticscholar.org/v1/peer-review).

This repo implements a simple command-line client for convenient access to the API. The provided API key gives access to a shared account for limited trial use. 

For full access to the API, contact our [partner team](https://pages.semanticscholar.org/data-partners). There is no charge for non-commercial use. Restrictions may apply to commercial use.

## Usage

Create a reviewer pool. Note the returned ID
```
./peer-review reviewer-pool create --name 'Test Reviewer Pool' --file sample-data/reviewers-input.csv
```

Create a submission pool. Note the returned ID
```
./peer-review submission-pool create --name 'Test Submission Pool' --file sample-data/submissions-input.csv
``` 

Given a reviewer pool and a submission pool, you can make two types of requests:

1. Detect conflicts of interest, based on a past co-author relationship between a reviewer and a submission's authors

1. Compute matching scores indicating a similarity between the subject matter of a submission and a reviewer's publication history

Both of these calculations rely on supplying the Semantic Scholar author ID for reviewers. Conflict of interest
 detection also relies on having Semantic Scholar author IDs for submission authors. 
 To find the Semantic Scholar ID for an author, search for one of the author's papers on [semanticscholar.org](https://www.semanticscholar.org),
 navigate to the author's profile and take the numeric ID from the final portion of the URL.
 
To get matching scores:

Submit a request to compute match scores for all reviewer-submission pairs in the two pools. Note the returned ID.
```
./peer-review reviewer-match request --reviewer-pool-id <id> --submission-pool-id <id>
```

Check status of the request until status is `COMPLETE`
```
./peer-review reviewer-match list
```

Write the matching scores to stdout
```
./peer-review reviewer-match download --request-id <id>
```

The process is identical for conflict of interest detection, using `./peer-reviewer conflict-of-interest`.

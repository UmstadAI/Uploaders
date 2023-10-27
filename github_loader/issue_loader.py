import os
from langchain.document_loaders import GitHubIssuesLoader

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

loader = GitHubIssuesLoader(
    repo="o1-labs/o1js",
    access_token=token,  # delete/comment out this argument if you've set the access token as an env var.
    include_prs=False,
)

docs = loader.load()

print(docs[188])
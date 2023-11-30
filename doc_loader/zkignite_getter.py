import os
import requests
import re
import base64
from github import Github

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

headers = {
    'Authorization': f'token {token}'
}

def download_readme(repo_url):
    parts = repo_url.strip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    print(f"Downloading {owner}/{repo} readme...")

    g = Github(token)
    repo = g.get_repo(f"{owner}/{repo}")

    readme = repo.get_readme()
    content = base64.b64decode(readme.content)

    return content.decode('utf-8')


urls = [
    "https://github.com/rhvall/MinaDevContainer",
    "https://github.com/airgap-it/airgap-coin-lib",
    "https://github.com/rloot/ZOK",
    "https://github.com/orochi-network/zkDatabase",
    "https://github.com/anomix-zk/anomix-network",
    "https://github.com/EasyMina/easyMina",
    "https://github.com/devarend/mina-playground",
]

if not os.path.exists(f"files/zkignite_docs"):
    os.mkdir(f"files/zkignite_docs")

for url in urls:
    readme = download_readme(url)
    if readme:
        file_name = url.split('/')[-1] + '_README.md'
        with open(f"files/zkignite_docs/{file_name}", 'w') as file:
            file.write(readme)
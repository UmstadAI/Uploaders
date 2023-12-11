import os
import requests
import re
import base64
from github import Github

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

token = os.getenv("GITHUB_ACCESS_TOKEN") or "GITHUB_ACCESS_TOKEN"

headers = {"Authorization": f"token {token}"}


def download_readme(repo_url):
    parts = repo_url.strip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    print(f"Downloading {owner}/{repo} readme...")

    g = Github(token)
    repo = g.get_repo(f"{owner}/{repo}")

    readme = repo.get_readme()
    content = base64.b64decode(readme.content)

    return content.decode("utf-8")


urls = [
    "https://github.com/rhvall/MinaDevContainer",
    "https://github.com/airgap-it/airgap-coin-lib",
    "https://github.com/rloot/ZOK",
    "https://github.com/orochi-network/zkDatabase",
    "https://github.com/anomix-zk/anomix-network",
    "https://github.com/EasyMina/easyMina",
    "https://github.com/devarend/mina-playground",
    "https://github.com/devarend/binance-oracle",
    "https://github.com/RaidasGrisk/zk-github-oracle",
    "https://github.com/ArturVargas/mina-oracle",
    "https://github.com/Raunaque97/privateVRF",
    "https://github.com/a6b8/mina-zk-ignite-cohort-0",
    "https://github.com/rhvall/ConOracle-Osmosis",
    "https://github.com/ubinix-warun/zkOracle-OCW",
    "https://github.com/orkunkilic/mina-decentralized-price-feed",
    "https://github.com/pico-labs/randomness-oracle",
    "https://github.com/iam-robi/zkapp-monorepo",
    "https://github.com/magestrio/bet-oracle",
    "https://github.com/coldstar1993/Voracle",
    "https://github.com/sqrt-xx/grin-oracle",
    "https://github.com/chucklam/mina-geoip-oracle",
    "https://github.com/Comdex/price-zkoracle",
    "https://github.com/lognorman20/zk-dog-oracle",
]

if not os.path.exists(f"files/zkignite_docs"):
    os.mkdir(f"files/zkignite_docs")

for url in urls:
    readme = download_readme(url)
    if readme:
        file_name = url.split("/")[-1] + "_README.md"
        with open(f"files/zkignite_docs/{file_name}", "w") as file:
            file.write(readme)

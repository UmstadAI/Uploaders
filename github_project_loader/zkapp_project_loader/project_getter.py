import os
import glob
import pygit2

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

projects = [
    "https://github.com/rpanic/vale-ui",
    "https://github.com/pico-labs/coinflip-executor-contract",
    "https://github.com/alysiahuggins/proof-of-ownership-zkapp",
    "https://github.com/sausage-dog/minanite",
    "https://github.com/iammadab/dark-chess",
    "https://github.com/gretzke/zkApp-data-types",
    "https://github.com/adrian-gierakowski/fba-on-mina",
    "https://github.com/chainwayxyz/mCash",
    "https://github.com/Sr-santi/mina-ui",
    "https://github.com/Trivo25/offchain-voting-poc",
    "https://github.com/mitschabaude/snarkyjs-sudoku",
    "https://github.com/gordonfreemanfree/snarkyjs-ml",
    "https://github.com/yunus433/snarkyjs-math",
]

os.makedirs('projects', exist_ok=True)

def clone_github_project(repo_link): 
    parts = repo_link.strip('/').split('/')
    owner, repo = parts[-2], parts[-1]

    repoClone = pygit2.clone_repository(repo_link, f"./projects/{repo}")


for repo_link in projects:
    clone_github_project(repo_link)
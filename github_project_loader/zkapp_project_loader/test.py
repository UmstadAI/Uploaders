import re
import os
import base64

from github import Github
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv(), override=True) # read local .env file

def export_project_description_from_readme(content):
    pattern = r'^#\s+(.+?)\n\n(.*?)\n\n'
    match = re.search(pattern, content.decode('utf-8'), re.DOTALL)

    if match:
        print("Found project description in README.md", match.group(2).strip())
        return match.group(2).strip()
    else:
        return None

def test_description_extraction(owner, project_name):
    token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

    g = Github(token)
    repo = g.get_repo(f"{owner}/{project_name}")

    project_description = repo.description

    if project_description is None:
        read_me = repo.get_readme()
        project_description = export_project_description_from_readme(base64.b64decode(read_me.content))
        print("Project description of ", project_name, "DESCRIPTION: ", project_description)

    print(project_description)

projects = [
    "https://github.com/rpanic/vale-ui",
    "https://github.com/pico-labs/coinflip-executor-contract",
    "https://github.com/alysiahuggins/proof-of-ownership-zkapp",
    "https://github.com/sausage-dog/minanite",
    "https://github.com/iammadab/dark-chess",
    "https://github.com/gretzke/zkApp-data-types",
    "https://github.com/Sr-santi/mina-ui",
    "https://github.com/Trivo25/offchain-voting-poc",
    "https://github.com/gordonfreemanfree/snarkyjs-ml",
]

for project in projects:
    parts = project.strip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    test_description_extraction(owner, repo)

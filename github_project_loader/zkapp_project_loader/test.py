import re
import os
import base64

from github import Github
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv(), override=True) # read local .env file

def export_project_description_from_readme(content):
    decoded_content = bytes(str(content), "utf-8").decode("unicode_escape")
    cleaned_content = re.sub(r'# ', '', decoded_content)
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    cleaned_content = re.sub(r'```.*?```', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = emoji_pattern.sub(r'', cleaned_content)

    return cleaned_content[:1000]

def test_description_extraction(owner, project_name):
    token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

    g = Github(token)
    repo = g.get_repo(f"{owner}/{project_name}")

    project_description = repo.description

    if project_description is None:
        read_me = repo.get_readme()
        project_description = export_project_description_from_readme(base64.b64decode(read_me.content))
        print("Project description of ", project_name, "DESCRIPTION: ", project_description)

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

import os
import requests
import re
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

headers = {
    'Authorization': f'token {token}'
}

if not os.path.exists("files"):
    os.mkdir("files")

def snake_case(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()

# list of github repositories
repos = ["o1-labs/docs2",
        "MinaProtocol/mina"]

def get_files(contents, repo_name, dir_name):
    """
    Uses stack to get all files from a github repository
    """
    stack = [(contents, repo_name, dir_name)]

    while stack:
        current_contents, current_repo_name, current_dir_name = stack.pop()

        for content in current_contents:
            if content["type"] == "file":
                file_name = content["name"]
                download_url = content["download_url"]
                file_content = requests.get(download_url, headers=headers).text

                with open(f"files/{current_repo_name}/{current_dir_name}/{file_name}", "w") as f:
                    f.write(file_content)
                    
            elif content["type"] == "dir":
                sub_dir_name = content["name"]
                dir_contents_url = content["url"]
                dir_contents = requests.get(dir_contents_url, headers=headers).json()

                if not os.path.exists(f"files/{current_repo_name}/{current_dir_name}/{sub_dir_name}"):
                    os.mkdir(f"files/{current_repo_name}/{current_dir_name}/{sub_dir_name}")

                stack.append((dir_contents, current_repo_name, f"{current_dir_name}/{sub_dir_name}"))

book_repo = "o1-labs/proof-systems"
book_repo_name = book_repo.split("/")[-1]

book_contents_url = f"https://api.github.com/repos/{book_repo}/contents/book/src"
book_contents = requests.get(book_contents_url, headers=headers).json()

if not os.path.exists(f"files/{book_repo_name}"):
    os.mkdir(f"files/{book_repo_name}")

get_files(book_contents, "proof-systems", "")

for repo in repos:
    repo_name = repo.split("/")[-1]
    contents_url = f"https://api.github.com/repos/{repo}/contents/docs"
    contents = requests.get(contents_url, headers=headers).json()

    if not os.path.exists(f"files/{repo_name}"):
        os.mkdir(f"files/{repo_name}")

    get_files(contents, repo_name, "")


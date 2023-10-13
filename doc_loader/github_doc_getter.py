import os
import requests
import re
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

headers = {
    'Authorization': f'token {token}'
}

# create a directory named "files" if it does not exist
if not os.path.exists("files"):
    os.mkdir("files")

# function to convert string to snake case
def snake_case(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()

# list of github repositories
repos = ["o1-labs/docs2",
         "MinaProtocol/mina"]

# function to get files from a directory
def get_files(contents, repo_name, dir_name):
    stack = [(contents, repo_name, dir_name)]  # Initialize stack with initial directory

    while stack:
        current_contents, current_repo_name, current_dir_name = stack.pop()

        for content in current_contents:
            if content["type"] == "file":
                # get the file name
                file_name = content["name"]
                # get the file download url
                download_url = content["download_url"]
                # get the file content
                file_content = requests.get(download_url, headers=headers).text
                # write the file content to a file
                with open(f"files/{current_repo_name}/{current_dir_name}/{file_name}", "w") as f:
                    f.write(file_content)
            elif content["type"] == "dir":
                # get the directory name
                sub_dir_name = content["name"]
                # get the directory contents API url
                dir_contents_url = content["url"]
                # get the directory contents
                dir_contents = requests.get(dir_contents_url, headers=headers).json()
                # create a directory with the directory name
                if not os.path.exists(f"files/{current_repo_name}/{current_dir_name}/{sub_dir_name}"):
                    os.mkdir(f"files/{current_repo_name}/{current_dir_name}/{sub_dir_name}")
                # Add sub-directory to stack
                stack.append((dir_contents, current_repo_name, f"{current_dir_name}/{sub_dir_name}"))

# loop through each repository
for repo in repos:
    # get the repository name
    repo_name = repo.split("/")[-1]
    # get the repository contents API url
    contents_url = f"https://api.github.com/repos/{repo}/contents/docs"
    # get the contents of the repository
    contents = requests.get(contents_url, headers=headers).json()

    if not os.path.exists(f"files/{repo_name}"):
        os.mkdir(f"files/{repo_name}")

    get_files(contents, repo_name, "")

            



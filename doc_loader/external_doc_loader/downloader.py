import os
import requests
import re
import time
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from requests.exceptions import HTTPError

# Load environment variables
_ = load_dotenv(find_dotenv(), override=True)  # read local .env file

# Get GitHub access token from environment
token = os.getenv("GITHUB_ACCESS_TOKEN")
if not token:
    raise ValueError("GITHUB_ACCESS_TOKEN is not set in the environment.")

headers = {"Authorization": f"token {token}"}
rate_limit_delay = (
    1  # seconds to wait between GitHub API requests to avoid rate limiting
)

# Ensure a directory exists for the downloaded files
base_dir = Path("files")
base_dir.mkdir(exist_ok=True)


def snake_case(string):
    """
    Convert a string to snake_case.
    """
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()


# List of GitHub repositories
repos = ["proto-kit/website"]


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

                with open(
                    f"files/{current_repo_name}/{current_dir_name}/{file_name}", "w"
                ) as f:
                    f.write(file_content)

            elif content["type"] == "dir":
                sub_dir_name = content["name"]
                dir_contents_url = content["url"]
                dir_contents = requests.get(dir_contents_url, headers=headers).json()

                if not os.path.exists(
                    f"files/{current_repo_name}/{current_dir_name}/{sub_dir_name}"
                ):
                    os.mkdir(
                        f"files/{current_repo_name}/{current_dir_name}/{sub_dir_name}"
                    )

                stack.append(
                    (
                        dir_contents,
                        current_repo_name,
                        f"{current_dir_name}/{sub_dir_name}",
                    )
                )


with requests.Session() as session:
    session.headers.update(headers)

    for repo in repos:
        repo_name = repo.split("/")[-1]
        contents_url = f"https://api.github.com/repos/{repo}/contents/src/pages/docs?ref=feature/docs"

        try:
            contents = session.get(contents_url).json()
        except HTTPError as e:
            print(f"Failed to get contents of {contents_url}: {e}")
            continue

        repo_path = Path("files") / repo_name
        repo_path.mkdir(exist_ok=True)

        get_files(contents, repo_name, "")

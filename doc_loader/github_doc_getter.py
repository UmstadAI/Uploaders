import os
import requests
import re

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

# loop through each repository
for repo in repos:
    # get the repository name
    repo_name = repo.split("/")[-1]
    # get the repository contents API url
    contents_url = f"https://api.github.com/repos/{repo}/contents/docs"
    # get the contents of the repository
    contents = requests.get(contents_url).json()

    if not os.path.exists(f"files/{repo_name}"):
        os.mkdir(f"files/{repo_name}")

    # function to get files from a directory
    def get_files(_contents, repo_name, dir_name):
        # loop through each content
        for content in _contents:
            if content["type"] == "file":
                # get the file name
                file_name = content["name"]
                # get the file download url
                download_url = content["download_url"]
                # get the file content
                file_content = requests.get(download_url).text
                # write the file content to a file
                with open(f"files/{repo_name}/{dir_name}/{snake_case(file_name)}", "w") as f:
                    f.write(file_content)
            elif content["type"] == "dir":
                # get the directory name
                dir_name = content["name"]
                # get the directory contents API url
                dir_contents_url = content["url"]
                # get the directory contents
                dir_contents = requests.get(dir_contents_url).json()
                # create a directory with the directory name
                if not os.path.exists(f"files/{repo_name}/{dir_name}"):
                    os.mkdir(f"files/{repo_name}/{dir_name}")
                # loop through each directory content
                get_files(dir_contents, repo_name, dir_name)

    # loop through each content
    for content in contents:
        if content["type"] == "file":
            # get the file name
            file_name = content["name"]
            # get the file download url
            download_url = content["download_url"]
            # get the file content
            file_content = requests.get(download_url).text
            # write the file content to a file
            with open(f"files/{repo_name}/{snake_case(file_name)}", "w") as f:
                f.write(file_content)
        elif content["type"] == "dir":
            # get the directory name
            dir_name = content["name"]
            # get the directory contents API url
            dir_contents_url = content["url"]
            # get the directory contents
            dir_contents = requests.get(dir_contents_url).json()
            # create a directory with the directory name
            if not os.path.exists(f"files/{repo_name}/{dir_name}"):
                os.mkdir(f"files/{repo_name}/{dir_name}")
            # loop through each directory content
            get_files(dir_contents, repo_name, dir_name)

            



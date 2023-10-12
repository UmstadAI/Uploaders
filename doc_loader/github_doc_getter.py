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
    contents_url = f"https://api.github.com/repos/{repo}/contents"
    # get the contents of the repository
    contents = requests.get(contents_url).json()
    # loop through each content
    for content in contents:
        # check if the content is a directory and its name is "docs"
        if content["type"] == "dir" and content["name"] == "docs":
            



import glob
import os
import openai
import pinecone
import time
import re
import base64

from github import Github
from uuid import uuid4

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

metadata_fields = {
    'project_name',
    'project_description',
    'file_name_with_folder',
    'comments',
    'functions'
}

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

openai.api_key = os.getenv('OPENAI_API_KEY') or 'OPENAI_API_KEY'
pinecone_api_key = os.getenv('PINECONE_API_KEY') or 'YOUR_API_KEY'
pinecone_env = os.getenv('PINECONE_ENVIRONMENT') or "YOUR_ENV"

def project_loader(owner, project_name):
    g = Github(token)
    repo = g.get_repo(f"{owner}/{project_name}")

    base_dir = './projects/{project_name}'
    project_description = repo.description
    
    def export_project_description_from_readme(content):
        # TODO: Create a function which exports project description from readMe content
        pass

    if project_description is None:
        read_me = repo.get_readme()
        project_description = export_project_description_from_readme(base64.b64decode(read_me.content))

    loader = GenericLoader.from_filesystem(
        base_dir,
        glob="**/*",
        suffixes=[".ts", ".js", ".json"],
        parser=LanguageParser(),
    )

    docs = loader.load()

    model_name = 'text-embedding-ada-002'

project_loader("Sr-santi", "mina-ui")
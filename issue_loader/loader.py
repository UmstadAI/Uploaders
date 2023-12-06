import glob
import os
import openai
import pinecone
import time
import re
import json

from uuid import uuid4

from langchain.document_loaders import JSONLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY') or 'OPENAI_API_KEY'
pinecone_api_key = os.getenv('PINECONE_API_KEY') or 'YOUR_API_KEY'
pinecone_env = os.getenv('PINECONE_ENVIRONMENT') or "YOUR_ENV"

base_dir = "issues_json"

loader = GenericLoader.from_filesystem(
    base_dir,
    glob="**/*",
    suffixes=[".json"],
)

issues = loader.load()
print(issues)

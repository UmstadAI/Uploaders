import glob
import os
import openai
import pinecone
import time
import re
import json

from uuid import uuid4

from langchain.document_loaders import DirectoryLoader

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY') or 'OPENAI_API_KEY'
pinecone_api_key = os.getenv('PINECONE_API_KEY') or 'YOUR_API_KEY'
pinecone_env = os.getenv('PINECONE_ENVIRONMENT') or "YOUR_ENV"

base_dir = "./issues_json"

json_files = glob.glob(os.path.join(base_dir, '**/*.json'), recursive=True)

issues = []

for issue_path in json_files:
    with open(issue_path, 'r') as file:
        issue = file.read()
        issue = json.loads(issue)

        try:
            question = issue['full_question'] + issue['question']
            answer = issue['answer']
        except:
            continue

        issues.append({"question": question, "answer": answer})

print(len(issues))
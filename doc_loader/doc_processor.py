import glob
import os
import openai
import tiktoken
import pinecone
import json
import time
import requests
import numpy as np

from uuid import uuid4
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

base_dir = "./files"

"""
 __    _____    __    ____  ____  _  _  ___ 
(  )  (  _  )  /__\  (  _ \(_  _)( \( )/ __)
 )(__  )(_)(  /(__)\  )(_) )_)(_  )  (( (_-.
(____)(_____)(__)(__)(____/(____)(_)\_)\___/
"""


markdown_files = glob.glob(os.path.join(base_dir, '**/*.md'), recursive=True)
markdown_files += glob.glob(os.path.join(base_dir, '**/*.mdx'), recursive=True)

print(len(markdown_files))
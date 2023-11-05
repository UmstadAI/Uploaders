import glob
import os
import openai
import pinecone
import time

from uuid import uuid4
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, Language

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY') or 'OPENAI_API_KEY'
pinecone_api_key = os.getenv('PINECONE_API_KEY') or 'YOUR_API_KEY'
pinecone_env = os.getenv('PINECONE_ENVIRONMENT') or "YOUR_ENV"

path_tutorial_docs = "../../doc_loader/files/docs2/zkapps/tutorials"

files = os.listdir(path_tutorial_docs)

md_files = [file for file in os.listdir(path_tutorial_docs) if file.endswith(".md")]
docs = DirectoryLoader(path_tutorial_docs + "/", glob="**/*.md", loader_cls=TextLoader, show_progress=True).load()

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splitted_docs = [markdown_splitter.split_text(doc.page_content) for doc in docs]

print(md_header_splitted_docs[0])

# print(md_header_splitted_docs[0][1])
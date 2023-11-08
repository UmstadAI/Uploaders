import glob
import os

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)

base_dir = "./examples/src/examples"
loader = GenericLoader.from_filesystem(
    base_dir,
    glob="**/*",
    suffixes=[".ts", ".js"],
    parser=LanguageParser(),
)

docs = loader.load()

ts_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.TS, chunk_size=3000, chunk_overlap=150
)

splitted_docs = ts_splitter.split_documents(docs)

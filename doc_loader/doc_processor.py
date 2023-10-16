import glob
import os
import openai

from uuid import uuid4
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, Language


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

base_dir = "./files"


# LOADING

markdown_files = glob.glob(os.path.join(base_dir, '**/*.md'), recursive=True)
docs = [UnstructuredMarkdownLoader(f, mode = "single").load()[0] for f in markdown_files]

"""
 ____  _  _  ____  ____  ____  ____  __  __  ____  _  _  ____  ___ 
( ___)( \/ )(  _ \( ___)(  _ \(_  _)(  \/  )( ___)( \( )(_  _)/ __)
 )__)  )  (  )___/ )__)  )   / _)(_  )    (  )__)  )  (   )(  \__ \
(____)(_/\_)(__)  (____)(_)\_)(____)(_/\/\_)(____)(_)\_) (__) (___/
"""

"""

If you want to use MarkdownHeaderTextSplitter, use this code

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splitted_docs = [markdown_splitter.split_text(doc.page_content) for doc in docs]

If you want to use from_language, use this code

md_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN, chunk_size=60, chunk_overlap=0
)

md_docs = [md_splitter.create_documents([markdown_text.page_content]) for markdown_text in docs]
"""

# SPLITTING

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 400,
    chunk_overlap  = 100,
    is_separator_regex = False,
)

splitted_docs = text_splitter.split_documents(docs)

# EMBEDDING
model_name = 'text-embedding-ada-002'
texts = [c.page_content for c in splitted_docs]

openai.api_key = os.getenv('OPENAI_API_KEY') or 'OPENAI_API_KEY'
embeddings = openai.Embedding.create(
    input=texts,
    model=model_name,
)

embeds = [record['embedding'] for record in embeddings['data']]
print(embeds)
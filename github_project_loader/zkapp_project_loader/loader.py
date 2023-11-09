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
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

metadata_fields = {
    'project_name',
    'project_description',
    'file_name_with_folder',
    'comments'
}

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

openai.api_key = os.getenv('OPENAI_API_KEY') or 'OPENAI_API_KEY'
pinecone_api_key = os.getenv('PINECONE_API_KEY') or 'YOUR_API_KEY'
pinecone_env = os.getenv('PINECONE_ENVIRONMENT') or "YOUR_ENV"

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

index_name = 'zkappumstad-projects'

if index_name in pinecone.list_indexes():
    pinecone.delete_index(index_name)

pinecone.create_index(
    name=index_name,
    metric='dotproduct',
    dimension=1536
) 

time.sleep(5)

def project_loader(owner, project_name):
    g = Github(token)
    repo = g.get_repo(f"{owner}/{project_name}")

    base_dir = f'./projects/{project_name}'
    project_description = repo.description
    
    def export_project_description_from_readme(content):
        # TODO: Create a function which exports project description from readMe content
        pass

    if project_description is None:
        read_me = repo.get_readme()
        project_description = base64.b64decode(read_me.content)

    loader = GenericLoader.from_filesystem(
        base_dir,
        glob="**/*",
        suffixes=[".ts", ".js", ".json", "jsx", "tsx"],
        parser=LanguageParser(),
    )

    docs = loader.load()

    ts_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.TS, chunk_size=1200, chunk_overlap=200
    )

    docs = ts_splitter.split_documents(docs)

    model_name = 'text-embedding-ada-002'

    def extract_comments_from_ts_code(ts_code):
        comment_pattern = r'(\/\/[^\n]*|\/\*[\s\S]*?\*\/)'
        comments = re.findall(comment_pattern, ts_code)
        comments_string = ' '.join(comment.strip('/*').strip('*/').strip('//').strip() for comment in comments)

        return comments_string
    
    texts = []
    metadatas = []

    for doc in docs:
        metadata = [
            project_name,
            project_description,
            doc.metadata['source'],
            extract_comments_from_ts_code(doc.page_content),
        ]

        texts.append(doc.page_content)
        metadatas.append(" ".join(metadata))

    chunks = [texts[i:(i + 1000) if (i+1000) <  len(texts) else len(texts)] for i in range(0, len(texts), 1000)]
    embeds = []

    print("Have", len(chunks), "chunks")
    print("Last chunk has", len(chunks[-1]), "texts")

    for chunk, i in zip(chunks, range(len(chunks))):
        print("Chunk", i, "of", len(chunk))
        new_embeddings = openai.Embedding.create(
            input=chunk,
            model=model_name,
        )
        new_embeds = [record['embedding'] for record in new_embeddings['data']]
        embeds.extend(new_embeds)

    while not pinecone.describe_index(index_name).status['ready']:
            time.sleep(1)

    index = pinecone.Index(index_name)

    ids = [str(uuid4()) for _ in range(len(docs))]

    vectors = [(ids[i], embeds[i], {
        'text': docs[i].page_content, 
        'title': metadatas[i]
    }) for i in range(len(docs))]

    print(vectors[23])

    namespace = "zkappumstad-projects"
    for i in range(0, len(vectors), 100):
        batch = vectors[i:i+100]
        print("Upserting batch:", i)
        index.upsert(batch, namespace=namespace)

    print(index.describe_index_stats())


project_loader("Sr-santi", "mina-ui")
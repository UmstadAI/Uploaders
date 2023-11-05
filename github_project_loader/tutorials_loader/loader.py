import os

path_example_docs = "../../doc_loader/files/docs2/zkapps/tutorials"

files = os.listdir(path_example_docs)

md_files = [file for file in os.listdir(path_example_docs) if file.endswith(".md")]

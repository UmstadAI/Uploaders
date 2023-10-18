from langchain.document_loaders import GitbookLoader

gitbook_path = "https://docs.aurowallet.com"

loader = GitbookLoader(gitbook_path, load_all_paths=True)
all_pages_data = loader.load()

print(f"fetched {len(all_pages_data)} documents.")

for i in all_pages_data:
    print("\n", i)
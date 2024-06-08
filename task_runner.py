import subprocess


# not included getting files or downloading files! please get them before running this script
# cd doc_loader && python github_doc_getter.py
# cd utils && node index.js

commands = [
    "cd doc_loader && python doc_processor.py",
    "cd doc_loader && python gitbook_loader.py",
    "cd doc_loader/blog_loader && python scraper_loader.py",
    "cd github_project_loader/example_loader && python loader.py",
    "cd github_project_loader/tutorials_loader && python loader.py",
    "cd github_project_loader/zkapp_project_loader && python loader.py",
    "cd issue_loader && python loader.py",
    "cd deprecated_loader && python loader.py",
]

for cmd in commands:
    subprocess.run(cmd, shell=True)

import os
import requests
import re
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

headers = {
    'Authorization': f'token {token}'
}

def download_readme(url):
    api_url = re.sub(r'github.com', 'api.github.com/repos', url)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        readme_content = response.json().get('content', '')
        return readme_content
    else:
        print(f"Failed to download README from {api_url}")
        return None
    
urls = [
    "https://github.com/rhvall/MinaDevContainer/blob/Release/README.md",
    "https://github.com/airgap-it/airgap-coin-lib/blob/master/readme.md",
    "https://github.com/rloot/ZOK/blob/main/README.md",
    "https://github.com/orochi-network/zkDatabase/blob/main/README.md",
    "https://github.com/anomix-zk/anomix-network/blob/main/README.md",
    "https://github.com/EasyMina/easyMina/blob/main/README.md",
    "https://github.com/devarend/mina-playground/blob/develop/README.md",
]

if not os.path.exists(f"files/zkignite_docs"):
    os.mkdir(f"files/zkignite_docs")

for url in urls:
    readme = download_readme(url)
    if readme:
        file_name = url.split('/')[-3] + '_README.md'
        with open(f"files/{file_name}", 'w') as file:
            file.write(readme)
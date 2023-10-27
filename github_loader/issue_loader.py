import os
import requests

from langchain.document_loaders import GitHubIssuesLoader

token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

loader = GitHubIssuesLoader(
    repo="o1-labs/o1js",
    access_token=token,
    state="all",
    include_prs=False,
)

docs = loader.load()
issue_links = [link.metadata['url'] for link in docs]

def get_github_issue_and_comments(issue_link):
    # Extract the owner, repository, and issue number from the provided link
    parts = issue_link.strip('/').split('/')
    owner, repo, issue_number = parts[-4], parts[-3], parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    response = requests.get(api_url)

    if response.status_code == 200:
        issue_data = response.json()
        comments_url = issue_data['comments_url']
        
        comments_response = requests.get(comments_url)
        
        if comments_response.status_code == 200:
            comments_data = comments_response.json()
            return issue_data, comments_data
        else:
            return None, f"Error fetching comments. Status code: {comments_response.status_code}"
    else:
        return None, f"Error fetching issue. Status code: {response.status_code}"


for link in issue_links:
    issue_data, comments_data = get_github_issue_and_comments(link)

    issue_number = issue_data['number']
    issue_title = issue_data['title']
    issue_writer = issue_data['user']['login']
    is_issue_open = issue_data['state'] == 'open'
    issue_body = issue_data['body']

    comments = []
    for comment in comments_data:
        comment_writer = comment['user']['login']
        comment_body = comment['body']
        comment_reactions = comment['reactions'].pop('url', None)
        comments.append((comment_writer, comment_body, comment_reactions))
    
    print(comments[0])

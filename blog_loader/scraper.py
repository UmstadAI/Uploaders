import requests
from bs4 import BeautifulSoup

def get_blog_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = soup.find_all('a', href=True)
    blog_links = [link['href'] for link in links if 'blog/' in link['href'] 
                  and 'page' not in link['href'] 
                  and '?by' not in link['href']
                  and '?cat' not in link['href']
                  and '?date' not in link['href']]
    return blog_links

blogs = []
for page in range(1, 18):
    main_blog_url = f'https://minaprotocol.com/blog/page/{page}'
    blog_links = get_blog_links(main_blog_url)

    blogs.extend(blog_links)



import requests
from bs4 import BeautifulSoup
from collections import deque

def get_urls(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")    
    return [f"https://en.wikipedia.org{a["href"]}"
            for a in soup.select("p > a") if "href" in a.attrs and a["href"].startswith("/wiki")]

def bfs(start_url: str, goal_url: str):
    queue = deque()
    queue.append(start_url)

    visited = {start_url : None}
    while queue:
        url = queue.popleft()
        if url == goal_url:
            break
        children = get_urls(url)
        for child in children:
            if child not in visited:
                visited[child] = url
                queue.append(child)

    chain = []
    parent = goal_url
    while parent is not None:
        chain.append(parent)
        parent = visited[parent]
    return reversed(chain)

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Operator-precedence_parser" 
    goal_url = "https://en.wikipedia.org/wiki/Formal_language"
    chain = bfs(start_url, goal_url)
    for url in chain:
        print(url)

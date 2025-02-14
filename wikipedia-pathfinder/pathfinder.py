import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from collections import deque

async def get_urls(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")    
        return (url, 
                [f"https://en.wikipedia.org{a["href"]}" 
                 for a in soup.select("p > a") if "href" in a.attrs and a["href"].startswith("/wiki")])

def recover_path(visited: dict, start_url: str, goal_url: str):
    path = []
    parent = goal_url
    while parent is not None:
        path.append(parent)
        parent = visited[parent]
    path.reverse()
    return path


async def bfs(start_url: str, goal_url: str):
    async with aiohttp.ClientSession() as session:
        queue = deque()
        queue.append(start_url)
        visited = {start_url : None}

        if start_url == goal_url:
            return [start_url]

        while queue:
            # Get next layer of URLs
            batch_size = 20 # Choose how many tasks to await at once
            size = 0
            tasks = []
            while queue and size <= batch_size:
                tasks.append(get_urls(session, queue.popleft()))
                size += 1

            layer = await asyncio.gather(*tasks)
            for node in layer:
                parent, children = node
                for child in children:
                    if child in visited:
                        continue
                    visited[child] = parent
                    queue.append(child)
                    if child == goal_url:
                        return recover_path(visited, start_url, goal_url)
        return None

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Harry_Potter" 
    goal_url = "https://en.wikipedia.org/wiki/Banana"

    start = time.process_time()
    path = asyncio.run(bfs(start_url, goal_url))
    stop = time.process_time()

    if path:
        for url in path:
            print(url)
    else:
        print("No path exists.")
    print(f"Time: {round(stop-start, 3)}s")
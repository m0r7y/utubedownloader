import subprocess
import sys
import asyncio
from arsenic import get_session, Session
from arsenic.browsers import Firefox
from arsenic.services import Geckodriver
from urllib.parse import urlencode, urljoin
from typing import Type, List

YOUTUBE_URL_SEARCH = 'https://www.youtube.com/results?'
YOUTUBE_URL_WATCH = 'https://www.youtube.com/watch?'
CMD = 'youtube-dl.exe -f best -x --audio-format mp3 -i'


async def fetch_all(s: Type[Session], titles: List[str]) -> None:
    tasks = [asyncio.create_task(download_title(s, title)) for title in titles]
    await asyncio.gather(*tasks)


async def get_url_title(s: Type[Session], title: str) -> str:
    query_string = f'{YOUTUBE_URL_SEARCH}{urlencode({"search_query": title})}'
    await s.get(query_string)
    content_el = await s.wait_for_element(5, '#primary')
    links_el = await content_el.get_elements('#video-title')
    return [await link.get_attribute('href') for link in links_el][0]  # return first watch link


async def download_title(s: Type[Session], title: str) -> None:
    watch_url = await get_url_title(s, title)
    full_watch_url = urljoin(YOUTUBE_URL_WATCH, watch_url)
    subprocess.Popen(f'{CMD} {full_watch_url}', shell=True)


async def main() -> None:
    if len(sys.argv) < 2:
        raise Exception("Please provide file name")

    with open(sys.argv[1], 'r') as file:
        titles = file.read().splitlines()
        async with get_session(Geckodriver(), Firefox()) as session:
            await fetch_all(session, titles)


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

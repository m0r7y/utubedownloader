import unittest
from main import get_url_title
from arsenic import get_session
from arsenic.browsers import Firefox
from arsenic.services import Geckodriver


class TestDownloader(unittest.IsolatedAsyncioTestCase):
    async def test_downloader(self):
        async with get_session(Geckodriver(), Firefox()) as session:
            self.assertEqual(await get_url_title(session, 'Lil Nas X - STAR WALKIN'), '/watch?v=HYsz1hP0BFo')


if __name__ == '_main__':
    unittest.main()

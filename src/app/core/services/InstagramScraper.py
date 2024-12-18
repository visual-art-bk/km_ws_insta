import asyncio
import time
from playwright.async_api import async_playwright
from .PlayWrightBrowser import PlayWrightBrowser
from app.core.utils.Logger import Logger

logger = Logger(name="InstagramScraper", log_file="InstagramScraper.log", max_files=5)


class InstagramScraper(PlayWrightBrowser):
    def __init__(self, playwright):
        super().__init__(playwright)

    async def signin(self, username, password):
        try:
            await self.page.get_by_label("전화번호, 사용자 이름 또는 이메일").fill(
                username
            )

            await self.page.get_by_label("비밀번호").fill(password)

            await self.page.wait_for_timeout(timeout=1500)

            await self.page.get_by_role("button", name="로그인", exact=True).click()

        except Exception as e:
            logger.log_exception(message="인스타그램 로그인 시도", obj=e)

    async def start_scraping(self, url):
        print("테스트성공")
        time.sleep(100)

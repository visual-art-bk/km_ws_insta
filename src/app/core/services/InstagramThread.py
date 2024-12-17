import asyncio
import time
import sys
import traceback
import datetime
from PySide6 import QtWidgets, QtGui, QtCore
from playwright.async_api import async_playwright
from .InstagramScraper import InstagramScraper
from .PlayWrightBrowser import PlayWrightBrowser


class InstagramThread(QtCore.QThread):
    update_status = QtCore.Signal(str)
    update_progress = QtCore.Signal(int)
    error_occurred = QtCore.Signal(str, str)
    finished = QtCore.Signal()

    def __init__(
        self,
        max_scraping_size,
        password,
        username="kekekj0509",
    ):
        super().__init__()
        self.url = "https://www.instagram.com/"
        self.max_scraping_size = max_scraping_size
        self.results = []
        self._username = username
        self._password = password

    async def async_run(self):

        try:
            async with async_playwright() as playwright:

                insta_scraper = InstagramScraper(playwright=playwright)

                await insta_scraper.init(
                    headless=False,
                )

                await insta_scraper.goto(self.url)

                await insta_scraper.signin(
                    username=self._username, password=self._password
                )

                await asyncio.sleep(30)

                # plbw = PlayWrightBrowser(playwright=playwright)

                # await plbw.init(headless=False, proxy=None)

                # browser = await plbw._playwright.chromium.launch(headless=False)
                # context = await plbw.browser.new_context()
                # page = await plbw.context.new_page()

                # await plbw.page.goto(url, timeout=1000000)

                await asyncio.sleep(1)
                # async with InstagramScraper(
                #     headless=False, playwright=playwright, proxy=None
                # ) as insta_scraper:

                #     await insta_scraper.goto(url="https://www.instagram.com/")
                #     self.update_status.emit('인스타그램에 접속')

                # browser = await playwright.chromium.launch(headless=False)
                # context = await browser.new_context()
                # page = await context.new_page()

                # self.update_status.emit(f"접속 중: {self.url}")

                # await page.goto(self.url)

                # self.update_status.emit(f"페이지 로드 완료: {self.url}")
                # time.sleep(10)

                # # 크롤링 로직
                # for i in range(self.max_scraping_size):
                #     try:
                #         await page.wait_for_selector('div.event', timeout=5000)
                #         events = await page.query_selector_all('div.event')

                #         if len(events) > i:
                #             event_text = await events[i].inner_text()
                #             self.results.append(event_text)
                #             self.update_progress.emit(len(self.results))
                #         else:
                #             break
                #     except Exception as e:
                #         await self.update_status.emit(f"데이터 수집 중 오류 발생: {e}")
                #         break

                # await browser.close()
                self.finished.emit()

        except Exception as e:
            error_trace = traceback.format_exc()
            self.error_occurred.emit("크롤링 중 오류 발생", error_trace)

    def run(self):
        # asyncio.run을 사용하여 async 메서드 실행
        try:
            asyncio.run(self.async_run())
        except Exception as e:
            error_trace = traceback.format_exc()
            self.error_occurred.emit("비동기 실행 중 오류 발생", error_trace)

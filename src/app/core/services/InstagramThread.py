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

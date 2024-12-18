import time
import sys
import traceback
import datetime
from PySide6 import QtWidgets, QtGui, QtCore
from playwright.async_api import async_playwright
from app.core.services.InstagramScraper import InstagramScraper


class CrawlerThread(QtCore.QThread):
    update_status = QtCore.Signal(str)
    update_result = QtCore.Signal(str)
    update_progress = QtCore.Signal(int)  # 크롤링된 브랜드 수 전달
    error_occurred = QtCore.Signal(str, str)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.results = []
        self.scraper = None
        self.kipris_scraper = None
        self.max_scraping_size = 50  # 기본값 설정

    async def async_run(self):
        async with async_playwright() as pw:
            async with InstagramScraper(playwright=pw) as yt_scraper:
                yt_scraper.scrap(url="https://www.youtube.com/")

    async def run(self):
        try:
            # max_scroll_attempts를 max_scraping_size의 비율에 따라 계산
            max_scroll_attempts = max(5, self.max_scraping_size // 10)

            await self.async_run()

            self.results = []

        except Exception as e:
            error_trace = traceback.format_exc()
            self.error_occurred.emit("알 수 없는 오류 발생.", error_trace)

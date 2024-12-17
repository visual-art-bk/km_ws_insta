import os
from pathlib import Path
import playwright
from playwright.async_api import Playwright, async_playwright
from playwright._impl._errors import Error, TimeoutError
from app.core.utils.Logger import Logger

logger = Logger(name="PlayWrightBrowser", log_file="PlayWrightBrowser.log", max_files=5)


class PlayWrightBrowser:
    def __init__(self, playwright: Playwright) -> None:

        self._playwright = playwright

        self.browser = None
        self.context = None
        self.page = None

    async def init(self, headless=False, proxy=None):
        if not playwright:
            self._playwright = async_playwright().start()

        browser_options = PlayWrightBrowser._get_browser_options(
            headless=headless, proxy=proxy
        )

        self.browser = await self._playwright.chromium.launch(**browser_options)

        self.context = await self.browser.new_context()

        # TODO 3042 - list로 막힐 시 여러 헤더스 설정을 돌면서 우회하게끔
        await self.context.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Safari/537.36"
            }
        )

        self.page = await self.context.new_page()

        await self.page.add_init_script(
            """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                """
        )

    async def __aexit__(self, exc_type, exc_value, traceback):
        import traceback as tb

        if exc_type:
            print(f"예외 발생: {exc_type.__name__}, {exc_value}")
            print("스택 추적 정보:")
            tb.print_tb(traceback)

        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def goto(self, url: str, timeout: int = 10000):
        try:
            await self.page.goto(url, timeout=timeout)
            return True
            # 사용자 행동 모방
            # await self.page.mouse.move(100, 200)  # 마우스 움직임 추가
            # await asyncio.sleep(0.5)  # 적절한 지연 추가

        except TimeoutError:
            self._log(f"페이지 로드 타임아웃: {url}")
        except Error as e:
            if "net::ERR_CONNECTION_RESET" in str(e):
                self._log(f"네트워크 연결이 끊겼습니다: {url}")
            elif "net::ERR_NAME_NOT_RESOLVED" in str(e):
                self._log(f"DNS 문제로 사이트를 찾을 수 없습니다: {url}")
            elif "net::ERR_TIMED_OUT" in str(e):
                self._log(f"네트워크 요청 시간이 초과되었습니다: {url}")
            else:
                self._log(f"Playwright 관련 오류: {str(e)}")
        except Exception as e:
            self._log(f"알 수 없는 오류 발생: {e}")

        return False

    @staticmethod
    def _get_browser_options(headless=False, proxy=None):
        try:
            options = {
                "args": [
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--disable-dev-shm-usage",
                    "--disable-extensions",
                ],
            }

            if headless == "new":
                options["executable_path"] = (
                    PlayWrightBrowser._get_headless_new_exec_path()
                )

                logger.get_logger().info("headless=new 모드로 전환\n")
                logger.get_logger().info(f"크롬exe path: {options["executable_path"]}")
            else:
                options["headless"] = headless

            if proxy != None:
                options["proxy"] = proxy

            return options

        except Exception as e:
            err_msg = f"driver의 browser options을 초기화 중 예외발생! {e}\n"
            PlayWrightBrowser._log(err_msg=err_msg)
            raise

    @staticmethod
    def _get_headless_new_exec_path():
        user_name = os.getlogin()

        # Playwright 브라우저 기본 설치 경로
        drivers_path = (
            Path(f"C:\\Users\\{user_name}\\AppData\\Local\\ms-playwright")
            / "chromium_headless_shell-1148"
            / "chrome-win"
        )

        # 브라우저 실행 파일 경로 설정
        browser_path = drivers_path / "headless_shell.exe"

        # 브라우저 파일이 존재하지 않을 경우 예외 처리
        if not browser_path.exists():
            err_msg = (
                f"[오류] Playwright 브라우저 실행 파일을 찾을 수 없습니다.\n"
                f"현재 경로: {browser_path}"
            )
            PlayWrightBrowser._log(err_msg=err_msg)
            raise FileNotFoundError(err_msg)

        return str(browser_path)

    @staticmethod
    def _log(err_msg="예외!"):
        import traceback as tb
        import os

        print(err_msg)

        tb.print_exc()

        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)

        with open(f"{log_folder}/error.log", "w", encoding="utf-8") as f:
            f.write(err_msg + "\n")

            tb.print_exc(file=f)

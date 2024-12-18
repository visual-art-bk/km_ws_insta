import sys
import traceback
import datetime
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QVBoxLayout
from app.ui.styles import window_appearance as win_appear
from app.ui.widgets.status_textedit import StatusTextEdit
from app.ui.widgets.input_field import InputField, PasswordField
from app.ui.widgets.boxes import ScrapingSizeSpinBox
from app.ui.widgets.buttons import WindowControls, CustomButton
from app.ui.utils.ui_logger import log_status, log_error_to_ui
from app.core.services.CrawlerThread import CrawlerThread
from app.core.utils.FileMaker import FileMaker
from app.core.services.InstagramThread import InstagramThread


# --- 상수 설정 ---
class Config:
    START_TIME = datetime.datetime(2024, 12, 10, 9, 0)
    LIMIT_TIME = datetime.timedelta(minutes=60 * 24 * 7)
    MAX_TITLES = 5


# --- UI 클래스 ---
class MainWindow(QtWidgets.QWidget):
    def paintEvent(self, event):
        """둥근 모서리 배경 그리기"""
        win_appear.paint_rounded_background(self, event, radius=30)

    def resizeEvent(self, event):
        """리사이즈 시 둥근 모서리 재적용"""
        win_appear.apply_rounded_corners(self, radius=30)

    @staticmethod
    def _scale_window_size(scale):
        width = 430
        height = 932
        return (int(width * scale), int(height * scale))

    def __init__(self):
        super().__init__()
        self.crawler_thread = None
        self.initUI()

    # --- UI 초기화 ---
    def initUI(self):
        self.setWindowTitle("크롤링 앱")
        layout = QtWidgets.QVBoxLayout()

        self._set_ui_appearance()
        self._set_ui_window_controls(layout)
        self._set_ui_status(layout)
        self._set_ui_signin(layout)
        self._set_ui_scraping_size(layout)
        self._set_ui_buttons(layout)
        self._set_ui_printout_result(layout)

        self.setLayout(layout)

    def _set_ui_appearance(self):
        size = MainWindow._scale_window_size(0.85)
        self.setFixedSize(*size)  # 고정 크기 설정

        win_appear.set_translucent_background(self)
        win_appear.apply_drop_shadow(self)

    def _set_ui_window_controls(self, layout: QVBoxLayout):
        self.window_controls = WindowControls(self)
        self.window_controls.add_to_main_layout(layout)

    def _set_ui_status(self, layout: QVBoxLayout):
        # 상태 로그
        self.status_label = StatusTextEdit("크롤링이 대기 중이에요")
        layout.addWidget(self.status_label)

    def _set_ui_signin(self, layout: QVBoxLayout):
        self.username_input = InputField("인스타그램 사용자 이름")
        self.password_input = PasswordField("인스타그램 비밀번호")

        layout.addWidget(QtWidgets.QLabel("사용자 이름:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QtWidgets.QLabel("비밀번호:"))
        layout.addWidget(self.password_input)

    def _set_ui_scraping_size(self, layout: QVBoxLayout):
        self.scraping_size_input = ScrapingSizeSpinBox(
            default_val=50, min_val=10, max_val=500
        )

        layout.addWidget(QtWidgets.QLabel("최대 크롤링 개수:"))
        layout.addWidget(self.scraping_size_input)

    def _set_ui_buttons(self, layout: QVBoxLayout):
        self.start_button = CustomButton("크롤링 시작", self.start_crawling)
        self.save_button = CustomButton(
            "엑셀로 저장", self.save_results_to_file, enabled=False
        )
        layout.addWidget(self.start_button)
        layout.addWidget(self.save_button)

    def _set_ui_printout_result(self, layout: QVBoxLayout):
        self.result_text = self.create_readonly_textedit("")

        layout.addWidget(self.result_text)

    def create_readonly_textedit(self, initial_text):
        text_edit = QtWidgets.QTextEdit(initial_text)
        text_edit.setReadOnly(True)
        return text_edit

    # --- 크롤링 시작 ---
    def start_crawling(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        max_scraping_size = self.scraping_size_input.value()

        if not username or not password:
            log_status("사용자 이름과 비밀번호를 모두 입력해주세요.")
            return

        self.crawler_thread = InstagramThread(
            max_scraping_size=max_scraping_size, username=username, password=password
        )

        # 연결 설정
        self.crawler_thread.update_status.connect(
            lambda msg: log_status(self.status_label, msg)
        )
        self.crawler_thread.update_progress.connect(self.update_progress)
        self.crawler_thread.error_occurred.connect(self.handle_thread_error)
        self.crawler_thread.finished.connect(self.handle_crawling_complete)

        self.crawler_thread.start()
        log_status(self.status_label, "크롤링 시작...")

    # --- 프로그래스 업데이트 ---
    def update_progress(self, count):
        log_status(self.status_label, f"수집된 데이터: {count}개")

    # --- 완료 처리 ---
    def handle_crawling_complete(self):
        self.save_button.setEnabled(True)
        log_status(self.status_label, "크롤링이 완료되었습니다!")

    # --- 결과 저장 ---
    def save_results_to_file(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "엑셀로 결과물 저장", "", "Excel Files (*.xlsx);;All Files (*)"
        )

        if file_path:
            try:
                FileMaker.save_to_excel_for_musinsa(
                    fixed_columns=["이벤트 내용"],
                    file_name=file_path,
                    infos_list=self.crawler_thread.results,
                )
                log_status(self.status_label, f"결과물이 {file_path}에 저장되었습니다.")

            except Exception:
                log_error_to_ui(
                    self.status_label, "엑셀 파일 저장 실패", traceback.format_exc()
                )

    # --- 오류 처리 ---
    def handle_thread_error(self, message):
        log_error_to_ui(self.result_text, message)

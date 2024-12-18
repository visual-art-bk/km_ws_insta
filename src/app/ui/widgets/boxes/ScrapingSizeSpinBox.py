from PySide6.QtWidgets import QSpinBox


class ScrapingSizeSpinBox(QSpinBox):
    def __init__(self, min_val=1, max_val=500, default_val=50, parent=None):
        """
        크롤링 사이즈 설정을 위한 커스텀 QSpinBox.

        Args:
            min_val (int): 최소값
            max_val (int): 최대값
            default_val (int): 기본값
            parent: 부모 위젯 (옵션)
        """
        super().__init__(parent)
        self.setRange(min_val, max_val)
        self.setValue(default_val)
        self.setup_ui()

    def setup_ui(self):
        """UI 설정 (필요에 따라 커스터마이징)."""
        self.setSuffix(" 개")  # 값 뒤에 '개'라는 텍스트를 붙임
        self.setSingleStep(10)  # 한 번에 증가/감소하는 스텝 크기

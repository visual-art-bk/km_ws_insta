from PySide6.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(self, text, callback, enabled=True):
        super().__init__(text)
        self.clicked.connect(callback)
        self.setEnabled(enabled)

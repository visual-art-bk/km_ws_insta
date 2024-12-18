from PySide6.QtWidgets import QTextEdit


class StatusTextEdit(QTextEdit):
    def __init__(self, initial_text=""):
        super().__init__(initial_text)
        self.setReadOnly(True)

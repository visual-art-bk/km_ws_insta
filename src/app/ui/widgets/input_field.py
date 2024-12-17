from PySide6.QtWidgets import QLineEdit

class InputField(QLineEdit):
    def __init__(self, placeholder):
        super().__init__()
        self.setPlaceholderText(placeholder)


class PasswordField(InputField):
    def __init__(self, placeholder):
        super().__init__(placeholder)
        self.setEchoMode(QLineEdit.Password)

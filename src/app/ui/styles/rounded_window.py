from PySide6 import QtCore, QtGui, QtWidgets

def set_translucent_background(widget: QtWidgets.QWidget):
    """위젯에 투명한 배경을 설정하는 함수"""
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 투명 배경
    widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)     # 프레임 비활성화

def apply_rounded_corners(widget: QtWidgets.QWidget, radius=30):
    """위젯에 둥근 모서리를 적용하는 함수"""
    path = QtGui.QPainterPath()
    rect = QtCore.QRectF(widget.rect())
    path.addRoundedRect(rect, radius, radius)
    region = QtGui.QRegion(path.toFillPolygon().toPolygon())
    widget.setMask(region)

def paint_rounded_background(widget, event, color=QtGui.QColor(240, 240, 240), radius=30):
    """위젯의 배경을 둥글게 그리고 배경 색상을 설정하는 함수"""
    painter = QtGui.QPainter(widget)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    painter.setBrush(color)  # 배경색
    painter.setPen(QtCore.Qt.NoPen)  # 테두리 없애기
    rect = widget.rect()
    painter.drawRoundedRect(rect, radius, radius)

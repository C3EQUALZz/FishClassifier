from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from app.core.enums import ButtonStateColor, IconStateColors
from app.core.utils import IconDrawer, ToolTip, ButtonParameters

STYLE_TOOLTIP = """ 
QLabel {		
	background-color: #0b0b0c;	
	color: rgb(230, 230, 230);
	padding-left: 10px;
	padding-right: 10px;
	border-radius: 17px;
    border: 1px solid #2f3032;
    border-left: 3px solid #bdff00;
    font: 800 9pt "Segoe UI";
}
"""


class LeftMenuButton(QWidget):
    """
    Левое меню в приложении
    """
    clicked = Signal()
    released = Signal()

    def __init__(self, parent: QMainWindow, name: str, icon: str, tooltip: str) -> None:
        super().__init__()
        self.parent = parent

        # DEFAULT PARAMETERS
        self.parameters = ButtonParameters()
        self.setGeometry(self.parameters.pos_x, self.parameters.pos_y, self.parameters.width, self.parameters.height)
        self.setMinimumSize(self.parameters.width, self.parameters.height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName(name)

        # BG COLORS
        self.button_current_color = ButtonStateColor.DEFAULT.value

        # ICON
        self.icon_current_path = Path.cwd() / icon
        self.icon_current_color = IconStateColors.DEFAULT.value

        # TOOLTIP
        self.tooltip = ToolTip(parent, tooltip, STYLE_TOOLTIP)
        self.tooltip.hide()

    # PAINT EVENT
    # Responsible for painting the button, as well as the icon
    def paintEvent(self, event):
        # PAINTER
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        # BRUSH
        brush = QBrush(self.button_current_color)

        # CREATE RECTANGLE
        rect = QRect(0, 0, self.parameters.width, self.parameters.height)
        paint.setPen(Qt.PenStyle.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(rect, self.parameters.border_radius, self.parameters.border_radius)

        # DRAW ICONS
        IconDrawer(
            painter=paint,
            svg_file=self.icon_current_path,
            rect=rect
        ).draw()

        # END PAINTER
        paint.end()

    def enterEvent(self, event: QEvent) -> None:
        """
        Событие срабатывает, когда мышь попадает в область кнопок.

        :param event: Объект QEvent, содержащий информацию о событии.
        """
        self.__change_style(QEvent.Type.Enter)
        self.__move_tooltip()
        self.tooltip.show()

    def leaveEvent(self, event: QEvent) -> None:
        """
        Событие срабатывает, когда мышь покидает область кнопок.

        :param event: Объект QEvent, содержащий информацию о событии.
        """
        self.__change_style(QEvent.Type.Leave)
        self.__move_tooltip()
        self.tooltip.hide()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Событие срабатывает при нажатии кнопки мыши.

        :param event: Объект QMouseEvent, содержащий информацию о событии.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.__change_style(QEvent.Type.MouseButtonPress)
            self.clicked.emit()
            self.setFocus()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Событие срабатывает при отпускании кнопки мыши.

        :param event: Объект QMouseEvent, содержащий информацию о событии.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.__change_style(QEvent.Type.MouseButtonRelease)
            self.released.emit()

    def __repaint_button(self, event: QEvent.Type) -> None:
        """
        При определенных event должна быть перерисовка
        :param event: QEvent. Type, который прилетает от приложения
        :return: ничего не возвращает
        """
        suitable_events = (
            QEvent.Type.Enter,
            QEvent.Type.Leave,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.MouseButtonRelease
        )

        if event in suitable_events:
            self.repaint()

    def __move_tooltip(self) -> None:
        """
        Перемещает всплывающую подсказку на соответствующую позицию.

        Этот метод вычисляет позицию всплывающей подсказки на основе позиции родительского виджета и его размеров.
        Затем он перемещает всплывающую подсказку на вычисленную позицию.
        """
        global_pos = self.mapToGlobal(QPoint(0, 0))

        local_pos = self.parent.mapFromGlobal(global_pos)

        tooltip_pos_x = local_pos.x() + self.parameters.width + 12
        tooltip_pos_y = local_pos.y() + (self.parameters.width - self.tooltip.height()) // 2

        self.tooltip.move(tooltip_pos_x, tooltip_pos_y)

    def __change_style(self, event_type: QEvent.Type) -> None:
        """
        Изменяет стиль кнопки в зависимости от события.

        Args:
            event_type: Тип события, которое произошло.
        """
        match event_type:
            case QEvent.Type.Enter:
                self.button_current_color = ButtonStateColor.HOVER.value
            case QEvent.Type.Leave:
                self.button_current_color = ButtonStateColor.DEFAULT.value
            case QEvent.Type.MouseButtonPress:
                self.button_current_color = ButtonStateColor.PRESSED.value
                self.icon_current_color = IconStateColors.PRESSED.value
            case QEvent.Type.MouseButtonRelease:
                self.button_current_color = ButtonStateColor.HOVER.value
                self.icon_current_color = IconStateColors.DEFAULT.value

        self.__repaint_button(event_type)

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import app.modules.app_settings as app_setting_namespace
import app.core.widgets.top_user_box.helpers as top_user_box_helpers_namespace
import logging
import os

logger = logging.getLogger(__name__)


# TOP USER BOX
# Top box with name, description and status
# ///////////////////////////////////////////////////////////////
class TopUserInfo(QWidget):
    status = Signal(str)

    def __init__(self, parent, left, top, my_name, my_description, *args, **kwargs):
        # ICON PATH
        # ///////////////////////////////////////////////////////////////
        super().__init__(parent, *args, **kwargs)
        self.parent_widget = parent
        settings = app_setting_namespace.Settings()

        image = settings["top_user_box"]["image"]
        icon_settings = settings["top_user_box"]["icon_settings"]

        # INITIAL SETUP
        # ///////////////////////////////////////////////////////////////
        self.setGeometry(0, 0, 240, 60)
        self.setObjectName("top_text_box")
        self.setStyleSheet("#top_text_box { background-color: #F00000 }")

        # CUSTOM PARAMETERS
        # ///////////////////////////////////////////////////////////////
        self.user_name = my_name
        self.user_description = my_description
        self.user_status = "online"
        self.user_image = os.path.join(os.path.abspath(os.getcwd()), image)
        self.icon_settings = QPixmap(icon_settings)
        self.status_color = "#46b946"

        # DRAW BASE FRAME
        # ///////////////////////////////////////////////////////////////
        self.setup_ui()

        # IMAGE FRAME EVENTS
        # ///////////////////////////////////////////////////////////////
        self.user_overlay.mousePressEvent = self.mouse_press
        self.user_overlay.enterEvent = self.mouse_enter
        self.user_overlay.leaveEvent = self.mouse_leave

        # SETUP STATUS BOX
        # ///////////////////////////////////////////////////////////////
        self.status_box = top_user_box_helpers_namespace.StatusBox(self)
        self.status_box.move(left, top)

    # OPEN STATUS BOX POPUP
    # ///////////////////////////////////////////////////////////////
    def mouse_press(self, event):
        if self.status_box.status_box.isVisible():
            self.status_box.status_box.hide()
            self.status_box.status_box.line_edit.setText("")
        else:
            self.status_box.status_box.show()
            self.status_box.status_box.line_edit.setFocus()

    # SHOW ICON
    # ///////////////////////////////////////////////////////////////
    def mouse_enter(self, event):
        self.user_overlay.setPixmap(self.icon_settings)

    # HIDE ICON
    # ///////////////////////////////////////////////////////////////
    def mouse_leave(self, event):
        self.user_overlay.setPixmap(QPixmap())

    # SETUP WIDGETS
    # ///////////////////////////////////////////////////////////////
    def setup_ui(self):
        # LAYOUT AND BORDER
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 0)
        self.border = QFrame(self)
        self.layout.addWidget(self.border)

        # FRAME IMAGE
        self.user_overlay = QLabel(self.border)
        self.user_overlay.setGeometry(0, 5, 40, 40)
        self.user_overlay.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.user_overlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        opacity = QGraphicsOpacityEffect(self)
        opacity.setOpacity(0.75)
        self.user_overlay.setGraphicsEffect(opacity)

        # FRAME TEXT
        self.text_frame = QFrame(self.border)
        self.text_frame.setGeometry(50, 0, 170, 50)

        # USER NAME
        self.label_user = QLabel(self.text_frame)
        self.label_user.setGeometry(0, 8, self.text_frame.width(), 20)
        self.label_user.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label_user.setText(self.user_name.capitalize())
        self.label_user.setStyleSheet("color: #bdff00; font: 700 10pt 'Segoe UI';")

        # USER STATUS
        self.label_description = QLabel(self.text_frame)
        self.label_description.setGeometry(0, 22, self.text_frame.width(), 18)
        self.label_description.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label_description.setText(self.user_description)
        self.label_description.setStyleSheet("color: #A6A6A6; font: 9pt 'Segoe UI';")

    # PAINT USER IMAGE EVENTS
    # ///////////////////////////////////////////////////////////////
    def paintEvent(self, event):
        # PAINTER USER IMAGE
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # RECT
        rect = QRect(10, 15, 40, 40)

        # CIRCLE
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#000000")))
        painter.drawEllipse(rect)

        # DRAW USER IMAGE
        self.draw_user_image(painter, self.user_image, rect)

        # PAINT END
        painter.end()

        # DRAW USER IMAGE
        self.draw_status(self.user_image, rect)

    # DRAW USER IMAGE
    # ///////////////////////////////////////////////////////////////
    def draw_user_image(self, qp, image, rect):
        user_image = QImage(image)
        path = QPainterPath()
        path.addEllipse(rect)
        qp.setClipPath(path)
        qp.drawImage(rect, user_image)

    # DRAW STATUS
    # ///////////////////////////////////////////////////////////////
    def draw_status(self, status, rect):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # PEN
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("#151617"))
        painter.setPen(pen)

        # BRUSH/STATUS COLOR
        painter.setBrush(QBrush(QColor(self.status_color)))

        # DRAW
        painter.drawEllipse(rect.x() + 27, rect.y() + 27, 13, 13)
        painter.end()

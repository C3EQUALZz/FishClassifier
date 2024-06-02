# Packages
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from app.core.widgets import *
# GUI
from app.views.chat.helpers.ui_main import UiMainWindow  # MainWindow
from app.modules.app_settings.settings import *

# GLOBAL VARS
# ///////////////////////////////////////////////////////////////
_is_maximized = False


# APP FUNCTIONS
# ///////////////////////////////////////////////////////////////
class UiFunctions(QFrame):

    def __init__(self) -> None:
        super().__init__()
        # GET WIDGETS FROM "ui_main.py"
        # Load widgets inside App Functions
        # ///////////////////////////////////////////////////////////////
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

    # SET UI DEFINITIONS
    # Set ui definitions before "self.show()" in main.py
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self):
        global _is_maximized

        # CHANGE UI AND RESIZE GRIP
        def change_ui():
            if not _is_maximized:
                self.resize(self.width() + 1, self.height() + 1)
                self.ui.margins_app.setContentsMargins(10, 10, 10, 10)
                self.ui.maximize_restore_app_btn.setToolTip("Restore")
                self.ui.maximize_restore_app_btn.setStyleSheet("background-image: url("
                                                               ":/icons_svg/images/icons_svg/icon_maximize.svg);")
                self.ui.bg_app.setStyleSheet("#bg_app { border-radius: 10px; border: 2px solid rgb(30, 32, 33); }")
                self.left_grip.show()
                self.right_grip.show()
                self.top_grip.show()
                self.bottom_grip.show()

            else:
                self.ui.margins_app.setContentsMargins(0, 0, 0, 0)
                self.ui.maximize_restore_app_btn.setToolTip("Restore")
                self.ui.maximize_restore_app_btn.setStyleSheet("background-image: url("
                                                               ":/icons_svg/images/icons_svg/icon_restore.svg);")
                self.ui.bg_app.setStyleSheet("#bg_app { border-radius: 0px; border: none; }")
                self.left_grip.hide()
                self.right_grip.hide()
                self.top_grip.hide()
                self.bottom_grip.hide()

        # CHECK EVENT
        if self.isMaximized():
            _is_maximized = False
            self.showNormal()
        else:
            _is_maximized = True
            self.showMaximized()

        change_ui()

    # START CHAT SELECTION
    # ///////////////////////////////////////////////////////////////
    def select_chat_message(self, widget_name: str) -> None:
        """
        Активирует выбранное сообщение чата.

        Этот метод выполняет поиск по всем дочерним элементам "messages_frame", которые имеют тип QWidget.
        Если имя объекта дочернего виджета совпадает с указанной строкой "widget",
        этот виджет становится активным.

        Args:
            widget_name (str): название объекта виджета, который должен быть активирован.
        """
        for widget in self.ui.messages_frame.findChildren(QWidget):
            if widget.objectName() == widget_name:
                widget.set_active(True)

    def deselect_other_chat_messages(self, widget_name: str) -> None:
        """
        Снимает выделение со всех сообщений чата, кроме текущего.

        Args:
            widget_name (str): Имя виджета, которое нужно оставить выбранным.
        """

        for widget in self.ui.messages_frame.findChildren(QWidget):
            if widget.objectName() != widget_name and hasattr(widget, 'set_active'):
                widget.set_active(False)

    # SET UI DEFINITIONS
    # Set ui definitions before "self.show()" in main.py
    # ///////////////////////////////////////////////////////////////
    def set_ui_definitions(self):

        # GET SETTINGS FROM JSON DESERIALIZED
        self.settings = Settings().items

        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # MOVE WINDOW / MAXIMIZE / RESTORE
        def move_window(event: QMouseEvent.Type.DragMove) -> None:
            # IF MAXIMIZED CHANGE TO NORMAL
            if self.isMaximized():
                UiFunctions.maximize_restore(self)
                curso_x = self.pos().x()
                curso_y = event.globalPos().y() - QCursor.pos().y()
                self.move(curso_x, curso_y)
            # MOVE WINDOW
            if event.buttons() == Qt.MouseButton.LeftButton:
                if self.dragPos is not None:
                    self.move((self.pos().toPointF() + event.globalPosition() - self.dragPos).toPoint())

                self.dragPos = event.globalPosition()
                event.accept()

        self.ui.logo_top.mouseMoveEvent = move_window
        self.ui.title_bar.mouseMoveEvent = move_window

        # DOUBLE CLICK MAXIMIZE / RESTORE
        def maximize_restore(event):
            if event.type() == QEvent.Type.MouseButtonDblClick:
                UiFunctions.maximize_restore(self)

        self.ui.title_bar.mouseDoubleClickEvent = maximize_restore

        # TOP BTNS
        self.ui.minimize_app_btn.clicked.connect(lambda: self.showMinimized())
        self.ui.maximize_restore_app_btn.clicked.connect(lambda: UiFunctions.maximize_restore(self))
        self.ui.close_app_btn.clicked.connect(lambda: self.close())

        # DEFAULT PARAMETERS
        self.setWindowTitle(self.settings["app_name"])
        self.resize(self.settings["startup_size"][0], self.settings["startup_size"][1])
        self.setMinimumSize(self.settings["minimum_size"][0], self.settings["minimum_size"][1])

        # APPLY DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.ui.stylesheet.setGraphicsEffect(self.shadow)

        # CUSTOM GRIPS
        # Create grips to resize window
        self.left_grip = CustomGrip(self, Qt.Edge.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.Edge.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.Edge.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.Edge.BottomEdge, True)

    # RESIZE GRIPS
    # This function should be called whenever "MainWindow/main.py" has its window resized.
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        self.left_grip.setGeometry(0, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 10)
        self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

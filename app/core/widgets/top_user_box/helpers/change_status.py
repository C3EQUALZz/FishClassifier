from PySide6.QtWidgets import QFrame, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import Signal
from .status_button import StatusButton

import app.core.utils.effects as effects_namespace

# SET STYLE TO POPUP
# ///////////////////////////////////////////////////////////////
style = """
/* QFrame */
QFrame {
    background: #333436; border-radius: 10px;
}
/* Search Message */
.QLineEdit {
	border: 2px solid rgb(47, 48, 50);
	border-radius: 15px;
	background-color: rgb(47, 48, 50);
	color: rgb(121, 121, 121);
	padding-left: 10px;
	padding-right: 10px;
}
.QLineEdit:hover {
	color: rgb(230, 230, 230);
	border: 2px solid rgb(62, 63, 66);
}
.QLineEdit:focus {
	color: rgb(230, 230, 230);
	border: 2px solid rgb(53, 54, 56);
	background-color: rgb(14, 14, 15);
}
/* QPushButton */
.QPushButton{
    background-color: transparent;
    border: none;
    border-radius: 10px;
    background-repeat: no-repeat;
    background-position: left center;
    text-align: left;
    color: #999999;
    padding-left: 38px;
}
.QPushButton:hover{
    background-color: #151617;
    color: #CCCCCC;
}

"""


class ChangeStatus(QFrame):
    status = Signal(str)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setFixedSize(230, 205)
        self.setStyleSheet(style)
        self.setParent(parent)

        self.layout = None
        self.border = None
        self.layout_content = None
        self.line_edit = None
        self.label = None

        self.setup_ui()

    def setup_ui(self):
        # LAYOUT AND BORDER
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.border = QFrame(self)
        self.layout.addWidget(self.border)

        # LINEEDIT AND BTNS BOX
        self.layout_content = QVBoxLayout(self.border)
        self.layout_content.setContentsMargins(0, 0, 0, 0)
        self.layout_content.setSpacing(1)

        # CHANGE DESCRIPTION
        self.line_edit = QLineEdit()
        self.line_edit.setMinimumHeight(30)
        self.line_edit.setPlaceholderText("Write what you are doing...")
        self.layout_content.addWidget(self.line_edit)

        # TOP LABEL
        self.label = QLabel("Change status:")
        self.label.setStyleSheet("padding-top: 5px; padding-bottom: 5px; color: rgb(121, 121, 121);")
        self.layout_content.addWidget(self.label)

        # ADD BUTTONS
        self.add_status_button("Online", ":/icons_svg/images/icons_svg/icon_online.svg", "online")
        self.add_status_button("Idle", ":/icons_svg/images/icons_svg/icon_idle.svg", "idle")
        self.add_status_button("Do not disturb", ":/icons_svg/images/icons_svg/icon_busy.svg", "busy")
        self.add_status_button("Invisible", ":/icons_svg/images/icons_svg/icon_invisible.svg", "invisible")

        # SET DROP SHADOW
        self.setGraphicsEffect(effects_namespace.ShadowEffect(self))

    def add_status_button(self, text, icon_path, status):
        button = StatusButton(text, icon_path, self)
        button.clicked.connect(lambda: self.send_signal(status))
        self.layout_content.addWidget(button)

    def send_signal(self, status):
        self.status.emit(status)

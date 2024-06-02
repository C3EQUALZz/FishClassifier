from app.views.chat.helpers.ui_main import UiMainWindow


# APP FUNCTIONS
# ///////////////////////////////////////////////////////////////
class AppFunctions:
    def __init__(self) -> None:
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

    def change_placeholder(self) -> None:
        self.ui.search_line_edit.setPlaceholderText("teste")

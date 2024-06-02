import typing
import app.views.login.helpers as helpers_namespace


class Progress(typing.Protocol):
    def show(self) -> None:
        ...

    def setFixedSize(self, width, height) -> None:
        ...

    def set_value(self, value) -> None:
        ...

    def add_shadow(self, value: bool) -> None:
        ...

    def setParent(self, ui_login: helpers_namespace.UiLogin) -> None:
        ...

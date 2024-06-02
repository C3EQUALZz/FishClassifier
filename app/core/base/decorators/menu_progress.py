from PySide6.QtCore import QRect, QEasingCurve, QTimer
from PySide6.QtGui import QColor

import app.core.abstract as abstract_namespace
import app.core.interfaces as interfaces_namespace
import app.views.login.helpers as helpers_namespace


class MenuProgress(abstract_namespace.ProgressDecorator):
    def __init__(self, progress: interfaces_namespace.Progress, ui_login: helpers_namespace.UiLogin) -> None:
        super().__init__(progress, ui_login)
        self.timer: QTimer = QTimer()
        self.counter: int = 0

    def start(self) -> None:
        """Sets up and starts the progress bar animation."""
        self.setup_progress_bar()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)

    def setup_progress_bar(self) -> None:
        """
        Configures the properties of the progress bar.
        """
        self.progress.width = 240
        self.progress.height = 240
        self.progress.value = 0
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.font_size = 20
        self.progress.add_shadow(True)
        self.progress.progress_width = 4
        self.progress.progress_color = QColor("#bdff00")
        self.progress.text_color = QColor("#E6E6E6")
        self.progress.bg_color = QColor("#222222")
        self.progress.setParent(self.ui.preloader)

    def update_progress(self) -> None:
        """Updates the value of the progress bar and starts the animation when complete."""
        self.progress.set_value(self.counter)

        if self.counter >= 100:
            self.timer.stop()
            self.start_animation()

        self.counter += 1

    def animation(self) -> None:
        """Restarts the timer for the progress bar animation."""
        self.timer.start(30)

    def start_animation(self) -> None:
        """Initiates the final animation when the progress bar is complete."""
        self.property_animation.setDuration(1500)
        self.property_animation.setStartValue(
            QRect(0, 70, self.ui.frame_widgets.width(), self.ui.frame_widgets.height())
        )

        self.property_animation.setEndValue(
            QRect(0, -325, self.ui.frame_widgets.width(), self.ui.frame_widgets.height())
        )

        self.property_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.property_animation.start()

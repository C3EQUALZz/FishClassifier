import json

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import atexit
import sys
import app.core.base as base
import logging
import logging.config
import logging.handlers
import pathlib

logger = logging.getLogger("my_app")


def setup_logger() -> None:
    """
    Настройка логирования
    :return: ничего не возвращает только инициализация
    """
    config_file = pathlib.Path("app/config/logger_config_log.json")
    with open(config_file, "r") as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def main() -> None:
    setup_logger()
    app = QApplication(sys.argv)
    logger.debug("Запуск приложения")
    app.setWindowIcon(QIcon("app/resources/images/icon.ico"))
    logger.debug("Установка иконки")
    window_manager = base.WindowManager(base.ViewFactory(), base.ControllerFactory())
    logger.debug("Создали WindowManager, DI был произведен удачно")
    window_manager.switch_to_window("LoginWindowView")
    logger.debug("Удачно переключились на LoginWindowView")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

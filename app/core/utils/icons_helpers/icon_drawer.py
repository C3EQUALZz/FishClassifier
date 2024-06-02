from dataclasses import dataclass
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect, QRectF
from PySide6.QtSvg import QSvgRenderer
from pathlib import Path


@dataclass
class IconDrawer:
    painter: QPainter
    svg_file: Path
    rect: QRect

    def draw(self) -> None:
        """
        Рисует и масштабирует SVG иконку, которую ей передали.
        :return: Ничего не возвращает
        """
        renderer = QSvgRenderer(str(self.svg_file))

        svg_size = renderer.defaultSize()
        target_size = self.rect.size()

        # Рассчитываем масштаб для сохранения пропорций
        scale_factor = min(target_size.width() / svg_size.width(), target_size.height() / svg_size.height()) * 0.65

        # Рассчитываем новый размер иконки с учетом масштаба
        new_width = svg_size.width() * scale_factor
        new_height = svg_size.height() * scale_factor

        # Вычисляем координаты для центрирования SVG
        x = self.rect.x() + (self.rect.width() - new_width) / 2
        y = self.rect.y() + (self.rect.height() - new_height) / 2

        # Создаем прямоугольник для рендеринга SVG
        render_rect = QRectF(x, y, new_width, new_height)

        renderer.render(self.painter, render_rect)

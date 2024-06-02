from dataclasses import dataclass


@dataclass
class ButtonParameters:
    """
    Класс для хранения параметров кнопки.


    Инициализирует объект ButtonParameters.

    Args:
        width (int): Ширина кнопки.
        height (int): Высота кнопки.
        pos (Tuple[int, int]): Позиция кнопки.
        border_radius (int): Радиус границы кнопки.
    """
    width: int = 40
    height: int = 40
    pos: tuple[int, int] = (0, 0)
    border_radius: int = 10

    def __post_init__(self):
        self.pos_x, self.pos_y = self.pos

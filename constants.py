from dataclasses import dataclass

@dataclass(frozen=True)
class Screen:
    WIDTH: int = 650
    HEIGHT: int = 750
    BG_COLOR: str = "#03001C"
    TITLE: str = "Breakout!"
    FPS: int = 60

@dataclass(frozen=True)
class Game:
    REG_FONT: tuple[str, int, str] = ("Helvetica", 16, "normal")
    REG_FONT_COL: str = "white"
    SCORE_POS: tuple = (-270, 310)
    SCORE_TXT: str = "SCORE: "
    LIVES: int = 3
    X_BOUNDARY: int = 215
    BORDER_DIM: tuple = (-280, -325, 280, 293)
    BORDER_COL: str = "#787A91"
    BORDER_THICKNESS: int = 2

@dataclass(frozen=True)
class Blocks:
    CELL_WIDTH: int = 80
    COLORS: tuple[str, ...] = ("red", "orange", "yellow", "green", "blue")
    SHAPESIZE: tuple = (0.75, 3.50, 0)
    STARTING_POS: int = 280
    ROW_SPACING: int = 25

@dataclass(frozen=True)
class Paddle:
    SPEED: int = 8
    SHAPESIZE: tuple = (0.60, 6) # (stretch_wid, stretch_len) scale factor of 20
    BASESIZE: int = 20
    STARTING_POS: int = -280
    COLOR: str = "#916BBF"

    @classmethod
    def width(cls) -> float:
        return cls.SHAPESIZE[1] * cls.BASESIZE

    @classmethod
    def half_width(cls) -> float:
        return cls.width() / 2

    @classmethod
    def height(cls) -> float:
        return cls.SHAPESIZE[0] * cls.BASESIZE

    @classmethod
    def half_height(cls) -> float:
        return cls.height() / 2

@dataclass(frozen=True)
class Ball:
    COLOR: str = "white"
    SHAPESIZE: tuple = (0.80, 0.80) # (stretch_wid, stretch_len) scale factor of 20
    BASESIZE: int = 20
    SPEED: int = 5

    @classmethod
    def width(cls) -> float:
        return cls.SHAPESIZE[1] * cls.BASESIZE

    @classmethod
    def height(cls) -> float:
        return cls.SHAPESIZE[0] * cls.BASESIZE

    @classmethod
    def half_height(cls) -> float:
        return cls.height() / 2

@dataclass(frozen=True)
class Physics:
    MAX_RATIO: float = 0.95
    PADDLE_PUSH: float = 0.25

@dataclass(frozen=True)
class Config:
    Screen: Screen = Screen()
    Game: Game = Game()
    Blocks: Blocks = Blocks()
    Paddle: Paddle = Paddle()
    Ball: Ball = Ball()
    Physics: Physics = Physics()

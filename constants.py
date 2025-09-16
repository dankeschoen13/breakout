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
    BASESIZE: int = 20
    STARTING_POS: int = 280
    ROW_SPACING: int = 25

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
class Paddle:
    SPEED: int = 5
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
    def diameter(cls) -> float:
        return cls.SHAPESIZE[0] * cls.BASESIZE

    @classmethod
    def radius(cls) -> float:
        return cls.diameter() / 2

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

class Rules:
    """
    FUTURE ME:
    - remember turtle elements are centered to its coordinates, that means:
        1. when positioning something on top of or on the side of something,
        divide the full height or width to 2 in order to get the edge.
    """

    @classmethod
    def paddle_x_limit(cls) -> int:
        """
        - excludes distance between border inner edge & paddle's center so paddle doesn't exceed the border
        :return: effective paddle horizontal movement limit
        """
        border_loc = abs(Config.Game.BORDER_DIM[0])
        border_inner_edge = border_loc - Config.Game.BORDER_THICKNESS / 2
        return border_inner_edge - Config.Paddle.half_width()

    @classmethod
    def ball_start_y(cls):
        """
        :return: the correct y-axis coordinate so the ball appears correctly on top of the paddle
        """
        paddle_top = Config.Paddle.STARTING_POS + Config.Paddle.half_height()
        return paddle_top + Config.Ball.radius()
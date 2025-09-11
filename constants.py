from dataclasses import dataclass

@dataclass(frozen=True)
class Screen:
    WIDTH: int = 650
    HEIGHT: int = 750
    BG_COLOR: str = "#03001C"
    TITLE: str = "Breakout!"
    FPS: int = 60

@dataclass(frozen=True)
class Paddle:
    SPEED: int = 8
    SHAPESIZE: tuple = (0.75, 6) # (stretch_wid, stretch_len) scale factor of 20
    POS: int = -280
    COLOR: str = "#916BBF"
    HALF_WIDTH: int = 50   # half-width in px
    HEIGHT: int = 20       # used for hitbox math

@dataclass(frozen=True)
class Ball:
    SHAPESIZE: tuple = (0.80, 0.80) # (stretch_wid, stretch_len) scale factor of 20
    SPEED: int = 5
    SIZE: int = 20  # base size of a turtle circle (scales with shapesize)
    COLOR: str = "white"

@dataclass(frozen=True)
class Physics:
    MAX_OFFSET_PERCENTAGE: float = 0.8
    PADDLE_DIR_INFLUENCE: float = 0.15

@dataclass(frozen=True)
class Game:
    LIVES: int = 3
    BLOCKS_COLORS: tuple[str, ...] = "red", "orange", "yellow", "green", "blue"
    X_BOUNDARY: int = 215
    BORDER_DIMENSIONS: tuple = (-280, -325, 280, 293)

@dataclass(frozen=True)
class Config:
    Screen: Screen = Screen()
    Paddle: Paddle = Paddle()
    Ball: Ball = Ball()
    Physics: Physics = Physics()
    Game: Game = Game()

class Settings:
    # Screen
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    SCREEN_BG_COLOR = "black"
    SCREEN_TITLE = "Breakout"

    #Game Area
    BOUNDARY = 215

    # Paddle
    PADDLE_SPEED = 8
    PADDLE_SHAPESIZE_W = 6 # scale factor of 20
    PADDLE_SHAPESIZE_H = 0.75 # scale factor of 20
    PADDLE_Y_POS = -280
    PADDLE_COLOR = "#916BBF"
    # PADDLE_HALF = 50   # half-width of paddle in px
    # PADDLE_HEIGHT = 20 # actual height (for hitbox math)

    # Ball
    BALL_SHAPESIZE_W = 0.80 # scale factor of 20
    BALL_SHAPESIZE_H = 0.80 # scale factor of 20
    BALL_SPEED = 5
    BALL_SIZE = 20  # base size of a turtle circle (scales with shapesize)
    BALL_COLOR = "white"

    # Physics
    MAX_OFFSET_PERCENTAGE = 0.8
    PADDLE_DIR_INFLUENCE = 0.15

    # Game
    LIVES = 3
    FPS = 60
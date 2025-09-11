from constants import Settings
import math

BOUNDARY = 215
BALL_SPEED = 5
PADDLE_SPEED = 8
PADDLE_HALF = 60
MAX_OFFSET_PERCENTAGE = 0.9
PADDLE_DIR_INFLUENCE = 0.2 # of ball speed

class Logic:

    def __init__(self, blocks, paddle, ball, scoreboard):
        self.blocks = blocks
        self.paddle = paddle
        self.ball = ball
        self.ball.reset_position(self.paddle.xcor(), self.get_ball_start_y())
        self.score = scoreboard
        # Game Stages Flag
        self.game_started = False
        self.first_move = []
        # Movement flags
        self.is_moving_left = False
        self.is_moving_right = False
        self.speed_val = PADDLE_SPEED

    # Key press trackers
    def press_left(self):
        self.game_started = True
        self.is_moving_left = True

    def release_left(self):
        self.is_moving_left = False

    def press_right(self):
        self.game_started = True
        self.is_moving_right = True

    def release_right(self):
        self.is_moving_right = False

    def paddle_move(self):
        moved = False

        if (self.is_moving_left
                and self.paddle.xcor() > -BOUNDARY):
            self.paddle.setx(self.paddle.xcor() - self.speed_val)
            moved = True

        if (self.is_moving_right
                and self.paddle.xcor() < BOUNDARY):
            self.paddle.setx(self.paddle.xcor() + self.speed_val)
            moved = True

        if moved and not self.ball.in_play:
            self.launch_ball()

    def get_ball_start_y(self):
        ball_height = 20 * self.ball.shapesize()[0]
        paddle_height = 20 * self.paddle.shapesize()[0]
        paddle_top = self.paddle.ycor() + (paddle_height / 2)
        return paddle_top + (ball_height / 2)

    def launch_ball(self):
        if self.ball.in_play:
            return  # Already launched

        self.ball.in_play = True

        speed = BALL_SPEED
        max_offset = PADDLE_HALF * MAX_OFFSET_PERCENTAGE
        offset = self.ball.xcor() - self.paddle.xcor()
        offset = max(-max_offset, min(offset, max_offset))

        self.ball.x_move = (offset / PADDLE_HALF) * speed

        if self.is_moving_right:
            self.ball.x_move += 1
        elif self.is_moving_left:
            self.ball.x_move -= 1

        self.ball.y_move = math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0))

    def check_paddle_collision(self):
        if (self.paddle.ycor() < self.ball.ycor() < self.get_ball_start_y()
                and self.paddle.xcor() - PADDLE_HALF < self.ball.xcor() < self.paddle.xcor() + PADDLE_HALF
                and self.ball.y_move < 0):
            self.ball.bounce_y()

            speed = math.hypot(self.ball.x_move, self.ball.y_move)

            max_offset = PADDLE_HALF * MAX_OFFSET_PERCENTAGE
            offset = self.ball.xcor() - self.paddle.xcor()
            offset = max(-max_offset, min(offset, max_offset))
            self.ball.x_move = offset / PADDLE_HALF * speed

            influence = PADDLE_DIR_INFLUENCE * speed
            if self.is_moving_right:
                self.ball.x_move += influence
            elif self.is_moving_left:
                self.ball.x_move -= influence

            self.ball.y_move = math.copysign(
                math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0)),
                self.ball.y_move
            )
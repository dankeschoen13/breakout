import math
from constants import Config, Rules

class Logic:

    def __init__(self, blocks, paddle, ball, scoreboard):
        self.blocks = blocks
        self.paddle = paddle
        self.ball = ball
        self.ball.reset_position(
            self.paddle.xcor(),
            Rules.ball_start_y()
        )
        self.score = scoreboard
        # Game Stages Flag
        self.game_started = False
        self.first_move = []
        # Movement flags
        self.is_moving_left = False
        self.is_moving_right = False
        self.paddle_step = Config.Paddle.SPEED

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
        """
        - Moves paddle based on movement flags
        - Clamps paddle movement to never exceed the set boundary
        - Automatically launches ball if ball is not in play
        """
        moved = False
        paddle_x = self.paddle.xcor()

        if self.is_moving_left:
            paddle_x -= self.paddle_step
            moved = True
        if self.is_moving_right:
            paddle_x += self.paddle_step
            moved = True

        paddle_x = max(-Rules.paddle_x_limit(),
                       min(Rules.paddle_x_limit(), paddle_x))
        self.paddle.setx(paddle_x)

        if moved and not self.ball.in_play:
            self.launch_ball()

    def launch_ball(self):
        """
        - Launches the ball from the paddle
        - Influences horizontal movement based on paddle direction.
        - Logic similar to check_paddle_collision. check below
        """
        if self.ball.in_play:
            return

        self.ball.in_play = True

        paddle_half = Config.Paddle.half_width()
        speed = Config.Ball.SPEED

        ratio = (self.ball.xcor() - self.paddle.xcor()) / paddle_half
        if self.is_moving_right:
            ratio += Config.Physics.PADDLE_PUSH
        elif self.is_moving_left:
            ratio -= Config.Physics.PADDLE_PUSH
        ratio = max(-Config.Physics.MAX_RATIO,
                    min(ratio, Config.Physics.MAX_RATIO))

        self.ball.x_move = ratio * speed
        self.ball.y_move = math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0))

    def check_paddle_collision(self):
        """
        - Detects collision only when all conditions are true:
            1. Ball enters small collision zone between paddle and ball starting position
                    ( paddle < ball < ball starting position )
            2. Ball is inside the paddle length
                    ( paddle left edge < ball < paddle right edge )
            3. Ball is moving downwards (-y)
        - Otherwise:
            1. Reset ball position.

        *** IMPORTANT: logic during collision
            1. Bounces normally by reversing y-axis movement (bounce_y)
            2. Calculates velocity based on current x and y value upon hit (math.hypot)
            3. Redistributes the velocity by calculating ratio of distribution for horizontal movement based on:
                a. where the ball hits the paddle
                b. direction of the paddle (adds fixed amount of influence)
            4. Clamps the value so horizontal movement doesn't take the entire speed allocation, preventing y=0 situations.
            5. Assigns the y-axis velocity based on speed not allocated to x
        """
        paddle_half = Config.Paddle.half_width()
        if (self.paddle.ycor() < self.ball.ycor() < Rules.ball_start_y()
                and self.paddle.xcor() - paddle_half < self.ball.xcor() < self.paddle.xcor() + paddle_half
                and self.ball.y_move < 0):

            self.ball.bounce_y()

            speed = math.hypot(self.ball.x_move, self.ball.y_move)

            ratio = (self.ball.xcor() - self.paddle.xcor()) / paddle_half
            if self.is_moving_right:
                ratio += Config.Physics.PADDLE_PUSH
            elif self.is_moving_left:
                ratio -= Config.Physics.PADDLE_PUSH
            ratio = max(-Config.Physics.MAX_RATIO,
                        min(ratio, Config.Physics.MAX_RATIO))

            self.ball.x_move = ratio * speed
            self.ball.y_move = math.copysign(
                math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0)),
                self.ball.y_move
            )

        elif self.ball.ycor() < Config.Game.BORDER_DIM[1] + Config.Ball.radius():
            self.ball.reset_position(
                self.paddle.xcor(),
                Rules.ball_start_y()
            )

    def check_blocks_collision(self):
        ball = self.ball
        r = Config.Ball.radius()

        for color, block_list in list(self.blocks.items()):
            for block in block_list[:]:
                if (abs(ball.xcor() - block.xcor()) < Config.Blocks.half_width() + r and
                        abs(ball.ycor() - block.ycor()) < Config.Blocks.half_height() + r):

                    dx = ball.xcor() - block.xcor()
                    dy = ball.ycor() - block.ycor()

                    if abs(dx / Config.Blocks.width()) > abs(dy / Config.Blocks.height()):
                        self.ball.bounce_x()
                    else:
                        self.ball.bounce_y()

                    block.hideturtle()
                    self.blocks[color].remove(block)

                    return




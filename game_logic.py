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

        ball_start_pos = (ball.xcor(), ball.ycor())
        ball_velocity = (ball.x_move, ball.y_move)

        if ball_velocity[0] == 0 and ball_velocity[1] == 0:
            return None

        first_collision = {
            "time": 1.0,
            "block": None,
            "normal": (0.0, 0.0)
        }

        for color, block_list in self.blocks.items():
            for block in block_list:

                west_side = block.xcor() - Config.Blocks.half_width() - r
                south_side = block.ycor() - Config.Blocks.half_height() - r
                east_side = block.xcor() + Config.Blocks.half_width() + r
                north_side = block.ycor() + Config.Blocks.half_height() + r

                if ball_velocity[0] == 0:
                    shortest_time_to_x_hit, longest_time_to_x_hit = -math.inf, math.inf
                else:
                    time_to_hit_west = (west_side - ball_start_pos[0]) / ball_velocity[0]
                    time_to_hit_east = (east_side - ball_start_pos[0]) / ball_velocity[0]

                    shortest_time_to_x_hit = min(time_to_hit_west, time_to_hit_east)
                    longest_time_to_x_hit = max(time_to_hit_west, time_to_hit_east)

                if ball_velocity[1] == 0:
                    shortest_time_to_y_hit, longest_time_to_y_hit = -math.inf, math.inf
                else:
                    time_to_hit_south = (south_side - ball_start_pos[1]) / ball_velocity[1]
                    time_to_hit_north = (north_side - ball_start_pos[1]) / ball_velocity[1]

                    shortest_time_to_y_hit = min(time_to_hit_south, time_to_hit_north)
                    longest_time_to_y_hit = max(time_to_hit_south, time_to_hit_north)

                # A collision occurs only if the time intervals
                # [shortest_time_to_x_hit, longest_time_to_x_hit]
                # and
                # [shortest_time_to_y_hit, longest_time_to_y_hit]
                # overlap
                t_hit_near = max(shortest_time_to_x_hit, shortest_time_to_y_hit)
                t_hit_far = min(longest_time_to_x_hit, longest_time_to_y_hit)

                # Conditions for a valid collision:
                # 1. The intervals must overlap (t_hit_near < t_hit_far)
                # 2. The collision must happen in the future (t_hit_near > 0)
                # 3. The collision must happen within this frame (t_hit_near < 1.0)
                # 4. It must be earlier than any other collision we've found so far
                if t_hit_near < t_hit_far and 0 < t_hit_near < first_collision["time"]:
                    first_collision["time"] = t_hit_near
                    first_collision["block"] = block
                    first_collision["color"] = color

                    if shortest_time_to_x_hit > shortest_time_to_y_hit:
                        first_collision["normal"] = (-math.copysign(1, ball_velocity[0]), 0)  # Hit a side wall
                    else:
                        first_collision["normal"] = (0, -math.copysign(1, ball_velocity[1]))  # Hit top/bottom

        if first_collision["block"] is not None:
            time = first_collision["time"]
            ball.setx(ball_start_pos[0] + ball_velocity[0] * time)
            ball.sety(ball_start_pos[1] + ball_velocity[1] * time)

            dot_product = ball.x_move * first_collision["normal"][0] + ball.y_move * first_collision["normal"][1]
            ball.x_move -= 2 * dot_product * first_collision["normal"][0]
            ball.y_move -= 2 * dot_product * first_collision["normal"][1]

            remaining_time = 1.0 - time
            ball.setx(ball.xcor() + ball.x_move * remaining_time)
            ball.sety(ball.ycor() + ball.y_move * remaining_time)

            block_to_remove = first_collision["block"]
            block_to_remove.hideturtle() # type: ignore
            self.blocks[first_collision["color"]].remove(block_to_remove)

            return True  # Indicate that a collision and move happened

        return False  # Indicate no collision happened




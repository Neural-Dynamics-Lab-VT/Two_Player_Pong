from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from pylsl import StreamInlet, resolve_stream
import numpy as np


def get_lsl_signal_stream():
    """
    Uses pylsl to receive the EEG stream from the cap. Must ideally have two streams.
    """
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')
    print("Received no of streams: {}".format(len(streams)))

    # create a new inlet to read from the stream
    inlet_1 = None
    inlet_2 = None
    for s in streams:
        stream_name = StreamInlet(s).info().name()
        if stream_name == "PongPlayer1":
            inlet_1 = StreamInlet(s)
        elif stream_name == "PongPlayer2":
            inlet_2 = StreamInlet(s)

    if inlet_1 is None:
        print("Stream for player 1 not found. Please ensure that the scenario is running.")
    if inlet_2 is None:
        print("Stream for player 2 not found. Please ensure that the scenario is running.")

    return inlet_1, inlet_2


class PongPaddle(Widget):
    """
    Widget used to specify the ball bouncing off of the paddle.
    """
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    """
    Widget the describes the ball and its velocity.
    """
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    """
    This is the real deal. Contains events handlers for keyboard inputs if pressed, updates the
    ball velocity on collision and also adds touchscreen controls (kinda useless for now).
    """
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    game = ObjectProperty(None)
    ball_velocity = 10

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.speed = 25
        self.beta_threshold = 1

        # TODO: Add paddle momentum
        # TODO: Change beta_threshold for actual EEG signal

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w' and self.player1.center_y < self.game.height - 100:
            print("Up")
            self.player1.center_y += self.speed
        elif keycode[1] == 's' and self.player1.center_y > 100:
            print("Down")
            self.player1.center_y -= self.speed
        elif keycode[1] == 'up' and self.player2.center_y < self.game.height - 100:
            self.player2.center_y += self.speed
        elif keycode[1] == 'down' and self.player2.center_y > 100:
            self.player2.center_y -= self.speed
        return True

    def serve_ball(self, vel=(ball_velocity, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        sample_1, _ = inlet_1.pull_sample()
        sample_2, _ = inlet_2.pull_sample()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(self.ball_velocity, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-self.ball_velocity, 0))

        avg_beta_signal_1 = np.mean(sample_1)
        avg_beta_signal_2 = np.mean(sample_2)

        if avg_beta_signal_1 > self.beta_threshold and self.player1.center_y < self.game.height - 100:
            self.player1.center_y += self.speed

        if avg_beta_signal_1 <= self.beta_threshold and self.player1.center_y > 100:
            self.player1.center_y -= self.speed

        if avg_beta_signal_2 > self.beta_threshold and self.player2.center_y < self.game.height - 100:
            self.player2.center_y += self.speed

        if avg_beta_signal_2 <= self.beta_threshold and self.player2.center_y > 100:
            self.player2.center_y -= self.speed

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    """
    A class to start the game.
    """

    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        print("The game's running")
        return game


if __name__ == '__main__':
    inlet_1, inlet_2 = get_lsl_signal_stream()
    PongApp().run()

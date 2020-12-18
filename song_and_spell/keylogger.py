import pynput.keyboard as Keyboard
from typing import Callable


class Logger(object):
    """Log the past N key-presses"""

    def __init__(self, max_length: int = 100):
        self.max_length = max_length
        self.index = 0
        self.pressed = [" "] * max_length

    @property
    def pos(self) -> int:
        return self.index % self.max_length

    def append(self, char: str) -> None:
        self.pressed[self.pos] = char
        self.index += 1

    def get_last(self, n: int) -> str:
        pos = self.pos
        if pos < n:
            left = n + pos - 1
            right = pos
            return "".join(self.pressed[left:]) + "".join(self.pressed[:right])
        return "".join(self.pressed[:n])

    def call_backs(self) -> Callable:
        """Build callbacks for the key-logger"""

        def on_press(key):
            # Callback for  key-press
            try:
                char = key.char
                print(f"Logged key '{char}'")
                self.append(char)
                print("pressed", self.pressed)
            except AttributeError:
                print(f"Special key {key} pressed!")

        def on_release(key):
            pass

        return on_press, on_release


def main():
    on_press, on_release = Logger(10).call_backs()
    with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()

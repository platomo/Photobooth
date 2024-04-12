import fire
from gpiozero import LED


def start_led(pin: int = 23):
    led = LED(pin)
    led.blink(n=3, background=False)


if __name__ == "__main__":
    fire.Fire(start_led)

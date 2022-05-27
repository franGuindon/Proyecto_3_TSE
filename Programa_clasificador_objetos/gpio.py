import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Pin:
    def __init__(self, pin_number):
        self.pin_number = pin_number
        GPIO.setup(pin_number, GPIO.OUT)
    def high(self): GPIO.output(self.pin_number, GPIO.HIGH)
    def low(self): GPIO.output(self.pin_number, GPIO.LOW)

def cleanup(): GPIO.cleanup()

if __name__ == "__main__":
    import time

    led = Pin(18)

    for i in range(10):
        led.high()
        time.sleep(0.2)
        led.low()
        time.sleep(0.2)

    cleanup()

import time

import RPi.GPIO as GPIO


class GPIOController:
    def __int__(self):
        self.driver_pins = {
            'IN11_PIN': 16,
            'IN12_PIN': 18,
            'IN13_PIN': 24,
            'IN14_PIN': 26,
            'IN21_PIN': 31,
            'IN22_PIN': 33,
            'IN23_PIN': 35,
            'IN24_PIN': 37,
        }
        self.grab_pins = None

        GPIO.setmode(GPIO.BOARD)

        self.stop()

    def clean_up(self):
        GPIO.cleanup()

    def move_forward(self):
        GPIO.output(self.driver_pins.get('IN11_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN13_PIN'), GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(self.driver_pins.get('IN21_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN23_PIN'), GPIO.HIGH)

    def move_backward(self):
        GPIO.output(self.driver_pins.get('IN12_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN14_PIN'), GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(self.driver_pins.get('IN22_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN24_PIN'), GPIO.HIGH)

    def move_right(self):
        GPIO.output(self.driver_pins.get('IN11_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN24_PIN'), GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(self.driver_pins.get('IN21_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN14_PIN'), GPIO.HIGH)

    def move_left(self):
        GPIO.output(self.driver_pins.get('IN12_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN23_PIN'), GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(self.driver_pins.get('IN22_PIN'), GPIO.HIGH)
        GPIO.output(self.driver_pins.get('IN13_PIN'), GPIO.HIGH)

    def stop(self):
        for pin in self.driver_pins.keys():
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

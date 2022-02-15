from time import sleep, time
from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory


host = "10.110.30.18"
local = False
pin_factory = PiGPIOFactory(host='127.0.0.1') if local else PiGPIOFactory(host=host)


class Control:
    def __init__(self, coil_pin, contact_pin, side, name, t_waggle=10, t_autolock=7200, t_alarm=18000):
        self.name = name
        self.side = side

        self.t_waggle = t_waggle
        self.t_autolock = t_autolock
        self.t_alarm = t_alarm

        self.coil = LED(coil_pin, pin_factory=pin_factory)
        self.contact = Button(contact_pin, pin_factory=pin_factory, pull_up=False)
        self.contact.when_pressed = self.key_present
        self.contact.when_released = self.key_present

        self.key_taken = None
        self.key_present()
        self.key_unlocked = False
        self.key_ready_to_return = False

    def key_present(self):
        self.key_taken = False
        if not self.contact.is_pressed:
            print(self.name, "taken")
            self.key_taken = time()
        else:
            print(self.name, "returned")
            self.key_taken = False

    def key_lock(self):
        self.coil.off()
        self.key_unlocked = False

    def key_unlock(self):
        self.coil.on()
        self.key_unlocked = time()


class Alarm:
    def __init__(self, buzz_pin):
        self.buzz = LED(buzz_pin, pin_factory=pin_factory)

    def command(self, state):
        if state:
            self.buzz.on()
        else:
            self.buzz.off()

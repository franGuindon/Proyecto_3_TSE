import time

from arg_parser import parse_args
#from gpio import Pin, cleanup as gpio_cleanup
from obj_classifier import \
    setup as classifier_setup, \
    classify_object, try_classify_object, \
    cleanup as classifier_cleanup

class Belt:

    def __init__(self, args):
        self.args = args
        self.setup_pins()

    def setup_pins(self):
        self.belt_motor = Pin(0)
        self.arm_motor = Pin(1)

    def step_belt(self):
        self.belt_motor.high()
        time.sleep(0.2)
        self.belt_motor.low()

    def place_object_at_camera(self):
        grabbed = False
        while not grabbed:
            self.step_belt()
            grabbed, self.obj_class = try_classify_object()

    def classify_object(self):
        obj_class = classify_oject()
    
    def run(self):
        self.running = True
        while self.running:
            self.place_object_at_camera()
            self.classify_object()

def main(args):
    belt = Belt(args)
    belt.run()

if __name__ == "__main__":
    args = parse_args()
    classifier_setup(args)
    main(args)
    #gpio_cleanup()
    classifier_cleanup()
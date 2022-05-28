import time

from arg_parser import parse_args
from gpio import Pin, cleanup as gpio_cleanup
from obj_classifier import \
    setup as classifier_setup, \
    classify_object, try_classify_object, \
    cleanup as classifier_cleanup

class Belt:

    def __init__(self, args):
        self.args = args
        self.setup_pins()

    def setup_pins(self):
        self.belt_motor_pins = Pin(13), Pin(11), Pin(15), Pin(12)
        #self.arm_motor = Pin(1)

    def write_belt(self, seq):
        a,b,c,d = seq
        seq = int(a), int(b), int(c), int(d)
        for val, pin in zip(seq, self.belt_motor_pins):
            if val: pin.high()
            else: pin.low()

    def step_belt(self):
        seq = ["1000","1100","0100","0110","0010","0011","0001","1001"]
        direction = self.args.step_count > 0
        if direction: index_range = range(0, self.args.step_count, 1)
        else: index_range = range(-self.args.step_count, 0, -1)
        for i in index_range:
            elem = seq[i]
            self.write_belt(elem)
            time.sleep(self.args.velocity)

    def place_object_at_camera(self):
        grabbed = False
        while not grabbed:
            self.step_belt()
            grabbed, self.obj_class = try_classify_object()

    def classify_object(self): pass
    
    def run(self):
        self.running = True
        while self.running:
            self.place_object_at_camera()
            self.classify_object()
    
    def test(self):
        self.step_belt()

def main(args):
    belt = Belt(args)
    belt.test()

if __name__ == "__main__":
    args = parse_args()
    classifier_setup(args)
    main(args)
    gpio_cleanup()
    classifier_cleanup()
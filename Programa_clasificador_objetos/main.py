print("importing time")
import time

print("importing opencv")
import cv2
from gpio import GPIO

print("importing parser")
from arg_parser import parse_args
print("importing gpio")
from gpio import Pin, cleanup as gpio_cleanup
print("importing classifier")
from obj_classifier import \
    grab_fame, \
    setup as classifier_setup, \
    classify_object, try_classify_object, \
    cleanup as classifier_cleanup, \
    continuosly_classify_object
from paleta import paleta

class Belt:

    def __init__(self, args):
        self.args = args
        self.setup_pins()
    
    def setup_pins(self):
        self.belt_motor_pins = Pin(31), Pin(33), Pin(35), Pin(37)

    def write_belt(self, seq):
        a,b,c,d = seq
        seq = int(a), int(b), int(c), int(d)
        for val, pin in zip(seq, self.belt_motor_pins):
            if val: pin.high()
            else: pin.low()

    def step_belt(self, step_count):
        seq = ["1000","1100","0100","0110","0010","0011","0001","1001"]
        direction = step_count > 0
        if direction: index_range = range(0, step_count, 1)
        else: index_range = range(-step_count, 0, -1)
        for i in index_range:
            elem = seq[i%8]
            self.write_belt(elem)
            time.sleep(self.args.velocity)

    def classify_object(self):
        self.obj_class = classify_object(args.class_count)
        self.obj_class += 1
    
    def run(self):
        self.running = True
        while self.running:
            self.step_belt(args.step0)
            self.classify_object()
            self.step_belt(args.step1)
            print(self.obj_class)
            paleta(self.obj_class)
            if cv2.waitKey(1) & 0xFF == ord('q'): self.running = False
    
    def test(self):
        continuosly_classify_object()

def main(args):
    belt = Belt(args)
    belt.run()

if __name__ == "__main__":
    print("running main")
    print("parsing args")
    args = parse_args()
    print("debug mode set to", args.debug)
    print("setting up classifier")
    classifier_setup(args)
    print("running main obj")
    main(args)
    print("gpio cleanup")
    gpio_cleanup()
    print("classifier cleanup")
    classifier_cleanup()
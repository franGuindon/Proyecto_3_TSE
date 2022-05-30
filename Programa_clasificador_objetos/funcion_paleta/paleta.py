from time import sleep
import RPi.GPIO as GPIO
from arg_parser import parse_args

def dir_clk(Motor1A, Motor1B):
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)

def dir_cnt_clk(Motor1A, Motor1B):
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)

def dir_off(Motor1A, Motor1B):
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)

def paleta(direccion):
    
    Motor1A = 11
    Motor1B = 13
    enable = 3
    estado = 5

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(enable,GPIO.OUT)
    GPIO.setup(estado,GPIO.IN)
    p=GPIO.PWM(enable,100)
    p.start(100)
    print("Before while", GPIO.input(estado))
    
    if direccion == 1:
        if (GPIO.input(estado) == 1): print("Switch off")
        else: print("Switch on")
        print("Mover horario hasta prender switch")
        while (GPIO.input(estado) == 1):
            dir_clk(Motor1A, Motor1B)
            sleep(0.01)
            dir_off(Motor1A, Motor1B)
            sleep(0.01)
        if (GPIO.input(estado) == 1): print("Switch off")
        else: print("Switch off")
        print("Mover antihorario hasta apagar switch")
        while (GPIO.input(estado) == 1):
            dir_clk(Motor1A, Motor1B)
            sleep(0.01)
            dir_off(Motor1A, Motor1B)
            sleep(0.01)
    
    if direccion == 2:
        while (GPIO.input(estado) == 1):
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            sleep(0.01)
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.LOW)
            sleep(0.01)
        while (GPIO.input(estado) == 0):
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            sleep(0.01)
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.LOW)
            sleep(0.01)
        while (GPIO.input(estado) == 1):
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            sleep(0.01)
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.LOW)
            sleep(0.01)
    if direccion == 3: pass
    GPIO.cleanup()

if __name__ == "__main__":
    args = parse_args()
    print("Direction", args.dir_pal)
    paleta(args.dir_pal)

from time import sleep
import RPi.GPIO as GPIO
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
    p=GPIO.PWM(enable,500)
    p.start(60)
    while (GPIO.input(estado) == 1):
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        #sleep(0.1)
    
    if direccion == 1:
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        sleep(0.4)
        while (GPIO.input(estado) == 1):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)
            #sleep(0.1)
    
    if direccion == 2:
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        sleep(0.4)
        while (GPIO.input(estado) == 1):
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            #sleep(0.1)
    if direccion == 3:
        GPIO.cleanup()

    GPIO.cleanup()

paleta(3)

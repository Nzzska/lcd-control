import RPi.GPIO as GPIO
import time
import binascii

def to_bin(ascii):
    byte_array = ascii.encode()
    binary_int = int.from_bytes(byte_array, "big")
    binary_string = bin(binary_int)
    return binary_string[2:]

def binary_to_gpio_pins(nibble, pins):
    for i in range(len(nibble)):
        if nibble[i] == 0 :
            GPIO.output(pins[f"d{i}"], GPIO.LOW)
        elif nibble[i] == 1:
            GPIO.output(pins[f"d{i}"], GPIO.HIGH)

def split_nibbles(input):
    inp = [int(sym) for sym in str(input)]
    nibble1 = inp[:4]
    nibble2 = inp[4:8]
    return [nibble1, nibble2]

def write_4bit_command(command, pins):

    nibbles = split_nibbles(command)

    #upper nibble
    binary_to_gpio_pins(nibbles[0], pins)
    GPIO.output(pins['rs'], GPIO.LOW)
    GPIO.output(pins['rw'], GPIO.LOW)
    GPIO.output(pins['en'], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pins['en'], GPIO.LOW)

    #lower nibble
    binary_to_gpio_pins(nibbles[1], pins)
    GPIO.output(pins['rs'], GPIO.LOW)
    GPIO.output(pins['rw'], GPIO.LOW)
    GPIO.output(pins['en'], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pins['en'], GPIO.LOW)

    time.sleep(1)

def write_4bit_data(data, pins):

    nibbles = split_nibbles(data)

    #upper nibble
    binary_to_gpio_pins(nibbles[0], pins)
    GPIO.output(pins['rs'], GPIO.HIGH)
    GPIO.output(pins['rw'], GPIO.LOW)
    GPIO.output(pins['en'], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pins['en'], GPIO.LOW)

    #lower nibble
    binary_to_gpio_pins(nibbles[1], pins)
    GPIO.output(pins['rs'], GPIO.HIGH)
    GPIO.output(pins['rw'], GPIO.LOW)
    GPIO.output(pins['en'], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pins['en'], GPIO.LOW)

    time.sleep(1)

def setup_4bit_pins(pins):
    if (len(pins) != 7):
        print('Incorrect number of data lines')
        pass
    else:
        try:
            for pin in pins:
                GPIO.setup(pin, GPIO.OUT)
            print('setup successful!')
        except:
            print('setup failed!')
            pass

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#for testing (1,2,3,4,5,6,7) for prod use pins numbers of the actual board!!
pins = {
    'd1':1,
    'd2':2,
    'd3':3,
    'd4':4,
    'rs':5,
    'rw':6,
    'en':7,
}

setup_4bit_pins(pins)
write_4bit_command('00000010', pins)
write_4bit_command('00101000', pins)
write_4bit_command('00001110', pins)
write_4bit_command('00000001', pins)
write_4bit_command('10000000', pins)
write_4bit_data(to_bin('M'), pins)
write_4bit_data(to_bin('a'), pins)
write_4bit_data(to_bin('r'), pins)
write_4bit_data(to_bin('g'), pins)
write_4bit_data(to_bin('a'), pins)
write_4bit_data(to_bin('r'), pins)
write_4bit_data(to_bin('i'), pins)
write_4bit_data(to_bin('t'), pins)
write_4bit_data(to_bin('a'), pins)
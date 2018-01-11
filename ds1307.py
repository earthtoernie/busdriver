import pyBusPirateLite.I2C as I2C
import re
import binascii
import serial
import time

# https://www.devdungeon.com/content/working-binary-data-python

def parseHex(line):
    line = line.strip().upper()
    pattern = re.compile("-X[\dABCDEF][\dABCDEF]")

    if(len(line) % 4 != 0):
        raise ValueError("line must be like -x1F-x1F .. groups of 4 chars")

    n = 4
    strings = [line[i:i+n] for i in range(0, len(line), n)]
    # print(strings)
    # for int in range

    to_unhexlify = ''

    for str in strings:
        if (pattern.match(str) == False) or (len(str) != 4):
            raise ValueError("must be formatted like -x1F, case insensitive")
        else:
            to_unhexlify += str[2:]




    print('our hex is:')
    print(binascii.unhexlify(to_unhexlify))
    # bs = bytes([ord(c) for c in word])
    # print(bs)
    # print(list(bs))
    return binascii.unhexlify(to_unhexlify)


# 0x3F is question mark in hex

ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
print(ser.name)

print(ser.isOpen())
print('Enter your commands below.\r\nInsert "exit" to leave the application.')


def settup():
    pass

def repl_loop():
    pass


def send_cmd(cmd):
    pass


while True:
    foo = input(">> ")
    # foo = bytes([ord(c) for c in foo])
    foo = parseHex(foo)
    if foo == b'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        # ser.write(foo + b'\r\n')
        ser.write(foo)
        out = b''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != b'':

            # print(out.decode("utf-8"))
            print(out)




# i2c = I2C.I2C(portname='/dev/ttyUSB0')
# i2c.speed = '5kHz'

# http://dangerousprototypes.com/blog/2009/10/09/bus-pirate-raw-bitbang-mode/
# https://gist.github.com/kost/592e96381ca3c97abe21

# picocom -b 115200 -r -l /dev/ttyUSB0
# we have RAM (0x08-0x3f). , 56 bytes
# Ernie is in ascii , 0x45, 0x72, 0x63, 0x69, 0x65
# 0xD0(0x68 W) 0xD1(0x68 R)

# [0xD0 0x08 0x45 0x72 0x63 0x69 0x65]
# write 'Ernie' to 0x08

# ?[0xD0 0x08 [0xD1 rrrrr]
# I2C>[0xD0 0x08 [0xD1 rrrrr]
# I2C START BIT
# WRITE: 0xD0 ACK
# WRITE: 0x08 ACK
# I2C START BIT
# WRITE: 0xD1 ACK
# READ: 0x45
# READ:  ACK 0x72
# READ:  ACK 0x63
# READ:  ACK 0x69
# READ:  ACK 0x65
# NACK
# I2C STOP BIT

# 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS
# 011000xx – Set I2C speed, 3=~400kHz, 2=~100kHz, 1=~50kHz, 0=~5kHz
# power only 010001000
# http://dangerousprototypes.com/blog/2009/10/09/bus-pirate-raw-bitbang-mode/

# -x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00

# go to raw bitbang mode
# -x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00

# go to raw i2c mode
# -x02

# set speed to 5kHz
# -x60

# power on
# -x88
# -x80
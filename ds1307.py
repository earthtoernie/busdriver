import pyBusPirateLite.I2C as I2C
import re
import binascii
import serial
import time
import sys
import lib.bp_serial_utils

# https://www.devdungeon.com/content/working-binary-data-python



if __name__ == '__main__':


    i2c_start = b'\x02'
    i2c_stop = b'\x03'

    ds1207_write_addr = b'\xD0'

    sp = lib.bp_serial_utils.init_to_i2c()


    pause = 0

    # print('***** send start expect: 0x01')
    # ret = write_bytes(sp, i2c_start, pause)
    # print(ret)
    #
    # print('***** start bulk write cmd for 6 bytes, 0x16 expect: 0x01')
    # # 0001 xxxx – Bulk I2C write, send 1 - 16 bytes(0 = 1 byte!)
    # #send 5 bytes 0001 0101 -? 0x15
    # ret = write_bytes(sp, b'\x16', pause)
    # print(ret)
    #
    #
    #
    # print('***** send write address, 0xD0 expect ack: 0x00')
    # ret = write_bytes(sp, ds1207_write_addr, pause)
    # print(ret)
    #
    # print('***** send write ram address, 0x08 expect ack: 0x00')
    # ret = write_bytes(sp, b'\x08', pause)
    # print(ret)
    #
    # print("***** send 'E' expect ack: 0x00")
    # ret = write_bytes(sp, b'E', pause)
    # print(ret)
    #
    # print("***** send 'r' expect ack: 0x00")
    # ret = write_bytes(sp, b'r', pause)
    # print(ret)
    #
    # print("***** send 'n' expect ack: 0x00")
    # ret = write_bytes(sp, b'n', pause)
    # print(ret)
    #
    # print("***** send 'i' expect ack: 0x00")
    # ret = write_bytes(sp, b'i', pause)
    # print(ret)
    #
    # print("***** send 'e' expect ack: 0x00", pause)
    # ret = write_bytes(sp, b'e')
    # print(ret)
    #
    # print('***** send stop expect: 0x01')
    # ret = write_bytes(sp, i2c_stop, pause)
    # print(ret)

    whole_thing = b'\x02\x16\xD0\x08Ernie\x03'
    ret = lib.bp_serial_utils.write_bytes(sp, whole_thing, 0)
    print(ret)

    ## write then read
    # 0x08 command
    # 0x00 write count Hi byte
    # 0x01 write count Low byte
    # 0x00 read count Hi byte
    # 0x00 read count Low byte
    # 0xD1 The actual byte stream to write, write address for ds1307
    # 0x08 ram address

    ### now write address then read
    print("****** set the pointer, response is:")
    # whole_thing = b'\x08\x00\x03\x00\x05\xD0\x08\xD1'
    whole_thing = b'\x08\x00\x02\x00\x00\xD0\x08'

    ret = lib.bp_serial_utils.write_bytes(sp, whole_thing, 0)
    print(ret)


    # 0x08 command
    # 0x00 write count Hi byte
    # 0x01 write count Low byte
    # 0x00 read count Hi byte
    # 0x05 read count Low byte
    # 0xD1 The actual byte stream to write, write address for ds1307

    print("****** response is:")
    # whole_thing = b'\x08\x00\x03\x00\x05\xD0\x08\xD1'
    whole_thing = b'\x08\x00\x01\x00\x05\xD1'

    ret = lib.bp_serial_utils.write_bytes(sp, whole_thing, 1)
    print(ret)




    # picocom -b 115200 -r -l /dev/ttyUSB0
    # we have RAM (0x08-0x3f). , 56 bytes
    # Ernie is in ascii , 0x45, 0x72, 0x63, 0x69, 0x65
    # 0xD0(0x68 W) 0xD1(0x68 R)

    # [0xD0 0x08 0x45 0x72 0x63 0x69 0x65]

    # WRITE: 0xD0 ACK
    # WRITE: 0x08 ACK
    # WRITE: 0x45 ACK
    # WRITE: 0x7 ACK
    # WRITE: 0x63 ACK
    # WRITE: 0x69 ACK
    # WRITE: 0x65 ACK
    # I2C STOP BIT

    # a turd [0xA0 0x08 0x45 0x72 0x63 0x69 0x65]

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




# 0x3F is question mark in hex
# 0x3F is question mark in hex
# 0x0A is \n (LF)
# 0x0D is \r (CR)
# -x3F-x0D-x0A


# i2c = I2C.I2C(portname='/dev/ttyUSB0')
# i2c.speed = '5kHz'

# http://dangerousprototypes.com/blog/2009/10/09/bus-pirate-raw-bitbang-mode/
# https://gist.github.com/kost/592e96381ca3c97abe21



# 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS
# 011000xx – Set I2C speed, 3=~400kHz, 2=~100kHz, 1=~50kHz, 0=~5kHz
# power only 010001000
# http://dangerousprototypes.com/blog/2009/10/09/bus-pirate-raw-bitbang-mode/

# -x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00
# gets us b'BBIO1'

# go to raw bitbang mode
# -x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00-x00

# go to raw i2c mode
# -x02
# responds b'I2C1'

# set speed to 5kHz
# -x60
# responds b'`'
# responds b'\x01'


# power on
# -x88
# -x80
"""
stuff to tak to the bus pirate over serial port
"""

import sys
import time

try:
    import serial.tools.list_ports as list_ports
except ImportError:
    raise ImportError('Pyserial version with serial.tools.list_port required')

import serial

def get_port():
    """Detect Buspirate and return first detected port

    Returns
        -------
    str
    First valid portname (ie: ttyUSB0)
    """
    pname=None
    # the API in version 2 and 3 is different
    if serial.VERSION[0] == '2':
        ports = list_ports.comports()
        for port in ports:
            if len(port) == 3 and '0403:6001' in port[2]:
                pname = port[0]
            if len(port) == 3 and 'VID_0403+PID_6001' in port[2]:
                pname = port[0]
    else:
        ports = list_ports.comports()
        for port in ports:
            if hasattr(port, 'pid') and hasattr(port, 'vid'):
                if port.vid == 1027 and port.pid == 24577:
                    pname = port.name

    if pname is None:
        raise FileNotFoundError('no bus pirate found')

    return pname

def write_bytes(ser, bytes, wait_secs=.1):
    """writes bytes then wait for a reply"""
    ser.write(bytes)
    out = b''
    time.sleep(wait_secs)
    while ser.inWaiting() > 0:
        out += ser.read(1)

    if out != b'':
        # print(out.decode("utf-8"))
        return out
    else:
        return None

def init_to_i2c():
    bp_port = get_port()
    if bp_port is None:
        sys.exit('err, cant find bus pirate')

    sp = serial.Serial(port='/dev/' + bp_port, baudrate=115200)

    # eval_loop(sp)

    # return_bytes = write_bytes(sp, b'?\n\r',1)
    # print(return_bytes)

    max_tries = 25
    for x in range(max_tries):
        return_bytes = write_bytes(sp, b'\x00', .01)
        # print('hhh ' + str(return_bytes))
        if return_bytes == b'BBIO1':
            inner_return_bytes = write_bytes(sp, b'\x0F\r\n', .1)
            # print('jjj' + str(foo))
            break
    else:
        sys.exit("too many attempts to send '0x00'")

    ############
    for x in range(max_tries):
        return_bytes = write_bytes(sp, b'\x00', .01)
        # print('hhh ' + str(return_bytes))
        if return_bytes == b'BBIO1':
            break
    else:
        sys.exit("too many attempts to send '0x00'")

    print('ok good we now in BBIO1')



    # print('**** resetting bus pirate, expecting "???"')
    # return_bytes = write_bytes(sp, b'\x0F\r\n')
    # print(return_bytes)
    #
    # print('**** entering raw bibnag, expecting "BBIOx"')
    # return_bytes = write_bytes(sp, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    # print(return_bytes)


    print('**** entering I2C, expecting "I2Cx"')
    return_bytes = write_bytes(sp, b'\x02')
    print(return_bytes)

    print('**** turning on the lights, check led and "0x01" ')
    # 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS ---> 01001000

    return_bytes = write_bytes(sp, b'\x48')
    print(return_bytes)

    return sp

    # print('****sending CR-LF 10 times')
    # return_bytes = write_bytes(sp, b'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n#\r\n')
    # print(return_bytes)

def eval_loop(ser):
    while True:
        foo = input(">> ")
        # foo = bytes([ord(c) for c in foo])
        foo = parse_hex(foo)
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


## todo below
## me thinks that this is ds1307 specific (def i2c specific) so move to a new folder




def send_ernie(sp):
    """
    send Ernie to address 0x08
    :param sp:
    :return:
    """

"""
stuff to tak to the bus pirate over serial port
"""

import sys
import time
# import serial.tools.list_ports as list_ports
import serial.tools.list_ports
from collections import namedtuple
# http://dangerousprototypes.com/docs/Bitbang



vid_pid_bp3 = (0x0403, 0x6001)
vid_pid_bp4 = (0x04d8, 0xfb00)

# last_used_port_name = None
# last_used_port = None

PirateId = namedtuple('PirateId', ['type_', 'dev'])


class BusPirate:
    """BusPirate class encapsulates a connections to *one single bus pirate*"""

    ## attributes
    #  __myPirateId , this is used before we establish a connection
    #  __myPiratePort


    def __init__(self, dev=None, preferred='bp4'):
        """
        :param dev: takes a PirateID, default is none (recommended) and we will choose the first found
        object can not be initialized if the port does not exist
        throws: IOError
        """

        pirates = BusPirate.__probe_for_pirates()
        if dev is None:


            bp3s = [p for p in pirates if p.type_=='bp3']
            bp4s = [p for p in pirates if p.type_=='bp4']

            if preferred == 'bp4' and len(bp4s) >= 1:
                self.__myPirateId = bp4s[0]
            elif preferred == 'bp4' and len(bp3s) >= 1:
                self.__myPirateId = bp3s[0]
            elif preferred == 'bp3' and len(bp3s) >= 1:
                self.__myPirateId = bp3s[0]
            elif preferred == 'bp3' and len(bp4s) >= 1:
                self.myPirateId = bp4s[0]
            else:
                raise IOError('could not find a reference *any* bus pirate')


        else:
            chosen_bp = [p for p in pirates if p.type_=='bp4']
            if len(chosen_bp) == 1:
                self.__myPirateId = chosen_bp
            else:
                raise IOError('port that was passed in does not exist')
        self.__myPiratePort = None



    @staticmethod
    def __probe_for_pirates():
        """

        :return: list of named tuples, ie if two are connected:
        [PirateId(type_='bp3', dev='ttyUSB0'), PirateId(type_='bp4', dev='ttyACM0')]

        """

        # PirateId = namedtuple('PirateId', 'type dev')
        ports = serial.tools.list_ports.comports()
        bp_ports =[]

        for port in ports:
            if hasattr(port, 'pid') and hasattr(port, 'vid') and port.pid is not None and port.vid is not None:
                print('merp')
                print('vid: {0:x} , pid: {1:x}'.format(port.vid, port.pid))
                if (port.vid, port.pid) == vid_pid_bp4:
                    print('found bus pirate 4')
                    print(port.name)
                    bp_ports.append(PirateId('bp4', port.name))
                elif (port.vid, port.pid) == vid_pid_bp3:
                    bp_ports.append(PirateId('bp3', port.name))

        return bp_ports

    @property
    def myPiratePort(self):
        return self.__myPiratePort

    @property
    def myPirateId(self):
        return self.__myPirateId

    def initConnection(self, baudrate=115200):
        self.__myPiratePort = serial.Serial(port='/dev/' + self.myPirateId.dev, baudrate=baudrate)


    def write_bytes(self, bytes=b'', wait_secs=.1):
        """writes bytes then wait for a reply"""
        ser = self.myPiratePort
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


    def init_to_BBIO1(self):
        # eval_loop(sp)

        # return_bytes = write_bytes(sp, b'?\n\r',1)
        # print(return_bytes)

        max_tries = 25
        for x in range(max_tries):
            return_bytes = self.write_bytes( b'\x00', .01)
            # print('hhh ' + str(return_bytes))
            if return_bytes == b'BBIO1':
                inner_return_bytes = self.write_bytes( b'\x0F\r\n', .1)
                # print('jjj' + str(foo))
                break
        else:
            sys.exit("too many attempts to send '0x00'")

        ############
        for x in range(max_tries):
            return_bytes = self.write_bytes( b'\x00', .01)
            # print('hhh ' + str(return_bytes))
            if return_bytes == b'BBIO1':
                break
        else:
            sys.exit("too many attempts to send '0x00'")

        print('ok good we now in BBIO1')


    def go_to_i2c(self):
        # init_to_BBIO1()

        # print('**** resetting bus pirate, expecting "???"')
        # return_bytes = write_bytes(sp, b'\x0F\r\n')
        # print(return_bytes)
        #
        # print('**** entering raw bibnag, expecting "BBIOx"')
        # return_bytes = write_bytes(sp, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        # print(return_bytes)

        print('**** entering I2C, expecting "I2Cx"')
        return_bytes = self.write_bytes( b'\x02')
        print(return_bytes)

        print('**** turning on the lights, check led and "0x01" ')
        # 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS ---> 01001000

        return_bytes = self.write_bytes( b'\x48')
        # print(return_bytes)

        return

        # print('****sending CR-LF 10 times')
        # return_bytes = write_bytes(sp, b'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n#\r\n')
        # print(return_bytes)

    def go_to_spi(self):
        print('**** entering SPI, expecting "SPI1"')
        return_bytes = self.write_bytes( b'\x01')
        print(return_bytes)

        print('**** turning on the lights, check led and "0x01" ')

        # spi config 0b10001010
        self.write_bytes(b'\x8a')

        #0100wxyz - Configure peripherals -> 0b01001111
        return_bytes = self.write_bytes(b'\x4f')


    def go_to_raw_wire(self):
        print('**** entering I2C, expecting "RAWx"')
        return_bytes = self.write_bytes( b'\x05')
        print(return_bytes)
        print('**** turning on the lights, check led and "0x01" ')
        # 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS ---> 01001000
        return_bytes = self.write_bytes( b'\x48')
        # print(return_bytes)
        return






# def eval_loop(ser):
#     while True:
#         foo = input(">> ")
#         # foo = bytes([ord(c) for c in foo])
#         foo = parse_hex(foo)
#         if foo == b'exit':
#             ser.close()
#             exit()
#         else:
#             # send the character to the device
#             # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
#             # ser.write(foo + b'\r\n')
#             ser.write(foo)
#             out = b''
#             # let's wait one second before reading output (let's give device time to answer)
#             time.sleep(1)
#             while ser.inWaiting() > 0:
#                 out += ser.read(1)
#
#             if out != b'':
#                 # print(out.decode("utf-8"))
#                 print(out)



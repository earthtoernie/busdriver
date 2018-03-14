from bp.bp_serial_utils import BusPirate
import time

# http://dangerousprototypes.com/docs/SPI_(binary)

class St7565:
    pass


class St7565Pirate(BusPirate, St7565):

    # todo this should go somewhere else
    def write_bytes_spi(self, data=b''):
    # def write_bytes(self, bytes=b'', wait_secs=.1):
    # uses '00000100 - Write then read' command
        ser = self.myPiratePort
        # ser.write(bytes)
        _ = ser.write(b'\x04') # Write then read mode
        print('entering write than read mode: {}'.format(_))
        _ = ser.write(b'\x00') # bytes to write (high)
        ser.write(b'\x01') # bytes to write (low)
        ser.write(b'\x00') # bytes to read (high)
        ser.write(b'\x00') # bytes to read (low)
        print(data)
        _ = ser.write(data)
        return _


    # # time.sleep(wait_secs)
    #     while ser.inWaiting() > 0:
    #         out += ser.read(1)
    #
    #     if out != b'':
    #         # print(out.decode("utf-8"))
    #         return out
    #     else:
    #         return None

    def io_init(self):
        _ = self.write_bytes_spi(b'\xe2') # Internal reset
        print(_)
        _ = self.write_bytes_spi(b'\xa2') # Sets the LCD drive voltage bias ratio ## TODO: i set to a2 instead of a3
        ##A2: 1/9 bias
        ##A3: 1/7 bias (ST7565V)
        _ = self.write_bytes_spi(b'\xa0') # Sets the display RAM address SEG output correspondence
        print(_)
        ##A0: normal
        ##A1: reverse

        _ = self.write_bytes_spi(b'\xc8') # Select COM output scan direction
        print(_)
        ##C0~C7: normal direction
        ##C8~CF: reverse direction

        _ = self.write_bytes_spi(b'\xa4') # Display all points ON/OFF
        print(_)
        ##A4: normal display
        ##A5: all points ON

        _ = self.write_bytes_spi(b'\xa6') # Sets the LCD display normal/inverted
        print(_)
        ##A6: normal
        ##A7: inverted

        _ = self.write_bytes_spi(b'\x2F') # select internal power supply operating mode
        print(_)
        ##28~2F: Operating mode

        _ = self.write_bytes_spi(b'\x60') # Display start line set
        print(_)
        ##40~7F Display start address

        _ = self.write_bytes_spi(b'\x27') # V5 voltage regulator internal resistor ratio set(contrast)
        print(_)
        ##20~27 small~large

        _ = self.write_bytes_spi(b'\x81') # Electronic volume mode set
        print(_)
        ##81: Set the V5 output voltage

        _ = self.write_bytes_spi(b'\x30') # Electronic volume register set
        print(_)
        ##00~3F: electronic volume register

        _ = self.write_bytes_spi(b'\xAF')
        print(_)
        ##    0b10101111: ON \xAF
        ##    0b10101110: OFF
        print('see ya later')

        pass

    def foo(self):
        pass


    def lcd_init(self):
        pass
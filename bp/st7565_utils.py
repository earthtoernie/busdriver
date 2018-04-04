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
    #http://dangerousprototypes.com/docs/SPI_(binary)
    #https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
        ser = self.myPiratePort
        # ser.write(bytes)
        if(len(data) == 1): #special case if we are writing only 1 byte
            _ = ser.write(b'\x04') # Write then read mode
            print('entering write than read mode: {}'.format(_))
            _ = ser.write(b'\x00') # bytes to write (high)
            ser.write(b'\x01') # bytes to write (low)
            ser.write(b'\x00') # bytes to read (high)
            ser.write(b'\x00') # bytes to read (low)
            print(data)
            _ = ser.write(data)
        else:
            # again use 'write then read' command
            assert len(data) < 0xFFFF
            lsb = bytes([len(data) & 0x00ff]) # for len
            print("&&&&&&&&&&&&&&", lsb)
            # print("&&&&&&&&&&&&&&", (len(data) & 0xff00) >> 8 )
            msb = bytes([(len(data) & 0xff00) >> 8]) # for len
            payload = b''.join([
                b'\x04',  # Write then read mode
                msb, # bytes to write (high)
                lsb, # bytes to write (low)
                b'\x00', # bytes to read (high)
                b'\x00', # bytes to read (low)
                data
            ])
            print('^^^^^^^^^^^^')
            print(','.join('{:02x}'.format(x) for x in payload))
            _ = ser.write(payload)  # Write then read mode
            print('result from bulk write: {}'.format(_))

        return _

    def set_aux(self, value=False):
        ser = self.myPirateId
        # 0100wxyz - Configure peripherals w=power, x=pull-ups, y=AUX, z=CS


    # # time.sleep(wait_secs)
    #     while ser.inWaiting() > 0:
    #         out += ser.read(1)
    #
    #     if out != b'':
    #         # print(out.decode("utf-8"))
    #         return out
    #     else:
    #         return None

    def io_init_individual(self):
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

        _ = self.write_bytes_spi(b'\xAF') #display ON
        print(_)
        ##    0b10101111: ON \xAF
        ##    0b10101110: OFF

        print('now writing stuff to screen ')


        print('see ya later')

        pass

    def io_init(self):

        ser = self.myPiratePort

        payload_init = b''.join([
            b'\xe2',  # Internal reset
            b'\xa2',  # Sets the LCD drive voltage bias ratio ## TODO: i set to a2 instead of a3
            b'\xa0',  # Sets the display RAM address SEG output correspondence
            b'\xc8',  # Select COM output scan direction
            b'\xa4',  # Display all points ON/OFF
            b'\xa7',  # Sets the LCD display normal/inverted
            b'\x2F',  # select internal power supply operating mode
            b'\x60',  # Display start line set
            b'\x27',  # V5 voltage regulator internal resistor ratio set(contrast)
            b'\x81',  # Electronic volume mode set
            b'\x30',  # Electronic volume register set
            # b'\x40',  # go back to the top left of the display
            b'\xAF',  # display ON
            b'\xB0',
            b'\x10',
            b'\x00'
        ])

        # 0b1010011X  where X is 1 for reversed or 0 for normal.
        # A7 is reverse

        # set A0 low so we are writing to data registers

        # 0100wxyz-Configure peripherals w=power, x=pull-ups, y=AUX, z=CS

        a0_low = b'\x49' # 0100 1001
        a0_high = b'\x4b' # 0100 1011

        ser.write(a0_low)

        self.write_bytes_spi(payload_init)

        ser.write(a0_high)



        # ser.write(a0_low)
        # _ = self.write_bytes_spi(payload_init)
        # ser.write(a0_high)
        # print(_)

        payload_data = b''.join([
            b'\x00',
        ])*132



        self.write_bytes_spi(payload_data)
        ser.write(a0_low)

        foo1 =  b''.join([b'\xB0', b'\x10', b'\x00',])

        ser.write(a0_low)
        # _ = self.write_bytes_spi(payload_data)
        # ser.write(a0_high)

    def foo(self):
        pass


    def lcd_init(self):
        pass
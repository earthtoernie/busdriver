import serial
import time

ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
print(ser.name)

print(ser.isOpen())
print('Enter your commands below.\r\nInsert "exit" to leave the application.')

# foo=1

while True:
    foo = input(">> ")
    foo = bytes([ord(c) for c in foo])
    if foo == b'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(foo + b'\r\n')
        out = b''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != b'':

            print(out.decode("utf-8"))
# ser.write(b'?')
#
# RFIDNum = ser.readline()
#
# print(RFIDNum)

# python miniterm.py port /dev/ttyUSB0 baudrate 115200
# python miniterm.py /dev/ttyUSB0 115200
# picocom -b 115200 -r -l /dev/ttyUSB0


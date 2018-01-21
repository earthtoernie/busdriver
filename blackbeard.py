#!/usr/bin/python3

import argparse
import fileinput

# takes a shell and a file

# if __name__ == '__main__':
#     print('hello world')

import fileinput
import re
import sys
import argparse

import lib.bp_serial_utils

# https://gist.github.com/martinth/ed991fb8cdcac3dfadf7

#

# def grep(lines, regexp):
#     return (line for line in lines if regexp.search(line))

# def main(args):
#     if len(args) < 1:
#         print("Usage: grep.py PATTERN [FILE...]", file=sys.stderr)
#         return 2
#     regexp = re.compile(args[0])
#     input_lines = fileinput.input(args[1:])
#     for output_line in grep(input_lines, regexp):
#         sys.stdout.write(output_line)

bus_types = ['i2c', 'st7565_spi'] # testing ST7565 graphic lcd specific spi device
morpher_types = ['none', 'ds1307', 'st7565']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="send an receive commands with Bus Pirate")
    parser.add_argument('-l', '--locate', action="store_true", default=False, help='locate bus pirate and exit')
    parser.add_argument('-t', '--terminal', action="store_true", default=False, help='keep terminal open')
    parser.add_argument('-p', '--proto', action="store", choices=bus_types, help='bus types')
    parser.add_argument('-m', '--morpher', action="store", choices=morpher_types, help='NOT YET IMPLEMENTED.. dsl for certain devices')
    parser.add_argument('file', nargs='?', action='store', help='file to send (also works with stdin)')
    args = parser.parse_args()
    # print(args)

    # see if we just want info about the Bus Pirate.. then exit

    if args.locate:
        try:
            bp_port = lib.bp_serial_utils.get_port()
            print('Bus Pirate found on: {}'.format(bp_port))
        except FileNotFoundError:
            print(' no Bus Pirate found')
        finally:
            sys.exit('goodbye you pirate')

    # if there is no commands and no file or stdin and --terminal is not added, nothing to do so exit
    # note this will hang till EOF (Ctrl d) is entered

    input_lines = fileinput.input(args.file)

    print
    if args.proto == 'i2c':
        print('doing i2c stuff now')

        if(args.terminal):
            print('goto terminal')


    # print('we have this many lines: ', str(len(input_lines)))
    for line in input_lines:
        # print(line)
        pass
    sys.exit(' nothing to do, goodbye')



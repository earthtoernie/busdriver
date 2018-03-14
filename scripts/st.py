import argparse
from bp.st7565_utils import St7565Pirate


def run_it(string_arg):
    try:
        myPirate = St7565Pirate()
    except IOError:
        print('can not find a bus pirate')
    myPirate.initConnection()
    myPirate.init_to_BBIO1()
    myPirate.go_to_spi()
    myPirate.io_init()

def main():
    parser = argparse.ArgumentParser(description='write to st7565 lcd screen',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    action_group=parser.add_argument_group()
    action_group.add_argument('--string', type=str, default='hello world', help='simple string to display')
    action_group.add_argument('--picture', type=str, help='not implemented yet')
    action_group.add_argument('--animation', type=str, help='not sure how to implement this , not implemented yet')

    args = parser.parse_args()
    # print(args)

    if args.string:
        print('about to display: {}'.format(args.string))
        run_it(args.string)



if __name__ == '__main__':
    main()
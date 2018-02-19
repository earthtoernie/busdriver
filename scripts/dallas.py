import argparse
import sys
import time
# import bp.bp_serial_utils as bp
from bp.rtc_utils import RtcPirate

def main():
    # https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments
    parser = argparse.ArgumentParser(description="set and get the time, works with Dallas rtc' (now Maxim)",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('action', type=str, choices=['set', 'get', 'poll'], default='get',
                        help='read or write time, poll reads time repeatedly ')
    parser.add_argument('--rtc', type=str, choices=['1307', '3231'], default=1307, help=' ')

    parser.add_argument('--date',
                        help="date and time to set to, matches format returned by gnu 'date',"
                             "ie 'Sat Feb 17 19:58:04 EST 2018', time zone must be present as 3 chars "
                                "but is ignored so, 'XXX' will do "
                                '**pro tip**: set now date with bp_dallas set --date="`date`"', type=str
                        )
    parser.add_argument('--interval', type=float, default=1.0, help='time, in seconds to poll the clock')
    #TODO add option to change bus speed
    #TODO add option to use a particular port

    args = parser.parse_args()

    print(args)

    if args.action=='get':
        try:
            myPirate = RtcPirate()
        except IOError:
            print('can not find a bus pirate')
            sys.exit(1)
        print('**using', myPirate.myPirateId)
        myPirate.initConnection()
        myPirate.init_to_BBIO1()
        myPirate.go_to_i2c()
        time = myPirate.readTime()
        # http://strftime.org/
        #time.tzname
        print('{:%a %b %-d %H:%M:%S {} %Y}'.format(time, 'XXX'))




        print('enjoy your *time* sir')
        sys.exit(0)

    if args.action=='poll':
        print('waiting for seconds: {}'.format(args.interval))
        print('press Control-C to exit')

        try:
            myPirate = RtcPirate()
        except IOError:
            print('can not find a bus pirate')
            sys.exit(1)
        myPirate.initConnection()
        myPirate.init_to_BBIO1()
        myPirate.go_to_i2c()
        while(True):
            try:
                # myPirate.initConnection()
                # myPirate.init_to_BBIO1()
                # myPirate.go_to_i2c()
                time = myPirate.readTime()
                print('{:%a %b %-d %H:%M:%S {} %Y}'.format(time, 'XXX'))
            except KeyboardInterrupt:
                sys.exit(0)
    if args.action=='set':
        print('entered the *date* string: {}'.format(args.date))
        print('*time* has been set')
        sys.exit(0)

if __name__ == '__main__':
    print('merp')


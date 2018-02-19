import datetime
from bp.bp_serial_utils import BusPirate
import bp.i2c_utils

class Rtc:
    ds1207_write_addr = b'\xD0'
    ds1207_read_addr = b'\xD1'
    ds1207_start_ram_reg = b'\x08'
    ds1207_start_timedate_reg = b'\x00'


    @staticmethod
    def _gen_rtc_regs(python_time, twenty_four=True):
        second = python_time.second % 10
        second10 = python_time.second // 10
        addr0_second = bytes([(second10 * 16) | second])  # mult 16 same as bitshift by 4

        minute = python_time.minute % 10
        minute10 = python_time.minute // 10
        addr1_minute = bytes([(minute10 * 16) | minute])

        # note. but 6 must be low always to be in 24 hour mode
        hour = python_time.hour % 10
        hour10 = python_time.hour // 10
        addr2_hour = bytes([(hour10 * 16) | hour])

        day = python_time.weekday()
        print('day is...')
        addr3_day = bytes([day])

        date = python_time.day % 10
        date10 = python_time.day // 10
        addr4_date = bytes([(date10 * 16) | date])

        month = python_time.month % 10
        month10 = python_time.month // 10
        addr5_month = bytes([(month10 * 16) | month])

        year = (python_time.year - 2000) % 10
        year10 = (python_time.year - 2000) // 10
        addr6_year = bytes([(year10 * 16) | year])

        return [addr0_second, addr1_minute, addr2_hour, addr3_day, addr4_date, addr5_month, addr6_year]
    pass


    @staticmethod
    def gen_datetime(rtc_regs_time):
        # print(rtc_regs_time)
        #todo assert that the format passed is correct

        # we bitwise and with 240 to get msb and bitwise and with 15 to get lsb
        pass
        #some_time = datetime.datetime(2003, 8, 4, 13, 30, 45)
        second_ls_nibble = rtc_regs_time[0]
        second_ms_nibble = rtc_regs_time[0]
        second = ((int(rtc_regs_time[0][0]) & 240) // 16)*10 + (int(rtc_regs_time[0][0]) & 15)
        minute = ((int(rtc_regs_time[1][0]) & 240) // 16)*10 + (int(rtc_regs_time[1][0]) & 15)
        hour = ((int(rtc_regs_time[2][0]) & 240) // 16)*10 + (int(rtc_regs_time[2][0]) & 15)
        weekday = ((int(rtc_regs_time[3][0]) & 240) // 16)*10 + (int(rtc_regs_time[3][0]) & 15)
        day = (int((rtc_regs_time[4][0]) & 240) // 16)*10 + (int(rtc_regs_time[4][0]) & 15)
        month = ((int(rtc_regs_time[5][0]) & 240) // 16)*10 + (int(rtc_regs_time[5][0]) & 15)
        year = ((int(rtc_regs_time[6][0]) & 240) // 16)*10 + (int(rtc_regs_time[6][0]) & 15) + 2000

        return datetime.datetime(year, month, day, hour, minute, second)

class RtcPirate(Rtc, BusPirate): # usin the concept of mixins here, stuff implemented here needs both rtc and bus pirate functinality
    ## todo, add good errors to tell user when methods are being called in an invalid order
    #obv we have to be initialized to i2c
    def setTime(self, python_time):
        time_regs = Rtc._gen_rtc_regs(python_time)
        super(BusPirate, self).write_bytes()



    def _ram_read_write_string_test(self):
        ######################################################
        ## writes string 'Ernie' then reads and prints
        ######################################################

        # write data to a register (includes writing pointer to that register)
        payload = bp.i2c_utils.gen_write_to_reg(Rtc.ds1207_write_addr, Rtc.ds1207_start_ram_reg, b'Ernie')
        ret = self.write_bytes(payload, .1)
        # print('********** payload is: {}'.format(payload))
        # print(ret) # should be none, depending on how long we wait

        # just write the pointer to that register
        payload = bp.i2c_utils.gen_write_addr_only(Rtc.ds1207_write_addr, Rtc.ds1207_start_ram_reg)
        ret = self.write_bytes(payload, .1)
        # print('********** payload is: {}'.format(payload))
        # print(ret) # should be none, depending on how long we wait

        # now read
        payload = bp.i2c_utils.gen_read_from_reg(Rtc.ds1207_read_addr, Rtc.ds1207_start_ram_reg, 5)
        ret =self.write_bytes( payload, .1)
        # print('********** payload is: {}'.format(payload))
        # print(ret)  # should be none, depending on how long we wait
        return ret

    def write_time(self, arg):
        # write data to a register (includes writing pointer to that register)

        reg_load = b''.join(bp.rtc_utils.gen_rtc_regs(arg))
        payload = bp.i2c_utils.gen_write_to_reg(Rtc.ds1207_write_addr, Rtc.ds1207_start_timedate_reg, reg_load)
        ret = self.write_bytes( payload, .1)
        # print('********** payload is: {}'.format(payload))
        # print(ret) # should be none, depending on how long we wait
        return (ret)

    def __read_time_reg(self,):
        read_len = 7
        # just write the pointer to that register
        payload = bp.i2c_utils.gen_write_addr_only(Rtc.ds1207_write_addr, Rtc.ds1207_start_timedate_reg)
        ret = self.write_bytes(payload, .1)
        # print('********** payload is: {}'.format(payload))
        # print(ret) # should be none, depending on how long we wait

        # now read
        payload = bp.i2c_utils.gen_read_from_reg(Rtc.ds1207_read_addr, Rtc.ds1207_start_timedate_reg, read_len)
        ret = self.write_bytes(payload, .1)
        # print('********** payload is: {}'.format(payload))
        # print(ret)  # should be none, depending on how long we wait
        return (ret, ret[len(ret) - read_len:])

    def readTime(self):
        read_statusdata, read_data = self.__read_time_reg()
        # print(read_time(sp))
        time_stamp = Rtc.gen_datetime([bytes([i]) for i in list(read_data)])
        return time_stamp












if __name__ == '__main__':
    some_time = datetime.datetime(2003, 8, 4, 13, 30, 45)
    print('*********** we put this in')
    print(some_time.strftime("%a %b %-d %H:%M:%S %Y"))

    reg_time = gen_rtc_regs(some_time)

    new_some_time = gen_datetime(reg_time)
    print('???????? old and new')
    print(some_time.strftime("%a %b %-d %H:%M:%S %Y"))
    print(new_some_time.strftime("%a %b %-d %H:%M:%S %Y"))

    # print('day of the week: {} '.format(some_time.weekday()))
    # print(')))))))))))))))))))))))))))))))))))')
    # my_regs = gen_rtc_regs(some_time)
    # print(my_regs)
    #
    # for i in my_regs:
    #     print(format(int(i[0]),  '#010b'))

    # about formatting binary
    # http://fmtlib.net/latest/syntax.html
    # https://stackoverflow.com/questions/16926130/convert-to-binary-and-keep-leading-zeros-in-python
    # https://www.devdungeon.com/content/working-binary-data-python


import datetime

def gen_rtc_regs(python_time, twenty_four = True):

    second = python_time.second % 10
    second10 = python_time.second // 10
    addr0_second = bytes([(second10 * 16) | second]) # mult 16 same as bitshift by 4

    minute = python_time.minute % 10
    minute10 = python_time.minute // 10
    addr1_minute= bytes([(minute10 * 16) | minute])


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

    return[addr0_second, addr1_minute, addr2_hour, addr3_day, addr4_date, addr5_month, addr6_year]

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


import libs.bp_serial_utils
import libs.i2c_utils
import libs.rtc_utils
import datetime
import time

ds1207_write_addr = b'\xD0'
ds1207_read_addr = b'\xD1'
ds1207_start_ram_reg = b'\x08'
ds1207_start_timedate_reg = b'\x00'

def read_write_string(sp):
    ######################################################
    ## writes string 'Ernie' then reads and prints
    ######################################################

    # write data to a register (includes writing pointer to that register)
    payload = libs.i2c_utils.gen_write_to_reg(ds1207_write_addr, ds1207_start_ram_reg, b'Ernie')
    ret = libs.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait

    # just write the pointer to that register
    payload = libs.i2c_utils.gen_write_addr_only(ds1207_write_addr, ds1207_start_ram_reg)
    ret = libs.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait

    # now read
    payload = libs.i2c_utils.gen_read_from_reg(ds1207_read_addr, ds1207_start_ram_reg, 5)
    ret = libs.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret)  # should be none, depending on how long we wait
    return ret



def write_time(sp, arg):
    # write data to a register (includes writing pointer to that register)

    reg_load = b''.join(libs.rtc_utils.gen_rtc_regs(arg))
    payload = libs.i2c_utils.gen_write_to_reg(ds1207_write_addr, ds1207_start_timedate_reg, reg_load)
    ret = libs.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait
    return(ret)


def read_time(sp):
    read_len = 7
    # just write the pointer to that register
    payload = libs.i2c_utils.gen_write_addr_only(ds1207_write_addr, ds1207_start_timedate_reg)
    ret = libs.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait

    # now read
    payload = libs.i2c_utils.gen_read_from_reg(ds1207_read_addr, ds1207_start_timedate_reg, read_len)
    ret = libs.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret)  # should be none, depending on how long we wait
    return (ret, ret[len(ret) - read_len:])


if __name__ == '__main__':

    # sp = libs.bp_serial_utils.init_to_i2c()
    # read_write_string(sp)

    # sp = libs.bp_serial_utils.init_to_i2c()
    sp = libs.bp_serial_utils.get_port()
    libs.bp_serial_utils.init_to_BBIO1()
    libs.bp_serial_utils.go_to_i2c()

    # Mon Aug 4 13:30:45 2003
    # # the_time = datetime.datetime(2003, 8, 4, 13, 30, 45)
    # the_time = datetime.datetime.now()
    # ret = write_time(sp, the_time)

    time.sleep(1)


    while True:
        read_statusdata, read_data = read_time(sp)
        print(read_time(sp))
        time_stamp = libs.rtc_utils.gen_datetime([bytes([i]) for i in list(read_data)])
        # print(read_data)
        print(time_stamp)
        time.sleep(1)
    # print(read_time().strftime("%a %b %-d %H:%M:%S %Y"))

    # the_time = datetime.datetime(2003, 8, 4, 13, 30, 45)
    # reg_load = b''.join(libs.rtc_utils.gen_rtc_regs(the_time))
    # print(reg_load)






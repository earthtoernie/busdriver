import lib.bp_serial_utils
import lib.i2c_utils
import lib.rtc_utils
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
    payload = lib.i2c_utils.gen_write_to_reg(ds1207_write_addr, ds1207_start_ram_reg, b'Ernie')
    ret = lib.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait

    # just write the pointer to that register
    payload = lib.i2c_utils.gen_write_addr_only(ds1207_write_addr, ds1207_start_ram_reg)
    ret = lib.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait

    # now read
    payload = lib.i2c_utils.gen_read_from_reg(ds1207_read_addr, ds1207_start_ram_reg, 5)
    ret = lib.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    print(ret)  # should be none, depending on how long we wait



def write_time(sp, arg):
    # write data to a register (includes writing pointer to that register)

    reg_load = b''.join(lib.rtc_utils.gen_rtc_regs(arg))
    payload = lib.i2c_utils.gen_write_to_reg(ds1207_write_addr, ds1207_start_timedate_reg, reg_load)
    ret = lib.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait
    return(ret)


def read_time(sp):
    # just write the pointer to that register
    payload = lib.i2c_utils.gen_write_addr_only(ds1207_write_addr, ds1207_start_timedate_reg)
    ret = lib.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret) # should be none, depending on how long we wait

    # now read
    payload = lib.i2c_utils.gen_read_from_reg(ds1207_read_addr, ds1207_start_timedate_reg, 7)
    ret = lib.bp_serial_utils.write_bytes(sp, payload, .1)
    # print('********** payload is: {}'.format(payload))
    # print(ret)  # should be none, depending on how long we wait
    return ret


if __name__ == '__main__':

    # sp = lib.bp_serial_utils.init_to_i2c()
    # read_write_string(sp)

    sp = lib.bp_serial_utils.init_to_i2c()
    the_time = datetime.datetime(2003, 8, 4, 13, 30, 45)
    # Mon Aug 4 13:30:45 2003
    # the_time = datetime.datetime.now()
    ret = write_time(sp, the_time)
    print(ret)

    time.sleep(3)

    read_time_junk = read_time(sp)
    print(read_time_junk)
    # print(read_time().strftime("%a %b %-d %H:%M:%S %Y"))

    # the_time = datetime.datetime(2003, 8, 4, 13, 30, 45)
    # reg_load = b''.join(lib.rtc_utils.gen_rtc_regs(the_time))
    # print(reg_load)






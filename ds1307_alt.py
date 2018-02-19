import libs.bp_serial_utils
import libs.i2c_utils

if __name__ == '__main__':
    ds1207_write_addr = b'\xD0'
    ds1207_read_addr = b'\xD1'
    ds1207_start_ram_reg = b'\x08'

    sp = libs.bp_serial_utils.init_to_i2c()

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
    ret = libs.bp_serial_utils.write_bytes(sp, payload, 1)
    # print('********** payload is: {}'.format(payload))
    print(ret) # should be none, depending on how long we wait


    pause = 0
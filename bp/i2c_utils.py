# consts in bus pirate control api

# https://stackoverflow.com/questions/444591/convert-a-string-of-bytes-into-an-int-python




def gen_write_to_reg(i2c_write_addr, reg, byts): #todo make this more felxable between reg and bytes
    """ uses 'Bulk I2C write', writes reg addr and byts in same motion
    >>>gen_write_to_reg(b'\xD0', b'\x08', b'Ernie')
    b'\x02\x16\xd0\x08Ernie\x03'
    :param i2c_write_addr: (bytes type)  must be one byte long
    :param reg: (bytes type) must be 1 byte long
    :param byts: (bytes type) must be between 1 and 15 in len
    :return: result (bytes type)
    """

    # print('len is: {}'.format(len()))

    if not (1 <= len(byts) <= 15):
        raise ValueError("byts is len: {} , must be 1 <= len(byts) <= 15")
    if not (len(i2c_write_addr) == 1):
        raise ValueError("i2c_write_addr is len: {} , must be 1")
    if not (len(reg) == 1):
        raise ValueError("reg is len: {} , must be 1")

    len_bytes_for_cmd = [(len(byts) + 1)]
    # print('type is...' + str(type(len_bytes_for_cmd[0])))
    # https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3
    bulk_cmd = bytes([b'\x10'[0] | len_bytes_for_cmd[0]])
    # print('part A command is: {}'.format((b'\x10'[0]) ))
    # print('part B command is: {}'.format(len_bytes_for_cmd[0]))
    # print('bulk command is: {}'.format(bulk_cmd))

    # 0x02 BP CMD, start signal
    # 0x16 BP CMD, 0001xxxx {00010110} - Bulk I2C write, send 1-16 bytes (0=1byte!) {send 6 bytes} {reg addr + 5 chars}
    # 0xD0 ds1307 write address
    # 0x08 reg addr, start of RAM on ds1207
    # Ernie just 4 bytes
    # 0x03 BP CMD. stop signal

    return b'\x02' + bulk_cmd + i2c_write_addr + reg + byts + b'\x03'

def gen_write_addr_only(i2c_write_addr, reg): #todo make this more felxable between reg and bytes:
    """ uses 0x08 - Write then read
    >>>gen_write_addr_only(b'\xD0', b'\x08')
    b'\x08\x00\x02\x00\x00\xD0\x08'
    :param i2c_write_addr: (bytes type)  must be one byte long
    :param reg: (bytes type) must be 1 byte long
    :return: result (bytes type)
    """
    if not (len(i2c_write_addr) == 1):
        raise ValueError("i2c_write_addr is len: {} , must be 1")
    if not (len(reg) == 1):
        raise ValueError("reg is len: {} , must be 1")

    # 0x08 command
    # 0x00 write count Hi byte
    # 0x02 write count Low byte (guess it doesnt count the bus write address)
    # 0x00 read count Hi byte
    # 0x00 read count Low byte
    # 0xD0 The actual byte stream to write, write address for ds1307
    # # 0x08 reg addr, start of RAM on ds1207

    return b'\x08\x00\x02\x00\x00' + i2c_write_addr + reg

def gen_read_from_reg(i2c_read_addr, reg, len):
    # 0x08 command
    # 0x00 write count Hi byte
    # 0x01 write count Low byte
    # 0x00 read count Hi byte
    # 0x05 read count Low byte
    # 0xD1 i2c read address

    # print("****** response is:")
    # whole_thing = b'\x08\x00\x03\x00\x05\xD0\x08\xD1'

    # len_bytes_for_cmd = [(len(byts) + 1)]
    # # print('type is...' + str(type(len_bytes_for_cmd[0])))
    # # https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3
    # bulk_cmd = bytes([b'\x10'[0] | len_bytes_for_cmd[0]])

    cmd = b'\x08\x00\x01\x00' + bytes([len]) + i2c_read_addr
    # return b'\x08\x00\x01\x00\x05\xD1'
    return cmd


if __name__ == '__main__':
    rex = gen_write_to_reg(b'\xD0', b'\x08', b'Ernie')
    print(rex)
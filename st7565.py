import libs.bp_serial_utils

#
# print(libs.bp_serial_utils.get_port())
# print(libs.bp_serial_utils.get_port())
# print(libs.bp_serial_utils.get_port())
# print(libs.bp_serial_utils.get_port())
# print(libs.bp_serial_utils.get_port())
#
#
# import timeit
# t = timeit.Timer(libs.bp_serial_utils.get_port)
# print(t.timeit(1000))


if __name__ == '__main__':
    sp = libs.bp_serial_utils.get_port()
    libs.bp_serial_utils.init_to_BBIO1() ## this is bitbang mode
    libs.bp_serial_utils.go_to_raw_wire()
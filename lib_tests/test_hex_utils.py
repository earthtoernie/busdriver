import unittest
from lib import hex_utils as hu


class TestHexUtils(unittest.TestCase):
    # def test_regex_combined(self):
    #     self.assertRegex('abc', 'c')
    #     self.assertRegex('abc', 'a')
    #     self.assertRegex('abc', 'A')
    #     self.assertRegex('abc', 'b')

    def test_string_to_bytes(self):
        strings_valid = [
            '-x45-x72-x6E-x69-x65', #Ernie
            '-x52-x4F-x42', #ROB
            '-x42-x65-x72-x74', #Bert
            '' ]
        bytess_correct = [
            b'Ernie',
            b'ROB',
            b'Brt',
            b'' ]
        for str, bys in zip(strings_valid, bytess_correct):
            with self.subTest(str=str, bys=bys):
                self.assertEqual(hu.string_to_bytes(str), bys)

        invalid_args = [
            {'line': 'x52-x4F-x42', 'sep': '-x', 'case_sen_sep': False, 'case_sen_num': False}, # wrong sep one time
            {'line': '-x52-x4G-x42', 'sep': '-x', 'case_sen_sep': False, 'case_sen_num': False}, # oob hex
            {'line': '-x52-x4FF-x42', 'sep': '-x', 'case_sen_sep': False, 'case_sen_num': False}, # oob hex
        ]

        for args in invalid_args:
            with self.subTest(args=args):
                self.assertRaises(ValueError, hu.string_to_bytes, **args)

        # we don't support case_sen at this time.. only testing one case
        not_yet_supoprted_arg = {'line': '-x52-x4F-x42', 'sep': '-x', 'case_sen_sep': False, 'case_sen_num': True}
        with self.subTest(not_yet_supoprted_arg=not_yet_supoprted_arg):
            self.assertRaises(AssertionError, hu.string_to_bytes, **not_yet_supoprted_arg)
import unittest

from bbs.protocol import parse_line


class TestProtocolParse(unittest.TestCase):
    def test_alias_menu(self):
        cmd, args = parse_line("?")
        self.assertEqual(cmd, "MENU")
        self.assertEqual(args, [])

    def test_alias_read(self):
        cmd, args = parse_line("R @MSG1")
        self.assertEqual(cmd, "READ")
        self.assertEqual(args, ["@MSG1"])

    def test_read_offset(self):
        cmd, args = parse_line("READ @MSG1 OFFSET 10")
        self.assertEqual(cmd, "READ")
        self.assertEqual(args, ["@MSG1", "OFFSET", "10"])


if __name__ == "__main__":
    unittest.main()

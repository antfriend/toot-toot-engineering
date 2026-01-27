import unittest

from bbs import mpdb_lite


SAMPLE = """@AREA1 | created:1 | updated:1

id: @AREA1
kind: area
area_name: general


@MSG1 | created:2 | updated:2 | relates:in_area>@AREA1,thread_root>@MSG1

id: @MSG1
kind: message
author: dan
timestamp: 2
area_name: general
body: Hello.\nSecond line.
"""


class TestMpdbLite(unittest.TestCase):
    def test_parse_and_dump_roundtrip(self):
        nodes = mpdb_lite.parse(SAMPLE)
        self.assertEqual(len(nodes), 2)
        out = mpdb_lite.dumps(nodes)
        nodes2 = mpdb_lite.parse(out)
        self.assertEqual(len(nodes2), 2)

        # edges preserved
        msg = [n for n in nodes2 if n["_id"] == "@MSG1"][0]
        self.assertIn(("in_area", "@AREA1"), msg["edges"])


if __name__ == "__main__":
    unittest.main()

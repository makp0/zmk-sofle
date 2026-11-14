import re
import unittest
from pathlib import Path


class SplitBehaviorTests(unittest.TestCase):
    def test_ota_device_name_fits_v03_split_payload(self):
        keymap = (Path(__file__).resolve().parents[1] / "config/eyelash_sofle.keymap").read_text()
        node = re.search(r"\bota:\s*([^\s{]+)\s*\{([^}]+)\}", keymap, re.S)
        self.assertIsNotNone(node, "The OTA binding must resolve to its device node")
        name, body = node.groups()
        label = re.search(r'\blabel\s*=\s*"([^"]+)"', body)
        device_name = label.group(1) if label else name
        # v0.3 app/include/zmk/split/bluetooth/service.h: DEV_LEN=9 includes NUL.
        # central.c uses strlcpy; the peripheral must look up the untruncated name.
        self.assertLessEqual(
            len(device_name.encode("utf-8")) + 1,
            9,
            f"OTA device name {device_name!r} truncates during split forwarding",
        )


if __name__ == "__main__":
    unittest.main()

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


class OptionalHyperLayerTests(unittest.TestCase):
    def test_hyper_layer_has_a_reachable_exit_and_preserves_the_other_keys(self):
        text = (Path(__file__).resolve().parents[1] / "config/eyelash_sofle.keymap").read_text()
        nodes = list(re.finditer(r'(\w+)\s*\{\s*label\s*=\s*"([^\"]+)";(?P<body>.*?)\n\s*\};', text, re.S))
        layers = {}
        for node in nodes:
            body = node.group('body')
            if 'bindings = <' not in body:
                continue
            bindings = body.split('bindings = <', 1)[1].split('>;', 1)[0]
            layers[node.group(2)] = (body, [' '.join(x.split()) for x in re.findall(r'&[^&]+', bindings)])
        self.assertEqual(list(layers), ['main', 'windows', 'secondary', 'hardware', 'Test', 'Reserved 1', 'Reserved 2', 'Reserved 3'])
        self.assertTrue(all(len(values[1]) == 64 for values in layers.values()))
        self.assertEqual(layers['main'][1][26], '&kp ESC')
        self.assertEqual(layers['main'][1][57], '&kp DEL')
        self.assertEqual(layers['main'][1][61], '&lt SECONDARY MINUS')
        self.assertEqual(layers['secondary'][1][18], '&tog TEST')
        self.assertEqual(layers['secondary'][1][61], '&kp DEL')
        test = layers['Test'][1]
        self.assertEqual(test[57], '&kp LC(LS(LA(LGUI)))')
        self.assertTrue(all(x == '&trans' for i, x in enumerate(test) if i != 57))
        self.assertEqual(test[61], '&trans')
        self.assertEqual(test[18], '&trans')
        for name in ['Reserved 1', 'Reserved 2', 'Reserved 3']:
            self.assertIn('status = "reserved"', layers[name][0])
            self.assertTrue(all(x == '&trans' for x in layers[name][1]))


if __name__ == "__main__":
    unittest.main()

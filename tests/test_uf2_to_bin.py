import importlib.util
import struct
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "uf2_to_bin", Path(__file__).resolve().parents[1] / "scripts/uf2_to_bin.py"
)
uf2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uf2)


def block(address=uf2.APP_START, number=0, total=1, family=uf2.NRF52840):
    return (
        struct.pack("<8I", 0x0A324655, 0x9E5D5157, 0x2000, address, 256, number, total, family)
        + bytes([number + 1]) * 256
        + bytes(220)
        + struct.pack("<I", 0x0AB16F30)
    )


class ApplicationBinaryTests(unittest.TestCase):
    def test_extracts_reordered_contiguous_blocks(self):
        data = block(uf2.APP_START + 256, 1, 2) + block(total=2)
        self.assertEqual(uf2.application_binary(data), bytes([1]) * 256 + bytes([2]) * 256)

    def test_rejects_bootloader_softdevice_and_settings_writes(self):
        for address in (0, uf2.APP_START - 256, uf2.APP_END, 0xF4000):
            with self.subTest(address=address), self.assertRaises(ValueError):
                uf2.application_binary(block(address=address))

    def test_rejects_wrong_family_and_incomplete_blocks(self):
        for data in (b"", block()[:-1], block(family=0), block(total=2)):
            with self.subTest(size=len(data)), self.assertRaises(ValueError):
                uf2.application_binary(data)

    def test_rejects_gaps_overlaps_and_duplicates(self):
        for data in (
            block(uf2.APP_START + 256),
            block(total=2) + block(uf2.APP_START + 512, 1, 2),
            block(total=2) + block(uf2.APP_START + 128, 1, 2),
            block(total=2) + block(number=1, total=2),
            block(total=2) + block(uf2.APP_START + 256, 0, 2),
        ):
            with self.subTest(data=data[:32]), self.assertRaises(ValueError):
                uf2.application_binary(data)

    def test_rejects_corrupt_magic_flags_and_size(self):
        for position, value in ((0, 0), (508, 0), (8, 0x2001), (16, 477)):
            data = bytearray(block())
            struct.pack_into("<I", data, position, value)
            with self.subTest(position=position), self.assertRaises(ValueError):
                uf2.application_binary(data)


if __name__ == "__main__":
    unittest.main()

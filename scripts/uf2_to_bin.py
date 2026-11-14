"""Extract only contiguous nRF52840 application blocks for this Eyelash board."""

import argparse
import struct
from pathlib import Path

APP_START = 0x26000
APP_END = 0xEC000
NRF52840 = 0xADA52840


def application_binary(data: bytes) -> bytes:
    if not data or len(data) % 512:
        raise ValueError("UF2 must contain complete 512-byte blocks")
    count = len(data) // 512
    chunks = {}
    block_numbers = set()
    for offset in range(0, len(data), 512):
        block = data[offset : offset + 512]
        magic0, magic1, flags, address, size, number, total, family = struct.unpack(
            "<8I", block[:32]
        )
        if (magic0, magic1) != (0x0A324655, 0x9E5D5157) or struct.unpack(
            "<I", block[508:]
        )[0] != 0x0AB16F30:
            raise ValueError("Invalid UF2 magic")
        if flags != 0x2000 or family != NRF52840:
            raise ValueError("Expected flash blocks with nRF52840 family ID only")
        if total != count or number >= count or number in block_numbers:
            raise ValueError("Missing, duplicate or inconsistent UF2 block numbers")
        if not 0 < size <= 476 or address < APP_START or address + size > APP_END:
            raise ValueError("Payload outside the Eyelash application partition")
        if address in chunks:
            raise ValueError("Duplicate UF2 destination address")
        block_numbers.add(number)
        chunks[address] = block[32 : 32 + size]

    result = bytearray()
    for address, payload in sorted(chunks.items()):
        if address != APP_START + len(result):
            raise ValueError("Application must start at 0x26000 with no gaps or overlaps")
        result.extend(payload)
    return bytes(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("uf2", type=Path)
    parser.add_argument("binary", type=Path)
    args = parser.parse_args()
    try:
        payload = application_binary(args.uf2.read_bytes())
    except ValueError as error:
        parser.error(str(error))
    args.binary.write_bytes(payload)
    print(f"Wrote {len(payload)} application bytes at {APP_START:#x}")

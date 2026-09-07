#!/usr/bin/env python3
"""Build an ath10k board-2.bin container from per-variant board.bin files.

ath10k looks up calibration by a name string built in
ath10k_core_create_board_name(); for WCN3990 on the snoc bus that is

    bus=snoc,qmi-board-id=<x>,qmi-chip-id=<x>[,variant=<v>]

where the variant comes from the device tree property
qcom,ath10k-calibration-variant.  Shipping one board-2.bin holding every
joan variant lets the driver pick the right calibration itself instead of
the packaging having to guess the model.

Format (drivers/net/wireless/ath/ath10k/hw.h):
    magic "QCA-ATH10K-BOARD\0"
    then 4-byte-aligned TLVs: __le32 id, __le32 len, data
      id 0 = ATH10K_BD_IE_BOARD, whose data is itself sub-TLVs:
        id 0 = ATH10K_BD_IE_BOARD_NAME
        id 1 = ATH10K_BD_IE_BOARD_DATA

Usage: tools-make-board-2.py OUT.bin NAME=FILE [NAME=FILE ...]
"""
import struct
import sys

MAGIC = b"QCA-ATH10K-BOARD\x00"
BD_IE_BOARD = 0
BD_IE_BOARD_NAME = 0
BD_IE_BOARD_DATA = 1


def pad4(b: bytes) -> bytes:
    return b + b"\x00" * (-len(b) % 4)


def tlv(ie_id: int, payload: bytes) -> bytes:
    return struct.pack("<II", ie_id, len(payload)) + pad4(payload)


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    out, pairs = argv[1], argv[2:]

    # The kernel does magic_len = ALIGN(strlen(MAGIC) + 1, 4) before walking
    # the TLV stream, so the 17-byte magic is padded to 20.  Without this the
    # second and later entries land misaligned and fail to parse.
    blob = bytearray(pad4(MAGIC))
    for pair in pairs:
        # Board names contain "=" themselves (bus=snoc,qmi-board-id=...),
        # so split on the LAST separator, not the first.
        name, _, path = pair.rpartition("=")
        if not name or not path:
            sys.exit(f"expected NAME=FILE, got {pair!r}")
        with open(path, "rb") as fh:
            data = fh.read()
        body = tlv(BD_IE_BOARD_NAME, name.encode()) + tlv(BD_IE_BOARD_DATA, data)
        blob += tlv(BD_IE_BOARD, body)
        print(f"  + {name}  ({len(data)} bytes from {path})")

    with open(out, "wb") as fh:
        fh.write(blob)
    print(f"wrote {out} ({len(blob)} bytes)")


if __name__ == "__main__":
    main(sys.argv)

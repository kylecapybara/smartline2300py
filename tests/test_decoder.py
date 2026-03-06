"""Unit tests for Smartline frame decoding."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pysmartline.decoder import decode_measurement


def test_decode_measurement_returns_float_and_flags() -> None:
    """Decoder returns expected value/flag types for a valid 5-byte frame."""
    frame = [0x20, 0x00, 0x00, 0x00, 0x00]

    value, start_flag, error_flag = decode_measurement(frame)

    assert isinstance(value, float)
    assert isinstance(start_flag, bool)
    assert isinstance(error_flag, bool)

"""Binary frame decoding for the Knauer Smartline detector."""

import math
from typing import Sequence, Tuple


def decode_measurement(p_buffer: Sequence[int]) -> Tuple[float, bool, bool]:
    """Decode a 5-byte Smartline detector frame.

    Params
    ----------
    p_buffer:
        signal measurement from the smarline device

    Returns
    -------
    tuple
        ``(value, start_flag, error_flag)`` where:
        - ``value`` is the decoded refractive-index signal (mRIU scaling),
          or ``0.0`` when ``error_flag`` is set.
        - ``start_flag`` is ``True`` when the start bit is set.
        - ``error_flag`` is ``True`` when the error bit is set.
    """
    if len(p_buffer) != 5:
        raise ValueError("p_buffer must contain exactly 5 bytes")

    frame = []
    for byte in p_buffer:
        if not isinstance(byte, int):
            raise TypeError("p_buffer must contain integers")
        if byte < 0 or byte > 255:
            raise ValueError("byte values must be in range 0..255")
        frame.append(byte)

    fl_phipho_start = 0x20
    fl_phipho_error = 0x10

    start_flag = bool(frame[0] & fl_phipho_start)
    error_flag = bool(frame[0] & fl_phipho_error)

    mantissa = (frame[3] >> 1)
    mantissa |= frame[2] << 6
    mantissa |= frame[1] << 13
    mantissa |= (frame[0] & 0x0F) << 20

    if mantissa & 0x00800000:
        mantissa -= 1 << 24

    raw_exp = (frame[4] | (frame[3] << 7)) & 0xFF
    exponent = raw_exp - 256 if raw_exp >= 0x80 else raw_exp

    if error_flag:
        return 0.0, start_flag, error_flag

    value = 1000.0 * math.ldexp(mantissa, exponent - 23)
    return float(value), start_flag, error_flag

"""Streaming acquisition helpers for Smartline measurements."""

import time
from typing import Iterator, Optional, Protocol, Tuple

from .decoder import decode_measurement


class FrameReader(Protocol):
    """Protocol describing the detector interface used by acquisition."""

    def read_frame(self) -> Optional[bytes]:
        """Return one 5-byte frame when available, otherwise ``None``."""


def acquire(detector: FrameReader) -> Iterator[Tuple[float, float]]:
    """Continuously acquire decoded measurements from a detector.

    Parameters
    ----------
    detector:
        Object that provides a ``read_frame()`` method returning ``bytes`` or ``None``.

    Yields
    ------
    tuple
        ``(timestamp, signal_value)`` where ``timestamp`` is elapsed seconds
        since acquisition start and ``signal_value`` is the decoded value.
    """
    start_time = time.time()

    while True:
        frame = detector.read_frame()
        if frame is None:
            time.sleep(0.001)
            continue

        signal_value, _start_flag, error_flag = decode_measurement(frame)
        if error_flag:
            continue

        timestamp = time.time() - start_time
        yield timestamp, signal_value

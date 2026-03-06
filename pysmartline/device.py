"""Serial device interface for the Knauer Smartline detector."""

from typing import Optional

try:
    import serial
except ModuleNotFoundError:  # pragma: no cover - depends on runtime environment
    serial = None


class SmartlineDetector:
    """Manage a Smartline detector serial connection.

    Parameters
    ----------
    port:
        Serial port identifier (for example ``"COM7"`` or ``"/dev/tty.usbserial"``).
    timeout:
        Read timeout in seconds.
    """

    def __init__(self, port: str, timeout: float = 1.0) -> None:
        if serial is None:
            raise ModuleNotFoundError(
                "pyserial is required to use SmartlineDetector. Install with 'pip install pyserial'."
            )

        self._serial = serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            timeout=timeout,
        )

    def read_frame(self) -> Optional[bytes]:
        """Read one 5-byte frame from the detector.

        Returns
        -------
        bytes or None
            A 5-byte frame when available, otherwise ``None``.
        """
        if not self._serial.is_open:
            return None

        if self._serial.in_waiting < 5:
            return None

        frame = self._serial.read(5)
        if len(frame) != 5:
            return None
        return frame

    def close(self) -> None:
        """Close the serial connection."""
        if self._serial.is_open:
            self._serial.close()

    def __enter__(self) -> "SmartlineDetector":
        """Return detector instance for context-manager use."""
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Close detector on context-manager exit."""
        self.close()

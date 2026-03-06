"""Live Smartline acquisition example with optional logging."""

import argparse
from typing import Optional, TextIO

import matplotlib.pyplot as plt

from pysmartline import SmartlineDetector, acquire
from pysmartline.plotting import create_realtime_plot, update_realtime_plot


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the live plotting example."""
    parser = argparse.ArgumentParser(description="Live acquisition from a Smartline detector")
    parser.add_argument("--port", required=True, help="Serial port (e.g., /dev/tty.usbserial or COM7)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Serial read timeout in seconds")
    parser.add_argument("--log-file", default=None, help="Optional CSV file path for logging")
    parser.add_argument("--title", default="Smartline Live Signal", help="Plot title")
    return parser.parse_args()


def main() -> None:
    """Run live acquisition, optional logging, and real-time plotting."""
    args = parse_args()

    times = []
    values = []
    log_handle: Optional[TextIO] = None

    plt.ion()
    fig, ax, line = create_realtime_plot(title=args.title)
    plt.show(block=False)

    detector = SmartlineDetector(port=args.port, timeout=args.timeout)

    try:
        if args.log_file:
            log_handle = open(args.log_file, "w", encoding="utf-8")
            log_handle.write("time_s,signal\n")

        for timestamp, signal_value in acquire(detector):
            times.append(timestamp)
            values.append(signal_value)

            update_realtime_plot(line, ax, times, values)
            plt.pause(0.001)

            if log_handle is not None:
                log_handle.write(f"{timestamp:.7f},{signal_value:.7f}\n")

    except KeyboardInterrupt:
        pass
    finally:
        if log_handle is not None:
            log_handle.close()
        detector.close()
        plt.ioff()
        plt.close(fig)


if __name__ == "__main__":
    main()

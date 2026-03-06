%matplotlib qt

import serial
import time
import math
from typing import Sequence, Tuple
import matplotlib.pyplot as plt


# serial connection configuration
ser = serial.Serial(
    port='COM7',  
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    timeout=1
)


def bytes_to_binary_string(b):
    return ''.join(format(byte, '08b') for byte in b)


def get_fi_pho_value(p_buffer: Sequence[int]) -> Tuple[float, bool, bool]:
    """
    Args:
        p_buffer: A bytes-like or sequence of integers (each 0..255) with at least 5 elements.

    Returns:
        A tuple (value, b_start, b_error):
          - value: float (0.0 if error flag set, otherwise computed value)
          - b_start: bool (True if FL_PHIPHO_START bit set in p_buffer[0])
          - b_error: bool (True if FL_PHIPHO_ERROR bit set in p_buffer[0])

    Notes:
        - Mantissa is assembled from bytes 0..3 (24-bit signed with sign extension)
        - Exponent is taken from low 8 bits of (p_buffer[4] | (p_buffer[3] << 7)) interpreted as signed char
        - Result is 1000 * mantissa * 2^(exp - 23)
    """
    if not isinstance(p_buffer, (bytes, bytearray, list, tuple, memoryview)):
        raise TypeError("p_buffer must be a bytes-like or sequence of integers")

    if len(p_buffer) < 5:
        raise ValueError("p_buffer must contain at least 5 bytes")
    
    FL_PHIPHO_START = 0x20
    FL_PHIPHO_ERROR = 0x10

    # Access as integers 0..255
    b_start = bool(p_buffer[0] & FL_PHIPHO_START)
    b_error = bool(p_buffer[0] & FL_PHIPHO_ERROR)

    # Build mantissa (24-bit field assembled from multiple bytes)
    l_mantiss = (p_buffer[3] >> 1)
    l_mantiss |= (p_buffer[2] << 6)
    l_mantiss |= (p_buffer[1] << 13)
    l_mantiss |= ((p_buffer[0] & 0x0F) << 20)

    # Sign-extend 24-bit signed mantissa to Python int
    if l_mantiss & 0x00800000:
        l_mantiss -= (1 << 24)

    # iExp is the signed char of (pBuffer[4] | (pBuffer[3] << 7))
    raw_exp = (p_buffer[4] | (p_buffer[3] << 7)) & 0xFF  # low 8 bits
    i_exp = raw_exp - 256 if raw_exp >= 0x80 else raw_exp

    if b_error:
        return 0.0, b_start, b_error

    result = 1000.0 * math.ldexp(l_mantiss, i_exp - 23)
    return float(result), b_start, b_error



resin_name = input('resin name:  ')
sugar = input('sugar name:  ')
date = input('date:  ')

timelist, signallist = [], []

# { setup matplotlib w/ blitting }
fig, ax = plt.subplots(figsize=(10,6), dpi=300)
ax.set(xlabel='Time (s)', ylabel='Refractive Index (mRIU)', xlim=(0,30*60), ylim=(-0.3,0.05), title=f'{resin_name} {sugar}, {date}')
fig.canvas.draw()
line, = ax.plot([],[],  marker='o', ls='', markersize=1,  color='purple')
text = ax.text(10,-0.1, "this is text")
axbackground = fig.canvas.copy_from_bbox(ax.bbox)
plt.show(block=False)
#

try:
    with open(f"{resin_name}-{sugar}-{date}.txt", "w") as log_file:
        log_file.write('time (sec),signal\n')
        starttime = time.time()

        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if len(data) == 5:
                    measurement, startcode, errorbool = get_fi_pho_value(data)

                    if not errorbool:
                        currenttime = time.time() - starttime
                        log_file.write(f"{currenttime:.7f},{measurement:.7f}\n")  
                        ser.flush()

                        timelist.append(currenttime)
                        signallist.append(measurement)

                        # { plot, with blitting }
                        line.set_data(timelist, signallist)
                        fig.canvas.restore_region(axbackground)
                        ax.draw_artist(line)
                        fig.canvas.blit(ax.bbox)
                        fig.canvas.flush_events()
                        #   


except KeyboardInterrupt:
    print("Interrupted by user; closing...")
finally:
    ser.close()

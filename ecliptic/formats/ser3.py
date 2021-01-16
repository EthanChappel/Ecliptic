from datetime import datetime
from datetime import timezone as tz
import time

MONO = 0
BAYER_RGGB = 8
BAYER_GRBG = 9
BAYER_GBRG = 10
BAYER_BGGR = 11
BAYER_CYYM = 16
BAYER_YCMY = 17
BAYER_YMCY = 18
BAYER_MYYC = 19

class Ser3Writer:
    def __init__(self, name, color_id, little_endian, width, height, bit_depth, observer, instrument, telescope):
        self.timestamps = []
        self.epoch = int((datetime.fromtimestamp(time.mktime(time.gmtime(0))) - datetime(1, 1, 1, 0, 0, 0)).total_seconds()) * (10 ** 7)
        self.frame_count = 0
        self.fp = open(name, 'wb')
        self.fp.write(b'LUCAM-RECORDER')  # FileID
        self.fp.write((0).to_bytes(4, 'little'))  # LuID
        self.fp.write((color_id).to_bytes(4, 'little'))  # ColorID
        self.fp.write(int(little_endian).to_bytes(4, 'little'))  # LittleEndian
        self.fp.write((width).to_bytes(4, 'little'))  # ImageWidth
        self.fp.write((height).to_bytes(4, 'little'))  # ImageHeight
        self.fp.write((bit_depth).to_bytes(4, 'little'))  # PixelDepthPerPlane
        self.frame_count_position = self.fp.tell()
        self.fp.write((0).to_bytes(4, 'little'))  # FrameCount placeholder
        self.fp.write(bytearray(observer, 'ascii') + b'\0' * (40 - len(observer)))  # Observer
        self.fp.write(bytearray(instrument, 'ascii') + b'\0' * (40 - len(instrument)))  # Instrument
        self.fp.write(bytearray(telescope, 'ascii') + b'\0' * (40 - len(telescope)))  # Telescope
        local_time = self.epoch + int((time.time() + time.timezone) * (10 ** 7))
        self.fp.write((local_time).to_bytes(8, 'little'))  # DateTime
        utc_time = self.epoch + int(time.time() * (10 ** 7))
        self.fp.write((utc_time).to_bytes(8, 'little'))  # DateTime_UTC

    def add_frame(self, frame):
        self.timestamps.append(self.epoch + int(time.time() * (10 ** 7)))
        self.fp.write(frame)
        self.frame_count += 1

    def close(self):
        for t in self.timestamps:
            self.fp.write((t).to_bytes(8, 'little'))
        self.fp.seek(self.frame_count_position)
        self.fp.write((self.frame_count).to_bytes(4, 'little'))
        self.fp.close()
    
    def __del__(self):
        self.close()
        
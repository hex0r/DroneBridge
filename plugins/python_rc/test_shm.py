#
#   This file is part of DroneBridge: https://github.com/seeul8er/DroneBridge
# *
# *   Copyright 2018 Wolfgang Christl
# *
# *   Licensed under the Apache License, Version 2.0 (the "License");
# *   you may not use this file except in compliance with the License.
# *   You may obtain a copy of the License at
# *
# *   http://www.apache.org/licenses/LICENSE-2.0
# *
# *   Unless required by applicable law or agreed to in writing, software
# *   distributed under the License is distributed on an "AS IS" BASIS,
# *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# *   See the License for the specific language governing permissions and
# *   limitations under the License.
# *
# */


import mmap
from posix_ipc import SharedMemory
from ctypes import sizeof
import ctypes
import time
import sys


rc_region = SharedMemory("db_rc_values_t")

#typedef struct {
#    uint16_t ch[NUM_CHANNELS];
#    uint16_t rssi;
#    struct timeval last_update;
#} __attribute__((packed)) db_rc_values_t;

class timeval(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long)]


class stru(ctypes.Structure):
    _fields_ = [
    ("ch1", ctypes.c_uint16),
    ("ch2", ctypes.c_uint16),
    ("ch3", ctypes.c_uint16),
    ("ch4", ctypes.c_uint16),
    ("ch5", ctypes.c_uint16),
    ("ch6", ctypes.c_uint16),
    ("ch7", ctypes.c_uint16),
    ("ch8", ctypes.c_uint16),
    ("ch9", ctypes.c_uint16),
    ("ch10",ctypes.c_uint16),
    ("ch11",ctypes.c_uint16),
    ("ch12",ctypes.c_uint16),
    ("ch13",ctypes.c_uint16),
    ("ch14",ctypes.c_uint16),
    ("rssi",ctypes.c_int8),
    ("packsec", ctypes.c_uint16),
    ("last_update", timeval)
    ]


librt = ctypes.CDLL('librt.so.1', use_errno=True)
clock_gettime = librt.clock_gettime
clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timeval)]


def timedifference_msec( t0, t1):
    return (t1.tv_sec - t0.tv_sec) * 1000.0 + (t1.tv_usec- t0.tv_usec) / 1000.0


def monotonic_time():
    t = timeval()
    if clock_gettime(0 , ctypes.pointer(t)) != 0:
        errno_ = ctypes.get_errno()
        raise OSError(errno_, os.strerror(errno_))
    t.tv_usec = int(t.tv_usec / 1000) # to ms
    return t


while True:
    now= monotonic_time()
    shm_buf =mmap.mmap(rc_region.fd, sizeof(stru))
    data = stru.from_buffer(shm_buf)
    diff= timedifference_msec(data.last_update,now)

    if(diff < 100): # lost connection last frame older than 100ms
        print("CH1 ",data.ch1,"CH2 ",data.ch2,"CH3 ",data.ch3,"CH4 ",data.ch4,"RSSI ",data.rssi )
    else:
        print("lost conection")
    time.sleep(0.1)

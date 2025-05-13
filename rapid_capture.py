# -----------------------------------------------------------------------------
# Copyright (c) 2024, Lucid Vision Labs, Inc.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------


import time, os
from PIL import Image as PIL_Image  # pip install Pillow
import numpy as np
from pathlib import Path

from arena_api.system import system
from arena_api.buffer import *

from utils import *
from configuration import *

import ctypes

def capture_image():
    """
    demonstrates live stream
    (1) Start device
    (2) Streaming setup and set configuration
    (2) Get a buffer and create a copy
    (3) Requeue the buffer
    (4) Calculate bytes per pixel for reshaping
    (5) Create array from buffer cpointer data
    (6) Create a NumPy array with the image shape
    (7) Display the NumPy array using OpenCV
    (8) When Esc is pressed, stop stream and destroy OpenCV windows
    """
    
    # (1) Start device
    devices = create_devices_with_tries()
    device = system.select_device(devices)
    nodemap = device.nodemap
    tl_stream_nodemap = device.tl_stream_nodemap
    print(f'Device used in the example:\n\t{device}')
    
    # (2) Streaming setup & set configuration
    check_initial_values(nodemap)
    streaming_setup(tl_stream_nodemap)
    set_configuration(nodemap) # exposure time, binning, gain, pixel format, height/width, gamma
    
    # (3)    
    img_cnt = 0
    png_path = constants.PNG_PATH
    
    with device.start_stream(constants.NUM_BUFFERS):
        print(f'Stream started with {constants.NUM_BUFFERS} buffers')

        print(f'Grabbing an image buffer')
        buffers = device.get_buffer(constants.NUM_BUFFERS)
        
        # Print image buffer info
        for count, buffer in enumerate(buffers):
            save_image_mono8_to_png_with_PIL(buffer, png_path, count)
            
        device.requeue_buffer(buffers)

    # (4) Clean up
    device.stop_stream()
        
    system.destroy_device()
    print(f'Destroyed all created devices')
        
if __name__ == "__main__":
    
    capture_image()    
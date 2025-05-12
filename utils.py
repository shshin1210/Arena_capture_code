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


from arena_api.system import system
import os, datetime
from PIL import Image as PIL_Image  # pip install Pillow
import numpy as np
from pathlib import Path
import constants
import cv2, time

def create_devices_with_tries():
    '''
    Waits for the user to connect a device before raising an exception if it fails
    '''
    
    tries = 0
    tries_max = 6
    sleep_time_secs = 10
    devices = None
    while tries < tries_max:
        devices = system.create_device()
        if not devices:
            print(
                f'Try {tries+1} of {tries_max}: waiting for {sleep_time_secs} '
                f'secs for a device to be connected!')
            for sec_count in range(sleep_time_secs):
                time.sleep(1)
                print(f'{sec_count + 1 } seconds passed ',
                    '.' * sec_count, end='\r')
            tries += 1
        else:
            return devices
    else:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the example again.')
        
def check_initial_values(nodemap):
    print(f"Store initial values")
    initial_acquisition_mode = nodemap.get_node("AcquisitionMode").value
    width_initial = nodemap.get_node("Width").value
    height_initial = nodemap.get_node("Height").value
    
    print('initial acquisition mode : %s \n'%(initial_acquisition_mode))
    print('initial width : %s \n'%(width_initial))
    print('initial height : %s'%(height_initial))

def streaming_setup(tl_stream_nodemap):
    """
    ##### Set buffer handling mode
    Set buffer handling mode before starting the stream. Starting the
    stream requires the buffer handling mode to be set beforehand. The
    buffer handling mode determines the order and behavior of buffers in
    the underlying stream engine. Setting the buffer handling mode to
    'NewestOnly' ensures the most recent image is delivered, even if it
    means skipping frames.
    
    ##### Enable stream auto negotiate packet size
    Setting the stream packet size is done before starting the stream.
    Setting the stream to automatically negotiate packet size instructs the
    camera to receive the largest packet size that the system will allow.
    This generally increases frame rate and results in fewer interrupts per
    image, thereby reducing CPU load on the host system. Ethernet settings
    may also be manually changed to allow for a larger packet size.
    
    ##### Enable stream packet resend
    Enable stream packet resend before starting the stream. Images are sent
    from the camera to the host in packets using UDP protocol, which
    includes a header image number, packet number, and timestamp
    information. If a packet is missed while receiving an image, a packet
    resend is requested and this information is used to retrieve and
    redeliver the missing packet in the correct order.

    """
    # Stream nodemap
    tl_stream_nodemap["StreamBufferHandlingMode"].value = "NewestOnly"
    tl_stream_nodemap['StreamAutoNegotiatePacketSize'].value = True
    tl_stream_nodemap['StreamPacketResendEnable'].value = True

def save_image_mono8_to_png_with_PIL(image_buffer, idx):
    """
    To save an image Pillow needs an array that is shaped to
    (height, width). In order to obtain such an array we use numpy
    library
    """
    print(f'Converting image buffer to a numpy array')

    """		
    Buffer.pdata is a (uint8, ctypes.c_ubyte)
    Buffer.data is a list of elements each represents one byte. Therefore
    for Mono8 each element represents a pixel.
    """

    """
    Method 1 (from Buffer.data)

    dtype is uint8 because Buffer.data returns a list or bytes and pixel
    format is also Mono8.
    NOTE:
    if 'ChunkModeActive' node value is True then the Buffer.data is
    a list of (image data + the chunkdata) so data list needs to be
    truncated to have image data only.
    can use either :
        - device.nodemap['ChunkModeActive'].value   (expensive)
        - buffer.has_chunkdata                 (less expensive)
    """
    image_only_data = None
    if image_buffer.has_chunkdata:
        # 8 is the number of bits in a byte
        bytes_pre_pixel = int(image_buffer.bits_per_pixel / 8)

        image_size_in_bytes = image_buffer.height * \
            image_buffer.width * bytes_pre_pixel

        image_only_data = image_buffer.data[:image_size_in_bytes]
    else:
        image_only_data = image_buffer.data

    nparray = np.asarray(image_only_data, dtype=np.uint8)
    # Reshape array for pillow
    nparray_reshaped = nparray.reshape((
        image_buffer.height,
        image_buffer.width
    ))

    """
    Method 2 (from Buffer.pdata)

    A more general way (not used in this simple example)

    Creates an already reshaped array to use directly with
    pillow.
    np.ctypeslib.as_array() detects that Buffer.pdata is (uint8, c_ubyte)
    type so it interprets each byte as an element.
    For 16Bit images Buffer.pdata must be cast to (uint16, c_ushort)
    using ctypes.cast(). After casting, np.ctypeslib.as_array() can
    interpret every two bytes as one array element (a pixel).

    Code:
    nparray_reshaped = np.ctypeslib.as_array( image_buffer.pdata,
    (image_buffer.height, image_buffer.width))
    """

    # Save image
    print(f'Saving image')
    png_path = constants.PNG_PATH + '/' + datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M')
    
    if not os.path.isdir(png_path):
        os.makedirs(png_path)
        
    png_name = "%s_%04d.png"%(constants.PNG_NAME, idx)
    png_array = PIL_Image.fromarray(nparray_reshaped)
    png_array.save(os.path.join(png_path, png_name))
    print(f'Saved image path is: {Path(png_path) / png_name}')
    
def save_image_opencv(npndarray, png_path, idx):
    
    
    if not os.path.isdir(png_path):
        os.makedirs(png_path)
        
    png_name = "%s_%04d.png"%(constants.PNG_NAME, idx)
    
    cv2.imwrite(os.path.join(png_path, png_name), npndarray)

    print(f'Saved image path is: {Path(png_path) / png_name}')

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


import time
from arena_api.system import system
import constants

def set_exposure(nodemap, long=False):
    
    nodes = nodemap.get_node(['ExposureAuto', 'ExposureTime', 'AcquisitionFrameRateEnable', 'AcquisitionFrameRate'])

    if long == False:
        if constants.EXPOSURE_TIME > nodes['ExposureTime'].max:
            nodes['ExposureTime'].value = nodes['ExposureTime'].max
            print(f'The value of exposure time is over maximum. Try "long = True"')
        elif constants.EXPOSURE_TIME < nodes['ExposureTime'].min:
            nodes['ExposureTime'].value = nodes['ExposureTime'].min
            print(f'The value of exposure time is less than minimum.')
        else:
            nodes['ExposureTime'].value = constants.EXPOSURE_TIME
    
    else:
        """
            Code to increase the maximum exposure time. By default,
            Lucid cameras are prioritized to achieve maximum frame rate. However, due to the
            high frame rate configuration, the exposure time will be limited as it is a dependant value. <br>
            If the frame rate is 30 FPS, the maximum allowable exposure would be 1/30 = 0.0333 seconds = 33.3 milliseconds. <br>
            So, a decrease in the frame rate is necessary for increasing the exposure time.
        """
    
        exposure_auto_initial = nodes['ExposureAuto'].value
        exposure_time_initial = nodes['ExposureTime'].value
        acquisition_fr_enable_initial = nodes['AcquisitionFrameRateEnable'].value
        acquisition_fr_initial = nodes['AcquisitionFrameRate'].value
        
        """
        ##### Demonstrates exposure: long
        1. Set Acquisition Frame Rate Enable to true
        2. Decrease Acquisition Frame Rate
        3. Set Exposure Auto to OFF
        4. Increase Exposure Time       
        """
        nodes['AcquisitionFrameRateEnable'].value = True
        nodes['AcquisitionFrameRate'].value = constants.FRAME_RATE
        
        # Disable automatic exposure before setting an exposure time. Automatic exposure controls whether the exposure time is set manually or
        # automatically by the device. Setting automatic exposure to 'Off' stops the device from automatically updating the exposure time.
        nodes['ExposureAuto'].value = 'Off'
        print(f'Disable Auto Exposure')

        # In order to get the exposure time maximum and minimum values, get the exposure time node. Failed attempts to get a node return null, so check
        # that the node exists. And because we expect to set its value, check that the exposure time node is writable.
        if nodes['ExposureTime'] is None:
            raise Exception("ExposureTime node not found")
        if not nodes['ExposureTime'].is_writable:
            raise Exception("ExposureTime node is not writable")
        
        if 1/constants.FRAME_RATE < constants.EXPOSURE_TIME*1e-6:
            print('Allowable exposure time : %6f [sec]'%(1/constants.FRAME_RATE))
            print('[WARNING] Lower the exposure time!!!!')
        assert 1/constants.FRAME_RATE > constants.EXPOSURE_TIME*1e-6 # unit to seconds (30 Hz frame rate -> max 1/30 sec exposure)
            
        # Set exposure time to defined constant value
        nodes['ExposureTime'].value = constants.EXPOSURE_TIME
        
        print(f'Acquisition FrameRate to %d HZ and Exposrue %d'%(constants.FRAME_RATE, constants.EXPOSURE_TIME))
        
def set_binning(nodemap):
    """
        set binning value
    """
    nodes = nodemap.get_node(['BinningSelector', 'BinningVertical', 'BinningHorizontal', 'BinningVerticalMode', 'BinningHorizontalMode'])

    binning_selector = nodemap["BinningSelector"]
    print("Checking if sensor binning is supported")
    if("Digital" not in binning_selector.enumentry_names or
            not binning_selector.enumentry_nodes.get("Digital").is_readable):
        print("Digital binning not supported by device: not available from BinningSelector")
        quit()

    # Entry we will use for BinningVerticalMode and BinningHorizontal Mode
    BINTYPE = "Sum"
    binning_selector.value = "Digital" # Digital or Sensor
    
    # Check writable BinningHorizontal / Vertical to their 
    if (not nodes["BinningVertical"].is_writable or
            not nodes["BinningVertical"].is_writable):
        print("Sensor binning is not supported: "
            "BinningVertical or BinningHorizontal not available")
        quit()
        
    print(f"Set binning mode to {BINTYPE}")
    nodes["BinningVerticalMode"].value = BINTYPE
    nodes["BinningHorizontalMode"].value = BINTYPE
    
    print(f"Set horizontal and vertical binning value %d"%(constants.BINNING))
    nodes['BinningHorizontal'].value = constants.BINNING
    nodes['BinningVertical'].value = constants.BINNING

def set_gain(nodemap):
    """
        set gain value
    """
    nodes = nodemap.get_node(['GainAuto', 'Gain'])

    # Set Gain auto to be off
    nodes['GainAuto'].value = 'Off'
    
    # Check if node gain is writable 
    if (not nodes["Gain"].is_writable or
            not nodes["Gain"].is_writable):
        print("Gain is not available")
        quit()
        
    print("Set gain to value : %d"%(constants.GAIN))
    nodes['Gain'].value = constants.GAIN
    
def set_pixel_format(nodemap):
    """
        set pixel format
    """
    nodes = nodemap.get_node(['PixelFormat'])
    
    # Check if node pixel format is writable 
    if (not nodes["PixelFormat"].is_writable or
            not nodes["PixelFormat"].is_writable):
        print("PixelFormat is not available")
        quit()
        
    print(f'Setting Pixel Format to {constants.PIXEL_FORMAT}')
    nodes['PixelFormat'].value = constants.PIXEL_FORMAT
    
def set_width_height(nodemap):
    """
        set width and height
    """
    nodes = nodemap.get_node(['Width', 'Height'])
    
    # Check if width is writable 
    if (not nodes["Width"].is_writable or
            not nodes["Width"].is_writable):
        print("Width is not available")
        quit()    
        
    print('Setting Width to its maximum value')
    nodes['Width'].value = nodes['Width'].max

    print('Setting Height to its maximum value')
    height = nodes['Height']
    height.value = height.max

def set_gamma(nodemap):
    """
        Set gamma value
    """
    nodes = nodemap.get_node(['Gamma'])

    # Check if Gamma is writable 
    if (not nodes["Gamma"].is_writable or
            not nodes["Gamma"].is_writable):
        print("Gamma is not available")
        quit()   
        
    print('Setting Gamma to %d'%(constants.GAMMA))
    nodes["Gamma"].value = constants.GAMMA

def set_configuration(nodemap):
    print('Start Setting =================')
    
    set_exposure(nodemap=nodemap, long=constants.EXPOSURE_LONG)
    set_binning(nodemap)
    set_gain(nodemap)
    set_pixel_format(nodemap)
    set_width_height(nodemap)
    set_gamma(nodemap)
    
    print('End Setting ===================')
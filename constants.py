import datetime

# Save
PNG_PATH = './captured_images' + '/' + datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M')
PNG_NAME = 'capture'

# streaming configuration
NUM_IMAGES = 10
TIMEOUT = 2000 # ms
NUM_BUFFERS = 1

# camera configuration
EXPOSURE_LONG = True
EXPOSURE_TIME = 10000.0 # us (float)
PIXEL_FORMAT = "Mono8"
WHITE_BALANCING = False # False = white balancing off
GAIN = 0.0
GAMMA = 1.0
BINNING = 1
TRIGGER_MODE = True # True = trigger mode ON


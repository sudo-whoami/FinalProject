import numpy as np
from scipy.io.wavfile import write
from PIL import Image
import sys

from rgb_tone import *

if len(sys.argv) != 2:
    print('Incorrect arguments!\nUsage: ./main.py <image>')
    sys.exit()

# Open the image jpg file
image = Image.open("images/" + sys.argv[1])
image.show()

# Convert the image to grayscale and get the pixel values
pixels = np.asarray(image)

# Normalize the pixel values between -1 and 1
pixels_resized = np.array(image.resize((128, 128)))
image_resized = Image.fromarray(pixels_resized)
image_resized.show()

# Save the pixel values as a WAV file, name will be input file name
write("sounds/" + sys.argv[1] + ".wav", 44100, pixels)
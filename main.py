import numpy as np
from scipy.io.wavfile import write
from PIL import Image
import sys

from rgb_tone import *

if len(sys.argv) != 3:
    print('Incorrect arguments!\nUsage: ./main.py <image> <sound>')
    sys.exit()

# Open the image file
image = Image.open(sys.argv[1])
image.show()

# Convert the image to grayscale and get the pixel values
image = image.convert('L')
image.show()

pixels = np.array(image)

# Normalize the pixel values between -1 and 1
pixels = pixels / 255.0
pixels = pixels * 2.0 - 1.0

""""
for x in range(pixels.shape[0]):
    for y in range(pixels.shape[1]):
        print(pixels[x][y])
"""

# Save the pixel values as a WAV file
write(sys.argv[2], 44100, pixels)
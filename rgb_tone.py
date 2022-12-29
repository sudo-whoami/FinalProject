import numpy as np

frequencies = np.array([4186.01, 3951.07, 3729.31, 3520, 3322.44, 3135.96, 2959.96, 2793.83, 2637.02, 
                        2489.02, 2349.32, 2217.46, 2093, 1975.53, 1864.66, 1760, 1661.22, 1567.98,
                        1479.98, 1396.91, 1318.51, 1244.51, 1174.66, 1108.73, 1046.5, 987.767, 932.328,
                            880, 830.609, 783.991, 739.989, 698.456, 659.255, 622.254, 587.33, 554.365,
                        523.251, 493.883, 466.164, 440, 415.305, 391.995, 369.994, 349.228, 329.628,
                        311.127, 293.665, 277.183, 261.626, 246.942, 233.082, 220, 207.652, 195.998,
                        184.997, 174.614, 164.814, 155.563, 146.832, 138.591, 130.813, 123.471, 116.541,
                            110, 103.826, 97.9989, 92.4986, 87.3071, 82.4069, 77.7817, 73.4162, 69.2957,
                        65.4064, 61.7354, 58.2705, 55, 51.9131, 48.9994, 46.2493, 43.6535, 41.2034, 38.8909,
                        36.7081, 34.6478, 32.7032, 30.8677, 29.1352, 27.5
                        ])
# create sinus waves with given freq, duration, samplerate
def to_sound(freq, duration, sp=44100):
    sine = np.sin(2*np.pi*np.arange(sp*duration)*freq/sp)
    return sine

def top_bottom(pixels, duration=10):
    mean_rows = np.mean(pixels, axis=1)  
    data = [] 
    for row in mean_rows:
        data.append(to_sound(frequencies[row], duration//pixels.shape[0]))
    return 

def left_right(pixels, duration=10):
    mean_columns = np.mean(pixels, axis=0)
    return

def in_out(pixels, duration=10):

    return

def topleft_bottomright(pixels, duration=10):

    return
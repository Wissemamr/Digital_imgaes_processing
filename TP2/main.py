from my_functions_tp02 import *

import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("figs\\flower.png", cv2.IMREAD_GRAYSCALE)

plt.imshow(image)

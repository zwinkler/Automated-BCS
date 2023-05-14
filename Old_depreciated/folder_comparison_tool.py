import pyrealsense2 as rs
import matplotlib.pyplot as plt
import numpy as np
import imageio
import time
import cv2
import glob
import os
import multiprocessing as mp
from itertools import repeat


filepath1 = glob.glob('From_pi_tif/*')
filepath2 = glob.glob('From_pi_tif_multi/*')
diff = []

for i in range(0, len(filepath1)):
    base = os.path.basename(filepath1[i])[0:-4]
    base_multi = os.path.basename(filepath2[i])[0:-4]
    if base == base_multi:
        im = imageio.imread(filepath1[i])
        im_multi = imageio.imread(filepath2[i])
        diff.append(np.sum(im-im_multi))

print(diff)

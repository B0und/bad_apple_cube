
import glob
import os
from concurrent.futures import ThreadPoolExecutor
import cv2
import numpy as np
from numba import njit


@njit()
def get_flat_pos_array(img_arr):
    """Converts grayscale image numpy array into flat array
    with cube positions for blender.
    """
    WIDTH = 160
    HEIGHT = 120
    THRESH = 127

    res_arr = np.zeros(WIDTH*HEIGHT*3)
    white_indexes = np.argwhere(img_arr > THRESH)
    for row in white_indexes:
        y, x = row
        res_arr[3*(WIDTH*y+x)] = (2*WIDTH - 2*x)*(-1)
        res_arr[3*(WIDTH*y+x)+1] = 2*HEIGHT - 2*y

    return res_arr


def process_frame(frame_num):
    BLACK_AND_WHITE_MODE = 2
    # read image from disk
    img_arr = cv2.imread("frames/{}.jpg".format(frame_num),
                         BLACK_AND_WHITE_MODE)
    # get xyz blender positions array from image array
    res_arr = get_flat_pos_array(img_arr)
    # write numpy array to file
    with open("./locations/{}.npy".format(LOC_FOLDER, frame_num), 'wb') as f:
        np.save(f, np.array(res_arr))


def main():
    try:
        os.mkdir('locations')
    except FileExistsError:
        pass

    frame_count = len(glob.glob(f'./frames/*.jpg'))
    with ThreadPoolExecutor() as ex:
        ex.map(process_frame, np.arange(frame_count))


if __name__ == '__main__':
    main()

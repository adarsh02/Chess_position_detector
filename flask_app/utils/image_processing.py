
import cv2
import numpy as np
from skimage.util.shape import view_as_blocks

def process_image(img,down=320):
    square_size = down//8
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img=cv2.resize(gray_img,(down,down))
    min_val = np.min(gray_img)
    max_val = np.max(gray_img)
    normalized_img = (gray_img - min_val) / (max_val - min_val)
    tiles = view_as_blocks(normalized_img, block_shape=(square_size, square_size))
    tiles = tiles.reshape((64, square_size, square_size))
    return tiles





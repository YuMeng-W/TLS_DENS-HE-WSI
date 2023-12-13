import os
import cv2
import pdb
import glob
import numpy as np
from PIL import Image
from tqdm import tqdm
from skimage import morphology


SEG_PATH = ./Puzzle'
MASK_PATH = './Post_process/'

def run():
    seg_paths = glob.glob((os.path.join(SEG_PATH, '*_seg.png')))
    print(len(seg_paths))
    seg_paths.sort()
    pbar = tqdm(seg_paths)
    for seg_path in pbar:
        ID_name = seg_path.split('/')[-1]
        ID_name = ID_name.split('_')[0]
        print(ID_name)
        pbar.set_description("Processing %s" % ID_name)
        
        seg_img= cv2.imread(seg_path)
        gray_img = cv2.cvtColor(seg_img, cv2.COLOR_BGR2GRAY)
        ret1, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)
        dst = morphology.remove_small_objects(img == False, min_size = 10, connectivity = 1)
        bg_mask = np.zeros(seg_img.shape[:2])
        bg_mask[dst == False] = 255
        seg_mask = np.array(bg_mask, np.uint8)
        
        cv2.imwrite(MASK_PATH + ID_name + '_mask.png', seg_mask)
                

if __name__=="__main__":
    run()
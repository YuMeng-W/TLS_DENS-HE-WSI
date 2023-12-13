
import os
import cv2
import pdb
import glob
import openslide
import numpy as np
from tqdm import tqdm
from PIL import Image
from scipy.io import loadmat, savemat

WSI_PATH = './WSI/YNCH/wsi/0'
MAT_RES = './MAT/'
VISUAL_PATH = './visual/'
DEF_LEVEL = 2

def run():
    wsi_paths = glob.glob((os.path.join(WSI_PATH,'*.svs')))
    # wsi_paths = glob.glob((os.path.join(WSI_PATH,'*.ndpi')))
    print('********************')
    print(len(wsi_paths))
    print('********************')
    wsi_paths.sort()
    pbar1 = tqdm(wsi_paths)
    
    for wsi_path in pbar1:
        ID_name = wsi_path.split('/')[-1]

        # ID_name = ID_name.split('-01Z')[0]         #TCGA
        # ID_name = ID_name.split(' TP')[0]                #SXCH
        ID_name = ID_name.split('.svs')[0]                 #GDPH/YNCH
        
        # if os.path.exists(VISUAL_PATH + ID_name + '_seg_rgb.png'):
        if os.path.exists(VISUAL_PATH + ID_name + '_seg.png'):
            pass
        else:
            
            pbar1.set_description("Processing %s" % ID_name)       
            slide = openslide.OpenSlide(wsi_path)

            wsi = np.array(slide.read_region((0, 0), DEF_LEVEL,
                                                slide.level_dimensions[DEF_LEVEL]))
            wsi = Image.fromarray(wsi).convert('RGB')
            h1, w1 = slide.level_dimensions[DEF_LEVEL]
            temp = Image.fromarray(np.zeros((w1, h1), np.uint8) + 4)                   #创建画板

            # pdb.set_trace()
            MAT_PATH = MAT_RES + ID_name 
            mat_paths = glob.glob((os.path.join(MAT_PATH,'*.mat'))) 
            print(len(mat_paths))
            mat_paths.sort()
            pbar2 = tqdm(mat_paths)
            for mat_path in pbar2:
                Coord = mat_path.split('/')[-1]
                Coord = Coord.split('_40x')[0]
                # print(Coord)
                Coord_X = int(Coord.split('_')[1]) // 16
                Coord_Y = int(Coord.split('_')[-1]) // 16            
                # Coord_X = int(Coord.split('_')[1]) // 64
                # Coord_Y = int(Coord.split('_')[-1]) // 64

                mat_data = loadmat(mat_path)
                tissue_map = mat_data['tissue_map']
                patch_map = cv2.resize(tissue_map, (128, 128), interpolation=cv2.INTER_NEAREST)         #16/8
                # patch_map = cv2.resize(tissue_map, (32, 32), interpolation=cv2.INTER_NEAREST)             #64/32
                patch_map = Image.fromarray(patch_map)
                temp.paste(patch_map, (Coord_X, Coord_Y))
                lym_mask = temp

            lym_mask = lym_mask.convert('P')
            #tumor ---0   stroma---1   lym---2   ner-+back--4
            # lym_mask.putpalette([0, 0, 255, 255,0, 0, 0, 255, 0, 255, 255, 255,255,255,255])
            # lym_mask.putpalette([255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255,255,255,255])
            # lym_mask.putpalette([0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0])
            lym_mask.putpalette([ 51, 51,205,  0,  165, 255,  0,255, 0,  255, 255, 255,255,255,255])
            lym_mask = lym_mask.convert('RGB')
            overlay = Image.blend(wsi, lym_mask, 0.5)   
            lym_mask  = np.array(lym_mask , np.uint8)
            overlay = np.array(overlay, np.uint8)

            # cv2.imwrite(VISUAL_PATH + ID_name + '_seg.png', lym_mask)
            cv2.imwrite(VISUAL_PATH + ID_name + '_seg_rgb.png', lym_mask)
            cv2.imwrite(VISUAL_PATH + ID_name + '_onwsi.png', overlay)



if __name__=="__main__":
    run()


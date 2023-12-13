import os
import cv2
import csv
import glob
import pdb
import openslide
import numpy as np
from tqdm import tqdm
from scipy.io import loadmat, savemat
from skimage.measure import label,regionprops


WSI_PATH = './wsi'
MAT_RES = './MAT/'
MASK_PATH = '.Post_process/'
SAVE_PATH = './Post_process/'
RES_PATH = './tls_density.csv'

headers = ['ID_name',  'Area_Tumor_ALL', 'Area_Tumor_2', 'TLS_Num', 'TLS_density_1', 'TLS_density_2']

def run():
    wsi_paths = glob.glob((os.path.join(WSI_PATH, '*.svs')))
    # wsi_paths = glob.glob((os.path.join(WSI_PATH,'*.ndpi')))
    print(len(wsi_paths))
    wsi_paths.sort()
    pbar = tqdm(wsi_paths)

    with open(RES_PATH ,'w' ) as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)

            for wsi_path in pbar:
                ID_name = wsi_path.split('/')[-1]
                # ID_name = ID_name.split('-01Z')[0]         #TCGA
                # ID_name = ID_name.split(' TP')[0]                #SXCH
                ID_name = ID_name.split('.svs')[0]                 #GDPH/YNCH

                print(ID_name)
                pbar.set_description("Processing %s" % ID_name)
                slide = openslide.OpenSlide(wsi_path)
                
                ##GDPH/JMCH/YNCH/TCGA
                mpp_x = openslide.PROPERTY_NAME_MPP_X
                mpp_x = slide.properties[mpp_x]
                mpp = float(mpp_x)
                # pdb.set_trace()
                
                thr_pixels = (150 / mpp) / 64                                      

                mask_path = MASK_PATH + ID_name + '_mask.png'
                mask = cv2.imread(mask_path)
                gray_img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                ret1, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)      #OTSU
                label_img = label(img)
                region_props = regionprops(label_img)
                
                Num = len(region_props)       
                # print(Num)

                tls_num = 0
                for n in range(Num):                     
                    axis_len =  region_props[n].major_axis_length                    
                    if axis_len > thr_pixels:                                                                    
                        tls_num = tls_num + 1
                        tls_bbox = region_props[n].bbox
                        y0, x0, y1, x1 = tls_bbox 
                        cv2.rectangle(mask, (x0, y0), (x1, y1), (0, 0, 255), 1)
                print(tls_num)
                cv2.imwrite(SAVE_PATH + ID_name + '_tls.png', mask)
                
                pixels_lym = 0
                pixels_epi = 0
                pixels_str = 0
                Aera_tumor = 0

                MAT_PATH = MAT_RES + ID_name
                mat_paths = glob.glob((os.path.join(MAT_PATH,'*.mat')))     

                #AREA--ALL      
                patch_num = len(mat_paths)
                # print(len(mat_paths))
                patch_area = (2048*mpp)**2

                #AREA = EPI + STR +  LYM
                mat_paths.sort()
                pbar2 = tqdm(mat_paths)                           
                for mat_path in pbar2: 
                    mat_data = loadmat(mat_path)
                    tissue_map = mat_data['tissue_map']
                    epi_patch = np.sum((tissue_map == 0) * 1)                     
                    str_patch = np.sum((tissue_map == 1) * 1)                                  lym_patch = np.sum((tissue_map == 2) * 1)                   
                    pixels_lym = pixels_lym + lym_patch
                    pixels_epi = pixels_epi + epi_patch
                    pixels_str = pixels_str + str_patch
                Pixels_Tumor = pixels_lym + pixels_epi + pixels_str

                Aera_tumor_all =  patch_area * patch_num                   
                Aera_tumor = Pixels_Tumor * mpp * mpp
                tls_density_1 = tls_num / Aera_tumor_all                    
                tls_density_2 = tls_num / Aera_tumor

                result = [ID_name,  Aera_tumor_all, Aera_tumor, tls_num, tls_density_1, tls_density_2]
                f_csv.writerow(result)


if __name__=="__main__":
    run()
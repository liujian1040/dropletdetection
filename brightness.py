import cv2
import os
import numpy as np
from shutil import copy

def _brightness(image, min=0.5, max=1.0):
    '''
    Randomly change the brightness of the input image.
    Protected against overflow.
    '''
    hsv = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
 
    random_br = np.random.uniform(min,max)
    #random_br=1.9
    #To protect against overflow: Calculate a mask for all pixels
    #where adjustment of the brightness would exceed the maximum
    #brightness value and set the value to the maximum at those pixels.
    mask = hsv[:,:,2] * random_br > 255
    v_channel = np.where(mask, 255, hsv[:,:,2] * random_br)
    hsv[:,:,2] = v_channel
 
    return cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)
 
def random_bright(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    brightness = (0.5, 2, 0.5)
    img = _brightness(img, min=brightness[0], max=brightness[1])
    return img


# this function is for read image,the input is directory name
def read_directory(input_dir, output_dir , ext):
    for filename in os.listdir(input_dir):
        if filename.endswith(ext):
            img = cv2.imread(input_dir + "/" + filename)
            print(input_dir + "/" + filename)
            #print(img)
            img = random_bright(img)
            cv2.imwrite(output_dir + "/" + filename, img)
            
def copy_json_label(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('json'):
            origin_file_path = input_dir + "/" + filename
            target_file_path = output_dir + "/" + filename
            #cmd = 'copy '+origin_file_path+' '+target_file_path+' '+'/B'
            #print(cmd)
            
            copy(origin_file_path, target_file_path)
            #os.system('copy '+origin_file_path+' '+target_file_path)               

input_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/train'
output_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/5'
ext='.png'

copy_json_label(input_dir, output_dir)
read_directory(input_dir, output_dir, ext)

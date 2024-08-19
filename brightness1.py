import cv2
import os
import numpy as np
from shutil import copy
import json
from base64 import b64encode

def _brightness(image, min=0.5, max=0.6):
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
            
def naive_copy_json_label(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('json'):
            origin_file_path = input_dir + "/" + filename
            target_file_path = output_dir + "/" + filename
            #cmd = 'copy '+origin_file_path+' '+target_file_path+' '+'/B'
            #print(cmd)
            #new_dict = label_match_img(new_dict, img_path)
            copy(origin_file_path, target_file_path)
            #os.system('copy '+origin_file_path+' '+target_file_path) 

def label_match_img(label_dict, img_path):
    with open(img_path, 'rb') as f:
        #byte_content = f.read()
        # 把原始字节码编码成 base64 字节码
        #base64_bytes = b64encode(byte_content)
        qrcode = b64encode(f.read()).decode()
        label_dict['imageData'] = qrcode
        
    return label_dict

def copy_json_label(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('json'):
            origin_file_path = input_dir + "/" + filename
            target_file_path = output_dir + "/" + filename
            #cmd = 'copy '+origin_file_path+' '+target_file_path+' '+'/B'
            #print(cmd)
            with open(origin_file_path,'r') as load_f:
                load_dict = json.load(load_f)
            img_path = output_dir + "/" + filename[:-4]+'png'
            new_dict = label_match_img(load_dict, img_path)
            print(img_path)
            with open(target_file_path, 'w+') as f:
                json.dump(new_dict, f)
            #copy(origin_file_path, target_file_path)
            #os.system('copy '+origin_file_path+' '+target_file_path)            



input_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/train'
output_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/1'
ext='.png'

read_directory(input_dir, output_dir, ext)
copy_json_label(input_dir, output_dir)


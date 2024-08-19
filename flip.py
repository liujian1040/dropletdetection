import cv2
import os
import numpy as np
from shutil import copy
import json
from base64 import b64encode

def _brightness(image, min=0.5, max=2.0):
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
    
def flip_img(img):
    #水平翻转
    #return cv2.flip(img,1)
    #垂直翻转
    return cv2.flip(img,0)


# this function is for read image,the input is directory name
def read_directory(input_dir, output_dir , ext):
    for filename in os.listdir(input_dir):
        if filename.endswith(ext):
            img = cv2.imread(input_dir + "/" + filename)
            print(input_dir + "/" + filename)
            #print(img)
            #img = random_bright(img)
            img = flip_img(img)
            cv2.imwrite(output_dir + "/" + filename, img)

def label_flip(label_dict, flag):
    shapes = label_dict['shapes']
    for shape_index, shape in enumerate(shapes):
        points = shape['points']
        new_points = []
        for point_index, point in enumerate(points):
            #水平翻转
            #point[0] = 2200-point[0]
            #垂直翻转
            point[1] = 1700-point[1]
            new_points.append(point)
        shapes[shape_index]['points']=new_points
    label_dict['shapes']=shapes
    
    return label_dict
    
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
            new_dict = label_flip(load_dict, 1)
            img_path = output_dir + "/" + filename[:-4]+'png'
            new_dict = label_match_img(new_dict, img_path)
            print(img_path)
            with open(target_file_path, 'w+') as f:
                json.dump(new_dict, f, indent=2)
            #copy(origin_file_path, target_file_path)
            #os.system('copy '+origin_file_path+' '+target_file_path)               

input_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/2'
output_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/4'
ext='.png'

read_directory(input_dir, output_dir, ext)
copy_json_label(input_dir, output_dir)




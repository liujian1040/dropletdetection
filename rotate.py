import cv2
import os
import json
from PIL import Image
from base64 import b64encode


def rotate_img(img):
    # Rotate the image by 90 degrees clockwise
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return rotated_img


def flip_img(img):
    # 水平翻转
    return cv2.flip(img, 1)
    # 垂直翻转
    # return cv2.flip(img,0)


def label_match_img(label_dict, img_path):
    with open(img_path, 'rb') as f:
        # byte_content = f.read()
        # 把原始字节码编码成 base64 字节码
        # base64_bytes = b64encode(byte_content)
        qrcode = b64encode(f.read()).decode()
        label_dict['imageData'] = qrcode

    return label_dict


# this function is for read image,the input is directory name
def read_directory(input_dir, output_dir, ext):
    for filename in os.listdir(input_dir):
        if filename.endswith(ext):
            img = cv2.imread(input_dir + "/" + filename)
            print(input_dir + "/" + filename)
            # print(img)
            # img = random_bright(img)
            img = flip_img(img)
            cv2.imwrite(output_dir + "/" + filename, img)


def rotate_labels(label_dict):
    shapes = label_dict['shapes']
    for shape in shapes:
        points = shape['points']
        new_points = []
        for point in points:
            # Rotate the label coordinates by 90 degrees clockwise
            # new_point = [point[1], label_dict['imageHeight'] - point[0]]
            new_point = [point[1], point[0]]
            new_points.append(new_point)
        shape['points'] = new_points

    return label_dict


def rotate_images_and_labels(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.png'):
            img_filename = filename[:-4] + '.png'
            img_path = os.path.join(input_dir, filename)
            img = cv2.imread(img_path)
            rotated_img = rotate_img(img)
            #rotated_img = rotate_img(rotated_img)
            #rotated_img = rotate_img(rotated_img)  # 转三次
            rotated_img_filename = img_filename
            rotated_img_path = os.path.join(output_dir, rotated_img_filename)
            cv2.imwrite(rotated_img_path, rotated_img)

            label_filename = filename[:-4] + '.json'
            label_path = os.path.join(input_dir, label_filename)
            with open(label_path, 'r') as f:
                label_dict = json.load(f)

            rotated_label_dict = rotate_labels(label_dict)

            rotated_label_filename = label_filename

            rotated_label_path = os.path.join(output_dir, rotated_label_filename)

            with open(rotated_label_path, 'w') as f:
                json.dump(rotated_label_dict, f, indent=2)


input_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/train'
output_dir = r'C:/Users/Administrator/Desktop/CystalDetection-master/7'

rotate_images_and_labels(input_dir, output_dir)
print('done rotate90')


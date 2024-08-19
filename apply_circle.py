import os
import cv2
import numpy as np
import pandas as pd
import json

def extract_segment_points(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    segment_points = []
    segment_circles = []

    # Iterate over each shape in the JSON file
    for shape in data['shapes']:
        # Extract the segment points for each shape
        if shape['shape_type'] == 'circle':
            segment_circles.append(shape['points'])
            # segment_points.append(shape['label'])

    return segment_circles


def fit_circle(segment_cir):
    if len(segment_cir) != 2:
        return None  # 如果不是两个点，则返回None或抛出异常

    center = segment_cir[0]
    edge = segment_cir[1]
    SCALE = 1

    # 计算直径
    x1, y1 = center
    x2, y2 = edge
    radius = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#    cv2.circle(circle_img, center, radius, ELLIPSE_COLOR[label], 5)
    return radius * 2 * SCALE


def single_img_ana(img_file, json_file):
    # Read the image
    img = cv2.imread(img_file)

    # Extract segment points from the JSON file
    segment_circles = extract_segment_points(json_file)

    # Perform any other necessary analysis
    # ...

    # Create an empty black image
    image = np.zeros_like(img)
    image_with_points = image.copy()
    crystal_list = []

    # Iterate over each segment


    # Iterate over each segment

    for circle in segment_circles:
        radius = fit_circle(circle)
        print(radius)
        contour_area = 3.14 * (radius ** 2)
        crystal = {"file": img_file, "Contour Area": contour_area, "radius": radius}
        crystal_list.append(crystal)

    # Calculate the length of each mask
    #mask_lengths = [cv2.arcLength(segment, True) for segment in segment_points]

    return crystal_list


def batch_img_ana(origin_img_dir, json_dir, output_file):
    df = pd.DataFrame()

    # Iterate over each image file in the directory
    for filename in os.listdir(origin_img_dir):
        if filename.endswith('.png'):
            img_file = os.path.join(origin_img_dir, filename)
            json_file = os.path.join(json_dir, filename.replace('.png', '.json'))

            # Analyze the image and extract mask lengths
            crystal_info_list = single_img_ana(img_file, json_file)

            # Create a dictionary with the image file and corresponding mask lengths
            for crystal_info in crystal_info_list:
                temp = pd.DataFrame.from_dict(crystal_info, orient='index').T
                df = pd.concat([df, temp], ignore_index=True)
        df.to_excel(output_file, engine='xlsxwriter')
    print('Done')

# Specify the input directories and output file path
origin_img_dir = 'C:/Users/Administrator/Desktop/CystalDetection-master/val'
json_dir = 'C:/Users/Administrator/Desktop/CystalDetection-master/val'
output_file = 'C:/Users/Administrator/Desktop/CystalDetection-master/val/data_val.xls'

# Call the function to analyze the images and extract mask lengths
batch_img_ana(origin_img_dir, json_dir, output_file)

import os
import cv2
import pandas as pd
import numpy as np
import json

def extract_segment_points(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    segment_points = []
    segment_circles = []
    labels = []

    for shape in data['shapes']:
        if shape['shape_type'] == 'polygon':
            segment_points.append(shape['points'])
            labels.append(shape['label'])
        elif shape['shape_type'] == 'circle':
            segment_circles.append(shape['points'])
            labels.append(shape['label'])

    return segment_points, segment_circles, labels

def fit_circle(segment_cir):
    if len(segment_cir) != 2:
        return None

    center = segment_cir[0]
    edge = segment_cir[1]
    SCALE = 5 / 9

    x1, y1 = center
    x2, y2 = edge
    radius = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * SCALE
    return radius

def single_img_ana(img_file, json_file):
    img = cv2.imread(img_file)
    segment_points, segment_circles, labels = extract_segment_points(json_file)
    total_mask_area = 0
    img_height, img_width = 2200, 1700
    total_img_area = img_height * img_width

    for segment in segment_points:
        segment_array = np.array(segment, dtype=np.int32)
        segment_array = segment_array.reshape((-1, 1, 2))
        contour_area = cv2.contourArea(segment_array)
        total_mask_area += contour_area

    for circle in segment_circles:
        radius = fit_circle(circle)
        if radius is None:
            continue
        contour_area = 3.1416 * (radius ** 2)
        total_mask_area += contour_area

    pixel_ratio = total_mask_area / total_img_area
    return pixel_ratio

def batch_img_ana(origin_img_dir, json_dir, output_file):
    results = []

    for filename in os.listdir(origin_img_dir):
        if filename.endswith('.png'):
            img_file = os.path.join(origin_img_dir, filename)
            json_file = os.path.join(json_dir, filename.replace('.png', '.json'))

            pixel_ratio = single_img_ana(img_file, json_file)
            results.append({"file": filename, "pixel_ratio": pixel_ratio})

    df = pd.DataFrame(results)
    df.to_excel(output_file, engine='xlsxwriter')
    print('Done')

# Specify the input directories and output file path
origin_img_dir = 'C:/Users/Administrator/Desktop/CystalDetection-master/val'
json_dir = 'C:/Users/Administrator/Desktop/CystalDetection-master/val'
output_file = 'C:/Users/Administrator/Desktop/CystalDetection-master/val/data_val1_pixel_ratios.xls'

# Call the function to analyze the images and extract pixel ratios
batch_img_ana(origin_img_dir, json_dir, output_file)
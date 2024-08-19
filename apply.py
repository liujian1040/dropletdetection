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
    labels = []  # 添加：用于保存每个形状的标签

    # Iterate over each shape in the JSON file
    for shape in data['shapes']:
        # Extract the segment points for each shape
        if shape['shape_type'] == 'polygon':
            segment_points.append(shape['points'])
            labels.append(shape['label'])  # 添加：保存多边形的标签
        elif shape['shape_type'] == 'circle':
            segment_circles.append(shape['points'])
            labels.append(shape['label'])  # 添加：保存圆形的标签

    return segment_points, segment_circles, labels  # 修改：返回值中加入了labels

def fit_circle(segment_cir):
    # 原有的fit_circle函数代码保持不变
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
    segment_points, segment_circles, labels = extract_segment_points(json_file)  # 现在也接收标签列表
    image = np.zeros_like(img)
    image_with_points = image.copy()
    crystal_list = []
    label_idx = 0  # 用于跟踪当前处理的标签索引
    SCALE = 5 / 9  # 引入SCALE，与圆形处理保持一致

    for segment in segment_points:
        for point in segment:
            cv2.circle(image, (int(point[0]), int(point[1])), 1, (255), -1)

    contour_image = np.zeros_like(img)

    for segment in segment_points:
        try:
            segment_array = np.array(segment, dtype=np.int32)
            segment_array = segment_array.reshape((-1, 1, 2))
            cv2.drawContours(contour_image, [segment_array], 0, (255), thickness=1)
            contour_area = cv2.contourArea(segment_array)
            ellipse = cv2.fitEllipse(segment_array)
            major_axis = max(ellipse[1]) * SCALE  # 应用SCALE
            minor_axis = min(ellipse[1]) * SCALE  # 应用SCALE
            circ = cv2.arcLength(segment_array, True)
            aspect_Ratio = major_axis / minor_axis if minor_axis else 0
            radius = 0  # 圆形的特殊处理略去

            crystal = {"file": img_file, "Label": labels[label_idx], "Contour Area": contour_area, "minor_axis": minor_axis, "major_axis": major_axis,
                       "circumference": circ, "aspect_Ratio": aspect_Ratio, "radius": radius}
            crystal_list.append(crystal)
            label_idx += 1  # 更新标签索引
        except:
            print('Error processing polygon.')
            continue

    for circle in segment_circles:
        try:
            radius = fit_circle(circle)
            if radius is None:
                continue
            contour_area = 3.1416 * (radius ** 2)
            crystal = {"file": img_file, "Label": labels[label_idx], "Contour Area": contour_area, "minor_axis": 0, "major_axis": 0,
                       "circumference": 2 * 3.1416 * radius, "aspect_Ratio": 1, "radius": radius}
            crystal_list.append(crystal)
            label_idx += 1
        except:
            print('Error processing circle.')
            continue

    return crystal_list

def batch_img_ana(origin_img_dir, json_dir, output_file):
    df = pd.DataFrame()

    for filename in os.listdir(origin_img_dir):
        if filename.endswith('.png'):
            img_file = os.path.join(origin_img_dir, filename)
            json_file = os.path.join(json_dir, filename.replace('.png', '.json'))

            crystal_info_list = single_img_ana(img_file, json_file)

            for crystal_info in crystal_info_list:
                temp = pd.DataFrame.from_dict(crystal_info, orient='index').T
                df = pd.concat([df, temp], ignore_index=True)
    df.to_excel(output_file, engine='xlsxwriter')
    print('Done')

# Specify the input directories and output file path
origin_img_dir = 'C:/Users/Administrator/Desktop/CystalDetection-master/val'
json_dir = 'C:/Users/Administrator/Desktop/CystalDetection-master/val'
output_file = 'C:/Users/Administrator/Desktop/CystalDetection-master/val/data_val1.xls'

# Call the function to analyze the images and extract mask lengths
batch_img_ana(origin_img_dir, json_dir, output_file)
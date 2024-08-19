import json
import os
import math
from PIL import Image
import base64
from io import BytesIO

def split_image_and_annotations_batch(input_folder, annotations_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image and annotations
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)
            annotations_filename = os.path.splitext(filename)[0] + ".json"
            annotations_path = os.path.join(annotations_folder, annotations_filename)
            
            if os.path.isfile(annotations_path):
                split_image_and_annotations(image_path, annotations_path, output_folder)

def split_image_and_annotations(image_path, annotations_path, output_folder):
    # Load image
    image = Image.open(image_path)
    width, height = image.size
    split_width = width // 2
    split_height = height // 2

    # Split image
    image_parts = []
    for i in range(2):
        for j in range(2):
            left = j * split_width
            top = i * split_height
            right = left + split_width
            bottom = top + split_height
            image_part = image.crop((left, top, right, bottom))
            image_parts.append(image_part)

    # Load annotations
    with open(annotations_path, 'r') as f:
        annotations = json.load(f)

    # Split annotations
    annotations_parts = []
    for i in range(2):
        for j in range(2):
            annotations_part = []
            for shape in annotations['shapes']:
                shape_type = shape.get('shape_type')
                if shape_type == 'circle':
                    points = shape['points']
                    center_x, center_y = points[0]
                    edge_x, edge_y = points[1]
                    if j == 1:
                        center_x -= split_width
                        edge_x -= split_width
                    if i == 1:
                        center_y -= split_height
                        edge_y -= split_height
                    if 0 <= center_x <= split_width and 0 <= center_y <= split_height \
                            and 0 <= edge_x <= split_width and 0 <= edge_y <= split_height:
                        radius = math.sqrt((edge_x - center_x) ** 2 + (edge_y - center_y) ** 2)
                        annotations_part.append({'label': shape['label'], 'points': [(center_x, center_y), (edge_x, edge_y)], 'shape_type': shape_type})
                elif shape_type == 'polygon':
                    points = shape['points']
                    processed_points = []
                    for point in points:
                        x, y = point
                        if j == 1:
                            x -= split_width
                        if i == 1:
                            y -= split_height
                        if 0 <= x <= split_width and 0 <= y <= split_height:
                            processed_points.append((x, y))
                    if processed_points:
                        annotations_part.append({'label': shape['label'], 'points': processed_points, 'shape_type': shape_type})
            annotations_parts.append(annotations_part)

    # Save image parts and annotations parts
    for idx, (image_part, annotations_part) in enumerate(zip(image_parts, annotations_parts)):
        # Generate output filenames based on imagePath in annotations
        base_image_name = os.path.splitext(os.path.basename(annotations['imagePath']))[0]
        image_part_name = f"{base_image_name}_part{idx+1}.png"
        annotation_part_name = f"{base_image_name}_part{idx+1}.json"
        
        # Save image part
        image_part_path = os.path.join(output_folder, image_part_name)
        image_part.save(image_part_path)
        
        # Save image part as Base64 encoded string
        buffer = BytesIO()
        image_part.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        image_data_base64 = base64.b64encode(image_data).decode('utf-8')

        # Update annotations with imageData, imageHeight, and imageWidth
        annotations_part_data = {
            'version': annotations['version'],
            'flags': {}, 
            'shapes': annotations_part,
            'imagePath': image_part_name,
            'imageData': image_data_base64,  # Base64 encoded image data
            'imageHeight': image_part.height,
            'imageWidth': image_part.width
        }

        # Add flags and group_id to annotations_part_data
        annotations_part_data['flags'] = {}  # Add flags
        for shape_data in annotations_part_data['shapes']:
            shape_data['flags'] = {}  # Add flags for each shape
            shape_data['group_id'] = None  # Add group_id for each shape

        # Save annotations part
        annotation_part_path = os.path.join(output_folder, annotation_part_name)
        with open(annotation_part_path, 'w') as f:
            json.dump(annotations_part_data, f, indent=4)

# Input and output folder paths
input_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/val"
annotations_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/val"
output_folder =  "C:/Users/Administrator/Desktop/CystalDetection-master/val111"

# Process images and annotations
split_image_and_annotations_batch(input_folder, annotations_folder, output_folder)
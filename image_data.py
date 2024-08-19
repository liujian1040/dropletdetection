'''import json
import cv2
import base64
import numpy as np

json_file_path = "H:/pre-demo/orig/without-seed1-1_0_1.json"

# Read the JSON file
with open(json_file_path, "r") as file:
    json_data = json.load(file)


processed_image_path = "H:/pre-demo/orig/without-seed1-1_0_1.png"

# Load the processed image
processed_image = cv2.imread(processed_image_path)

# Convert the processed image to base64-encoded string
_, image_encoded = cv2.imencode(".png", processed_image)
image_data = base64.b64encode(image_encoded).decode("utf-8")

# Update the imageData field in the JSON dictionary
json_data["imageData"] = image_data

updated_json_file_path = "H:/pre-demo/original image/without-seed1-1_0_1.json"

# Save the updated JSON file
with open(updated_json_file_path, "w") as file:
    json.dump(json_data, file)
'''
# convert json file imagedata from original dir to processed dir
import os
import json
import cv2
import base64

# Set the paths to the folders containing the original images, processed images, and JSON label files
#original_images_folder = "H:/pre-demo/train/done"
#processed_images_folder = "H:/pre-demo/orig"
#json_folder = "H:/pre-demo/orig"
original_images_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/7"
processed_images_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/8"
json_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/8"


# Iterate over the files in the JSON label folder
for json_file_name in os.listdir(json_folder):
    if json_file_name.endswith(".json"):
        json_file_path = os.path.join(json_folder, json_file_name)

        # Read the JSON file and load its contents into a Python dictionary
        with open(json_file_path, "r") as file:
            json_data = json.load(file)

        # Get the corresponding image file name
        image_file_name = json_data["imagePath"]

        # Set the paths to the original image and processed image
        '''for original_image_name in os.listdir(original_images_folder):
            if original_image_name.endswith(".png"):
                original_image_path = os.path.join(original_images_folder, original_image_name)
        for processed_image_name in os.listdir(processed_images_folder):
            if processed_image_name.endswith(".png"):
                processed_image_path = os.path.join(processed_images_folder, processed_image_name)'''
        original_image_path = os.path.join(original_images_folder, image_file_name)
        processed_image_path = os.path.join(processed_images_folder, image_file_name)

        # Load the processed image
        processed_image = cv2.imread(processed_image_path)

        # Convert the processed image to base64-encoded string
        _, image_encoded = cv2.imencode(".png", processed_image)
        image_data = base64.b64encode(image_encoded).decode("utf-8")

        # Update the imageData field in the JSON dictionary
        json_data["imageData"] = image_data

        # Save the updated JSON file
        updated_json_file_path = os.path.join(json_folder, json_file_name)
        with open(updated_json_file_path, "w") as file:
            json.dump(json_data, file)

        print(f"Updated JSON file: {updated_json_file_path}")

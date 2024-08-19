import json
import cv2
import base64
import numpy as np
import os

json_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/val"

for json_file_name in os.listdir(json_folder):
    if json_file_name.endswith(".json"):
        json_file_path = os.path.join(json_folder, json_file_name)

        # Read the JSON file
        with open(json_file_path, "r") as file:
            json_data = json.load(file)

        image_file_name = json_data["imagePath"]
        image_path = os.path.join(json_folder, image_file_name)

        # Load the processed image
        processed_image = cv2.imread(image_path)
        _, image_encoded = cv2.imencode(".png", processed_image)
        image_data = base64.b64encode(image_encoded).decode("utf-8")

        # Update the imageData field in the JSON dictionary
        json_data["imageData"] = image_data

        # Save the updated JSON file
        updated_json_file_path = os.path.join(json_folder, json_file_name)
        with open(updated_json_file_path, "w") as file:
            json.dump(json_data, file)

        print(f"Updated JSON file: {updated_json_file_path}")
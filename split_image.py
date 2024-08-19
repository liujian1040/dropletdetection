import os
from PIL import Image

def split_image_batch(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 处理每个图像
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)
            split_image(image_path, output_folder)

def split_image(image_path, output_folder):
    # 加载图像
    image = Image.open(image_path)
    width, height = image.size
    split_width = width // 2
    split_height = height // 2

    # 分割图像
    image_parts = []
    for i in range(2):
        for j in range(2):
            left = j * split_width
            top = i * split_height
            right = left + split_width
            bottom = top + split_height
            image_part = image.crop((left, top, right, bottom))
            image_parts.append(image_part)

    # 保存图像部分
    base_image_name = os.path.splitext(os.path.basename(image_path))[0]
    for idx, image_part in enumerate(image_parts):
        image_part_name = f"{base_image_name}_part{idx+1}.png"
        image_part_path = os.path.join(output_folder, image_part_name)
        image_part.save(image_part_path)

# 输入和输出文件夹路径
input_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/val"
output_folder = "C:/Users/Administrator/Desktop/CystalDetection-master/val"

# 处理图像
split_image_batch(input_folder, output_folder)
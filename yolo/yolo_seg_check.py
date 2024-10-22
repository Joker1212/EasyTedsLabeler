import os
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def read_label_file(label_path):
    """
    读取新的标注文件格式，返回一个包含类别和归一化坐标的列表。
    """
    with open(label_path, 'r') as file:
        lines = file.readlines()
    annotations = []
    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x1, y1, x2, y2, x3, y3, x4, y4 = map(float, parts[1:])
        annotations.append((class_id, x1, y1, x2, y2, x3, y3, x4, y4))
    return annotations

def plot_image_with_boxes(image_path, annotations, image_size):
    """
    使用matplotlib绘制带有边界框的图片。
    """
    # 读取图片
    image = Image.open(image_path)
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # 显示原图
    ax[0].imshow(image)
    ax[0].set_title('Original Image')
    ax[0].axis('off')

    # 显示带有边界框的图片
    ax[1].imshow(image)
    ax[1].set_title('Image with Bounding Boxes')
    ax[1].axis('off')

    for class_id, x1, y1, x2, y2, x3, y3, x4, y4 in annotations:
        # 反归一化
        x1 *= image_size[0]
        y1 *= image_size[1]
        x2 *= image_size[0]
        y2 *= image_size[1]
        x3 *= image_size[0]
        y3 *= image_size[1]
        x4 *= image_size[0]
        y4 *= image_size[1]

        # 绘制多边形
        polygon = patches.Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], linewidth=1, edgecolor='r', facecolor='none')
        ax[1].add_patch(polygon)

    plt.show()

def check_annotation(image_dir, label_dir, image_name):
    """
    检查某个标注文件，并显示带有边界框的图片。
    """
    # 构建图片和标注文件的路径
    image_path = os.path.join(image_dir, image_name)
    label_path = os.path.join(label_dir, os.path.splitext(image_name)[0] + '.txt')

    # 读取标注文件
    annotations = read_label_file(label_path)

    # 获取图片的大小
    with Image.open(image_path) as img:
        image_size = img.size

    # 绘制带有边界框的图片
    plot_image_with_boxes(image_path, annotations, image_size)

if __name__ == '__main__':

    # 示例用法
    image_dir = 'new_dir/images/train'
    label_dir = 'new_dir/labels/train'
    # 随机抽取20张图像
    all_images = [f for f in os.listdir(image_dir) if f.endswith('.jpg') and int(f.split('.')[0]) <= 8000]
    selected_images = random.sample(all_images, 20)

    for image_name in selected_images:
        check_annotation(image_dir, label_dir, image_name)

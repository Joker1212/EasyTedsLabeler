import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def read_label_file(label_path):
    """
    读取COCO格式的标注文件，返回一个包含类别和归一化坐标的列表。
    """
    with open(label_path, 'r') as file:
        lines = file.readlines()
    annotations = []
    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center, y_center, width, height = map(float, parts[1:])
        annotations.append((class_id, x_center, y_center, width, height))
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

    for class_id, x_center, y_center, width, height in annotations:
        # 反归一化
        x_center *= image_size[0]
        y_center *= image_size[1]
        width *= image_size[0]
        height *= image_size[1]

        # 计算边界框的左上角坐标
        x_min = x_center - width / 2
        y_min = y_center - height / 2

        # 绘制边界框
        rect = patches.Rectangle((x_min, y_min), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax[1].add_patch(rect)

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
    image_name = '05437.jpg'

    check_annotation(image_dir, label_dir, image_name)

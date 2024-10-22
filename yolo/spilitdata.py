import os
import random
import shutil

# 定义路径
images_dir = 'table_det/cropped_images'
labels_dir = 'new_dir/labels/cropped'
train_images_dir = 'new_dir/images/train'
val_images_dir = 'new_dir/images/val'
train_labels_dir = 'new_dir/labels/train'
val_labels_dir = 'new_dir/labels/val'

# 创建目标文件夹
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

if __name__ == '__main__':

    # 获取所有图片文件
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # 划分数据集
    random.shuffle(image_files)
    train_size = len(image_files)
    val_size = int(len(image_files) * 0.1)
    train_images = image_files
    val_images = image_files[:val_size]

    # 重命名并复制图片和标注文件到训练集
    for i, image_name in enumerate(train_images):
        base_name = os.path.splitext(image_name)[0]
        new_name = f"{i + 1:05d}.jpg"
        new_label_name = f"{i + 1:05d}.txt"

        shutil.copy(os.path.join(images_dir, image_name), os.path.join(train_images_dir, new_name))
        label_file = os.path.join(labels_dir, f"{base_name}.txt")
        if os.path.exists(label_file):
            shutil.copy(label_file, os.path.join(train_labels_dir, new_label_name))

    # 重命名并复制图片和标注文件到验证集
    for i, image_name in enumerate(val_images):
        base_name = os.path.splitext(image_name)[0]
        new_name = f"{i + 1:05d}.jpg"
        new_label_name = f"{i + 1:05d}.txt"

        shutil.copy(os.path.join(images_dir, image_name), os.path.join(val_images_dir, new_name))
        label_file = os.path.join(labels_dir, f"{base_name}.txt")
        if os.path.exists(label_file):
            shutil.copy(label_file, os.path.join(val_labels_dir, new_label_name))

    print("数据集划分完成！")
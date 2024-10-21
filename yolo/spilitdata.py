import os
import random
import shutil

# 定义路径
images_dir = 'images'
labels_dir = 'new_dir/labels/train_all'
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

    # 重命名图片文件并记录新的文件名及对应的老文件名
    new_image_names = {}
    for i, image_file in enumerate(image_files):
        old_path = os.path.join(images_dir, image_file)
        new_name = f"{i+1:05d}.jpg"
        new_path = os.path.join(images_dir, new_name)
        os.rename(old_path, new_path)
        new_image_names[new_name] = image_file

    # 重命名对应的标注文件
    for new_image_name, old_image_name in new_image_names.items():
        base_name = os.path.splitext(new_image_name)[0]
        old_base_name = os.path.splitext(old_image_name)[0]
        old_label_file = os.path.join(labels_dir, f"{old_base_name}.txt")
        new_label_file = os.path.join(labels_dir, f"{base_name}.txt")
        if os.path.exists(old_label_file):
            os.rename(old_label_file, new_label_file)

    # 划分数据集
    new_image_names_list = list(new_image_names.keys())
    random.shuffle(new_image_names_list)
    train_size = int(len(new_image_names_list) * 0.9)
    train_images = new_image_names_list[:train_size]
    val_images = new_image_names_list[train_size:]

    # 移动图片和标注文件
    for image_name in train_images:
        base_name = os.path.splitext(image_name)[0]
        shutil.move(os.path.join(images_dir, image_name), os.path.join(train_images_dir, image_name))
        shutil.move(os.path.join(labels_dir, f"{base_name}.txt"), os.path.join(train_labels_dir, f"{base_name}.txt"))

    for image_name in val_images:
        base_name = os.path.splitext(image_name)[0]
        shutil.move(os.path.join(images_dir, image_name), os.path.join(val_images_dir, image_name))
        shutil.move(os.path.join(labels_dir, f"{base_name}.txt"), os.path.join(val_labels_dir, f"{base_name}.txt"))

    print("数据集划分完成！")

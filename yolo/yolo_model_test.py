from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def display_image_with_box(image_path, box):
    """
    显示带有边界框的图像。

    :param image_path: 图像文件的路径
    :param box: 边界框的坐标 [xmin, ymin, xmax, ymax]
    """
    # 打开图像
    image = Image.open(image_path)

    # 创建一个新的图形
    fig, ax = plt.subplots(1)

    # 显示图像
    ax.imshow(image)

    # 解包边界框坐标
    xmin, ymin, xmax, ymax = box

    # 计算边界框的宽度和高度
    width = xmax - xmin
    height = ymax - ymin

    # 创建一个矩形补丁
    rect = patches.Rectangle((xmin, ymin), width, height, linewidth=2, edgecolor='r', facecolor='none')

    # 将矩形补丁添加到图像中
    ax.add_patch(rect)

    # 显示图像
    plt.show()
if __name__ == '__main__':
    img_path = "/Users/macbookc23551/PycharmProjects/EasyTedsLabeler/outputs/image/37bea1eecff4edf1ea6e7eff7879257c2b8c5f8c.jpg"
    model = YOLO("./yolo11n-seg.pt")  # load a pretrained model (recommended for training)
    results = model(img_path, save_dir="./output")  # predict on an image
    # print(results)
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        for t_box in boxes:
            box = t_box.xyxy[0].numpy()
            display_image_with_box(img_path, box)
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        result.show()  # display to screen
        result.save(filename="result.jpg")
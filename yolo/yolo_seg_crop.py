import json
import os
import cv2

def validate_segmentation(segmentation):
    """
    验证 segmentation 是否只有一条记录且包含 8 个数值
    """
    if len(segmentation) != 1 or len(segmentation[0]) != 8:
        raise ValueError("Segmentation must contain exactly one list with 8 values.")
    return segmentation[0]

def adjust_segmentation(segmentation, xmin, ymin):
    """
    调整 segmentation 的坐标以适应裁剪后的图像
    """
    adjusted_segmentation = [point - (xmin if i % 2 == 0 else ymin) for i, point in enumerate(segmentation)]
    return [adjusted_segmentation]

def adjust_bbox(bbox, xmin, ymin):
    """
    调整 bbox 的坐标以适应裁剪后的图像
    """
    x, y, w, h = bbox
    adjusted_bbox = [0, 0, w, h]
    adjusted_bbox[0] = 0
    adjusted_bbox[1] = 0
    adjusted_bbox[2] = w - (xmin - x)
    adjusted_bbox[3] = h - (ymin - y)
    return adjusted_bbox
if __name__ == '__main__':

    # 读取原始的 COCO 标注文件
    input_annotation_file = 'table_det/train_all.json'
    output_annotation_file = 'table_det/cropped.json'
    image_dir = 'table_det/images'  # 原始图像文件所在的目录
    cropped_image_dir = 'table_det/cropped_images'  # 新的裁剪图像文件存储目录

    # 创建新的裁剪图像目录
    if not os.path.exists(cropped_image_dir):
        os.makedirs(cropped_image_dir)

    # 读取 COCO 标注文件
    with open(input_annotation_file, 'r') as f:
        coco_data = json.load(f)

    # 初始化新的 COCO 数据结构
    new_coco_data = {
        "images": [],
        "annotations": [],
        "categories": coco_data["categories"]
    }

    # 用于生成新的 image_id 和 annotation_id
    new_image_id = 0
    new_annotation_id = 0
    pad = 5
    # 遍历每个标注
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        bbox = annotation['bbox']
        segmentation = validate_segmentation(annotation['segmentation'])
        area = annotation['area']
        category_id = annotation['category_id']
        iscrowd = annotation['iscrowd']

        # 获取对应的图像信息
        image_info = next(img for img in coco_data['images'] if img['id'] == image_id)
        image_path = os.path.join(image_dir, image_info['file_name'])

        # 读取图像
        image = cv2.imread(image_path)
        h, w, _ = image.shape

        # 计算裁剪区域
        boxes = segmentation
        xmin = max(min(boxes[0], boxes[2], boxes[4], boxes[6]) - pad, 0)
        ymin = max(min(boxes[1], boxes[3], boxes[5], boxes[7]) - pad, 0)
        xmax = min(max(boxes[0], boxes[2], boxes[4], boxes[6]) + pad, w)
        ymax = min(max(boxes[1], boxes[3], boxes[5], boxes[7]) + pad, h)

        cropped_image = image[int(ymin):int(ymax), int(xmin):int(xmax), :]

        # 生成新的图像文件名
        new_image_filename = f"cropped_{image_info['file_name'].split('.')[0]}_{new_image_id}.jpg"
        new_image_path = os.path.join(cropped_image_dir, new_image_filename)

        # 保存裁剪后的图像
        cv2.imwrite(new_image_path, cropped_image)

        # 更新新的图像信息
        new_image_info = {
            "height": int(ymax - ymin),
            "width": int(xmax - xmin),
            "id": new_image_id,
            "file_name": new_image_filename
        }
        new_coco_data['images'].append(new_image_info)

        # 调整 segmentation 和 bbox 的坐标
        adjusted_segmentation = adjust_segmentation(segmentation, xmin, ymin)
        adjusted_bbox = adjust_bbox(bbox, xmin, ymin)

        # 更新新的标注信息
        new_annotation = {
            "segmentation": adjusted_segmentation,
            "iscrowd": iscrowd,
            "image_id": new_image_id,
            "bbox": adjusted_bbox,
            "area": area,
            "category_id": category_id,
            "id": new_annotation_id
        }
        new_coco_data['annotations'].append(new_annotation)

        # 更新 ID
        new_image_id += 1
        new_annotation_id += 1

    # 保存新的 COCO 标注文件
    with open(output_annotation_file, 'w') as f:
        json.dump(new_coco_data, f, indent=4)

    print(f"处理完成，新的标注文件已保存到 {output_annotation_file}")
    print(f"裁剪后的图像已保存到 {cropped_image_dir}")

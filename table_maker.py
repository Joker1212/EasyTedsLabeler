import argparse
import json
import os
import random
import shutil
import streamlit as st
from rapid_table import RapidTable
from rapidocr_onnxruntime import RapidOCR
from utils import format_html, add_newlines_to_html
import yaml

# 读取配置文件
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 从配置文件中读取参数
source_folder = config['source_folder']
target_folder = config['target_folder']
prefix = config['prefix']
model_path = config['model_path']
shuffle = config['shuffle']

# 初始化 OCR 和表格处理引擎
rapid_table = RapidTable(model_path=model_path)
ocr_engine = RapidOCR()



class HtmlTableProcessor:
    def __init__(self, source_folder, target_folder, prefix, shuffle=False):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.prefix = prefix
        self.selected_image = None
        self.html_str = None
        self.formatted_html = None
        self.shuffle = shuffle

        # 确保目标文件夹存在
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        if not os.path.exists(os.path.join(target_folder, "html")):
            os.makedirs(os.path.join(target_folder, "html"))

        self.metadata_file = os.path.join(target_folder, "metadata.jsonl")

    def select_image_path(self):
        st.sidebar.title("选择图片")
        images = [img for img in os.listdir(self.source_folder) if
                  os.path.isfile(os.path.join(self.source_folder, img)) and img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if self.shuffle and not st.session_state.get('selected_image'):
            random.shuffle(images)
        return st.sidebar.selectbox("请选择图片", images)

    def save_metadata(self, metadata_file, metadata):
        with open(metadata_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(metadata, ensure_ascii=False) + '\n')

    def gen_html(self, img_path):
        ocr_result, _ = ocr_engine(img_path)
        table_html_str, table_cell_bboxes, elapse = rapid_table(img_path, ocr_result)
        formatted_html = add_newlines_to_html(table_html_str)
        return formatted_html

    def process_image(self, img_name):
        img_path = os.path.join(self.source_folder, img_name)
        metadata_file = os.path.join(self.target_folder, "metadata.jsonl")

        # 检查是否为文件且为图片
        if not (os.path.isfile(img_path) and img_name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            st.error("无效的图片文件，请重新选择。")
            return

        # 复制图片到目标文件夹，并加上前缀
        new_img_name = f"{self.prefix}_{img_name}"
        new_img_path = os.path.join(self.target_folder, new_img_name)

        # 保存 HTML 文件，并加上前缀
        html_file_name = f"{os.path.splitext(new_img_name)[0]}.html"
        html_file_path = os.path.join(self.target_folder, "html", html_file_name)

        # 显示图片
        st.image(img_path, caption=new_img_name, use_column_width=True)

        # 按钮操作
        if st.button("生成HTML"):
            html_str = self.gen_html(img_path)
            st.success("table模型调用成功")
            formatted_html = format_html(html_str)
            st.session_state.html_str = html_str
            st.session_state.formatted_html = formatted_html

        if st.button("保存") and st.session_state.html_str:
            html_str = st.session_state.html_str.replace("\n", "")
            # 保存到 metadata.jsonl
            metadata = {"file_name": new_img_name, "html": html_str}
            self.save_metadata(metadata_file, metadata)
            shutil.copy(img_path, new_img_path)
            # 更新 HTML 文件
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(st.session_state.formatted_html)
                st.success("保存成功")
        # 展示编辑器和渲染结果
        if st.session_state.html_str:
            # 使用容器确保占据整个宽度
            with st.container():
                st.markdown("### HTML 编辑器")
                html_str = st.text_area("HTML", value=st.session_state.html_str, height=300, key="html_editor",
                                        on_change=self._on_change, args=(st.session_state.html_str,))
                st.session_state.html_str = html_str

                # 实时更新渲染结果
                st.markdown("### HTML 渲染结果")
                formatted_html = format_html(st.session_state.html_str)
                st.session_state.formatted_html = formatted_html
                st.components.v1.html(formatted_html, height=600, scrolling=True)

    def _on_change(self, html_str):
        st.session_state.html_str = html_str
        st.session_state.formatted_html = format_html(html_str)

    def run(self):
        if 'selected_image' not in st.session_state:
            st.session_state.selected_image = None
        # 侧边栏选择图片
        selected_image = self.select_image_path()
        # 当用户选择新图片时，清除旧的状态
        if selected_image != st.session_state.selected_image:
            st.session_state.selected_image = selected_image
            st.session_state.html_str = None
            st.session_state.formatted_html = None
            self.selected_image = selected_image
            self.html_str = ""
            self.formatted_html = ""
        if st.session_state.selected_image:
            self.process_image(st.session_state.selected_image)


def main():
    processor = HtmlTableProcessor(source_folder, target_folder, prefix, shuffle=shuffle)
    processor.run()


if __name__ == "__main__":
    main()

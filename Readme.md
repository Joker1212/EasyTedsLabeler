# 图片表格标注工具

## 简介

这是一个基于 Streamlit 的简单图片表格标注工具，用于从图片中提取表格信息并生成 HTML 文件。该工具使用了 `RapidOCR` 和 `RapidTable` 进行 OCR 和表格识别。

## 安装说明

1. **安装依赖库**：
```python
pip install streamlit pillow rapidocr_onnxruntime rapid_table
```
2. **下载模型文件**：
   - 下载 `ch_ppstructure_mobile_v2_SLANet.onnx` 模型文件，并将其放置在项目根目录下的 `models` 文件夹中。

## 使用说明
1. **配置信息**
   - 修改config.yaml文件，设置输入folder,输出folder等配置信息
2. **启动应用**：
   - streamlit run table_maker.py
3. **选择图片**：
   - 在侧边栏选择一张图片进行标注。
4. **生成 HTML**：
   - 点击“生成HTML”按钮，工具会自动识别表格并生成 HTML。
5. **修改html**：
   - 在html编辑器中根据图片和预览渲染结果对照进行修正微调
6. **保存结果**：
   - 点击“保存”按钮，保存生成的 HTML 文件和图片到指定的目标文件夹。

## 生成结果目录结构

生成的结果默认位于根目录下的 `outputs` 文件夹中，具体结构如下

outputs/ 

├── html/ 

│ └── example.html 

├── example.png 

└── metadata.jsonl

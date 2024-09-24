import re
from bs4 import BeautifulSoup


def format_html(html):
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')
    # 使用 prettify() 方法格式化 HTML
    formatted_html = soup.prettify()
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>Complex Table Example</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
    </head>
    <body>
    {formatted_html}
    </body>
    </html>
    """


def add_newlines_to_html(html):
    # 定义需要在前后添加换行符的标签列表
    tags_to_newline = ['<table>', '<tr>', '<body>', '<thead>', '<tbody>']
    close_tags_to_newline = ['</table>', '</tr>', '</body>', '</thead>', '</tbody>']

    # 使用正则表达式为每个指定开标签前后添加换行符
    for tag in tags_to_newline:
        html = re.sub(tag, f'\n{tag}\n', html)

    # 使用正则表达式为每个指定闭标签前后添加换行符
    for tag in close_tags_to_newline:
        html = re.sub(tag, f'\n{tag}\n', html)

    return html

import re
import os.path as osp
from io import BytesIO

import requests

from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Inches

invalid_char = r'<>:"/\|?*'
def insert_img(img_url: str, doc):
    image_from_url = requests.get(img_url)
    io_url = BytesIO(image_from_url.content)
    doc.add_picture(io_url, Inches(6))

def crawl_content(url: str) -> None:
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    all_tag = soup.find_all(re.compile(r'^(?:p$|h[1-6]|img)'))

    start, end = 0, len(all_tag)
    for i, tag in enumerate(all_tag):
        if re.findall(r'^<h1', str(tag)):
            start = i
            break
    for i, tag in enumerate(all_tag):
        if re.findall(r'^<h3', str(tag)):
            end = i - 1
            break
    all_tag = all_tag[start:end]

    doc_file = Document()
    for tag in all_tag:
        if re.findall(r'^<[ph]', str(tag)):
            doc_file.add_paragraph(tag.get_text())
        elif 'data-src' in tag.attrs: #imag
            insert_img(tag['data-src'], doc_file)
        
    title = ''
    for char in soup.title.string:
        if not char in invalid_char: title += char
    save_dir = osp.join('.', 'Output', title + '.docx')
    doc_file.save(save_dir)
import os
import re
from config import ALLOWED_EXTENSIONS

# 判断文件格式
def allowFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 获取文件路径
def getFilePath(image_url):
    file_name = re.findall(r"images/(.+)", image_url)[0]
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, '../static/images', file_name)
    return file_path
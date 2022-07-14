from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# 实例化app
app = Flask(__name__, static_folder='./images')
# 注册cors，允许访问所有api
CORS(app, resource=r'/*')
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
# 读取配置
app.config.from_object(Config)
# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)

from app import routes

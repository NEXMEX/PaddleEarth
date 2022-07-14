# 数据库配置
class Config(object):
    # 配置数据库地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:SchrodingersCat@localhost:3306/PaddleEarth'
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 禁止自动提交数据处理
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

# ip地址
host = '0.0.0.0'

# 端口
port = 80

# 公网地址
public_ip = '0.0.0.0'

# 文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'img', 'tiff', 'svg', 'PNG', 'JPG', 'JEPG', 'IMG', 'TIFF', 'SVG'])

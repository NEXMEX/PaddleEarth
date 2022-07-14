from app import app, db
from config import port, host
import pymysql

pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()

# # 删除表（用于调试）
# db.drop_all()
# 创建表
db.create_all()

if __name__ == '__main__':
    # 这个模式用于开发环境调试，部署线上需要使用WSGI替代
    app.run(port=port, host=host, debug=True)
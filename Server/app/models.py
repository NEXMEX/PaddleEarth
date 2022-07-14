from app import db

# 用户表
class User(db.Model):
    # 表名
    __tablename__ = 'users'
    # 字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    telephone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100), unique=False)

# 记录表
class Record(db.Model):
    # 表名
    __tablename__ = 'records'
    # 字段
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Integer, unique=False)
    image1_url = db.Column(db.String(100), unique=False)
    image2_url = db.Column(db.String(100), unique=False)
    result_url = db.Column(db.String(100), unique=False)
    index = db.Column(db.Text, unique=False)
    time = db.Column(db.String(20), unique=False)


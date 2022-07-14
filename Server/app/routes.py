import json
from flask import request, jsonify, send_file, make_response
import hashlib
import datetime
import os
from app import app, db
from app.models import User, Record
from utils import jwttoken, file, interpret
from config import port, host, public_ip
from time import sleep


# 注册
@app.route('/register', methods=["POST"])
def getRegisterRequest():
    # 接收post请求的参数
    result = request.get_json()
    print('\n', result, '\n')
    name = result['name']
    telephone = result['telephone']
    password = result['password']
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user = User.query.filter_by(telephone=telephone).first()
    # 判断用户是否已存在
    if user:
        result = {"code": 422, "message": "用户已存在"}
        return responseHeader(make_response(jsonify(result)))

    # 创建用户
    user = User(name=name, telephone=telephone, password=password)
    db.session.add(user)
    db.session.commit()

    # 注册成功
    result = {"code": 200, "message": "注册成功"}
    return responseHeader(make_response(jsonify(result)))


# 登录
@app.route('/login', methods=["POST"])
def getLoginRequest():
    # 接收post请求的参数
    result = request.get_json()
    telephone = result['telephone']
    password = result['password']
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user = User.query.filter_by(telephone=telephone).first()
    # 判断用户是否已存在
    if not user:
        result = {"code": 422, "message": "用户不存在"}
        return responseHeader(make_response(jsonify(result)))
    # 判断密码是否正确
    if user.password != password:
        result = {"code": 422, "message": "密码错误"}
        return responseHeader(make_response(jsonify(result)))

    # 发放token
    token = jwttoken.releaseToken(user.id)

    # 登录成功
    result = {"code": 200, "data": {"token": token}, "message": "登录成功"}
    return responseHeader(make_response(jsonify(result)))


# 修改密码
@app.route('/revise', methods=["POST"])
def getReviseRequest():
    # 接收post请求的参数
    result = request.get_json()
    telephone = result['telephone']
    new_password = result['new_password']
    new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

    # 判断用户是否已存在
    user = User.query.filter_by(telephone=telephone).first()
    if not user:
        result = {"code": 422, "message": "用户不存在"}
        return responseHeader(make_response(jsonify(result)))

    # 修改密码
    User.query.filter_by(telephone=telephone).update({"password": new_password})
    db.session.commit()

    # 修改成功
    result = {"code": 200, "message": "修改成功"}
    return responseHeader(make_response(jsonify(result)))


# 解译图像
@app.route('/interpret', methods=['POST'])
def getInterpretRequest():
    # 接收post请求的参数
    result = request.get_json()
    print('Request:', result)
    image1_url = result['image1_url']
    image2_url = result['image2_url']
    type = result['type']
    coordinate = result['coordinate']
    cur_time = datetime.datetime.now()
    time = datetime.datetime.strftime(cur_time, '%Y-%m-%d %H:%M')
    # 根据type返回不同结果
    try:
        if type == 0:
            result = interpret.target_extract(image1_url, coordinate)
            result_url = "http://" + public_ip + ":" + str(port) + "/images/" + os.path.basename(result['image_path'])
            index = {
                'image_path': result['image_path'],
                'coverage' : result['coverage'],
                'cover_score': result['cover_score'],
                'scale_score': result['scale_score'],
                'accessible_score': result['accessible_score'],
                'matching_score': result['matching_score'],
                'totality_level': result['totality_level']
            }
            index_str = json.dumps(index)
        elif type == 1:
            result = interpret.change_detect(image1_url, image2_url, coordinate)
            result_url = "http://" + public_ip + ":" + str(port) + "/images/" + os.path.basename(result['image_path'])
            index = {
                "change": result['change'],
                "early_coverage": result['early_coverage'],
                "later_coverage": result['later_coverage'],
                "scope": result['scope'],
                "strength": result['strength']
            }
            index_str = json.dumps(index)
        elif type == 2:
            result = interpret.target_detect(image1_url, coordinate)
            result_url = "http://" + public_ip + ":" + str(port) + "/images/" + os.path.basename(result['image_path'])
            index = {
                "name": result['name'],
                "amount": result['amount'],
                "amount_score": result['amount_score'],
                "scope_score": result['scope_score'],
                "density_score": result['density_score'],
                "rationality": result['rationality']
            }
            index_str = json.dumps(index)
        elif type == 3:
            result = interpret.terrian_classify(image1_url, coordinate)
            result_url = "http://" + public_ip + ":" + str(port) + "/images/" + os.path.basename(result['image_path'])
            index = {
                "building_coverage": result['building_coverage'],
                "road_coverage": result['road_coverage'],
                "forest_coverage": result['forest_coverage'],
                "rationality": result['rationality'],
                "availability": result['availability']
            }
            index_str = json.dumps(index)
        else:
            raise Exception('No such type.')
    except Exception as E:
        print('Error:', E)


    # 获取请求头中的token
    token_string = request.headers.get('Authorization')
    if token_string:
        if token_string.startswith('Bearer '):
            token_string = token_string[7:]
            payload = jwttoken.parseToken(token_string)
            user_id = payload.get('data').get('id')
            # 创建记录
            record = Record(user_id=user_id, type=type, image1_url=image1_url, image2_url=image2_url, result_url=result_url, index=index_str, time=time)
            db.session.add(record)
            db.session.commit()
        else:
            result = {"code": 401, "message": "验证失败"}
            return responseHeader(make_response(jsonify(result)))

    data = {
        "result_url": result_url,
        "index": index,
        "time": time
    }
    result = {"code": 200, "data": data, "message": "解译成功"}
    return responseHeader(make_response(jsonify(result)))


# 查询记录
@app.route('/query', methods=['GET'])
def getQueryRequest():
    # 获取请求头中的token
    token_string = request.headers.get('Authorization')

    if token_string and token_string.startswith('Bearer '):
        token_string = token_string[7:]
        payload = jwttoken.parseToken(token_string)
        user_id = payload.get('data').get('id')
        records = Record.query.filter_by(user_id=user_id).all()
        record_list = []
        for record_info in records:
            r = {
                "image1_url": record_info.image1_url,
                "type": record_info.type,
                "result_url": record_info.result_url,
                "index": json.loads(record_info.index),
                "time": record_info.time
            }
            record_list.append(r)

        result = {"code": 200, "data": record_list, "message": "查询成功"}
        return responseHeader(make_response(jsonify(result)))

    else:
        result = {"code": 401, "message": "权限不足"}
        return responseHeader(make_response(jsonify(result)))


# 上传图像
@app.route('/upload', methods=['POST'])
def getUploadRequest():
    f = request.files['file']
    if not (f and file.allowFile(f.filename)):
        result = {"code": 1001, "message": "文件格式错误"}
        return responseHeader(make_response(jsonify(result)))

    cur_time = datetime.datetime.now()
    time = datetime.datetime.strftime(cur_time, '%Y-%m-%d %H:%M:%S')
    name_tuple = f.filename.rpartition('.')

    # 文件名加密
    name = hashlib.md5((name_tuple[0] + time).encode(encoding='UTF-8')).hexdigest()
    file_name = name + name_tuple[1] + name_tuple[2]

    # 保存图片到images文件夹
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, '../static/images', file_name)
    f.save(upload_path)

    image_url = "http://"+ public_ip +":"+str(port)+"/images/"+file_name

    result = {"code": 200, "data": {"image_url": image_url}, "message": "上传成功"}
    return responseHeader(make_response(jsonify(result)))


# 下载图像
@app.route('/download', methods=['POST'])
def getDownloadRequest():
    # 接收post请求的参数
    result = request.get_json()
    image_url = result['image_url']
    image_path = file.getFilePath(image_url)
    result = send_file(image_path)
    return responseHeader(make_response(result))


# 图像查看
@app.route("/images/<file_name>")
def getLookupRequest(file_name):
    basepath = os.path.dirname(__file__)
    image_path = os.path.join(basepath, '../static/images', file_name)
    result = send_file(image_path)
    return responseHeader(make_response(result))


# response请求头
def responseHeader(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

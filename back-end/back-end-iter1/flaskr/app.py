import requests
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import config
import re
import json
import paramiko
import os
from PIL import Image
from database import db
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS




rasperry_ip='192.168.234.137'
tongue_ip='http://192.168.234.83:5003/tongue'
teeth_ip='http://192.168.43.209:5001/teeth'
cancer_ip='http://192.168.43.188:5002/cancer'
threedim_ip='http://192.168.234.83:5004'

app = Flask(__name__)
CORS(app)
app.config.from_object(config.Config)
app.config['WTF_CSRF_ENABLED'] = False
csrf = CSRFProtect(app)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

cur_pic_route=''
cur_pic=''


@app.route('/')
def home():
    return "Hello, world!"

'''
这是登录部分的开始
'''

@app.before_request
def create_tables():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    from models import User  # 将导入移动到函数内部以避免循环导入
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in', 'status': 'error'}), 400
    from forms import RegistrationForm
    from models import User
    form = RegistrationForm(request.form)
    if form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Your account has been created! You are now able to log in', 'status': 'success'}), 201
    else:
        errors = form.errors
        return jsonify({'message': 'Registration failed', 'errors': errors, 'status': 'error'}), 400

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
        #return redirect(url_for('remembered'))
    from forms import LoginForm  # 将导入移动到函数内部以避免循环导入
    from models import User
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return jsonify({'message': 'Your account has been logged in', 'status': 'success'}), 201
        else:
            return jsonify({'message': 'log in failed,wrong username or password', 'status': 'error'}), 400
    else:
        return jsonify({'message': 'log in failed,wrong data form', 'status': 'error'}), 400


@app.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'your account has been safely logged out', 'status': 'success'}), 201


@app.route('/hello')
def hello():
    return 'Hello, World!'

'''
这是登录部分的结束
'''

'''
这是核心功能的开始

'''
@app.route('/getpictures_teeth',methods=['POST','GET'])
def getpictures_teeth():
    # 检查请求中是否包含文件
    print(request.files)
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    # 如果用户没有选择文件
    if file.filename == '':
        return 'No selected file', 400

    # 保存文件
    if file:
        save_path = os.path.join('test', file.filename)  # 文件保存路径
        file.save(save_path)
        return file.filename, 200


@app.route('/prepare_teeth', methods=['POST', 'GET'])
def prepare_teeth():
    import datetime

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"picture/capture_{timestamp}.jpg"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(rasperry_ip, username='planet', password='831143')

    # 运行拍照命令并保存图片
    # command = f"libcamera-jpeg -o /home/planet/pi/capture_{timestamp}.jpg -t 500"
    command = f"fswebcam -r 2560x1600 --no-banner /home/planet/pi/capture_{timestamp}.jpg "
    ssh.exec_command(command)

    # 等待命令执行完成（可以适当等待一段时间，具体根据情况调整）
    import time
    time.sleep(2)  # 等待拍照完成

    sftp = ssh.open_sftp()
    local_path = filename
    sftp.get(f"/home/planet/pi/capture_{timestamp}.jpg", local_path)
    sftp.close()
    ssh.close()

    return jsonify({'message':f"capture_{timestamp}.jpg" , 'status': 'success'}), 200

@app.route('/shot_teeth/<filename>', methods=['GET','POST'])
def shot_teeth(filename):
    return send_from_directory('test', filename)

    

@app.route('/confirm_shot_teeth/<picname>',methods=['POST','GET'])
def confirm_shot_teeth(picname):
    # picname = request.form.get('picname')

    image_path = 'test/'+picname
    url = teeth_ip



    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        response = requests.post(url, files=files)


    import qianfan

    os.environ["QIANFAN_ACCESS_KEY"] = "ALTAK8VmX9lGmRSpxsE3BP5a5i"
    os.environ["QIANFAN_SECRET_KEY"] = "65889326e24d48909ce8ea6a07f38b3f"
    response_json_str = json.dumps(response.json())
    chat_comp = qianfan.ChatCompletion()
    print(response.json())
    sentence = "我的口腔有" + response.json()['message'] + "的疾病，请分点提供一些口腔健康的建议，请按如下的json格式给我：{\"analyse\":[{\"title\":{},\"content\":{}}]}只要单纯的json对象，不需要其它任何多余语言。"
    resp = chat_comp.do(model="ERNIE-Lite-8K-0308", messages=[{
        "role": "user",
        "content": sentence
    }])

    # 提取result字段中的JSON内容
    result_text = resp["body"]["result"]
    print(result_text)
    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
    if json_match:
        result_json = json_match.group(0)
        try:
            parsed_json = json.loads(result_json)

            # 将content字段中的每一段分成item数组


            # for section in parsed_json.get('analyse', []):
            #     if 'content' in section:
            #         section['content'] = section['content'].split(',')

            return jsonify({'message': parsed_json,'problem':response.json(), 'status': 'success'}), 200
        except json.JSONDecodeError as e:
            return jsonify({'message': 'Failed to decode JSON', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'No JSON found in response', 'status': 'failure'}), 500


#
# @app.route('/gpt_teeth',methods=['POST','GET'])
# def gpt_teeth():
#     gpt = request.form.get('gpt')
#     if(gpt=='1'):
#         import os
#         import qianfan
#
#
#         os.environ["QIANFAN_ACCESS_KEY"] = ""
#         os.environ["QIANFAN_SECRET_KEY"] = ""
#
#         chat_comp = qianfan.ChatCompletion()
#         sentence="请提供一些口腔ph过低的建议，不要分点回答，请直接给出建议"
#
#
#         resp = chat_comp.do(model="ERNIE-Lite-8K-0308", messages=[{
#             "role": "user",
#             "content": sentence
#         }])
#
#         print(resp["body"])
#         return jsonify({'message': resp["body"], 'status': 'success'}), 200
#
#
#
#
#     else:
#         return jsonify({'message': 'chat failed', 'status': 'error'}), 400


@app.route('/video_tongue', methods=['POST', 'GET'])
def video_tongue():
    video = request.form.get('video')
    if (video == '1'):
        pass
        # 向开发板发送预览请求


    else:
        return jsonify({'message': 'shot failed', 'status': 'error'}), 400


@app.route('/getpictures_tongue',methods=['POST','GET'])
def getpictures_tongue():
    # 检查请求中是否包含文件
    print(request.files)
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    # 如果用户没有选择文件
    if file.filename == '':
        return 'No selected file', 400

    # 保存文件
    if file:
        save_path = os.path.join('test', file.filename)  # 文件保存路径
        file.save(save_path)
        return file.filename, 200

@app.route('/prepare_tongue', methods=['POST', 'GET'])
def prepare_tongue():
    import datetime

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"picture/capture_{timestamp}.jpg"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(rasperry_ip, username='planet', password='831143')

    # 运行拍照命令并保存图片
    # command = f"libcamera-jpeg -o /home/planet/pi/capture_{timestamp}.jpg -t 1000"
    command = f"fswebcam -r 2560x1600 --no-banner /home/planet/pi/capture_{timestamp}.jpg "
    ssh.exec_command(command)

    # 等待命令执行完成（可以适当等待一段时间，具体根据情况调整）
    import time
    time.sleep(2.5)  # 等待拍照完成

    sftp = ssh.open_sftp()
    local_path = filename
    sftp.get(f"/home/planet/pi/capture_{timestamp}.jpg", local_path)
    sftp.close()
    ssh.close()

    return jsonify({'message':f"capture_{timestamp}.jpg" , 'status': 'success'}), 200




@app.route('/shot_tongue/<filename>', methods=['GET','POST'])
def shot_tongue(filename):
    return send_from_directory('test', filename)



@app.route('/confirm_shot_tongue/<picname>', methods=['POST', 'GET'])
def confirm_shot_tongue(picname):
    # picname = request.form.get('picname')
    image_path = 'test/'+picname
    url = tongue_ip

    img = Image.open(image_path)
    img_resized = img.resize((64,64), Image.Resampling.LANCZOS)
    img_resized.save(image_path)


    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        response = requests.post(url, files=files)

    import os
    import qianfan

    os.environ["QIANFAN_ACCESS_KEY"] = "ALTAK8VmX9lGmRSpxsE3BP5a5i"
    os.environ["QIANFAN_SECRET_KEY"] = "65889326e24d48909ce8ea6a07f38b3f"

    chat_comp = qianfan.ChatCompletion()
    sentence = "我的舌苔颜色为"+response.json()['coating_color']+"，我的舌头颜色为"+response.json()['tongue_color']+"，我的舌头的薄厚指标是"+response.json()['tongue_thickness']+"，我的舌头腐或腻的指标为"+response.json()['rotandgreasy']+"我的舌头的ph是6.86。请分析一下我的口腔状况并提供一些中医和西医方面的口腔健康的建议，请按如下的json格式给我：{\"condition\":[{\"titile\":{},\"content\":{}}],\"analyse\":[{\"title\":{},\"content\":{}}]}只要单纯的json对象，不需要其它任何多余语言。"
    resp = chat_comp.do(model="ERNIE-Lite-8K-0308", messages=[{
        "role": "user",
        "content": sentence
    }])
    # 提取result字段中的JSON内容
    result_text = resp["body"]["result"]
    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
    if json_match:
        result_json = json_match.group(0)
        try:
            parsed_json = json.loads(result_json)

            # 将content字段中的每一段分成item数组
            for section in parsed_json.get('condition', []):
                if 'content' in section:
                    # section['content'] = section['content'].split('\n')
                    if isinstance(section['content'], dict):
                        # 如果 content 是字典，可以直接使用
                        section['content'] = section['content']
                    elif isinstance(section['content'], str):
                        # 如果 content 是字符串，按行分割
                        section['content'] = section['content'].split('\n')
            for section in parsed_json.get('analyse', []):
                if 'content' in section:
                    # section['content'] = section['content'].split('\n')
                    if isinstance(section['content'], dict):
                        # 如果 content 是字典，可以直接使用
                        section['content'] = section['content']
                    elif isinstance(section['content'], str):
                        # 如果 content 是字符串，按行分割
                        section['content'] = section['content'].split('\n')
            return jsonify({'message': parsed_json, 'status': 'success'}), 200
        except json.JSONDecodeError as e:
            return jsonify({'message': 'Failed to decode JSON', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'No JSON found in response', 'status': 'failure'}), 500

    # print(resp["body"])
    # return jsonify({'message': resp["body"], 'status': 'success'}), 200
    # return jsonify({'message': 'Image sent successfully', 'response': response.json()})




# @app.route('/gpt_tongue', methods=['POST', 'GET'])
# def gpt_tongue():
#     gpt = request.form.get('gpt')
#     if (gpt == '1'):
#         import os
#         import qianfan
#
#         os.environ["QIANFAN_ACCESS_KEY"] = ""
#         os.environ["QIANFAN_SECRET_KEY"] = ""
#
#         chat_comp = qianfan.ChatCompletion()
#         sentence = "请提供一些口腔ph过低的建议，不要分点回答，请直接给出建议"
#
#         resp = chat_comp.do(model="ERNIE-Lite-8K-0308", messages=[{
#             "role": "user",
#             "content": sentence
#         }])
#
#         print(resp["body"])
#         return jsonify({'message': resp["body"], 'status': 'success'}), 200



    #
    # else:
    #     return jsonify({'message': 'chat failed', 'status': 'error'}), 400

@app.route('/prepare_cancer', methods=['POST', 'GET'])
def prepare_cancer():
    import datetime

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"picture/capture_{timestamp}.jpg"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(rasperry_ip, username='planet', password='831143')

    # 运行拍照命令并保存图片
    # command = f"libcamera-jpeg -o /home/planet/pi/capture_{timestamp}.jpg -t 500"
    command = f"fswebcam -r 2560x1600 --no-banner /home/planet/pi/capture_{timestamp}.jpg "
    ssh.exec_command(command)

    # 等待命令执行完成（可以适当等待一段时间，具体根据情况调整）
    import time
    time.sleep(2)  # 等待拍照完成

    sftp = ssh.open_sftp()
    local_path = filename
    sftp.get(f"/home/planet/pi/capture_{timestamp}.jpg", local_path)
    sftp.close()
    ssh.close()

    return jsonify({'message':f"capture_{timestamp}.jpg" , 'status': 'success'}), 200


@app.route('/getpictures_cancer',methods=['POST','GET'])
def getpictures_cancer():
    # 检查请求中是否包含文件
    print(request.files)
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    # 如果用户没有选择文件
    if file.filename == '':
        return 'No selected file', 400

    # 保存文件
    if file:
        save_path = os.path.join('test', file.filename)  # 文件保存路径
        file.save(save_path)
        return file.filename, 200

@app.route('/shot_cancer/<filename>', methods=['GET','POST'])
def shot_cancer(filename):
    return send_from_directory('test', filename)






@app.route('/confirm_shot_cancer/<picname>', methods=['POST', 'GET'])
def confirm_shot_cancer(picname):
    # picname = request.form.get('picname')
    image_path = 'test/'+picname
    url = cancer_ip


    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        response = requests.post(url, files=files)

    import os
    import qianfan

    os.environ["QIANFAN_ACCESS_KEY"] = "ALTAK8VmX9lGmRSpxsE3BP5a5i"
    os.environ["QIANFAN_SECRET_KEY"] = "65889326e24d48909ce8ea6a07f38b3f"

    chat_comp = qianfan.ChatCompletion()
    sentence = "我"+response.json()['message']+"。请提供一些口腔健康的建议，请按如下的json格式给我：{\"analyse\":[{\"title\":{},\"content\":{}}]}只要单纯的json对象，不需要其它任何多余语言。"
    resp = chat_comp.do(model="ERNIE-Lite-8K-0308", messages=[{
        "role": "user",
        "content": sentence
    }])
    # 提取result字段中的JSON内容
    result_text = resp["body"]["result"]
    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
    if json_match:
        result_json = json_match.group(0)
        try:
            parsed_json = json.loads(result_json)
            print(parsed_json)


            # 将content字段中的每一段分成item数组
            for section in parsed_json.get('condition', []):


                if 'content' in section:
                    # section['content'] = section['content'].split('\n')
                    if isinstance(section['content'], dict):
                        # 如果 content 是字典，可以直接使用
                        section['content'] = section['content']
                    elif isinstance(section['content'], str):
                        # 如果 content 是字符串，按行分割
                        section['content'] = section['content'].split('\n')

            for section in parsed_json.get('analyse', []):
                if 'content' in section:
                    # section['content'] = section['content'].split('\n')
                    if isinstance(section['content'], dict):
                        # 如果 content 是字典，可以直接使用
                        section['content'] = section['content']
                    elif isinstance(section['content'], str):
                        # 如果 content 是字符串，按行分割
                        section['content'] = section['content'].split('\n')
            return jsonify({'message': parsed_json,'problem': response.json(), 'status': 'success'}), 200
        except json.JSONDecodeError as e:
            return jsonify({'message': 'Failed to decode JSON', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'No JSON found in response', 'status': 'failure'}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5173)

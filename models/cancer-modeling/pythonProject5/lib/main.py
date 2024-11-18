import torch
import torchvision.transforms as transforms
from PIL import Image
import _init_paths
import models
from config import config
from config import update_config
import argparse
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet18
from PIL import Image
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/cancer', methods=['POST', 'GET'])
def cancer():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 保存文件到本地并验证
    save_path = f'../pics/{file.filename}'
    file.save(save_path)

    def parse_args(subdir):
        parser = argparse.ArgumentParser(description='Test classification network')
        parser.add_argument('--cfg', help='experiment configure file name', type=str,
                            default="E:\\mybackup\\pythonProject5\\experiments\\cls_hrnet_w18_sgd_lr5e-2_wd1e-4_bs32_x100.yaml")
        parser.add_argument('--modelDir', help='model directory', type=str, default='')
        parser.add_argument('--logDir', help='log directory', type=str, default='')
        parser.add_argument('--dataDir', help='data directory', type=str, default='')
        parser.add_argument('--subDir', help='sub directory', type=str, default=subdir)
        parser.add_argument('--testModel', help='testModel', type=str,
                            default='E:\\mybackup\\pythonProject5\\save_weights\\cls_hrnet-v4_4-18-19_tcv.pth')
        args = parser.parse_args()
        update_config(config, args)
        return args

    def load_image(image_path):
        try:
            input_image = Image.open(image_path).convert('RGB')
        except Exception as e:
            return None

        input_image = input_image.resize((config.MODEL.IMAGE_SIZE[1], config.MODEL.IMAGE_SIZE[0]))
        image_array = np.array(input_image, dtype=np.float32) / 255.0
        input_tensor = torch.tensor(image_array, dtype=torch.float32).permute(2, 0, 1)
        preprocess = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        input_tensor = preprocess(input_tensor)
        input_tensor = input_tensor.unsqueeze(0)
        return input_tensor

    subdir = 'v4'
    args = parse_args(subdir)

    model = eval('models.' + config.MODEL.NAME + '.get_cls_net')(config)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(args.testModel, map_location=device))
    model = model.to(device)
    model.eval()

    image_path = save_path
    input_tensor = load_image(image_path)
    if input_tensor is None:
        return jsonify ({'message':'error'}),500

    input_tensor = input_tensor.to(device)

    with torch.no_grad():
        output = model(input_tensor)

    _, predicted_class = torch.max(output, 1)

    class_map = {
        0: '有低风险得口腔癌',
        1: '有低风险得口腔癌',
        2: '有低风险得口腔癌',
        3: '口腔状态正常',
        4: '口腔有溃疡'
    }

    result = class_map.get(predicted_class.item(), '未知类别')
    print(f'Result: {result}')
    return jsonify ({'message':f'{result}'})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
# Define the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')






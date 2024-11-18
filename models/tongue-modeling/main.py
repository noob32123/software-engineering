import queue
import tempfile
import torch
import torchvision.transforms.functional as TF
from PIL import Image
import numpy as np
from yolov5 import load as load_yolov5
from application.net.model.unet import UNet
from application.net.model.resnet import ResNetPredictor
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/tongue', methods=['POST', 'GET'])
def tongue():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        # 如果没有文件部分，返回错误信息
        return jsonify({'message': 'No file part'}), 400

    # 从请求中获取文件
    file = request.files['file']
    # 如果没有选择文件，返回错误信息
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    save_path = f'{file.filename}'
    file.save(save_path)

    class TonguePredictor:
        _instance = None
        _initialized = False

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self,
                     yolo_path='yolov5.pt',
                     unet_path='unet.pth',
                     resnet_path=[
                         'tongue_color.pth',
                         'tongue_coat_color.pth',
                         'thickness.pth',
                         'rot_and_greasy.pth'
                     ]
                     ):
            if self._initialized:
                return
            self.device = torch.device('cpu')

            # yolov5模型
            self.yolo = load_yolov5(yolo_path, device='cpu')

            # UNet模型
            self.unet = UNet()
            self.unet.load_state_dict(torch.load(unet_path, map_location=self.device))
            self.unet.eval()

            # 残差网络
            self.resnet = ResNetPredictor(resnet_path)
            self.queue = queue.Queue()

            TonguePredictor._initialized = True

        def __predict(self, img, record_id, fun):
            """
            预测舌像
            :param img: 图片文件
            :param record_id: 记录id
            :param fun: 回调函数
            :return:
            """
            predict_img = Image.open(img).convert('RGB')

            # 舌体定位
            self.yolo.eval()
            with torch.no_grad():
                pred = self.yolo(predict_img)
            if len(pred.xyxy[0]) < 1:
                fun(tongue_color=None,
                    coating_color=None,
                    tongue_thickness=None,
                    rot_greasy=None)
                return
            elif len(pred.xyxy[0]) > 1:
                fun(tongue_color=None,
                    coating_color=None,
                    tongue_thickness=None,
                    rot_greasy=None)
                return

            # 舌体分割
            with torch.no_grad():
                x1, y1, x2, y2 = (
                    pred.xyxy[0][0, 0].item(), pred.xyxy[0][0, 1].item(), pred.xyxy[0][0, 2].item(),
                    pred.xyxy[0][0, 3].item())
                cropped_img = predict_img.crop((x1, y1, x2, y2))
                cropped_img = cropped_img.resize((224, 224))
                image_tensor = TF.to_tensor(cropped_img).unsqueeze(0)
                output = self.unet(image_tensor)
                mask = output.squeeze().cpu().numpy() > 0.5
                segmented_img = np.array(cropped_img) * mask[..., np.newaxis]
                result_img = Image.fromarray(segmented_img.astype(np.uint8)).convert("RGB")

            # 舌体分析
            result = self.resnet.predict(result_img)

            # 对应结果的实际意义
            tongue_color_map = ["淡百舌", "淡红舌", "红舌", "绛舌", "青紫舌"]
            coating_color_map = ["白苔", "黄苔", "灰黑苔"]
            tongue_thickness_map = ["薄", "厚"]
            rot_and_greasy_map = ["腻", "腐"]

            predict_result = {
                "tongue_color": tongue_color_map[result[0]] if result[0] is not None else None,
                "coating_color": coating_color_map[result[1]] if result[1] is not None else None,
                "tongue_thickness": tongue_thickness_map[result[2]] if result[2] is not None else None,
                "rot_and_greasy": rot_and_greasy_map[result[3]] if result[3] is not None else None
            }

            # 保存结果
            fun(tongue_color=predict_result['tongue_color'],
                coating_color=predict_result['coating_color'],
                tongue_thickness=predict_result['tongue_thickness'],
                rot_greasy=predict_result['rot_and_greasy'])

            return predict_result

        def predict(self, img, record_id, fun):
            """
            复制图片到临时文件，然后放入队列
            :param img:
            :param record_id:
            :param fun:
            :return:
            """
            try:
                img.seek(0)
                tmpfile = tempfile.SpooledTemporaryFile()
                content = img.read()
                tmpfile.write(content)
                self.queue.put((tmpfile, record_id, fun))
                img.seek(0)
                return {"code": 0}
            except Exception as e:
                return {"code": 3}

        def main(self):
            """
            不断读取队列中的图片进行预测
            :return:
            """
            while True:
                if self.queue.empty():
                    break
                img, record_id, fun = self.queue.get()
                try:
                    self.__predict(img, record_id, fun)
                except Exception as e:
                    print(e)
                    fun(tongue_color=None,
                        coating_color=None,
                        tongue_thickness=None,
                        rot_greasy=None)
                finally:
                    img.close()

        def dummy_callback(self,tongue_color, coating_color, tongue_thickness, rot_greasy):
            print(tongue_color)
            print("testingtestingtesting^^^^^^")
            self.tc=tongue_color
            self.cc=coating_color
            self.tt=tongue_color
            self.rg=rot_greasy
            print(f"Tongue Color: {tongue_color}, Coating Color: {coating_color}, "
                  f"Tongue Thickness: {tongue_thickness}, Rot and Greasy: {rot_greasy}")

    # 创建预测器实例
    predictor = TonguePredictor()
    # 模拟图像输入
    image_path = save_path
    with open(image_path, 'rb') as img:
        predictor.predict(img, record_id=1, fun=predictor.dummy_callback)
    # 启动预测器
    predictor.main()
    print("finished")
    print(predictor.tc)
    print(predictor.cc)
    print(predictor.tt)
    print(predictor.rg)
    return jsonify({'tongue_color': predictor.tc, 'coating_color': predictor.cc,'tongue_thickness': predictor.tt, 'rotandgreasy': predictor.rg}),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

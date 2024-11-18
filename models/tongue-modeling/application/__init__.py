import queue
import tempfile
import torch
import torchvision.transforms.functional as TF
from PIL import Image
import numpy as np
from yolov5 import load as load_yolov5
from application.net.model.unet import UNet
from application.net.model.resnet import ResNetPredictor

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
        print("舌体定位")
        with torch.no_grad():
            pred = self.yolo(predict_img)
        if len(pred.xyxy[0]) < 1:
            # 图片不合法
            fun(event_id=record_id,
                tongue_color=None,
                coating_color=None,
                tongue_thickness=None,
                rot_greasy=None,
                code=201)
            print("图片不合法，没舌头")
            return
        elif len(pred.xyxy[0]) > 1:
            # 图片不合法
            fun(event_id=record_id,
                tongue_color=None,
                coating_color=None,
                tongue_thickness=None,
                rot_greasy=None,
                code=202)
            print("图片不合法，舌头太多了")
            return
        # 舌体分割
        print("舌体分割")
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

        result = self.resnet.predict(result_img)
        print("舌体分析")

        predict_result = {
            "code": 0,
            'tongue_color': result[0],
            'tongue_coat_color': result[1],
            'thickness': result[2],
            'rot_and_greasy': result[3]
        }
        # 保存结果
        fun(event_id=record_id,
            tongue_color=result[0],
            coating_color=result[1],
            tongue_thickness=result[2],
            rot_greasy=result[3],
            code=1)

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
                continue
            img, record_id, fun = self.queue.get()
            try:
                self.__predict(img, record_id, fun)
            except Exception as e:
                print(e)
                fun(event_id=record_id,
                    tongue_color=None,
                    coating_color=None,
                    tongue_thickness=None,
                    rot_greasy=None,
                    code=203)
            finally:
                img.close()

# 示例代码，用于本地测试
if __name__ == "__main__":
    def dummy_callback(event_id, tongue_color, coating_color, tongue_thickness, rot_greasy, code):
        print(f"Event ID: {event_id}, Tongue Color: {tongue_color}, Coating Color: {coating_color}, "
              f"Tongue Thickness: {tongue_thickness}, Rot and Greasy: {rot_greasy}, Code: {code}")

    # 创建预测器实例
    predictor = TonguePredictor()

    # 模拟图像输入
    image_path = '464.jpg'  # 替换为实际的图像路径
    with open(image_path, 'rb') as img:
        predictor.predict(img, record_id=1, fun=dummy_callback)

    # 启动预测器
    predictor.main()

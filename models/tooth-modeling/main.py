import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet18
from PIL import Image
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/teeth', methods=['POST', 'GET'])
def teeth():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        # 如果没有文件部分，返回错误信息
        return jsonify({'message': 'No file part'}), 400

    # 从请求中获取文件
    file = request.files['file']
    # 如果没有选择文件，返回错误信息
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 构建保存路径，确保在任何环境下都有效
    save_path = os.path.join('pics', file.filename)

    # 确保保存目录存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 保存文件到本地路径，并继续处理
    try:
        file.save(save_path)
        print('File saved successfully')
    except Exception as e:
        print(f'Error saving file: {e}')
        return jsonify({'message': 'Error saving file'}), 500

    # 检查设备是否支持CUDA（GPU），否则使用CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 定义模型类（与训练时使用的相同）
    class CustomModel(nn.Module):
        def __init__(self):
            super(CustomModel, self).__init__()
            # 使用ResNet18预训练模型
            self.model = resnet18(weights=True)
            # 将最后的全连接层修改为与分类数相匹配
            self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

        # 前向传播函数
        def forward(self, x):
            return self.model(x)

    # 定义从检查点加载模型的函数
    def load_model(checkpoint_path):
        model = CustomModel()  # 初始化模型
        # 加载模型参数
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        # 将模型移动到计算设备（GPU或CPU）
        model.to(device)
        # 设置模型为评估模式
        model.eval()
        return model

    # 定义预处理输入图像的函数
    def preprocess_image(image_path):
        # 打开图像并将其转换为RGB模式
        image = Image.open(image_path).convert('RGB')
        # 定义图像预处理操作
        preprocess = transforms.Compose([
            transforms.Resize((128, 128)),  # 调整图像大小为128x128，确保与训练时一致
            transforms.ToTensor(),  # 转换为Tensor
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),  # 归一化
        ])
        # 预处理图像并添加批量维度，然后移动到计算设备
        image_tensor = preprocess(image).unsqueeze(0).to(device)
        return image_tensor

    # 定义用于预测图像类别的函数
    def predict(image_path, model, class_names):
        # 预处理输入图像
        image_tensor = preprocess_image(image_path)
        # 禁用梯度计算，因为这是推理过程
        with torch.no_grad():
            # 通过模型获取输出
            outputs = model(image_tensor)
            # 获取预测的类别
            _, predicted = torch.max(outputs, 1)
            # 根据预测结果返回对应的类别名称
            predicted_class = class_names[predicted.item()]
        return predicted_class

    # 从检查点加载训练好的模型
    checkpoint_path = os.path.join("model_checkpoints", "best_model.pth")  # 模型检查点的路径
    num_classes = 6  # 类别数量，确保与训练数据中的类别数相同
    model = load_model(checkpoint_path)  # 加载模型

    # 定义类别名称，确保与训练时使用的类别顺序相同cd
    class_names = ['Calculus', 'Caries', 'Gingivitis', 'Ulcers', 'Tooth Discoloration', 'Hypodontia']
    # 对应的中文类别名称
    class_names_cn = ['牙结石', '龋齿', '牙龈炎', '溃疡', '牙齿变色', '牙齿结构异常']

    # 输入图像的路径
    image_path = save_path  # 此处为保存的文件路径

    # 预测输入图像的类别
    predicted_class = predict(image_path, model, class_names)  # 返回英文类别
    predicted_class_cn = class_names_cn[class_names.index(predicted_class)]  # 查找对应的中文类别

    # 打印预测结果
    print(f'{predicted_class_cn}')
    # 返回预测结果
    result = f'{predicted_class_cn}'
    return jsonify({'message': result}), 500  # 将预测结果封装成JSON并返回，状态码500表示服务器处理时出现问题


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001)
    # Define the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

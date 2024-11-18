import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os
from PIL import Image

# 定义设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'使用设备: {device}')

# 定义类别数
num_classes = 6
class_names = ['Calculus', 'Caries', 'Gingivitis', 'Ulcers', 'Tooth Discoloration', 'Hypodontia']

# 数据预处理
test_transforms = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

# 测试集路径
test_dir = 'kaggle/working/dataset/test'  # 这里修改为测试集路径

# 加载测试数据集
test_dataset = datasets.ImageFolder(test_dir, transform=test_transforms)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)


# 定义模型
class CustomModel(nn.Module):
    def __init__(self, num_classes=6):
        super(CustomModel, self).__init__()
        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        return self.model(x)


# 初始化模型并加载训练好的权重
model = CustomModel(num_classes=num_classes)
model.load_state_dict(torch.load('train_model_checkpoints/final_model.pth'))  # 修改为最佳模型的路径
model = model.to(device)
model.eval()  # 设置模型为评估模式


# 评估函数
def evaluate_model(model, dataloader):
    running_corrects = 0

    with torch.no_grad():  # 禁用梯度计算
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            # 前向传播
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            # 统计正确的预测数量
            running_corrects += torch.sum(preds == labels.data)

    # 计算准确率
    accuracy = running_corrects.double() / len(dataloader.dataset)
    return accuracy


if __name__ == '__main__':
    # 执行评估
    test_accuracy = evaluate_model(model, test_loader)
    print(f'测试集准确率: {test_accuracy:.4f}')

import torch
import torch.nn as nn
import torch.optim as optim
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
train_transforms = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

val_transforms = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

# 数据集路径
train_dir = 'kaggle/working/dataset/train'
val_dir = 'kaggle/working/dataset/val'

# 加载数据集
train_dataset = datasets.ImageFolder(train_dir, transform=train_transforms)
val_dataset = datasets.ImageFolder(val_dir, transform=val_transforms)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)


# 定义模型
class CustomModel(nn.Module):
    def __init__(self, num_classes=6):
        super(CustomModel, self).__init__()
        # 加载预训练的ResNet18模型
        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        # 修改最后的全连接层
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        return self.model(x)


model = CustomModel(num_classes=num_classes)
model = model.to(device)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 学习率调整策略
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)


# 训练和验证函数
def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
    best_model_wts = None
    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f'Epoch {epoch + 1}/{num_epochs}')
        print('-' * 10)

        # 每个epoch都有训练和验证阶段
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # 设置模型为训练模式
                dataloader = train_loader
            else:
                model.eval()  # 设置模型为评估模式
                dataloader = val_loader

            running_loss = 0.0
            running_corrects = 0

            # 遍历数据
            for inputs, labels in dataloader:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # 前向传播
                # 只在训练阶段记录梯度
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # 反向传播和优化
                    if phase == 'train':
                        optimizer.zero_grad()
                        loss.backward()
                        optimizer.step()

                # 统计
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / len(dataloader.dataset)
            epoch_acc = running_corrects.double() / len(dataloader.dataset)

            print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # 深拷贝模型
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = model.state_dict().copy()
                # 保存最好的模型
                torch.save(best_model_wts, 'model_checkpoints/best_model.pth')

        print()

    print(f'最佳验证精度: {best_acc:.4f}')

    # 加载最佳模型权重
    if best_model_wts is not None:
        model.load_state_dict(best_model_wts)
    return model


if __name__ == '__main__':
    # 创建保存模型的目录
    checkpoint_dir = 'train_model_checkpoints'
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)
    # 设置训练参数并启动训练
    trained_model = train_model(model, criterion, optimizer, scheduler, num_epochs=25)
    # 保存最终模型
    torch.save(trained_model.state_dict(), os.path.join(checkpoint_dir, 'final_model.pth'))
    print('训练完成，模型已保存。')

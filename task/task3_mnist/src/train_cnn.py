import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import os

# 1. 准备数据 (放在 src 里运行，所以是 "./data")
transform = transforms.ToTensor()
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)


# 2. 搭建 CNN 网络
class CNNNet(nn.Module):
    def __init__(self):
        super().__init__()
        # 卷积层 1：输入 1 通道，输出 16 通道，3x3 窗口
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        # 池化层：2x2 窗口
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # 卷积层 2：输入 16，输出 32
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)

        # 全连接层：经过两次池化，图片变成 32通道 x 7 x 7
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # 注意：这里不需要 view 拍平！
        x = self.pool(self.relu(self.conv1(x)))  # -> [64, 16, 14, 14]
        x = self.pool(self.relu(self.conv2(x)))  # -> [64, 32, 7, 7]

        # 提取完特征后，再拍平送给全连接层
        x = x.view(-1, 32 * 7 * 7)  # -> [64, 1568]
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


model = CNNNet()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. 开始训练
print("====== 开始训练 CNN ======")
epochs = 3
loss_list = []
epoch_list = []

for epoch in range(epochs):
    model.train()
    for batch_idx, (images, labels) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        if batch_idx % 300 == 0:
            print(f"进度: {batch_idx * len(images)}/{len(train_data)}, 当前 Loss: {loss.item():.4f}")
            loss_list.append(loss.item())
            epoch_list.append(batch_idx)

# 保存 CNN 的图 (存到外面的 outputs 文件夹，所以是 "../outputs")
plt.plot(epoch_list, loss_list)
plt.title("CNN Training Loss Curve")
plt.xlabel("Batch")
plt.ylabel("Loss")
plt.savefig("../outputs/loss_curve_cnn.png")
print("CNN Loss 曲线已保存到 ../outputs/loss_curve_cnn.png")

# 保存 CNN 模型
torch.save(model.state_dict(), "../outputs/mnist_cnn.pth")
print("CNN 模型已保存到 ../outputs/mnist_cnn.pth")

# 4. 测试
print("====== 开始测试 CNN ======")
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"测试集共 {total} 张图，猜对 {correct} 张。")
print(f"CNN 测试准确率: {100 * correct / total:.2f}%")
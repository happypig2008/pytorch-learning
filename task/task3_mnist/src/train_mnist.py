import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# 1. 准备数据
transform = transforms.ToTensor()
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

# 每次喂给电脑 64 张图（batch）
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# 2. 搭建两层全连接网络
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 256) # 输入 784，中间层 128
        self.relu = nn.ReLU()              # 激活函数
        self.fc2 = nn.Linear(256, 10)      # 输出 10 个分数

    def forward(self, x):
        x = x.view(-1, 28 * 28)            # 把图拉平成一排
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

model = Net()
criterion = nn.CrossEntropyLoss()          # 算误差的方法
optimizer = optim.Adam(model.parameters(), lr=0.001) # 调参数的优化器

# 3. 开始训练 (跑 1 个 epoch 看看)
print("====== 开始训练 ======")
epochs = 3
loss_list = []    # 准备空列表装 Loss
epoch_list = []   # 准备空列表装批次
for epoch in range(epochs):
    model.train() # 告诉网络：现在是学习时间
    for batch_idx, (images, labels) in enumerate(train_loader):
        optimizer.zero_grad()          # 1. 清空旧账
        outputs = model(images)        # 2. 猜答案
        loss = criterion(outputs, labels) # 3. 对答案算误差
        loss.backward()                # 4. 反向找原因
        optimizer.step()               # 5. 调参数

        # 每 300 批打印一次，看看 loss 是不是在变小
        if batch_idx % 300 == 0:
            print(f"进度: {batch_idx * len(images)}/{len(train_data)}, 当前 Loss: {loss.item():.4f}")
            # 把 loss 存起来
            loss_list.append(loss.item())
            epoch_list.append(batch_idx)
# 训练结束后，画图并保存
plt.plot(epoch_list, loss_list)
plt.title("Training Loss Curve")
plt.xlabel("Batch")
plt.ylabel("Loss")
plt.savefig("../outputs/loss_curve.png")
print("Loss 曲线已保存到 outputs/loss_curve.png")
import os
if not os.path.exists("../outputs"):   # 确保文件夹存在
    os.makedirs("../outputs")
torch.save(model.state_dict(), "../outputs/mnist_mlp.pth")
print("模型已保存到 outputs/mnist_mlp.pth")


# 4. 考试时间（测试集跑一遍）
print("====== 开始测试 ======")
model.eval() # 告诉网络：现在是考试时间
correct = 0
total = 0

# 考试不需要算梯度，用 no_grad 加快速度并省内存
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        # 取分数最大的那个作为预测结果
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"测试集共 {total} 张图，猜对 {correct} 张。")
print(f"测试准确率: {100 * correct / total:.2f}%")
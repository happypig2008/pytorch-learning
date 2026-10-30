import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torchvision.transforms import GaussianBlur
import matplotlib.pyplot as plt

# 重新定义你的 CNN 架构（必须和你保存的模型一模一样）
class CNNNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 加载你保存的“学霸大脑”
model = CNNNet()
model.load_state_dict(torch.load("../outputs/mnist_cnn.pth"))
model.eval()

# 【核心：制造近视眼】
# 给图片加上高斯模糊（模糊半径5）
blur_transform = transforms.Compose([
    GaussianBlur(kernel_size=5, sigma=2.0), # 极度模糊
    transforms.ToTensor()
])

# 下载经过模糊处理的测试集
test_data_blur = datasets.MNIST(root="./data", train=False, download=True, transform=blur_transform)
test_loader_blur = DataLoader(test_data_blur, batch_size=64, shuffle=False)

# 展示一张模糊的图看看
images, labels = next(iter(test_loader_blur))
plt.imshow(images[0].squeeze(), cmap="gray")
plt.title(f"Blurred Label: {labels[0]}")
plt.show()

# 开始测试
print("====== 开始测试 模糊视力 ======")
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader_blur:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"模糊测试集准确率: {100 * correct / total:.2f}%")
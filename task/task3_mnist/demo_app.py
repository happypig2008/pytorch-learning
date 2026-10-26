import torch
import torch.nn as nn
import gradio as gr
import torchvision.transforms as transforms
from PIL import Image, ImageOps
import numpy as np


# 1. 完全复制你训练时的 CNN 架构（少一层都加载不了模型）
class CNNNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# 2. 加载你刚才保存的模型
model = CNNNet()
# ⚠️ 注意这里的路径：因为你的 demo_app.py 和 outputs 文件夹平级，所以是 ./outputs/
# 如果报错找不到文件，去左边看看你的 mnist_cnn.pth 到底存在哪
model.load_state_dict(torch.load("./outputs/mnist_cnn.pth", map_location=torch.device('cpu')))
model.eval()


# 3. 核心识别函数
def recognize_digit(image):
    if image is None:
        return "请先画一个数字"

    # 解决 Gradio 新版本的字典格式问题
    if isinstance(image, dict):
        image = image.get("composite")

    if image is None:
        return "请先画一个数字"

    # 转成灰度图
    image = Image.fromarray(image)
    if image.mode != 'L':
        image = image.convert('RGB').convert('L')

    # 缩放到 28x28
    image = image.resize((28, 28))

    # 颜色反转（非常关键）
    image = ImageOps.invert(image)

    # 转 Tensor 并预测
    transform = transforms.ToTensor()
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()

    return f"预测结果: {predicted_class} (置信度: {confidence * 100:.2f}%)"


# 4. 构建网页界面
interface = gr.Interface(
    fn=recognize_digit,
    inputs=gr.Sketchpad(label="在这里用鼠标画一个数字（0-9）", type="numpy"),
    outputs=gr.Textbox(label="AI 识别结果"),
    title="深度视觉农业实验室 - 手写数字识别演示",
    description="这是任务四的拓展 Demo。加载了自己手写的 CNN 模型，支持实时画板识别。"
)

# 5. 启动网页
if __name__ == "__main__":
    interface.launch()
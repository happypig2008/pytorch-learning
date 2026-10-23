## 1. 项目简介
本项目使用 PyTorch 框架，手动搭建了多层感知机（MLP）与卷积神经网络（CNN）两种模型，完成了 MNIST 手写数字集的 0-9 分类任务。
除了基础要求外，本项目还进行了“模型结构对比”以及“高斯模糊（模拟近视）鲁棒性测试”拓展实验。

## 2. 环境依赖
- 操作系统：Windows
- 开发环境：Anaconda + Python 3.10
- 核心依赖库：`torch`、`torchvision`、`matplotlib`

## 3. 数据文件说明
程序会自动下载 MNIST 数据集。
- 训练集：60000 张 28x28 灰度图。
- 测试集：10000 张 28x28 灰度图。
- 存放路径：首次运行代码时，会自动在当前目录下创建 `data/` 文件夹并保存数据。

## 4. 程序运行方式
在 `src` 目录下，通过终端执行以下命令：
- 运行全连接网络（MLP）：`python train_mlp.py`
- 运行卷积神经网络（CNN）：`python train_cnn.py`
- 运行模糊鲁棒性测试：`python test_blur.py`

运行结束后，模型权重与 Loss 曲线图会自动保存至 `../outputs/` 目录下。

## 5. 目录结构
```text
task3_mnist/
├── docs/                # 开发报告与文档
├── outputs/             # 保存的模型(.pth)与Loss曲线图(.png)
├── src/                 # 源代码
│   ├── data/            # 自动下载的 MNIST 数据集
│   ├── train_mlp.py     # 方案一：全连接网络
│   ├── train_cnn.py     # 方案二：CNN网络
│   └── test_blur.py     # 拓展：高斯模糊测试
└── README.md            # 项目说明
```



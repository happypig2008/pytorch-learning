# 任务二：OKTI 图像压缩与解压
## 1. 项目简介
本项目实现了 OKTI（OK Text Image）格式的完整图像编解码工具。
- **解码器（Decoder）**：读取 `.okti` 文本文件，还原为可视化图像。
- **编码器（Encoder）**：读取常见图片（PPM/PNG），将其压缩为紧凑的 OKTI 文本格式。

OKTI 格式利用像素重复（r/R）、历史颜色索引（i/I）、相邻像素差值（d）以及全量 RGB（p）四种规则，实现文本层面的数据压缩。本项目同时实现了编解码闭环，并添加了实用的拓展统计功能。

## 2. 环境与运行方式
- **环境**：Python 3.10, Pillow 库, SimpleGraphics 模块。
- **依赖安装**：`pip install pillow`
- **运行方式**：
    - **编码器运行**：`python src/task2_okti_encoder.py <图片名>`（无需后缀，程序会自动搜索并转码）
    - **解码器运行**：`python src/task2_okti_decoder.py <文件名.okti>`
    - **交互模式**：直接运行程序，根据提示输入文件名。
- **输出文件**：
    - 编码器输出 `src/output.okti`（建议手动移动到 `outputs/` 目录）。
    - 解码器输出 `output.png`。

## 3. 项目结构说明
```text
task2_okti_decoder/
├── docs/                        # 开发文档与日志
│   ├── AI使用日志.md
│   ├── 任务二_开发总结报告.md
│   └── 思考问题总结.md
├── outputs/                     # 生成的图片和中间文件
│   ├── differences_small.png
│   ├── indices.png
│   ├── output.png
│   ├── runs_long_small.png
│   ├── runs_short_small.png
│   └── smallindices_small.png
├── src/                         # 源代码
│   ├── output.okti              # 编码器生成的压缩文件
│   ├── task2_okti_decoder.py    # 解码器（支持p/d/r/R/i/I）
│   ├── task2_okti_encoder.py    # 编码器（支持p/d/r/R/i/I及统计功能）
│   └── test.ppm                 # 测试图片（png转换成ppm模式后的存放处）
├── tests/                       # 测试用例（解码器用）
│   ├── invalid/                 # 异常测试文件（文件不存在、格式错误等）
│   └── valid/                   # 正常测试文件（small.okti, test_r.okti等）
└── README.md                    # 项目说明文档（本文件）
```
## 4. 核心实现思路

### 4.1 解码器逻辑（Decoder）

-  读取文件，校验首行是否为 okti 及尺寸是否合法。
- 依次解析六种像素类型：
-  p：完整 RGB，将 6 位十六进制转为三个十进制。
- d：差值，减去偏置 8，与上一个像素的 RGB 相加。
-  r/R：复制上一个像素，小写 r 占 1 位，大写 R 占 2 位。
-  i/I：从最多 256 个颜色的历史列表里按索引取色。
- 使用 SimpleGraphics 的 putPixel(img, x, y, r, g, b) 绘制，并在循环中处理坐标越界。

### 4.2 编码器逻辑（Encoder）

严格按 PDF 要求的优先级顺序进行编码：

1. run（r/R）：若当前像素与上一个相同，统计连续像素数量（1-15 用 r，16-255 用 R，超过 255 拆分 Rff）。
2. index（i/I）：若颜色在 256 个历史颜色列表中，使用 i 或 I 引用。
3. difference（d）：若 RGB 差值在 -8 到 +7 之间，加偏置 8 后编码。
4. full RGB（p）：不满足以上条件，用 p 存全量。

## 5. 拓展功能与项目亮点

本项目在基础要求之上，添加了以下实用功能：

1. 智能图片搜索与自动格式转换：使用 os 模块自动在多级目录中搜索图片，并内置了 convert_to_ppm 逻辑，解决了 SimpleGraphics 无法读取 PNG 文件的兼容性问题。

2. 运行数据统计（拓展功能）：在编码器中加入计数器，运行时输出各类编码的使用次数（如 编码统计: p=100, d=50, r/R=20），直观了解图片的压缩特征。

3. 压缩率量化计算（拓展功能）：自动计算原始 PPM 图片与压缩后 .okti 文件的大小差异，并输出压缩率百分比（如 缩减量: 35.42%），用数据量化压缩效果。

## 6. 异常处理

程序能够妥善处理以下异常：

-  文件不存在：提示具体文件名，退出程序。
- 格式错误：首行不是 "okti"，或宽高小于等于 0。
- 非法类型：显示第几行出错以及出错的内容，安全退出。
- TclError：捕获 _tkinter.TclError，处理图片损坏或无法打开的情况。
- 无显示器兼容：若 drawImage 弹出失败，自动跳过展示直接编码。


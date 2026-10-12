# 姓名：周倩羽
# 学号：202600293
# 程序说明：任务二 OKTI 编码器

import sys
from SimpleGraphics import *
import _tkinter


def encode_image(image):
    """将图片对象编码为 OKTI 文本字符串（只支持 p 类型）"""
    width, height = image.size
    lines = ["okti", f"{width} {height}"]

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            # 转成十六进制：%02x 表示不足两位补0
            line = "p" + ("%02x" % r) + ("%02x" % g) + ("%02x" % b)
            lines.append(line)

    return "\n".join(lines)


def main():
    args = sys.argv
    if len(args) > 2:
        print("错误：参数过多");
        return
    elif len(args) == 2:
        filename = args[1]
    else:
        filename = input("请输入要压缩的图片名（例如 test.png）：")

    print(f"正在读取图片：{filename}")
    try:
        img = Image.open(filename)
    except Exception as e:
        print(f"错误：无法打开图片，原因：{e}");
        return

    print("正在编码...")
    okti_text = encode_image(img)

    # 按照 PDF 要求，固定输出为 output.okti
    with open("output.okti", "w") as f:
        f.write(okti_text)

    print("编码完成！已保存为 output.okti")
    img.show()


if __name__ == "__main__":
    main()
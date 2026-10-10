# 姓名：周倩羽
# 学号：202600293
# 程序说明：任务二 OKTI 图像解码器，第一阶段只读取文件头并解析尺寸
import os
import sys
from PIL import Image

def read_header(filename):
    """
    读取 OKTI 文件的前两行，检查是否为 OKTI 格式并解析宽高。
    参数 filename: 要读取的文件名
    返回值: 宽和高（整数元组），若出错则返回 None
    """
    try:
        # 使用 with open 自动关闭文件
        with open(filename, "r") as f:
            # 读取第一行并去除末尾换行符
            first_line = f.readline().strip()

            # 检查第一行是否为 okti
            if first_line != "okti":
                print(f"错误：文件 {filename} 不是 OKTI 格式，第一行是：{first_line}")
                return None

            # 读取第二行
            second_line = f.readline().strip()
            if not second_line:
                print("错误：文件缺少尺寸信息（第二行）。")
                return None

            # 拆分第二行，按空格分割
            parts = second_line.split()
            if len(parts) != 2:
                print(f"错误：尺寸信息格式错误，应该有两个数字，实际为：{second_line}")
                return None

            width = int(parts[0])
            height = int(parts[1])

            # 检查宽高合法性
            if width <= 0 or height <= 0:
                print(f"错误：图片尺寸无效，宽={width}, 高={height}，必须大于0。")
                return None

            print(f"成功读取文件头！")
            print(f"格式：OKTI")
            print(f"尺寸：{width} x {height}")

            return width, height

    except FileNotFoundError:
        # 文件不存在报错
        print(f"错误：找不到文件 {filename}，请检查文件路径。")
        return None


def parse_pixel_p(line):
    """
    解析 p 类型像素。
    参数 line: 形如 "pff0000" 的字符串
    返回值: 包含 (红, 绿, 蓝) 的元组
    """
    # line[1:3] 取第2、3个字符，即 "ff"
    # line[3:5] 取第4、5个字符，即 "00"
    # line[5:7] 取第6、7个字符，即 "00"
    r_hex = line[1:3]
    g_hex = line[3:5]
    b_hex = line[5:7]

    # int(字符串, 16) 把十六进制字符串转为十进制整数
    r = int(r_hex, 16)
    g = int(g_hex, 16)
    b = int(b_hex, 16)

    return r, g, b
def parse_pixel_d(line, prev_r, prev_g, prev_b):
    """
    解析 d 类型像素（差值）。
    """
    r_hex = line[1:2]
    g_hex = line[2:3]
    b_hex = line[3:4]

    r_diff = int(r_hex, 16) - 8
    g_diff = int(g_hex, 16) - 8
    b_diff = int(b_hex, 16) - 8

    current_r = prev_r + r_diff
    current_g = prev_g + g_diff
    current_b = prev_b + b_diff

    return current_r, current_g, current_b

def parse_pixel_r(line):
    """
    解析 r 或 R 类型像素。
    参数 line: 形如 "r2" 或 "R20" 的字符串
    返回值: 需要额外复制的次数（整数）
    """
    if line[0] == "r":
        # 小写 r，后面只有 1 位十六进制数字
        count = int(line[1:2], 16)
    else:
        # 大写 R，后面有 2 位十六进制数字
        count = int(line[1:3], 16)

    return count

def parse_pixel_i(line, colors):
    """
    解析 i 或 I 类型像素。
    """
    if line[0] == "i":
        index = int(line[1:2], 16)
    else:
        index = int(line[1:3], 16)
    return colors[index]


def main():
    """主函数，测试读取"""
    filename = "../tests/valid/test_r. okti"
    print(f"尝试读取文件：{filename}")

    result = read_header(filename)

    if result is not None:
        w, h = result
        # 创建一个 w 宽 h 高的黑色画布
        img = Image.new("RGB", (w, h), (0, 0, 0))
        print(f"接下来应该解析 {w * h} 个像素的数据。")
        print("第一阶段测试通过！")
    else:
        print("第一阶段测试失败。")


if __name__ == "__main__":
    def main():
        # 获取命令行参数
        args = sys.argv

        user_input = ""  # 先定义一个空变量，用来接用户输入

        if len(args) > 2:
            print("错误：参数过多，请只提供一个文件名。")
            return
        elif len(args) == 2:
            user_input = args[1]  # 从命令行参数获取文件名
        else:
            # 没有参数，用 input 提示输入
            user_input = input("请输入要打开的 OKTI 文件名（例如 small.okti）：")

        # 自动补全路径
        # 判断用户输入的内容里，有没有斜杠或者反斜杠
        if os.sep not in user_input and "/" not in user_input:
            # 1. 先尝试去 valid 找
            filename = os.path.join("..", "tests", "valid", user_input)
            if not os.path.exists(filename):
                # 2. 没找到，去 invalid 找
                filename = os.path.join("..", "tests", "invalid", user_input)
                if not os.path.exists(filename):
                    # 3. 还没找到，干脆按用户输入的名字，在当前目录找找看
                    filename = user_input
        else:
            # 用户带了路径，直接按用户的路径读
            filename = user_input

        print(f"尝试读取文件：{filename}")

        # 先读文件头，获取宽高
        result = read_header(filename)

        if result is not None:
            w, h = result
            img = Image.new("RGB", (w, h), (0, 0, 0))
            total_pixels = w * h
            print(f"预计需要解析 {total_pixels} 个像素。")

            # 重新打开文件，跳过前两行（okti和尺寸行），开始读取像素
            with open(filename, "r") as f:
                # 跳过第一行和第二行
                f.readline()
                f.readline()

                pixel_count = 0
                prev_r, prev_g, prev_b = 0, 0, 0
                colors = [(0, 0, 0)]  # 历史颜色列表，初始为黑色

                # 循环读取每一行像素数据

                line_num = 2

                for line in f:
                    line_num += 1  # 记录当前是第几行
                    line = line.strip()  # 去掉换行符
                    if not line:  # 如果是空行，跳过
                        continue

                    # 判断这一行的第一个字符是什么
                    pixel_type = line[0]

                    if pixel_type == "p":
                        # 调用刚才写的 parse_pixel_p 解析颜色
                        r, g, b = parse_pixel_p(line)
                        # 计算当前像素在画布上的坐标 (x, y)
                        x = pixel_count % w
                        y = pixel_count // w
                        # 把颜色画上去
                        img.putpixel((x, y), (r, g, b))
                        pixel_count += 1
                        print(f"像素 {pixel_count}: R={r}, G={g}, B={b}")



                    elif pixel_type == "d":

                        # 调用刚刚写的 parse_pixel_d  <-- 注释也要缩进！

                        r, g, b = parse_pixel_d(line, prev_r, prev_g, prev_b)
                        # 计算当前像素在画布上的坐标 (x, y)
                        x = pixel_count % w
                        y = pixel_count // w
                        # 把颜色画上去
                        img.putpixel((x, y), (r, g, b))

                        pixel_count += 1

                        print(f"像素 {pixel_count}: R={r}, G={g}, B={b}")



                    elif pixel_type in ["r", "R"]:
                        # 1. 调用刚才写的函数，获取“额外复制”的次数
                        count = parse_pixel_r(line)

                        # 2. 循环复制上一个像素
                        for _ in range(count):
                            # 计算当前像素在画布上的坐标 (x, y)
                            x = pixel_count % w
                            y = pixel_count // w
                            # 把颜色画上去
                            img.putpixel((x, y), (r, g, b))
                            pixel_count += 1
                            # 注意：这里打印用的是 prev_r，因为颜色没有变
                            print(f"像素 {pixel_count}: R={prev_r}, G={prev_g}, B={prev_b}")


                        r, g, b = prev_r, prev_g, prev_b


                    elif pixel_type in ["i", "I"]:
                        r, g, b = parse_pixel_i(line, colors)
                        x = pixel_count % w
                        y = pixel_count // w
                        img.putpixel((x, y), (r, g, b))
                        pixel_count += 1
                        print(f"像素 {pixel_count}: R={r}, G={g}, B={b}")



                    else:

                        # 遇到非法像素类型，显示行号和行内容

                        print(f"错误：第 {line_num} 行包含未知的像素类型 '{pixel_type}'")

                        print(f"出错的内容：{line}")

                        # 关闭图像窗口并退出程序

                        img.close()  # 释放图片内存

                        sys.exit()  # 退出程序

                    prev_r, prev_g, prev_b = r, g, b
                    # 更新历史颜色列表
                    if (r, g, b) not in colors:
                        colors.insert(0, (r, g, b))
                        if len(colors) > 256:
                            colors.pop()
                img.save("output.png")  # 把图片保存到文件
                img.show()  # 弹出一个窗口显示图片

                print(f"解析完毕，共处理 {pixel_count} 个像素。")


    if __name__ == "__main__":
        main()
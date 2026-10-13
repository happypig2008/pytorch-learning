# 姓名：周倩羽
# 学号：202600293
# 程序说明：任务二 OKTI 图像编码器

import os
import sys
import _tkinter
from PIL import Image
from SimpleGraphics import loadImage, drawImage


def find_image_file(name):
    """在项目文件夹中搜索图片文件。
    参数:
        name: 用户输入的图片名字，比如 "test"
    返回:
        找到的真实文件路径（如 "test.ppm" 或 "../outputs/test.png"），找不到返回 None
    """
    # 常见图片扩展名
    extensions = [".ppm", ".png"]

    # 搜索范围：当前目录、上一级目录、outputs 目录
    search_dirs = [".", "..", "../outputs", "outputs"]

    for ext in extensions:
        for directory in search_dirs:
            # 拼接路径，比如 ".." + "/test" + ".png" = "../test.png"
            potential_path = os.path.join(directory, name + ext)
            if os.path.exists(potential_path):
                return potential_path
    return None


def ensure_ppm_format(filepath):
    """确保图片是 PPM 格式。如果是 PNG，则自动转换。
    参数:
        filepath: 图片文件的路径
    返回:
        PPM 格式文件的路径
    """
    if filepath.lower().endswith(".png"):
        print(f"检测到 PNG 格式，正在自动转换为 PPM...")
        try:
            img = Image.open(filepath)
            img = img.convert('RGB')  #强制丢失透明度
            # 转换并保存到当前 src 目录下，名字叫 test.ppm
            ppm_path = "test.ppm"
            img.save(ppm_path)
            img.close()
            print(f"转换成功！已生成 {ppm_path}")
            return ppm_path
        except Exception as e:
            print(f"转换失败：{e}")
            return None
    else:
        print("图片已经是 PPM 格式，无需转换。")
        return filepath


def count_run(image, x, y, width, height, target_color):
    """从 (x, y) 开始，向右数连续有多少个像素等于 target_color（支持跨行）。
    参数:
        image: 图片对象
        x, y: 起始坐标
        width, height: 图片宽高
        target_color: 要比较的颜色 (r, g, b)
    返回:
        连续相同像素的个数（包含起点）
    """
    count = 0
    while y < height:
        current = image.get(x, y)
        if current == target_color:
            count += 1
            x += 1
            if x >= width:
                x = 0
                y += 1
        else:
            return count
    return count


def advance_position(x, y, n, width):
    """把坐标向前移动 n 个像素，处理跨行。
    参数:
        x, y: 当前坐标
        n: 要前进的步数
        width: 图片宽度
    返回:
        新的 (x, y)
    """
    x += n
    while x >= width:
        x -= width
        y += 1
    return x, y


def encode_image(image, filename):
    """把图片按 OKTI 格式写入文件，支持 p, d, r, R 编码。
    参数:
        image: 图片对象
        filename: 输出文件名，例如 output.okti
    返回:
        无
    """
    width = image.width()
    height = image.height()

    previous_color = (0, 0, 0)  # 初始化为黑色
    x = 0
    y = 0

    with open(filename, "w", newline="\n") as out:
        out.write("okti\n")
        out.write("%d %d\n" % (width, height))

        while y < height:
            current_color = image.get(x, y)

            # 1. 优先判断能不能用 run (r 或 R)
            if current_color == previous_color:
                # 数一数后面有多少个连续相同的像素
                run_length = count_run(image, x, y, width, height, current_color)

                # run_length 包含了当前这个像素，所以额外副本数是 run_length - 1
                extra_copies = run_length - 1

                # 处理超长 run，分次编码（每次最多 255 个）
                while extra_copies > 0:
                    if extra_copies <= 15:
                        out.write("r%x\n" % extra_copies)
                        extra_copies = 0
                    elif extra_copies <= 255:
                        out.write("R%02x\n" % extra_copies)
                        extra_copies = 0
                    else:
                        out.write("Rff\n")
                        extra_copies -= 255

                # 跳过这些像素，更新坐标
                x, y = advance_position(x, y, run_length, width)

            else:
                # 2. 判断能不能用 d (差值)
                dr = current_color[0] - previous_color[0]
                dg = current_color[1] - previous_color[1]
                db = current_color[2] - previous_color[2]

                # 差值必须在 -8 到 7 之间
                if -8 <= dr <= 7 and -8 <= dg <= 7 and -8 <= db <= 7:
                    # 差值加上 8 的偏置，转成十六进制
                    out.write("d%x%x%x\n" % (dr + 8, dg + 8, db + 8))
                else:
                    # 3. 只能用 p (完整RGB)
                    out.write("p%02x%02x%02x\n" % (current_color[0], current_color[1], current_color[2]))

                # 使用了 d 或 p，一个像素处理完毕
                previous_color = current_color  # 更新前一个颜色

                # 前进一个像素
                x += 1
                if x >= width:
                    x = 0
                    y += 1


def main():
    """主程序：自动找图 -> 转换格式 -> 编码"""
    if len(sys.argv) > 2:
        print("错误：提供了太多命令行参数。")
        return

    # 1. 获取输入名字
    if len(sys.argv) == 2:
        input_name = sys.argv[1]
    else:
        input_name = input("请输入图片名字（不需要带后缀，比如 test）：")

    # 2. 自动寻找文件
    print(f"正在搜索图片：{input_name}...")
    found_path = find_image_file(input_name)

    if found_path is None:
        print(f"错误：找不到图片 '{input_name}'，请检查它是否在当前目录、上一级或 outputs 目录下。")
        return

    print(f"成功找到文件：{found_path}")

    # 3. 格式判断和转换
    final_ppm_path = ensure_ppm_format(found_path)
    if final_ppm_path is None:
        return

    # 4. 用 SimpleGraphics 打开并编码
    print("正在加载 PPM 图片并编码...")
    try:
        image = loadImage(final_ppm_path)
        try:
            drawImage(image, 0, 0)
        except Exception:
            print("提示：当前环境无显示器，跳过图片展示，直接开始编码。")
        encode_image(image, "output.okti")
        print("编码完成！已保存为 output.okti")
    except _tkinter.TclError:
        print("错误：无法打开文件，可能是格式错误或文件损坏。")
    except Exception as e:
        print(f"发生未知错误：{e}")


if __name__ == "__main__":
    main()



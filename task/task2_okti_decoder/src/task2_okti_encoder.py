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


def encode_image(image, filename):
    """把图片按 OKTI 格式写入文件，只使用 p 编码。
    参数:
        image: loadImage 返回的图片对象（Tkinter PhotoImage）
        filename: 输出文件名，例如 output.okti
    返回:
        无
    """
    width = image.width()
    height = image.height()

    out = open(filename, "w", newline="\n")
    out.write("okti\n")
    out.write("%d %d\n" % (width, height))

    y = 0
    while y < height:
        x = 0
        while x < width:
            # 直接解包出 r, g, b，它已经是 0-255 的整数了
            r, g, b = image.get(x, y)

            # 直接格式化写入 p 编码
            out.write("p%02x%02x%02x\n" % (r, g, b))
            x += 1
        y += 1

    out.close()

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
        drawImage(image,0,0)
        encode_image(image, "output.okti")
        print("编码完成！已保存为 output.okti")
    except _tkinter.TclError:
        print("错误：无法打开文件，可能是格式错误或文件损坏。")
    except Exception as e:
        print(f"发生未知错误：{e}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
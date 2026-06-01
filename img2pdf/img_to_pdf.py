import os
import shutil
import img2pdf
from PIL import Image

PAPER_SIZES = {
    '1': ('原尺寸', None),
    '2': ('A4', (210, 297)),
    '3': ('B5', (176, 250)),
    '4': ('Letter', (215.9, 279.4)),
    '5': ('Legal', (215.9, 355.6)),
}

def get_image_files(folder_path):
    """遍历文件夹，获取所有图片文件"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    image_files = []

    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(image_extensions):
                image_files.append(entry)

    return image_files

def sort_by_creation_time(image_files):
    """根据文件创建时间排序"""
    return sorted(image_files, key=lambda x: x.stat().st_ctime)

def compress_image(input_path, output_path, quality=85):
    """压缩图片并保持格式"""
    try:
        with Image.open(input_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(output_path, quality=quality, optimize=True)
        return True
    except Exception as e:
        print(f"压缩图片失败 {input_path}: {e}")
        return False

def images_to_pdf(image_paths, output_pdf, paper_size=None):
    """将图片列表转换为PDF"""
    if paper_size is None:
        with open(output_pdf, 'wb') as f:
            f.write(img2pdf.convert(image_paths))
    else:
        size_pt = (img2pdf.mm_to_pt(paper_size[0]), img2pdf.mm_to_pt(paper_size[1]))
        layout_fun = img2pdf.get_layout_fun(size_pt)
        with open(output_pdf, 'wb') as f:
            f.write(img2pdf.convert(image_paths, layout_fun=layout_fun))

def select_paper_size():
    """让用户选择纸张尺寸"""
    print("\n请选择PDF纸张尺寸:")
    for key, (name, _) in PAPER_SIZES.items():
        print(f"  {key}. {name}")
    while True:
        choice = input("请输入选项数字：").strip()
        if choice in PAPER_SIZES:
            return PAPER_SIZES[choice][1]
        print("无效选择，请重新输入")

def main():
    source_folder = input("请输入存放图片的文件夹路径:").strip()
    if not source_folder:
        source_folder = ''

    if not os.path.exists(source_folder):
        print(f"文件夹不存在")
        return

    output_folder = 'temp_imgs'
    os.makedirs(output_folder, exist_ok=True)

    print("正在扫描图片文件...")
    image_files = get_image_files(source_folder)

    if not image_files:
        print("未找到任何图片文件")
        return

    print("按创建时间排序...")
    sorted_files = sort_by_creation_time(image_files)

    compressed_paths = []
    print("正在压缩图片...")
    for entry in sorted_files:
        output_path = os.path.join(output_folder, entry.name)
        if compress_image(entry.path, output_path):
            compressed_paths.append(output_path)

    if not compressed_paths:
        print("压缩失败,无法生成PDF")
        return

    paper_size = select_paper_size()

    output_pdf_name = input("\n请输入输出PDF文件名(不包含扩展名):").strip()
    if not output_pdf_name:
        output_pdf_name = 'output'
    output_pdf = f"{output_pdf_name}.pdf"

    print("正在生成PDF...")
    images_to_pdf(compressed_paths, output_pdf, paper_size)
    print(f"PDF生成成功: {output_pdf}")
    print(f'PDF大小为:{os.path.getsize(output_pdf)}字节')

    print("正在清理临时文件...")
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
        print('已删除临时文件夹')
    
    print("所有操作完成！！！")

if __name__ == '__main__':
    main()
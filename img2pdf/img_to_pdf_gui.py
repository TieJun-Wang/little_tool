import os
import shutil
import img2pdf
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from threading import Thread
import ctypes

PAPER_SIZES = {
    '原尺寸': None,
    'A4': (210, 297),
    'B5': (176, 250),
    'Letter': (215.9, 279.4),
    'Legal': (215.9, 355.6),
}

def setup_high_dpi():
    """设置高DPI支持"""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

def format_file_size(bytes_size):
    """格式化文件大小"""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.2f} MB"

class ImageToPdfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片转PDF工具")
        
        self.setup_dpi_scaling()
        self.root.geometry("600x500")
        
        self.source_folder = tk.StringVar()
        self.output_pdf = tk.StringVar()
        self.paper_size = tk.StringVar(value='A4')
        self.progress = tk.StringVar(value='准备就绪')
        self.stats_info = tk.StringVar(value='')
        self.progress_bar = None
        
        self.create_widgets()
    
    def setup_dpi_scaling(self):
        try:
            dpi = self.root.winfo_fpixels('1i')
            scale = dpi / 96.0
            self.root.tk.call('tk', 'scaling', scale)
        except Exception:
            pass
    
    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Microsoft YaHei', 12))
        style.configure('TButton', font=('Microsoft YaHei', 12))
        style.configure('TEntry', font=('Microsoft YaHei', 12))
        style.configure('TCombobox', font=('Microsoft YaHei', 12))
        
        # 图片文件夹选择
        frame1 = ttk.Frame(self.root, padding="15")
        frame1.pack(fill=tk.X, padx=15, pady=6)
        ttk.Label(frame1, text="图片文件夹:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame1, textvariable=self.source_folder, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame1, text="浏览", command=self.browse_source, width=10).pack(side=tk.LEFT, padx=5)
        
        # 输出PDF选择
        frame2 = ttk.Frame(self.root, padding="15")
        frame2.pack(fill=tk.X, padx=15, pady=6)
        ttk.Label(frame2, text="输出PDF:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame2, textvariable=self.output_pdf, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame2, text="浏览", command=self.browse_output, width=10).pack(side=tk.LEFT, padx=5)
        
        # 纸张尺寸选择
        frame3 = ttk.Frame(self.root, padding="15")
        frame3.pack(fill=tk.X, padx=15, pady=6)
        ttk.Label(frame3, text="纸张尺寸:").pack(side=tk.LEFT, padx=5)
        combo = ttk.Combobox(frame3, textvariable=self.paper_size, values=list(PAPER_SIZES.keys()), width=12)
        combo.pack(side=tk.LEFT, padx=5)
        
        # 进度显示
        frame4 = ttk.Frame(self.root, padding="15")
        frame4.pack(fill=tk.X, padx=15, pady=6)
        ttk.Label(frame4, textvariable=self.progress).pack(side=tk.LEFT, padx=5)
        self.progress_bar = ttk.Progressbar(frame4, orient=tk.HORIZONTAL, length=350, mode='indeterminate')
        self.progress_bar.pack(side=tk.RIGHT, padx=5)
        
        # 统计信息显示
        frame5 = ttk.Frame(self.root, padding="15")
        frame5.pack(fill=tk.X, padx=15, pady=6)
        ttk.Label(frame5, text="统计信息:").pack(side=tk.LEFT, padx=5)
        ttk.Label(frame5, textvariable=self.stats_info, foreground='#0066CC').pack(side=tk.LEFT, padx=5)
        
        # 开始按钮
        frame6 = ttk.Frame(self.root, padding="15")
        frame6.pack(fill=tk.X, padx=15, pady=15)
        ttk.Button(frame6, text="开始转换", command=self.start_conversion, width=25).pack()
    
    def browse_source(self):
        folder = filedialog.askdirectory(title="选择图片文件夹")
        if folder:
            self.source_folder.set(folder)
    
    def browse_output(self):
        file = filedialog.asksaveasfilename(title="保存PDF文件", defaultextension=".pdf", filetypes=[("PDF文件", "*.pdf")])
        if file:
            self.output_pdf.set(file)
    
    def get_image_files(self, folder_path):
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        image_files = []
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.lower().endswith(image_extensions):
                    image_files.append(entry)
        return image_files
    
    def sort_by_creation_time(self, image_files):
        return sorted(image_files, key=lambda x: x.stat().st_ctime)
    
    def compress_image(self, input_path, output_path, quality=85):
        try:
            with Image.open(input_path) as img:
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(output_path, quality=quality, optimize=True)
            return True
        except Exception as e:
            print(f"压缩失败 {input_path}: {e}")
            return False
    
    def images_to_pdf(self, image_paths, output_pdf, paper_size):
        if paper_size is None:
            with open(output_pdf, 'wb') as f:
                f.write(img2pdf.convert(image_paths))
        else:
            size_pt = (img2pdf.mm_to_pt(paper_size[0]), img2pdf.mm_to_pt(paper_size[1]))
            layout_fun = img2pdf.get_layout_fun(size_pt)
            with open(output_pdf, 'wb') as f:
                f.write(img2pdf.convert(image_paths, layout_fun=layout_fun))
    
    def convert(self):
        start_time = time.time()
        source_folder = self.source_folder.get()
        output_pdf = self.output_pdf.get()
        
        if not source_folder:
            messagebox.showerror("错误", "请选择图片文件夹")
            return
        
        if not output_pdf:
            messagebox.showerror("错误", "请选择输出PDF路径")
            return
        
        if not os.path.exists(source_folder):
            messagebox.showerror("错误", "图片文件夹不存在")
            return
        
        self.progress.set("正在扫描图片...")
        image_files = self.get_image_files(source_folder)
        
        if not image_files:
            messagebox.showinfo("提示", "未找到图片文件")
            self.progress.set("准备就绪")
            return
        
        self.progress.set("按创建时间排序...")
        sorted_files = self.sort_by_creation_time(image_files)
        total_images = len(sorted_files)
        
        output_folder = 'temp_imgs'
        os.makedirs(output_folder, exist_ok=True)
        
        self.progress.set("正在压缩图片...")
        compressed_paths = []
        for entry in sorted_files:
            output_path = os.path.join(output_folder, entry.name)
            if self.compress_image(entry.path, output_path):
                compressed_paths.append(output_path)
        
        if not compressed_paths:
            messagebox.showerror("错误", "压缩失败")
            self.progress.set("准备就绪")
            return
        
        self.progress.set("正在生成PDF...")
        paper_size = PAPER_SIZES[self.paper_size.get()]
        self.images_to_pdf(compressed_paths, output_pdf, paper_size)
        
        self.progress.set("正在清理临时文件...")
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        
        # 计算用时和文件大小
        end_time = time.time()
        total_time = end_time - start_time
        pdf_size = os.path.getsize(output_pdf)
        pdf_dir = os.path.dirname(output_pdf)
        pdf_name = os.path.basename(output_pdf)
        
        # 格式化显示
        time_str = f"{total_time:.2f} 秒"
        size_str = format_file_size(pdf_size)
        
        # 更新统计信息
        self.stats_info.set(f"处理图片: {total_images} 张 | 用时: {time_str} | 大小: {size_str}")
        
        # 显示详细信息
        message = f"PDF生成成功!\n\n"
        message += f"文件名: {pdf_name}\n"
        message += f"保存位置: {pdf_dir}\n"
        message += f"文件大小: {size_str}\n"
        message += f"处理图片: {total_images} 张\n"
        message += f"总用时: {time_str}"
        
        self.progress.set("完成")
        messagebox.showinfo("成功", message)
        self.progress_bar.stop()
        self.progress.set("准备就绪")
    
    def start_conversion(self):
        self.stats_info.set('')
        self.progress_bar.start()
        Thread(target=self.convert).start()

if __name__ == '__main__':
    setup_high_dpi()
    root = tk.Tk()
    app = ImageToPdfApp(root)
    root.mainloop()
"""
Morandi Color Palette Image Processing App
莫兰迪色系图片处理应用 - 无边框圆角设计
"""

import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance, ImageOps, ImageSequence
import os
import sys
from tkinter import filedialog
import ctypes

# 设置外观模式
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ========== 莫兰迪色系 ==========
class MorandiColors:
    """莫兰迪色系配色"""
    # 主色调 - 灰粉色系
    ROSE_GRAY = "#C4B7A6"      # 玫瑰灰
    DUSTY_PINK = "#D4C4BC"     # 脏粉色
    SAGE_GREEN = "#A8B5A2"     # 鼠尾草绿
    DUSTY_BLUE = "#9AACB8"     # 灰蓝色
    WARM_GRAY = "#B8AFA9"      # 暖灰色
    LAVENDER = "#C5B9CD"       # 薰衣草紫
    CREAM = "#E8E4DF"          # 奶油色
    TAUPE = "#A69B8D"          # 灰褐色
    
    # 背景色
    BG_LIGHT = "#F5F3F0"       # 浅米色背景
    BG_CARD = "#FDFCFB"        # 卡片背景
    
    # 文字色
    TEXT_PRIMARY = "#5D5449"   # 主要文字
    TEXT_SECONDARY = "#8B8178" # 次要文字
    TEXT_MUTED = "#A9A29A"     # 淡化文字
    
    # 强调色
    ACCENT = "#B5A397"         # 强调色
    ACCENT_HOVER = "#A69285"   # 悬停色


class AnimatedGIF:
    """处理GIF动画的类"""
    def __init__(self, label, gif_path, size=(60, 60)):
        self.label = label
        self.size = size
        self.frames = []
        self.durations = []
        self.current_frame = 0
        self.is_playing = True
        
        try:
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                pil_frame = frame.copy().convert("RGBA")
                pil_frame = pil_frame.resize(size, Image.Resampling.LANCZOS)
                ctk_image = ctk.CTkImage(light_image=pil_frame, dark_image=pil_frame, size=size)
                self.frames.append(ctk_image)
                duration = gif.info.get('duration', 100)
                self.durations.append(duration if duration > 0 else 100)
        except Exception as e:
            print(f"加载GIF失败: {e}")
            self.frames = []
    
    def animate(self):
        if self.frames and self.is_playing:
            self.label.configure(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            duration = self.durations[self.current_frame] if self.durations else 100
            self.label.after(duration, self.animate)
    
    def start(self):
        if self.frames:
            self.is_playing = True
            self.animate()
    
    def stop(self):
        self.is_playing = False


class MorandiImageApp(ctk.CTk):
    """莫兰迪色系图片处理应用"""
    
    def __init__(self):
        super().__init__()
        
        # 路径设置
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.gif_path = os.path.join(self.script_dir, "d0c438b0de1b4f779ced045eeac32c175127bf0a6930-YP8Y17_fw1200.gif")
        
        # 图片相关
        self.current_image = None
        self.original_image = None
        self.image_path = None
        
        # 窗口配置
        self.title("Morandi Image Studio")
        self.geometry("1100x750")
        self.configure(fg_color=MorandiColors.BG_LIGHT)
        
        # 无边框设置
        self.overrideredirect(True)
        
        # 设置窗口圆角（Windows 11）
        self.setup_rounded_corners()
        
        # 居中显示
        self.center_window()
        
        # 拖动数据
        self.drag_data = {"x": 0, "y": 0}
        
        # 创建UI
        self.create_main_container()
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        
        # 绑定事件
        self.bind_events()
    
    def setup_rounded_corners(self):
        """设置窗口圆角 (Windows 11)"""
        try:
            # Windows 11 圆角支持
            from ctypes import windll, byref, sizeof, c_int
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWM_WINDOW_CORNER_PREFERENCE_ROUND = 2
            windll.dwmapi.DwmSetWindowAttribute(
                windll.user32.GetParent(self.winfo_id()),
                DWMWA_WINDOW_CORNER_PREFERENCE,
                byref(c_int(DWM_WINDOW_CORNER_PREFERENCE_ROUND)),
                sizeof(c_int)
            )
        except:
            pass
    
    def center_window(self):
        """居中显示窗口"""
        self.update_idletasks()
        width = 1100
        height = 750
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_main_container(self):
        """创建主容器 - 无边框圆角"""
        self.main_container = ctk.CTkFrame(
            self,
            corner_radius=28,
            fg_color=MorandiColors.BG_CARD,
            border_width=0
        )
        self.main_container.pack(fill="both", expand=True)
    
    def create_header(self):
        """创建顶部标题栏"""
        self.header = ctk.CTkFrame(
            self.main_container,
            height=70,
            corner_radius=0,
            fg_color="transparent"
        )
        self.header.pack(fill="x", padx=25, pady=(20, 0))
        self.header.pack_propagate(False)
        
        # 左侧 - GIF动画
        self.gif_label = ctk.CTkLabel(
            self.header,
            text="",
            width=60,
            height=60
        )
        self.gif_label.place(x=0, y=5)
        
        if os.path.exists(self.gif_path):
            self.animated_gif = AnimatedGIF(self.gif_label, self.gif_path, size=(55, 55))
            self.animated_gif.start()
        else:
            self.gif_label.configure(text="🎨", font=ctk.CTkFont(size=35))
        
        # 标题
        self.title_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.title_frame.place(x=70, y=8)
        
        self.app_title = ctk.CTkLabel(
            self.title_frame,
            text="Morandi Image Studio",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=MorandiColors.TEXT_PRIMARY
        )
        self.app_title.pack(anchor="w")
        
        self.app_subtitle = ctk.CTkLabel(
            self.title_frame,
            text="莫兰迪色系 · 优雅图片处理",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=MorandiColors.TEXT_SECONDARY
        )
        self.app_subtitle.pack(anchor="w")
        
        # 控制按钮
        self.controls_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.controls_frame.place(relx=1.0, x=-10, y=15, anchor="ne")
        
        self.min_btn = ctk.CTkButton(
            self.controls_frame,
            text="─",
            width=38,
            height=38,
            corner_radius=19,
            fg_color=MorandiColors.CREAM,
            hover_color=MorandiColors.WARM_GRAY,
            text_color=MorandiColors.TEXT_SECONDARY,
            font=ctk.CTkFont(size=14, weight="bold"),
            border_width=0,
            command=self.iconify
        )
        self.min_btn.pack(side="left", padx=5)
        
        self.close_btn = ctk.CTkButton(
            self.controls_frame,
            text="×",
            width=38,
            height=38,
            corner_radius=19,
            fg_color=MorandiColors.DUSTY_PINK,
            hover_color=MorandiColors.ROSE_GRAY,
            text_color=MorandiColors.TEXT_PRIMARY,
            font=ctk.CTkFont(size=18, weight="bold"),
            border_width=0,
            command=self.close_window
        )
        self.close_btn.pack(side="left", padx=5)
    
    def create_sidebar(self):
        """创建左侧工具栏"""
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=280,
            corner_radius=20,
            fg_color=MorandiColors.BG_LIGHT,
            border_width=0
        )
        self.sidebar.pack(side="left", fill="y", padx=(25, 15), pady=20)
        self.sidebar.pack_propagate(False)
        
        # 工具标题
        tools_title = ctk.CTkLabel(
            self.sidebar,
            text="🛠️ 图片工具",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=MorandiColors.TEXT_PRIMARY
        )
        tools_title.pack(pady=(25, 20), padx=20, anchor="w")
        
        # 文件操作区
        self.create_file_section()
        
        # 分隔线
        separator1 = ctk.CTkFrame(self.sidebar, height=1, fg_color=MorandiColors.CREAM)
        separator1.pack(fill="x", padx=20, pady=15)
        
        # 滤镜效果区
        self.create_filter_section()
        
        # 分隔线
        separator2 = ctk.CTkFrame(self.sidebar, height=1, fg_color=MorandiColors.CREAM)
        separator2.pack(fill="x", padx=20, pady=15)
        
        # 调整工具区
        self.create_adjustment_section()
    
    def create_file_section(self):
        """创建文件操作区"""
        file_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        file_frame.pack(fill="x", padx=20)
        
        # 打开图片
        self.open_btn = ctk.CTkButton(
            file_frame,
            text="📂 打开图片",
            height=42,
            corner_radius=21,
            fg_color=MorandiColors.SAGE_GREEN,
            hover_color="#96A68F",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            border_width=0,
            command=self.open_image
        )
        self.open_btn.pack(fill="x", pady=5)
        
        # 保存图片
        self.save_btn = ctk.CTkButton(
            file_frame,
            text="💾 保存图片",
            height=42,
            corner_radius=21,
            fg_color=MorandiColors.DUSTY_BLUE,
            hover_color="#8A9CAA",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            border_width=0,
            command=self.save_image
        )
        self.save_btn.pack(fill="x", pady=5)
    
    def create_filter_section(self):
        """创建滤镜效果区"""
        filter_label = ctk.CTkLabel(
            self.sidebar,
            text="✨ 莫兰迪滤镜",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=MorandiColors.TEXT_PRIMARY
        )
        filter_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        filter_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20)
        
        # 滤镜按钮
        filters = [
            ("🌸 玫瑰灰调", self.apply_rose_filter, MorandiColors.DUSTY_PINK),
            ("🌿 鼠尾草绿", self.apply_sage_filter, MorandiColors.SAGE_GREEN),
            ("💜 薰衣草紫", self.apply_lavender_filter, MorandiColors.LAVENDER),
            ("☁️ 雾霾蓝", self.apply_dusty_blue_filter, MorandiColors.DUSTY_BLUE),
        ]
        
        for text, command, color in filters:
            btn = ctk.CTkButton(
                filter_frame,
                text=text,
                height=38,
                corner_radius=19,
                fg_color=color,
                hover_color=MorandiColors.TAUPE,
                text_color="#ffffff",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                border_width=0,
                command=command
            )
            btn.pack(fill="x", pady=4)
    
    def create_adjustment_section(self):
        """创建调整工具区"""
        adjust_label = ctk.CTkLabel(
            self.sidebar,
            text="🎚️ 图片调整",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=MorandiColors.TEXT_PRIMARY
        )
        adjust_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        adjust_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        adjust_frame.pack(fill="x", padx=20)
        
        # 亮度滑块
        brightness_label = ctk.CTkLabel(
            adjust_frame,
            text="亮度",
            font=ctk.CTkFont(size=12),
            text_color=MorandiColors.TEXT_SECONDARY
        )
        brightness_label.pack(anchor="w", pady=(5, 2))
        
        self.brightness_slider = ctk.CTkSlider(
            adjust_frame,
            from_=0.5,
            to=1.5,
            number_of_steps=100,
            progress_color=MorandiColors.ROSE_GRAY,
            button_color=MorandiColors.TAUPE,
            button_hover_color=MorandiColors.ACCENT_HOVER,
            command=self.adjust_brightness
        )
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack(fill="x", pady=(0, 10))
        
        # 对比度滑块
        contrast_label = ctk.CTkLabel(
            adjust_frame,
            text="对比度",
            font=ctk.CTkFont(size=12),
            text_color=MorandiColors.TEXT_SECONDARY
        )
        contrast_label.pack(anchor="w", pady=(5, 2))
        
        self.contrast_slider = ctk.CTkSlider(
            adjust_frame,
            from_=0.5,
            to=1.5,
            number_of_steps=100,
            progress_color=MorandiColors.SAGE_GREEN,
            button_color=MorandiColors.TAUPE,
            button_hover_color=MorandiColors.ACCENT_HOVER,
            command=self.adjust_contrast
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill="x", pady=(0, 10))
        
        # 饱和度滑块
        saturation_label = ctk.CTkLabel(
            adjust_frame,
            text="饱和度",
            font=ctk.CTkFont(size=12),
            text_color=MorandiColors.TEXT_SECONDARY
        )
        saturation_label.pack(anchor="w", pady=(5, 2))
        
        self.saturation_slider = ctk.CTkSlider(
            adjust_frame,
            from_=0.0,
            to=2.0,
            number_of_steps=100,
            progress_color=MorandiColors.LAVENDER,
            button_color=MorandiColors.TAUPE,
            button_hover_color=MorandiColors.ACCENT_HOVER,
            command=self.adjust_saturation
        )
        self.saturation_slider.set(1.0)
        self.saturation_slider.pack(fill="x", pady=(0, 10))
        
        # 重置按钮
        self.reset_btn = ctk.CTkButton(
            adjust_frame,
            text="🔄 重置效果",
            height=38,
            corner_radius=19,
            fg_color=MorandiColors.WARM_GRAY,
            hover_color=MorandiColors.TAUPE,
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            border_width=0,
            command=self.reset_image
        )
        self.reset_btn.pack(fill="x", pady=(10, 5))
    
    def create_main_content(self):
        """创建主内容区 - 图片显示"""
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            corner_radius=20,
            fg_color=MorandiColors.BG_LIGHT,
            border_width=0
        )
        self.content_frame.pack(side="right", fill="both", expand=True, padx=(0, 25), pady=20)
        
        # 图片显示区域
        self.image_frame = ctk.CTkFrame(
            self.content_frame,
            corner_radius=16,
            fg_color=MorandiColors.CREAM,
            border_width=0
        )
        self.image_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 图片标签
        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=MorandiColors.TEXT_MUTED
        )
        self.image_label.pack(fill="both", expand=True)
        
        # 默认提示
        self.show_placeholder()
        
        # 底部信息栏
        self.info_bar = ctk.CTkFrame(
            self.content_frame,
            height=40,
            corner_radius=10,
            fg_color="transparent",
            border_width=0
        )
        self.info_bar.pack(fill="x", padx=20, pady=(0, 10))
        
        self.info_label = ctk.CTkLabel(
            self.info_bar,
            text="📷 暂无图片",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=MorandiColors.TEXT_MUTED
        )
        self.info_label.pack(side="left")
        
        self.size_label = ctk.CTkLabel(
            self.info_bar,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=MorandiColors.TEXT_MUTED
        )
        self.size_label.pack(side="right")
    
    def show_placeholder(self):
        """显示占位符"""
        self.image_label.configure(
            text="🖼️\n\n拖放图片到此处\n或点击「打开图片」按钮",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color=MorandiColors.TEXT_MUTED
        )
    
    def bind_events(self):
        """绑定事件"""
        # 窗口拖动
        for widget in [self.header, self.title_frame, self.app_title, self.app_subtitle]:
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
        
        self.bind("<Escape>", lambda e: self.close_window())
    
    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def do_drag(self, event):
        x = self.winfo_x() + event.x - self.drag_data["x"]
        y = self.winfo_y() + event.y - self.drag_data["y"]
        self.geometry(f"+{x}+{y}")
    
    def close_window(self):
        if hasattr(self, 'animated_gif'):
            self.animated_gif.stop()
        self.destroy()
    
    # ========== 图片操作 ==========
    
    def open_image(self):
        """打开图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path).convert("RGB")
            self.current_image = self.original_image.copy()
            self.display_image()
            self.update_info()
    
    def save_image(self):
        """保存图片"""
        if self.current_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg"),
                    ("BMP", "*.bmp")
                ]
            )
            if file_path:
                self.current_image.save(file_path)
    
    def display_image(self):
        """显示图片"""
        if self.current_image:
            # 计算适应显示区域的尺寸
            display_width = self.image_frame.winfo_width() - 40
            display_height = self.image_frame.winfo_height() - 40
            
            if display_width < 100:
                display_width = 600
            if display_height < 100:
                display_height = 500
            
            # 保持宽高比缩放
            img_ratio = self.current_image.width / self.current_image.height
            display_ratio = display_width / display_height
            
            if img_ratio > display_ratio:
                new_width = display_width
                new_height = int(display_width / img_ratio)
            else:
                new_height = display_height
                new_width = int(display_height * img_ratio)
            
            # 缩放并显示
            resized = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=resized, dark_image=resized, size=(new_width, new_height))
            self.image_label.configure(image=ctk_image, text="")
            self.image_label.image = ctk_image
    
    def update_info(self):
        """更新图片信息"""
        if self.current_image:
            filename = os.path.basename(self.image_path) if self.image_path else "未命名"
            self.info_label.configure(text=f"📷 {filename}")
            self.size_label.configure(text=f"{self.current_image.width} × {self.current_image.height} px")
    
    def reset_image(self):
        """重置图片"""
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.brightness_slider.set(1.0)
            self.contrast_slider.set(1.0)
            self.saturation_slider.set(1.0)
            self.display_image()
    
    # ========== 莫兰迪滤镜 ==========
    
    def apply_morandi_tone(self, image, r_shift, g_shift, b_shift, saturation=0.7):
        """应用莫兰迪色调"""
        # 降低饱和度
        enhancer = ImageEnhance.Color(image)
        img = enhancer.enhance(saturation)
        
        # 调整色调
        r, g, b = img.split()
        r = r.point(lambda x: min(255, x + r_shift))
        g = g.point(lambda x: min(255, x + g_shift))
        b = b.point(lambda x: min(255, x + b_shift))
        
        return Image.merge('RGB', (r, g, b))
    
    def apply_rose_filter(self):
        """玫瑰灰调滤镜"""
        if self.original_image:
            self.current_image = self.apply_morandi_tone(
                self.original_image.copy(), 15, -5, -10, 0.65
            )
            self.display_image()
    
    def apply_sage_filter(self):
        """鼠尾草绿滤镜"""
        if self.original_image:
            self.current_image = self.apply_morandi_tone(
                self.original_image.copy(), -10, 10, -5, 0.6
            )
            self.display_image()
    
    def apply_lavender_filter(self):
        """薰衣草紫滤镜"""
        if self.original_image:
            self.current_image = self.apply_morandi_tone(
                self.original_image.copy(), 5, -5, 15, 0.6
            )
            self.display_image()
    
    def apply_dusty_blue_filter(self):
        """雾霾蓝滤镜"""
        if self.original_image:
            self.current_image = self.apply_morandi_tone(
                self.original_image.copy(), -10, 0, 15, 0.55
            )
            self.display_image()
    
    # ========== 图片调整 ==========
    
    def adjust_brightness(self, value):
        """调整亮度"""
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.current_image)
            self.current_image = enhancer.enhance(value)
            self.display_image()
    
    def adjust_contrast(self, value):
        """调整对比度"""
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.current_image)
            self.current_image = enhancer.enhance(value)
            self.display_image()
    
    def adjust_saturation(self, value):
        """调整饱和度"""
        if self.original_image:
            enhancer = ImageEnhance.Color(self.current_image)
            self.current_image = enhancer.enhance(value)
            self.display_image()


def main():
    try:
        import customtkinter
        from PIL import Image
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter", "pillow"])
        print("依赖安装完成，请重新运行程序。")
        return
    
    app = MorandiImageApp()
    app.mainloop()


if __name__ == "__main__":
    main()

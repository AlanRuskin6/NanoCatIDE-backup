"""
Liquid Glass Style Borderless Rounded Window Application
使用 CustomTkinter 实现液态玻璃风格的现代 UI
"""

import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageSequence
import urllib.request
import io
import os
import sys

# 设置外观模式和默认颜色主题
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AnimatedGIF:
    """处理GIF动画的类 - 支持CTkImage以获得更好的HighDPI支持"""
    def __init__(self, label, gif_path, size=(80, 80)):
        self.label = label
        self.size = size
        self.frames = []
        self.pil_frames = []  # 保存PIL图像用于CTkImage
        self.durations = []
        self.current_frame = 0
        self.is_playing = True
        
        # 加载GIF帧
        try:
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                # 转换并调整大小
                pil_frame = frame.copy().convert("RGBA")
                pil_frame = pil_frame.resize(size, Image.Resampling.LANCZOS)
                self.pil_frames.append(pil_frame)
                # 创建CTkImage以支持HighDPI
                ctk_image = ctk.CTkImage(light_image=pil_frame, dark_image=pil_frame, size=size)
                self.frames.append(ctk_image)
                # 获取帧持续时间
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


class LiquidGlassCard(ctk.CTkFrame):
    """液态玻璃风格卡片组件"""
    def __init__(self, master, title="", description="", icon_url=None, **kwargs):
        super().__init__(
            master,
            corner_radius=20,
            fg_color=("rgba(255, 255, 255, 0.7)", "rgba(255, 255, 255, 0.7)"),
            border_width=1,
            border_color=("#e0e0e0", "#e0e0e0"),
            **kwargs
        )
        
        # 半透明白色背景模拟玻璃效果
        self.configure(fg_color="#ffffff")
        
        # 图标区域
        self.icon_frame = ctk.CTkFrame(
            self,
            width=50,
            height=50,
            corner_radius=15,
            fg_color="#f0f4ff"
        )
        self.icon_frame.pack(pady=(20, 10))
        self.icon_frame.pack_propagate(False)
        
        # 图标标签
        self.icon_label = ctk.CTkLabel(
            self.icon_frame,
            text="🔮",
            font=ctk.CTkFont(size=24)
        )
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#1a1a2e"
        )
        self.title_label.pack(pady=(5, 5))
        
        # 描述
        self.desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#666666",
            wraplength=150
        )
        self.desc_label.pack(pady=(0, 20))


class LiquidGlassButton(ctk.CTkButton):
    """液态玻璃风格按钮"""
    def __init__(self, master, **kwargs):
        default_config = {
            "corner_radius": 25,
            "fg_color": "#6366f1",
            "hover_color": "#4f46e5",
            "border_width": 0,
            "font": ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            "height": 45
        }
        default_config.update(kwargs)
        super().__init__(master, **default_config)


class LiquidGlassApp(ctk.CTk):
    """主应用窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 获取GIF路径
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.gif_path = os.path.join(self.script_dir, "d0c438b0de1b4f779ced045eeac32c175127bf0a6930-YP8Y17_fw1200.gif")
        
        # 窗口配置
        self.title("Liquid Glass UI")
        self.geometry("1000x700")
        self.configure(fg_color="#f8fafc")  # 浅白色背景
        
        # 无边框设置
        self.overrideredirect(True)
        
        # 圆角窗口（通过透明区域实现）
        self.attributes("-transparentcolor", "")
        self.attributes("-alpha", 0.98)
        
        # 居中显示
        self.center_window()
        
        # 窗口拖动
        self.drag_data = {"x": 0, "y": 0}
        
        # 创建主容器
        self.create_main_container()
        
        # 创建UI组件
        self.create_header()
        self.create_content()
        self.create_footer()
        
        # 绑定事件
        self.bind_events()
    
    def center_window(self):
        """居中显示窗口"""
        self.update_idletasks()
        width = 1000
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_main_container(self):
        """创建主容器，无边框设计"""
        # 主容器 - 白色背景，无边框
        self.main_container = ctk.CTkFrame(
            self,
            corner_radius=25,
            fg_color="#ffffff",
            border_width=0
        )
        self.main_container.pack(fill="both", expand=True)
    
    def create_header(self):
        """创建顶部标题栏"""
        self.header = ctk.CTkFrame(
            self.main_container,
            height=80,
            corner_radius=0,
            fg_color="transparent"
        )
        self.header.pack(fill="x", padx=20, pady=(15, 0))
        self.header.pack_propagate(False)
        
        # 左侧 - GIF动画
        self.gif_label = ctk.CTkLabel(
            self.header,
            text="",
            width=80,
            height=80
        )
        self.gif_label.place(x=0, y=0)
        
        # 加载并播放GIF
        if os.path.exists(self.gif_path):
            self.animated_gif = AnimatedGIF(self.gif_label, self.gif_path, size=(70, 70))
            self.animated_gif.start()
        else:
            # 如果GIF不存在，显示占位符
            self.gif_label.configure(text="✨", font=ctk.CTkFont(size=40))
        
        # 标题区域
        self.title_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        self.title_frame.place(x=90, y=10)
        
        self.app_title = ctk.CTkLabel(
            self.title_frame,
            text="Liquid Glass Design",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#1e293b"
        )
        self.app_title.pack(anchor="w")
        
        self.app_subtitle = ctk.CTkLabel(
            self.title_frame,
            text="现代化液态玻璃风格界面",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#64748b"
        )
        self.app_subtitle.pack(anchor="w")
        
        # 右侧控制按钮
        self.controls_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        self.controls_frame.place(relx=1.0, x=-10, y=20, anchor="ne")
        
        # 最小化按钮
        self.min_btn = ctk.CTkButton(
            self.controls_frame,
            text="─",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#64748b",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.minimize_window
        )
        self.min_btn.pack(side="left", padx=5)
        
        # 关闭按钮
        self.close_btn = ctk.CTkButton(
            self.controls_frame,
            text="×",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#fee2e2",
            hover_color="#fecaca",
            text_color="#ef4444",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.close_window
        )
        self.close_btn.pack(side="left", padx=5)
    
    def create_content(self):
        """创建主内容区域"""
        self.content = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 顶部横幅
        self.create_banner()
        
        # 功能卡片区域
        self.create_cards_section()
        
        # 底部操作区
        self.create_action_section()
    
    def create_banner(self):
        """创建顶部横幅"""
        self.banner = ctk.CTkFrame(
            self.content,
            height=150,
            corner_radius=20,
            fg_color="#6366f1"
        )
        self.banner.pack(fill="x", pady=(0, 25))
        self.banner.pack_propagate(False)
        
        # 横幅内容
        banner_content = ctk.CTkFrame(
            self.banner,
            fg_color="transparent"
        )
        banner_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # 左侧文字
        text_frame = ctk.CTkFrame(banner_content, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        
        welcome_label = ctk.CTkLabel(
            text_frame,
            text="✨ 欢迎体验液态玻璃设计",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#ffffff"
        )
        welcome_label.pack(anchor="w", pady=(10, 5))
        
        desc_label = ctk.CTkLabel(
            text_frame,
            text="探索现代化的透明质感UI设计，体验流畅的视觉效果",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#c7d2fe"
        )
        desc_label.pack(anchor="w")
        
        # 右侧装饰
        deco_frame = ctk.CTkFrame(banner_content, fg_color="transparent")
        deco_frame.pack(side="right", fill="y")
        
        # 装饰性图标
        icons = ["🌟", "💎", "🔮"]
        for i, icon in enumerate(icons):
            icon_label = ctk.CTkLabel(
                deco_frame,
                text=icon,
                font=ctk.CTkFont(size=30),
                fg_color="#818cf8",
                corner_radius=15,
                width=50,
                height=50
            )
            icon_label.pack(side="left", padx=5)
    
    def create_cards_section(self):
        """创建功能卡片区域"""
        cards_container = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        cards_container.pack(fill="x", pady=(0, 20))
        
        # 配置网格列权重
        for i in range(4):
            cards_container.columnconfigure(i, weight=1)
        
        # 卡片数据
        cards_data = [
            {"title": "云端存储", "desc": "安全的云端数据存储", "icon": "☁️", "color": "#dbeafe"},
            {"title": "智能分析", "desc": "AI驱动的数据分析", "icon": "🧠", "color": "#fce7f3"},
            {"title": "实时同步", "desc": "多设备实时同步", "icon": "🔄", "color": "#d1fae5"},
            {"title": "安全防护", "desc": "企业级安全保护", "icon": "🛡️", "color": "#fef3c7"}
        ]
        
        for i, card_info in enumerate(cards_data):
            card = self.create_glass_card(
                cards_container,
                card_info["title"],
                card_info["desc"],
                card_info["icon"],
                card_info["color"]
            )
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
    
    def create_glass_card(self, parent, title, description, icon, icon_bg):
        """创建单个玻璃卡片"""
        card = ctk.CTkFrame(
            parent,
            corner_radius=20,
            fg_color="#ffffff",
            border_width=0
        )
        
        # 图标容器
        icon_frame = ctk.CTkFrame(
            card,
            width=55,
            height=55,
            corner_radius=15,
            fg_color=icon_bg
        )
        icon_frame.pack(pady=(25, 12))
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=ctk.CTkFont(size=26)
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 标题
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#1e293b"
        )
        title_label.pack(pady=(0, 5))
        
        # 描述
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#64748b"
        )
        desc_label.pack(pady=(0, 25))
        
        # 悬停效果
        def on_enter(e):
            card.configure(fg_color="#f0f4ff")
        
        def on_leave(e):
            card.configure(fg_color="#ffffff")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return card
    
    def create_action_section(self):
        """创建底部操作区"""
        action_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        action_frame.pack(fill="x", pady=(10, 0))
        
        # 左侧信息
        info_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        info_frame.pack(side="left")
        
        status_label = ctk.CTkLabel(
            info_frame,
            text="● 系统运行正常",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#22c55e"
        )
        status_label.pack(anchor="w")
        
        version_label = ctk.CTkLabel(
            info_frame,
            text="版本 1.0.0 | Liquid Glass UI Framework",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#94a3b8"
        )
        version_label.pack(anchor="w")
        
        # 右侧按钮
        btn_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # 次要按钮
        secondary_btn = ctk.CTkButton(
            btn_frame,
            text="📖 文档",
            width=100,
            height=42,
            corner_radius=21,
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        secondary_btn.pack(side="left", padx=8)
        
        # 次要按钮2
        settings_btn = ctk.CTkButton(
            btn_frame,
            text="⚙️ 设置",
            width=100,
            height=42,
            corner_radius=21,
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        settings_btn.pack(side="left", padx=8)
        
        # 主要按钮
        primary_btn = ctk.CTkButton(
            btn_frame,
            text="🚀 开始使用",
            width=130,
            height=42,
            corner_radius=21,
            fg_color="#6366f1",
            hover_color="#4f46e5",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        primary_btn.pack(side="left", padx=8)
    
    def create_footer(self):
        """创建底部状态栏"""
        self.footer = ctk.CTkFrame(
            self.main_container,
            height=40,
            corner_radius=0,
            fg_color="#f8fafc"
        )
        self.footer.pack(fill="x", side="bottom", padx=20, pady=(0, 15))
        
        # 底部信息
        footer_label = ctk.CTkLabel(
            self.footer,
            text="© 2024 Liquid Glass UI • Designed with ❤️",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#94a3b8"
        )
        footer_label.pack(side="left", pady=10)
        
        # 右侧时间显示
        import datetime
        time_label = ctk.CTkLabel(
            self.footer,
            text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#94a3b8"
        )
        time_label.pack(side="right", pady=10)
    
    def bind_events(self):
        """绑定窗口事件"""
        # 窗口拖动
        self.header.bind("<Button-1>", self.start_drag)
        self.header.bind("<B1-Motion>", self.do_drag)
        self.title_frame.bind("<Button-1>", self.start_drag)
        self.title_frame.bind("<B1-Motion>", self.do_drag)
        self.app_title.bind("<Button-1>", self.start_drag)
        self.app_title.bind("<B1-Motion>", self.do_drag)
        self.app_subtitle.bind("<Button-1>", self.start_drag)
        self.app_subtitle.bind("<B1-Motion>", self.do_drag)
        
        # 键盘快捷键
        self.bind("<Escape>", lambda e: self.close_window())
    
    def start_drag(self, event):
        """开始拖动"""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def do_drag(self, event):
        """执行拖动"""
        x = self.winfo_x() + event.x - self.drag_data["x"]
        y = self.winfo_y() + event.y - self.drag_data["y"]
        self.geometry(f"+{x}+{y}")
    
    def minimize_window(self):
        """最小化窗口"""
        self.iconify()
    
    def close_window(self):
        """关闭窗口"""
        if hasattr(self, 'animated_gif'):
            self.animated_gif.stop()
        self.destroy()


def main():
    """主函数"""
    # 检查依赖
    try:
        import customtkinter
        from PIL import Image
    except ImportError as e:
        print("缺少必要的依赖库，正在安装...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter", "pillow"])
        print("依赖安装完成，请重新运行程序。")
        return
    
    app = LiquidGlassApp()
    app.mainloop()


if __name__ == "__main__":
    main()

# Liquid Glass App

一个使用 C# WPF 开发的现代化 Liquid Glass 风格无边框圆角应用程序。

## 特性

- 🎨 **Liquid Glass 设计风格** - 浅白色调背景，柔和渐变效果
- 🪟 **无边框圆角窗口** - 使用 `WindowStyle="None"` 和 `AllowsTransparency="True"`
- 🎬 **GIF 动画装饰** - 左上角装饰性 GIF 动画
- 📊 **交互式图表** - 使用 Canvas 绘制的数据趋势图
- 🎯 **现代化 UI 组件** - 卡片、按钮、导航等均采用玻璃拟态设计

## 使用的库

| 库名 | 版本 | 用途 |
|------|------|------|
| WpfAnimatedGif | 2.0.2 | GIF 动画支持 |
| FluentWPF | 0.10.2 | 流畅设计效果支持 |

## 设计语言

- **主色调**: 浅白色 (#FAFBFC)
- **强调色**: 紫蓝渐变 (#667EEA → #764BA2)
- **圆角**: 10-20px
- **阴影**: 柔和投影，低透明度

## 运行方式

```powershell
cd c:\Users\joyto\Desktop\design\LiquidGlassApp
dotnet run
```

或者直接运行编译后的 exe:
```
.\bin\Debug\net8.0-windows\LiquidGlassApp.exe
```

## 项目结构

```
LiquidGlassApp/
├── App.xaml              # 应用资源和样式定义
├── App.xaml.cs
├── MainWindow.xaml       # 主界面 XAML
├── MainWindow.xaml.cs    # 主界面逻辑
├── LiquidGlassApp.csproj # 项目文件
├── Assets/               # 资源文件目录
│   └── *.gif            # GIF 动画文件
└── README.md
```

## 窗口功能

- ✅ 拖动标题栏移动窗口
- ✅ 双击标题栏最大化/还原
- ✅ 最小化、最大化、关闭按钮
- ✅ 可调整窗口大小

## 截图

应用程序展示了一个现代化的仪表盘界面，包含：
- 左侧导航菜单
- 统计卡片
- 数据趋势图表
- 最近活动列表
- 底部行动号召区域

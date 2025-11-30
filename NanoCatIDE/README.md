<p align="center">
  <img src="docs/images/logo.png" alt="NanoCat IDE Logo" width="120" height="120">
</p>

<h1 align="center">NanoCat IDE</h1>

<p align="center">
  <strong>🐱 一款现代化的数据分析集成开发环境</strong>
</p>

<p align="center">
  <a href="#特性">特性</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#项目结构">项目结构</a> •
  <a href="#贡献指南">贡献指南</a> •
  <a href="#许可证">许可证</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet" alt=".NET 8.0">
  <img src="https://img.shields.io/badge/WPF-Windows-0078D6?logo=windows" alt="WPF">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python" alt="Python 3.11">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

---

## ✨ 特性

- 🎨 **Liquid Glass 设计风格** - 6 种精心设计的莫兰迪色系主题
- 🐍 **内置 Python 环境** - 独立隔离，无需额外安装，开箱即用
- 📊 **数据分析工作流** - 数据导入、清洗、审查、分析一站式完成
- 🤖 **AI 智能助手** - 自然语言交互，让数据分析更简单
- 📦 **环境管理** - 可视化管理 Python 库，支持国内镜像源
- 🪟 **现代化 UI** - 无边框圆角窗口，流畅动画效果

## 📸 截图

> TODO: 添加应用截图

## 🚀 快速开始

### 系统要求

- Windows 10/11 (64-bit)
- .NET 8.0 Runtime（或使用独立版本无需安装）

### 下载安装

从 [Releases](https://github.com/AlanRuskin6/NanoCatIDE-backup/releases) 下载最新版本。

### 从源码构建

```powershell
# 克隆仓库
git clone https://github.com/AlanRuskin6/NanoCatIDE-backup.git
cd NanoCatIDE-backup/NanoCatIDE

# 还原依赖并构建
dotnet restore
dotnet build

# 运行
dotnet run
```

### 发布独立版本

```powershell
# 发布为单文件可执行程序
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
```

## 📁 项目结构

```
NanoCatIDE/
├── 📄 App.xaml                 # 应用程序入口和全局样式
├── 📄 App.xaml.cs
├── 📄 MainWindow.xaml          # 主窗口界面
├── 📄 MainWindow.xaml.cs       # 主窗口逻辑（含主题系统）
├── 📄 NanoCatIDE.csproj        # 项目配置文件
├── 📄 app.manifest             # Windows 应用清单
│
├── 📁 Pages/                   # 页面组件
│   ├── AgentPage.xaml/.cs      # AI 助手聊天页面
│   ├── DataAnalysisPage.xaml/.cs   # 数据分析页面
│   ├── DataCleanPage.xaml/.cs  # 数据清洗页面
│   ├── DataReviewPage.xaml/.cs # 数据审查页面
│   ├── EnvironmentPage.xaml/.cs    # 环境管理页面
│   └── AIProcessPage.xaml/.cs  # AI 处理页面
│
├── 📁 Assets/                  # 静态资源
│   └── gif/                    # GIF 动画资源
│
├── 📁 PythonEmbed/             # 内嵌 Python 环境
│   └── python311/              # Python 3.11 运行时
│
├── 📁 Themes/                  # 主题资源（扩展用）
│
├── 📄 run.ps1                  # 开发运行脚本
└── 📄 publish.ps1              # 发布脚本
```

## 🎨 主题系统

NanoCat IDE 内置 6 种精心设计的莫兰迪色系主题：

| 主题 | 描述 |
|------|------|
| 💠 经典 | 极简蓝灰，专业稳重 |
| 🌿 青雾 | 莫兰迪绿，自然清新 |
| ☁️ 雾灰 | 高级中性灰，优雅内敛 |
| 🌅 黛紫 | 烟熏紫色，浪漫神秘 |
| 🌊 雾蓝 | 雾霾蓝调，宁静舒适 |

点击右上角的主题按钮即可切换。

## 🐍 Python 环境

NanoCat IDE 使用独立的内嵌 Python 环境：

- **位置**: `%LOCALAPPDATA%\NanoCatIDE\PythonEmbed\python311\`
- **版本**: Python 3.11.9
- **特点**: 与系统 Python 完全隔离，可随时重置

### 预装库

- pandas - 数据分析
- numpy - 科学计算
- matplotlib - 数据可视化
- openpyxl - Excel 支持
- 更多...

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| .NET 8.0 | 运行时框架 |
| WPF | UI 框架 |
| WpfAnimatedGif | GIF 动画支持 |
| FluentWPF | 流畅设计效果 |
| LiveCharts | 图表可视化 |
| Python 3.11 | 数据处理引擎 |

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. **Fork** 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起 **Pull Request**

### 开发规范

- 遵循 C# 编码规范
- XAML 使用 4 空格缩进
- 新功能需要添加相应注释
- 提交信息使用中文或英文均可

### 待办事项

- [ ] 添加单元测试
- [ ] 完善 AI 助手功能
- [ ] 支持更多数据格式导入
- [ ] 添加数据可视化图表
- [ ] 国际化支持
- [ ] 深色主题

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🙏 致谢

- [WpfAnimatedGif](https://github.com/XamlAnimatedGif/WpfAnimatedGif) - GIF 动画支持
- [FluentWPF](https://github.com/sourcechord/FluentWPF) - 流畅设计
- [LiveCharts](https://github.com/Live-Charts/Live-Charts) - 图表库

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/AlanRuskin6">AlanRuskin6</a>
</p>

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

# 贡献指南

感谢你考虑为 NanoCat IDE 做出贡献！🎉

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请创建一个 Issue，并包含以下信息：

- 问题的详细描述
- 复现步骤
- 预期行为 vs 实际行为
- 系统环境（Windows 版本、.NET 版本等）
- 如果可能，附上截图或错误日志

### 提出新功能

欢迎提出新功能建议！请在 Issue 中描述：

- 功能的具体用途
- 为什么这个功能对用户有帮助
- 可能的实现方式（可选）

### 提交代码

1. **Fork 仓库**
   
   点击右上角的 Fork 按钮

2. **克隆到本地**
   ```bash
   git clone https://github.com/你的用户名/NanoCatIDE-backup.git
   cd NanoCatIDE-backup
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/你的功能名称
   ```

4. **进行开发**
   
   请确保代码符合项目规范

5. **测试你的更改**
   ```bash
   dotnet build
   dotnet run
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加了某某功能"
   ```

7. **推送到你的仓库**
   ```bash
   git push origin feature/你的功能名称
   ```

8. **创建 Pull Request**
   
   在 GitHub 上发起 Pull Request

## 开发规范

### 代码风格

- **C#**: 遵循 Microsoft C# 编码规范
- **XAML**: 使用 4 空格缩进，属性换行对齐
- **命名**: 使用 PascalCase 命名类和方法，camelCase 命名局部变量

### 提交信息格式

使用语义化提交信息：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整（不影响功能）
- `refactor:` 代码重构
- `perf:` 性能优化
- `test:` 添加测试
- `chore:` 构建/工具链相关

示例：
```
feat: 添加深色主题支持
fix: 修复数据导入时的编码问题
docs: 更新 README 安装说明
```

### 分支命名

- `feature/xxx` - 新功能
- `fix/xxx` - Bug 修复
- `docs/xxx` - 文档更新
- `refactor/xxx` - 代码重构

## 开发环境设置

### 必需工具

- Visual Studio 2022 或 VS Code
- .NET 8.0 SDK
- Git

### 推荐扩展

**Visual Studio:**
- XAML Styler

**VS Code:**
- C# Dev Kit
- XAML Language Support

## 项目架构

```
NanoCatIDE/
├── App.xaml              # 全局资源和样式
├── MainWindow.xaml       # 主窗口 + 导航 + 主题系统
├── Pages/                # 各功能页面
│   ├── AgentPage         # AI 助手
│   ├── DataAnalysisPage  # 数据分析
│   ├── DataCleanPage     # 数据清洗
│   ├── DataReviewPage    # 数据审查
│   └── EnvironmentPage   # 环境管理
└── PythonEmbed/          # 内嵌 Python 环境
```

### 添加新页面

1. 在 `Pages/` 目录创建新的 `.xaml` 和 `.xaml.cs` 文件
2. 在 `MainWindow.xaml.cs` 的导航逻辑中添加对应处理
3. 在侧边栏添加导航按钮

### 添加新主题

在 `MainWindow.xaml.cs` 的 `_themes` 数组中添加新的 `ThemeConfig`：

```csharp
new ThemeConfig
{
    Name = "主题名称",
    Icon = "🎨",
    PrimaryLight = Color.FromRgb(R, G, B),
    // ... 其他颜色配置
}
```

## 获取帮助

如有疑问，请：

1. 查看现有的 Issues
2. 创建新的 Discussion
3. 在 Issue 中 @ 维护者

再次感谢你的贡献！❤️

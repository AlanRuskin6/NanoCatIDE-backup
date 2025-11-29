using System;
using System.Linq;
using System.Net.Http;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Effects;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Windows.Threading;
using WpfAnimatedGif;
using IOPath = System.IO.Path;
using IOFile = System.IO.File;
using IODirectory = System.IO.Directory;
using IOMemoryStream = System.IO.MemoryStream;

namespace LiquidGlassApp
{
    // 淡雅主题配置
    public class ThemeConfig
    {
        public string Name { get; set; } = "";
        public string Icon { get; set; } = "";
        // 基础色
        public Color PrimaryLight { get; set; }
        public Color PrimaryMedium { get; set; }
        public Color PrimaryAccent { get; set; }
        // 背景色
        public Color BackgroundStart { get; set; }
        public Color BackgroundEnd { get; set; }
        public Color SidebarStart { get; set; }
        public Color SidebarEnd { get; set; }
        public Color BorderAccent { get; set; }
        // 强调色 (用于按钮、头像、选中状态等)
        public Color AccentStart { get; set; }
        public Color AccentMiddle { get; set; }
        public Color AccentEnd { get; set; }
        // 卡片背景
        public Color CardBackground { get; set; }
        public Color CardBorder { get; set; }
        // 图标背景色
        public Color IconBg1 { get; set; }
        public Color IconBg2 { get; set; }
        public Color IconBg3 { get; set; }
        public Color IconBg4 { get; set; }
        // 阴影颜色
        public Color ShadowColor { get; set; }
    }

    public partial class MainWindow : Window
    {
        private readonly Random _random = new Random();
        private readonly DispatcherTimer _gifTimer;
        private string[] _availableGifs = Array.Empty<string>();
        
        // GIF 所在目录
        private const string GIF_DIRECTORY = @"c:\Users\joyto\Desktop\design";
        
        // 主题系统
        private int _currentThemeIndex = 0;
        private readonly ThemeConfig[] _themes = new ThemeConfig[]
        {
            // 🌸 烟粉 - 莫兰迪粉（低饱和度）
            new ThemeConfig
            {
                Name = "烟粉",
                Icon = "🌸",
                PrimaryLight = Color.FromRgb(252, 250, 250),
                PrimaryMedium = Color.FromRgb(248, 244, 245),
                PrimaryAccent = Color.FromRgb(240, 232, 234),
                BackgroundStart = Color.FromRgb(253, 251, 251),
                BackgroundEnd = Color.FromRgb(250, 247, 248),
                SidebarStart = Color.FromRgb(251, 249, 249),
                SidebarEnd = Color.FromRgb(247, 244, 245),
                BorderAccent = Color.FromArgb(20, 180, 160, 165),
                AccentStart = Color.FromRgb(200, 175, 180),
                AccentMiddle = Color.FromRgb(185, 158, 165),
                AccentEnd = Color.FromRgb(168, 140, 148),
                CardBackground = Color.FromRgb(252, 250, 250),
                CardBorder = Color.FromArgb(15, 180, 160, 165),
                IconBg1 = Color.FromRgb(245, 240, 241),
                IconBg2 = Color.FromRgb(242, 236, 238),
                IconBg3 = Color.FromRgb(247, 243, 244),
                IconBg4 = Color.FromRgb(244, 239, 240),
                ShadowColor = Color.FromRgb(180, 160, 165)
            },
            // 🌿 青雾 - 莫兰迪绿（雾霾蓝绿）
            new ThemeConfig
            {
                Name = "青雾",
                Icon = "🌿",
                PrimaryLight = Color.FromRgb(249, 252, 251),
                PrimaryMedium = Color.FromRgb(244, 248, 246),
                PrimaryAccent = Color.FromRgb(230, 238, 235),
                BackgroundStart = Color.FromRgb(250, 253, 252),
                BackgroundEnd = Color.FromRgb(246, 250, 248),
                SidebarStart = Color.FromRgb(248, 251, 250),
                SidebarEnd = Color.FromRgb(243, 248, 246),
                BorderAccent = Color.FromArgb(20, 145, 165, 158),
                AccentStart = Color.FromRgb(168, 188, 180),
                AccentMiddle = Color.FromRgb(148, 172, 162),
                AccentEnd = Color.FromRgb(128, 152, 142),
                CardBackground = Color.FromRgb(250, 252, 251),
                CardBorder = Color.FromArgb(15, 145, 165, 158),
                IconBg1 = Color.FromRgb(240, 246, 244),
                IconBg2 = Color.FromRgb(236, 243, 240),
                IconBg3 = Color.FromRgb(243, 248, 246),
                IconBg4 = Color.FromRgb(238, 245, 242),
                ShadowColor = Color.FromRgb(145, 165, 158)
            },
            // ☁️ 雾灰 - 高级中性灰
            new ThemeConfig
            {
                Name = "雾灰",
                Icon = "☁️",
                PrimaryLight = Color.FromRgb(250, 250, 251),
                PrimaryMedium = Color.FromRgb(245, 246, 248),
                PrimaryAccent = Color.FromRgb(232, 234, 238),
                BackgroundStart = Color.FromRgb(251, 251, 252),
                BackgroundEnd = Color.FromRgb(247, 248, 250),
                SidebarStart = Color.FromRgb(249, 250, 251),
                SidebarEnd = Color.FromRgb(244, 245, 248),
                BorderAccent = Color.FromArgb(20, 140, 148, 160),
                AccentStart = Color.FromRgb(170, 178, 190),
                AccentMiddle = Color.FromRgb(150, 160, 175),
                AccentEnd = Color.FromRgb(130, 140, 158),
                CardBackground = Color.FromRgb(251, 251, 252),
                CardBorder = Color.FromArgb(15, 140, 148, 160),
                IconBg1 = Color.FromRgb(242, 244, 248),
                IconBg2 = Color.FromRgb(238, 240, 245),
                IconBg3 = Color.FromRgb(245, 246, 250),
                IconBg4 = Color.FromRgb(240, 242, 247),
                ShadowColor = Color.FromRgb(140, 148, 160)
            },
            // 🌅 黛紫 - 莫兰迪紫（烟熏紫）
            new ThemeConfig
            {
                Name = "黛紫",
                Icon = "🌅",
                PrimaryLight = Color.FromRgb(251, 250, 252),
                PrimaryMedium = Color.FromRgb(246, 244, 250),
                PrimaryAccent = Color.FromRgb(235, 230, 242),
                BackgroundStart = Color.FromRgb(252, 251, 253),
                BackgroundEnd = Color.FromRgb(248, 246, 251),
                SidebarStart = Color.FromRgb(250, 249, 252),
                SidebarEnd = Color.FromRgb(245, 243, 249),
                BorderAccent = Color.FromArgb(20, 155, 148, 172),
                AccentStart = Color.FromRgb(180, 172, 195),
                AccentMiddle = Color.FromRgb(162, 152, 180),
                AccentEnd = Color.FromRgb(142, 132, 162),
                CardBackground = Color.FromRgb(251, 250, 252),
                CardBorder = Color.FromArgb(15, 155, 148, 172),
                IconBg1 = Color.FromRgb(244, 241, 249),
                IconBg2 = Color.FromRgb(240, 237, 246),
                IconBg3 = Color.FromRgb(246, 244, 251),
                IconBg4 = Color.FromRgb(242, 239, 248),
                ShadowColor = Color.FromRgb(155, 148, 172)
            },
            // 🌊 雾蓝 - 莫兰迪蓝（雾霾蓝）
            new ThemeConfig
            {
                Name = "雾蓝",
                Icon = "🌊",
                PrimaryLight = Color.FromRgb(249, 251, 253),
                PrimaryMedium = Color.FromRgb(244, 247, 251),
                PrimaryAccent = Color.FromRgb(230, 236, 244),
                BackgroundStart = Color.FromRgb(250, 252, 254),
                BackgroundEnd = Color.FromRgb(246, 249, 252),
                SidebarStart = Color.FromRgb(248, 251, 253),
                SidebarEnd = Color.FromRgb(243, 247, 251),
                BorderAccent = Color.FromArgb(20, 140, 158, 178),
                AccentStart = Color.FromRgb(165, 182, 200),
                AccentMiddle = Color.FromRgb(145, 165, 188),
                AccentEnd = Color.FromRgb(125, 148, 172),
                CardBackground = Color.FromRgb(250, 252, 253),
                CardBorder = Color.FromArgb(15, 140, 158, 178),
                IconBg1 = Color.FromRgb(240, 245, 251),
                IconBg2 = Color.FromRgb(236, 242, 249),
                IconBg3 = Color.FromRgb(243, 248, 253),
                IconBg4 = Color.FromRgb(238, 244, 250),
                ShadowColor = Color.FromRgb(140, 158, 178)
            }
        };
        
        public MainWindow()
        {
            InitializeComponent();
            
            // 初始化 GIF 定时器 - 每 5 秒随机切换
            _gifTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromSeconds(5)
            };
            _gifTimer.Tick += (s, e) => LoadRandomGif();
            
            // 窗口加载完成后应用初始主题和加载资源
            Loaded += async (s, e) => 
            {
                ApplyTheme(_themes[_currentThemeIndex]);
                
                // 尝试播放动画，如果失败则确保窗口可见
                try 
                {
                    // 确保在 UI 线程空闲时执行动画，避免初始化竞争
                    await Dispatcher.InvokeAsync(() => PlayOpenAnimation(), DispatcherPriority.ApplicationIdle);
                }
                catch (Exception)
                {
                    Opacity = 1;
                }

                // 异步加载 GIF，避免阻塞 UI 线程
                await System.Threading.Tasks.Task.Run(() => LoadAvailableGifs());
                LoadRandomGif();
                
                // 启动定时器
                _gifTimer.Start();
            };
        }

        /// <summary>
        /// 播放窗口打开动画 - 模拟 Windows 原生弹出效果
        /// </summary>
        private void PlayOpenAnimation()
        {
            // 确保初始状态
            Opacity = 0;
            
            var duration = TimeSpan.FromMilliseconds(250); // 原生动画通常较快
            var easing = new CubicEase { EasingMode = EasingMode.EaseOut }; // 使用 CubicEase 更接近原生感觉

            // 设置变换原点为中心
            RenderTransformOrigin = new Point(0.5, 0.5);

            // 设置 RenderTransform
            var transformGroup = new TransformGroup();
            var scaleTransform = new ScaleTransform(0.95, 0.95); // 原生缩放幅度较小
            transformGroup.Children.Add(scaleTransform);
            RenderTransform = transformGroup;

            // 淡入动画
            var fadeIn = new DoubleAnimation(0, 1, duration) { EasingFunction = easing };

            // 缩放动画
            var scaleX = new DoubleAnimation(0.95, 1, duration) { EasingFunction = easing };
            var scaleY = new DoubleAnimation(0.95, 1, duration) { EasingFunction = easing };
            
            // 启动动画
            BeginAnimation(OpacityProperty, fadeIn);
            scaleTransform.BeginAnimation(ScaleTransform.ScaleXProperty, scaleX);
            scaleTransform.BeginAnimation(ScaleTransform.ScaleYProperty, scaleY);
        }

        /// <summary>
        /// 加载目录中所有可用的 GIF 文件
        /// </summary>
        private void LoadAvailableGifs()
        {
            try
            {
                if (IODirectory.Exists(GIF_DIRECTORY))
                {
                    _availableGifs = IODirectory.GetFiles(GIF_DIRECTORY, "*.gif")
                        .Where(f => IOFile.Exists(f))
                        .ToArray();
                }
            }
            catch (Exception)
            {
                _availableGifs = Array.Empty<string>();
            }
        }

        /// <summary>
        /// 随机加载一个 GIF
        /// </summary>
        private void LoadRandomGif()
        {
            try
            {
                if (_availableGifs.Length > 0)
                {
                    // 随机选择一个 GIF
                    int randomIndex = _random.Next(_availableGifs.Length);
                    string selectedGif = _availableGifs[randomIndex];
                    
                    LoadGifFromPath(selectedGif);
                }
                else
                {
                    // 没有本地 GIF，加载在线 GIF
                    LoadOnlineGif();
                }
            }
            catch (Exception)
            {
                LoadOnlineGif();
            }
        }

        /// <summary>
        /// 从指定路径加载 GIF
        /// </summary>
        private void LoadGifFromPath(string gifPath)
        {
            try
            {
                if (IOFile.Exists(gifPath))
                {
                    var image = new BitmapImage();
                    image.BeginInit();
                    image.UriSource = new Uri(gifPath, UriKind.Absolute);
                    image.CacheOption = BitmapCacheOption.OnLoad;
                    image.EndInit();
                    
                    ImageBehavior.SetAnimatedSource(DecorationGif, image);
                }
            }
            catch (Exception)
            {
                // 忽略单个 GIF 加载失败
            }
        }

        private async void LoadOnlineGif()
        {
            try
            {
                // 使用高质量的在线装饰性 GIF
                string onlineGifUrl = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif";
                
                using (HttpClient client = new HttpClient())
                {
                    byte[] gifData = await client.GetByteArrayAsync(onlineGifUrl);
                    
                    using (IOMemoryStream stream = new IOMemoryStream(gifData))
                    {
                        var image = new BitmapImage();
                        image.BeginInit();
                        image.StreamSource = stream;
                        image.CacheOption = BitmapCacheOption.OnLoad;
                        image.EndInit();
                        image.Freeze();
                        
                        Dispatcher.Invoke(() =>
                        {
                            ImageBehavior.SetAnimatedSource(DecorationGif, image);
                        });
                    }
                }
            }
            catch (Exception)
            {
                // 如果在线加载也失败，使用渐变占位符
                Dispatcher.Invoke(() =>
                {
                    DecorationGif.Visibility = Visibility.Collapsed;
                });
            }
        }

        private void UpdateChart(ThemeConfig theme)
        {
            if (ChartCanvas == null) return;
            ChartCanvas.Children.Clear();
            
            double[] values = { 30, 50, 40, 70, 45, 80, 65, 90, 75, 85, 95, 88 };
            double width = ChartCanvas.ActualWidth > 0 ? ChartCanvas.ActualWidth : 400;
            double height = ChartCanvas.ActualHeight > 0 ? ChartCanvas.ActualHeight : 160;
            
            if (width <= 0 || height <= 0) return;
            
            double stepX = width / (values.Length - 1);
            double maxValue = 100;
            
            // 创建渐变填充
            PathFigure areaFigure = new PathFigure();
            areaFigure.StartPoint = new Point(0, height);
            
            PolyLineSegment areaSegment = new PolyLineSegment();
            areaSegment.Points.Add(new Point(0, height - (values[0] / maxValue * height)));
            
            for (int i = 1; i < values.Length; i++)
            {
                double x = i * stepX;
                double y = height - (values[i] / maxValue * height);
                areaSegment.Points.Add(new Point(x, y));
            }
            
            areaSegment.Points.Add(new Point((values.Length - 1) * stepX, height));
            areaFigure.Segments.Add(areaSegment);
            
            PathGeometry areaGeometry = new PathGeometry();
            areaGeometry.Figures.Add(areaFigure);
            
            Path areaPath = new Path();
            areaPath.Data = areaGeometry;
            
            // 使用主题色
            var fillBrush = new LinearGradientBrush(
                Color.FromArgb(40, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B),
                Color.FromArgb(5, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B),
                90);
            fillBrush.Freeze();
            areaPath.Fill = fillBrush;
            
            ChartCanvas.Children.Add(areaPath);
            
            // 绘制折线
            Polyline line = new Polyline();
            var strokeBrush = new LinearGradientBrush(
                theme.AccentMiddle,
                theme.AccentEnd,
                0);
            strokeBrush.Freeze();
            line.Stroke = strokeBrush;
            
            line.StrokeThickness = 3;
            line.StrokeLineJoin = PenLineJoin.Round;
            
            PointCollection points = new PointCollection();
            for (int i = 0; i < values.Length; i++)
            {
                double x = i * stepX;
                double y = height - (values[i] / maxValue * height);
                points.Add(new Point(x, y));
            }
            line.Points = points;
            
            ChartCanvas.Children.Add(line);
            
            // 添加数据点
            var dotFill = new LinearGradientBrush(
                theme.AccentMiddle,
                theme.AccentEnd,
                45);
            dotFill.Freeze();
            
            for (int i = 0; i < values.Length; i++)
            {
                double x = i * stepX;
                double y = height - (values[i] / maxValue * height);
                
                Ellipse dot = new Ellipse();
                dot.Width = 8;
                dot.Height = 8;
                dot.Fill = dotFill;
                dot.Stroke = Brushes.White;
                dot.StrokeThickness = 2;
                
                Canvas.SetLeft(dot, x - 4);
                Canvas.SetTop(dot, y - 4);
                
                ChartCanvas.Children.Add(dot);
            }
        }

        // 窗口拖动
        private void TitleBar_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ClickCount == 2)
            {
                MaximizeButton_Click(sender, e);
            }
            else
            {
                DragMove();
            }
        }

        // 最小化
        private void MinimizeButton_Click(object sender, RoutedEventArgs e)
        {
            WindowState = WindowState.Minimized;
        }

        // 最大化/还原
        private void MaximizeButton_Click(object sender, RoutedEventArgs e)
        {
            if (WindowState == WindowState.Maximized)
            {
                WindowState = WindowState.Normal;
            }
            else
            {
                WindowState = WindowState.Maximized;
            }
        }

        // 关闭窗口 - 带动画
        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            // 创建关闭动画
            var duration = TimeSpan.FromMilliseconds(200);
            var easing = new QuadraticEase { EasingMode = EasingMode.EaseIn };

            // 设置变换原点为中心
            RenderTransformOrigin = new Point(0.5, 0.5);

            // 设置 RenderTransform
            var transformGroup = new TransformGroup();
            var scaleTransform = new ScaleTransform(1, 1);
            var translateTransform = new TranslateTransform(0, 0);
            transformGroup.Children.Add(scaleTransform);
            transformGroup.Children.Add(translateTransform);
            RenderTransform = transformGroup;

            // 淡出动画
            var fadeOut = new DoubleAnimation(1, 0, duration) { EasingFunction = easing };
            
            // 缩小动画
            var scaleX = new DoubleAnimation(1, 0.95, duration) { EasingFunction = easing };
            var scaleY = new DoubleAnimation(1, 0.95, duration) { EasingFunction = easing };
            
            // 上移动画 (模拟窗口飞走的效果)
            var translateY = new DoubleAnimation(0, -20, duration) { EasingFunction = easing };

            // 动画完成后关闭窗口
            fadeOut.Completed += (s, args) => Close();

            // 启动动画
            BeginAnimation(OpacityProperty, fadeOut);
            scaleTransform.BeginAnimation(ScaleTransform.ScaleXProperty, scaleX);
            scaleTransform.BeginAnimation(ScaleTransform.ScaleYProperty, scaleY);
            translateTransform.BeginAnimation(TranslateTransform.YProperty, translateY);
        }
        
        // 主题切换
        private void ThemeButton_Click(object sender, RoutedEventArgs e)
        {
            _currentThemeIndex = (_currentThemeIndex + 1) % _themes.Length;
            ApplyTheme(_themes[_currentThemeIndex]);
            ShowThemeNameBadge(_themes[_currentThemeIndex]);
        }
        
        private void ShowThemeNameBadge(ThemeConfig theme)
        {
            // 更新主题名称显示
            if (FindName("ThemeNameBadge") is Border badge && FindName("ThemeNameText") is TextBlock nameText)
            {
                nameText.Text = theme.Name;
                
                // 更新徽章背景色
                badge.Background = new LinearGradientBrush(
                    new GradientStopCollection
                    {
                        new GradientStop(theme.AccentStart, 0),
                        new GradientStop(theme.AccentEnd, 1)
                    },
                    new Point(0, 0),
                    new Point(1, 1)
                );
                
                // 显示徽章
                badge.Visibility = Visibility.Visible;
                
                // 2秒后自动隐藏
                var timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(2) };
                timer.Tick += (s, args) =>
                {
                    badge.Visibility = Visibility.Collapsed;
                    timer.Stop();
                };
                timer.Start();
            }
        }
        
        private void ApplyTheme(ThemeConfig theme)
        {
            // 使用 Dispatcher 异步执行主题更新，避免阻塞UI
            Dispatcher.BeginInvoke(System.Windows.Threading.DispatcherPriority.Background, new Action(() =>
            {
                ApplyThemeCore(theme);
            }));
        }
        
        private void ApplyThemeCore(ThemeConfig theme)
        {
            // 更新主题图标和提示
            ThemeIcon.Text = theme.Icon;
            ThemeButton.ToolTip = $"当前: {theme.Name} - 点击切换";
            
            // 创建常用的画笔并冻结以提高性能
            var accentGradient = new LinearGradientBrush(
                new GradientStopCollection
                {
                    new GradientStop(theme.AccentStart, 0),
                    new GradientStop(theme.AccentMiddle, 0.5),
                    new GradientStop(theme.AccentEnd, 1)
                },
                new Point(0, 0),
                new Point(1, 1)
            );
            accentGradient.Freeze();
            
            var cardGradient = new LinearGradientBrush(
                new GradientStopCollection
                {
                    new GradientStop(theme.CardBackground, 0),
                    new GradientStop(theme.PrimaryLight, 0.5),
                    new GradientStop(theme.PrimaryMedium, 1)
                },
                new Point(0, 0),
                new Point(1, 1)
            );
            cardGradient.Freeze();
            
            // 更新命名控件 (只更新有名称的关键控件)
            UpdateNamedControls(theme, accentGradient, cardGradient);
            
            // 查找主容器并更新背景
            if (this.Content is Border mainBorder)
            {
                // 更新主背景
                var mainBg = new LinearGradientBrush(
                    new GradientStopCollection
                    {
                        new GradientStop(theme.BackgroundStart, 0),
                        new GradientStop(theme.PrimaryLight, 0.3),
                        new GradientStop(theme.PrimaryMedium, 0.7),
                        new GradientStop(theme.BackgroundEnd, 1)
                    },
                    new Point(0, 0),
                    new Point(1, 1)
                );
                mainBg.Freeze();
                mainBorder.Background = mainBg;
                
                // 更新边框颜色
                var borderBrush = new SolidColorBrush(theme.BorderAccent);
                borderBrush.Freeze();
                mainBorder.BorderBrush = borderBrush;
                
                // 只更新侧边栏，不递归遍历所有控件
                UpdateSidebar(theme);
                
                // 更新导航项样式资源
                UpdateNavItemResources(theme);
                
                // 更新图表颜色
                UpdateChart(theme);
            }
        }
        
        private void UpdateSidebar(ThemeConfig theme)
        {
            // 通过名称查找侧边栏，如果有的话
            if (FindName("SidebarPanel") is Border sidebar)
            {
                var sidebarBg = new LinearGradientBrush(
                    new GradientStopCollection
                    {
                        new GradientStop(theme.SidebarStart, 0),
                        new GradientStop(theme.PrimaryLight, 0.3),
                        new GradientStop(theme.PrimaryMedium, 0.6),
                        new GradientStop(theme.SidebarEnd, 1)
                    },
                    new Point(0, 0),
                    new Point(1, 1)
                );
                sidebarBg.Freeze();
                sidebar.Background = sidebarBg;
            }
        }
        
        private void UpdateNavItemResources(ThemeConfig theme)
        {
            // 更新悬停背景
            var hoverBg = new SolidColorBrush(Color.FromArgb(24, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            hoverBg.Freeze();
            Resources["NavItemHoverBackground"] = hoverBg;
            
            // 更新悬停边框
            var hoverBorder = new SolidColorBrush(Color.FromArgb(48, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            hoverBorder.Freeze();
            Resources["NavItemHoverBorder"] = hoverBorder;
            
            // 更新窗口按钮悬停背景
            var winBtnHover = new SolidColorBrush(Color.FromArgb(32, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            winBtnHover.Freeze();
            Resources["WindowButtonHoverBackground"] = winBtnHover;
            
            // 更新关闭按钮悬停背景
            var closeBtnHover = new SolidColorBrush(Color.FromArgb(255, 255, 143, 171)); // 保持红色系但稍微柔和
            if (theme.Name == "薄荷霜" || theme.Name == "晨曦蓝")
            {
                // 冷色调主题使用稍微不同的红色
                closeBtnHover = new SolidColorBrush(Color.FromArgb(255, 255, 120, 150));
            }
            closeBtnHover.Freeze();
            Resources["CloseButtonHoverBackground"] = closeBtnHover;
            
            // 更新阴影颜色
            Resources["NavItemShadowColor"] = theme.ShadowColor;
            
            // 更新选中背景
            var checkedBg = new LinearGradientBrush(
                new GradientStopCollection
                {
                    new GradientStop(theme.AccentStart, 0),
                    new GradientStop(theme.AccentMiddle, 0.5),
                    new GradientStop(theme.AccentEnd, 1)
                },
                new Point(0, 0),
                new Point(1, 1)
            );
            checkedBg.Freeze();
            Resources["NavItemCheckedBackground"] = checkedBg;
            
            // 更新全局主题资源
            Resources["ThemeShadowColor"] = theme.ShadowColor;
            
            // 主题边框画笔
            var themeBorderBrush = new SolidColorBrush(Color.FromArgb(32, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            themeBorderBrush.Freeze();
            Resources["ThemeBorderBrush"] = themeBorderBrush;
            
            var themeBorderBrushLight = new SolidColorBrush(Color.FromArgb(21, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            themeBorderBrushLight.Freeze();
            Resources["ThemeBorderBrushLight"] = themeBorderBrushLight;
            
            // 主题强调色渐变
            var themeAccentGradient = new LinearGradientBrush(
                new GradientStopCollection
                {
                    new GradientStop(theme.AccentStart, 0),
                    new GradientStop(theme.AccentMiddle, 0.5),
                    new GradientStop(theme.AccentEnd, 1)
                },
                new Point(0, 0),
                new Point(1, 1)
            );
            themeAccentGradient.Freeze();
            Resources["ThemeAccentGradient"] = themeAccentGradient;
            
            // 卡片背景渐变
            var themeCardBackground = new LinearGradientBrush(
                new GradientStopCollection
                {
                    new GradientStop(theme.CardBackground, 0),
                    new GradientStop(theme.PrimaryLight, 0.5),
                    new GradientStop(theme.PrimaryMedium, 1)
                },
                new Point(0, 0),
                new Point(1, 1)
            );
            themeCardBackground.Freeze();
            Resources["ThemeCardBackground"] = themeCardBackground;
            
            // 用户信息区域背景
            var themeUserInfoBackground = new LinearGradientBrush(
                new GradientStopCollection
                {
                    new GradientStop(Colors.White, 0),
                    new GradientStop(theme.PrimaryLight, 0.5),
                    new GradientStop(theme.PrimaryMedium, 1)
                },
                new Point(0, 0),
                new Point(1, 1)
            );
            themeUserInfoBackground.Freeze();
            Resources["ThemeUserInfoBackground"] = themeUserInfoBackground;
            
            // 底部操作区背景（使用更深的主题色）
            var themeBottomActionBackground = new LinearGradientBrush(
                new GradientStopCollection
                {
                    new GradientStop(theme.AccentStart, 0),
                    new GradientStop(theme.AccentMiddle, 0.3),
                    new GradientStop(theme.AccentEnd, 0.7),
                    new GradientStop(Color.FromRgb(
                        (byte)(theme.AccentEnd.R * 0.85),
                        (byte)(theme.AccentEnd.G * 0.85),
                        (byte)(theme.AccentEnd.B * 0.85)), 1)
                },
                new Point(0, 0),
                new Point(1, 1)
            );
            themeBottomActionBackground.Freeze();
            Resources["ThemeBottomActionBackground"] = themeBottomActionBackground;
        }
        
        private void UpdateNamedControls(ThemeConfig theme, LinearGradientBrush accentGradient, LinearGradientBrush cardGradient)
        {
            // 创建可变画笔用于需要单独实例的控件
            LinearGradientBrush CreateAccentBrush()
            {
                var brush = new LinearGradientBrush(
                    new GradientStopCollection
                    {
                        new GradientStop(theme.AccentStart, 0),
                        new GradientStop(theme.AccentMiddle, 0.5),
                        new GradientStop(theme.AccentEnd, 1)
                    },
                    new Point(0, 0),
                    new Point(1, 1)
                );
                return brush;
            }
            
            LinearGradientBrush CreateCardBrush()
            {
                var brush = new LinearGradientBrush(
                    new GradientStopCollection
                    {
                        new GradientStop(theme.CardBackground, 0),
                        new GradientStop(theme.PrimaryLight, 0.5),
                        new GradientStop(theme.PrimaryMedium, 1)
                    },
                    new Point(0, 0),
                    new Point(1, 1)
                );
                return brush;
            }
            
            var accentBorderBrush = new SolidColorBrush(Color.FromArgb(60, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            var cardBorderBrush = new SolidColorBrush(Color.FromArgb(20, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            var searchBorderBrush = new SolidColorBrush(Color.FromArgb(30, theme.AccentMiddle.R, theme.AccentMiddle.G, theme.AccentMiddle.B));
            
            // 更新用户头像
            if (FindName("UserAvatar") is Border userAvatar)
            {
                userAvatar.Background = CreateAccentBrush();
                userAvatar.BorderBrush = accentBorderBrush;
                if (userAvatar.Effect is DropShadowEffect shadow)
                {
                    shadow.Color = theme.ShadowColor;
                }
            }
            
            // 更新右上角用户头像
            if (FindName("TopUserAvatar") is Border topUserAvatar)
            {
                topUserAvatar.Background = CreateAccentBrush();
                topUserAvatar.BorderBrush = accentBorderBrush;
                if (topUserAvatar.Effect is DropShadowEffect shadow)
                {
                    shadow.Color = theme.ShadowColor;
                }
            }
            
            // 更新功能按钮组容器
            if (FindName("FunctionButtonsContainer") is Border funcContainer)
            {
                funcContainer.Background = CreateCardBrush();
                funcContainer.BorderBrush = cardBorderBrush;
                if (funcContainer.Effect is DropShadowEffect shadow)
                {
                    shadow.Color = theme.ShadowColor;
                }
            }
            
            // 更新搜索框
            if (FindName("SearchBox") is Border searchBox)
            {
                searchBox.Background = CreateCardBrush();
                searchBox.BorderBrush = searchBorderBrush;
                if (searchBox.Effect is DropShadowEffect shadow)
                {
                    shadow.Color = theme.ShadowColor;
                }
            }
            
            // 更新用户信息区域
            if (FindName("UserInfoPanel") is Border userInfoPanel)
            {
                userInfoPanel.Background = new LinearGradientBrush(
                    new GradientStopCollection
                    {
                        new GradientStop(Colors.White, 0),
                        new GradientStop(theme.PrimaryLight, 0.5),
                        new GradientStop(theme.PrimaryMedium, 1)
                    },
                    new Point(0, 0),
                    new Point(1, 1)
                );
                if (userInfoPanel.Effect is DropShadowEffect shadow)
                {
                    shadow.Color = theme.ShadowColor;
                }
            }
        }
        
    }
}

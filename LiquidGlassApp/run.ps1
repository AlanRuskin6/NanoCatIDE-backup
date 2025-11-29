# Liquid Glass App 构建和运行脚本

# 复制 GIF 文件到 Assets 目录
$sourceGif = "c:\Users\joyto\Desktop\design\d0c438b0de1b4f779ced045eeac32c175127bf0a6930-YP8Y17_fw1200.gif"
$targetDir = "c:\Users\joyto\Desktop\design\LiquidGlassApp\Assets"

if (Test-Path $sourceGif) {
    Copy-Item $sourceGif -Destination $targetDir -Force
    Write-Host "GIF 文件已复制到 Assets 目录" -ForegroundColor Green
}

# 构建并运行项目
Set-Location "c:\Users\joyto\Desktop\design\LiquidGlassApp"
dotnet build
if ($LASTEXITCODE -eq 0) {
    Write-Host "构建成功！正在启动应用..." -ForegroundColor Green
    dotnet run
} else {
    Write-Host "构建失败，请检查错误信息" -ForegroundColor Red
}

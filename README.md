# wrety

[![Build Android APK](https://github.com/a10140/wrety/actions/workflows/build-apk.yml/badge.svg)](https://github.com/a10140/wrety/actions/workflows/build-apk.yml)

WREP AI Console - Android Application

一个基于Kivy框架的AI聊天应用，支持用户认证、会话管理和本地数据存储。

## 🚀 云端一键打包（推荐）

**无需任何环境配置，直接在GitHub云端构建APK！**

### 立即在云端打包：

1. 访问 [Actions 工作流页面](https://github.com/a10140/wrety/actions/workflows/build-apk.yml)
2. 点击 **"Run workflow"** 按钮
3. 选择分支（如 `main`）并点击绿色的 **"Run workflow"**
4. 等待20-30分钟（首次）或5-10分钟（后续）
5. 在 **"Artifacts"** 部分下载 `wrep-android-apk`

📖 详细说明请查看：[云端打包完整指南](CLOUD_BUILD.md)

## 快速开始

### 方法一：从GitHub Actions下载APK（最简单，无需构建）

每次代码推送时，GitHub Actions会自动构建APK。你可以：

1. 访问仓库的 [Actions](https://github.com/a10140/wrety/actions) 页面
2. 选择最新的成功构建（绿色✓）
3. 在 "Artifacts" 部分下载 `wrep-android-apk`
4. 解压后将APK传输到Android设备安装

或者在 [Releases](https://github.com/a10140/wrety/releases) 页面直接下载正式版本的APK。

### 方法二：使用构建脚本（本地构建）

```bash
# 克隆仓库
git clone https://github.com/a10140/wrety.git
cd wrety

# 运行构建脚本
./build.sh
```

### 方法三：手动构建

#### 前置要求
- Linux系统（推荐Ubuntu 20.04+）
- Python 3.8+
- Buildozer

#### 安装步骤

1. 安装系统依赖：
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev
```

2. 安装Python工具：
```bash
pip3 install --upgrade buildozer cython==0.29.33
```

3. 构建APK：
```bash
buildozer android debug
```

4. 安装到设备：
```bash
# 自动安装并运行
buildozer android deploy run

# 或手动安装：APK文件位于 bin/ 目录
# 文件名：wrep-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

## 测试

运行测试脚本验证应用程序：
```bash
./test_app.py
```

## 功能特性

✅ 用户认证系统（登录/注册）  
✅ 多会话聊天管理  
✅ 本地SQLite数据库存储  
✅ 简洁直观的用户界面  
✅ 针对Android优化的稳定性能  
✅ 消息历史记录  
✅ 会话管理  

## 文件说明

- **main.py** - Kivy主应用程序（Android核心）
- **buildozer.spec** - Android构建配置文件
- **build.sh** - 自动化构建脚本
- **test_app.py** - 应用程序测试脚本
- **requirements.txt** - Python依赖列表
- **api.php** - PHP后端API（可选，用于服务器部署）
- **style.html** - Web界面（可选替代方案）
- **wrep_db.sql** - MySQL数据库架构（服务器使用）

## 架构说明

本项目提供三种部署方式：

### 1. Android应用（main.py + buildozer）
- 使用Kivy框架构建
- 本地SQLite数据库
- 完全离线运行
- **这是主要的推荐方式**

### 2. Web应用（style.html + api.php）
- 基于HTML/CSS/JavaScript
- 需要PHP服务器
- MySQL数据库
- 适合在线服务

### 3. 混合部署
- Android应用作为客户端
- PHP API作为后端服务
- 支持跨设备数据同步

## 构建说明

### APK文件输出
构建成功后，APK文件将位于：
```
bin/wrep-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

### 支持的Android版本
- 最低API：21（Android 5.0 Lollipop）
- 目标API：33（Android 13）
- 架构：arm64-v8a, armeabi-v7a

### 清理构建缓存
```bash
./build.sh clean
```

或手动清理：
```bash
rm -rf .buildozer bin build
```

## 故障排除

### 问题：构建失败
- 确保所有系统依赖已正确安装
- 检查JDK版本（需要17）
- 尝试清理构建缓存后重新构建

### 问题：APK无法安装
- 确保Android设备允许安装未知来源应用
- 检查设备架构是否支持（arm64-v8a或armeabi-v7a）

### 问题：应用闪退
- 查看logcat日志：`adb logcat | grep python`
- 检查数据库权限

## 开发

### 修改应用后重新构建
```bash
# 清理并重新构建
./build.sh clean
./build.sh
```

### 调试
```bash
# 查看实时日志
buildozer android adb -- logcat
```

## 许可证

本项目开源，供学习和研究使用。

## 贡献

欢迎提交Issue和Pull Request！

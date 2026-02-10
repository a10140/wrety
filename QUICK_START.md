# WREP AI Console - 快速构建指南

## 一键构建APK

### 步骤 1: 准备环境（仅首次需要）

在Linux系统（推荐Ubuntu）上运行：

```bash
# 安装系统依赖
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 安装Python构建工具
pip3 install --upgrade buildozer cython==0.29.33
```

### 步骤 2: 构建APK

```bash
# 克隆项目（如果还没有）
git clone https://github.com/a10140/wrety.git
cd wrety

# 运行构建脚本
./build.sh

# 首次构建可能需要20-30分钟
# 之后的构建会快很多
```

### 步骤 3: 获取APK

构建完成后，APK文件位于：
```
bin/wrep-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

### 步骤 4: 安装到手机

#### 方法A：自动安装（推荐）
```bash
# 连接手机并启用USB调试
buildozer android deploy run
```

#### 方法B：手动安装
1. 将APK文件传输到手机
2. 在手机上找到APK文件
3. 点击安装（可能需要允许安装未知来源应用）

## 验证构建

在构建前，可以运行测试脚本：
```bash
./test_app.py
```

看到 "✅ ALL TESTS PASSED!" 表示一切正常。

## 常见问题

**Q: 构建时间太长？**  
A: 首次构建需要下载Android SDK和NDK，需要20-30分钟。之后的构建只需要几分钟。

**Q: 构建失败？**  
A: 运行 `./build.sh clean` 清理后重试。

**Q: 手机无法安装？**  
A: 检查手机设置中是否允许安装未知来源应用。

**Q: 需要什么配置的电脑？**  
A: 推荐8GB以上内存，20GB以上磁盘空间。

## 需要帮助？

查看完整文档：[README.md](README.md)

创建Issue：https://github.com/a10140/wrety/issues

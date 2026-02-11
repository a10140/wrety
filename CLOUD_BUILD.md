# 云端自动打包APK指南

本项目已配置GitHub Actions自动化构建，可以在GitHub的云端服务器上自动打包APK，**无需本地环境**。

## 方法一：手动触发云端打包（推荐）

1. 访问 [GitHub Actions 工作流页面](https://github.com/a10140/wrety/actions/workflows/build-apk.yml)

2. 点击右上角的 **"Run workflow"** 按钮

3. 在弹出的对话框中：
   - 选择要构建的分支（例如 `main` 或 `copilot/build-apk-package`）
   - 点击绿色的 **"Run workflow"** 按钮

4. 等待构建完成（首次约20-30分钟，后续约5-10分钟）

5. 构建完成后，在该工作流运行页面底部的 **"Artifacts"** 部分下载 `wrep-android-apk`

## 方法二：自动触发（推送代码时）

当您推送代码到以下分支时，会自动触发云端打包：
- `main`
- `master`
- `develop`

例如：
```bash
git push origin main
```

推送后，访问 [Actions 页面](https://github.com/a10140/wrety/actions) 查看构建进度。

## 方法三：创建Release自动打包

1. 在GitHub上创建新的 Release
2. 工作流会自动运行
3. APK会自动附加到Release中，可以直接下载

创建Release步骤：
1. 访问仓库的 [Releases 页面](https://github.com/a10140/wrety/releases)
2. 点击 **"Draft a new release"**
3. 填写版本号（如 `v1.0.0`）和说明
4. 点击 **"Publish release"**
5. 等待APK自动构建并附加到Release

## 获取构建的APK

### 从Actions Artifacts下载：
1. 访问 [Actions](https://github.com/a10140/wrety/actions)
2. 选择最近成功的工作流运行（绿色✓）
3. 滚动到页面底部的 **"Artifacts"** 部分
4. 点击 `wrep-android-apk` 下载ZIP文件
5. 解压ZIP获取APK文件

### 从Release下载：
1. 访问 [Releases](https://github.com/a10140/wrety/releases)
2. 选择最新版本
3. 在 **"Assets"** 部分直接下载APK文件

## 构建状态查看

在README.md顶部有构建状态徽章：

[![Build Android APK](https://github.com/a10140/wrety/actions/workflows/build-apk.yml/badge.svg)](https://github.com/a10140/wrety/actions/workflows/build-apk.yml)

- ✅ 绿色：构建成功
- ❌ 红色：构建失败
- 🟡 黄色：构建进行中

## 优势

✅ **零环境配置** - 无需安装Android SDK、NDK等工具  
✅ **自动化** - 推送代码即自动构建  
✅ **云端资源** - 使用GitHub提供的构建服务器  
✅ **快速获取** - 构建完成后直接下载APK  
✅ **版本管理** - Release自动附加APK  

## 注意事项

1. **首次构建时间较长**：首次构建需要下载Android SDK/NDK，大约需要20-30分钟
2. **后续构建更快**：由于缓存，后续构建只需5-10分钟
3. **Artifacts保留期**：Actions产生的APK artifacts保留30天
4. **Release永久保存**：通过Release发布的APK会永久保存

## 故障排除

如果构建失败：
1. 访问失败的工作流运行页面
2. 查看详细的构建日志
3. 检查错误信息
4. 常见问题：
   - buildozer.spec配置错误
   - requirements.txt缺少依赖
   - API版本兼容性问题

## 需要帮助？

- 查看构建日志：[Actions](https://github.com/a10140/wrety/actions)
- 提交问题：[Issues](https://github.com/a10140/wrety/issues)
- 查看完整文档：[README.md](README.md)

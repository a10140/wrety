# GitHub Actions Workflow - Build APK

This workflow automatically builds an Android APK for the WREP AI Console application.

## Triggers

The workflow runs on:
- **Push** to `main`, `master`, or `develop` branches
- **Pull requests** to `main`, `master`, or `develop` branches
- **Release** creation
- **Manual trigger** via workflow_dispatch

## What it does

1. **Setup Environment**
   - Ubuntu latest runner
   - Python 3.10
   - JDK 17
   - Required system dependencies for Android development

2. **Caching**
   - Caches buildozer global directory (~/.buildozer)
   - Caches local buildozer directory (.buildozer)
   - Significantly speeds up subsequent builds

3. **Build Process**
   - Installs buildozer and dependencies
   - Runs `buildozer android debug` to create APK
   - Lists built files

4. **Artifact Upload**
   - Uploads APK as GitHub Actions artifact (30 days retention)
   - For releases: Automatically attaches APK to the release

## Using the Built APK

### From GitHub Actions

1. Go to the [Actions tab](https://github.com/a10140/wrety/actions)
2. Click on the latest successful workflow run (green checkmark)
3. Scroll down to "Artifacts" section
4. Download `wrep-android-apk`
5. Unzip the downloaded file to get the APK

### From Releases

When a new release is created, the APK is automatically attached to the release page.

## Build Time

- **First build**: 20-30 minutes (downloads SDK, NDK, etc.)
- **Subsequent builds**: 5-10 minutes (with caching)

## Troubleshooting

If the build fails:
1. Check the workflow logs in the Actions tab
2. Common issues:
   - Buildozer spec configuration errors
   - Missing dependencies in requirements.txt
   - API/NDK version compatibility issues

## Manual Build

To test the workflow locally or build manually:

```bash
# Install dependencies (Ubuntu)
sudo apt-get install -y git zip unzip autoconf libtool pkg-config \
  zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake \
  libffi-dev libssl-dev build-essential ccache

# Install Python tools
pip install --upgrade buildozer cython==0.29.33

# Build APK
buildozer android debug
```

The APK will be in the `bin/` directory.

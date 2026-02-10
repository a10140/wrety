#!/bin/bash
# Build script for WREP AI Console Android APK

set -e

echo "========================================"
echo "WREP AI Console - APK Builder"
echo "========================================"
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer is not installed!"
    echo ""
    echo "Please install buildozer first:"
    echo "  sudo apt update"
    echo "  sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev"
    echo "  pip3 install --upgrade buildozer cython==0.29.33"
    exit 1
fi

echo "✓ Buildozer found"
echo ""

# Clean previous builds (optional)
if [ "$1" = "clean" ]; then
    echo "🧹 Cleaning previous builds..."
    rm -rf .buildozer bin build
    echo "✓ Clean complete"
    echo ""
fi

# Build APK
echo "🔨 Building APK..."
buildozer android debug

echo ""
echo "========================================"
echo "✅ Build Complete!"
echo "========================================"
echo ""
echo "APK location: bin/wrep-1.0-arm64-v8a_armeabi-v7a-debug.apk"
echo ""
echo "To install on device:"
echo "  buildozer android deploy run"
echo ""
echo "Or transfer the APK file to your Android device"
echo "and install it manually."
echo ""

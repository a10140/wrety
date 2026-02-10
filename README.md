# wrety

WREP AI Console - Android Application

## Build APK

### Prerequisites
- Linux system (Ubuntu recommended)
- Python 3.8+
- Buildozer installed

### Installation Steps

1. Install buildozer and dependencies:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --upgrade buildozer cython==0.29.33
```

2. Clone this repository:
```bash
git clone https://github.com/a10140/wrety.git
cd wrety
```

3. Build the APK:
```bash
buildozer android debug
```

4. The APK will be generated in `bin/` directory as `wrep-1.0-arm64-v8a_armeabi-v7a-debug.apk`

### Install on Android Device

```bash
buildozer android deploy run
```

Or manually transfer the APK from `bin/` directory to your Android device and install it.

## Features

- User authentication (login/register)
- Chat sessions management
- Local SQLite database storage
- Clean and intuitive UI
- Stable Android performance

## Files

- **main.py** - Main Kivy application
- **buildozer.spec** - Android build configuration
- **api.php** - PHP backend API (for server deployment)
- **style.html** - Web interface alternative
- **wrep_db.sql** - MySQL database schema (for server)

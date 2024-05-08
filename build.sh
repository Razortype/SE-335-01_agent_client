#!/bin/bash

# Check if EMAIL and PASSWORD are set
if [ -z "$EMAIL" ] || [ -z "$PASSWORD" ]; then
    echo "Error: EMAIL and PASSWORD must be set." >&2
    exit 1
fi

# Set PROFILE to "product" by default if it's not set
if [ -z "$PROFILE" ]; then
    PROFILE="product"
fi

# Get the platform from the command-line arguments
platform=$1

# Check if dist directory exists, create it if not
if [ ! -d "dist" ]; then
    mkdir dist
fi

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Error: PyInstaller is not installed. Please install it using 'pip install pyinstaller'." >&2
    exit 1
fi

# If platform is not provided, default to the current system's platform
if [ -z "$platform" ]; then
    platform=$(uname)
fi

case $platform in
    "Windows"|"MINGW"*|"MSYS"*|"CYGWIN"*)
        platform="win"
        extension=".exe"
        ;;
    "Darwin")
        platform="mac"
        extension=""
        ;;
    "Linux")
        platform="linux"
        extension=""
        ;;
    *)
        echo "Invalid platform. Please enter 'Windows', 'macOS', or 'Linux'."
        exit 1
        ;;
esac

# Ask for executable file name
read -p "Enter the desired name of your executable (without extension): " executable_name

# Replace 'src/main.py' with the path to your main script
EMAIL=$EMAIL PASSWORD=$PASSWORD pyinstaller src/main.py --distpath dist --onefile --platform $platform

# Move the executable with the desired name and extension
mv dist/main "dist/$executable_name$extension"

# Remove build directory
rm -rf build

echo "Build completed successfully."
#!/bin/bash

# Check if dist directory exists, create it if not
if [ ! -d "dist" ]; then
    mkdir dist
fi

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Error: PyInstaller is not installed. Please install it using 'pip install pyinstaller'." >&2
    exit 1
fi

# Select the operating system
options=("Windows" "macOS" "Linux" "Quit")
echo "Select the operating system for the executable:"
select os in "${options[@]}"; do
    case $os in
        "Windows")
            platform="win"
            extension=".exe"
            break
            ;;
        "macOS")
            platform="mac"
            extension=""
            break
            ;;
        "Linux")
            platform="linux"
            extension=""
            break
            ;;
        "Quit")
            echo "Exiting..."
            exit 0
            ;;
        *) echo "Invalid option";;
    esac
done

# Ask for executable file name
read -p "Enter the desired name of your executable (without extension): " executable_name

# Replace 'src/main.py' with the path to your main script
pyinstaller src/main.py --distpath dist --onefile --platform $platform

# Move the executable with the desired name and extension
mv dist/main "dist/$executable_name$extension"

# Remove build directory
rm -rf build

echo "Build completed successfully."

import os
import subprocess
import sys
import shutil

def build_exe():
    print("--- Starting JARVIS EXE Build Process ---")
    
    # 1. Verify requirements
    try:
        import PyInstaller
        import customtkinter
    except ImportError as e:
        print(f"Error: {e}")
        print("Please run: pip install pyinstaller customtkinter")
        return

    # 2. Get CustomTkinter path for assets
    ctk_path = os.path.dirname(customtkinter.__file__)
    print(f"Found CustomTkinter at: {ctk_path}")

    # 3. Construct PyInstaller command
    # --noconsole: Don't show terminal window
    # --onefile: Bundle into single .exe
    # --add-data: Include CustomTkinter assets (path_to_ctk;customtkinter)
    # --add-data: Include the src directory
    
    # Use 'py -m PyInstaller' instead of 'pyinstaller' to ensure it's found
    command = [
        "py", "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name", "JARVIS",
        f"--add-data={ctk_path}{os.pathsep}customtkinter",
        f"--add-data=src{os.pathsep}src",
        "main.py"
    ]

    print(f"Running command: {' '.join(command)}")
    
    try:
        subprocess.run(command, check=True)
        print("\nSUCCESS! Your executable is in the 'dist' folder.")
    except subprocess.CalledProcessError:
        print("\nERROR: Build failed. Check the output above.")
    except FileNotFoundError:
        print("\nERROR: 'pyinstaller' command not found. Ensure it is in your PATH.")

if __name__ == "__main__":
    build_exe()

import subprocess
import sys
import os
import json
import shutil
import glob

def create_default_files():
    """Create default data files if they don't exist"""
    
    # Create default preferences file
    if not os.path.exists("preferences.txt"):
        default_prefs = {
            "theme": {
                "background": "dark",
                "button_color": "blue",
                "priority_color": "orange",
                "complete_color": "green",
                "delete_color": "red",
                "edit_color": "blue",
                "accent_color": "orange",
                "text_color": "white",
                "header_color": "red"
            },
            "fonts": {
                "title": ("Arial", 24),
                "header": ("Arial", 12),
                "task": ("Arial", 11),
                "button": ("Arial", 10),
                "label": ("Arial", 10)
            },
            "sizes": {
                "window": "600x600",
                "button_width": 120,
                "entry_width": 300,
                "icon_width": 30,
                "icon_height": 25
            }
        }
        with open("preferences.txt", "w") as f:
            json.dump(default_prefs, f, indent=4)
        print("✅ Created default preferences.txt")
    
    # Create empty tasks file
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as f:
            pass
        print("✅ Created empty tasks.txt")
    
    # Create default categories file
    if not os.path.exists("categories.txt"):
        with open("categories.txt", "w") as f:
            f.write("General\n")
        print("✅ Created default categories.txt")

def build_executable():
    """Build the To-Do List application as an executable"""
    
    print("🚀 Building To-Do List Application...")
    print("=" * 50)
    
    # Create default files first
    create_default_files()
    
    # PyInstaller command
    command = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # Hide console window
        "--name=ToDo-List",             # Name of the executable
        "--clean",                      # Clean cache
        "main.py"
    ]
    
    # Add icon if it exists
    if os.path.exists("app.ico"):
        command.insert(-1, "--icon=app.ico")
        print("📎 Using custom icon: app.ico")
    
    try:
        print("🔨 Running PyInstaller...")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print("\n✅ Build successful!")
        print("📁 Executable created in 'dist' folder")
        print("🎯 File: dist/ToDo-List.exe")
        print("\n📋 Next steps:")
        print("   1. Navigate to the 'dist' folder")
        print("   2. Run ToDo-List.exe")
        print("   3. The app will create its own data files on first run")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed!")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False
        
    except FileNotFoundError:
        print("❌ PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        return False

def clean_build_files():
    """Clean up build artifacts"""
    
    artifacts_dirs = ["build", "__pycache__"]
    artifacts_files = glob.glob("*.spec")
    
    # Remove directories
    for artifact in artifacts_dirs:
        if os.path.exists(artifact):
            shutil.rmtree(artifact)
            print(f"🧹 Removed directory: {artifact}")
    
    # Remove .spec files
    for artifact in artifacts_files:
        if os.path.exists(artifact):
            os.remove(artifact)
            print(f"🧹 Removed file: {artifact}")

if __name__ == "__main__":
    success = build_executable()
    
    if success:
        clean_choice = input("\n🧹 Clean build artifacts? (y/n): ").lower()
        if clean_choice == 'y':
            clean_build_files()
    
    print("\n🎉 Build process complete!")
    input("Press Enter to exit...")

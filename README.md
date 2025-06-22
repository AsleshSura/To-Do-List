# To-Do List Application

A modern, feature-rich desktop To-Do List application built with Python and CustomTkinter.

## Features

- ✅ Add, edit, and delete tasks
- 🌟 Priority marking with star system
- 📅 Due date and time support
- 🏷️ Custom categories
- 🔍 Search and filter functionality
- 🎨 Customizable themes and preferences
- 💾 Persistent data storage

## For End Users

1. Download `ToDo-List.exe` from the releases
2. Double-click to run - no installation needed!
3. The app will create its data files automatically

## For Developers

### Requirements
- Python 3.8+
- pip

### Quick Start
1. Clone this repository
2. Run `setup_and_build.bat` (Windows) or install manually:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

### Building Executable
```bash
# Automatic build
python build_exe.py

# Or use batch file
setup_and_build.bat

# Create release packages
create_release.bat
```

## File Structure
- `main.py` - Main application code
- `requirements.txt` - Python dependencies
- `build_exe.py` - Build script for creating executable
- `preferences.txt` - User preferences (auto-generated)
- `tasks.txt` - Task data (auto-generated)
- `categories.txt` - Custom categories (auto-generated)

## License
MIT License - see LICENSE file for details

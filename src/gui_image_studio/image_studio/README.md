# Image Studio - Refactored Structure

This is a refactored version of the Image Studio application, organized into a modular structure for better maintainability.

## Structure Overview

```
image_studio/
├── __init__.py                 # Package initialization
├── main_app.py                 # Main application class
├── README.md                   # This file
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── image_manager.py        # Image storage and management
│   ├── drawing_tools.py        # Drawing tools and settings
│   └── canvas_manager.py       # Canvas operations and display
├── ui/                         # User interface components
│   ├── __init__.py
│   ├── menu.py                 # Menu bar setup
│   ├── panels.py               # Panel setup (left, center, right)
│   └── dialogs.py              # Dialog windows
└── utils/                      # Utility modules
    ├── __init__.py
    └── tooltip.py              # Tooltip functionality
```

## Key Components

### Core Modules

- **`ImageManager`**: Handles image storage, previews, and basic operations
- **`DrawingToolsManager`**: Manages drawing tools, brush settings, and cursors
- **`CanvasManager`**: Handles canvas operations, drawing, and display

### UI Modules

- **`MenuManager`**: Sets up the application menu bar
- **`PanelManager`**: Configures the three-pane layout (tools, canvas, properties)
- **Dialog classes**: Various dialog windows (ImageSizeDialog, CodePreviewWindow, HelpWindow)

### Main Application

- **`EnhancedImageDesignerGUI`**: Main application class that coordinates all components

## Benefits of Refactoring

1. **Separation of Concerns**: Each module has a specific responsibility
2. **Easier Maintenance**: Changes to one feature don't affect others
3. **Better Testing**: Individual components can be tested in isolation
4. **Code Reusability**: Components can be reused in other projects
5. **Cleaner Architecture**: Clear dependencies and interfaces

## Usage

### Running the Application

#### Option 1: Use the standalone entry point (recommended)
```bash
python run_image_studio.py
```

#### Option 2: Use the module entry point
```bash
python src/gui_image_studio/image_studio_refactored.py
```

#### Option 3: Import and run programmatically
```python
import sys
import os
sys.path.insert(0, 'src')
from gui_image_studio.image_studio.main_app import main
main()
```

### Extending the Application

To add new functionality:

1. **New drawing tool**: Extend `DrawingToolsManager` in `core/drawing_tools.py`
2. **New dialog**: Add to `ui/dialogs.py`
3. **New panel feature**: Modify `ui/panels.py`
4. **New menu item**: Update `ui/menu.py`

## Migration from Original

The original `image_studio.py` file has been backed up as `image_studio.py.backup`. The refactored version maintains the same functionality while providing a cleaner structure.

### Key Changes

- Single large class split into focused managers
- UI setup separated from business logic
- Better error handling and resource management
- Improved code organization and documentation

## Dependencies

The refactored version maintains the same dependencies as the original:
- `tkinter` (built-in)
- `PIL` (Pillow)
- `threepanewindows`
- Optional: `psutil` for memory monitoring

## Future Improvements

The modular structure makes it easier to implement:
- Plugin system for custom tools
- Theme support
- Better undo/redo functionality
- Advanced image filters
- Export to different formats
- Collaborative editing features

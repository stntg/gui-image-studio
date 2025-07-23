"""
Drawing tools for Image Studio.

This module automatically discovers and registers all available drawing tools.
"""

import glob
import importlib
import os

from .base_tool import BaseTool, ToolRegistry, register_tool


def _auto_discover_tools():
    """Automatically discover and import all tool files in the tools directory."""
    # Get the directory where this __init__.py file is located
    tools_dir = os.path.dirname(__file__)

    # Find all Python files that end with '_tool.py' (excluding base_tool.py and __init__.py)
    tool_files = glob.glob(os.path.join(tools_dir, "*_tool.py"))

    imported_tools = []

    for tool_file in tool_files:
        # Get the filename without path and extension
        filename = os.path.basename(tool_file)
        module_name = filename[:-3]  # Remove .py extension

        # Skip base_tool.py
        if module_name == "base_tool":
            continue

        try:
            # Import the module dynamically
            module = importlib.import_module(f".{module_name}", package=__name__)
            imported_tools.append(module_name)
            print(f"Auto-discovered and imported tool: {module_name}")
        except ImportError as e:
            print(f"Warning: Failed to import tool {module_name}: {e}")
        except Exception as e:
            print(f"Warning: Error loading tool {module_name}: {e}")

    return imported_tools


# Automatically discover and import all tools
_discovered_tools = _auto_discover_tools()

# Export the registry and base classes
__all__ = ["BaseTool", "ToolRegistry", "register_tool"] + _discovered_tools

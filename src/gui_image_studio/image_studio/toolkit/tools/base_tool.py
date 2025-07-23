"""
Base tool interface for drawing tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

from PIL import Image, ImageDraw


class BaseTool(ABC):
    """Base class for all drawing tools."""

    def __init__(self, name: str, display_name: str, cursor: str = "crosshair"):
        self.name = name
        self.display_name = display_name
        self.cursor = cursor
        self.settings = {}

    @abstractmethod
    def get_icon(self) -> str:
        """Return the icon name/path for this tool."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Return a description of what this tool does."""
        pass

    @abstractmethod
    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click events."""
        pass

    @abstractmethod
    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag events (mouse move while pressed)."""
        pass

    @abstractmethod
    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release events (for shapes and lines)."""
        pass

    def supports_preview(self) -> bool:
        """Return True if this tool supports shape preview."""
        return False

    def supports_click(self) -> bool:
        """Return True if this tool responds to single clicks."""
        return True  # Most tools support clicks

    def supports_drag(self) -> bool:
        """Return True if this tool responds to drag operations."""
        return True  # Most tools support dragging

    def supports_release(self) -> bool:
        """Return True if this tool uses mouse release events (shapes)."""
        return self.supports_preview()  # Tools with preview typically use release

    def requires_text_input(self) -> bool:
        """Return True if this tool requires text input."""
        return False

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, zoom: float, **kwargs
    ) -> Optional[int]:
        """Create a preview shape on the canvas. Return canvas item ID."""
        return None

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration for this tool."""
        return None

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize tool settings."""
        return settings

    def get_cursor_for_size(self, size: int) -> str:
        """Get cursor based on tool size (for size-dependent cursors)."""
        return self.cursor


class ToolRegistry:
    """Registry for self-registering tools."""

    _tools: Dict[str, BaseTool] = {}

    @classmethod
    def register(cls, tool: BaseTool) -> None:
        """Register a tool."""
        cls._tools[tool.name] = tool

    @classmethod
    def get_tool(cls, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return cls._tools.get(name)

    @classmethod
    def get_all_tools(cls) -> Dict[str, BaseTool]:
        """Get all registered tools."""
        return cls._tools.copy()

    @classmethod
    def get_tool_names(cls) -> list:
        """Get list of all tool names."""
        return list(cls._tools.keys())


def register_tool(tool_class):
    """Decorator to automatically register a tool."""

    def wrapper(*args, **kwargs):
        tool_instance = tool_class(*args, **kwargs)
        ToolRegistry.register(tool_instance)
        return tool_instance

    return wrapper

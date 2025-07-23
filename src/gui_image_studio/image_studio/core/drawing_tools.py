"""
Drawing tools manager - manages tool selection and delegates to individual tools.
"""

from typing import Any, Dict, List, Optional

from PIL import Image

from ..toolkit.tools import BaseTool, ToolRegistry


class DrawingToolsManager:
    """Manages drawing tools and their settings using a modular tool system."""

    def __init__(self):
        # Core state
        self.current_tool_name = "brush"
        self.brush_size = 5
        self.brush_color = "#000000"
        self.canvas_size = (300, 300)
        self.zoom_level = 1.0
        self.show_grid = False
        self.drawing = False
        self.start_x = 0
        self.start_y = 0

        # Shape preview state
        self.preview_shape = None  # Canvas item ID for preview shape
        self.preview_active = False

        # Pixel highlight for precise drawing
        self.pixel_highlight = None  # Canvas item ID for pixel highlight
        self.last_highlight_pos = None  # Track last highlighted position

        # Tool-specific settings storage
        self.tool_settings = {}

        # Initialize tool settings for all registered tools
        self._initialize_tool_settings()

    def _initialize_tool_settings(self) -> None:
        """Initialize settings for all registered tools."""
        for tool_name, tool in ToolRegistry.get_all_tools().items():
            if hasattr(tool, "settings"):
                self.tool_settings[tool_name] = tool.settings.copy()

    def get_available_tools(self) -> List[str]:
        """Get list of all available tool names."""
        return ToolRegistry.get_tool_names()

    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool."""
        tool = ToolRegistry.get_tool(tool_name)
        if tool:
            return {
                "name": tool.name,
                "display_name": tool.display_name,
                "description": tool.get_description(),
                "icon": tool.get_icon(),
                "cursor": tool.cursor,
                "supports_preview": tool.supports_preview(),
            }
        return None

    def get_all_tool_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all registered tools."""
        tools_info = {}
        for tool_name, tool in ToolRegistry.get_all_tools().items():
            tools_info[tool_name] = {
                "name": tool.name,
                "display_name": tool.display_name,
                "description": tool.get_description(),
                "icon": tool.get_icon(),
                "cursor": tool.cursor,
                "supports_preview": tool.supports_preview(),
            }
        return tools_info

    def get_tools_by_capability(self, capability: str) -> List[str]:
        """Get list of tool names that support a specific capability."""
        tools = []
        for tool_name, tool in ToolRegistry.get_all_tools().items():
            if capability == "click" and tool.supports_click():
                tools.append(tool_name)
            elif capability == "drag" and tool.supports_drag():
                tools.append(tool_name)
            elif capability == "release" and tool.supports_release():
                tools.append(tool_name)
            elif capability == "preview" and tool.supports_preview():
                tools.append(tool_name)
            elif capability == "text_input" and tool.requires_text_input():
                tools.append(tool_name)
        return tools

    def select_tool(self, tool_name: str) -> bool:
        """Select a drawing tool by name."""
        if ToolRegistry.get_tool(tool_name):
            self.current_tool_name = tool_name
            return True
        return False

    def get_current_tool(self) -> str:
        """Get the currently selected tool name."""
        return self.current_tool_name

    def get_current_tool_instance(self) -> Optional[BaseTool]:
        """Get the current tool instance."""
        return ToolRegistry.get_tool(self.current_tool_name)

    # Tool operation methods
    def handle_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle click event with current tool."""
        tool = self.get_current_tool_instance()
        if tool:
            # Merge global settings with tool-specific settings
            merged_kwargs = self._merge_settings(kwargs)
            tool.on_click(image, x, y, **merged_kwargs)

    def handle_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag event with current tool."""
        tool = self.get_current_tool_instance()
        if tool:
            merged_kwargs = self._merge_settings(kwargs)
            tool.on_drag(image, x1, y1, x2, y2, **merged_kwargs)

    def handle_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle release event with current tool."""
        tool = self.get_current_tool_instance()
        if tool:
            merged_kwargs = self._merge_settings(kwargs)
            tool.on_release(image, x1, y1, x2, y2, **merged_kwargs)

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> Optional[int]:
        """Create preview shape with current tool."""
        tool = self.get_current_tool_instance()
        if tool and tool.supports_preview():
            merged_kwargs = self._merge_settings(kwargs)
            return tool.create_preview(
                canvas, x1, y1, x2, y2, self.zoom_level, **merged_kwargs
            )
        return None

    def _merge_settings(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge global settings with tool-specific settings and provided kwargs."""
        merged = {
            "size": self.brush_size,
            "color": self.brush_color,
            "zoom_level": self.zoom_level,
            "show_grid": self.show_grid,
            "canvas_size": self.canvas_size,
        }

        # Add tool-specific settings (but don't override global color)
        tool_settings = self.tool_settings.get(self.current_tool_name, {})
        for key, value in tool_settings.items():
            if (
                key != "color"
            ):  # Don't let tool-specific color override global brush color
                merged[key] = value

        # Override with provided kwargs
        merged.update(kwargs)

        return merged

    # Settings management
    def get_tool_settings(self, tool_name: str) -> Dict[str, Any]:
        """Get settings for a specific tool."""
        return self.tool_settings.get(tool_name, {}).copy()

    def set_tool_setting(self, tool_name: str, setting: str, value: Any) -> None:
        """Set a specific setting for a tool."""
        if tool_name not in self.tool_settings:
            self.tool_settings[tool_name] = {}

        # Validate setting with tool
        tool = ToolRegistry.get_tool(tool_name)
        if tool:
            temp_settings = self.tool_settings[tool_name].copy()
            temp_settings[setting] = value
            validated = tool.validate_settings(temp_settings)
            self.tool_settings[tool_name] = validated
        else:
            self.tool_settings[tool_name][setting] = value

    def get_tool_settings_panel(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get settings panel configuration for a tool."""
        tool = ToolRegistry.get_tool(tool_name)
        return tool.get_settings_panel() if tool else None

    # Legacy compatibility methods
    def set_brush_size(self, size: int) -> None:
        """Set the brush size (affects all tools that use size)."""
        self.brush_size = max(1, min(50, size))

    def get_brush_size(self) -> int:
        """Get the current brush size."""
        return self.brush_size

    def set_brush_color(self, color: str) -> None:
        """Set the brush color (affects all tools that use color)."""
        self.brush_color = color

    def get_brush_color(self) -> str:
        """Get the current brush color."""
        return self.brush_color

    def set_zoom_level(self, zoom: float) -> None:
        """Set the zoom level."""
        self.zoom_level = max(0.1, min(10.0, zoom))

    def get_zoom_level(self) -> float:
        """Get the current zoom level."""
        return self.zoom_level

    def toggle_grid(self) -> bool:
        """Toggle grid display."""
        self.show_grid = not self.show_grid
        return self.show_grid

    def get_cursor_for_tool(self, tool_name: str) -> str:
        """Get the cursor for a specific tool."""
        tool = ToolRegistry.get_tool(tool_name)
        if tool:
            return tool.get_cursor_for_size(self.brush_size)
        return "arrow"

    def set_cursor_for_tool(self, tool_name: str, cursor: str) -> None:
        """Set the cursor for a specific tool."""
        tool = ToolRegistry.get_tool(tool_name)
        if tool:
            tool.cursor = cursor

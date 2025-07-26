"""
UI panel setup methods for Image Studio.
"""

from typing import TYPE_CHECKING

from .center_panel import CenterPanel
from .left_panel import LeftPanel
from .right_panel import RightPanel

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class PanelManager:
    """Manages the setup of UI panels."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app
        self.left_panel = LeftPanel(app)
        self.center_panel = CenterPanel(app)
        self.right_panel = RightPanel(app)

    def setup_left_panel(self, parent):
        """Setup the left panel with tools and image management."""
        self.left_panel.setup(parent)

    def setup_center_panel(self, parent):
        """Setup the center panel with the drawing canvas."""
        self.center_panel.setup(parent)

    def setup_right_panel(self, parent):
        """Setup the right panel with properties and code generation."""
        self.right_panel.setup(parent)

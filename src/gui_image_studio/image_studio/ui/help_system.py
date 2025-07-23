"""
Comprehensive help system for Image Studio.
"""

import tkinter as tk
import webbrowser
from tkinter import font, messagebox, ttk
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..toolkit.tools import ToolRegistry

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class HelpContentManager:
    """Manages help content generation and organization."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app

    def get_tools_help(self) -> str:
        """Generate dynamic tools help content."""
        content = ["DRAWING TOOLS\n" + "=" * 50 + "\n"]

        # Get all tools dynamically
        all_tools = ToolRegistry.get_all_tools()

        # Group tools by category
        drawing_tools = []
        shape_tools = []
        utility_tools = []

        for tool_name, tool in all_tools.items():
            tool_info = {
                "name": tool.display_name,
                "description": tool.get_description(),
                "supports_click": tool.supports_click(),
                "supports_drag": tool.supports_drag(),
                "supports_preview": tool.supports_preview(),
                "requires_text": tool.requires_text_input(),
            }

            if tool.supports_preview():
                shape_tools.append(tool_info)
            elif tool.requires_text_input():
                utility_tools.append(tool_info)
            else:
                drawing_tools.append(tool_info)

        # Drawing Tools Section
        if drawing_tools:
            content.append("DRAWING TOOLS:")
            for tool in sorted(drawing_tools, key=lambda x: x["name"]):
                content.append(f"• {tool['name']}: {tool['description']}")
                if tool["supports_click"] and tool["supports_drag"]:
                    content.append("  - Click to draw single points")
                    content.append("  - Drag to draw continuous strokes")
                elif tool["supports_click"]:
                    content.append("  - Click to apply effect")
                content.append("")

        # Shape Tools Section
        if shape_tools:
            content.append("SHAPE TOOLS:")
            for tool in sorted(shape_tools, key=lambda x: x["name"]):
                content.append(f"• {tool['name']}: {tool['description']}")
                content.append("  - Click and drag to define shape")
                content.append("  - Release to complete shape")
                content.append("  - Live preview while dragging")
                content.append("")

        # Utility Tools Section
        if utility_tools:
            content.append("UTILITY TOOLS:")
            for tool in sorted(utility_tools, key=lambda x: x["name"]):
                content.append(f"• {tool['name']}: {tool['description']}")
                if tool["requires_text"]:
                    content.append("  - Click to place text cursor")
                    content.append("  - Type to enter text")
                content.append("")

        return "\n".join(content)

    def get_shortcuts_help(self) -> str:
        """Generate keyboard shortcuts help content."""
        return """KEYBOARD SHORTCUTS
==================================================

FILE OPERATIONS:
• Ctrl+N          New image
• Ctrl+O          Load image
• Ctrl+S          Save image (if implemented)
• Ctrl+Q          Quit application

CANVAS OPERATIONS:
• G               Toggle grid display
• Ctrl+Z          Undo (if implemented)
• Ctrl+Y          Redo (if implemented)
• Delete          Clear canvas
• Escape          Cancel current operation

ZOOM & VIEW:
• +               Zoom in
• -               Zoom out
• 0               Reset zoom to 100%
• Ctrl++          Zoom in (alternative)
• Ctrl+-          Zoom out (alternative)
• Ctrl+0          Reset zoom (alternative)
• F               Fit to window

TOOL SELECTION:
• B               Brush tool
• P               Pencil tool
• E               Eraser tool
• L               Line tool
• R               Rectangle tool
• C               Circle tool
• T               Text tool
• F               Fill tool
• S               Spray tool
• M               Marker tool (if available)
• H               Highlighter tool (if available)

PANELS & UI:
• F1              Show this help
• F11             Toggle fullscreen (if implemented)
• Tab             Toggle panel visibility
• Ctrl+1          Toggle left panel
• Ctrl+2          Toggle right panel

COLOR & SETTINGS:
• Ctrl+Shift+C    Open color chooser
• [               Decrease brush size
• ]               Increase brush size
• Shift+[         Decrease opacity
• Shift+]         Increase opacity

CANVAS NAVIGATION:
• Arrow Keys      Move canvas (if pan mode)
• Space+Drag      Pan canvas
• Ctrl+Home       Center canvas
• Page Up/Down    Scroll canvas vertically
• Shift+Page Up/Down  Scroll canvas horizontally

Note: Some shortcuts may vary depending on your operating system.
"""

    def get_interface_help(self) -> str:
        """Generate interface help content."""
        return """USER INTERFACE GUIDE
==================================================

MAIN WINDOW LAYOUT:

┌─────────────────────────────────────────────────┐
│ File  Edit  View  Panels  Settings  Help       │ Menu Bar
├─────────────────────────────────────────────────┤
│ [Tools] [Colors] [Size] [Options]               │ Toolbar
├──────────┬─────────────────────────┬────────────┤
│          │                         │            │
│   Tool   │                         │  Layers    │
│ Palette  │      Canvas Area        │  History   │
│          │                         │  Info      │
│ Settings │                         │            │
│          │                         │            │
├──────────┴─────────────────────────┴────────────┤
│ Status: Ready | Zoom: 100% | Tool: Brush       │ Status Bar
└─────────────────────────────────────────────────┘

TOOL PALETTE (Left Panel):
• Click tool icons to select drawing tools
• Current tool is highlighted
• Hover for tool descriptions
• Right-click for tool options (if available)

CANVAS AREA (Center):
• Main drawing surface
• Grid overlay (toggle with G)
• Zoom controls in corner
• Scroll bars for navigation
• Context menu (right-click)

PROPERTIES PANEL (Right Panel):
• Tool-specific settings
• Color picker and palette
• Brush size and opacity
• Layer management (if implemented)
• Image information

MENU BAR:
• File: New, Open, Save, Export operations
• Edit: Canvas operations, undo/redo
• View: Zoom, grid, panel visibility
• Panels: Show/hide interface panels
• Settings: Application preferences
• Help: Documentation and about info

TOOLBAR:
• Quick access to common tools
• Color selection buttons
• Size and opacity sliders
• Tool options and settings

STATUS BAR:
• Current operation status
• Zoom level indicator
• Active tool display
• Canvas dimensions
• Mouse coordinates (when drawing)

PANEL MANAGEMENT:
• Panels can be toggled on/off
• Resizable panel boundaries
• Collapsible sections
• Dockable panels (if implemented)

CONTEXT MENUS:
• Right-click on canvas for options
• Right-click on tools for settings
• Right-click on panels for customization
"""

    def get_getting_started_help(self) -> str:
        """Generate getting started guide."""
        return """GETTING STARTED GUIDE
==================================================

WELCOME TO IMAGE STUDIO!

This guide will help you create your first image in just a few steps.

STEP 1: CREATE A NEW IMAGE
1. Click "File" → "New Image" (or press Ctrl+N)
2. Choose your image dimensions (default: 400x400)
3. Select background color (default: white)
4. Click "Create" to start

STEP 2: SELECT A DRAWING TOOL
1. Look at the tool palette on the left
2. Click on the Brush tool (or press B)
3. The selected tool will be highlighted
4. You'll see tool options in the right panel

STEP 3: CHOOSE A COLOR
1. In the right panel, find the color section
2. Click the color button to open color picker
3. Choose your desired color
4. The color button will update to show your selection

STEP 4: ADJUST TOOL SETTINGS
1. In the right panel, adjust brush size
2. Set opacity if needed
3. Configure any tool-specific options
4. Settings apply immediately

STEP 5: START DRAWING
1. Move your mouse over the canvas
2. Click and drag to draw
3. Release mouse button to finish stroke
4. Continue drawing as desired

STEP 6: USE ADDITIONAL TOOLS
• Try the Pencil tool for precise pixel work
• Use Shape tools (Rectangle, Circle, Line) for geometric shapes
• Experiment with the Eraser to remove parts
• Add text with the Text tool

STEP 7: SAVE YOUR WORK
1. Click "File" → "Export Images"
2. Choose your export format
3. Select destination folder
4. Click "Export" to save

TIPS FOR BEGINNERS:
• Use the Grid (press G) for precise alignment
• Zoom in (+) for detailed work
• Zoom out (-) to see the full image
• Use Undo (Ctrl+Z) if you make mistakes
• Experiment with different tools and settings
• Save frequently to avoid losing work

COMMON WORKFLOWS:

ICON CREATION:
1. Create small image (32x32 or 64x64)
2. Use Pencil tool for pixel-perfect work
3. Enable grid for alignment
4. Use limited color palette
5. Export as PNG for transparency

DIGITAL SKETCHING:
1. Create larger canvas (800x600 or more)
2. Use Brush tool with varying sizes
3. Start with light strokes for outline
4. Add details with smaller brush
5. Use layers for organization (if available)

LOGO DESIGN:
1. Plan your design on paper first
2. Use Shape tools for geometric elements
3. Add text with Text tool
4. Use consistent colors
5. Export in multiple formats

Remember: Practice makes perfect! Don't be afraid to experiment with different tools and techniques.
"""

    def get_troubleshooting_help(self) -> str:
        """Generate troubleshooting guide."""
        return """TROUBLESHOOTING GUIDE
==================================================

COMMON ISSUES AND SOLUTIONS:

DRAWING PROBLEMS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: Can't draw on canvas
Solutions:
• Check if a drawing tool is selected
• Ensure canvas is not locked
• Try clicking directly on canvas area
• Check if zoom level is appropriate
• Restart application if issue persists

Problem: Lines appear jagged or pixelated
Solutions:
• This is normal for pixel-based drawing
• Use higher resolution canvas for smoother lines
• Try different brush sizes
• Consider using vector-based tools for smooth curves

Problem: Colors not applying correctly
Solutions:
• Check color picker selection
• Ensure tool supports color (Eraser doesn't use color)
• Verify opacity settings (100% = fully opaque)
• Try selecting color again

PERFORMANCE ISSUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: Application runs slowly
Solutions:
• Close other applications to free memory
• Use smaller canvas sizes for better performance
• Reduce zoom level when not needed
• Clear undo history if available
• Restart application periodically

Problem: High memory usage
Solutions:
• Work with smaller images when possible
• Export and restart for large projects
• Close unused images/windows
• Monitor system resources

INTERFACE ISSUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: Panels disappeared
Solutions:
• Use View menu to restore panels
• Press Ctrl+1 for left panel
• Press Ctrl+2 for right panel
• Use "Reset Panel Layout" in Panels menu

Problem: Tools not responding
Solutions:
• Click directly on tool icons
• Check if tool is already selected
• Try keyboard shortcuts (B for Brush, etc.)
• Restart application if needed

Problem: Menu items grayed out
Solutions:
• Some features require an active image
• Create new image or load existing one
• Check if operation is valid for current state
• Some features may not be implemented yet

FILE OPERATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: Can't save or export images
Solutions:
• Check file permissions in target directory
• Ensure filename is valid (no special characters)
• Try different export format
• Check available disk space
• Run application as administrator if needed

Problem: Images appear corrupted after saving
Solutions:
• Try different file format (PNG, JPEG, BMP)
• Check if image dimensions are valid
• Ensure sufficient disk space during save
• Avoid special characters in filename

Problem: Can't load existing images
Solutions:
• Check if file format is supported
• Verify file is not corrupted
• Try copying file to different location
• Check file permissions
• Use standard image formats (PNG, JPEG, BMP)

KEYBOARD SHORTCUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: Shortcuts not working
Solutions:
• Check if correct modifier keys are used (Ctrl, Shift)
• Ensure application has focus (click on window)
• Some shortcuts may be OS-specific
• Check for conflicting system shortcuts
• Try using menu items instead

SYSTEM COMPATIBILITY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: Application won't start
Solutions:
• Check Python version compatibility
• Install required dependencies (PIL, tkinter)
• Check system requirements
• Try running from command line for error messages
• Update graphics drivers

Problem: Display issues or artifacts
Solutions:
• Update graphics drivers
• Try different display scaling settings
• Check color depth settings (24-bit or 32-bit)
• Disable hardware acceleration if available
• Try different screen resolution

GETTING HELP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you continue to experience issues:

1. Check the application logs for error messages
2. Try reproducing the issue with minimal steps
3. Note your system specifications and OS version
4. Document exact error messages
5. Try with a fresh installation
6. Contact support with detailed information

REPORTING BUGS:
When reporting issues, please include:
• Operating system and version
• Python version
• Steps to reproduce the problem
• Expected vs actual behavior
• Screenshots if applicable
• Error messages (if any)

Remember: Most issues can be resolved by restarting the application or using alternative approaches to achieve your goal.
"""

    def get_advanced_tips_help(self) -> str:
        """Generate advanced tips and techniques."""
        return """ADVANCED TIPS & TECHNIQUES
==================================================

PROFESSIONAL WORKFLOWS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PIXEL ART CREATION:
• Use small canvas sizes (16x16, 32x32, 64x64)
• Enable grid for precise pixel placement
• Use Pencil tool for exact pixel control
• Work with limited color palettes
• Zoom in heavily (800% or more) for detail work
• Use Rectangle tool for large solid areas
• Save as PNG to preserve sharp edges

ICON DESIGN WORKFLOW:
1. Start with rough sketch on paper
2. Create multiple sizes (16x16, 32x32, 48x48)
3. Begin with largest size, work down to smaller
4. Use consistent visual metaphors
5. Test at actual display sizes
6. Export in multiple formats (PNG, ICO)

DIGITAL PAINTING TECHNIQUES:
• Start with large brush for base shapes
• Gradually use smaller brushes for details
• Build up colors in layers
• Use opacity variations for blending effects
• Work from general to specific
• Step back frequently to assess overall composition

TOOL MASTERY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRUSH TOOL ADVANCED TECHNIQUES:
• Vary pressure for different line weights
• Use quick strokes for energy, slow for precision
• Overlap strokes for texture effects
• Change size mid-stroke for dynamic lines
• Use low opacity for subtle shading

SHAPE TOOL COMBINATIONS:
• Combine multiple shapes for complex forms
• Use Rectangle + Circle for rounded rectangles
• Layer shapes with different opacities
• Create patterns with repeated shapes
• Use shapes as guides for freehand drawing

TEXT TOOL BEST PRACTICES:
• Choose fonts appropriate for image purpose
• Consider readability at target size
• Use consistent text styling
• Align text with other elements
• Test text visibility on different backgrounds

SPRAY TOOL CREATIVE USES:
• Create texture and noise effects
• Simulate natural materials (stone, fabric)
• Add atmospheric effects (fog, dust)
• Create organic, irregular shapes
• Build up gradual color transitions

COLOR THEORY APPLICATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COLOR HARMONY:
• Use complementary colors for contrast
• Apply analogous colors for harmony
• Create focal points with accent colors
• Consider color temperature (warm/cool)
• Test colors in different lighting conditions

PALETTE STRATEGIES:
• Limit palette for cohesive look
• Use color variations rather than pure hues
• Create custom palettes for projects
• Save successful color combinations
• Study color relationships in reference images

COMPOSITION TECHNIQUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE OF THIRDS:
• Place important elements on grid intersections
• Use grid overlay to guide placement
• Balance elements across the composition
• Create visual flow with element positioning

VISUAL HIERARCHY:
• Use size to indicate importance
• Apply contrast to draw attention
• Group related elements together
• Create clear focal points
• Guide viewer's eye through the image

EFFICIENCY TIPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEYBOARD SHORTCUTS MASTERY:
• Learn tool shortcuts (B, P, E, L, R, C, T, F, S)
• Use zoom shortcuts (+, -, 0) frequently
• Master color picker shortcuts
• Memorize common operations (Ctrl+N, Ctrl+O)
• Create custom shortcuts if available

WORKFLOW OPTIMIZATION:
• Plan your image before starting
• Work in logical order (background to foreground)
• Use consistent naming for files
• Save work-in-progress versions
• Keep reference images handy
• Take breaks to maintain perspective

CANVAS MANAGEMENT:
• Choose appropriate canvas size for purpose
• Consider final output requirements
• Use grid for alignment and proportion
• Zoom appropriately for current task
• Keep canvas organized and clean

QUALITY CONTROL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TESTING AND VALIDATION:
• View image at 100% zoom regularly
• Test at intended display size
• Check image in different contexts
• Validate color accuracy on different monitors
• Get feedback from others
• Compare with similar successful images

EXPORT OPTIMIZATION:
• Choose appropriate file format for use case
• PNG for images with transparency
• JPEG for photographs and complex images
• BMP for system compatibility
• Consider file size vs quality trade-offs
• Test exported images in target applications

CREATIVE EXERCISES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SKILL BUILDING:
• Practice basic shapes daily
• Copy existing icons to learn techniques
• Create variations of the same concept
• Work with limited color palettes
• Try different artistic styles
• Challenge yourself with complex subjects

PROJECT IDEAS:
• Create a complete icon set
• Design user interface elements
• Make pixel art characters
• Design logos and branding elements
• Create decorative patterns
• Build sprite sheets for games

Remember: Mastery comes through practice and experimentation. Don't be afraid to try new techniques and push the boundaries of what's possible with the available tools.
"""


class InteractiveTutorial:
    """Interactive tutorial system."""

    def __init__(self, parent, app: "EnhancedImageDesignerGUI"):
        self.parent = parent
        self.app = app
        self.current_step = 0
        self.tutorial_steps = []

    def start_basic_tutorial(self):
        """Start the basic drawing tutorial."""
        self.tutorial_steps = [
            {
                "title": "Welcome to Image Studio!",
                "content": 'This tutorial will guide you through creating your first image.\n\nClick "Next" to continue.',
                "action": None,
            },
            {
                "title": "Step 1: Create New Image",
                "content": "First, let's create a new image.\n\nGo to File → New Image or press Ctrl+N.",
                "action": "highlight_menu_file",
            },
            {
                "title": "Step 2: Select Brush Tool",
                "content": 'Now select the Brush tool from the tool palette on the left.\n\nYou can also press "B" on your keyboard.',
                "action": "highlight_brush_tool",
            },
            {
                "title": "Step 3: Choose a Color",
                "content": "Click the color button in the right panel to choose a drawing color.",
                "action": "highlight_color_picker",
            },
            {
                "title": "Step 4: Start Drawing",
                "content": "Now click and drag on the canvas to draw!\n\nTry making some strokes to get familiar with the tool.",
                "action": "highlight_canvas",
            },
            {
                "title": "Step 5: Try Other Tools",
                "content": "Experiment with other tools like Pencil (P), Rectangle (R), or Circle (C).\n\nEach tool has different properties and uses.",
                "action": "highlight_tool_palette",
            },
            {
                "title": "Tutorial Complete!",
                "content": "Congratulations! You've learned the basics of Image Studio.\n\nExplore the Help menu for more detailed information.",
                "action": None,
            },
        ]

        self.current_step = 0
        self.show_tutorial_window()

    def show_tutorial_window(self):
        """Show the tutorial window."""
        if hasattr(self, "tutorial_window"):
            self.tutorial_window.destroy()

        self.tutorial_window = tk.Toplevel(self.parent)
        self.tutorial_window.title("Interactive Tutorial")
        self.tutorial_window.geometry("400x300")
        self.tutorial_window.transient(self.parent)
        self.tutorial_window.attributes("-topmost", True)

        # Content frame
        content_frame = ttk.Frame(self.tutorial_window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Step indicator
        step_label = ttk.Label(
            content_frame,
            text=f"Step {self.current_step + 1} of {len(self.tutorial_steps)}",
            font=("Arial", 10, "bold"),
        )
        step_label.pack(anchor=tk.W)

        # Title
        title_label = ttk.Label(
            content_frame,
            text=self.tutorial_steps[self.current_step]["title"],
            font=("Arial", 14, "bold"),
        )
        title_label.pack(anchor=tk.W, pady=(10, 5))

        # Content
        content_text = tk.Text(
            content_frame, wrap=tk.WORD, height=8, font=("Arial", 11)
        )
        content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        content_text.insert(tk.END, self.tutorial_steps[self.current_step]["content"])
        content_text.configure(state=tk.DISABLED)

        # Buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)

        if self.current_step > 0:
            ttk.Button(button_frame, text="Previous", command=self.previous_step).pack(
                side=tk.LEFT
            )

        ttk.Button(
            button_frame, text="Close", command=self.tutorial_window.destroy
        ).pack(side=tk.RIGHT)

        if self.current_step < len(self.tutorial_steps) - 1:
            ttk.Button(button_frame, text="Next", command=self.next_step).pack(
                side=tk.RIGHT, padx=(0, 10)
            )

        # Execute step action
        self.execute_step_action()

    def next_step(self):
        """Go to next tutorial step."""
        if self.current_step < len(self.tutorial_steps) - 1:
            self.current_step += 1
            self.show_tutorial_window()

    def previous_step(self):
        """Go to previous tutorial step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_tutorial_window()

    def execute_step_action(self):
        """Execute the action for the current step."""
        action = self.tutorial_steps[self.current_step].get("action")
        if action:
            # Here you would implement highlighting or other visual cues
            # For now, we'll just pass
            pass


class ComprehensiveHelpWindow:
    """Enhanced help window with multiple tabs and interactive features."""

    def __init__(self, parent, app: "EnhancedImageDesignerGUI"):
        self.parent = parent
        self.app = app
        self.content_manager = HelpContentManager(app)

        self.window = tk.Toplevel(parent)
        self.window.title("Image Studio Help")
        self.window.geometry("900x700")
        self.window.transient(parent)

        # Make window resizable
        self.window.minsize(600, 400)

        self.setup_ui()

    def setup_ui(self):
        """Setup the help window UI."""
        # Create main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_getting_started_tab()
        self.create_tools_tab()
        self.create_interface_tab()
        self.create_shortcuts_tab()
        self.create_advanced_tab()
        self.create_troubleshooting_tab()
        self.create_about_tab()

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Tutorial button
        ttk.Button(
            button_frame, text="Start Interactive Tutorial", command=self.start_tutorial
        ).pack(side=tk.LEFT)

        # Online help button
        ttk.Button(
            button_frame, text="Online Documentation", command=self.open_online_help
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Close button
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(
            side=tk.RIGHT
        )

    def create_text_tab(self, title: str, content: str) -> ttk.Frame:
        """Create a tab with scrollable text content."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)

        # Create text widget with scrollbar
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text_widget = tk.Text(
            text_frame, wrap=tk.WORD, font=("Consolas", 10), padx=10, pady=10
        )

        scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=text_widget.yview
        )
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert content
        text_widget.insert(tk.END, content)
        text_widget.configure(state=tk.DISABLED)

        return frame

    def create_getting_started_tab(self):
        """Create the getting started tab."""
        content = self.content_manager.get_getting_started_help()
        self.create_text_tab("Getting Started", content)

    def create_tools_tab(self):
        """Create the tools help tab."""
        content = self.content_manager.get_tools_help()
        self.create_text_tab("Tools", content)

    def create_interface_tab(self):
        """Create the interface help tab."""
        content = self.content_manager.get_interface_help()
        self.create_text_tab("Interface", content)

    def create_shortcuts_tab(self):
        """Create the keyboard shortcuts tab."""
        content = self.content_manager.get_shortcuts_help()
        self.create_text_tab("Shortcuts", content)

    def create_advanced_tab(self):
        """Create the advanced tips tab."""
        content = self.content_manager.get_advanced_tips_help()
        self.create_text_tab("Advanced Tips", content)

    def create_troubleshooting_tab(self):
        """Create the troubleshooting tab."""
        content = self.content_manager.get_troubleshooting_help()
        self.create_text_tab("Troubleshooting", content)

    def create_about_tab(self):
        """Create the about tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="About")

        # Create content frame
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # App title
        title_label = ttk.Label(
            content_frame, text="GUI Image Studio", font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Version info
        version_label = ttk.Label(
            content_frame, text="Version 2.0 - Enhanced Edition", font=("Arial", 12)
        )
        version_label.pack(pady=(0, 20))

        # Description
        desc_text = tk.Text(
            content_frame,
            wrap=tk.WORD,
            height=10,
            font=("Arial", 11),
            relief=tk.FLAT,
            bg=self.window.cget("bg"),
        )
        desc_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        description = """A comprehensive visual tool for developers and designers to create images, icons, and graphics with an intuitive interface.

Features:
• Dynamic tool system with plugin support
• Multiple drawing tools (brush, pencil, shapes, text, etc.)
• Advanced color management
• Grid overlay for precise alignment
• Zoom and pan capabilities
• Export to multiple formats
• Comprehensive help system
• Keyboard shortcuts for efficiency

Built with Python and Tkinter for cross-platform compatibility.

This enhanced version features a completely refactored architecture with improved maintainability, extensibility, and user experience."""

        desc_text.insert(tk.END, description)
        desc_text.configure(state=tk.DISABLED)

        # System info
        info_frame = ttk.LabelFrame(content_frame, text="System Information")
        info_frame.pack(fill=tk.X, pady=(0, 20))

        import platform
        import sys

        system_info = f"""Python Version: {sys.version.split()[0]}
Platform: {platform.system()} {platform.release()}
Architecture: {platform.machine()}
Tools Available: {len(ToolRegistry.get_all_tools())}"""

        info_label = ttk.Label(
            info_frame, text=system_info, font=("Consolas", 10), justify=tk.LEFT
        )
        info_label.pack(padx=10, pady=10, anchor=tk.W)

        # Credits
        credits_frame = ttk.LabelFrame(content_frame, text="Credits")
        credits_frame.pack(fill=tk.X)

        credits_text = """Developed with ❤️ for the developer community
Built using Python, Tkinter, and PIL/Pillow
Icons and interface design by the development team"""

        credits_label = ttk.Label(
            credits_frame, text=credits_text, font=("Arial", 10), justify=tk.CENTER
        )
        credits_label.pack(padx=10, pady=10)

    def start_tutorial(self):
        """Start the interactive tutorial."""
        tutorial = InteractiveTutorial(self.window, self.app)
        tutorial.start_basic_tutorial()

    def open_online_help(self):
        """Open online documentation."""
        # In a real application, this would open a web browser to documentation
        messagebox.showinfo(
            "Online Help",
            "Online documentation would be available at:\nhttps://your-domain.com/image-studio/docs\n\n"
            "For now, use the comprehensive help tabs in this window.",
        )


# Update the original HelpWindow to use the new comprehensive system
class HelpWindow(ComprehensiveHelpWindow):
    """Backward compatibility wrapper for the enhanced help system."""

    pass

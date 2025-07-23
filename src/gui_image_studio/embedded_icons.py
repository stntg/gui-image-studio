"""
Embedded icon data for GUI Image Studio panels.
Generated from simple colored rectangles as proper .ico files.
"""

import base64
import io
import os
import tempfile
from typing import Optional

# Base64 encoded .ico data
ICON_DATA = {
    "tools": "AAABAAEAEBAAAAAAIAAwAQAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/YQAAAAPdJREFUeJztkz1Ow0AQhWd2xraQY0NEFNEnB6DiHnAMTkBPwwk4VKocIOlRRKQQexV5vbOD1gqiWyxR0PCKLUb7vdH84ez+WcXLm/i+QUQEQIWkFFVVibOKmG44wsvF4unqen7rTm1AVJPEFUN+MTGH/W692W5fWKT/qCblXTWbP3bHDJAonV8EinoK0tnXyDKCMT6Eztmj7zvrAYDTJYBHSxyZyHKMGAT8BvEHg6FFfGYgWe8YmX8D+HsDjk/QYbhxifx5zinFf18MsEIIbEyRlzWrCI9YZc7LGviwLwaWKLtsWrui950be0zO9aZp7Zooe8DfnvMnErKFgaSqEPcAAAAASUVORK5CYII=",
    "canvas": "AAABAAEAEBAAAAAAIAAsAQAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/YQQAAAPNJREFUeJztk01KxEAQhV/9jCGEqDguXMscQFx4EL2FJ/AInsBDuZA5wODajYKJIfaku0o6waVhIFvfohua+l5Tf/RyfecxxjdLqQWBAHLMygkOZ5FaVS80w5vLzUO5PrviEMwAnsMZMCsK7t8/trvX3aOmlD6r4/rm6PT8Hl0LyCwPJAOqGjwMT5lVIuKUUkDfRey/IwCdd0AEc/44ZFbzCxHl7Cfw9/6zBFPMyEwpLRMv5PFvgOUGmg93dzjyEMWxz/MaY0YmG7i7iUiBslKY6QGjrCgryFdTZFZF5KRr2mdbrfYHL9MQuG/arYjc0tJ1/gGdJXuT31qqYgAAAABJRU5ErkJggg==",
    "settings": "AAABAAEAEBAAAAAAIAAeAQAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/YQAAAOVJREFUeJztkzGKw0AMRTWWYPDAEDAutvcFtso1DDlGTpAj5AR7qK1yAtcp3BiBzcQjT5DjbT2BLbbZDzOFF0PtC8GXatk0xxruIsDHGAECCfZmUUkJET0QfJCL3pmkudV1/TtO0AECRMVjKsiz6vr91XXdVg8F7f6yq6szMgIi7tIiA9x5CCF/Kkk4UkTCOYwwhRADQ2p4iIorgoCytS712/wFzBmvPxkBu36yKfwP4ewPST7OtAdleTmvPxqwGCyJa55ymi96IMjnnYBgGq6wCB2b+ttY+3j2meZ4LZr4h4sn89pyftVl4tAxmX4cAAAAASUVORK5CYII=",
}


def get_icon_path(icon_name: str) -> Optional[str]:
    """Get a temporary file path for the specified icon."""
    if icon_name not in ICON_DATA:
        return None

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=f"_{icon_name}.ico", delete=False)

    # Decode and write the icon data
    icon_bytes = base64.b64decode(ICON_DATA[icon_name])
    temp_file.write(icon_bytes)
    temp_file.close()

    return temp_file.name


def cleanup_icon(icon_path: Optional[str]) -> None:
    """Clean up a temporary icon file."""
    if icon_path and os.path.exists(icon_path):
        try:
            os.unlink(icon_path)
        except:
            pass  # Ignore cleanup errors

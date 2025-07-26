"""
Image effects registry system.

This module provides a self-discovery registry for image effects, allowing
dynamic registration and discovery of available image transformations.
"""

import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from PIL import Image


@dataclass
class EffectParameter:
    """Definition of an effect parameter."""

    name: str
    param_type: type
    default: Any = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    description: str = ""
    choices: Optional[List[Any]] = None

    def validate(self, value: Any) -> Any:
        """Validate and convert a parameter value."""
        if value is None and self.default is not None:
            return self.default

        # Check choices first, before type conversion
        if self.choices is not None:
            if value not in self.choices:
                raise ValueError(
                    f"Value {value} not in allowed choices: {self.choices}"
                )
            return value

        # Type conversion
        if self.param_type == bool:
            if isinstance(value, str):
                return value.lower() in ("true", "1", "yes", "on")
            return bool(value)
        elif self.param_type in (int, float):
            converted = self.param_type(value)
            if self.min_value is not None and converted < self.min_value:
                converted = self.min_value
            if self.max_value is not None and converted > self.max_value:
                converted = self.max_value
            return converted
        elif self.param_type == str:
            return str(value)
        else:
            return self.param_type(value)


@dataclass
class ImageEffect:
    """Definition of an image effect."""

    name: str
    display_name: str
    description: str
    category: str
    function: Callable[[Image.Image, ...], Image.Image]
    parameters: List[EffectParameter] = field(default_factory=list)
    preview_safe: bool = True  # Whether effect is safe for real-time preview

    def apply(self, image: Image.Image, **kwargs) -> Image.Image:
        """Apply the effect to an image with parameter validation."""
        # Validate and prepare parameters
        validated_params = {}
        for param in self.parameters:
            if param.name in kwargs:
                validated_params[param.name] = param.validate(kwargs[param.name])
            elif param.default is not None:
                validated_params[param.name] = param.default

        # Apply the effect
        return self.function(image, **validated_params)

    def get_parameter_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about effect parameters."""
        return {
            param.name: {
                "type": param.param_type.__name__,
                "default": param.default,
                "min": param.min_value,
                "max": param.max_value,
                "description": param.description,
                "choices": param.choices,
            }
            for param in self.parameters
        }


class EffectsRegistry:
    """Registry for self-registering image effects."""

    _effects: Dict[str, ImageEffect] = {}
    _categories: Dict[str, List[str]] = {}

    @classmethod
    def register(cls, effect: ImageEffect) -> None:
        """Register an image effect."""
        cls._effects[effect.name] = effect

        # Update categories
        if effect.category not in cls._categories:
            cls._categories[effect.category] = []
        if effect.name not in cls._categories[effect.category]:
            cls._categories[effect.category].append(effect.name)

    @classmethod
    def get_effect(cls, name: str) -> Optional[ImageEffect]:
        """Get an effect by name."""
        return cls._effects.get(name)

    @classmethod
    def get_all_effects(cls) -> Dict[str, ImageEffect]:
        """Get all registered effects."""
        return cls._effects.copy()

    @classmethod
    def get_effect_names(cls) -> List[str]:
        """Get list of all effect names."""
        return list(cls._effects.keys())

    @classmethod
    def get_categories(cls) -> Dict[str, List[str]]:
        """Get effects organized by category."""
        return cls._categories.copy()

    @classmethod
    def get_effects_in_category(cls, category: str) -> List[ImageEffect]:
        """Get all effects in a specific category."""
        if category not in cls._categories:
            return []
        return [cls._effects[name] for name in cls._categories[category]]

    @classmethod
    def apply_effect(
        cls, effect_name: str, image: Image.Image, **kwargs
    ) -> Image.Image:
        """Apply an effect by name."""
        effect = cls.get_effect(effect_name)
        if effect is None:
            raise ValueError(f"Unknown effect: {effect_name}")
        return effect.apply(image, **kwargs)

    @classmethod
    def get_preview_safe_effects(cls) -> List[str]:
        """Get effects that are safe for real-time preview."""
        return [name for name, effect in cls._effects.items() if effect.preview_safe]

    @classmethod
    def clear_registry(cls) -> None:
        """Clear all registered effects (mainly for testing)."""
        cls._effects.clear()
        cls._categories.clear()


def register_effect(
    name: str,
    display_name: str = None,
    description: str = "",
    category: str = "general",
    parameters: List[EffectParameter] = None,
    preview_safe: bool = True,
):
    """Decorator to automatically register an image effect function."""

    def decorator(func: Callable[[Image.Image, ...], Image.Image]):
        effect = ImageEffect(
            name=name,
            display_name=display_name or name.replace("_", " ").title(),
            description=description,
            category=category,
            function=func,
            parameters=parameters or [],
            preview_safe=preview_safe,
        )
        EffectsRegistry.register(effect)
        return func

    return decorator


def auto_register_effect(
    display_name: str = None,
    description: str = "",
    category: str = "general",
    parameters: List[EffectParameter] = None,
    preview_safe: bool = True,
):
    """Decorator that auto-detects effect name from function name."""

    def decorator(func: Callable[[Image.Image, ...], Image.Image]):
        # Auto-detect name from function name
        name = func.__name__
        if name.startswith("apply_"):
            name = name[6:]  # Remove 'apply_' prefix

        return register_effect(
            name=name,
            display_name=display_name,
            description=description,
            category=category,
            parameters=parameters,
            preview_safe=preview_safe,
        )(func)

    return decorator


def create_parameter(
    name: str,
    param_type: type,
    default: Any = None,
    min_value: Optional[Union[int, float]] = None,
    max_value: Optional[Union[int, float]] = None,
    description: str = "",
    choices: Optional[List[Any]] = None,
) -> EffectParameter:
    """Helper function to create effect parameters."""
    return EffectParameter(
        name=name,
        param_type=param_type,
        default=default,
        min_value=min_value,
        max_value=max_value,
        description=description,
        choices=choices,
    )


# Convenience functions for common parameter types
def size_parameter(
    name: str = "size",
    default: Tuple[int, int] = None,
    description: str = "Target size (width, height)",
) -> EffectParameter:
    """Create a size parameter."""
    return EffectParameter(name, tuple, default, description=description)


def float_parameter(
    name: str,
    default: float = 1.0,
    min_val: float = 0.0,
    max_val: float = 10.0,
    description: str = "",
) -> EffectParameter:
    """Create a float parameter with bounds."""
    return EffectParameter(name, float, default, min_val, max_val, description)


def int_parameter(
    name: str,
    default: int = 0,
    min_val: int = 0,
    max_val: int = 100,
    description: str = "",
) -> EffectParameter:
    """Create an integer parameter with bounds."""
    return EffectParameter(name, int, default, min_val, max_val, description)


def bool_parameter(
    name: str, default: bool = False, description: str = ""
) -> EffectParameter:
    """Create a boolean parameter."""
    return EffectParameter(name, bool, default, description=description)


def choice_parameter(
    name: str, choices: List[Any], default: Any = None, description: str = ""
) -> EffectParameter:
    """Create a choice parameter."""
    if default is None and choices:
        default = choices[0]
    return EffectParameter(
        name,
        type(default) if default is not None else str,
        default,
        choices=choices,
        description=description,
    )


def discover_and_register_effects():
    """
    Discover and register effects from the image_effects module.

    This function automatically registers existing effects that haven't been
    registered yet, providing backward compatibility.
    """
    from . import image_effects

    # Define effects with their metadata
    effects_metadata = [
        {
            "func": image_effects.resize,
            "name": "resize",
            "display_name": "Resize",
            "description": "Resize image to specified dimensions",
            "category": "geometry",
            "parameters": [
                create_parameter(
                    "size", tuple, (100, 100), description="Target size (width, height)"
                ),
                create_parameter(
                    "preserve_aspect", bool, False, description="Preserve aspect ratio"
                ),
            ],
        },
        {
            "func": image_effects.apply_grayscale,
            "name": "grayscale",
            "display_name": "Grayscale",
            "description": "Convert image to grayscale",
            "category": "color",
            "parameters": [],
        },
        {
            "func": image_effects.apply_rotation,
            "name": "rotation",
            "display_name": "Rotate",
            "description": "Rotate image by specified angle",
            "category": "geometry",
            "parameters": [
                float_parameter(
                    "angle", 0.0, -360.0, 360.0, "Rotation angle in degrees"
                ),
                choice_parameter(
                    "expand", [True, False], True, "Expand image to fit rotated content"
                ),
            ],
        },
        {
            "func": image_effects.apply_transparency,
            "name": "transparency",
            "display_name": "Transparency",
            "description": "Adjust image transparency/opacity",
            "category": "color",
            "parameters": [
                float_parameter(
                    "alpha",
                    1.0,
                    0.0,
                    1.0,
                    "Alpha/opacity level (0=transparent, 1=opaque)",
                )
            ],
        },
        {
            "func": image_effects.apply_contrast,
            "name": "contrast",
            "display_name": "Contrast",
            "description": "Adjust image contrast",
            "category": "enhancement",
            "parameters": [
                float_parameter(
                    "factor", 1.0, 0.0, 3.0, "Contrast factor (1.0=no change)"
                )
            ],
        },
        {
            "func": image_effects.apply_saturation,
            "name": "saturation",
            "display_name": "Saturation",
            "description": "Adjust color saturation",
            "category": "color",
            "parameters": [
                float_parameter(
                    "factor", 1.0, 0.0, 3.0, "Saturation factor (0=grayscale, 1=normal)"
                )
            ],
        },
        {
            "func": image_effects.apply_brightness,
            "name": "brightness",
            "display_name": "Brightness",
            "description": "Adjust image brightness",
            "category": "enhancement",
            "parameters": [
                float_parameter(
                    "factor", 1.0, 0.0, 3.0, "Brightness factor (1.0=no change)"
                )
            ],
        },
        {
            "func": image_effects.apply_sharpness,
            "name": "sharpness",
            "display_name": "Sharpness",
            "description": "Adjust image sharpness",
            "category": "enhancement",
            "parameters": [
                float_parameter(
                    "factor", 1.0, 0.0, 3.0, "Sharpness factor (1.0=no change)"
                )
            ],
        },
        {
            "func": image_effects.apply_blur,
            "name": "blur",
            "display_name": "Blur",
            "description": "Apply blur effect to image",
            "category": "filter",
            "parameters": [float_parameter("radius", 1.0, 0.0, 10.0, "Blur radius")],
        },
        {
            "func": image_effects.apply_tint,
            "name": "tint",
            "display_name": "Tint",
            "description": "Apply color tint to image",
            "category": "color",
            "parameters": [
                create_parameter(
                    "color", tuple, (255, 255, 255), description="Tint color (R, G, B)"
                ),
                float_parameter("strength", 0.5, 0.0, 1.0, "Tint strength"),
            ],
        },
    ]

    # Register effects
    for effect_meta in effects_metadata:
        if not EffectsRegistry.get_effect(effect_meta["name"]):
            effect = ImageEffect(
                name=effect_meta["name"],
                display_name=effect_meta["display_name"],
                description=effect_meta["description"],
                category=effect_meta["category"],
                function=effect_meta["func"],
                parameters=effect_meta["parameters"],
            )
            EffectsRegistry.register(effect)


# Auto-discovery will be called after image_effects module is fully loaded
# to avoid circular import issues


# Bridge toolkit effects to core registry for unified access
def bridge_toolkit_effects():
    """Bridge toolkit effects to the core registry for unified access."""
    try:
        from ..image_studio.toolkit import effects  # This triggers effect registration
        from ..image_studio.toolkit.effects.base_effect import (
            EffectRegistry as ToolkitEffectRegistry,
        )

        toolkit_effects = ToolkitEffectRegistry.get_all_effects()

        for name, effect in toolkit_effects.items():
            # Skip if already registered
            if EffectsRegistry.get_effect(name) is not None:
                continue

            # Create a wrapper function that matches core registry expectations
            def make_effect_wrapper(effect_instance):
                def effect_wrapper(image, **params):
                    return effect_instance.apply_with_validation(image, **params)

                return effect_wrapper

            effect_wrapper = make_effect_wrapper(effect)

            # Convert toolkit parameters to core registry format
            core_parameters = []
            for param in effect.get_parameters():
                if param.param_type == "float":
                    core_param = float_parameter(
                        param.name,
                        param.default,
                        param.min_value or 0.0,
                        param.max_value or 10.0,
                        param.description,
                    )
                elif param.param_type == "int":
                    core_param = int_parameter(
                        param.name,
                        param.default,
                        param.min_value or 0,
                        param.max_value or 100,
                        param.description,
                    )
                elif param.param_type == "bool":
                    core_param = bool_parameter(
                        param.name, param.default, param.description
                    )
                elif param.param_type == "choice":
                    core_param = choice_parameter(
                        param.name,
                        param.choices or [],
                        param.default,
                        param.description,
                    )
                else:
                    core_param = create_parameter(
                        param.name,
                        type(param.default),
                        param.default,
                        param.description,
                    )
                core_parameters.append(core_param)

            # Register with core registry
            core_effect = ImageEffect(
                name=name,
                display_name=effect.display_name,
                description=effect.get_description(),
                category=effect.category,
                function=effect_wrapper,
                parameters=core_parameters,
                preview_safe=getattr(effect, "preview_safe", True),
            )
            EffectsRegistry.register(core_effect)

    except ImportError:
        # Toolkit effects not available
        pass


# Bridge the effects systems
bridge_toolkit_effects()

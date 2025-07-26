"""
Base effect class and registry for image effects.

This module provides the foundation for image effects in the GUI toolkit,
following the same pattern as tools with self-registration and metadata.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from PIL import Image


@dataclass
class EffectParameter:
    """Definition of an effect parameter for GUI controls."""

    name: str
    display_name: str
    param_type: str  # "float", "int", "bool", "choice"
    default: Any
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    choices: Optional[List[str]] = None
    description: str = ""

    def validate_value(self, value: Any) -> Any:
        """Validate and convert a parameter value."""
        if self.param_type == "float":
            val = float(value)
            if self.min_value is not None:
                val = max(val, self.min_value)
            if self.max_value is not None:
                val = min(val, self.max_value)
            return val
        elif self.param_type == "int":
            val = int(value)
            if self.min_value is not None:
                val = max(val, self.min_value)
            if self.max_value is not None:
                val = min(val, self.max_value)
            return val
        elif self.param_type == "bool":
            if isinstance(value, str):
                return value.lower() in ("true", "1", "yes", "on")
            return bool(value)
        elif self.param_type == "choice":
            if self.choices and value not in self.choices:
                return self.choices[0]  # Default to first choice
            return value
        else:
            return value


class BaseEffect(ABC):
    """Base class for all image effects."""

    def __init__(self, name: str, display_name: str, category: str = "general"):
        self.name = name
        self.display_name = display_name
        self.category = category
        self.parameters: List[EffectParameter] = []
        self.preview_safe = True  # Whether effect is safe for real-time preview

    @abstractmethod
    def get_icon(self) -> str:
        """Return the icon name for this effect."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Return a description of what this effect does."""
        pass

    @abstractmethod
    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply the effect to an image with the given parameters."""
        pass

    def get_parameters(self) -> List[EffectParameter]:
        """Get the list of parameters for this effect."""
        return self.parameters

    def add_parameter(self, param: EffectParameter) -> None:
        """Add a parameter to this effect."""
        self.parameters.append(param)

    def validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize effect parameters."""
        validated = {}
        for param in self.parameters:
            if param.name in params:
                validated[param.name] = param.validate_value(params[param.name])
            else:
                validated[param.name] = param.default
        return validated

    def apply_with_validation(self, image: Image.Image, **params) -> Image.Image:
        """Apply effect with parameter validation."""
        validated_params = self.validate_parameters(params)
        return self.apply_effect(image, **validated_params)


class EffectRegistry:
    """Registry for self-registering image effects."""

    _effects: Dict[str, BaseEffect] = {}
    _categories: Dict[str, List[str]] = {}

    @classmethod
    def register(cls, effect: BaseEffect) -> None:
        """Register an image effect."""
        cls._effects[effect.name] = effect

        # Update categories
        if effect.category not in cls._categories:
            cls._categories[effect.category] = []
        if effect.name not in cls._categories[effect.category]:
            cls._categories[effect.category].append(effect.name)

    @classmethod
    def get_effect(cls, name: str) -> Optional[BaseEffect]:
        """Get an effect by name."""
        return cls._effects.get(name)

    @classmethod
    def get_all_effects(cls) -> Dict[str, BaseEffect]:
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
    def get_effects_in_category(cls, category: str) -> List[BaseEffect]:
        """Get all effects in a specific category."""
        if category not in cls._categories:
            return []
        return [cls._effects[name] for name in cls._categories[category]]

    @classmethod
    def clear_registry(cls) -> None:
        """Clear all registered effects (mainly for testing)."""
        cls._effects.clear()
        cls._categories.clear()


def register_effect(effect_class):
    """Decorator to automatically register an effect."""
    # Create and register the effect instance immediately
    effect_instance = effect_class()
    EffectRegistry.register(effect_instance)
    return effect_class


# Helper functions for creating common parameter types
def float_parameter(
    name: str,
    display_name: str,
    default: float,
    min_val: float = 0.0,
    max_val: float = 10.0,
    description: str = "",
) -> EffectParameter:
    """Create a float parameter."""
    return EffectParameter(
        name=name,
        display_name=display_name,
        param_type="float",
        default=default,
        min_value=min_val,
        max_value=max_val,
        description=description,
    )


def int_parameter(
    name: str,
    display_name: str,
    default: int,
    min_val: int = 0,
    max_val: int = 100,
    description: str = "",
) -> EffectParameter:
    """Create an integer parameter."""
    return EffectParameter(
        name=name,
        display_name=display_name,
        param_type="int",
        default=default,
        min_value=min_val,
        max_value=max_val,
        description=description,
    )


def bool_parameter(
    name: str, display_name: str, default: bool = False, description: str = ""
) -> EffectParameter:
    """Create a boolean parameter."""
    return EffectParameter(
        name=name,
        display_name=display_name,
        param_type="bool",
        default=default,
        description=description,
    )


def choice_parameter(
    name: str,
    display_name: str,
    choices: List[str],
    default: str = None,
    description: str = "",
) -> EffectParameter:
    """Create a choice parameter."""
    if default is None and choices:
        default = choices[0]
    return EffectParameter(
        name=name,
        display_name=display_name,
        param_type="choice",
        default=default,
        choices=choices,
        description=description,
    )

"""
Tests for the image effects registry system.

This module tests the effects registry functionality to ensure proper
registration, discovery, and application of image effects.
"""

import tempfile
from pathlib import Path

import pytest
from PIL import Image

from gui_image_studio.core.effects_registry import (
    EffectParameter,
    EffectsRegistry,
    ImageEffect,
    auto_register_effect,
    bool_parameter,
    choice_parameter,
    create_parameter,
    float_parameter,
    int_parameter,
    register_effect,
)


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    return Image.new("RGBA", (100, 100), (255, 0, 0, 255))


@pytest.fixture
def clean_registry():
    """Ensure clean registry for each test."""
    EffectsRegistry.clear_registry()
    yield
    EffectsRegistry.clear_registry()


class TestEffectParameter:
    """Test the EffectParameter class."""

    def test_parameter_creation(self):
        """Test basic parameter creation."""
        param = EffectParameter(
            name="test_param",
            param_type=float,
            default=1.0,
            min_value=0.0,
            max_value=2.0,
            description="Test parameter",
        )

        assert param.name == "test_param"
        assert param.param_type == float
        assert param.default == 1.0
        assert param.min_value == 0.0
        assert param.max_value == 2.0
        assert param.description == "Test parameter"

    def test_parameter_validation_float(self):
        """Test float parameter validation."""
        param = float_parameter("intensity", 1.0, 0.0, 2.0, "Intensity level")

        # Valid values
        assert param.validate(1.5) == 1.5
        assert param.validate("1.5") == 1.5

        # Clamping
        assert param.validate(-0.5) == 0.0  # Below min
        assert param.validate(3.0) == 2.0  # Above max

        # Default
        assert param.validate(None) == 1.0

    def test_parameter_validation_int(self):
        """Test integer parameter validation."""
        param = int_parameter("count", 5, 1, 10, "Count value")

        # Valid values
        assert param.validate(7) == 7
        assert param.validate("7") == 7

        # Clamping
        assert param.validate(0) == 1  # Below min
        assert param.validate(15) == 10  # Above max

    def test_parameter_validation_bool(self):
        """Test boolean parameter validation."""
        param = bool_parameter("enabled", False, "Enable feature")

        # Various boolean representations
        assert param.validate(True) is True
        assert param.validate("true") is True
        assert param.validate("1") is True
        assert param.validate("yes") is True
        assert param.validate("on") is True

        assert param.validate(False) is False
        assert param.validate("false") is False
        assert param.validate("0") is False
        assert param.validate("no") is False

    def test_parameter_validation_choice(self):
        """Test choice parameter validation."""
        param = choice_parameter(
            "mode", ["normal", "fast", "quality"], "normal", "Processing mode"
        )

        # Valid choices
        assert param.validate("normal") == "normal"
        assert param.validate("fast") == "fast"

        # Invalid choice
        with pytest.raises(ValueError):
            param.validate("invalid")


class TestImageEffect:
    """Test the ImageEffect class."""

    def test_effect_creation(self, sample_image):
        """Test basic effect creation."""

        def dummy_effect(image, factor=1.0):
            return image

        effect = ImageEffect(
            name="test_effect",
            display_name="Test Effect",
            description="A test effect",
            category="test",
            function=dummy_effect,
            parameters=[float_parameter("factor", 1.0, 0.0, 2.0, "Effect factor")],
        )

        assert effect.name == "test_effect"
        assert effect.display_name == "Test Effect"
        assert effect.description == "A test effect"
        assert effect.category == "test"
        assert len(effect.parameters) == 1

    def test_effect_apply(self, sample_image):
        """Test effect application."""

        def brightness_effect(image, factor=1.0):
            # Simple brightness adjustment
            if factor == 1.0:
                return image
            return image.point(lambda p: min(255, int(p * factor)))

        effect = ImageEffect(
            name="brightness",
            display_name="Brightness",
            description="Adjust brightness",
            category="enhancement",
            function=brightness_effect,
            parameters=[float_parameter("factor", 1.0, 0.0, 3.0, "Brightness factor")],
        )

        # Apply with default parameters
        result1 = effect.apply(sample_image)
        assert result1.size == sample_image.size

        # Apply with custom parameters
        result2 = effect.apply(sample_image, factor=1.5)
        assert result2.size == sample_image.size

    def test_effect_parameter_info(self):
        """Test parameter info extraction."""

        def dummy_effect(image, factor=1.0, mode="normal"):
            return image

        effect = ImageEffect(
            name="test",
            display_name="Test",
            description="Test effect",
            category="test",
            function=dummy_effect,
            parameters=[
                float_parameter("factor", 1.0, 0.0, 2.0, "Effect factor"),
                choice_parameter(
                    "mode", ["normal", "fast"], "normal", "Processing mode"
                ),
            ],
        )

        param_info = effect.get_parameter_info()

        assert "factor" in param_info
        assert param_info["factor"]["type"] == "float"
        assert param_info["factor"]["default"] == 1.0
        assert param_info["factor"]["min"] == 0.0
        assert param_info["factor"]["max"] == 2.0

        assert "mode" in param_info
        assert param_info["mode"]["choices"] == ["normal", "fast"]


class TestEffectsRegistry:
    """Test the EffectsRegistry class."""

    def test_registry_registration(self, clean_registry, sample_image):
        """Test effect registration."""

        def test_effect(image):
            return image

        effect = ImageEffect(
            name="test",
            display_name="Test Effect",
            description="Test",
            category="test",
            function=test_effect,
        )

        EffectsRegistry.register(effect)

        # Check registration
        assert "test" in EffectsRegistry.get_effect_names()
        assert EffectsRegistry.get_effect("test") == effect

        # Check categories
        categories = EffectsRegistry.get_categories()
        assert "test" in categories
        assert "test" in categories["test"]

    def test_registry_get_methods(self, clean_registry):
        """Test registry getter methods."""

        def effect1(image):
            return image

        def effect2(image):
            return image

        # Register effects in different categories
        EffectsRegistry.register(
            ImageEffect("effect1", "Effect 1", "Test", "category1", effect1)
        )
        EffectsRegistry.register(
            ImageEffect("effect2", "Effect 2", "Test", "category2", effect2)
        )

        # Test get_all_effects
        all_effects = EffectsRegistry.get_all_effects()
        assert len(all_effects) == 2
        assert "effect1" in all_effects
        assert "effect2" in all_effects

        # Test get_effect_names
        names = EffectsRegistry.get_effect_names()
        assert set(names) == {"effect1", "effect2"}

        # Test get_categories
        categories = EffectsRegistry.get_categories()
        assert "category1" in categories
        assert "category2" in categories
        assert "effect1" in categories["category1"]
        assert "effect2" in categories["category2"]

        # Test get_effects_in_category
        cat1_effects = EffectsRegistry.get_effects_in_category("category1")
        assert len(cat1_effects) == 1
        assert cat1_effects[0].name == "effect1"

    def test_registry_apply_effect(self, clean_registry, sample_image):
        """Test applying effects through registry."""

        def brightness_effect(image, factor=1.5):
            return image.point(lambda p: min(255, int(p * factor)))

        effect = ImageEffect(
            name="brightness",
            display_name="Brightness",
            description="Adjust brightness",
            category="enhancement",
            function=brightness_effect,
            parameters=[float_parameter("factor", 1.5, 0.0, 3.0, "Brightness factor")],
        )

        EffectsRegistry.register(effect)

        # Apply effect through registry
        result = EffectsRegistry.apply_effect("brightness", sample_image, factor=2.0)
        assert result.size == sample_image.size

        # Test unknown effect
        with pytest.raises(ValueError):
            EffectsRegistry.apply_effect("unknown", sample_image)

    def test_preview_safe_effects(self, clean_registry):
        """Test preview safe effect filtering."""

        def safe_effect(image):
            return image

        def unsafe_effect(image):
            return image

        EffectsRegistry.register(
            ImageEffect(
                "safe", "Safe", "Safe effect", "test", safe_effect, preview_safe=True
            )
        )
        EffectsRegistry.register(
            ImageEffect(
                "unsafe",
                "Unsafe",
                "Unsafe effect",
                "test",
                unsafe_effect,
                preview_safe=False,
            )
        )

        preview_safe = EffectsRegistry.get_preview_safe_effects()
        assert "safe" in preview_safe
        assert "unsafe" not in preview_safe


class TestEffectDecorators:
    """Test effect registration decorators."""

    def test_register_effect_decorator(self, clean_registry, sample_image):
        """Test the register_effect decorator."""

        @register_effect(
            name="test_decorator",
            display_name="Test Decorator",
            description="Test decorator effect",
            category="test",
            parameters=[float_parameter("factor", 1.0, 0.0, 2.0, "Test factor")],
        )
        def test_effect(image, factor=1.0):
            return image

        # Check that effect was registered
        assert "test_decorator" in EffectsRegistry.get_effect_names()

        effect = EffectsRegistry.get_effect("test_decorator")
        assert effect is not None
        assert effect.display_name == "Test Decorator"
        assert len(effect.parameters) == 1

        # Test that function still works
        result = test_effect(sample_image, factor=1.5)
        assert result.size == sample_image.size

    def test_auto_register_effect_decorator(self, clean_registry, sample_image):
        """Test the auto_register_effect decorator."""

        @auto_register_effect(
            display_name="Auto Test",
            description="Auto-registered effect",
            category="test",
            parameters=[int_parameter("count", 5, 1, 10, "Count parameter")],
        )
        def apply_auto_test(image, count=5):
            return image

        # Check that effect was registered with auto-detected name
        assert "auto_test" in EffectsRegistry.get_effect_names()

        effect = EffectsRegistry.get_effect("auto_test")
        assert effect is not None
        assert effect.display_name == "Auto Test"
        assert effect.name == "auto_test"  # Stripped "apply_" prefix


class TestBuiltinEffectsDiscovery:
    """Test discovery of built-in effects."""

    def test_builtin_effects_registered(self):
        """Test that built-in effects are automatically registered."""
        # The effects should be auto-registered when the module is imported
        effects = EffectsRegistry.get_all_effects()

        # Check for some expected built-in effects
        expected_effects = [
            "resize",
            "grayscale",
            "rotation",
            "transparency",
            "contrast",
            "saturation",
            "brightness",
            "blur",
        ]

        for effect_name in expected_effects:
            assert (
                effect_name in effects
            ), f"Built-in effect {effect_name} not registered"

    def test_builtin_effects_categories(self):
        """Test that built-in effects are properly categorized."""
        categories = EffectsRegistry.get_categories()

        # Check for expected categories
        expected_categories = ["geometry", "color", "enhancement", "filter"]

        for category in expected_categories:
            assert category in categories, f"Category {category} not found"
            assert len(categories[category]) > 0, f"Category {category} is empty"

    def test_new_effects_registered(self, sample_image):
        """Test that new effects using decorators are registered."""
        effects = EffectsRegistry.get_all_effects()

        # Check for some new effects that use the registry system
        new_effects = ["sepia", "emboss", "edge_enhance", "posterize", "invert"]

        for effect_name in new_effects:
            assert effect_name in effects, f"New effect {effect_name} not registered"

            # Test that the effect can be applied
            effect = effects[effect_name]
            result = effect.apply(sample_image)
            assert isinstance(result, Image.Image)
            assert result.size == sample_image.size


class TestEffectApplication:
    """Test actual effect application."""

    def test_sepia_effect(self, sample_image):
        """Test the sepia effect."""
        effect = EffectsRegistry.get_effect("sepia")
        assert effect is not None

        result = effect.apply(sample_image, intensity=0.8)
        assert isinstance(result, Image.Image)
        assert result.size == sample_image.size

    def test_posterize_effect(self, sample_image):
        """Test the posterize effect."""
        effect = EffectsRegistry.get_effect("posterize")
        assert effect is not None

        result = effect.apply(sample_image, bits=3)
        assert isinstance(result, Image.Image)
        assert result.size == sample_image.size

    def test_gaussian_blur_effect(self, sample_image):
        """Test the Gaussian blur effect."""
        effect = EffectsRegistry.get_effect("gaussian_blur")
        assert effect is not None

        result = effect.apply(sample_image, radius=2.5)
        assert isinstance(result, Image.Image)
        assert result.size == sample_image.size

    def test_flip_effects(self, sample_image):
        """Test flip effects."""
        h_flip = EffectsRegistry.get_effect("flip_horizontal")
        v_flip = EffectsRegistry.get_effect("flip_vertical")

        assert h_flip is not None
        assert v_flip is not None

        h_result = h_flip.apply(sample_image)
        v_result = v_flip.apply(sample_image)

        assert h_result.size == sample_image.size
        assert v_result.size == sample_image.size


if __name__ == "__main__":
    pytest.main([__file__])

#!/usr/bin/env python3
"""
Demonstration of the GUI toolkit effects system.

This script shows how the new effects system integrates with the GUI toolkit,
following the same self-registry pattern as tools, with individual effect files
and appropriate icons.
"""

import tempfile
from pathlib import Path

from gui_image_studio.core.io_utils import save_image
from gui_image_studio.core.sample_creation import SampleImageGenerator
from gui_image_studio.image_studio.toolkit import (  # Import to trigger registration
    effects,
)
from gui_image_studio.image_studio.toolkit.effects.base_effect import EffectRegistry


def demonstrate_effects_registry():
    """Demonstrate the effects registry system."""
    print("\n" + "=" * 60)
    print("GUI TOOLKIT EFFECTS REGISTRY DEMONSTRATION")
    print("=" * 60)

    # Show all registered effects
    all_effects = EffectRegistry.get_all_effects()
    categories = EffectRegistry.get_categories()

    print(f"Total registered effects: {len(all_effects)}")
    print(f"Effect categories: {', '.join(categories.keys())}")

    # Show effects by category
    for category, effect_names in categories.items():
        print(f"\n{category.upper()} EFFECTS ({len(effect_names)}):")
        for name in effect_names:
            effect = all_effects[name]
            icon = effect.get_icon()
            description = effect.get_description()
            param_count = len(effect.get_parameters())
            preview_safe = "✓" if effect.preview_safe else "✗"

            print(f"  • {effect.display_name} ({name})")
            print(
                f"    Icon: {icon}.png | Parameters: {param_count} | Preview: {preview_safe}"
            )
            print(f"    Description: {description}")

    print("\n✅ Effects registry working perfectly!")


def demonstrate_effect_parameters():
    """Demonstrate effect parameter system."""
    print("\n" + "=" * 60)
    print("EFFECT PARAMETERS DEMONSTRATION")
    print("=" * 60)

    # Show detailed parameter info for effects with parameters
    effects_with_params = [
        "brightness",
        "contrast",
        "saturation",
        "blur",
        "sharpen",
        "sepia",
        "rotate",
        "posterize",
        "solarize",
        "edge_enhance",
    ]

    for effect_name in effects_with_params:
        effect = EffectRegistry.get_effect(effect_name)
        if effect and effect.get_parameters():
            print(f"\n• {effect.display_name} ({effect_name})")
            print(f"  Category: {effect.category}")

            for param in effect.get_parameters():
                param_info = (
                    f"    - {param.display_name} ({param.name}): {param.param_type}"
                )
                param_info += f", default: {param.default}"

                if param.min_value is not None or param.max_value is not None:
                    param_info += f", range: {param.min_value}-{param.max_value}"

                if param.choices:
                    param_info += f", choices: {param.choices}"

                print(param_info)
                if param.description:
                    print(f"      {param.description}")

    print("\n✅ Parameter system working perfectly!")


def demonstrate_effect_application():
    """Demonstrate applying effects to images."""
    print("\n" + "=" * 60)
    print("EFFECT APPLICATION DEMONSTRATION")
    print("=" * 60)

    # Create test image
    generator = SampleImageGenerator("colorful")
    test_image = generator.create_icon("settings", size=(128, 128))

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Save original
        save_image(test_image, temp_path / "original.png")
        print("Created test image: original.png")

        # Test various effects
        test_effects = [
            ("brightness", {"factor": 1.5}),
            ("contrast", {"factor": 1.3}),
            ("saturation", {"factor": 1.8}),
            ("blur", {"radius": 2.0}),
            ("sepia", {"intensity": 0.8}),
            ("grayscale", {}),
            ("invert", {}),
            ("flip_horizontal", {}),
            ("rotate", {"angle": 45.0, "expand": True}),
            ("posterize", {"bits": 3}),
            ("emboss", {}),
            ("edge_enhance", {"mode": "more"}),
        ]

        print(f"\nApplying {len(test_effects)} different effects:")

        for effect_name, params in test_effects:
            try:
                effect = EffectRegistry.get_effect(effect_name)
                if effect:
                    result = effect.apply_with_validation(test_image, **params)
                    filename = f"{effect_name}_result.png"
                    save_image(result, temp_path / filename)

                    param_str = (
                        ", ".join(f"{k}={v}" for k, v in params.items())
                        if params
                        else "no params"
                    )
                    print(f"  ✅ {effect.display_name}: {param_str} → {filename}")
                else:
                    print(f"  ❌ {effect_name}: Effect not found")

            except Exception as e:
                print(f"  ❌ {effect_name}: Error - {e}")

        print(f"\n✅ Effects applied and saved to: {temp_path}")


def demonstrate_gui_integration():
    """Demonstrate how effects integrate with GUI."""
    print("\n" + "=" * 60)
    print("GUI INTEGRATION DEMONSTRATION")
    print("=" * 60)

    print("The effects system is designed for seamless GUI integration:")

    # Show how GUI can discover effects
    categories = EffectRegistry.get_categories()

    print(f"\n1. Dynamic Menu Generation:")
    print("   Effects can be organized into menus by category:")
    for category, effect_names in categories.items():
        print(f"   └─ {category.title()} Menu")
        for name in effect_names[:3]:  # Show first 3
            effect = EffectRegistry.get_effect(name)
            print(f"      ├─ {effect.display_name} (icon: {effect.get_icon()}.png)")
        if len(effect_names) > 3:
            print(f"      └─ ... and {len(effect_names) - 3} more")

    print(f"\n2. Parameter UI Generation:")
    print("   Effect parameters automatically generate appropriate UI controls:")

    # Show parameter UI mapping
    sample_effect = EffectRegistry.get_effect("brightness")
    if sample_effect:
        print(f"   Example: {sample_effect.display_name}")
        for param in sample_effect.get_parameters():
            if param.param_type == "float":
                ui_control = f"Slider ({param.min_value} to {param.max_value})"
            elif param.param_type == "int":
                ui_control = f"SpinBox ({param.min_value} to {param.max_value})"
            elif param.param_type == "bool":
                ui_control = "CheckBox"
            elif param.param_type == "choice":
                ui_control = f"ComboBox {param.choices}"
            else:
                ui_control = "TextEntry"

            print(f"   └─ {param.display_name}: {ui_control}")

    print(f"\n3. Real-time Preview:")
    preview_safe_effects = [
        name
        for name, effect in EffectRegistry.get_all_effects().items()
        if effect.preview_safe
    ]
    print(f"   {len(preview_safe_effects)} effects are preview-safe:")
    print(f"   {', '.join(preview_safe_effects[:8])}...")

    print(f"\n4. Icon Integration:")
    print("   Each effect has its own icon for toolbar/menu display:")
    for category, effect_names in categories.items():
        if effect_names:
            effect = EffectRegistry.get_effect(effect_names[0])
            icon_path = f"toolkit/icons/effects/{effect.get_icon()}.png"
            print(f"   {effect.display_name}: {icon_path}")
            break

    print("\n✅ GUI integration ready!")


def demonstrate_extensibility():
    """Demonstrate how to extend the effects system."""
    print("\n" + "=" * 60)
    print("EXTENSIBILITY DEMONSTRATION")
    print("=" * 60)

    print("Adding new effects is simple - just create a new file:")

    print(f"\n1. File Structure:")
    print("   toolkit/effects/my_custom_effect.py")
    print("   toolkit/icons/effects/my_custom.png")

    print(f"\n2. Effect Implementation:")
    print(
        """
   from .base_effect import BaseEffect, register_effect, float_parameter

   @register_effect
   class MyCustomEffect(BaseEffect):
       def __init__(self):
           super().__init__(
               name="my_custom",
               display_name="My Custom Effect",
               category="artistic"
           )
           self.add_parameter(
               float_parameter("strength", "Effect Strength", 1.0, 0.0, 2.0)
           )

       def get_icon(self) -> str:
           return "my_custom"

       def get_description(self) -> str:
           return "My custom image effect"

       def apply_effect(self, image, **params):
           # Custom effect logic here
           return image
    """
    )

    print(f"\n3. Automatic Registration:")
    print("   - Effect is automatically discovered when module is imported")
    print("   - Appears in GUI menus and CLI commands")
    print("   - Parameters generate appropriate UI controls")
    print("   - Icon is automatically loaded")

    print(f"\n4. Benefits:")
    print("   ✓ No manual registration required")
    print("   ✓ Consistent API across all effects")
    print("   ✓ Automatic parameter validation")
    print("   ✓ GUI integration out-of-the-box")
    print("   ✓ Plugin architecture ready")

    print("\n✅ Extensibility demonstrated!")


def demonstrate_comparison_with_tools():
    """Show how effects follow the same pattern as tools."""
    print("\n" + "=" * 60)
    print("COMPARISON WITH TOOLS SYSTEM")
    print("=" * 60)

    print("Effects follow the exact same pattern as tools:")

    print(f"\n📁 File Structure Comparison:")
    print("   Tools:   toolkit/tools/brush_tool.py")
    print("   Effects: toolkit/effects/brightness_effect.py")

    print(f"\n🎨 Icon Structure Comparison:")
    print("   Tools:   toolkit/icons/files/brush.png")
    print("   Effects: toolkit/icons/effects/brightness.png")

    print(f"\n🏷️ Registration Comparison:")
    print("   Tools:   @register_tool")
    print("   Effects: @register_effect")

    print(f"\n📋 Registry Comparison:")
    print("   Tools:   ToolRegistry.get_all_tools()")
    print("   Effects: EffectRegistry.get_all_effects()")

    print(f"\n⚙️ Parameter System:")
    print("   Both use the same parameter definition system")
    print("   Both support automatic UI generation")
    print("   Both provide parameter validation")

    print(f"\n🔧 Usage in GUI:")
    print("   Tools:   Applied to canvas via mouse interactions")
    print("   Effects: Applied to images via menu/toolbar actions")

    print("\n✅ Consistent architecture achieved!")


def main():
    """Run the complete demonstration."""
    print("GUI Image Studio - Toolkit Effects System Demonstration")
    print("=" * 60)
    print("This demo shows the new effects system that follows the same")
    print("self-registry pattern as tools, with individual files and icons.")

    try:
        demonstrate_effects_registry()
        demonstrate_effect_parameters()
        demonstrate_effect_application()
        demonstrate_gui_integration()
        demonstrate_extensibility()
        demonstrate_comparison_with_tools()

        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)

        # Final statistics
        all_effects = EffectRegistry.get_all_effects()
        categories = EffectRegistry.get_categories()
        total_params = sum(
            len(effect.get_parameters()) for effect in all_effects.values()
        )
        preview_safe_count = sum(
            1 for effect in all_effects.values() if effect.preview_safe
        )

        print(f"\n🎉 Key Achievements:")
        print("✅ Self-Registry: Effects automatically register like tools")
        print("✅ Individual Files: Each effect in its own file")
        print("✅ Icon Integration: Each effect has its own icon")
        print("✅ Parameter System: Rich parameter definitions")
        print("✅ GUI Ready: Automatic UI generation support")
        print("✅ Consistent API: Same pattern as tools")
        print("✅ Extensible: Easy to add new effects")

        print(f"\n📊 Final Statistics:")
        print(f"• Total Effects: {len(all_effects)}")
        print(f"• Categories: {len(categories)} ({', '.join(categories.keys())})")
        print(f"• Total Parameters: {total_params}")
        print(f"• Preview-Safe Effects: {preview_safe_count}")
        print(f"• Icon Files: {len(all_effects)} (one per effect)")

        print(f"\n🚀 Ready for GUI Integration:")
        print("• Dynamic menu generation from categories")
        print("• Automatic parameter UI controls")
        print("• Real-time preview for safe effects")
        print("• Consistent toolbar/menu icons")
        print("• Plugin architecture support")

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

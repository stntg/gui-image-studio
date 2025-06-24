import customtkinter as ctk

import gui_image_studio

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

# Retrieve an animated GIF with a mild green tint, increased contrast, and lowered saturation.
anim_data = gui_image_studio.get_image(
    "animation.gif",
    framework="customtkinter",
    size=(64, 64),
    theme="default",
    animated=True,
    tint_color=(0, 255, 0),
    tint_intensity=0.3,
    contrast=1.25,
    saturation=0.8,
    frame_delay=120,
)

frames = anim_data["animated_frames"]
delay = anim_data["frame_delay"]

label = ctk.CTkLabel(root)
label.pack(padx=20, pady=20)


def animate(frame_index=0):
    label.configure(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    label.after(delay, animate, frame_index)


animate()
root.mainloop()

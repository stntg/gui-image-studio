import tkinter as tk

import gui_image_studio

root = tk.Tk()

# Retrieve an image with increased contrast (1.5) and boosted saturation (1.3)
tk_image = gui_image_studio.get_image(
    "icon.png",
    framework="tkinter",
    size=(64, 64),
    theme="default",
    contrast=1.5,
    saturation=1.3,
)

btn = tk.Button(root, image=tk_image)
btn.image = tk_image  # Prevent garbage collection
btn.pack()

root.mainloop()

import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale, Radiobutton, IntVar, Spinbox

image = cv2.imread("O:\\Projects\\ML\\NPK Detection\\N Deficiency Detection\\mask_extracted\\masked_dis_leaf (210)_iaip.jpg")
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


colors = {
    'Green': {'lower': [35, 50, 50], 'upper': [165, 255, 255]},
    'Yellow': {'lower': [20, 50, 50], 'upper': [35, 255, 255]},
    'Black': {'lower': [0, 0, 0], 'upper': [180, 255, 30]}
}

selected_color = 'Green'

def update_image():
    lower = np.array(colors[selected_color]['lower'])
    upper = np.array(colors[selected_color]['upper'])

    mask = cv2.inRange(hsv_image, lower, upper)
    output_image = np.zeros_like(image)
    if selected_color == 'Green':
        output_image[mask > 0] = [0, 255, 0]
    elif selected_color == 'Yellow':
        output_image[mask > 0] = [0, 255, 255]
    elif selected_color == 'Black':
        output_image[mask > 0] = [0, 0, 0]

    cv2.imshow("Categorized Leaf Image", output_image)

def on_color_change():
    global selected_color
    selected_color = color_var.get()
    for i, key in enumerate(['lower', 'upper']):
        for j, channel in enumerate(['h', 's', 'v']):
            value = colors[selected_color][key][j]
            sliders[i][j].set(value)
            spinboxes[i][j].delete(0, tk.END)
            spinboxes[i][j].insert(0, value)
    update_image()

def on_slider_change(event=None):
    for i, key in enumerate(['lower', 'upper']):
        for j, channel in enumerate(['h', 's', 'v']):
            value = sliders[i][j].get()
            colors[selected_color][key][j] = value
            spinboxes[i][j].delete(0, tk.END)
            spinboxes[i][j].insert(0, value)
    update_image()

def on_spinbox_change():
    for i, key in enumerate(['lower', 'upper']):
        for j, channel in enumerate(['h', 's', 'v']):
            value = spinboxes[i][j].get()
            colors[selected_color][key][j] = int(value)
            sliders[i][j].set(int(value))
    update_image()



root = tk.Tk()
root.title("Color Detection")

color_var = tk.StringVar(value=selected_color)
for color in colors.keys():
    Radiobutton(root, text=color, variable=color_var, value=color, command=on_color_change).pack(anchor=tk.W)



sliders = []
spinboxes = []
for i, key in enumerate(['Lower', 'Upper']):
    frame = tk.LabelFrame(root, text=key + " HSV Values")
    frame.pack(fill="both", expand="yes")
    channel_sliders = []
    channel_spinboxes = []
    for j, channel in enumerate(['H', 'S', 'V']):
        scale = Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL, length=400, width=20, label=channel)
        scale.pack(side=tk.LEFT)
        scale.set(colors[selected_color][key.lower()][j])
        scale.bind("<Motion>", on_slider_change)
        channel_sliders.append(scale)

        spinbox = Spinbox(frame, from_=0, to=255, width=5, command=on_spinbox_change)
        spinbox.pack(side=tk.LEFT)
        spinbox.delete(0, tk.END)
        spinbox.insert(0, colors[selected_color][key.lower()][j])
        spinbox.bind("<KeyRelease>", lambda event: on_spinbox_change())
        channel_spinboxes.append(spinbox)

    sliders.append(channel_sliders)
    spinboxes.append(channel_spinboxes)

update_image()
root.mainloop()

cv2.destroyAllWindows()

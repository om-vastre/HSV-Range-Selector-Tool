import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale, Spinbox, filedialog, Button
from tkinter.colorchooser import askcolor


def load_image():
    global image, hsv_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        image = cv2.imread(file_path)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        update_image()


def pick_color():
    global selected_color_rgb, selected_color_hsv
    color = askcolor()[0]
    if color:
        selected_color_rgb = np.array([[[color[0], color[1], color[2]]]], dtype=np.uint8)
        selected_color_hsv = cv2.cvtColor(selected_color_rgb, cv2.COLOR_RGB2HSV)[0][0]

        for i, key in enumerate(['lower', 'upper']):
            colors['Custom'][key] = [
                max(0, selected_color_hsv[0] - 10), 50, 50] if key == 'lower' else [
                min(179, selected_color_hsv[0] + 10), 255, 255]

        on_color_change()


# starting HSV values
colors = {
    'Custom': {'lower': [0, 50, 50], 'upper': [10, 255, 255]}
}

selected_color = 'Custom'
selected_color_rgb = np.array([[[0, 255, 0]]], dtype=np.uint8)
selected_color_hsv = cv2.cvtColor(selected_color_rgb, cv2.COLOR_RGB2HSV)[0][0]


def update_image():
    lower = np.array(colors[selected_color]['lower'])
    upper = np.array(colors[selected_color]['upper'])

    mask = cv2.inRange(hsv_image, lower, upper)
    output_image = image.copy()
    output_image[mask > 0] = selected_color_rgb[0][0]

    cv2.imshow("Categorized Leaf Image", output_image)


def on_color_change():
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


# Main window
root = tk.Tk()
root.title("Color Detection")


# choose img button
load_button = Button(root, text="Load Image", command=load_image)
load_button.pack(pady=10)


# color picker
pick_color_button = Button(root, text="Pick Color", command=pick_color)
pick_color_button.pack(pady=10)


# sliders and spinboxes
sliders = []
spinboxes = []
for i, key in enumerate(['Lower', 'Upper']):
    frame = tk.LabelFrame(root, text=key + " HSV Values")
    frame.pack(fill="both", expand="yes")
    channel_sliders = []
    channel_spinboxes = []
    for j, (channel, max_value) in enumerate([('H', 179), ('S', 255), ('V', 255)]):
        sub_frame = tk.Frame(frame)
        sub_frame.pack(fill="x", pady=5)

        scale = Scale(sub_frame, from_=0, to=max_value, orient=tk.HORIZONTAL, length=400, width=20, label=channel)
        scale.pack(side=tk.LEFT)
        scale.set(colors[selected_color][key.lower()][j])
        scale.bind("<Motion>", on_slider_change)
        channel_sliders.append(scale)

        spinbox = Spinbox(sub_frame, from_=0, to=max_value, width=5, command=on_spinbox_change)
        spinbox.pack(side=tk.LEFT, padx=5)
        spinbox.delete(0, tk.END)
        spinbox.insert(0, colors[selected_color][key.lower()][j])
        spinbox.bind("<KeyRelease>", lambda event: on_spinbox_change())
        channel_spinboxes.append(spinbox)

    sliders.append(channel_sliders)
    spinboxes.append(channel_spinboxes)

root.mainloop()

cv2.destroyAllWindows()

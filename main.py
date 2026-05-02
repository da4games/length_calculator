import math
import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow
import os
import sys


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# User configuration
WINDOW_TITLE = "Length Measurement Tool"
IMAGE_PATH = resource_path("assets/Asturien Grundriss big 2.jpg")
MARGIN = 20
REFERENCE_P1 = (1138, 900)  # In original image pixels (unscaled)
REFERENCE_P2 = (459, 900)  # In original image pixels (unscaled)
REFERENCE_REAL_DISTANCE = 540  # In reference units
REFERENCE_UNIT = "cm"
REFERENCE_COLOR = "red"
MEASUREMENT_COLOR = "#0066cc"
LINE_WIDTH = 2  # In pixels on the canvas (not scaled)
MARKER_RADIUS = 2  # In pixels on the canvas (not scaled)
LABEL_OFFSET = (
    4  # Vertical offset for labels above the line, in pixels on the canvas (not scaled)
)
SHIFT_MASK = 0x0001

root = tk.Tk()
root.title(WINDOW_TITLE)
root.state("zoomed")  # Windows: maximize

# Force window info to update before getting screen size
root.update()
window_w = root.winfo_width()
window_h = root.winfo_height()

available_w = window_w - (MARGIN * 2)
available_h = window_h - (MARGIN * 2)

# Load image
img_orig = Image.open(IMAGE_PATH)

# Scale to fit available area while preserving aspect ratio
scale = min(available_w / img_orig.width, available_h / img_orig.height)
new_w = int(img_orig.width * scale)
new_h = int(img_orig.height * scale)
img = img_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)

photo = ImageTk.PhotoImage(img)

canvas = tk.Canvas(root, width=window_w, height=window_h)
canvas.pack(fill="both", expand=True)

# Center the image within the available area, offset by margins
x = MARGIN + (available_w // 2)
y = MARGIN + (available_h // 2)
canvas.create_image(x, y, image=photo, anchor="center")

# Top-left corner of the scaled image on the canvas
image_left = x - (new_w / 2)
image_top = y - (new_h / 2)

# Reference points are in ORIGINAL image pixels (unscaled)
reference_p1 = REFERENCE_P1
reference_p2 = REFERENCE_P2
reference_real_distance = REFERENCE_REAL_DISTANCE
reference_unit = REFERENCE_UNIT


def image_to_canvas_coords(ix, iy):
    return (image_left + (ix * scale), image_top + (iy * scale))


def draw_reference_line(p1, p2, label_text, color=REFERENCE_COLOR):
    x1, y1 = image_to_canvas_coords(p1[0], p1[1])
    x2, y2 = image_to_canvas_coords(p2[0], p2[1])
    items = []
    items.append(canvas.create_line(x1, y1, x2, y2, fill=color, width=LINE_WIDTH))
    items.append(
        canvas.create_oval(
            x1 - MARKER_RADIUS,
            y1 - MARKER_RADIUS,
            x1 + MARKER_RADIUS,
            y1 + MARKER_RADIUS,
            fill=color,
            outline="",
        )
    )
    items.append(
        canvas.create_oval(
            x2 - MARKER_RADIUS,
            y2 - MARKER_RADIUS,
            x2 + MARKER_RADIUS,
            y2 + MARKER_RADIUS,
            fill=color,
            outline="",
        )
    )

    label_x = (x1 + x2) / 2
    label_y = min(y1, y2) - LABEL_OFFSET
    items.append(
        canvas.create_text(label_x, label_y, text=label_text, fill=color, anchor="s")
    )
    return items


def draw_click_marker(p, color):
    cx, cy = image_to_canvas_coords(p[0], p[1])
    return canvas.create_oval(
        cx - MARKER_RADIUS,
        cy - MARKER_RADIUS,
        cx + MARKER_RADIUS,
        cy + MARKER_RADIUS,
        fill=color,
        outline="",
    )


draw_reference_line(
    reference_p1,
    reference_p2,
    f"{reference_real_distance} {reference_unit}",
    color=REFERENCE_COLOR,
)

ref_pixel_distance = math.hypot(
    reference_p2[0] - reference_p1[0],
    reference_p2[1] - reference_p1[1],
)
real_per_pixel = (
    reference_real_distance / ref_pixel_distance if ref_pixel_distance != 0 else None
)

clicks = []
click_markers = []
measurement_items = []


def canvas_to_image_coords(cx, cy):
    ix = cx - image_left
    iy = cy - image_top
    if ix < 0 or iy < 0 or ix >= new_w or iy >= new_h:
        return None
    return (ix / scale, iy / scale)


def on_click(event):
    img_pt = canvas_to_image_coords(event.x, event.y)
    if img_pt is None:
        print("Click ignored (outside image)")
        return

    is_shift = (event.state & SHIFT_MASK) != 0
    if is_shift and len(clicks) % 2 == 1:
        x0, y0 = clicks[-1]
        dx = img_pt[0] - x0
        dy = img_pt[1] - y0
        if abs(dx) >= abs(dy):
            img_pt = (img_pt[0], y0)
        else:
            img_pt = (x0, img_pt[1])

    clicks.append(img_pt)
    print(f"Click {len(clicks)} at image coords: ({img_pt[0]:.1f}, {img_pt[1]:.1f})")

    click_markers.append(draw_click_marker(img_pt, MEASUREMENT_COLOR))

    if len(clicks) % 2 == 0:
        (x1, y1), (x2, y2) = clicks[-2], clicks[-1]
        pixel_distance = math.hypot(x2 - x1, y2 - y1)
        if real_per_pixel is None:
            print("Reference points are identical; cannot scale")
            return

        real_distance = pixel_distance * real_per_pixel
        measurement_items.append(
            draw_reference_line(
                (x1, y1),
                (x2, y2),
                f"{real_distance:.3f} {reference_unit}",
                color=MEASUREMENT_COLOR,
            )
        )
        print(f"Distance: {real_distance:.3f} {reference_unit}")


def undo_last(event=None):
    if not clicks:
        return

    if len(clicks) % 2 == 0 and measurement_items:
        for item_id in measurement_items.pop():
            canvas.delete(item_id)

    if click_markers:
        canvas.delete(click_markers.pop())
    clicks.pop()


canvas.bind("<Button-1>", on_click)
root.bind_all("<Control-z>", undo_last)

root.mainloop()

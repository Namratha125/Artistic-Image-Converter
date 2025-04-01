import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def pencil_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)

def cartoonize(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, d=9, sigmaColor=300, sigmaSpace=300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

def hdr_effect(image):
    hdr = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)
    return cv2.cvtColor(hdr, cv2.COLOR_BGR2RGB)

def oil_painting_effect(image):
    oil_paint = cv2.xphoto.oilPainting(image, size=7, dynRatio=1)
    return cv2.cvtColor(oil_paint, cv2.COLOR_BGR2RGB)

def open_image():
    global img, image_cv, processed_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if not file_path:
        return
    image_cv = cv2.imread(file_path)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    processed_image = image_cv.copy()
    update_display()

def apply_effect(effect):
    global image_cv, processed_image
    if image_cv is None:
        messagebox.showerror("Error", "Please load an image first!")
        return
    
    if effect == "sketch":
        processed_image = pencil_sketch(image_cv)
    elif effect == "cartoon":
        processed_image = cartoonize(image_cv)
    elif effect == "hdr":
        processed_image = hdr_effect(image_cv)
    elif effect == "oil_painting":
        processed_image = oil_painting_effect(image_cv)
    else:
        return
    
    update_display()

def update_display():
    global img, img_result, processed_image
    # Resize images to fit in the display
    max_height = 400
    max_width = 400
    
    # Process original image
    orig_img = Image.fromarray(image_cv)
    orig_img.thumbnail((max_width, max_height), Image.LANCZOS)
    img = ImageTk.PhotoImage(orig_img)
    panel_original.config(image=img)
    panel_original.image = img
    
    # Process processed image
    proc_img = Image.fromarray(processed_image)
    proc_img.thumbnail((max_width, max_height), Image.LANCZOS)
    img_result = ImageTk.PhotoImage(proc_img)
    panel_processed.config(image=img_result)
    panel_processed.image = img_result

def save_image():
    global processed_image
    if processed_image is None:
        messagebox.showerror("Error", "No processed image to save!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                           filetypes=[("PNG files", "*.png"), 
                                                      ("JPEG files", "*.jpg"), 
                                                      ("All Files", "*.*")])
    if file_path:
        Image.fromarray(processed_image).save(file_path)
        messagebox.showinfo("Success", "Image saved successfully!")

# GUI Setup
root = tk.Tk()
root.title("ImageFX - Artistic Image Converter")
root.geometry("900x600")  # Adjusted window size for side-by-side display
root.configure(bg="#2c3e50")

# Control buttons frame
control_frame = tk.Frame(root, bg="#34495e", pady=10)
control_frame.pack(fill="x")

btn_open = tk.Button(control_frame, text="Open Image", command=open_image, bg="#1abc9c", fg="white", padx=10, pady=5)
btn_open.grid(row=0, column=0, padx=5, pady=5)
btn_sketch = tk.Button(control_frame, text="Pencil Sketch", command=lambda: apply_effect("sketch"), bg="#3498db", fg="white", padx=10, pady=5)
btn_sketch.grid(row=0, column=1, padx=5, pady=5)
btn_cartoon = tk.Button(control_frame, text="Cartoon", command=lambda: apply_effect("cartoon"), bg="#e74c3c", fg="white", padx=10, pady=5)
btn_cartoon.grid(row=0, column=2, padx=5, pady=5)
btn_hdr = tk.Button(control_frame, text="HDR Effect", command=lambda: apply_effect("hdr"), bg="#f1c40f", fg="black", padx=10, pady=5)
btn_hdr.grid(row=0, column=3, padx=5, pady=5)
btn_oil = tk.Button(control_frame, text="Oil Painting", command=lambda: apply_effect("oil_painting"), bg="#9b59b6", fg="white", padx=10, pady=5)
btn_oil.grid(row=0, column=4, padx=5, pady=5)
btn_save = tk.Button(control_frame, text="Save Image", command=save_image, bg="#2ecc71", fg="white", padx=10, pady=5)
btn_save.grid(row=0, column=5, padx=5, pady=5)

# Image display frame
image_frame = tk.Frame(root, bg="#2c3e50")
image_frame.pack(pady=20)

# Original image panel
original_label = tk.Label(image_frame, text="Original Image", bg="#2c3e50", fg="white", font=('Arial', 12))
original_label.grid(row=0, column=0, padx=10)
panel_original = tk.Label(image_frame, bg="#2c3e50")
panel_original.grid(row=1, column=0, padx=10)

# Processed image panel
processed_label = tk.Label(image_frame, text="Processed Image", bg="#2c3e50", fg="white", font=('Arial', 12))
processed_label.grid(row=0, column=1, padx=10)
panel_processed = tk.Label(image_frame, bg="#2c3e50")
panel_processed.grid(row=1, column=1, padx=10)

image_cv = None
processed_image = None
img_result = None

root.mainloop()
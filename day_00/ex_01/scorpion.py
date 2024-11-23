#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
import sys
import signal
import piexif

file_path = ""

def open_file():
    """
    Open a file dialog to select an image and display its metadata.
    """
    global file_path # in here i have used the global file_path to overid the globale variable and make it accessible from all the functions without passing it all the times
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.xmp")])
    if file_path != "":
        try:
            img = Image.open(file_path)
            info_dict = {
                "Filename": img.filename,
                "Image Size": img.size,
                "Image Height": img.height,
                "Image Width": img.width,
                "Image Format": img.format,
                "Image Mode": img.mode,
                "Image is Animated": getattr(img, "is_animated", False),
                "Frames in Image": getattr(img, "n_frames", 1)
            }

            metadata_display.delete("2.0", tk.END)
            metadata_display.insert(tk.END, "\n\n")
            for label,value in info_dict.items():
                metadata_display.insert(tk.END, f"{label:25}: {value}\n")
            metadata_display.insert(tk.END, "\n\n")

            if hasattr(img, "getexif"):
                exif_data = img.getexif()
                if exif_data:
                    # print("........ exif_inside ...........")
                    metadata_display.insert(tk.END, "EXIF Data:\n")
                    for tag_id, value in exif_data.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        metadata_display.insert(tk.END, f"ID: {tag_id}, NAME: {tag_name}, VALUE: {value}\n")
        except UnidentifiedImageError:
            messagebox.showerror("Error", "Selected file is not a valid image.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def modify_metadata():
    """
    Modify a selected EXIF tag and update the metadata display.
    """
    try:
        # Check if a file is selected
        if not file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        # Get tag and value from the entry fields
        tag = modify_tag_entry.get()
        value = modify_value_entry.get()

        print(f"Tag: {tag}, Value: {value}")
        
        if not tag or not value:
            messagebox.showwarning("Warning", "Please provide both tag and value to modify.")
            return

        # Convert tag to an integer key (required for EXIF data)
        try:
            tag = int(tag)  # Ensure tag is an integer
        except ValueError:
            messagebox.showerror("Error", "Tag must be a valid numeric EXIF tag ID.")
            return
        
        # Open the image
        img = Image.open(file_path)
        exif_data = piexif.load(img.info.get("exif", b""))
        
        # Update the EXIF data with the new tag-value pair
        exif_data["0th"][tag] = value.encode("utf-8")  # EXIF values must be bytes
        
        # Save the image with the updated EXIF data
        exif_bytes = piexif.dump(exif_data)
        img.save(file_path, exif=exif_bytes)
        
        messagebox.showinfo("Success", "Metadata modified and saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def delete_metadata():
    """
    Delete all metadata from the image.
    """
    try:
        if file_path == "":
            messagebox.showerror("error", f"please select a file first !!")
            return
        image = Image.open(file_path)
        image.save(file_path, exif=None)
    except Exception as e:
        messagebox.showinfo(f"Error deleting EXIF data for {file_path}: {e}")


def handle_sigint(signal_received, frame):
    print("Exiting gracefully...")
    root.destroy()
    sys.exit(0)


def check_for_signals():
    root.after(100, check_for_signals)

# Set up signal handling
signal.signal(signal.SIGINT, handle_sigint)

# GUI Setup
root = tk.Tk()
root.title("Scorpion Metadata Manager")
root.geometry("600x400")
root.minsize(300, 200)
root.maxsize(800, 600)

# File Open Button
open_button = tk.Button(root, text="Open Image", command=open_file)
open_button.pack(pady=5)

# Metadata Display
metadata_display = tk.Text(root, wrap=tk.WORD, height=15)
metadata_display.pack(pady=1)

# Modify Metadata Section
modify_frame = tk.Frame(root)
modify_frame.pack(pady=5)

tk.Label(modify_frame, text="Modify Metadata").grid(row=0, column=0, columnspan=3, pady=5)

# Tag Entry
tk.Label(modify_frame, text="Tag_id:").grid(row=1, column=0)
modify_tag_entry = tk.Entry(modify_frame, width=15)
modify_tag_entry.grid(row=2, column=0)

# Value Entry
tk.Label(modify_frame, text="Value:").grid(row=1, column=1)
modify_value_entry = tk.Entry(modify_frame, width=20)
modify_value_entry.grid(row=2, column=1)

# Modify Button
modify_button = tk.Button(modify_frame, text="Modify", command=modify_metadata)
modify_button.grid(row=2, column=2, padx=10)

# Delete Metadata Button
delete_button = tk.Button(root, text="Delete Metadata", command=delete_metadata)
delete_button.pack(pady=5)

root.after(100, check_for_signals)
# Run the GUI
root.mainloop()

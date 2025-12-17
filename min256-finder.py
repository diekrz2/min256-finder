# Licensed under the MIT License

import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

def read_block(file, block_size=4096):
    return file.read(block_size)

def find_sha(file_path):
    find_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                byte_block = f.read(4096)
                if not byte_block:
                    break
                find_hash.update(byte_block)
        return find_hash.hexdigest()
    except Exception as e:
        return f"Error: {str(e)}"

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select an ISO file",
        filetypes=[("ISO", "*.iso"), ("All files", "*.*")]
    )
    
    if file_path:
        messagebox.showinfo("Info", "Calculating...")
        hash_value = find_sha(file_path)
        result_label.config(text=f"SHA256:\n\n{hash_value}")
    else:
        messagebox.showinfo("Info", "No file selected.")

# Main window 
root = tk.Tk()
root.title("min256-finder")
root.geometry("400x100")

# If False (twice) there will be no 'resize' option
# in title bar
root.resizable(False, False)

# Result
result_label = tk.Label(root, text="Select an ISO file", wraplength=350)
result_label.pack(pady=20)

# Button
select_button = tk.Button(root, text="Select", command=select_file)
select_button.pack(pady=10)

root.mainloop()

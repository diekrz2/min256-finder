# Licensed under the MIT License

import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

def read_block(file, block_size=4096):
    return file.read(block_size)

def find_sha(file_path):
    sha256 = hashlib.sha256()
    
    total_size = os.path.getsize(file_path)
    read_size = 0

    try:
        last_percent = -1
        with open(file_path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                
                sha256.update(data)
                read_size += len(data)

                # Simple percentage calculation
                percent = int((read_size / total_size) * 100)
                
                if percent != last_percent:
                   result_label.config(text=f"Calculating... {percent}%")
   
                # GUI update
                root.update_idletasks()
                last_percent = percent
                
        return sha256.hexdigest()

    except Exception as e:
        return f"Error: {str(e)}"

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select an ISO file",
        filetypes=[("ISO", "*.iso"), ("All files", "*.*")]
    )

    if file_path:
        select_button.config(state="disabled")
        result_label.config(text="Calculating... 0%")
        root.update_idletasks()

        # Restart calculating after GUI update
        root.after(100, lambda: start_calculation(file_path))
    else:
        result_label.config(text="No file selected.")
        
def start_calculation(file_path):
    hash_value = find_sha(file_path)

    select_button.config(state="normal")

    # Show result
    result_label.config(text=f"SHA256:\n\n{hash_value}")
    # Final popup 
    messagebox.showinfo("Info", "Done.")

# Main window 
root = tk.Tk()
root.title("min256-finder")
root.geometry("400x100")

# If False (twice) there will be no 'resize' option
# in title bar
root.resizable(False, False)

# Main window
result_label = tk.Label(root, text="Select an ISO file", wraplength=350)
result_label.pack(pady=20)

# Button
select_button = tk.Button(root, text="Select", command=select_file)
select_button.pack(pady=10)

root.mainloop()

# Licensed under the MIT License

import os
import sys
import hashlib
import threading
import queue
import tkinter as tk
from tkinter import filedialog, messagebox
import gettext

APP_NAME = "min256-finder"


def get_resource_path(relative_path=""):

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# localization with gettext:


def get_locale_path():

    # PyInstaller (Windows exe)
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'locales')

    local_path = os.path.join(os.path.dirname(__file__), 'locales')
    if os.path.exists(local_path):
        return local_path

    # Linux (.deb)
    return "/usr/share/locale"


def get_lang_code():
    for env_var in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
        val = os.environ.get(env_var)
        if val:
            code = val.split(':')[0].split('.')[0].split('_')[0].lower()
            if code and code != 'c' and len(code) >= 2:
                return code
    try:
        import locale
        win_lang = locale.getdefaultlocale()[0]
        if win_lang:
            code = win_lang.split('_')[0].lower()
            if code and code != 'c':
                return code
    except Exception:
        pass

    # fallback to English
    return 'en'


lang_code = get_lang_code()

try:
    translation = gettext.translation(
        APP_NAME,
        localedir=get_locale_path(),
        languages=[lang_code, lang_code.split("_")[0]],
        fallback=True
    )
    _ = translation.gettext

except Exception:

    def _(text):
        return text


def find_sha(file_path, cancel_event, progress_queue):
    sha256 = hashlib.sha256()
    read_size = 0
    last_percent = -1

    try:
        total_size = os.path.getsize(file_path)
    except OSError as e:
        progress_queue.put(("error", _("Error: %s") % str(e)))
        return

    try:
        with open(file_path, "rb") as f:
            while True:
                if cancel_event.is_set():
                    progress_queue.put(("cancelled", None))
                    return

                data = f.read(1024 * 1024)
                if not data:
                    break

                sha256.update(data)
                read_size += len(data)
                percent = int((read_size / total_size) * 100)

                if percent != last_percent:
                    progress_queue.put(("progress", percent))
                    last_percent = percent

    except OSError as e:
        progress_queue.put(("error", _("Error: %s") % str(e)))
        return

    progress_queue.put(("done", sha256.hexdigest()))


def select_file():
    file_path = filedialog.askopenfilename(
        title=_("Select an ISO file"),
        filetypes=[("ISO", "*.iso"), (_("All files"), "*.*")]
    )

    if file_path:
        start_calculation(file_path)
    else:
        result_label.config(text=_("No file selected."))


def start_calculation(file_path):
    global worker_thread, cancel_event, progress_queue

    select_button.config(state="disabled")
    idle_exit_button.pack_forget()
    cancel_button.config(state="normal")
    cancel_button.pack(side="left", padx=5)
    result_label.config(text=_("Calculating... 0%"))

    cancel_event = threading.Event()
    progress_queue = queue.Queue()

    worker_thread = threading.Thread(
        target=find_sha,
        args=(file_path, cancel_event, progress_queue),
        daemon=True
    )
    worker_thread.start()

    root.after(50, poll_queue)


def cancel_calculation():
    if cancel_event is not None:
        cancel_event.set()
    cancel_button.config(state="disabled")


def new_calculation():
    result_frame.pack_forget()
    cancel_button.pack_forget()
    idle_exit_button.pack(side="left", padx=5)
    button_frame.pack(pady=10)
    result_label.config(text=_("Select an ISO file"))
    root.geometry("400x100")


def exit_app():
    root.destroy()


def poll_queue():
    try:
        while True:
            msg_type, payload = progress_queue.get_nowait()

            if msg_type == "progress":
                result_label.config(text=_("Calculating... %d%%") % payload)

            elif msg_type == "done":
                select_button.config(state="normal")
                cancel_button.config(state="disabled")
                result_label.config(text=_("SHA256:\n\n%s") % payload)
                button_frame.pack_forget()
                result_frame.pack(pady=10)
                root.geometry("400x160")
                messagebox.showinfo(_("Info"), _("Done."))
                return

            elif msg_type == "error":
                select_button.config(state="normal")
                cancel_button.config(state="disabled")
                result_label.config(text=payload)
                button_frame.pack_forget()
                result_frame.pack(pady=10)
                root.geometry("400x100")
                return

            elif msg_type == "cancelled":
                select_button.config(state="normal")
                cancel_button.config(state="disabled")
                result_label.config(text=_("Cancelled."))
                button_frame.pack_forget()
                result_frame.pack(pady=10)
                root.geometry("400x100")
                return

    except queue.Empty:
        pass

    if worker_thread is not None and worker_thread.is_alive():
        root.after(50, poll_queue)


worker_thread = None
cancel_event = None
progress_queue = None


# Main window
root = tk.Tk(className="min256-finder")
root.title("min256-finder")
root.geometry("400x100")

# If False (twice) there will be no 'resize' option
# in title bar
root.resizable(False, False)

# Main window
result_label = tk.Label(root, text=_("Select an ISO file"), wraplength=350)
result_label.pack(pady=20)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

select_button = tk.Button(button_frame, text=_("Select"), command=select_file)
select_button.pack(side="left", padx=5)

cancel_button = tk.Button(
    button_frame, text=_("Cancel"),
    command=cancel_calculation,
    state="normal")

idle_exit_button = tk.Button(button_frame, text=_("Exit"), command=exit_app)
idle_exit_button.pack(side="left", padx=5)

result_frame = tk.Frame(root)

new_button = tk.Button(result_frame, text=_("New"), command=new_calculation)
new_button.pack(side="left", padx=5)

exit_button = tk.Button(result_frame, text=_("Exit"), command=exit_app)
exit_button.pack(side="left", padx=5)

root.mainloop()

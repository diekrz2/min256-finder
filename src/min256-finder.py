# Licensed under the MIT License

import os
import sys
import hashlib
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
                    result_label.config(
                        text=_("Calculating... %d%%") % percent
                    )

                # GUI update
                root.update_idletasks()
                last_percent = percent

        return sha256.hexdigest()

    except Exception as e:

        return _("Error: %s") % str(e)


def select_file():
    file_path = filedialog.askopenfilename(
        title=_("Select an ISO file"),
        filetypes=[("ISO", "*.iso"), (_("All files"), "*.*")]
    )

    if file_path:
        select_button.config(state="disabled")
        result_label.config(text=_("Calculating... 0%%"))
        root.update_idletasks()

        # Restart calculating after GUI update
        root.after(100, lambda: start_calculation(file_path))
    else:
        result_label.config(text=_("No file selected."))


def start_calculation(file_path):
    hash_value = find_sha(file_path)

    select_button.config(state="normal")

    # Show result
    result_label.config(text=_("SHA256:\n\n%s") % hash_value)
    # Final popup
    messagebox.showinfo(_("Info"), _("Done."))


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

# Button
select_button = tk.Button(root, text=_("Select"), command=select_file)
select_button.pack(pady=10)

root.mainloop()

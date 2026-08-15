# min256-finder
An easy way to find the SHA-256 hash.
This cross-platform tool allows you to find the SHA256 hashes of ISO files (and any other file) with just a few clicks. The app is ready for Debian packaging and an .exe file has been generated using PyInstaller to make it easier to use on Windows systems.

Supported languages: English, Italian and Polish.

<ins>***Dependencies (Linux):***</ins>
- `python3`
- `python3-tk`

<img width="428" height="155" alt="Screenshot-223740" src="https://github.com/user-attachments/assets/2b94b8d8-69b3-4ad4-acfc-392f7d6364c1" />

**Install:**
-------------
<ins>***Windows:***</ins>

It does not require installation. Simply download the .exe file and run it by double-clicking. It works for both 64 bit and 32 bit. Tested on Windows 10 and Windows 11.

<ins>***Linux:***</ins>

**Build with:**  `dpkg-buildpackage -us -uc -b`

**Install with:**  `sudo dpkg -i ../min256-finder_*.deb`

**or...**  `sudo apt install ../min256-finder_*.deb`

>[!NOTE]
>There is a <ins>**locales**</ins> folder containing the translations in the form of .mo files, organized in the standard path ***<lang_code>/LC_MESSAGES***. 
>This setup allows the .deb package to copy the translation files on Linux systems to ***/usr/share/locale/<lang_code>/LC_MESSAGES***, and at the same time serves as the source of >the translations inside the .exe file for Windows.

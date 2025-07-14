<p align="center">
    <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python Version" />
    <img src="https://img.shields.io/badge/GUI-tkinter-blueviolet" alt="tkinter GUI" />
    <img src="https://img.shields.io/badge/PLC-Siemens-green" alt="Siemens PLC" />
</p>

<p align="center">
    <img src="https://raw.githubusercontent.com/Snap7Project/python-snap7/master/docs/_static/snap7-logo.png" alt="snap7 logo" width="120" />
</p>

<h1 align="center">Siemens PLC Data Logger</h1>

<p align="center">
    <b>A simple Python GUI application to connect to a Siemens PLC, read Data Block (DB) data, and save it to a CSV file.</b><br>
    <i>Built with <code>tkinter</code> and <code>snap7</code>.</i>
</p>

---

## Features

- Connect to Siemens PLC using IP, rack, and slot.
- Read entire Data Block (DB) from PLC.
- Save DB data to a timestamped CSV file.
- Basic data parsing (raw bytes, bool, int, float).
- User-friendly GUI with status and log messages.

---

## Requirements

- Python 3.x
- [snap7](https://python-snap7.readthedocs.io/en/latest/)
- tkinter (usually included with Python)
- struct (standard library)

Install snap7 via pip:

```bash
pip install python-snap7
```

---

## Usage

1. Run the script:

   ```bash
   python your_script.py
   ```

2. Enter the PLC IP address, DB number, rack, and slot.
3. Click **Connect to PLC**.
4. Once connected, click **Read DB and Save to CSV**.
5. The data will be saved in a CSV file in the current directory.

---

## Notes

- The DB parsing is generic; for custom DB structures, modify the parsing logic in `read_db_and_save()`.
- Ensure your PLC is reachable from your computer.

---

## Example Screenshots

<p align="center">
    <img src="screenshot.png" alt="GUI Screenshot" width="400" />
</p>

<p align="center">
    <img src="https://user-images.githubusercontent.com/674621/209474104-2e8e6b6b-2e2e-4b8e-8e7e-7e7b7e7b7e7b.png" alt="Sample CSV Output" width="400" />
</p>

---

## License

MIT License

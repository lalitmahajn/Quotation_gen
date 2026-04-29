# 🚀 Quotation PDF Generator

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![Jinja2](https://img.shields.io/badge/Jinja2-3.1.3-B41717.svg)](https://jinja.palletsprojects.com/)
[![PyInstaller](https://img.shields.io/badge/PyInstaller-6.20.0-3776AB.svg)](https://pyinstaller.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A dynamic, fully-featured application designed to replace static HTML quotation layouts with a highly customizable form. This tool generates clean, professional, and **pixel-perfect PDF quotations** by utilizing a browser-based rendering approach, bypassing the CSS limitations of traditional Python PDF libraries.

---

## ✨ Key Features

- 🖥️ **Dual Interfaces**: Choose between a zero-setup, portable **Tkinter Desktop App** or a modern **Streamlit Web App**.
- 🛒 **Dynamic Line Items**: Add/remove rows seamlessly with auto-calculating subtotals, GST (0%, 5%, 12%, 18%, 28%), and grand totals.
- 🏢 **Deep Customization**: Editable fields for company details, bank info, Bill To / Ship To logic, and dynamic terms & conditions.
- 🖨️ **Pixel-Perfect PDF Generation**: Exports via a browser-based print trick (`Ctrl + P` -> Save as PDF) to ensure 100% fidelity to the original template layout.
- 💼 **Portable Distribution**: Pre-packaged as a standalone Windows executable (`.exe`), requiring no local Python installation.

---

## 🛠️ Tech Stack

### Core Technologies
| Technology | Description |
| :--- | :--- |
| **Python** | The primary backend logic and scripting language. |
| **Tkinter** | Python's standard GUI library for the standalone desktop application. |
| **Streamlit** | Rapid web application framework for the browser-based interface. |
| **Jinja2** | Powerful templating engine used to inject dynamic data into the HTML structure. |
| **PyInstaller** | Tool used to package the Python application into a portable Windows executable. |

---

## ⚙️ Setup & Configuration

### Prerequisites
- **Python 3.11+** (Only required if you are not using the `.exe`)
- Your preferred modern web browser (Chrome, Edge, Firefox) for rendering the final PDF.

---

## 🚀 Quick Start (Windows)

Depending on your workflow, you can choose to run the portable executable or host the web application.

### Option 1: Standalone Desktop App (Recommended)
No setup or installation is required. This is a fully portable environment.
```powershell
# Navigate to the dist directory
cd dist

# Double-click the executable or run it from the terminal
.\QuotationGenerator.exe
```

> **⚠️ Note on Windows Security:** Because this `.exe` is custom-built and not digitally signed, Windows Defender may flag it with a *"Windows protected your PC"* popup. Click **"More info"** -> **"Run anyway"**.

### Option 2: Streamlit Web App
Useful for running an internal office server or modifying the source code.
```powershell
# Install required dependencies
pip install -r requirements.txt

# Start the Streamlit application
streamlit run app.py
```
*The web interface will automatically open at: `http://localhost:8501`*

---

## 🔦 Usage & PDF Generation

Because traditional Python PDF libraries struggle with complex CSS structures, this tool leverages your browser's print engine.

1. Fill out your quotation details in the application.
2. Click **"Open in Browser & Print"**. The formatted HTML will open in your default browser.
3. Press <kbd>Ctrl</kbd> + <kbd>P</kbd>.
4. Set the print destination to **"Save as PDF"**.
5. **Important:** Expand "More settings" in the print dialog and ensure **"Headers and footers" is UNCHECKED** to remove unwanted timestamps and file paths.
6. Click Save.

---

## 🏗️ Building from Source

If you make modifications to the UI (`app_desktop.py`) or the structural layout (`template.html`), you can rebuild the standalone executable:

```powershell
# Compile a fresh version of the .exe
pyinstaller --onefile --windowed --add-data "template.html;." --name "QuotationGenerator" --clean app_desktop.py
```
*The newly built file will replace the old one in the `dist/` directory.*

---

## 📁 Project Structure

```text
├── dist/                # Compiled .exe (Ignored by Git; download from GitHub Releases)
├── app_desktop.py       # Source code for the Tkinter desktop application
├── app.py               # Source code for the Streamlit web application
├── pdf_generator.py     # Jinja2 HTML rendering logic
├── template.html        # The visual HTML structure and CSS styling for the quotation
├── requirements.txt     # Python dependency list
├── README.md            # Project documentation
└── LICENSE              # Open-source MIT license file
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

Developed with ❤️ by ARROWTECH COMPUTER.

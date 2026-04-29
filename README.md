<div align="center">
  <h1>📄 Quotation Generator</h1>
  <p>
    <strong>A dynamic, fully-featured desktop application for generating pixel-perfect PDF quotations.</strong>
  </p>
  <p>
    <a href="https://github.com/lalitmahajn/Quotation_gen/issues"><img alt="Issues" src="https://img.shields.io/github/issues/lalitmahajn/Quotation_gen?style=for-the-badge&color=blue"></a>
    <a href="https://github.com/lalitmahajn/Quotation_gen/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/lalitmahajn/Quotation_gen?style=for-the-badge&color=yellow"></a>
    <a href="https://github.com/lalitmahajn/Quotation_gen/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/lalitmahajn/Quotation_gen?style=for-the-badge&color=green"></a>
  </p>
</div>

---

## 📖 About The Project

This project was built to replace a static HTML quotation layout with a dynamic desktop application. It allows you to input company details, dynamic line items, and terms & conditions to generate a clean, professional, and pixel-perfect PDF. 

By relying on the browser's native print engine instead of traditional Python PDF libraries, it ensures the final output exactly matches the styling and structure of your intended design without CSS incompatibilities.

### ✨ Features
* 🖥️ **Two Interfaces**: Choose between a portable Tkinter Desktop app (no setup required) or a modern Streamlit web app.
* 🛒 **Dynamic Line Items**: Easily add/remove items with auto-calculating subtotals, GST (dropdowns for 0%, 5%, 12%, 18%, 28%), and grand totals.
* 🏢 **Customizable Details**: Includes Bill To / Ship To logic, bank details, optional logo uploading, and dynamic terms & conditions.
* 🖨️ **Pixel-Perfect PDF Generation**: Exports via a browser-based print trick to ensure 100% layout fidelity.

---

## 🚀 Getting Started

There are two versions of this application depending on your needs.

### Option 1: Standalone Desktop App (Recommended)
A completely portable Windows executable (`.exe`) built using Tkinter. It requires **no installation, no Python, and no web server**.

1. Navigate to the `dist/` directory.
2. Double-click `QuotationGenerator.exe`.
3. The app will launch immediately.

> **⚠️ Note on Windows Security:** Because this `.exe` is custom-built and not digitally signed by a paid Certificate Authority, Microsoft SmartScreen or Windows Defender may flag it with a *"Windows protected your PC"* popup. This is a common false positive. Simply click **"More info"** and then **"Run anyway"**.

### Option 2: Streamlit Web App
A modern, browser-based version of the tool. Useful if you want to run it on an internal office server or modify the Python code directly.

1. Clone the repo
   ```sh
   git clone https://github.com/lalitmahajn/Quotation_gen.git
   ```
2. Install Python dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Streamlit server
   ```sh
   streamlit run app.py
   ```
4. Access the app in your browser at `http://localhost:8501`.

---

## 🛠️ Usage & PDF Generation

Because Python PDF libraries notoriously struggle with complex CSS grids and flexbox layouts, this application relies on your **web browser's built-in print engine** to guarantee flawless output.

1. Fill out your quotation details in the application.
2. Click the **"Open in Browser & Print"** button. Your default web browser will instantly open the formatted quotation.
3. Press <kbd>Ctrl</kbd> + <kbd>P</kbd> on your keyboard.
4. Set the destination to **"Save as PDF"**.
5. *Important:* Expand "More settings" in the print dialog and ensure **"Headers and footers" is UNCHECKED**. *(This removes the file path and timestamps from the corners of the page).*
6. Click Save!

---

## 🎨 Customizing the Template

The visual structure of the quotation is stored in `template.html`. 
It uses the **Jinja2** templating engine to inject your data into the HTML structure. 

If you need to change fonts, add a new column, or adjust the borders, simply edit the HTML/CSS inside `template.html`.

---

## 📦 Building the `.exe` from Source

If you make modifications to `app_desktop.py` or `template.html` and want to compile a fresh version of the standalone `.exe`, run the following command in your terminal:

```sh
pyinstaller --onefile --windowed --add-data "template.html;." --name "QuotationGenerator" --clean app_desktop.py
```

The newly compiled application will be placed in the `dist` folder.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

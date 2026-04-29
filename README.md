# Quotation Generator

A dynamic, fully-featured quotation generator that allows you to input company details, line items, and terms & conditions to generate a clean, professional, and pixel-perfect PDF.

This project was built to replace a static HTML layout with a dynamic application, ensuring that the final output matches the exact styling and structure of the original layout without the hassle of CSS incompatibilities in traditional PDF libraries.

## Two Versions Available

This project includes two separate versions of the tool depending on your workflow:

### 1. Standalone Desktop App (Recommended)
A completely portable Windows executable (`.exe`) built using Tkinter. It requires **no installation, no Python, and no web server**.

- **Where to find it:** `dist/QuotationGenerator.exe`
- **How to use it:** Just double-click the `.exe` file.
- **Portability:** You can copy this file to a USB drive or share it with trusted colleagues. It runs locally and entirely offline.

> **Note on Windows Security:** Because this `.exe` is custom-built and not digitally signed by a paid Certificate Authority, Microsoft SmartScreen or Windows Defender may flag it as "Windows protected your PC" the first time you run it. This is a common false positive. Simply click **"More info"** and then **"Run anyway"**.

### 2. Streamlit Web App
A modern, browser-based version of the tool. Useful if you want to run it on an internal office server or modify the Python code directly.

- **How to run:** 
  1. Ensure you have Python installed.
  2. Install dependencies: `pip install -r requirements.txt`
  3. Run the app: `streamlit run app.py`
  4. It will open in your browser at `http://localhost:8501`

## Generating the Final PDF

Because Python PDF libraries (like `xhtml2pdf`) notoriously struggle with complex layouts and CSS, this application relies on your **web browser's built-in print engine** to guarantee pixel-perfect output.

**Steps to generate the PDF:**
1. Fill out your quotation details in the application.
2. Click the **"Open in Browser & Print"** button. Your default web browser will instantly open the perfectly formatted quotation.
3. Press **Ctrl + P** on your keyboard.
4. Set the destination to **"Save as PDF"**.
5. *Important:* Expand "More settings" in the print dialog and ensure **"Headers and footers" is UNCHECKED**. (This removes the file path and timestamps from the corners of the page).
6. Click Save!

## Modifying the Template

The visual structure of the quotation is stored in `template.html`. 
It uses the **Jinja2** templating engine to inject your data into the HTML structure. If you need to change fonts, add a new column, or adjust the borders, simply edit the HTML/CSS inside `template.html`.

## Building the `.exe` from Source

If you make modifications to `app_desktop.py` or `template.html` and want to compile a fresh version of the `.exe`, run the following command in your terminal:

```cmd
pyinstaller --onefile --windowed --add-data "template.html;." --name "QuotationGenerator" --clean app_desktop.py
```

The newly compiled application will be placed in the `dist` folder.

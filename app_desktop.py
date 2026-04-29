"""
Quotation Generator — Desktop App
Portable tkinter-based UI. Package with PyInstaller for a standalone .exe.
"""

import os
import sys
import base64
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date
from pdf_generator import render_html

# ── Paths ──────────────────────────────────────────────────────────
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    OUTPUT_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = BASE_DIR

GST_OPTIONS = ["0", "5", "12", "18", "28"]
PAYMENT_OPTIONS = ["100% Advance", "50% Advance", "Net 30", "Net 60"]
VALIDITY_OPTIONS = ["7 Days", "15 Days", "30 Days", "45 Days"]

DEFAULT_TERMS = [
    "100% advance payment",
    "Delivery within 2–5 days",
    "Extra charges if applicable",
    "Warranty as per manufacturer",
    "GST included",
    "Valid for 15 days",
]


class ScrollableFrame(ttk.Frame):
    """A scrollable frame container."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class QuotationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 Quotation Generator")
        self.root.geometry("950x720")
        self.root.minsize(850, 600)

        # Theme & Styling
        style = ttk.Style()
        theme = "vista" if "vista" in style.theme_names() else "clam"
        style.theme_use(theme)
        
        # Modern Typography and Colors
        style.configure(".", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#1a1a2e")
        style.configure("Section.TLabel", font=("Segoe UI", 12, "bold"), foreground="#16213e")
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("Delete.TButton", font=("Segoe UI", 10), foreground="#d9534f")
        
        self.root.configure(background="#f8f9fc")

        self.logo_base64 = None
        self.item_rows = []
        self.term_rows = []

        self._build_ui()

    # ── BUILD UI ───────────────────────────────────────────────────
    def _build_ui(self):
        # Scrollable container
        self.scroll = ScrollableFrame(self.root)
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)
        f = self.scroll.inner

        # Title
        title_frame = ttk.Frame(f)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        ttk.Label(title_frame, text="📄 Quotation Generator", style="Header.TLabel").pack(side="left")
        ttk.Label(title_frame, text="Professional PDF Export", font=("Segoe UI", 10, "italic"), foreground="#7f8c8d").pack(side="right", anchor="s")
        ttk.Separator(f, orient="horizontal").pack(fill="x", padx=20, pady=(0, 15))

        # ── Company Details ────────────────────────────────────────
        sec = ttk.Frame(f)
        sec.pack(fill="x", padx=20, pady=5)
        ttk.Label(sec, text="🏢 Company Details", style="Section.TLabel").pack(anchor="w")
        ttk.Separator(sec, orient="horizontal").pack(fill="x", pady=(2, 10))

        r = ttk.Frame(sec)
        r.pack(fill="x", padx=8, pady=4)
        self.company_name = self._field(r, "Company Name", 0, 0, default="ARROWTECH COMPUTER", width=30)
        self.company_address = self._field(r, "Address", 0, 2, default="C-173, 1st Floor, Golani Market, Jalgaon", width=40)

        r2 = ttk.Frame(sec)
        r2.pack(fill="x", padx=8, pady=4)
        self.company_zip = self._field(r2, "ZIP", 0, 0, default="425001", width=12)
        self.company_phone = self._field(r2, "Phone", 0, 2, default="9579488300", width=15)

        r3 = ttk.Frame(sec)
        r3.pack(fill="x", padx=8, pady=4)
        ttk.Label(r3, text="Logo (optional):").grid(row=0, column=0, sticky="w")
        ttk.Button(r3, text="Browse...", command=self._pick_logo).grid(row=0, column=1, padx=4)
        self.logo_label = ttk.Label(r3, text="No file selected", foreground="gray")
        self.logo_label.grid(row=0, column=2, sticky="w", padx=4)

        # ── Quotation Details ──────────────────────────────────────
        sec = ttk.Frame(f)
        sec.pack(fill="x", padx=20, pady=(15, 5))
        ttk.Label(sec, text="📋 Quotation Details", style="Section.TLabel").pack(anchor="w")
        ttk.Separator(sec, orient="horizontal").pack(fill="x", pady=(2, 10))

        r = ttk.Frame(sec)
        r.pack(fill="x", padx=8, pady=4)
        self.quotation_no = self._field(r, "Quotation No", 0, 0, default="ATC/2025-26/001", width=20)
        self.place_of_supply = self._field(r, "Place of Supply", 0, 2, default="Maharashtra", width=20)

        r2 = ttk.Frame(sec)
        r2.pack(fill="x", padx=8, pady=4)
        ttk.Label(r2, text="Date:").grid(row=0, column=0, sticky="w")
        self.date_entry = ttk.Entry(r2, width=15)
        self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.date_entry.grid(row=0, column=1, padx=(4, 16), sticky="w")

        ttk.Label(r2, text="Payment Terms:").grid(row=0, column=2, sticky="w")
        self.payment_terms = ttk.Combobox(r2, values=PAYMENT_OPTIONS, width=18, state="readonly")
        self.payment_terms.set("100% Advance")
        self.payment_terms.grid(row=0, column=3, padx=(4, 16), sticky="w")

        ttk.Label(r2, text="Validity:").grid(row=0, column=4, sticky="w")
        self.validity = ttk.Combobox(r2, values=VALIDITY_OPTIONS, width=12, state="readonly")
        self.validity.set("15 Days")
        self.validity.grid(row=0, column=5, padx=4, sticky="w")

        # ── Bill To / Ship To ──────────────────────────────────────
        sec = ttk.Frame(f)
        sec.pack(fill="x", padx=20, pady=(15, 5))
        ttk.Label(sec, text="📬 Bill To / Ship To", style="Section.TLabel").pack(anchor="w")
        ttk.Separator(sec, orient="horizontal").pack(fill="x", pady=(2, 10))

        cols = ttk.Frame(sec)
        cols.pack(fill="x", padx=8, pady=4)

        # Bill To
        bf = ttk.LabelFrame(cols, text="Bill To")
        bf.pack(side="left", fill="both", expand=True, padx=(0, 4))
        self.bill_name = self._field(bf, "Name", 0, 0, width=35, pad=4)
        ttk.Label(bf, text="Address:").grid(row=1, column=0, sticky="nw", padx=4)
        self.bill_addr = tk.Text(bf, width=38, height=3, font=("Segoe UI", 9))
        self.bill_addr.grid(row=1, column=1, padx=4, pady=2, sticky="w")

        # Ship To
        sf = ttk.LabelFrame(cols, text="Ship To")
        sf.pack(side="left", fill="both", expand=True, padx=(4, 0))

        self.same_as_bill = tk.BooleanVar(value=True)
        ttk.Checkbutton(sf, text="Same as Bill To", variable=self.same_as_bill,
                        command=self._toggle_ship).grid(row=0, column=0, columnspan=2, sticky="w", padx=4)
        self.ship_name = self._field(sf, "Name", 1, 0, width=35, pad=4)
        ttk.Label(sf, text="Address:").grid(row=2, column=0, sticky="nw", padx=4)
        self.ship_addr = tk.Text(sf, width=38, height=3, font=("Segoe UI", 9))
        self.ship_addr.grid(row=2, column=1, padx=4, pady=2, sticky="w")
        self._toggle_ship()

        # ── Line Items ─────────────────────────────────────────────
        sec = ttk.Frame(f)
        sec.pack(fill="x", padx=20, pady=(15, 5))
        ttk.Label(sec, text="🛒 Line Items", style="Section.TLabel").pack(anchor="w")
        ttk.Separator(sec, orient="horizontal").pack(fill="x", pady=(2, 10))

        # Header
        hdr = ttk.Frame(sec)
        hdr.pack(fill="x", padx=8, pady=(4, 0))
        for col, (txt, w) in enumerate([("#", 4), ("Description", 35), ("Qty", 6),
                                         ("Unit Price", 12), ("GST %", 6), ("Total", 12), ("", 4)]):
            ttk.Label(hdr, text=txt, font=("Segoe UI", 9, "bold"), width=w).grid(row=0, column=col, padx=2)

        self.items_frame = ttk.Frame(sec)
        self.items_frame.pack(fill="x", padx=8)

        btn_row = ttk.Frame(sec)
        btn_row.pack(fill="x", padx=8, pady=4)
        ttk.Button(btn_row, text="➕ Add Item", command=self._add_item).pack(side="left")

        # Add first item
        self._add_item()

        # ── Bank Details ───────────────────────────────────────────
        sec = ttk.Frame(f)
        sec.pack(fill="x", padx=20, pady=(15, 5))
        ttk.Label(sec, text="🏦 Bank Details", style="Section.TLabel").pack(anchor="w")
        ttk.Separator(sec, orient="horizontal").pack(fill="x", pady=(2, 10))

        r = ttk.Frame(sec)
        r.pack(fill="x", padx=8, pady=4)
        self.bank_name = self._field(r, "Account Name", 0, 0, default="ARROWTECH COMPUTER", width=25)
        self.bank_number = self._field(r, "Account No", 0, 2, default="50200100181071", width=20)

        r2 = ttk.Frame(sec)
        r2.pack(fill="x", padx=8, pady=4)
        self.bank_ifsc = self._field(r2, "IFSC", 0, 0, default="HDFC0001785", width=15)
        self.bank_branch = self._field(r2, "Branch", 0, 2, default="Jalgaon Dana Bazaar", width=25)
        self.bank_upi = self._field(r2, "UPI", 0, 4, default="9579488300@hdfcbank", width=25)

        # ── Terms & Conditions ─────────────────────────────────────
        sec = ttk.Frame(f)
        sec.pack(fill="x", padx=20, pady=(15, 5))
        ttk.Label(sec, text="📜 Terms & Conditions", style="Section.TLabel").pack(anchor="w")
        ttk.Separator(sec, orient="horizontal").pack(fill="x", pady=(2, 10))

        self.terms_frame = ttk.Frame(sec)
        self.terms_frame.pack(fill="x", padx=8)

        btn_row = ttk.Frame(sec)
        btn_row.pack(fill="x", padx=8, pady=4)
        ttk.Button(btn_row, text="➕ Add Term", command=self._add_term).pack(side="left")

        for t in DEFAULT_TERMS:
            self._add_term(t)

        # ── Action Buttons ─────────────────────────────────────────
        ttk.Separator(f, orient="horizontal").pack(fill="x", padx=20, pady=(15, 10))
        
        action_frame = ttk.Frame(f)
        action_frame.pack(fill="x", padx=20, pady=(0, 15))

        ttk.Button(action_frame, text="🖨️  Open in Browser & Print",
                   command=self._open_in_browser, style="Action.TButton").pack(side="left", padx=4)
        ttk.Button(action_frame, text="💾  Save HTML File",
                   command=self._save_html, style="Action.TButton").pack(side="left", padx=4)

        # Status bar
        self.status = ttk.Label(f, text="Ready", foreground="gray", font=("Segoe UI", 9))
        self.status.pack(pady=(0, 8))

    # ── HELPERS ────────────────────────────────────────────────────
    def _field(self, parent, label, row, col, default="", width=20, pad=4):
        ttk.Label(parent, text=f"{label}:").grid(row=row, column=col, sticky="w", padx=pad)
        entry = ttk.Entry(parent, width=width)
        entry.insert(0, default)
        entry.grid(row=row, column=col + 1, padx=(4, 16), sticky="w")
        return entry

    def _pick_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            with open(path, "rb") as f:
                self.logo_base64 = base64.b64encode(f.read()).decode("utf-8")
            self.logo_label.config(text=os.path.basename(path), foreground="green")

    def _toggle_ship(self):
        state = "disabled" if self.same_as_bill.get() else "normal"
        self.ship_name.config(state=state)
        self.ship_addr.config(state=state)

    # ── LINE ITEMS ─────────────────────────────────────────────────
    def _add_item(self):
        idx = len(self.item_rows)
        row_frame = ttk.Frame(self.items_frame)
        row_frame.pack(fill="x", pady=1)

        num = ttk.Label(row_frame, text=str(idx + 1), width=4)
        num.grid(row=0, column=0, padx=2)

        desc = ttk.Entry(row_frame, width=35)
        desc.grid(row=0, column=1, padx=2)

        qty = ttk.Spinbox(row_frame, from_=1, to=9999, width=5)
        qty.set(1)
        qty.grid(row=0, column=2, padx=2)

        price = ttk.Entry(row_frame, width=12)
        price.insert(0, "0.00")
        price.grid(row=0, column=3, padx=2)

        gst = ttk.Combobox(row_frame, values=GST_OPTIONS, width=5, state="readonly")
        gst.set("18")
        gst.grid(row=0, column=4, padx=2)

        total_lbl = ttk.Label(row_frame, text="0.00", width=12, anchor="e")
        total_lbl.grid(row=0, column=5, padx=2)

        del_btn = ttk.Button(row_frame, text="✕", width=3, style="Delete.TButton",
                             command=lambda: self._remove_item(row_frame))
        del_btn.grid(row=0, column=6, padx=2)

        # Auto-calculate on change
        for widget in (qty, price, gst):
            widget.bind("<KeyRelease>", lambda e, q=qty, p=price, g=gst, t=total_lbl: self._calc_row(q, p, g, t))
            widget.bind("<<ComboboxSelected>>", lambda e, q=qty, p=price, g=gst, t=total_lbl: self._calc_row(q, p, g, t))

        self.item_rows.append({
            "frame": row_frame, "num": num, "desc": desc,
            "qty": qty, "price": price, "gst": gst, "total": total_lbl
        })

    def _remove_item(self, frame):
        if len(self.item_rows) <= 1:
            return
        self.item_rows = [r for r in self.item_rows if r["frame"] != frame]
        frame.destroy()
        # Re-number
        for i, r in enumerate(self.item_rows):
            r["num"].config(text=str(i + 1))

    def _calc_row(self, qty_w, price_w, gst_w, total_w):
        try:
            q = float(qty_w.get())
            p = float(price_w.get())
            g = float(gst_w.get())
            total = q * p * (1 + g / 100)
            total_w.config(text=f"{total:,.2f}")
        except ValueError:
            total_w.config(text="—")

    # ── TERMS ──────────────────────────────────────────────────────
    def _add_term(self, text=""):
        row_frame = ttk.Frame(self.terms_frame)
        row_frame.pack(fill="x", pady=1)

        entry = ttk.Entry(row_frame, width=70)
        entry.insert(0, text)
        entry.pack(side="left", padx=(0, 4))

        ttk.Button(row_frame, text="✕", width=3, style="Delete.TButton",
                   command=lambda: self._remove_term(row_frame)).pack(side="left")

        self.term_rows.append({"frame": row_frame, "entry": entry})

    def _remove_term(self, frame):
        if len(self.term_rows) <= 1:
            return
        self.term_rows = [r for r in self.term_rows if r["frame"] != frame]
        frame.destroy()

    # ── DATA COLLECTION ────────────────────────────────────────────
    def _collect_data(self):
        items = []
        for r in self.item_rows:
            items.append({
                "description": r["desc"].get(),
                "qty": int(float(r["qty"].get())) if r["qty"].get() else 1,
                "unit_price": float(r["price"].get()) if r["price"].get() else 0,
                "gst_percent": int(r["gst"].get()) if r["gst"].get() else 18,
            })

        terms = [r["entry"].get() for r in self.term_rows if r["entry"].get().strip()]

        ship_name = self.bill_name.get() if self.same_as_bill.get() else self.ship_name.get()
        ship_addr = self.bill_addr.get("1.0", "end").strip() if self.same_as_bill.get() else self.ship_addr.get("1.0", "end").strip()

        return {
            "company_name": self.company_name.get(),
            "company_address": self.company_address.get(),
            "company_zip": self.company_zip.get(),
            "company_phone": self.company_phone.get(),
            "logo_base64": self.logo_base64,
            "quotation_no": self.quotation_no.get(),
            "date": self.date_entry.get(),
            "place_of_supply": self.place_of_supply.get(),
            "payment_terms": self.payment_terms.get(),
            "validity": self.validity.get(),
            "bill_to_name": self.bill_name.get(),
            "bill_to_address": self.bill_addr.get("1.0", "end").strip(),
            "ship_to_name": ship_name,
            "ship_to_address": ship_addr,
            "items": items,
            "bank_account_name": self.bank_name.get(),
            "bank_account_number": self.bank_number.get(),
            "bank_ifsc": self.bank_ifsc.get(),
            "bank_branch": self.bank_branch.get(),
            "bank_upi": self.bank_upi.get(),
            "terms": terms,
        }

    def _generate_html(self):
        data = self._collect_data()
        return render_html(data), data

    # ── ACTIONS ────────────────────────────────────────────────────
    def _open_in_browser(self):
        try:
            html, data = self._generate_html()
            safe_name = data["quotation_no"].replace("/", "_")
            filename = f"Quotation_{safe_name}.html"
            path = os.path.join(OUTPUT_DIR, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            webbrowser.open(f"file:///{path.replace(os.sep, '/')}")
            self.status.config(text=f"✅ Opened: {filename}  —  Press Ctrl+P in browser to print/save as PDF", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _save_html(self):
        try:
            html, data = self._generate_html()
            safe_name = data["quotation_no"].replace("/", "_")
            default_name = f"Quotation_{safe_name}.html"
            path = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html")],
                initialfile=default_name,
            )
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)
                self.status.config(text=f"✅ Saved: {path}", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuotationApp(root)
    root.mainloop()

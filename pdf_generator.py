"""
pdf_generator.py
Renders quotation data into HTML using Jinja2.
"""

import os
import sys
from jinja2 import Environment, FileSystemLoader


# Support PyInstaller bundled path
if getattr(sys, 'frozen', False):
    TEMPLATE_DIR = sys._MEIPASS
else:
    TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))


def render_html(data: dict) -> str:
    """
    Render the quotation HTML from Jinja2 template with the provided data.
    
    Args:
        data: Dictionary containing all quotation fields:
            - company_name, company_address, company_zip, company_phone
            - logo_base64 (optional)
            - quotation_no, date, place_of_supply, payment_terms, validity
            - bill_to_name, bill_to_address
            - ship_to_name, ship_to_address
            - items: list of dicts with description, qty, unit_price, gst_percent
            - bank_account_name, bank_account_number, bank_ifsc, bank_branch, bank_upi
            - terms: list of strings
    
    Returns:
        Rendered HTML string
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("template.html")

    # Calculate item-level values
    items = []
    subtotal = 0.0
    total_gst = 0.0

    for item in data.get("items", []):
        qty = float(item.get("qty", 0))
        unit_price = float(item.get("unit_price", 0))
        gst_percent = float(item.get("gst_percent", 18))

        base_amount = qty * unit_price
        gst_amount = base_amount * gst_percent / 100
        total = base_amount + gst_amount

        items.append({
            "description": item.get("description", ""),
            "qty": int(qty) if qty == int(qty) else qty,
            "unit_price": unit_price,
            "gst_percent": int(gst_percent) if gst_percent == int(gst_percent) else gst_percent,
            "gst_amount": round(gst_amount, 2),
            "total": round(total, 2),
        })

        subtotal += base_amount
        total_gst += gst_amount

    grand_total = subtotal + total_gst

    # Build template context
    context = {
        **data,
        "items": items,
        "subtotal": round(subtotal, 2),
        "total_gst": round(total_gst, 2),
        "grand_total": round(grand_total, 2),
    }

    return template.render(**context)

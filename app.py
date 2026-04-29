"""
app.py
Streamlit-based Quotation Generator UI.
Run with: streamlit run app.py
"""

import os
import base64
import streamlit as st
from datetime import date
from pdf_generator import render_html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ─── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Quotation Generator",
    page_icon="📄",
    layout="wide",
)

# ─── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background & font */
    .stApp {
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        margin: 16px 0 10px 0;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Item row card */
    .item-card {
        background: #f8f9fc;
        border: 1px solid #e2e4ea;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 32px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        letter-spacing: 0.5px;
        width: 100%;
    }

    /* Computed values */
    .computed-value {
        background: #e8f5e9;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        color: #2e7d32;
        display: inline-block;
        margin: 2px 0;
    }

    .grand-total-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #fff;
        padding: 14px 20px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: 700;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State Initialization ──────────────────────────────────
if "line_items" not in st.session_state:
    st.session_state.line_items = [
        {"description": "", "qty": 1, "unit_price": 0.0, "gst_percent": 18}
    ]

if "terms" not in st.session_state:
    st.session_state.terms = [
        "100% advance payment",
        "Delivery within 2–5 days",
        "Extra charges if applicable",
        "Warranty as per manufacturer",
        "GST included",
        "Valid for 15 days",
    ]

GST_OPTIONS = [0, 5, 12, 18, 28]
PAYMENT_TERMS_OPTIONS = ["100% Advance", "50% Advance", "Net 30", "Net 60"]
VALIDITY_OPTIONS = ["7 Days", "15 Days", "30 Days", "45 Days"]


# ─── Helper Functions ──────────────────────────────────────────────
def add_item():
    st.session_state.line_items.append(
        {"description": "", "qty": 1, "unit_price": 0.0, "gst_percent": 18}
    )

def remove_item(idx):
    if len(st.session_state.line_items) > 1:
        st.session_state.line_items.pop(idx)

def add_term():
    st.session_state.terms.append("")

def remove_term(idx):
    if len(st.session_state.terms) > 1:
        st.session_state.terms.pop(idx)


# ─── Title ─────────────────────────────────────────────────────────
st.markdown("# 📄 Quotation Generator")
st.markdown("Fill in the details below and generate a professional PDF quotation.")


# ═══════════════════════════════════════════════════════════════════
# COMPANY DETAILS & LOGO
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🏢 Company Details</div>', unsafe_allow_html=True)

cc1, cc2, cc3, cc4 = st.columns(4)
with cc1:
    company_name = st.text_input("Company Name", value="ARROWTECH COMPUTER")
with cc2:
    company_address = st.text_input("Address", value="C-173, 1st Floor, Golani Market, Jalgaon")
with cc3:
    company_zip = st.text_input("ZIP Code", value="425001")
with cc4:
    company_phone = st.text_input("Phone", value="9579488300")

logo_base64 = None
with st.expander("🖼️ Upload Company Logo (Optional)"):
    logo_file = st.file_uploader("Upload logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode("utf-8")
        st.image(logo_file, width=150, caption="Logo preview")


# ═══════════════════════════════════════════════════════════════════
# QUOTATION DETAILS
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📋 Quotation Details</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    quotation_no = st.text_input("Quotation No", value="ATC/2025-26/001")
    place_of_supply = st.text_input("Place of Supply", value="Maharashtra")
with col2:
    quotation_date = st.date_input("Date", value=date.today())
    payment_terms = st.selectbox("Payment Terms", PAYMENT_TERMS_OPTIONS, index=0)
with col3:
    validity = st.selectbox("Validity", VALIDITY_OPTIONS, index=1)


# ─── Bill To / Ship To ────────────────────────────────────────────
st.markdown('<div class="section-header">📬 Bill To / Ship To</div>', unsafe_allow_html=True)

col_bill, col_ship = st.columns(2)

with col_bill:
    st.markdown("**Bill To**")
    bill_to_name = st.text_input("Company / Customer Name", value="", key="bill_name")
    bill_to_address = st.text_area("Address", value="", height=80, key="bill_addr")

with col_ship:
    st.markdown("**Ship To**")
    same_as_bill = st.checkbox("Same as Bill To", value=True)
    if same_as_bill:
        ship_to_name = bill_to_name
        ship_to_address = bill_to_address
        st.text_input("Company / Customer Name", value=bill_to_name, key="ship_name", disabled=True)
        st.text_area("Address", value=bill_to_address, height=80, key="ship_addr", disabled=True)
    else:
        ship_to_name = st.text_input("Company / Customer Name", value="", key="ship_name")
        ship_to_address = st.text_area("Address", value="", height=80, key="ship_addr")


# ─── Line Items ───────────────────────────────────────────────────
st.markdown('<div class="section-header">🛒 Line Items</div>', unsafe_allow_html=True)

# Column headers
hcol1, hcol2, hcol3, hcol4, hcol5, hcol6, hcol7 = st.columns([0.4, 3, 0.8, 1.2, 0.8, 1.2, 0.5])
with hcol1:
    st.markdown("**#**")
with hcol2:
    st.markdown("**Description**")
with hcol3:
    st.markdown("**Qty**")
with hcol4:
    st.markdown("**Unit Price (₹)**")
with hcol5:
    st.markdown("**GST %**")
with hcol6:
    st.markdown("**Total (₹)**")
with hcol7:
    st.markdown("**🗑️**")

subtotal = 0.0
total_gst = 0.0
items_data = []

for i, item in enumerate(st.session_state.line_items):
    c1, c2, c3, c4, c5, c6, c7 = st.columns([0.4, 3, 0.8, 1.2, 0.8, 1.2, 0.5])

    with c1:
        st.markdown(f"**{i + 1}**")

    with c2:
        desc = st.text_input(
            "desc", value=item["description"], key=f"desc_{i}",
            label_visibility="collapsed", placeholder="Item description"
        )

    with c3:
        qty = st.number_input(
            "qty", min_value=1, value=int(item["qty"]), key=f"qty_{i}",
            label_visibility="collapsed"
        )

    with c4:
        price = st.number_input(
            "price", min_value=0.0, value=float(item["unit_price"]),
            key=f"price_{i}", label_visibility="collapsed", format="%.2f"
        )

    with c5:
        gst_idx = GST_OPTIONS.index(item["gst_percent"]) if item["gst_percent"] in GST_OPTIONS else 3
        gst = st.selectbox(
            "gst", GST_OPTIONS, index=gst_idx, key=f"gst_{i}",
            label_visibility="collapsed", format_func=lambda x: f"{x}%"
        )

    # Calculate
    base = qty * price
    gst_amt = base * gst / 100
    row_total = base + gst_amt
    subtotal += base
    total_gst += gst_amt

    with c6:
        st.markdown(f"<div class='computed-value'>₹ {row_total:,.2f}</div>", unsafe_allow_html=True)

    with c7:
        if len(st.session_state.line_items) > 1:
            st.button("✕", key=f"del_{i}", on_click=remove_item, args=(i,), type="secondary")

    # Update session state
    st.session_state.line_items[i] = {
        "description": desc, "qty": qty, "unit_price": price, "gst_percent": gst
    }
    items_data.append(st.session_state.line_items[i])

grand_total = subtotal + total_gst

# Add item button
st.button("➕ Add Item", on_click=add_item, type="primary")

# Totals display
st.markdown("---")
tcol1, tcol2, tcol3 = st.columns(3)
with tcol1:
    st.metric("Subtotal", f"₹ {subtotal:,.2f}")
with tcol2:
    st.metric("Total GST", f"₹ {total_gst:,.2f}")
with tcol3:
    st.markdown(f'<div class="grand-total-box">Grand Total: ₹ {grand_total:,.2f}</div>', unsafe_allow_html=True)


# ─── Terms & Conditions ───────────────────────────────────────────
st.markdown('<div class="section-header">📜 Terms & Conditions</div>', unsafe_allow_html=True)

updated_terms = []
for i, term in enumerate(st.session_state.terms):
    tcol1, tcol2 = st.columns([10, 1])
    with tcol1:
        val = st.text_input(
            f"Term {i+1}", value=term, key=f"term_{i}",
            label_visibility="collapsed", placeholder=f"Term {i+1}"
        )
        updated_terms.append(val)
    with tcol2:
        if len(st.session_state.terms) > 1:
            st.button("✕", key=f"del_term_{i}", on_click=remove_term, args=(i,), type="secondary")

st.session_state.terms = updated_terms
st.button("➕ Add Term", on_click=add_term, type="secondary")


# ═══════════════════════════════════════════════════════════════════
# BANK DETAILS
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🏦 Bank Details</div>', unsafe_allow_html=True)

bc1, bc2, bc3 = st.columns(3)
with bc1:
    bank_account_name = st.text_input("Account Name", value="ARROWTECH COMPUTER", key="bank_name")
    bank_account_number = st.text_input("Account Number", value="50200100181071")
with bc2:
    bank_ifsc = st.text_input("IFSC Code", value="HDFC0001785")
    bank_branch = st.text_input("Branch", value="Jalgaon Dana Bazaar")
with bc3:
    bank_upi = st.text_input("UPI ID", value="9579488300@hdfcbank")


# ═══════════════════════════════════════════════════════════════════
# GENERATE & PRINT
# ═══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-header">📥 Generate Quotation</div>', unsafe_allow_html=True)

# Filter out empty terms
final_terms = [t for t in st.session_state.terms if t.strip()]

# Build data dict
quotation_data = {
    "company_name": company_name,
    "company_address": company_address,
    "company_zip": company_zip,
    "company_phone": company_phone,
    "logo_base64": logo_base64,
    "quotation_no": quotation_no,
    "date": quotation_date.strftime("%d/%m/%Y"),
    "place_of_supply": place_of_supply,
    "payment_terms": payment_terms,
    "validity": validity,
    "bill_to_name": bill_to_name,
    "bill_to_address": bill_to_address,
    "ship_to_name": ship_to_name,
    "ship_to_address": ship_to_address,
    "items": items_data,
    "bank_account_name": bank_account_name,
    "bank_account_number": bank_account_number,
    "bank_ifsc": bank_ifsc,
    "bank_branch": bank_branch,
    "bank_upi": bank_upi,
    "terms": final_terms,
}

html_output = render_html(quotation_data)
safe_name = quotation_no.replace("/", "_")
filename_base = f"Quotation_{safe_name}_{quotation_date.strftime('%Y%m%d')}"

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("🔍 Preview", use_container_width=True, type="secondary"):
        st.session_state.show_preview = True

with col_b:
    # Save HTML and open in browser for printing (Ctrl+P → Save as PDF)
    if st.button("🖨️ Open in Browser & Print", use_container_width=True, type="primary"):
        import webbrowser
        output_path = os.path.join(SCRIPT_DIR, f"{filename_base}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        webbrowser.open(f"file:///{output_path.replace(os.sep, '/')}")
        st.success(f"✅ Opened in browser — use **Ctrl+P** to Print or Save as PDF")

with col_c:
    st.download_button(
        label="💾 Download HTML",
        data=html_output.encode("utf-8"),
        file_name=f"{filename_base}.html",
        mime="text/html",
        use_container_width=True,
    )

st.info("💡 **Tip:** Click **Open in Browser & Print** → then press **Ctrl+P** → choose **Save as PDF** for a pixel-perfect PDF.")

# Preview area
if st.session_state.get("show_preview", False):
    st.markdown("---")
    st.markdown("### Preview")
    st.components.v1.html(html_output, height=900, scrolling=True)


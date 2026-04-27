#!/usr/bin/env python3
"""
BillSathi Branding Replacement Script
Replaces ALL InvoicePro branding with BillSathi across every HTML file.
Handles: sidebar, navbar, login pages, PDF invoice header, favicon, and title tags.
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# FAVICON TAG — inject into <head> if missing, or replace existing
# ─────────────────────────────────────────────────────────────────────────────
FAVICON_TAG = '<link rel="icon" type="image/png" href="assets/favicon.png" />'

# ─────────────────────────────────────────────────────────────────────────────
# LOGO HTML SNIPPETS (used as replacement targets)
# ─────────────────────────────────────────────────────────────────────────────

# The inline CSS for sidebar logo (replaces .sb-logo-mark SVG approach)
SIDEBAR_LOGO_CSS = """        /* BillSathi Logo */
        .sb-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 14px 16px 13px;
            border-bottom: 1px solid var(--line);
            flex-shrink: 0;
            text-decoration: none;
        }
        .sb-logo-img {
            height: 34px;
            width: auto;
            object-fit: contain;
            display: block;
        }
        .sb-logo-name {
            font-size: 15px;
            font-weight: 700;
            color: var(--t1);
            letter-spacing: -.4px;
        }
        .sb-logo-name em {
            color: var(--brand);
            font-style: normal;
        }"""

# Full-logo (icon+wordmark) sidebar HTML
SIDEBAR_LOGO_HTML = '''<img src="assets/logo.png" alt="BillSathi" class="sb-logo-img" />'''

# Navbar logo HTML (for index, features, pricing, etc.)
NAVBAR_LOGO_HTML = '''<img src="assets/logo.png" alt="BillSathi" style="height:38px;width:auto;object-fit:contain;display:block;" />'''

# Login/signup page logo (larger, centered or left-aligned)
LOGIN_LOGO_HTML = '''<img src="assets/logo.png" alt="BillSathi" style="height:48px;width:auto;object-fit:contain;display:block;" />'''

# Left panel logo (customer-login.html)
LEFT_PANEL_LOGO_HTML = '''<img src="assets/logo.png" alt="BillSathi" style="height:44px;width:auto;object-fit:contain;display:block;" />'''

# PDF invoice header logo (base64 or img tag in builder.html print section)
PDF_LOGO_HTML = '''<img src="assets/logo.png" alt="BillSathi" style="height:52px;width:auto;object-fit:contain;display:block;max-width:220px;" />'''


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Written: {os.path.basename(path)}")

def ensure_favicon(html):
    """Inject/replace favicon link tag in <head>."""
    # Remove existing favicon links
    html = re.sub(r'<link[^>]+rel=["\'](?:shortcut )?icon["\'][^>]*/?\s*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<link[^>]+href=["\'][^"\']*favicon[^"\']*["\'][^>]*/?\s*>', '', html, flags=re.IGNORECASE)
    # Inject after <meta charset ...>
    if FAVICON_TAG not in html:
        html = re.sub(r'(<meta\s+charset[^>]+>)', r'\1\n    ' + FAVICON_TAG, html, count=1, flags=re.IGNORECASE)
    return html

def replace_titles(html):
    """Replace page titles — swap InvoicePro → BillSathi."""
    html = re.sub(r'InvoicePro\s*[—–-]\s*', 'BillSathi — ', html)
    html = re.sub(r'InvoicePro', 'BillSathi', html)
    return html

def replace_meta_descriptions(html):
    """Update meta descriptions."""
    html = re.sub(
        r'(content="[^"]*?)InvoicePro([^"]*")',
        r'\1BillSathi\2',
        html, flags=re.IGNORECASE
    )
    return html


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN REPLACERS — sidebar, navbar, login, PDF
# ─────────────────────────────────────────────────────────────────────────────

def replace_sidebar_logo_css(html):
    """Replace .sb-logo-mark CSS block with image-based logo CSS."""
    # Replace the entire logo CSS block (from /* Logo */ comment to end of .sb-logo-name em)
    pattern = re.compile(
        r'/\*\s*Logo\s*\*/\s*'
        r'\.sb-logo\s*\{[^}]*\}\s*'
        r'\.sb-logo-mark\s*\{[^}]*\}\s*'
        r'\.sb-logo-mark\s+svg\s*\{[^}]*\}\s*'
        r'\.sb-logo-name\s*\{[^}]*\}\s*'
        r'\.sb-logo-name\s+em\s*\{[^}]*\}',
        re.DOTALL
    )
    if pattern.search(html):
        html = pattern.sub(SIDEBAR_LOGO_CSS, html, count=1)
    return html

def replace_sidebar_logo_html(html):
    """Replace sidebar logo markup (sb-logo-mark div + sb-logo-name span) with img tag."""
    # Pattern: <div class="sb-logo-mark">...</div>\n...<span/div class="sb-logo-name">Invoice<em>Pro</em></span/div>
    pattern = re.compile(
        r'<div\s+class="sb-logo-mark">.*?</div>\s*'
        r'(?:<span|<div)[^>]*class="sb-logo-name"[^>]*>.*?(?:</span>|</div>)',
        re.DOTALL
    )
    if pattern.search(html):
        html = pattern.sub(SIDEBAR_LOGO_HTML, html, count=1)
    return html

def replace_navbar_logo_icon(html, is_login=False, is_left_panel=False):
    """Replace .logo-icon SVG + text with BillSathi img tag inside .logo anchors."""
    img = LEFT_PANEL_LOGO_HTML if is_left_panel else (LOGIN_LOGO_HTML if is_login else NAVBAR_LOGO_HTML)

    # Pattern 1: <div class="logo-icon">...</div>Invoice<em>Pro</em>  (with optional whitespace/newlines)
    pattern1 = re.compile(
        r'<div\s+class="logo-icon"[^>]*>.*?</div>\s*Invoice\s*<em>Pro</em>',
        re.DOTALL
    )
    if pattern1.search(html):
        html = pattern1.sub(img, html)
        return html

    # Pattern 2: <div class="logo-icon">...</div>BillSathi (already partly replaced)
    pattern2 = re.compile(
        r'<div\s+class="logo-icon"[^>]*>.*?</div>\s*(?:Invoice\s*<em>Pro</em>|BillSathi)',
        re.DOTALL
    )
    if pattern2.search(html):
        html = pattern2.sub(img, html)
    return html

def replace_left_logo_panel(html):
    """Replace .left-logo content (customer-login.html left panel logo)."""
    # The left-logo <a> contains: <div class="li">SVG</div><span>Invoice</span><em>Pro</em>
    pattern = re.compile(
        r'(<a[^>]+class="left-logo"[^>]*>)\s*'
        r'(?:<div[^>]*class="li"[^>]*>.*?</div>|<div[^>]*>.*?</div>)?\s*'
        r'(?:Invoice\s*<em>Pro</em>|<span[^>]*>.*?</span>\s*(?:<em>.*?</em>)?)',
        re.DOTALL
    )
    if pattern.search(html):
        html = pattern.sub(r'\1\n            ' + LEFT_PANEL_LOGO_HTML, html)
    return html

def replace_pdf_logo(html):
    """Replace PDF/print invoice header logo."""
    # Look for invoice header SVG logo in print/builder context
    # Pattern: <div ...invoice-logo...> or similar
    pattern_div = re.compile(
        r'(<div[^>]*(?:invoice-logo|pdf-logo|inv-logo|logo-wrap)[^>]*>).*?(</div>)',
        re.DOTALL | re.IGNORECASE
    )
    if pattern_div.search(html):
        html = pattern_div.sub(r'\1' + PDF_LOGO_HTML + r'\2', html)

    # Also look for the invoice header brand text in PDF
    # Pattern: <span class="brand">Invoice<em>Pro</em></span> or similar in print section
    pattern_brand = re.compile(
        r'(<(?:span|div|h1|h2)[^>]*(?:brand|company-name|inv-brand)[^>]*>)\s*Invoice\s*(?:<em>)?Pro(?:</em>)?\s*(</(?:span|div|h1|h2)>)',
        re.DOTALL | re.IGNORECASE
    )
    if pattern_brand.search(html):
        html = pattern_brand.sub(r'\1BillSathi\2', html)

    return html

def replace_css_logo_icon_block(html):
    """Replace CSS .logo-icon block (used in navbar pages) with img-friendly rules."""
    # Keep .logo class, but update .logo-icon to be an img container
    pattern = re.compile(
        r'\.logo-icon\s*\{[^}]*\}\s*'
        r'(?:\.logo:hover\s+\.logo-icon\s*\{[^}]*\}\s*)?'
        r'(?:\.logo-icon\s+svg\s*\{[^}]*\}\s*)?',
        re.DOTALL
    )
    replacement = (
        '.logo-img { height: 38px; width: auto; object-fit: contain; display: block; }\n'
    )
    if pattern.search(html):
        html = pattern.sub(replacement, html, count=1)
    return html

def replace_sb_logo_name_text(html):
    """Catch any remaining Invoice<em>Pro</em> inside sb-logo-name."""
    html = re.sub(r'Invoice<em>Pro</em>', 'BillSathi', html)
    html = re.sub(r'Invoice\s*<em>\s*Pro\s*</em>', 'BillSathi', html)
    return html


# ─────────────────────────────────────────────────────────────────────────────
# FILE-SPECIFIC HANDLERS
# ─────────────────────────────────────────────────────────────────────────────

def process_dashboard_billing(path):
    """dashboard.html, billing-history.html, my-bills.html — sidebar pages."""
    html = read(path)
    html = ensure_favicon(html)
    html = replace_titles(html)
    html = replace_sidebar_logo_css(html)
    html = replace_sidebar_logo_html(html)
    html = replace_sb_logo_name_text(html)
    write(path, html)

def process_navbar_page(path, is_login=False):
    """index.html, features.html, pricing.html, how-it-works.html, templates.html, login.html, signup.html."""
    html = read(path)
    html = ensure_favicon(html)
    html = replace_titles(html)
    html = replace_meta_descriptions(html)
    html = replace_css_logo_icon_block(html)
    html = replace_navbar_logo_icon(html, is_login=is_login)
    html = replace_sb_logo_name_text(html)
    write(path, html)

def process_login(path):
    """login.html, signup.html — auth pages."""
    process_navbar_page(path, is_login=True)

def process_customer_login(path):
    """customer-login.html — left panel logo."""
    html = read(path)
    html = ensure_favicon(html)
    html = replace_titles(html)
    html = replace_css_logo_icon_block(html)
    html = replace_left_logo_panel(html)
    html = replace_navbar_logo_icon(html, is_left_panel=True)
    html = replace_sb_logo_name_text(html)
    write(path, html)

def process_builder(path):
    """builder.html — sidebar + PDF invoice header."""
    html = read(path)
    html = ensure_favicon(html)
    html = replace_titles(html)
    html = replace_sidebar_logo_css(html)
    html = replace_sidebar_logo_html(html)
    html = replace_pdf_logo(html)
    html = replace_sb_logo_name_text(html)
    write(path, html)

def process_simple_page(path):
    """gdpr.html, privacy.html, terms.html, cookies.html — simple nav pages."""
    html = read(path)
    html = ensure_favicon(html)
    html = replace_titles(html)
    html = replace_css_logo_icon_block(html)
    html = replace_navbar_logo_icon(html)
    html = replace_sb_logo_name_text(html)
    write(path, html)

def process_business_page(path):
    """business-type.html, business-category.html, gst-verification.html."""
    html = read(path)
    html = ensure_favicon(html)
    html = replace_titles(html)
    html = replace_css_logo_icon_block(html)
    html = replace_navbar_logo_icon(html)
    html = replace_sb_logo_name_text(html)
    write(path, html)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("\n🚀 BillSathi Branding Replacement Starting...\n")

    # Sidebar/App pages
    for fname in ['dashboard.html', 'billing-history.html', 'my-bills.html']:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Sidebar] {fname}")
            process_dashboard_billing(p)

    # Builder (sidebar + PDF header)
    builder_path = os.path.join(BASE, 'builder.html')
    if os.path.exists(builder_path):
        print(f"[Builder+PDF] builder.html")
        process_builder(builder_path)

    # Auth pages (larger logo)
    for fname in ['login.html', 'signup.html']:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Login] {fname}")
            process_login(p)

    # Customer login (split panel)
    cl_path = os.path.join(BASE, 'customer-login.html')
    if os.path.exists(cl_path):
        print(f"[CustomerLogin] customer-login.html")
        process_customer_login(cl_path)

    # Public navbar pages
    for fname in ['index.html', 'features.html', 'pricing.html', 'how-it-works.html', 'templates.html']:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Navbar] {fname}")
            process_navbar_page(p)

    # Business flow pages
    for fname in ['business-type.html', 'business-category.html', 'gst-verification.html']:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Business] {fname}")
            process_business_page(p)

    # Simple legal/info pages
    for fname in ['gdpr.html', 'privacy.html', 'terms.html', 'cookies.html']:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Legal] {fname}")
            process_simple_page(p)

    print("\n✅ All files updated with BillSathi branding!\n")

if __name__ == '__main__':
    main()

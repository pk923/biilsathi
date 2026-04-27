#!/usr/bin/env python3
"""
Fix BillSathi Logo Display Issues Across All Pages.

Problems fixed:
  1. Old `.li` SVG box still present on login/signup pages (not replaced)
  2. Sidebar logo too small (34px → 44px height)  
  3. Navbar logo too small (38px → 44px height)
  4. Wrapper <a> has leftover font-size/gap CSS creating ghost spacing
  5. Login page `.left-logo .li` block CSS never cleaned
"""

import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    with open(p, encoding='utf-8') as f: return f.read()

def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)
    print(f"  ✅ Fixed: {os.path.basename(p)}")

# ─── CSS FIXES ───────────────────────────────────────────────────────────────

def fix_navbar_logo_css(html):
    """Fix .logo wrapper — remove font-size/gap that create ghost space.
       Logo <img> is the sole child so no gap/font needed."""
    # Replace .logo { display:flex; align-items:center; gap:...; font-size:...; ... }
    html = re.sub(
        r'(\.logo\s*\{[^}]*?)font-size\s*:\s*[^;]+;\s*',
        r'\1',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'(\.logo\s*\{[^}]*?)font-weight\s*:\s*[^;]+;\s*',
        r'\1',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'(\.logo\s*\{[^}]*?)color\s*:\s*var\(--ink\)\s*;\s*',
        r'\1',
        html, flags=re.DOTALL
    )
    # Set gap to 0 since logo img contains both icon+wordmark
    html = re.sub(
        r'(\.logo\s*\{[^}]*?)gap\s*:\s*[^;]+;',
        r'\1gap: 0;',
        html, flags=re.DOTALL
    )
    return html

def fix_logo_img_css(html):
    """Update .logo-img height to 44px (navbar), clean any box styling."""
    html = re.sub(
        r'\.logo-img\s*\{[^}]*\}',
        '.logo-img { height: 44px; width: auto; object-fit: contain; display: block; background: none; border: none; box-shadow: none; }',
        html, flags=re.DOTALL
    )
    return html

def fix_sb_logo_css(html):
    """Fix sidebar logo CSS — increase size, remove any bg/border from img."""
    # Update .sb-logo-img height
    html = re.sub(
        r'\.sb-logo-img\s*\{[^}]*\}',
        '.sb-logo-img { height: 44px; width: auto; object-fit: contain; display: block; max-width: 180px; background: none; border: none; box-shadow: none; }',
        html, flags=re.DOTALL
    )
    # Remove .sb-logo-mark leftover CSS if any
    html = re.sub(
        r'\.sb-logo-mark\s*\{[^}]*\}\s*',
        '',
        html, flags=re.DOTALL
    )
    # Remove .sb-logo-name if it exists (the img contains the full wordmark)
    # Actually keep it in case it's used elsewhere, just ensure it doesn't show
    return html

def fix_left_logo_css(html):
    """Fix .left-logo CSS on login/signup pages — remove .li box styles."""
    # Remove the old .li box CSS entirely
    html = re.sub(
        r'\.left-logo\s+\.li\s*\{[^}]*\}\s*',
        '',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'\.left-logo\s+\.li\s+svg\s*\{[^}]*\}\s*',
        '',
        html, flags=re.DOTALL
    )
    # Remove .left-logo span (text was "BillSathi") — img has full logo
    html = re.sub(
        r'\.left-logo\s+span\s*\{[^}]*\}\s*',
        '',
        html, flags=re.DOTALL
    )
    # Remove .left-logo em
    html = re.sub(
        r'\.left-logo\s+em\s*\{[^}]*\}\s*',
        '',
        html, flags=re.DOTALL
    )
    # Update .left-logo itself — remove gap (no text child anymore)
    html = re.sub(
        r'(\.left-logo\s*\{[^}]*?)gap\s*:\s*[^;]+;',
        r'\1gap: 0;',
        html, flags=re.DOTALL
    )
    # Add or update .left-logo-img
    if '.left-logo-img' not in html:
        html = re.sub(
            r'(\.left-logo\s*\{[^}]*\})',
            r'\1\n        .left-logo-img { height: 52px; width: auto; object-fit: contain; display: block; background: none; border: none; box-shadow: none; }',
            html, flags=re.DOTALL
        )
    else:
        html = re.sub(
            r'\.left-logo-img\s*\{[^}]*\}',
            '.left-logo-img { height: 52px; width: auto; object-fit: contain; display: block; background: none; border: none; box-shadow: none; }',
            html, flags=re.DOTALL
        )
    return html

# ─── HTML FIXES ──────────────────────────────────────────────────────────────

def fix_navbar_logo_html(html):
    """Replace img inline style with class, fix height to 44px."""
    # Fix inline-styled logo imgs (navbar pages)
    html = re.sub(
        r'(<img\s+src="assets/logo\.png"\s+alt="BillSathi"\s+)style="[^"]*"(\s*/?>)',
        r'\1class="logo-img"\2',
        html
    )
    return html

def fix_sb_logo_html(html):
    """Fix sidebar logo img — use class, remove inline styles."""
    html = re.sub(
        r'(<img\s+src="assets/logo\.png"\s+alt="BillSathi"\s+)class="sb-logo-img"(\s*/?>)',
        r'\1class="sb-logo-img"\2',
        html
    )
    return html

def fix_left_logo_html(html):
    """Replace old .li SVG box + span text with clean logo img in login/signup."""
    # Pattern: <div class="li"><svg ...>...</svg></div>\n<span>BillSathi</span>
    # OR: just the img already there but with wrong class/style
    
    # Remove leftover <div class="li"> SVG box if still present
    pattern_li = re.compile(
        r'<div\s+class="li"\s*>.*?</div>\s*',
        re.DOTALL
    )
    if pattern_li.search(html):
        html = pattern_li.sub('', html)
    
    # Remove leftover <span>BillSathi</span> or <span>Invoice...</span>
    pattern_span = re.compile(
        r'<span\s*>(?:BillSathi|Invoice(?:<em>)?Pro(?:</em>)?)\s*</span>\s*',
        re.DOTALL
    )
    if pattern_span.search(html):
        html = pattern_span.sub('', html)

    # Now fix the img inside .left-logo — replace inline style img or add it
    # Check if img already exists in left-logo
    # Replace img with class-based approach
    html = re.sub(
        r'(<a[^>]+class="left-logo"[^>]*>\s*)<img\s+src="assets/logo\.png"[^>]*/?>',
        r'\1<img src="assets/logo.png" alt="BillSathi" class="left-logo-img" />',
        html, flags=re.DOTALL
    )
    
    # If no img inside left-logo yet, inject it (after removing old content)
    # Check if the left-logo anchor is now empty or only has whitespace
    def inject_img_if_empty(m):
        inner = m.group(2)
        if 'left-logo-img' not in inner and 'logo.png' not in inner:
            return m.group(1) + '\n            <img src="assets/logo.png" alt="BillSathi" class="left-logo-img" />\n        ' + m.group(3)
        return m.group(0)
    
    html = re.sub(
        r'(<a[^>]+class="left-logo"[^>]*>)(.*?)(</a>)',
        inject_img_if_empty,
        html, flags=re.DOTALL
    )
    
    return html

def fix_generic_logo_img_inline(html):
    """Fix all remaining inline-styled logo imgs to use class instead."""
    # For any remaining inline style imgs
    html = re.sub(
        r'<img\s+src="assets/logo\.png"\s+alt="BillSathi"\s+style="height:\d+px;[^"]*"(\s*/?>)',
        r'<img src="assets/logo.png" alt="BillSathi" class="logo-img"\1',
        html
    )
    return html

# ─── PER-FILE PROCESSORS ─────────────────────────────────────────────────────

def process_navbar_page(path):
    """index.html, features.html, pricing.html, how-it-works.html, templates.html"""
    html = read(path)
    html = fix_navbar_logo_css(html)
    html = fix_logo_img_css(html)
    html = fix_navbar_logo_html(html)
    html = fix_generic_logo_img_inline(html)
    write(path, html)

def process_sidebar_page(path):
    """dashboard.html, billing-history.html, my-bills.html, builder.html"""
    html = read(path)
    html = fix_sb_logo_css(html)
    html = fix_sb_logo_html(html)
    write(path, html)

def process_auth_page(path):
    """login.html, signup.html, customer-login.html"""
    html = read(path)
    html = fix_left_logo_css(html)
    html = fix_left_logo_html(html)
    # Also fix any navbar-style logos on these pages
    html = fix_logo_img_css(html)
    html = fix_generic_logo_img_inline(html)
    write(path, html)

def process_simple_page(path):
    """gdpr.html, privacy.html, terms.html, cookies.html, business-type.html, etc."""
    html = read(path)
    html = fix_logo_img_css(html)
    html = fix_generic_logo_img_inline(html)
    write(path, html)

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("\n🔧 Fixing BillSathi Logo Display...\n")

    navbar_pages = ['index.html', 'features.html', 'pricing.html', 'how-it-works.html', 'templates.html']
    sidebar_pages = ['dashboard.html', 'billing-history.html', 'my-bills.html', 'builder.html']
    auth_pages = ['login.html', 'signup.html', 'customer-login.html']
    simple_pages = ['gdpr.html', 'privacy.html', 'terms.html', 'cookies.html',
                    'business-type.html', 'business-category.html', 'gst-verification.html']

    for fname in navbar_pages:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Navbar]  {fname}")
            process_navbar_page(p)

    for fname in sidebar_pages:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Sidebar] {fname}")
            process_sidebar_page(p)

    for fname in auth_pages:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Auth]    {fname}")
            process_auth_page(p)

    for fname in simple_pages:
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            print(f"[Page]    {fname}")
            process_simple_page(p)

    print("\n✅ Logo display fixed across all pages!\n")

if __name__ == '__main__':
    main()

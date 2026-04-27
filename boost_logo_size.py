#!/usr/bin/env python3
"""
Boost BillSathi Logo Size — One-pass bulk replacement across all HTML files.
Targets the three CSS classes and replaces their height values + removes max-width cap.
Also injects responsive @media overrides.
"""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ── New CSS rules ─────────────────────────────────────────────────────────────

# Navbar pages (index, features, pricing, etc.)
LOGO_IMG_CSS = (
    '.logo-img { '
    'height: 64px; '
    'width: auto; '
    'object-fit: contain; '
    'display: block; '
    'background: none; '
    'border: none; '
    'box-shadow: none; '
    'image-rendering: -webkit-optimize-contrast; '
    '}'
)

LOGO_IMG_MEDIA = (
    '@media (max-width: 768px) { .logo-img { height: 48px; } }'
)

# Sidebar pages (dashboard, billing-history, my-bills, builder)
SB_LOGO_IMG_CSS = (
    '.sb-logo-img { '
    'height: 56px; '
    'width: auto; '
    'object-fit: contain; '
    'display: block; '
    'background: none; '
    'border: none; '
    'box-shadow: none; '
    'image-rendering: -webkit-optimize-contrast; '
    '}'
)

SB_LOGO_IMG_MEDIA = (
    '@media (max-width: 768px) { .sb-logo-img { height: 44px; } }'
)

# Login / signup / customer-login (left panel)
LEFT_LOGO_IMG_CSS = (
    '.left-logo-img { '
    'height: 64px; '
    'width: auto; '
    'object-fit: contain; '
    'display: block; '
    'background: none; '
    'border: none; '
    'box-shadow: none; '
    'image-rendering: -webkit-optimize-contrast; '
    '}'
)

LEFT_LOGO_IMG_MEDIA = (
    '@media (max-width: 768px) { .left-logo-img { height: 48px; } }'
)

# ── Helper ───────────────────────────────────────────────────────────────────

def replace_css_rule(html, selector_pattern, new_rule, media_rule=None):
    """Replace an existing CSS rule block matching selector_pattern."""
    pattern = re.compile(
        selector_pattern + r'\s*\{[^}]*\}',
        re.DOTALL
    )
    if pattern.search(html):
        html = pattern.sub(new_rule, html, count=1)
        # Remove any duplicate/old @media for this class
        if media_rule:
            # Remove old media queries for this selector if any
            old_media = re.compile(
                r'@media[^{]*\{[^{}]*' + selector_pattern + r'[^{}]*\{[^}]*\}[^}]*\}',
                re.DOTALL
            )
            html = old_media.sub('', html)
            # Inject new media rule right after the main rule
            html = html.replace(new_rule, new_rule + '\n    ' + media_rule, 1)
    return html

def process(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Fix .logo-img (navbar pages)
    if '.logo-img' in html:
        html = replace_css_rule(html, r'\.logo-img', LOGO_IMG_CSS, LOGO_IMG_MEDIA)

    # 2. Fix .sb-logo-img (sidebar pages)
    if '.sb-logo-img' in html:
        html = replace_css_rule(html, r'\.sb-logo-img', SB_LOGO_IMG_CSS, SB_LOGO_IMG_MEDIA)

    # 3. Fix .left-logo-img (auth pages)
    if '.left-logo-img' in html:
        html = replace_css_rule(html, r'\.left-logo-img', LEFT_LOGO_IMG_CSS, LEFT_LOGO_IMG_MEDIA)

    # 4. Fix any residual inline-style logo imgs with old heights
    #    e.g. style="height:38px;..." or style="height:44px;..."
    html = re.sub(
        r'(<img\s+src="assets/logo\.png"[^>]+)style="[^"]*"',
        lambda m: m.group(1),  # strip inline style — class handles it
        html
    )

    # 5. Remove max-width from sb-logo-img if still present inline
    html = re.sub(
        r'(\.sb-logo-img\s*\{[^}]*?)max-width\s*:[^;]+;\s*',
        r'\1',
        html, flags=re.DOTALL
    )

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {os.path.basename(path)}")
    else:
        print(f"  — {os.path.basename(path)} (no change needed)")

def main():
    print("\n🚀 Boosting BillSathi logo sizes...\n")

    all_html = glob.glob(os.path.join(BASE, '*.html'))
    # exclude originals and node_modules
    all_html = [p for p in all_html
                if '_original-html' not in p
                and 'node_modules' not in p]
    all_html.sort()

    for path in all_html:
        process(path)

    print("\n✅ All logo sizes boosted!\n")
    print("Sizes applied:")
    print("  Navbar  (.logo-img):       64px desktop | 48px mobile")
    print("  Sidebar (.sb-logo-img):    56px desktop | 44px mobile")
    print("  Auth    (.left-logo-img):  64px desktop | 48px mobile")

if __name__ == '__main__':
    main()

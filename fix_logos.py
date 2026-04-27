import os, glob, re

css_replacements = {
    '.logo-img': "height: 72px; width: auto; max-width: none; max-height: none; object-fit: contain; display: block; background: transparent; border: none; box-shadow: none; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;",
    '.left-logo-img': "height: 72px; width: auto; max-width: none; max-height: none; object-fit: contain; display: block; background: transparent; border: none; box-shadow: none; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;",
    '.gv-logo-img': "height: 72px; width: auto; max-width: none; max-height: none; object-fit: contain; display: block; background: transparent; border: none; box-shadow: none; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;",
    '.sb-logo-img': "height: 62px; width: auto; max-width: none; max-height: none; object-fit: contain; display: block; background: transparent; border: none; box-shadow: none; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;"
}

mobile_heights = {
    '.logo-img': '60px',
    '.left-logo-img': '60px',
    '.gv-logo-img': '60px',
    '.sb-logo-img': '50px'
}

html_files = glob.glob('*.html')
if os.path.exists('dist/index.html'):
    html_files.append('dist/index.html')

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    original_content = content
    for cls, rules in css_replacements.items():
        cls_esc = cls.replace('.', '\\.')
        
        # Replace main class definition
        content = re.sub(
            cls_esc + r'\s*\{[^}]*\}',
            cls + ' { ' + rules + ' }',
            content
        )
        
        # Replace mobile media query definition
        content = re.sub(
            r'@media\s*\(\s*max-width\s*:\s*768px\s*\)\s*\{\s*' + cls_esc + r'\s*\{[^}]*\}\s*\}',
            f'@media (max-width: 768px) {{ {cls} {{ height: {mobile_heights[cls]}; }} }}',
            content
        )

    def img_repl(m):
        tag = m.group(0)
        tag = re.sub(r'src="[^"]+"', 'src="assets/logo.png"', tag)
        return tag

    content = re.sub(r'<img[^>]+class="[^"]*(logo-img)[^"]*"[^>]*>', img_repl, content)

    if content != original_content:
        with open(file, 'w') as f:
            f.write(content)
        print(f"Updated {file}")

print("Done.")

import re

filepath = '/Users/apple/Desktop/untitled folder 2/invoicepro/builder.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix preview-paper styling
old_style = r"""        \.preview-paper \{
            width: 100%;
            max-width: 680px;
            min-height: 880px;
            background: white;
            box-shadow: 0 24px 64px rgba\(91, 63, 255, 0\.12\), 0 4px 12px rgba\(0, 0, 0, 0\.04\);
            border-radius: 6px;
            overflow: hidden;
            margin: 0 auto;
        \}"""

new_style = """        .preview-paper {
            width: 700px;
            min-height: 900px;
            background: white;
            box-shadow: 0 32px 80px rgba(91, 63, 255, 0.15), 0 4px 12px rgba(0,0,0,0.05);
            border-radius: 4px;
            overflow: hidden;
            margin: 0 auto;
        }"""

content = re.sub(old_style, new_style, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated preview-paper CSS.")

import re

files_to_fix = [
    '/Users/apple/Desktop/untitled folder 2/invoicepro/builder.html',
    '/Users/apple/Desktop/untitled folder 2/invoicepro/templates.html'
]

font_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'

for fp in files_to_fix:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update baseStyle to include font_link and use Inter
    content = re.sub(
        r'(function baseStyle\(\) \{ return \'<!DOCTYPE html><html><head><meta charset="utf-8">)(<style>)',
        r'\1' + font_link + r'\2',
        content
    )
    
    content = content.replace('font-family:"Segoe UI",system-ui,sans-serif;', 'font-family:"Inter",system-ui,sans-serif;')
    
    # 2. Update all inline head strings in tpl_p4, tpl_p5, tpl_s3
    content = re.sub(
        r'\'<!DOCTYPE html><html><head><meta charset="utf-8">(<style>)',
        '\'' + '<!DOCTYPE html><html><head><meta charset="utf-8">' + font_link + r'\1',
        content
    )
    
    # 3. Replace font-family:"Segoe UI" or font-family:Segoe UI inside templates
    content = content.replace('font-family:Segoe UI,sans-serif', 'font-family:\\\'Inter\\\',sans-serif')
    content = content.replace('font-family:"Segoe UI",sans-serif', 'font-family:\\\'Inter\\\',sans-serif')
    
    # 4. Replace Georgia,serif with Plus Jakarta Sans
    content = content.replace('font-family:Georgia,serif', 'font-family:\\\'Plus Jakarta Sans\\\',sans-serif')
    
    # 5. Update global CSS body font
    content = content.replace(
        "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;",
        "font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;"
    )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Fonts updated and layout links injected.")

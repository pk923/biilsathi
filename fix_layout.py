import re

def fix_file(filepath, is_templates=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add flex-shrink:0 to qrSVG and strict width/height
    content = content.replace(
        '<svg viewBox="0 0 66 66" width="60" height="60" xmlns="http://www.w3.org/2000/svg">',
        '<svg viewBox="0 0 66 66" width="60" height="60" style="width:60px;height:60px;flex-shrink:0" xmlns="http://www.w3.org/2000/svg">'
    )

    # Ensure logo placeholder has flex-shrink:0
    content = content.replace(
        '<div style="width:52px;height:52px;background:\' + acc + \';border-radius:12px;display:flex;align-items:center;justify-content:center">',
        '<div style="width:52px;height:52px;background:\' + acc + \';border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0">'
    )

    if is_templates:
        # Update use template buttons to redirect to builder.html
        content = re.sub(
            r'card\.querySelector\(\'\.tcard-use\'\)\.onclick = function \(e\) \{ e\.stopPropagation\(\); openBuilder\(tpl\); \};',
            r"card.querySelector('.tcard-use').onclick = function (e) { e.stopPropagation(); window.location.href = 'builder.html?template=' + tpl.id; };",
            content
        )
        
        # Update openBuilderFromPreview
        content = re.sub(
            r'function openBuilderFromPreview\(\) \{ closePreview\(\); openBuilder\(currentTpl\); \}',
            r"function openBuilderFromPreview() { closePreview(); window.location.href = 'builder.html?template=' + currentTpl.id; }",
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('/Users/apple/Desktop/untitled folder 2/invoicepro/builder.html', is_templates=False)
fix_file('/Users/apple/Desktop/untitled folder 2/invoicepro/templates.html', is_templates=True)

print("Fixes applied.")

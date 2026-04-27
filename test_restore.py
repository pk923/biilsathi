import os, glob, re
history_dir = "/Users/apple/Library/Application Support/Antigravity/User/History"
html_files = glob.glob(os.path.join(history_dir, "**", "*.html"), recursive=True)
for f in html_files:
    try:
        with open(f, "r") as file:
            content = file.read()
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if m:
                print(m.group(1).strip())
    except:
        pass

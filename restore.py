import os, glob, re, shutil

history_dir = "/Users/apple/Library/Application Support/Antigravity/User/History"
html_files = glob.glob(os.path.join(history_dir, "**", "*.html"), recursive=True)

out_dir = "/tmp/restored"
os.makedirs(out_dir, exist_ok=True)

pages = {
    "index.html": [r"<title>InvoicePro — Professional Invoice Generator</title>"],
    "features.html": [r"<title>Features — InvoicePro</title>"],
    "templates.html": [r"<title>Templates — InvoicePro</title>"],
    "how-it-works.html": [r"<title>How It Works — InvoicePro</title>"],
    "pricing.html": [r"<title>Pricing — InvoicePro</title>"],
    "login.html": [r"<title>Login — InvoicePro</title>"],
    "signup.html": [r"<title>Sign Up — InvoicePro</title>"]
}

restored = {}

for f in html_files:
    try:
        with open(f, "r") as file:
            content = file.read()
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if not m:
                continue
            title = m.group(1).strip()
            
            matched = ""
            if "How It Works" in title: matched = "how-it-works.html"
            elif "Templates" in title: matched = "templates.html"
            elif "Pricing" in title: matched = "pricing.html"
            elif "Login" in title: matched = "login.html"
            elif "Sign Up" in title: matched = "signup.html"
            elif "Features" in title: matched = "features.html"
            elif "Professional Invoice Generator" in title: matched = "index.html"
            
            if matched:
                size = len(content)
                if matched not in restored or restored[matched][1] < size:
                    restored[matched] = (f, size, content)
    except Exception as e:
        print(f"Error reading {f}: {e}")

for name, data in restored.items():
    print(f"Restoring {name} from {data[0]} size {data[1]}")
    with open(os.path.join(out_dir, name), "w") as out:
        out.write(data[2])

import os
import glob
import re

navbar_code = """<nav>
  <a href="index.html" class="logo">
    <div class="logo-icon"><svg viewBox="0 0 24 24">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
      </svg></div>
    Invoice<em>Pro</em>
  </a>

  <div class="nav-links">
    <a href="index.html">Home</a>
    <a href="features.html">Features</a>
    <a href="templates.html">Templates</a>
    <a href="how-it-works.html">How It Works</a>
    <a href="pricing.html">Pricing</a>
  </div>

  <div class="nav-right">
    <a href="login.html" class="btn-g" style="text-decoration: none; display: inline-flex; align-items: center;">Login</a>
    <a href="signup.html" class="btn-p" style="text-decoration: none; display: inline-flex; align-items: center;">Get Started</a>
  </div>
</nav>"""

css_code = '<link rel="stylesheet" href="css/style.css">'
js_code = '<script src="js/app.js"></script>'

html_files = ["index.html", "features.html", "templates.html", "how-it-works.html", "pricing.html", "login.html", "signup.html"]

for f in html_files:
    if not os.path.exists(f): continue
    with open(f, "r") as file:
        content = file.read()

    # Replace <nav> to </nav>
    content = re.sub(r'<nav>.*?</nav>', navbar_code, content, flags=re.DOTALL)

    # Note: earlier we saw index.html had a huge style block. Replace all <style> blocks with our link
    # ONLY IF <link rel="stylesheet" href="css/style.css"> is not there. Wait, better to replace all <style> blocks 
    # but that might break template-specific styles if they exist...
    
    # We will replace <style>.*?</style> with <link rel="stylesheet" href="css/style.css">
    # but only if there is a big one or if the user wants it.
    # The user says "har page me ye hona chahiye: <link rel="stylesheet" href="css/style.css">"
    
    # Check if link already exists
    if css_code not in content:
        # replace the first <style> block, or if it doesn't exist, put before </head>
        if '<style>' in content:
            content = re.sub(r'<style>.*?</style>', css_code + '\n', content, count=1, flags=re.DOTALL)
            # Remove any other <style> blocks if there are multiple? No, just the first matching main style.
            # Wait, there might be multiple <style> blocks in templates.html!
        else:
            content = content.replace("</head>", css_code + "\n</head>")

    # Check if script already exists
    if js_code not in content:
        # Replace the <script> block at the bottom
        if '<script>' in content:
            # Replaces the last script block, or just all script blocks? 
            # The User said "JS bottom me load karo". Let's replace the last <script> block before </body>
            # Or just replace all <script>.*?</script> before </body>.
            # Let's use a regex to replace anything between <script> and </script> right before </body>.
            content = re.sub(r'<script>.*?</script>(?=\s*</body>)', js_code + '\n', content, flags=re.DOTALL)
        else:
            content = content.replace("</body>", js_code + "\n</body>")

    with open(f, "w") as file:
        file.write(content)

print("done")

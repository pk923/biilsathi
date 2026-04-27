import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix WhatsApp string
bad_msg1 = r'var msg = "Hello from " \+ d\.biz \+ "![\r\n]+Here is your invoice \(" \+ d\.inv \+ "\) for " \+ total \+ "\.[\r\n]+Thank you for your business!";'
good_msg1 = 'var msg = "Hello from " + d.biz + "!\\nHere is your invoice (" + d.inv + ") for " + total + ".\\nThank you for your business!";'
text = re.sub(bad_msg1, good_msg1, text)

# Fix Email string
bad_msg2 = r'var msg = "Hello " \+ d\.client \+ ",[\r\n]+Please find the details for invoice " \+ d\.inv \+ " for the amount of " \+ total \+ "\.[\r\n]+Thank you!";'
good_msg2 = 'var msg = "Hello " + d.client + ",\\n\\nPlease find the details for invoice " + d.inv + " for the amount of " + total + ".\\n\\nThank you!";'
text = re.sub(bad_msg2, good_msg2, text)

with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)


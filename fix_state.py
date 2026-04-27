import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

state_vars = """        /* ─── STATE ─── */
        var uploadedLogo = null;
        var uploadedSig = null;
        var currentSigTab = "draw";
        var builderTpl = null;
        var lineItems = [];
        var g_d = {};
        var g_currency = '₹';
        var bizType = 'product';
        var bizCategory = '';
        
        var savedClients = [];
        var savedProducts = [];
        var savedBiz = {};
        var savedDraft = {};
        
        try {
            savedClients = JSON.parse(localStorage.getItem('INV_clients') || '[]');
            savedProducts = JSON.parse(localStorage.getItem('INV_products') || '[]');
            savedBiz = JSON.parse(localStorage.getItem('INV_biz_profile') || '{}');
            savedDraft = JSON.parse(localStorage.getItem('INV_draft') || '{}');
        } catch(e) {}
"""

text = re.sub(r'        /\* ─── STATE ─── \*/\n        var uploadedLogo = null;.*?\n        var lineItems = \[\];', state_vars, text, flags=re.DOTALL)

with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)


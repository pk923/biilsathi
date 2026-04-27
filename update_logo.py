import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Modify saveDraft to persist logo and signature
save_draft = """        function saveDraft() {
            var d = prepareData();
            localStorage.setItem('INV_draft', JSON.stringify(d));
            
            var localSig = null;
            if(uploadedSig) localSig = uploadedSig;
            else {
                try {
                    var c = document.getElementById('sig-canvas');
                    if (c) {
                        var dataUrl = c.toDataURL('image/png');
                        var blank = document.createElement('canvas'); blank.width = c.width; blank.height = c.height;
                        if (dataUrl !== blank.toDataURL('image/png')) localSig = dataUrl;
                    }
                } catch(e) {}
            }

            // Auto-save biz profile
            savedBiz = {
                name: d.biz,
                tax: d.taxPercent,
                currency: d.currency,
                notes: d.notes,
                payMethod: document.getElementById('df-pay-method') ? document.getElementById('df-pay-method').value : '',
                logo: uploadedLogo,
                signature: localSig
            };
            localStorage.setItem('INV_biz_profile', JSON.stringify(savedBiz));"""

text = re.sub(r'function saveDraft\(\) \{.*?localStorage\.setItem\(\'INV_biz_profile\', JSON\.stringify\(savedBiz\)\);', save_draft, text, flags=re.DOTALL)

# Modify init() to correctly load logo and signature
init_defaults = """            // Auto Defaults
            if(savedBiz.name) {
                var setEl = function(id,v){if(document.getElementById(id)) document.getElementById(id).value=v;}
                setEl('df-biz', savedBiz.name);
                setEl('df-tax', savedBiz.tax || 0);
                setEl('df-currency', savedBiz.currency || '₹');
                setEl('df-notes', savedBiz.notes || '');
                setEl('df-pay-method', savedBiz.payMethod || 'Bank Transfer');
            }
            if(savedBiz.logo) {
                uploadedLogo = savedBiz.logo;
            }
            if(savedBiz.signature) {
                uploadedSig = savedBiz.signature;
                currentSigTab = 'upload';
            }"""

text = re.sub(r'// Auto Defaults.*?\}\n(\s*document\.getElementById\(\'df-inv\'\)\.value = generateInvNumber\(\);)', init_defaults + r'\n\1', text, flags=re.DOTALL)

# Update renderLogoSection logic slightly so it automatically renders the logo loaded initially.
# Well, actually renderLogoSection is called via renderForm? No, it's not. But updatePreview() calls renderLogoSection implicitly? 
# No, `renderLogoSection()` must be explicitly called. We will add `renderLogoSection()` right after `renderForm()` in `init()`.
text = text.replace('renderForm();\n            renderDatalists();', 'renderForm();\n            renderDatalists();\n            renderLogoSection();')


with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)

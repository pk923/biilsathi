import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

funcs = """
        function generateInvNumber() {
            var dt = new Date();
            var dStr = dt.getFullYear() + ('0' + (dt.getMonth()+1)).slice(-2) + ('0' + dt.getDate()).slice(-2);
            var num = Math.floor(Math.random() * 900) + 100;
            return 'INV-' + dStr + '-' + num;
        }

        function renderDatalists() {
            var html = '<datalist id="client-list">';
            savedClients.forEach(c => { html += '<option value="' + c.name + '">'; });
            html += '</datalist><datalist id="product-list">';
            savedProducts.forEach(p => { html += '<option value="' + p.name + '">'; });
            html += '</datalist>';
            var dl = document.getElementById('global-datalists');
            if(!dl) {
                dl = document.createElement('div');
                dl.id = 'global-datalists';
                document.body.appendChild(dl);
            }
            dl.innerHTML = html;
        }

        function clientSelected(val) {
            var c = savedClients.find(x => x.name === val);
            if(c) {
                var s = function(id,v){var el=document.getElementById(id);if(el)el.value=v;};
                s('df-bemail', c.email||'');
                s('df-bphone', c.phone||'');
                s('df-baddr', c.address||'');
                updatePreview();
            }
        }

        function productSelected(inputEl, val) {
            var row = inputEl.closest('.line-item-card');
            if(!row) return;
            var p = savedProducts.find(x => x.name === val);
            if(p) {
                var pInput = row.querySelector('.item-price');
                if(pInput && (!pInput.value || pInput.value == '0')) pInput.value = p.price;
                var gstInput = row.querySelector('.item-gst');
                if(gstInput && p.gst) gstInput.value = p.gst;
                updatePreview();
            }
        }

        function shareWhatsApp() {
            var d = prepareData();
            var total = document.getElementById('v-grand') ? document.getElementById('v-grand').textContent : '0';
            var msg = "Hello from " + d.biz + "!\nHere is your invoice (" + d.inv + ") for " + total + ".\nThank you for your business!";
            window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank');
            showToast('Prepared WhatsApp message! ✓');
        }

        function shareEmail() {
            var d = prepareData();
            var total = document.getElementById('v-grand') ? document.getElementById('v-grand').textContent : '0';
            var msg = "Hello " + d.client + ",\\n\\nPlease find the details for invoice " + d.inv + " for the amount of " + total + ".\\n\\nThank you!";
            window.location.href = 'mailto:' + (d.bemail||'') + '?subject=' + encodeURIComponent('Invoice ' + d.inv + ' from ' + d.biz) + '&body=' + encodeURIComponent(msg);
            showToast('Opening native email client! ✓');
        }

        function copyLink() {
            var l = window.location.href.split('?')[0] + '?template=' + (builderTpl ? builderTpl.id : 'p1');
            navigator.clipboard.writeText(l).then(() => showToast('Link copied to clipboard! ✓'));
        }
"""

text = re.sub(r'        function showToast\(msg\) \{', funcs + '\n        function showToast(msg) {', text)

with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)


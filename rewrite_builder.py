import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. State Variables
add_state = """        /* ─── BUILDER LOGIC ─── */
        var savedClients = JSON.parse(localStorage.getItem('INV_clients') || '[]');
        var savedBiz = JSON.parse(localStorage.getItem('INV_biz_profile') || '{}');
        var savedDraft = JSON.parse(localStorage.getItem('INV_draft') || '{}');
        var savedProducts = JSON.parse(localStorage.getItem('INV_products') || '[]');

        function generateInvNumber() {
            var d = new Date();
            var ymd = d.getFullYear().toString() + (d.getMonth() + 1).toString().padStart(2, '0') + d.getDate().toString().padStart(2, '0');
            var rnd = Math.floor(Math.random() * 900) + 100;
            return 'INV-' + ymd + '-' + rnd;
        }

        function renderDatalists() {
            var cList = document.getElementById('client-list');
            if (!cList) { cList = document.createElement('datalist'); cList.id = 'client-list'; document.body.appendChild(cList); }
            cList.innerHTML = savedClients.map(c => '<option value="' + c.name + '">').join('');

            var pList = document.getElementById('product-list');
            if (!pList) { pList = document.createElement('datalist'); pList.id = 'product-list'; document.body.appendChild(pList); }
            pList.innerHTML = savedProducts.map(p => '<option value="' + p.name + '">').join('');
        }

        function clientSelected(name) {
            var c = savedClients.find(x => x.name === name);
            if(c) {
                document.getElementById('df-bemail').value = c.email || '';
                document.getElementById('df-bphone').value = c.phone || '';
                document.getElementById('df-baddr').value = c.address || '';
                showToast('Client info auto-filled! ✨');
                updatePreview();
            }
        }

        function productSelected(inputEl, name) {
            var p = savedProducts.find(x => x.name === name);
            if(p) {
                var row = inputEl.closest('.line-item-card');
                if(row) {
                    var priceEl = row.querySelector('.item-price');
                    if(priceEl) priceEl.value = p.price || 0;
                    var gstEl = row.querySelector('.item-gst');
                    if(gstEl && p.gst !== undefined) gstEl.value = p.gst;
                    showToast('Item auto-filled! ✨');
                    updatePreview();
                }
            }
        }
"""
text = text.replace('/* ─── BUILDER LOGIC ─── */', add_state)

# 2. Modify `renderForm` for inputs hooking to datalist
text = text.replace('<input type="text" id="df-client">', '<input type="text" id="df-client" list="client-list" oninput="clientSelected(this.value)" placeholder="Type to search clients...">')
text = text.replace('<input type="text" class="item-name" placeholder="Name">', '<input type="text" class="item-name" placeholder="Name" list="product-list" oninput="productSelected(this, this.value)">')
text = text.replace('<input type="text" class="item-name" placeholder="Service">', '<input type="text" class="item-name" placeholder="Service" list="product-list" oninput="productSelected(this, this.value)">')

# Add Enter key support for quick row add
text = text.replace('<input type="number" class="item-price" value="0">', '<input type="number" class="item-price" value="0" onkeydown="if(event.key===\'Enter\'){ event.preventDefault(); addLineItem(); }">')

# Modify Top Action Buttons
top_btns = """<div class="top-right">
            <button onclick="shareWhatsApp()" class="btn-exit" style="cursor:pointer; border:1px solid #c4b8ff; background:white;">WhatsApp</button>
            <button onclick="copyLink()" class="btn-exit" style="cursor:pointer; border:1px solid #c4b8ff; background:white;">Copy Link</button>
            <button onclick="window.print()" class="btn-exit" style="cursor:pointer; border:none; background:transparent;">Print</button>
            <button onclick="downloadInvoice()" class="btn-save">Download PDF</button>
        </div>"""
text = re.sub(r'<div class="top-right">.*?</div>', top_btns, text, flags=re.DOTALL)

# Inject auto save and handlers
auto_logic = """
        function saveDraft() {
            var d = prepareData();
            localStorage.setItem('INV_draft', JSON.stringify(d));
            
            // Auto-save biz profile
            savedBiz = {
                name: d.biz,
                tax: d.taxPercent,
                currency: d.currency,
                notes: d.notes,
                payMethod: document.getElementById('df-pay-method') ? document.getElementById('df-pay-method').value : ''
            };
            localStorage.setItem('INV_biz_profile', JSON.stringify(savedBiz));

            // Auto-save clients
            if(d.client && !savedClients.find(c => c.name === d.client)) {
                savedClients.push({name: d.client, email: d.bemail, phone: d.bphone, address: d.baddr});
                localStorage.setItem('INV_clients', JSON.stringify(savedClients));
                renderDatalists();
            }

            // Auto-save items
            if(d.items) {
                d.items.forEach(it => {
                    if(it.name && !savedProducts.find(p => p.name === it.name)) {
                        savedProducts.push({name: it.name, price: it.price, gst: it.gst});
                    }
                });
                localStorage.setItem('INV_products', JSON.stringify(savedProducts));
                renderDatalists();
            }
            
            var t = document.getElementById('toast');
            if(t && !t.classList.contains('show')) {
               // silent save normally
            }
        }

        function confirmRestore() {
            var wrapper = document.createElement('div');
            wrapper.style.cssText = 'position:fixed; bottom:24px; left:24px; background:#fff; padding:16px 24px; border-radius:12px; box-shadow:0 12px 40px rgba(0,0,0,0.15); z-index:9999; border:1px solid #ede9ff; font-size:13px; font-weight:600;';
            wrapper.innerHTML = '<span style="margin-right:16px">Draft restored from your last session.</span> <button onclick="this.parentNode.remove()" style="padding:6px 12px; background:var(--accent); color:#fff; border:none; border-radius:8px; cursor:pointer;">Dismiss</button>';
            document.body.appendChild(wrapper);
        }

        function restoreDraft(d) {
            var setv = function(id, val) { var el = document.getElementById(id); if(el && val !== undefined && val !== '') el.value = val; };
            setv('df-inv', d.inv);
            setv('df-date', d.date);
            setv('df-currency', d.currency);
            setv('df-biz', d.biz);
            setv('df-client', d.client);
            setv('df-bemail', d.bemail);
            setv('df-bphone', d.bphone);
            setv('df-baddr', d.baddr);
            setv('df-notes', d.notes);
            setv('df-tax', d.taxPercent);
            setv('df-disc', d.discountVal);
            setv('df-ship', d.shipping);
            setv('df-paid', d.paid);
            
            if(d.items && d.items.length > 0 && bizType !== 'freelancer') {
                lineItems = []; // reset dynamically
                d.items.forEach((it, idx) => {
                    var id = Date.now() + '' + idx;
                    lineItems.push({ id: id });
                });
                renderLineItems();
                d.items.forEach((it, idx) => {
                    var row = document.getElementById('line-item-' + lineItems[idx].id);
                    if(row) {
                        var qn = row.querySelector('.item-name'); if(qn) qn.value = it.name || '';
                        var qq = row.querySelector('.item-qty'); if(qq) qq.value = it.qty || it.hrs || 1;
                        var qp = row.querySelector('.item-price'); if(qp) qp.value = it.price || it.rate || 0;
                        var qsku = row.querySelector('.item-sku'); if(qsku) qsku.value = it.sku || '';
                        var qd = row.querySelector('.item-desc'); if(qd) qd.value = it.desc || '';
                        var qdisc = row.querySelector('.item-disc'); if(qdisc) qdisc.value = it.discount || 0;
                        var qgst = row.querySelector('.item-gst'); if(qgst) qgst.value = it.gst || 0;
                    }
                });
            }
            updatePreview();
        }

        function shareWhatsApp() {
            var d = prepareData();
            var grand = document.getElementById('v-grand').textContent;
            var due = document.getElementById('v-due').textContent;
            var text = encodeURIComponent('Hello ' + (d.client||'Client') + ',\\n\\nHere is your invoice *' + (d.inv||'INV') + '* for *' + grand + '*.\\nRemaining due: *' + due + '*.\\n\\nThank you!\\n- ' + d.biz);
            window.open('https://api.whatsapp.com/send?text=' + text, '_blank');
        }

        function shareEmail() {
            var d = prepareData();
            var grand = document.getElementById('v-grand').textContent;
            var subject = encodeURIComponent('Invoice ' + d.inv + ' from ' + d.biz);
            var body = encodeURIComponent('Hello ' + (d.client||'Client') + ',\\n\\nPlease find attached the invoice ' + (d.inv||'') + ' for ' + grand + '.\\n\\nThank you,\\n' + d.biz);
            window.location.href = 'mailto:' + (d.bemail||'') + '?subject=' + subject + '&body=' + body;
        }

        function copyLink() {
            var url = window.location.href.split('?')[0] + '?template=' + (builderTpl ? builderTpl.id : 'p1') + '&view=1';
            navigator.clipboard.writeText(url).then(function() {
                showToast('Shareable Link copied! ✨');
            });
        }
"""
text = text.replace('/* ─── BUILDER LOGIC ─── */', '/* ─── BUILDER LOGIC ─── */\n' + auto_logic)

# Modify init() to include calls to restore
init_mod = """        function init() {
            bizType = localStorage.getItem('selectedBusinessType') || 'product';
            bizCategory = localStorage.getItem('selectedBusinessCategory') || '';
            renderForm();
            renderDatalists();
            
            // Auto Defaults
            if(savedBiz.name) {
                var setEl = function(id,v){if(document.getElementById(id)) document.getElementById(id).value=v;}
                setEl('df-biz', savedBiz.name);
                setEl('df-tax', savedBiz.tax || 0);
                setEl('df-currency', savedBiz.currency || '₹');
                setEl('df-notes', savedBiz.notes || '');
                setEl('df-pay-method', savedBiz.payMethod || 'Bank Transfer');
            }
            document.getElementById('df-inv').value = generateInvNumber();
            var dt = new Date();
            document.getElementById('df-date').value = dt.toISOString().split('T')[0];
            dt.setDate(dt.getDate() + 7);
            document.getElementById('df-due').value = dt.toISOString().split('T')[0];
            
            var params = new URLSearchParams(window.location.search);
"""
text = text.replace("""        function init() {
            bizType = localStorage.getItem('selectedBusinessType') || 'product';
            bizCategory = localStorage.getItem('selectedBusinessCategory') || '';
            renderForm();
            
            var params = new URLSearchParams(window.location.search);""", init_mod)

# Setup Auto-Restore and Interval after updatePreview() is first called in init()
init_end = """            renderSignatureSection();
            updatePreview();
            
            // Auto restore logic
            if (Object.keys(savedDraft).length > 0 && confirm("You have an unsaved draft. Restore it?")) {
                restoreDraft(savedDraft);
                confirmRestore();
            }
            
            // Auto save every 10 seconds silently
            setInterval(saveDraft, 10000);
        }"""
text = text.replace("""            renderSignatureSection();
            updatePreview();
        }""", init_end)

# Also intercept the actions section button hooks in renderForm
text = text.replace('onclick="showToast(\'Draft Saved!\')">Save Draft', 'onclick="saveDraft(); showToast(\'Progress Saved! ✓\')">Save')
text = text.replace('onclick="showToast(\'WhatsApp share initialized\')">Share WhatsApp', 'onclick="shareWhatsApp()">WhatsApp')
text = text.replace('onclick="showToast(\'Email draft opened\')">Send Email', 'onclick="shareEmail()">Email')

with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Automations injected!")

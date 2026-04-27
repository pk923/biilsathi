import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace fmtINR with fmtCurrency
text = text.replace('fmtINR', 'fmtCurrency')
text = text.replace("function fmtCurrency(n) { return '\u20b9' + (n || 0).toLocaleString('en-IN'); }", """var g_currency = '₹';
        function fmtCurrency(n) { return g_currency + (n || 0).toLocaleString('en-US'); }""")

# Replace calcProd, calcSvc, calcSub
calc_funcs = """        function calcProd(d) {
            var items = d.items || []; var sub = 0, rows = '';
            items.forEach(function (it, i) { 
                var amt = (it.qty || 1) * (it.price || 0); 
                if (it.discount) amt -= it.discount;
                sub += amt; 
                var extra = [];
                if(it.sku) extra.push('SKU: ' + it.sku);
                if(it.desc) extra.push(it.desc);
                var descStr = extra.length ? '<br><span style="color:#94a3b8;font-size:10px">' + extra.join(' | ') + '</span>' : '';
                rows += '<tr' + (i % 2 ? ' style="background:#fafafa"' : '') + '><td style="padding:9px 12px"><strong>' + (it.name || 'Product') + '</strong>' + descStr + '</td><td style="padding:9px 12px;text-align:center">' + (it.qty || 1) + '</td><td style="padding:9px 12px;text-align:right">' + fmtCurrency(it.price || 0) + '</td><td style="padding:9px 12px;text-align:center">' + (it.gst || d.taxPercent || 0) + '%</td><td style="padding:9px 12px;text-align:right;font-weight:700">' + fmtCurrency(amt) + '</td></tr>'; 
            });
            var taxAmt = Math.round(sub * ((d.taxPercent||0) / 100)) || 0;
            var discAmt = d.discountVal || 0;
            var shipAmt = d.shipping || 0;
            var grand = sub + taxAmt + shipAmt - discAmt;
            return { sub: sub, tax: taxAmt, grand: grand, rows: rows, items: items };
        }
        function calcSvc(d) {
            var items = d.items || []; var sub = 0, rows = '';
            items.forEach(function (it, i) { 
                var amt = (it.hrs || 1) * (it.rate || 0); 
                sub += amt; 
                rows += '<tr' + (i % 2 ? ' style="background:#fafafa"' : '') + '><td style="padding:9px 12px;vertical-align:top"><strong>' + (it.name || 'Service') + '</strong>' + (it.desc ? '<br><span style="color:#94a3b8;font-size:10px">' + it.desc + '</span>' : '') + '</td><td style="padding:9px 12px;text-align:center">' + (it.hrs || 1) + '</td><td style="padding:9px 12px;text-align:right">' + fmtCurrency(it.rate || 0) + '</td><td style="padding:9px 12px;text-align:right;font-weight:700">' + fmtCurrency(amt) + '</td></tr>'; 
            });
            var taxAmt = Math.round(sub * ((d.taxPercent||0) / 100)) || 0;
            var discAmt = d.discountVal || 0;
            var shipAmt = d.shipping || 0;
            var grand = sub + taxAmt + shipAmt - discAmt;
            return { sub: sub, tax: taxAmt, grand: grand, rows: rows, items: items };
        }
        function calcSub(d) {
            var items = d.items || []; var sub = 0, rows = '';
            items.forEach(function (it, i) { 
                sub += (it.price || 0); 
                rows += '<tr' + (i % 2 ? ' style="background:#fafafa"' : '') + '><td style="padding:9px 12px"><strong>' + (it.name || 'Item') + '</strong>' + (it.desc ? '<br><span style="color:#94a3b8;font-size:10px">' + it.desc + '</span>':'') + '</td><td style="padding:9px 12px;text-align:center">' + (it.duration || '1') + '</td><td style="padding:9px 12px;text-align:right">' + fmtCurrency(it.price || 0) + '</td><td style="padding:9px 12px;text-align:right;font-weight:700">' + fmtCurrency(it.price || 0) + '</td></tr>'; 
            });
            var taxAmt = Math.round(sub * ((d.taxPercent||0) / 100)) || 0;
            var discAmt = d.discountVal || 0;
            var shipAmt = d.shipping || 0;
            var grand = sub + taxAmt + shipAmt - discAmt;
            return { sub: sub, tax: taxAmt, grand: grand, rows: rows };
        }"""
text = re.sub(r'function calcProd\(d\).*?return \{ sub: sub, tax: tax, grand: sub \+ tax, rows: rows \};\s*\}', calc_funcs, text, flags=re.DOTALL)
text = re.sub(r'function calcProd\(d\).*?return \{ sub: sub, tax: tax, grand: sub \+ tax, rows: rows, items: items \};\s*\}', calc_funcs, text, flags=re.DOTALL)

# Re-run a rigid replace for the group of calc functions if regex failed
calc_regex = re.compile(r'function calcProd.*?function baseStyle', re.DOTALL)
text = calc_regex.sub(calc_funcs + '\n        function baseStyle', text)

# Replace totalsBox
totals_box_new = """function totalsBox(sub, tax, grand, acc) {
            var d = g_d || {};
            var s = '<div style="width:200px;flex-shrink:0">';
            s += '<div style="display:flex;justify-content:space-between;padding:7px 12px;font-size:11px;background:' + acc + '0a;border-bottom:1px solid ' + acc + '15"><span style="color:#64748b">Subtotal</span><span style="font-weight:600">' + fmtCurrency(sub) + '</span></div>';
            if (d.discountVal > 0) s += '<div style="display:flex;justify-content:space-between;padding:7px 12px;font-size:11px;background:' + acc + '0d;border-bottom:1px solid ' + acc + '15"><span style="color:#64748b">Discount</span><span style="font-weight:600">-' + fmtCurrency(d.discountVal) + '</span></div>';
            if (d.shipping > 0) s += '<div style="display:flex;justify-content:space-between;padding:7px 12px;font-size:11px;background:' + acc + '0d;border-bottom:1px solid ' + acc + '15"><span style="color:#64748b">Shipping</span><span style="font-weight:600">' + fmtCurrency(d.shipping) + '</span></div>';
            if (d.taxPercent > 0) s += '<div style="display:flex;justify-content:space-between;padding:7px 12px;font-size:11px;background:' + acc + '12;border-bottom:1px solid ' + acc + '15"><span style="color:#64748b">Tax (' + d.taxPercent + '%)</span><span style="font-weight:600">' + fmtCurrency(tax) + '</span></div>';
            s += '<div style="display:flex;justify-content:space-between;padding:7px 12px;font-size:13px;background:' + acc + '"><span style="color:#fff;font-weight:800">Grand Total</span><span style="color:#fff;font-weight:800">' + fmtCurrency(grand) + '</span></div>';
            return s + '</div>';
        }"""
text = re.sub(r'function totalsBox\(sub, tax, grand, acc\).*?return s \+ \'</div>\';\s*\}', totals_box_new, text, flags=re.DOTALL)

# Inject Form Generator & state variables
JS_INJECT = """
        var bizType = 'product';
        var bizCategory = '';
        var g_d = {};
        var debounceTimer;

        function debounceUpdate() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function() { updatePreview(); }, 100);
        }

        function renderForm() {
            var html = '';
            
            // 1. Universal Common Fields
            html += '<div class="form-section">'
                + '<div class="form-section-title">Invoice Details</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Invoice Number</label><input type="text" id="df-inv" value="INV-001"></div>'
                + '<div class="field"><label>Currency</label>'
                + '<select id="df-currency">'
                + '<option value="₹">₹ INR</option>'
                + '<option value="$">$ USD</option>'
                + '<option value="€">€ EUR</option>'
                + '<option value="£">£ GBP</option>'
                + '</select>'
                + '</div></div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Invoice Date</label><input type="date" id="df-date" value="' + new Date().toISOString().split('T')[0] + '"></div>'
                + '<div class="field"><label>Due Date</label><input type="date" id="df-due"></div>'
                + '</div></div>';

            html += '<div class="form-section">'
                + '<div class="form-section-title">Business & Client</div>'
                + '<div class="field-row single">'
                + '<div class="field"><label>Your Business Name</label><input type="text" id="df-biz" value="Your Business Name"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Client Name</label><input type="text" id="df-client"></div>'
                + '<div class="field"><label>Client Email</label><input type="email" id="df-bemail"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Client Phone</label><input type="text" id="df-bphone"></div>'
                + '<div class="field"><label>Billing Address</label><textarea id="df-baddr" rows="2"></textarea></div>'
                + '</div></div>';

            // 2. Category Customizations
            var catHtml = '';
            var cat = (bizCategory || '').toLowerCase();
            if (cat.indexOf('clothing') > -1) catHtml = '<div class="field-row"><div class="field"><label>Size</label><input type="text" id="df-c-size"></div><div class="field"><label>Color</label><input type="text" id="df-c-color"></div></div>';
            else if (cat.indexOf('salon') > -1) catHtml = '<div class="field-row"><div class="field"><label>Appointment Time</label><input type="time" id="df-c-time"></div><div class="field"><label>Stylist</label><input type="text" id="df-c-stylist"></div></div>';
            else if (cat.indexOf('web') > -1) catHtml = '<div class="field-row"><div class="field"><label>Hosting / Domain</label><input type="text" id="df-c-hosting"></div><div class="field"><label>Maintenance Period</label><input type="text" id="df-c-maint"></div></div>';
            else if (cat.indexOf('bakery') > -1) catHtml = '<div class="field-row single"><div class="field"><label>Delivery Date</label><input type="date" id="df-c-deliv"></div></div>';
            else if (cat.indexOf('photographer') > -1) catHtml = '<div class="field-row"><div class="field"><label>Event Date</label><input type="date" id="df-c-event"></div><div class="field"><label>Shoot Hours</label><input type="number" id="df-c-shoot"></div></div>';
            else if (cat.indexOf('gym') > -1) catHtml = '<div class="field-row single"><div class="field"><label>Membership Duration</label><input type="text" id="df-c-duration"></div></div>';
            else if (cat.indexOf('medical') > -1) catHtml = '<div class="field-row"><div class="field"><label>Batch No</label><input type="text" id="df-c-batch"></div><div class="field"><label>Expiry</label><input type="month" id="df-c-expiry"></div></div>';

            if (catHtml) {
                html += '<div class="form-section"><div class="form-section-title">Category Details: ' + bizCategory + '</div>' + catHtml + '</div>';
            }

            // 3. Dynamic Fields based on Type
            if (bizType === 'freelancer') {
                html += '<div class="form-section"><div class="form-section-title">Project Details</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Project Name</label><input type="text" id="df-proj-name"></div>'
                + '<div class="field"><label>Deliverable</label><input type="text" id="df-proj-deliv"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Package Type</label><input type="text" id="df-proj-pkg"></div>'
                + '<div class="field"><label>Platform</label><input type="text" id="df-proj-plat"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Start Date</label><input type="date" id="df-proj-start"></div>'
                + '<div class="field"><label>Deadline</label><input type="date" id="df-proj-end"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Revisions</label><input type="number" id="df-proj-rev"></div>'
                + '<div class="field"><label>Flat Price</label><input type="number" id="df-proj-price" value="0"></div>'
                + '</div></div>';
            } else {
                html += '<div class="form-section"><div class="form-section-title">Billing Items</div>'
                + '<div id="line-items-container"></div>'
                + '<button type="button" class="btn-add-line" onclick="addLineItem()">+ Add Row</button>'
                + '</div>';
            }

            // 4. Totals and Settings
            html += '<div class="form-section">'
                + '<div class="form-section-title">Totals & Settings</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Tax / GST (%)</label><input type="number" id="df-tax" value="18"></div>'
                + '<div class="field"><label>Discount Amount</label><input type="number" id="df-disc" value="0"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Shipping Charge</label><input type="number" id="df-ship" value="0"></div>'
                + '<div class="field"><label>Amount Paid (Advance)</label><input type="number" id="df-paid" value="0"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Payment Method</label><select id="df-pay-method"><option>Cash</option><option>Bank Transfer</option><option>Online</option></select></div>'
                + '<div class="field"><label>Status</label><select id="df-pay-status"><option>Unpaid</option><option>Paid</option><option>Partial</option></select></div>'
                + '</div>'
                + '<div class="field-row single">'
                + '<div class="field"><label>Notes / Terms</label><textarea id="df-notes" rows="2"></textarea></div>'
                + '</div>'
                + '</div>';
            
            // Real-time calculation display
            html += '<div style="background:var(--accent-soft); padding:16px; border-radius:12px; margin-bottom:24px;">'
                + '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Subtotal:</span> <span id="v-sub">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Tax:</span> <span id="v-tax">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Discount:</span> <span id="v-disc">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Shipping:</span> <span id="v-ship">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-top:12px; padding-top:12px; border-top:1.5px dashed #c4b8ff; font-size:16px; font-weight:800; color:var(--accent)"><span>Grand Total:</span> <span id="v-grand">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-top:8px; font-size:12px; font-weight:600; color:var(--green)"><span>Paid Amount:</span> <span id="v-paid">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-top:8px; font-size:12px; font-weight:600; color:#ef4444"><span>Remaining Due:</span> <span id="v-due">0</span></div>'
                + '</div>';
                
            document.getElementById('dynamic-form-wrap').innerHTML = html;
            
            lineItems = [];
            if(bizType !== 'freelancer') addLineItem();

            // Event listener for inputs
            document.getElementById('builderForm').addEventListener('input', debounceUpdate);
            // Also select elements emit change
            document.getElementById('builderForm').addEventListener('change', debounceUpdate);
        }

        function addLineItem() {
            var id = Date.now() + Math.random().toString().substr(2, 5);
            lineItems.push({ id: id });
            renderLineItems();
            updatePreview();
        }
        function removeLineItem(id) {
            lineItems = lineItems.filter(function(i) { return i.id != id; });
            renderLineItems();
            updatePreview();
        }
        function renderLineItems() {
            var container = document.getElementById('line-items-container');
            if (!container) return;
            var html = '';
            
            lineItems.forEach(function(item, index) {
                html += '<div class="line-item-card" id="line-item-' + item.id + '">'
                    + '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">'
                    + '<span style="font-size:12px; font-weight:700; color:var(--ink);">Item ' + (index + 1) + '</span>'
                    + '<button type="button" style="background:#fee2e2; color:#ef4444; border:none; border-radius:6px; padding:6px; cursor:pointer; font-size:10px; font-weight:700; font-family:inherit;" onclick="removeLineItem(\\'' + item.id + '\\')">Remove</button>'
                    + '</div>';
                
                if (bizType === 'product') {
                    html += '<div class="field-row">'
                        + '<div class="field"><label>Product Name</label><input type="text" class="item-name" placeholder="Name"></div>'
                        + '<div class="field"><label>SKU/Code</label><input type="text" class="item-sku" placeholder="SKU"></div>'
                        + '</div>'
                        + '<div class="field-row">'
                        + '<div class="field"><label>Qty</label><input type="number" class="item-qty" value="1"></div>'
                        + '<div class="field"><label>Unit Price</label><input type="number" class="item-price" value="0"></div>'
                        + '</div>'
                        + '<div class="field-row">'
                        + '<div class="field"><label>Discount Amount</label><input type="number" class="item-disc" value="0"></div>'
                        + '<div class="field"><label>GST %</label><input type="number" class="item-gst" value="18"></div>'
                        + '</div>';
                } else {
                    html += '<div class="field-row single">'
                        + '<div class="field"><label>Service / Milestone Name</label><input type="text" class="item-name" placeholder="Service"></div>'
                        + '</div>'
                        + '<div class="field-row single">'
                        + '<div class="field"><label>Description</label><input type="text" class="item-desc" placeholder="Details"></div>'
                        + '</div>'
                        + '<div class="field-row">'
                        + '<div class="field"><label>Hours / Qty</label><input type="number" class="item-qty" value="1"></div>'
                        + '<div class="field"><label>Rate</label><input type="number" class="item-price" value="0"></div>'
                        + '</div>';
                }
                html += '</div>';
            });
            
            container.innerHTML = html;
        }

        function prepareData() {
            var d = {};
            var val = function(id) { var el = document.getElementById(id); return el ? el.value : ''; };
            
            d.inv = val('df-inv') || 'INV-001';
            d.date = val('df-date');
            d.currency = val('df-currency') || '₹';
            g_currency = d.currency;
            d.biz = val('df-biz') || 'Your Business Name';
            d.client = val('df-client') || 'Client Name';
            d.email = 'hello@yourbusiness.com';
            d.phone = '+91 00000 00000';
            d.bemail = val('df-bemail');
            d.bphone = val('df-bphone');
            d.baddr = val('df-baddr');
            d.notes = val('df-notes');
            d.terms = val('df-notes') || 'Payment due within 15 days.';
            
            d.taxPercent = parseFloat(val('df-tax')) || 0;
            d.discountVal = parseFloat(val('df-disc')) || 0;
            d.shipping = parseFloat(val('df-ship')) || 0;
            d.paid = parseFloat(val('df-paid')) || 0;

            d.items = [];
            if (bizType === 'freelancer') {
                var pprice = parseFloat(val('df-proj-price')) || 0;
                d.items.push({
                    name: val('df-proj-name') || 'Project Deliverable',
                    desc: 'Package: ' + (val('df-proj-pkg')||'Standard') + ' | Deadline: ' + (val('df-proj-end')||'TBD'),
                    qty: 1, price: pprice, hrs: 1, rate: pprice
                });
            } else {
                lineItems.forEach(function(item) {
                    var row = document.getElementById('line-item-' + item.id);
                    if (!row) return;
                    var qname = row.querySelector('.item-name');
                    var qqty = row.querySelector('.item-qty');
                    var qprice = row.querySelector('.item-price');
                    var qdesc = row.querySelector('.item-desc');
                    var qsku = row.querySelector('.item-sku');
                    var qdisc = row.querySelector('.item-disc');
                    var qgst = row.querySelector('.item-gst');
                    
                    d.items.push({
                        name: qname ? qname.value || 'Item' : 'Item',
                        qty: qqty ? parseFloat(qqty.value) || 1 : 1,
                        price: qprice ? parseFloat(qprice.value) || 0 : 0,
                        hrs: qqty ? parseFloat(qqty.value) || 1 : 1,
                        rate: qprice ? parseFloat(qprice.value) || 0 : 0,
                        desc: qdesc ? qdesc.value : '',
                        sku: qsku ? qsku.value : '',
                        discount: qdisc ? parseFloat(qdisc.value) || 0 : 0,
                        gst: qgst ? parseFloat(qgst.value) || 0 : 0
                    });
                });
            }
            
            var extradesc = [];
            if(val('df-c-size')) extradesc.push('Size: ' + val('df-c-size'));
            if(val('df-c-color')) extradesc.push('Color: ' + val('df-c-color'));
            if(val('df-c-time')) extradesc.push('Appt: ' + val('df-c-time'));
            if(val('df-c-stylist')) extradesc.push('Stylist: ' + val('df-c-stylist'));
            if(val('df-c-hosting')) extradesc.push('Domain: ' + val('df-c-hosting'));
            if(val('df-c-maint')) extradesc.push('Maint: ' + val('df-c-maint'));
            if(val('df-c-deliv')) extradesc.push('Delivery: ' + val('df-c-deliv'));
            if(val('df-c-event')) extradesc.push('Event: ' + val('df-c-event'));
            if(val('df-c-shoot')) extradesc.push('Hours: ' + val('df-c-shoot'));
            if(val('df-c-duration')) extradesc.push('Duration: ' + val('df-c-duration'));
            if(val('df-c-batch')) extradesc.push('Batch: ' + val('df-c-batch'));
            if(val('df-c-expiry')) extradesc.push('Expiry: ' + val('df-c-expiry'));

            if(extradesc.length > 0 && d.items.length > 0) {
                d.items[0].desc = (d.items[0].desc ? d.items[0].desc + ' | ' : '') + extradesc.join(' | ');
            }

            d.logo = uploadedLogo;
            return d;
        }

        // We override the start of init() to load forms
"""

# Next we inject inside updatePreview so it uses our data
update_preview_new = """function updatePreview() {
            if (!builderTpl) return;
            var d = prepareData();
            g_d = d;
            
            var html = TPL_MAP[builderTpl.id](d);
            var iframe = document.getElementById('bm-iframe');
            try { var doc = iframe.contentDocument || iframe.contentWindow.document; doc.open(); doc.write(html); doc.close(); } catch (e) { }

            // Update real-time display
            var sub = 0;
            if(d.items) d.items.forEach(function(i){ sub += (i.qty||1)*(i.price||0) - (i.discount||0); });
            var tax = Math.round(sub * (d.taxPercent / 100));
            var grand = sub + tax + d.shipping - d.discountVal;
            var remaining = grand - d.paid;
            
            var setv = function(id, v) { var el = document.getElementById(id); if(el) el.textContent = g_currency + v.toLocaleString('en-US'); };
            setv('v-sub', sub);
            setv('v-tax', tax);
            setv('v-disc', d.discountVal);
            setv('v-ship', d.shipping);
            setv('v-grand', grand);
            setv('v-paid', d.paid);
            setv('v-due', remaining);
        }"""
text = re.sub(r'function updatePreview\(\) \{.*?catch \(e\) \{ \}\s*\}', update_preview_new, text, flags=re.DOTALL)

# Inject the form generation block in the HTML and JS
# 1. Modify HTML
html_form_placeholder = """<div class="editor-content" id="builderForm">
                <div id="dynamic-form-wrap"></div>
                <div class="form-section" style="margin-top:24px;">"""
text = text.replace('<div class="editor-content" id="builderForm">\n                <div class="form-section">', html_form_placeholder)

# 2. Add extra buttons to the top
top_btns = """<div class="top-right">
            <button onclick="showToast('Draft Saved! ✓')" class="btn-exit" style="cursor:pointer; border:none; background:transparent;">Save Draft</button>
            <button onclick="window.print()" class="btn-exit" style="cursor:pointer; border:none; background:transparent;">Print</button>
            <a href="templates.html" class="btn-exit">Templates</a>
            <button onclick="downloadInvoice()" class="btn-save">Download PDF</button>
        </div>"""
text = re.sub(r'<div class="top-right">.*?</div>', top_btns, text, flags=re.DOTALL)

# 3. Add JS
# Finding the start of init()
init_start = """function init() {
            var params = new URLSearchParams(window.location.search);"""
inject_init = """function init() {
            bizType = localStorage.getItem('selectedBusinessType') || 'product';
            bizCategory = localStorage.getItem('selectedBusinessCategory') || '';
            renderForm();
            
            var params = new URLSearchParams(window.location.search);"""
text = text.replace(init_start, inject_init)
text = text.replace('/* ─── BUILDER LOGIC ─── */', '/* ─── BUILDER LOGIC ─── */\n' + JS_INJECT)

with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("done")

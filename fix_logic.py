import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace renderForm
renderForm_code = """        function renderForm() {
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
                + '<div class="field"><label>Client Name</label><input type="text" id="df-client" list="client-list" oninput="clientSelected(this.value)" placeholder="Type to search clients..."></div>'
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
                + '<div class="field"><label>Package</label><input type="text" id="df-proj-pkg"></div>'
                + '<div class="field"><label>Deadline</label><input type="date" id="df-proj-end"></div>'
                + '</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Revisions</label><input type="number" id="df-proj-rev"></div>'
                + '<div class="field"><label>Flat Price</label><input type="number" id="df-proj-price" value="0"></div>'
                + '</div></div>';
            } else {
                html += '<div class="form-section"><div class="form-section-title">Billing Items</div>'
                + '<div id="line-items-container"></div>'
                + '<button type="button" class="btn-add-line" onclick="addLineItem()">+ ' + (bizType === 'product' ? 'Add Product Row' : 'Add Service Row') + '</button>'
                + '</div>';
            }

            // 4. Totals and Settings
            html += '<div class="form-section">'
                + '<div class="form-section-title">Totals & Settings</div>'
                + '<div class="field-row">'
                + '<div class="field"><label>Tax / GST (%)</label><input type="number" id="df-tax" value="18"></div>'
                + '<div class="field"><label>Discount Amount</label><input type="number" id="df-disc" value="0" min="0"></div>'
                + '</div>';
                
            if (bizType === 'product') {
                html += '<div class="field-row single"><div class="field"><label>Shipping Charge</label><input type="number" id="df-ship" value="0" min="0"></div></div>';
            }
            
            html += '<div class="field-row">'
                + '<div class="field"><label>' + (bizType === 'freelancer' ? 'Advance Paid' : 'Amount Paid') + '</label><input type="number" id="df-paid" value="0" min="0"></div>'
                + '<div class="field"><label>Payment Method</label><select id="df-pay-method"><option>Cash</option><option>Bank Transfer</option><option>Online</option></select></div>'
                + '</div>'
                + '<div class="field-row single">'
                + '<div class="field"><label>Notes / Terms</label><textarea id="df-notes" rows="2"></textarea></div>'
                + '</div>'
                + '</div>';
            
            // Real-time calculation display
            html += '<div style="background:var(--accent-soft); padding:16px; border-radius:12px; margin-bottom:24px;">'
                + '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Subtotal:</span> <span id="v-sub">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Tax:</span> <span id="v-tax">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Discount:</span> <span id="v-disc">0</span></div>';
            
            if (bizType === 'product') {
                html += '<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-weight:600; color:var(--ink2)"><span>Shipping:</span> <span id="v-ship">0</span></div>';
            }
            else {
                html += '<div style="display:none;"><span id="v-ship">0</span></div>';
            }
            
            html += '<div style="display:flex; justify-content:space-between; margin-top:12px; padding-top:12px; border-top:1.5px dashed #c4b8ff; font-size:16px; font-weight:800; color:var(--accent)"><span>Grand Total:</span> <span id="v-grand">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-top:8px; font-size:12px; font-weight:600; color:var(--green)"><span>' + (bizType === 'freelancer' ? 'Advance Paid' : 'Amount Paid') + ':</span> <span id="v-paid">0</span></div>'
                + '<div style="display:flex; justify-content:space-between; margin-top:8px; font-size:12px; font-weight:600; color:#ef4444"><span>Remaining Amount:</span> <span id="v-due">0</span></div>'
                + '</div>';
                
            document.getElementById('dynamic-form-wrap').innerHTML = html;
            
            lineItems = [];
            if(bizType !== 'freelancer') addLineItem();

            document.getElementById('builderForm').addEventListener('input', debounceUpdate);
            document.getElementById('builderForm').addEventListener('change', debounceUpdate);
        }"""
text = re.sub(r'function renderForm\(\) \{.*?document\.getElementById\(\'builderForm\'\)\.addEventListener\(\'change\', debounceUpdate\);\n        \}', renderForm_code, text, flags=re.DOTALL)

# Replace renderLineItems
renderLineItems_code = """        function renderLineItems() {
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
                        + '<div class="field"><label>Product Name</label><input type="text" class="item-name" placeholder="Name" list="product-list" oninput="productSelected(this, this.value)"></div>'
                        + '<div class="field"><label>SKU</label><input type="text" class="item-sku" placeholder="SKU"></div>'
                        + '</div>'
                        + '<div class="field-row">'
                        + '<div class="field"><label>Quantity</label><input type="number" class="item-qty" value="1" min="0"></div>'
                        + '<div class="field"><label>Unit Price</label><input type="number" class="item-price" value="0" min="0" onkeydown="if(event.key===\\'Enter\\'){ event.preventDefault(); addLineItem(); }"></div>'
                        + '</div>'
                        + '<div class="field-row single">'
                        + '<div class="field"><label>Item Tax %</label><input type="number" class="item-gst" value="18" min="0" max="100"></div>'
                        + '</div>';
                } else {
                    html += '<div class="field-row">'
                        + '<div class="field"><label>Service Name</label><input type="text" class="item-name" placeholder="Service" list="product-list" oninput="productSelected(this, this.value)"></div>'
                        + '<div class="field"><label>Milestone</label><input type="text" class="item-sku" placeholder="Milestone"></div>'
                        + '</div>'
                        + '<div class="field-row single">'
                        + '<div class="field"><label>Description</label><input type="text" class="item-desc" placeholder="Details"></div>'
                        + '</div>'
                        + '<div class="field-row">'
                        + '<div class="field"><label>Hours / Qty</label><input type="number" class="item-qty" value="1" min="0"></div>'
                        + '<div class="field"><label>Rate</label><input type="number" class="item-price" value="0" min="0" onkeydown="if(event.key===\\'Enter\\'){ event.preventDefault(); addLineItem(); }"></div>'
                        + '</div>'
                        + '<div class="field-row single">'
                        + '<div class="field"><label>Appointment Date</label><input type="date" class="item-appt"></div>'
                        + '</div>';
                }
                html += '</div>';
            });
            
            container.innerHTML = html;
        }"""
text = re.sub(r'function renderLineItems\(\) \{.*?container\.innerHTML = html;\n        \}', renderLineItems_code, text, flags=re.DOTALL)

# Modify prepareData logic lightly to capture item-appt
prepareData_mod = """                    var qgst = row.querySelector('.item-gst');
                    var qappt = row.querySelector('.item-appt');
                    
                        var itmName = qname ? qname.value : 'Item';
                        if (!itmName.trim()) return; // skip empty rows
                        
                        var finalDesc = qdesc ? qdesc.value : '';
                        var extras = [];
                        if(qappt && qappt.value) extras.push('Appt: ' + qappt.value);
                        if(bizType === 'service' && qsku && qsku.value) extras.push('Milestone: ' + qsku.value);
                        if(extras.length > 0) finalDesc = finalDesc ? finalDesc + ' | ' + extras.join(' | ') : extras.join(' | ');

                        d.items.push({
                            name: itmName,
                        qty: qqty ? parseFloat(qqty.value) || 1 : 1,
                        price: qprice ? parseFloat(qprice.value) || 0 : 0,
                        hrs: qqty ? parseFloat(qqty.value) || 1 : 1,
                        rate: qprice ? parseFloat(qprice.value) || 0 : 0,
                        desc: finalDesc,
                        sku: (bizType === 'product' && qsku) ? qsku.value : '',
                        discount: qdisc ? parseFloat(qdisc.value) || 0 : 0,
                        gst: qgst ? parseFloat(qgst.value) || 0 : 0
                    });"""
text = re.sub(r'var qgst = row\.querySelector\(\'\.item-gst\'\).*?gst: qgst \? parseFloat\(qgst\.value\) \|\| 0 : 0\n                    \}\);', prepareData_mod, text, flags=re.DOTALL)

with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)

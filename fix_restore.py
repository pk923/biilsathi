import re

with open('builder.html', 'r', encoding='utf-8') as f:
    text = f.read()

correct_restore = """        function restoreDraft(d) {
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
                        var qappt = row.querySelector('.item-appt'); if(qappt) qappt.value = it.appt || '';
                    }
                });
            }
        }"""

text = re.sub(r'function restoreDraft\(d\) \{.*?\n        \}\n\n        // We override', correct_restore + '\n\n        // We override', text, flags=re.DOTALL)

with open('builder.html', 'w', encoding='utf-8') as f:
    f.write(text)


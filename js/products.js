// Products Logic
let products = [];

function loadProducts() {
    try {
        products = JSON.parse(localStorage.getItem('INV_products') || '[]');
    } catch (e) {
        products = [];
    }
    renderProducts();
}

function formatCurrency(val) {
    return '₹' + parseFloat(val || 0).toLocaleString('en-IN');
}

function getBillingBadge(type) {
    const map = {
        'hourly': '<span class="badge hourly">Hourly</span>',
        'monthly': '<span class="badge monthly">Monthly</span>',
        'fixed': '<span class="badge fixed">Fixed Price</span>',
        'quantity': '<span class="badge quantity">Qty Based</span>'
    };
    return map[type] || map['fixed'];
}

function renderProducts(query = '') {
    const listEl = document.getElementById('products-list');
    const tableEl = document.getElementById('products-table');
    const emptyEl = document.getElementById('empty-state');
    
    listEl.innerHTML = '';
    
    const filtered = products.filter(p => {
        const q = query.toLowerCase();
        const nameMatch = (p.name || '').toLowerCase().includes(q);
        const refMatch = (p.ref || p.sku || '').toLowerCase().includes(q);
        return nameMatch || refMatch;
    });
    
    if (filtered.length === 0) {
        tableEl.style.display = 'none';
        emptyEl.style.display = 'block';
        if(query) emptyEl.querySelector('h3').textContent = 'No matching products found';
        else emptyEl.querySelector('h3').textContent = 'No items saved yet';
        return;
    }
    
    tableEl.style.display = 'table';
    emptyEl.style.display = 'none';
    
    filtered.forEach((p, index) => {
        const bType = p.billingType || 'fixed';
        const ref = p.ref || p.sku || '-';
        const desc = p.desc ? `<div style="font-size: 11.5px; color: var(--t3); margin-top: 2px;">${p.desc}</div>` : '';
        const pId = p.id || index;
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <div class="client-name">${p.name}</div>
                ${desc}
            </td>
            <td class="cell-id">${ref}</td>
            <td>${getBillingBadge(bType)}</td>
            <td class="cell-amount">${formatCurrency(p.price)}</td>
            <td class="cell-date">${p.gst || 0}%</td>
            <td>
                <button class="action-icon" onclick="editProduct('${pId}')" title="Edit">
                    <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                </button>
                <button class="action-icon delete" onclick="deleteProduct('${pId}')" title="Delete">
                    <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                </button>
            </td>
        `;
        listEl.appendChild(tr);
    });
}

function filterProducts() {
    const q = document.getElementById('prod-search').value;
    renderProducts(q);
}

function toggleDurationField() {
    const type = document.getElementById('p-type').value;
    const durField = document.getElementById('duration-field');
    if (type === 'hourly' || type === 'monthly' || type === 'quantity') {
        durField.style.display = 'block';
        durField.querySelector('label').textContent = type === 'hourly' ? 'Default Hours' : type === 'monthly' ? 'Default Months' : 'Default Qty';
    } else {
        durField.style.display = 'none';
    }
}

function openProductModal() {
    document.getElementById('modal-title').textContent = 'Add New Item';
    document.getElementById('p-id').value = '';
    document.getElementById('p-name').value = '';
    document.getElementById('p-desc').value = '';
    document.getElementById('p-ref').value = '';
    document.getElementById('p-type').value = 'fixed';
    document.getElementById('p-price').value = '0';
    document.getElementById('p-duration').value = '1';
    document.getElementById('p-tax').value = '18';
    toggleDurationField();
    document.getElementById('product-modal').classList.add('open');
    setTimeout(() => document.getElementById('p-name').focus(), 100);
}

function closeProductModal() {
    document.getElementById('product-modal').classList.remove('open');
}

function editProduct(idOrIndex) {
    let p = products.find(x => x.id == idOrIndex);
    if (!p) {
        const idx = parseInt(idOrIndex);
        if (!isNaN(idx)) p = products[idx];
    }
    
    if (p) {
        document.getElementById('modal-title').textContent = 'Edit Item';
        document.getElementById('p-id').value = p.id || idOrIndex;
        document.getElementById('p-name').value = p.name || '';
        document.getElementById('p-desc').value = p.desc || '';
        document.getElementById('p-ref').value = p.ref || p.sku || '';
        document.getElementById('p-type').value = p.billingType || 'fixed';
        document.getElementById('p-price').value = p.price || 0;
        document.getElementById('p-duration').value = p.duration || 1;
        document.getElementById('p-tax').value = p.gst || 0;
        
        toggleDurationField();
        document.getElementById('product-modal').classList.add('open');
    }
}

function saveProduct() {
    const name = document.getElementById('p-name').value.trim();
    if (!name) {
        showToast('Product name is required');
        return;
    }
    
    const id = document.getElementById('p-id').value;
    const item = {
        id: id || 'P-' + Date.now().toString(36).toUpperCase(),
        name: name,
        desc: document.getElementById('p-desc').value.trim(),
        ref: document.getElementById('p-ref').value.trim(),
        sku: document.getElementById('p-ref').value.trim(), 
        billingType: document.getElementById('p-type').value,
        price: parseFloat(document.getElementById('p-price').value) || 0,
        duration: parseFloat(document.getElementById('p-duration').value) || 1,
        gst: parseFloat(document.getElementById('p-tax').value) || 0
    };

    if (id) {
        const index = products.findIndex(p => p.id == id || products.indexOf(p) == id);
        if (index > -1) {
            products[index] = item;
        }
    } else {
        const exists = products.find(p => p.name.toLowerCase() === name.toLowerCase());
        if (exists) {
            if(!confirm('An item with this name already exists. Save anyway?')) return;
        }
        products.push(item);
    }

    localStorage.setItem('INV_products', JSON.stringify(products));
    closeProductModal();
    renderProducts(document.getElementById('prod-search').value);
    showToast('Item saved successfully ✓');
}

function deleteProduct(idOrIndex) {
    if (!confirm('Are you sure you want to delete this item?')) return;
    
    let index = products.findIndex(x => x.id == idOrIndex);
    if (index === -1) index = parseInt(idOrIndex);
    
    if (index > -1 && index < products.length) {
        products.splice(index, 1);
        localStorage.setItem('INV_products', JSON.stringify(products));
        renderProducts(document.getElementById('prod-search').value);
        showToast('Item deleted');
    }
}

function showToast(msg) {
    const t = document.getElementById('toast');
    document.getElementById('t-msg').textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    document.getElementById('product-modal').addEventListener('click', (e) => {
        if (e.target.id === 'product-modal') closeProductModal();
    });
});

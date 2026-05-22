const API_BASE = '';

let allProducts = [];
let editingProductId = null;

// Load products on page load
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
});

async function loadProducts() {
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch(`${API_BASE}/inventory/`);
        if (!response.ok) throw new Error('Failed to load products');
        
        allProducts = await response.json();
        displayProducts(allProducts);
        updateStats();
        
        showLoading(false);
    } catch (error) {
        showError('Failed to load inventory. Please try again.');
        showLoading(false);
    }
}

function displayProducts(products) {
    const grid = document.getElementById('productsGrid');
    
    if (products.length === 0) {
        grid.innerHTML = '<div class="no-products"><p>No products found</p></div>';
        return;
    }
    
    grid.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-header">
                <div class="product-code">${product.product_code}</div>
                <span class="product-badge badge-${product.shape}">${product.shape}</span>
            </div>
            
            <div class="product-details">
                <div class="detail-row">
                    <span class="detail-label">Grade:</span>
                    <span class="detail-value">${product.grade}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Dimensions:</span>
                    <span class="detail-value">
                        ${product.length_mm}mm × ${product.width_mm || 'N/A'}mm × ${product.thickness_mm}mm
                    </span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Quantity:</span>
                    <span class="detail-value">
                        <span class="quantity-badge ${getQuantityClass(product.quantity)}">
                            ${product.quantity} units
                        </span>
                    </span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Location:</span>
                    <span class="detail-value">${product.location}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Last Updated:</span>
                    <span class="detail-value">${formatDate(product.last_updated)}</span>
                </div>
            </div>
            
            <div class="product-actions">
                <button class="btn btn-success btn-sm" onclick="editProduct(${product.id})">
                    ✏️ Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteProduct(${product.id}, '${product.product_code}')">
                    🗑️ Delete
                </button>
            </div>
        </div>
    `).join('');
}

function getQuantityClass(quantity) {
    if (quantity >= 100) return 'quantity-high';
    if (quantity >= 50) return 'quantity-medium';
    return 'quantity-low';
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function updateStats() {
    document.getElementById('totalProducts').textContent = allProducts.length;
    
    const totalQuantity = allProducts.reduce((sum, p) => sum + p.quantity, 0);
    document.getElementById('totalQuantity').textContent = totalQuantity.toLocaleString();
    
    const warehouses = new Set(allProducts.map(p => p.location));
    document.getElementById('warehouseCount').textContent = warehouses.size;
    
    const grades = new Set(allProducts.map(p => p.grade));
    document.getElementById('gradeCount').textContent = grades.size;
}

function filterProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const shapeFilter = document.getElementById('shapeFilter').value;
    const locationFilter = document.getElementById('locationFilter').value;
    
    const filtered = allProducts.filter(product => {
        const matchesSearch = product.product_code.toLowerCase().includes(searchTerm) ||
                            product.grade.toLowerCase().includes(searchTerm);
        const matchesShape = !shapeFilter || product.shape === shapeFilter;
        const matchesLocation = !locationFilter || product.location === locationFilter;
        
        return matchesSearch && matchesShape && matchesLocation;
    });
    
    displayProducts(filtered);
}

function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('shapeFilter').value = '';
    document.getElementById('locationFilter').value = '';
    displayProducts(allProducts);
}

function showAddProductModal() {
    editingProductId = null;
    document.getElementById('modalTitle').textContent = 'Add New Product';
    document.getElementById('productForm').reset();
    document.getElementById('productModal').style.display = 'block';
}

function editProduct(id) {
    const product = allProducts.find(p => p.id === id);
    if (!product) return;
    
    editingProductId = id;
    document.getElementById('modalTitle').textContent = 'Edit Product';
    
    document.getElementById('productCode').value = product.product_code;
    document.getElementById('grade').value = product.grade;
    document.getElementById('shape').value = product.shape;
    document.getElementById('location').value = product.location;
    document.getElementById('length').value = product.length_mm;
    document.getElementById('width').value = product.width_mm || '';
    document.getElementById('thickness').value = product.thickness_mm;
    document.getElementById('quantity').value = product.quantity;
    
    document.getElementById('productModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('productModal').style.display = 'none';
    document.getElementById('productForm').reset();
    editingProductId = null;
}

async function saveProduct(event) {
    event.preventDefault();
    
    const productData = {
        product_code: document.getElementById('productCode').value,
        grade: document.getElementById('grade').value,
        shape: document.getElementById('shape').value,
        location: document.getElementById('location').value,
        length_mm: parseFloat(document.getElementById('length').value),
        width_mm: document.getElementById('width').value ? parseFloat(document.getElementById('width').value) : null,
        thickness_mm: parseFloat(document.getElementById('thickness').value),
        quantity: parseInt(document.getElementById('quantity').value)
    };
    
    try {
        let response;
        if (editingProductId) {
            // Update existing product
            response = await fetch(`${API_BASE}/inventory/${editingProductId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    quantity: productData.quantity,
                    location: productData.location
                })
            });
        } else {
            // Create new product
            response = await fetch(`${API_BASE}/inventory/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to save product');
        }
        
        closeModal();
        loadProducts();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function deleteProduct(id, productCode) {
    if (!confirm(`Are you sure you want to delete ${productCode}?`)) return;
    
    try {
        const response = await fetch(`${API_BASE}/inventory/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete product');
        
        loadProducts();
    } catch (error) {
        alert('Error deleting product: ' + error.message);
    }
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
    document.getElementById('productsGrid').style.display = show ? 'none' : 'grid';
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').style.display = 'block';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('productModal');
    if (event.target === modal) {
        closeModal();
    }
}

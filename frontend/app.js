// API Configuration
const API_URL = 'http://localhost:5000/api';
let accessToken = localStorage.getItem('accessToken');
let refreshToken = localStorage.getItem('refreshToken');

// DOM Elements
const authSection = document.getElementById('auth-section');
const appSection = document.getElementById('app-section');
const loadingSpinner = document.getElementById('loading-spinner');
const errorMessage = document.getElementById('error-message');
const successMessage = document.getElementById('success-message');
const authMessage = document.getElementById('auth-message');

// Authentication Functions
async function register(username, email, password) {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Registration failed');
        }
        
        handleAuthSuccess(data);
        showSuccess('Registration successful!');
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function login(username, password) {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }
        
        handleAuthSuccess(data);
        showSuccess('Login successful!');
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

function handleAuthSuccess(data) {
    accessToken = data.access_token;
    refreshToken = data.refresh_token;
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    showApp();
}

function logout() {
    accessToken = null;
    refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    showAuth();
}

// UI State Functions
function showLoading() {
    loadingSpinner.classList.remove('hidden');
}

function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.classList.remove('hidden');
    setTimeout(() => {
        successMessage.classList.add('hidden');
    }, 5000);
}

function showAuth() {
    authSection.classList.remove('hidden');
    appSection.classList.add('hidden');
}

function showApp() {
    authSection.classList.add('hidden');
    appSection.classList.remove('hidden');
    loadExpenses();
}

// Expense Functions
async function loadExpenses() {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/expenses`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Session expired. Please login again.');
            }
            throw new Error('Failed to load expenses');
        }
        
        const expenses = await response.json();
        displayExpenses(expenses);
    } catch (error) {
        showError(error.message);
        if (error.message.includes('Session expired')) {
            logout();
        }
    } finally {
        hideLoading();
    }
}

async function addExpense(expenseData) {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/expenses`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(expenseData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to add expense');
        }
        
        showSuccess('Expense added successfully!');
        loadExpenses();
        document.getElementById('expense-form').reset();
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function deleteExpense(id) {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/expenses/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete expense');
        }
        
        showSuccess('Expense deleted successfully!');
        loadExpenses();
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Display Functions
function displayExpenses(expenses) {
    const expensesList = document.getElementById('expenses-list');
    expensesList.innerHTML = '';
    
    expenses.forEach(expense => {
        const expenseElement = document.createElement('div');
        expenseElement.className = 'expense-item';
        expenseElement.innerHTML = `
            <div>
                <h3>${expense.name}</h3>
                <p>Category: ${expense.category}</p>
                <p>Date: ${new Date(expense.date).toLocaleDateString()}</p>
            </div>
            <div>
                <p class="amount">$${expense.amount.toFixed(2)}</p>
                <button class="btn btn-secondary" onclick="deleteExpense(${expense.id})">Delete</button>
            </div>
        `;
        expensesList.appendChild(expenseElement);
    });
    
    updateSummary(expenses);
}

function updateSummary(expenses) {
    const summaryContent = document.getElementById('summary-content');
    const total = expenses.reduce((sum, expense) => sum + expense.amount, 0);
    const byCategory = expenses.reduce((acc, expense) => {
        acc[expense.category] = (acc[expense.category] || 0) + expense.amount;
        return acc;
    }, {});
    
    summaryContent.innerHTML = `
        <p>Total Expenses: $${total.toFixed(2)}</p>
        <h3>By Category:</h3>
        ${Object.entries(byCategory).map(([category, amount]) => `
            <p>${category}: $${amount.toFixed(2)}</p>
        `).join('')}
    `;
}

// Event Listeners
document.getElementById('register').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    await register(username, email, password);
});

document.getElementById('login').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    await login(username, password);
});

document.getElementById('expense-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const expenseData = {
        name: document.getElementById('expense-name').value,
        amount: parseFloat(document.getElementById('expense-amount').value),
        category: document.getElementById('expense-category').value,
        date: document.getElementById('expense-date').value
    };
    await addExpense(expenseData);
});

document.getElementById('logout-btn').addEventListener('click', logout);

// Search and Filter
document.getElementById('search-expenses').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const expenses = document.querySelectorAll('.expense-item');
    expenses.forEach(expense => {
        const text = expense.textContent.toLowerCase();
        expense.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});

document.getElementById('filter-category').addEventListener('change', (e) => {
    const category = e.target.value;
    const expenses = document.querySelectorAll('.expense-item');
    expenses.forEach(expense => {
        const expenseCategory = expense.querySelector('p').textContent.split(': ')[1];
        expense.style.display = !category || expenseCategory === category ? '' : 'none';
    });
});

// Initialize
if (accessToken) {
    showApp();
} else {
    showAuth();
}

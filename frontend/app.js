document.addEventListener('DOMContentLoaded', async () => {
    let categoryChart, monthlySpendingChart;
    
    // Initialize charts
    const initCharts = async () => {
        // Destroy existing charts if they exist
        if (categoryChart) categoryChart.destroy();
        if (monthlySpendingChart) monthlySpendingChart.destroy();
        
        // Fetch data for charts
        const response = await fetch('/api/expenses');
        const expenses = await response.json();
        
        // Process data for charts
        const categoryData = processCategoryData(expenses);
        const monthlyData = processMonthlyData(expenses);
        
        // Category pie chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        categoryChart = new Chart(categoryCtx, {
            type: 'pie',
            data: {
                labels: categoryData.labels,
                datasets: [{
                    data: categoryData.amounts,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                    ]
                }]
            }
        });
        
        // Monthly spending line chart
        const monthlyCtx = document.getElementById('monthlySpendingChart').getContext('2d');
        monthlySpendingChart = new Chart(monthlyCtx, {
            type: 'line',
            data: {
                labels: monthlyData.labels,
                datasets: [{
                    label: 'Monthly Spending',
                    data: monthlyData.amounts,
                    borderColor: '#36A2EB',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    };
    
    // Process category data
    const processCategoryData = (expenses) => {
        const categories = {};
        expenses.forEach(expense => {
            categories[expense.category] = (categories[expense.category] || 0) + expense.amount;
        });
        
        return {
            labels: Object.keys(categories),
            amounts: Object.values(categories)
        };
    };
    
    // Process monthly data
    const processMonthlyData = (expenses) => {
        const monthly = {};
        expenses.forEach(expense => {
            const date = new Date(expense.date || new Date());
            const monthYear = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
            monthly[monthYear] = (monthly[monthYear] || 0) + expense.amount;
        });
        
        const sortedMonths = Object.keys(monthly).sort();
        return {
            labels: sortedMonths,
            amounts: sortedMonths.map(month => monthly[month])
        };
    };
    
    // Update charts when expenses change
    const updateCharts = async () => {
        await initCharts();
    };
    
    // Load existing expenses and initialize charts
    const initialResponse = await fetch('/api/expenses');
    if (initialResponse.ok) {
        const expenses = await initialResponse.json();
        expenses.forEach(expense => addExpenseToTable(expense));
        await initCharts();
    }
    
    // Add expense handler with chart update
    document.getElementById('add-expense').addEventListener('click', async () => {
        const nameInput = document.getElementById('expense-name');
        const amountInput = document.getElementById('expense-amount');
        const categorySelect = document.getElementById('expense-category');
        const errorMessage = document.getElementById('error-message');

        errorMessage.textContent = '';

        if (!nameInput.value || !amountInput.value) {
            errorMessage.textContent = 'Please fill in all required fields';
            return;
        }

        try {
            const response = await fetch('/api/expenses', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: nameInput.value,
                    amount: parseFloat(amountInput.value),
                    category: categorySelect.value,
                    date: document.getElementById('expense-date').value
                })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const expense = await response.json();
            addExpenseToTable(expense);
            await updateCharts();

            nameInput.value = '';
            amountInput.value = '';
            categorySelect.value = 'Food';

        } catch (error) {
            const errorText = await response.text();
            errorMessage.textContent = `Error submitting expense: ${errorText}`;
        }
    });

    // Delete expense handler with chart update
    document.getElementById('expense-list').addEventListener('click', async (event) => {
        const row = event.target.closest('tr');
        const id = row?.dataset.expenseId;
        
        if (event.target.classList.contains('delete-btn')) {
            await deleteExpense(id);
            await updateCharts();
        }
        else if (event.target.classList.contains('edit-btn')) {
            const cells = row.querySelectorAll('.editable');
            const originalValues = {};
            
            // Toggle edit mode
            cells.forEach(cell => {
                const field = cell.dataset.field;
                const value = field === 'date'
                    ? new Date(cell.textContent).toISOString().split('T')[0]
                    : field === 'amount'
                    ? parseFloat(cell.textContent.replace('$', '')).toFixed(2)
                    : cell.textContent;
                
                originalValues[field] = value;
                if (field === 'category') {
                    cell.innerHTML = `
                        <select class="form-control form-control-sm">
                            <option value="food" ${value === 'food' ? 'selected' : ''}>Food</option>
                            <option value="transportation" ${value === 'transportation' ? 'selected' : ''}>Transportation</option>
                            <option value="housing" ${value === 'housing' ? 'selected' : ''}>Housing</option>
                            <option value="entertainment" ${value === 'entertainment' ? 'selected' : ''}>Entertainment</option>
                            <option value="other" ${value === 'other' ? 'selected' : ''}>Other</option>
                        </select>`;
                } else {
                    cell.innerHTML = `<input class="form-control form-control-sm"
                        type="${field === 'date' ? 'date' : field === 'amount' ? 'number' : 'text'}"
                        value="${value}">`;
                }
            });
            
            // Change button to save
            event.target.textContent = 'Save';
            event.target.classList.replace('btn-primary', 'btn-success');
            event.target.classList.add('save-btn');
            event.target.classList.remove('edit-btn');
            
            // Handle save action
            const saveHandler = async () => {
                try {
                    const updates = {};
                    cells.forEach((cell, index) => {
                        const field = cell.dataset.field;
                        const input = cell.querySelector('input');
                        const select = cell.querySelector('select');
                        const newValue = (select ? select.value : input.value).trim();
                        
                        if (newValue !== originalValues[field]) {
                            updates[field] = field === 'amount' ? parseFloat(newValue) : newValue;
                        }
                    });
                    
                    if (Object.keys(updates).length > 0) {
                        const response = await fetch(`/api/expenses/${id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(updates)
                        });
                        
                        const updatedExpense = await response.json();
                        // Update the row with new data
                        // Update the row with server response and restore view mode
                        cells.forEach(cell => {
                            const field = cell.dataset.field;
                            const value = updatedExpense[field];
                            originalValues[field] = value; // Update original values
                            cell.textContent = field === 'date'
                                ? new Date(value).toLocaleDateString()
                                : field === 'amount'
                                ? `$${parseFloat(value).toFixed(2)}`
                                : value;
                        });
                        await updateCharts();
                    }
                    
                } catch (error) {
                    document.getElementById('error-message').textContent = `Error saving changes: ${error.message}`;
                } finally {
                    // Restore button state
                    event.target.textContent = 'Edit';
                    event.target.classList.replace('btn-success', 'btn-primary');
                    event.target.classList.remove('save-btn');
                    event.target.classList.add('edit-btn');
                    event.target.removeEventListener('click', saveHandler);
                }
            };
            
            event.target.addEventListener('click', saveHandler);
        }
    });
});

function addExpenseToTable(expense) {
    const tbody = document.getElementById('expense-list');
    const row = document.createElement('tr');
    row.dataset.expenseId = expense.id;
    
    row.innerHTML = `
        <td class="editable" data-field="name">${expense.name}</td>
        <td class="editable" data-field="amount">$${expense.amount.toFixed(2)}</td>
        <td class="editable" data-field="category">${expense.category}</td>
        <td class="editable" data-field="date">${new Date(expense.date || Date.now()).toLocaleDateString()}</td>
        <td>
            <button class="btn btn-primary btn-sm edit-btn">Edit</button>
            <button class="btn btn-danger btn-sm delete-btn">Delete</button>
        </td>
    `;
    
    tbody.appendChild(row);
}

async function deleteExpense(id) {
    try {
        const response = await fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        document.querySelector(`tr[data-expense-id="${id}"]`)?.remove();
    } catch (error) {
        console.error('Error deleting expense:', error);
        document.getElementById('error-message').textContent = `Error deleting expense: ${error.message}`;
    }
}

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
                    category: categorySelect.value
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
            errorMessage.textContent = `Error submitting expense: ${error.message}`;
        }
    });

    // Delete expense handler with chart update
    document.getElementById('expense-list').addEventListener('click', async (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const id = event.target.closest('tr').dataset.expenseId;
            await deleteExpense(id);
            await updateCharts();
        }
    });
});

function addExpenseToTable(expense) {
    const tbody = document.getElementById('expense-list');
    const row = document.createElement('tr');
    row.dataset.expenseId = expense.id;
    
    row.innerHTML = `
        <td>${expense.name}</td>
        <td>$${expense.amount.toFixed(2)}</td>
        <td>${expense.category}</td>
        <td>${new Date(expense.date || Date.now()).toLocaleDateString()}</td>
        <td>
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

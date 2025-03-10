document.addEventListener('DOMContentLoaded', async () => {
    // Load existing expenses on page load
    const response = await fetch('/api/expenses');
    if (response.ok) {
        const expenses = await response.json();
        expenses.forEach(expense => addExpenseToTable(expense));
    }
    
    // Add delete handler for dynamically created buttons
    document.getElementById('expense-list').addEventListener('click', async (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const id = event.target.closest('tr').dataset.expenseId;
            await deleteExpense(id);
        }
    });
});

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

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const expense = await response.json();
        addExpenseToTable(expense);
        
        // Clear form inputs
        nameInput.value = '';
        amountInput.value = '';
        categorySelect.value = 'Food';

    } catch (error) {
        errorMessage.textContent = `Error submitting expense: ${error.message}`;
    }
});

function addExpenseToTable(expense) {
    const tbody = document.getElementById('expense-list');
    const row = document.createElement('tr');
    row.dataset.expenseId = expense.id;
    
    row.innerHTML = `
        <td>${expense.name}</td>
        <td>$${expense.amount.toFixed(2)}</td>
        <td>${expense.category}</td>
        <td>${new Date().toLocaleDateString()}</td>
        <td>
            <button class="btn btn-danger btn-sm" onclick="deleteExpense('${expense.id}')">Delete</button>
        </td>
    `;
    
    tbody.appendChild(row);
}

async function deleteExpense(id) {
    try {
        const response = await fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Remove the row from UI
        const row = document.querySelector(`tr[data-expense-id="${id}"]`);
        if (row) {
            row.remove();
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
        document.getElementById('error-message').textContent = `Error deleting expense: ${error.message}`;
    }
}


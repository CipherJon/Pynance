document.getElementById('add-expense').addEventListener('click', async () => {
    const name = document.getElementById('expense-name').value;
    const amount = document.getElementById('expense-amount').value;

    if (name && amount) {
        const response = await fetch('/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, amount })
        });

        if (response.ok) {
            const expense = await response.json();
            addExpenseToList(expense);
        }
    }
});

function addExpenseToList(expense) {
    const li = document.createElement('li');
    li.textContent = `${expense.name}: $${expense.amount}`;
    document.getElementById('expense-list').appendChild(li);
}


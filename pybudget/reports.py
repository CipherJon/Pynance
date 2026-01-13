# pybudget/reports.py

"""
Reports module for generating budget and expense reports.
"""


def generate_report(budget):
    """
    Generate a report for a given budget.

    Args:
        budget: A Budget object to generate the report for.

    Returns:
        str: A formatted report string.
    """
    report = []
    report.append(f"Budget Report for '{budget.name}'")
    report.append("=" * 40)
    report.append(f"Total Budget: ${budget.amount:.2f}")
    report.append(f"Remaining Budget: ${budget.get_remaining_amount():.2f}")
    report.append("\nExpenses:")
    report.append("-" * 40)

    if not budget.expenses:
        report.append("No expenses recorded.")
    else:
        for expense in budget.expenses:
            report.append(str(expense))

    return "\n".join(report)

from tools.add_purchase import add_expense
from tools.monthly_report import get_monthly_report

# Test writing
print(add_expense("2025-08-13", "Food", "Coffee", "Cà phê", 55000, "VND"))

# Test reading
print(get_monthly_report(2025, 8))

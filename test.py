from tools.add_purchase import add_expense
from tools.monthly_report import get_monthly_report

# Test writing
print(add_expense("2025-08-14", "Transport", "Metro", "Tàu điện ngầm", 100, "EUR"))

# Test reading
print(get_monthly_report(2025, 8))

from datetime import datetime
import time

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ggsheet_functions import init_sheet

def monthly_report(year=None, month=None):
    # Get current date in YYYY-MM-DD format
    current_date = time.strftime("%Y-%m-%d")
    current_year = int(time.strftime("%Y"))
    current_month = int(time.strftime("%m"))
    
    # Use current year/month if not provided
    year = year or current_year
    month = month or current_month

    sheet = init_sheet()
    data = sheet.get_all_records()

    filtered = []
    for row in data:
        try:
            row_date = datetime.strptime(row['Date'], "%Y-%m-%d")
            if row_date.year == year and row_date.month == month:
                filtered.append(row)
        except ValueError:
            # Skip rows with invalid or empty date
            continue

    total = sum(float(row['Fee']) for row in filtered)
    by_category = {}
    for row in filtered:
        cat = row['Category']
        by_category[cat] = by_category.get(cat, 0) + float(row['Fee'])
    
    top_expenses = sorted(filtered, key=lambda x: float(x['Fee']), reverse=True)[:3]
    
    return {
        "current_date": current_date,
        "year": year,
        "month": month,
        "total": total,
        "by_category": by_category,
        "top_expenses": top_expenses
    }

if __name__ == "__main__":
    try:
        print(monthly_report())
        print("Success! monthly_report() works just fine!")
    except Exception as e:
        print(e)

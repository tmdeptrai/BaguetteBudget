import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import yaml
import time

def init_sheet():
    config = yaml.safe_load(open("./config/mcp_client.yaml"))
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(config['mcp']['creds_file'], scope)
    client = gspread.authorize(creds)
    return client.open_by_key(config['mcp']['sheet_id']).sheet1

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

# Now you can call it with no arguments to get the current month report
print(monthly_report())
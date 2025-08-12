import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import yaml

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

def get_monthly_report(year, month):
    sheet = init_sheet()
    data = sheet.get_all_records()
    filtered = [
        row for row in data
        if datetime.strptime(row['Date'], "%Y-%m-%d").year == year
        and datetime.strptime(row['Date'], "%Y-%m-%d").month == month
    ]
    
    total = sum(float(row['Fee']) for row in filtered)
    by_category = {}
    for row in filtered:
        cat = row['Category']
        by_category[cat] = by_category.get(cat, 0) + float(row['Fee'])
    
    top_expenses = sorted(filtered, key=lambda x: float(x['Fee']), reverse=True)[:3]
    
    return {
        "year": year,
        "month": month,
        "total": total,
        "by_category": by_category,
        "top_expenses": top_expenses
    }

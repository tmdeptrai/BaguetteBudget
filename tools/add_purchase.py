import gspread
from oauth2client.service_account import ServiceAccountCredentials
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

def add_purchase(category, description, description_vi, fee):
    # Automatically get today's date in YYYY-MM-DD format
    date = time.strftime("%Y-%m-%d")
    currency = "EUR"  # Hardcoded since it's always EUR

    sheet = init_sheet()
    sheet.append_row([date, category, description, description_vi, fee, currency])

    return {
        "status": "success",
        "message": f"Added {fee} {currency} for {category} on {date}"
    }

add_purchase("Food","test","thu nghiem",10)
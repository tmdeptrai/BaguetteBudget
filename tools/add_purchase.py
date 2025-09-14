import gspread
from oauth2client.service_account import ServiceAccountCredentials
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

def add_purchase(date, category, description, description_vi, fee, currency):
    sheet = init_sheet()
    sheet.append_row([date, category, description, description_vi, fee, currency])
    return {"status": "success", "message": f"Added {fee} {currency} for {category} on {date}"}

# add_purchase("2025-09-13","Food","test","thu nghiem",10,"EUR")
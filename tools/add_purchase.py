import time
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ggsheet_functions import init_sheet

# def init_sheet():
#     config = yaml.safe_load(open("./config/mcp_client.yaml"))
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive.file",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(config['mcp']['creds_file'], scope)
#     client = gspread.authorize(creds)
#     return client.open_by_key(config['mcp']['sheet_id']).sheet1

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

if __name__ == "__main__":
    try:
        print(add_purchase("Food","test","thu nghiem",10))
        print("Success! add_purchase() works just fine!")
    except Exception as e:
        print(e)
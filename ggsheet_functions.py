import os
import json
import gspread
from dotenv import load_dotenv

load_dotenv()

PATH_TO_CREDS = "./creds/google_creds.json"

def init_sheet():
    """
    Initializes the Google Sheet connection.
    Uses Streamlit secrets in cloud (detected by env var), 
    otherwise uses local service_account.json for dev.
    """
    creds = None

    if os.getenv("STREAMLIT_RUNTIME"):  # Streamlit Cloud sets this internally
        import streamlit as st
        creds = dict(st.secrets["gcp_service_account"])  # copy as plain dict
        sheet_id = creds.pop("sheet_id")  # remove so gspread doesn't complain
    else:
        # Local dev mode
        if not os.path.exists(PATH_TO_CREDS):
            raise FileNotFoundError(
                "Missing service_account.json in local dev. "
                "Download it from GCP and place in project root."
            )
        with open(PATH_TO_CREDS, "r") as f:
            creds = json.load(f)

        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        if not sheet_id:
            raise ValueError("Set GOOGLE_SHEET_ID in your .env or shell for local development.")

    # Authenticate & open Google Sheet
    gc = gspread.service_account_from_dict(creds)
    sh = gc.open_by_key(sheet_id).sheet1
    return sh

if __name__ == "__main__":
    sh = init_sheet()
    if sh is not None:
        print(sh)
        print("Success")
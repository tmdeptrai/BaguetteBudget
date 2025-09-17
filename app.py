import streamlit as st
import pandas as pd
from orchestration import handle_user_input, monthly_report_tool
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml
from datetime import datetime

# --- CONFIG / GOOGLE SHEET INIT ---
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

sheet = init_sheet()

# --- STREAMLIT APP ---
st.set_page_config(page_title="Expense Dashboard", page_icon="💸", layout="centered")

st.title("💸 Expense Dashboard")

# 1. NATURAL LANGUAGE ENTRY
st.subheader("💬 Add a new expense")
user_input = st.text_input("Enter expense in natural language (e.g. 'Add 12 euros for lunch in Paris')")

if st.button("Submit") and user_input:
    result = handle_user_input(user_input)
    st.success(result['output'])  # Show the agent response

# 2. RECENT PURCHASES
st.subheader("📋 Recent Purchases")
data = sheet.get_all_records()
df = pd.DataFrame(data)
if not df.empty:
    df = df.sort_values(by="Date", ascending=False).head(10)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No purchases found yet.")

# 3. MONTHLY REPORT (placeholder for now)
st.subheader("📊 Monthly Report")
current_year = datetime.now().year
current_month = datetime.now().month
st.info("Coming soon")

# if st.button("Generate Monthly Report"):
#     report = monthly_report_tool(current_year, current_month)
#     st.metric("Total Expenses", f"{report['total']:.2f} EUR")
#     st.write("By Category:", report['by_category'])
import streamlit as st
import pandas as pd
from orchestration import handle_user_input, monthly_report_tool
from datetime import datetime
from ggsheet_functions import init_sheet


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
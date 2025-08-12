from mcp.server.fastmcp import FastMCP
from tools.add_purchase import add_expense
from tools.monthly_report import get_monthly_report

mcp = FastMCP("ExpenseTrackerMCP")

@mcp.tool(name="add_expense", description="Add a new expense to Google Sheet")
def add_expense_tool(date: str, category: str, description: str, description_vi: str, amount: float, fee_or_cost: str):
    return add_expense(date, category, description, description_vi, amount, fee_or_cost)

@mcp.tool(name="get_monthly_report", description="Get a monthly expense summary")
def get_monthly_report_tool(year: int, month: int):
    return get_monthly_report(year, month)

if __name__ == "__main__":
    mcp.run()

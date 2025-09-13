
from fastmcp import FastMCP
from tools.add_purchase import add_purchase
from tools.monthly_report import get_monthly_report
from starlette.requests import Request
from starlette.responses import PlainTextResponse

app = FastMCP("ExpenseTrackerMCP",json_response=True,stateless_http=True)

@app.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

@app.tool(name="add_purchase", description="Add a new expense to Google Sheet")
def add_purchase_tool(date: str, category: str, description: str, description_vi: str, fee: float, currency: str):
    return add_purchase(date, category, description, description_vi, fee, currency)

@app.tool(name="get_monthly_report", description="Get a monthly expense summary")
def get_monthly_report_tool(year: int, month: int):
    return get_monthly_report(year, month)

# if __name__ == "__main__":
#     # Expose as HTTP server
#     mcp.run(transport="http")

# Just run: fastmcp run mcp_server.py:mcp --host 127.0.0.1 --port 8000 --transport http


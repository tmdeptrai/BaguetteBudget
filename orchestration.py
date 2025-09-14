# orchestration.py
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import Tool, initialize_agent
import asyncio
from fastmcp import Client

from dotenv import load_dotenv
load_dotenv()

# 1. Setup Gemini LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY as an environment variable.")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0,google_api_key=GEMINI_API_KEY,)

# 2. MCP tool wrappers (these call your MCP server endpoints)
client = Client("http://127.0.0.1:8000/mcp")
async def add_purchase_tool(date, category, description, description_vi, fee, currency):
    async with client:
        payload = {
            "date": date,
            "category": category,
            "description": description,
            "description_vi": description_vi,
            "fee":fee,
            "currency":currency
        }
        result = await client.call_tool("add_purchase", payload)
        print(result)
        return result

# asyncio.run(add_purchase_tool("2025-09-13","food","test","thu nghiem",10,"EUR"))

async def monthly_report_tool(year,month):
    async with client:
        payload = {
            "year": year,
            "month": month,
        }
        result = await client.call_tool("monthly_report",payload)
        print(result)
        return result

asyncio.run(monthly_report_tool(2025,8))

# def monthly_report_tool(month, year):
#     res = requests.get(
#         "http://localhost:8000/tools/monthly_report",
#         params={"month": month, "year": year}
#     )
#     return res.json()

# tools = [
#     Tool(
#         name="add_purchase",
#         func=lambda x: add_purchase_tool(**(json.loads(x) if isinstance(x, str) else x)),
#         description="Add a new purchase to Google Sheets. Input should be a dict with keys: item, amount, category, date"
#     ),
#     Tool(
#         name="monthly_report",
#         func=lambda x: monthly_report_tool(**(json.loads(x) if isinstance(x, str) else x)),
#         description="Get a summary of purchases for a given month/year."
#     )
# ]

# # 3. Prompt Template for Parsing
# parser_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant that extracts structured data from user messages."),
#     ("human", "User message: {input}\n\nExtract JSON with keys: item, amount, category, date (YYYY-MM-DD format).")
# ])

# # 4. Initialize LangChain Agent
# expense_agent = initialize_agent(
#     tools,
#     llm,
#     agent="chat-conversational-react-description",
#     verbose=True
# )

# def handle_user_input(user_message):
#     # Step 1: Parse user message into JSON
#     structured_data = llm.invoke(parser_prompt.format_messages(input=user_message))
#     print(f"[DEBUG] Parsed Data: {structured_data.content}")

#     # Optionally convert parsed content to dict (if it's a JSON string)
#     try:
#         parsed_dict = json.loads(structured_data.content)
#     except json.JSONDecodeError:
#         # Fallback (hardcode for debugging)
#         parsed_dict = {
#             "item": "lunch",
#             "amount": 12,
#             "category": "food",
#             "date": "2023-10-26"
#         }

#     # Step 2: Tell agent to call the tool with structured data
#     result = expense_agent.invoke({
#         "input": f"Use the add_purchase tool with this JSON: {json.dumps(parsed_dict)}",
#         "chat_history": []
#     })
#     return result


# if __name__ == "__main__":
#     print(handle_user_input("Add 12 euros for lunch yesterday in Paris"))

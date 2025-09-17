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

def add_purchase_tool(category, description, description_vi, fee):
    async def _coro():
        async with client:
            payload = {
                "category": category,
                "description": description,
                "description_vi": description_vi,
                "fee": fee,
            }
            return await client.call_tool("add_purchase", payload)
    return asyncio.run(_coro())

# asyncio.run(add_purchase_tool("food","test","thu nghiem",10))

def monthly_report_tool(year, month):
    async def _coro():
        async with client:
            payload = {"year": year, "month": month}
            return await client.call_tool("monthly_report", payload)
    return asyncio.run(_coro())

# asyncio.run(monthly_report_tool(2025,8))

tools = [
    Tool(
        name="add_purchase",
        func=lambda x: add_purchase_tool(**(json.loads(x) if isinstance(x, str) else x)),
        description="Add a new purchase to Google Sheets. Input should be a dict with keys: category, description, description_vi, fee"
    ),
    Tool(
        name="monthly_report",
        func=lambda x: monthly_report_tool(**(json.loads(x) if isinstance(x, str) else x)),
        description="Get a summary of purchases for a given month/year."
    )
]

# 3. Prompt Template for Parsing
list_of_categories = ["Rent","Utilities","Food","Transport","Health","Clothing(including laundry)","Entertainment","Travel","Education","Bank Fees / Taxes","Others"]
parser_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a helpful assistant that extracts structured data from user messages. "
        "Return **ONLY** a single valid JSON object (no surrounding text, no backticks, "
        "no markdown, nothing else). Keys required: category, description, description_vi, fee. "
        "Use these categories: " + ", ".join(list_of_categories)
    )),
    ("human", "User message: {input}\n\nExtract JSON with keys: category, description, description_vi, fee")
])

# 4. Initialize LangChain Agent
expense_agent = initialize_agent(
    tools,
    llm,
    agent="chat-conversational-react-description",
    verbose=True
)

chat_history=[]

def handle_user_input(user_message):
    structured_data = llm.invoke(parser_prompt.format_messages(input=user_message))
    print(f"[DEBUG] Parsed Data: {structured_data.content}")
    
    result = expense_agent.invoke({
        "input": f"Use the add_purchase tool with this JSON: {structured_data.content}",
        "chat_history": chat_history
    })

    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": result})

    return result

if __name__ == "__main__":
    print(handle_user_input("Add a purchase of 19.45 euros for today's meat, vegetables and rice"))
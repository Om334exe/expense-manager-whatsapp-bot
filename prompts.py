intent_prompt_template = """
You are a smart classifier that determines the user's intent. Analyze the following user input and decide whether the user intends to add a new expense, query past expenses, or something else.

- If the user wants to add a new expense, output "Expense".
- If the user is asking about their expenses (e.g. "How much did I spend on coffee this month?"), output "Query".
- Otherwise, output "Others".

User input: {user_input}
"""
expense_prompt_template = """
You are a smart parser that extracts structured expense information. From the user input below, extract the following fields:
- price: A numeric value in INR (If price is not provided return price as -1).
- object: The item name or title (If object is not provided return object).
- dateAndTime: In YYYY-MM-DD HH:MM:SS format; if no date or is provided, use today's date and current time.
- otherDetails: Any extra relevant detail or keyword or remark that is not included in the above information.

Current date and time is {datetimes} and day is {day}.

Note: There can be multiple expenses also. 

User input: {user_input}
    """

query_prompt_template = """
You are a Python code generator. Your task is to generate only Python code that accomplishes the following:

1. Read a JSON file named "tempfile.json" which contains a list (JSON array) of expense records.
2. Each expense record is an object with the following keys:
   - "price": a number representing the expense amount in INR,
   - "object": a string describing the expense item,
   - "date": a date string in YYYY-MM-DD format,
   - "dateAndTime": a date and time string in YYYY-MM-DD HH:MM:SS format (if missing, default to today's date and current time),
   - "otherDetails": a string containing any extra relevant detail or remark.
3. Filter the expense records to select only those that are relevant to the user's query. and also compute the final answer of the query. The user's query is provided in the variable user_query in the end.
   - For example, if the query contains keywords like "coffee", then only include expenses where the "object" or "otherDetails" mention "coffee" (case-insensitive).
4. Format the output as a single string that is well organized and human readable. If output is a list and multiple expenses match the query, output each expense on its own line in a list format with clear labels for each field.
5. If no expenses match the query, output a string that says "No expenses matches the query".
6. If the required output is sum of expenses your code should do that or just give the required output only
6. Your final output must be only Python code (no additional commentary or text).

Below is an example structure that your generated code should follow:
- Import necessary modules.
- Read the JSON data from "tempfile.json".
- Filter the expenses based on the query.
- Format the filtered expenses into a human readable string.
- Print the final output string.

Do not output anything other than the Python code.

Example:
------------------------------------------------
<YOUR GENERATED CODE HERE>
------------------------------------------------

Now, generate the complete Python code according to the above instructions.

user_query: {user_input}
"""


query_prompt_template_backup = """
You are a financial assistant that helps filter expenses based on a user's query.
You are provided with:
1. A user's query: 
{user_input}
2. A list of expense records in JSON format: 
{expenses_data}
Each expense record is an object with the following keys:
   - "price": a number representing the expense amount in INR,
   - "object": a string describing the expense item,
   - "date": a date in YYYY-MM-DD format.
   - "dateAndTime": In YYYY-MM-DD HH:MM:SS format; if no date or is provided, use today's date and current time.
   - "otherDetails": Any extra relevant detail or keyword or remark that is not included in the above information.

Your task is to select those expense objects that are relevant to the user's query, perform that query steps and the final answer asked by the user.
"""

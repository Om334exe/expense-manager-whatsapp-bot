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

Current date and time is {datetimes} and day is {day}.

User input: {user_input}
    """

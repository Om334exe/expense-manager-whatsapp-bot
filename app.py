import warnings

warnings.filterwarnings("ignore")
from flask import Flask, request
from googlesearch import search
from twilio.twiml.messaging_response import MessagingResponse
from classes import *
from datetime import date
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import calendar
from prompts import *
from dotenv import load_dotenv
import os
from langgraph.graph import END, StateGraph

load_dotenv()

app = Flask(__name__)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


def intent_classification_node(state: AppState):
    intent_prompt = PromptTemplate(
        input_variables=["user_input"], template=intent_prompt_template
    )

    user_message = state["user_query"]

    prompt = intent_prompt.format(user_input=user_message)

    structured_llm = llm.with_structured_output(Intent)

    parsed_data = structured_llm.invoke(prompt)

    print(parsed_data)

    return {"intent": parsed_data.intent}


def parse_expense_node(state: AppState):
    """
    Parse a user's expense entry using ChatGroq with structured JSON output.
    The function expects state["user_message"] to contain the user's text.
    It then invokes the LLM to extract the expense details and builds an Expense instance.
    """
    expense_prompt = PromptTemplate(
        input_variables=["user_input", "datetimes", "day"],
        template=expense_prompt_template,
    )
    user_message = state["user_query"]
    prompt = expense_prompt.format(
        user_input=user_message,
        datetimes=datetime.today(),
        day=calendar.day_name[date.today().weekday()],
    )

    structured_llm = llm.with_structured_output(Expenses)

    parsed_data = structured_llm.invoke(prompt)

    print(parsed_data)
    return {"expenses": parsed_data.expenses}


def final_response_node(state: AppState):
    # state["final_,response"] = state.get("db_result", "Expense recorded.")
    return {"final_response": "All queries processed perfectly!"}


def query_expense_node(state: AppState):
    pass


def intent_check(state: AppState):
    return state["intent"]


graph = StateGraph(AppState)
graph.support_multiple_edges = True


graph.add_node("intent_classifier_node", intent_classification_node)
graph.add_node("parse_expense_node", parse_expense_node)
graph.add_node("query_expense_node", query_expense_node)
graph.add_node("final_response_node", final_response_node)

graph.add_conditional_edges(
    "intent_classifier_node",
    intent_check,
    {"Query": "query_expense_node", "Expense": "parse_expense_node"},
)

graph.add_edge("parse_expense_node", "final_response_node")
graph.add_edge("query_expense_node", "final_response_node")

graph.set_entry_point("intent_classifier_node")
graph.set_finish_point("final_response_node")


graph_app = graph.compile()
# png_graph = graph_app.get_graph().draw_mermaid_png()
# with open("my_graph.png", "wb") as f:
#     f.write(png_graph)

print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
# graph.add_node()


# @app.route("/", methods=["POST"])
def main():

    # user input

    # user_msg = request.values.get("Body", "")
    user_msg = "Today I bought a coffee for 20 rs and a coca cola for 80 rs."
    # state = intent_classification_node({"user_query": user_msg})
    state = graph_app.invoke({"user_query": user_msg})

    print(state)

    # user = request.values.get("From", "").split(":")[1]
    # intent_classification_node(user_message=user_msg)

    # creating object of MessagingResponse
    response = MessagingResponse()

    # response.message(
    #     f"Your message recieved: {}, from user number: {} and output is {str(parse_expense_node(user_msg))}"
    # )

    return str(response)


main()
# if __name__ == "__main__":
#     app.run(port=5002, debug=True)

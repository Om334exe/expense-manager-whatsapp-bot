from flask import Flask, request
from googlesearch import search
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/", methods=["POST"])
def main():

    # user input
    print("Hello")
    user_msg = request.values.get("Body", "")

    user = request.values.get("From", "").split(":")[1]

    # creating object of MessagingResponse
    response = MessagingResponse()

    response.message(f"Your message recieved: {user_msg}, from user number: {user}")

    return str(response)


if __name__ == "__main__":
    app.run(port=5002, debug=True)

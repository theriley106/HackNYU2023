from flask import Flask
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Welcome to Polyglot AI Language Tutor!! This is our project for HACKNYU", voice='alice')

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
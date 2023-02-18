from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
import audioop
import base64
import json
import os
from flask import Flask, request
from flask_sock import Sock, ConnectionClosed
from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client
import vosk
try:
    from keys import *
except:
    AUTH = input("Auth")
    SID = input("SID")

app = Flask(__name__)
sock = Sock(app)
twilio_client = Client(SID, AUTH)
model = vosk.Model('/Users/christopherlambert/Downloads/vosk-model-en-us-0.42-gigaspeech')

CL = '\x1b[0K'
BS = '\x08'



@app.route("/answerz", methods=['GET', 'POST'])
def answer_callz():
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Welcome to Polyglot AI Language Tutor!! This is our project for HACKNYU", voice='alice')

    return str(resp)

@app.route('/answer', methods=['POST'])
def call():
    """Accept a phone call."""
    response = VoiceResponse()
    start = Start()
    start.stream(url=f'wss://{request.host}/stream')
    response.append(start)
    response.say('Please leave a message')
    response.pause(length=60)
    while IS_LOADING_STILL[0] == False:
        time.sleep(.1)
        response.pause(length=20)
    print(f'Incoming call from {request.form["From"]}')
    return str(response), 200, {'Content-Type': 'text/xml'}

IS_LOADING_STILL = [False]

@sock.route('/stream')
def stream(ws):
    """Receive and transcribe audio stream."""
    rec = vosk.KaldiRecognizer(model, 16000)
    while True:
        message = ws.receive()
        packet = json.loads(message)
        if packet['event'] == 'start':
            print('Streaming is starting')
        elif packet['event'] == 'stop':
            IS_LOADING_STILL[0] = True
            print('\nStreaming has stopped')
        elif packet['event'] == 'media':
            audio = base64.b64decode(packet['media']['payload'])
            audio = audioop.ulaw2lin(audio, 2)
            audio = audioop.ratecv(audio, 2, 1, 8000, 16000, None)[0]
            if rec.AcceptWaveform(audio):
                r = json.loads(rec.Result())
                print(CL + r['text'] + ' ', end='', flush=True)
            else:
                r = json.loads(rec.PartialResult())
                print(CL + r['partial'] + BS * len(r['partial']), end='', flush=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
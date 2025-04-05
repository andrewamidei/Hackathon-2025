from flask import Flask, jsonify, request
import requests
import json
import logging



app = Flask(__name__)

serverip: str = "192.168.8.137"

logging.basicConfig(level=logging.DEBUG)

MODEL = 'mistral'
URL = 'http://192.168.8.137:11434/api/generate'


class LLmanager:
    def __init__(self, model=MODEL, url=URL):
        self.model = model
        self.url = url
        self.discOne = "Joyfull"
        self.discTwo = "Super Nice"

    def llmQuery(self, message: str, sender: str = "") -> str:
        # Create a context-aware prompt for chat messages
        prompt = (
            f"Transform this message to be more {self.discOne} and {self.discTwo}. "
            f"Message from {sender}: \"{message}\"\n"
            "Only provide the transformed message without any additional context or explanation."
        )

        data = {'model': self.model, 'prompt': prompt, 'stream': False}
        logging.debug(f"Sending prompt to LLM: {prompt}")

        try:
            with requests.post(self.url, json=data, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        json_line = line.decode('utf-8')
                        response_data = json.loads(json_line)
                        if response_data['response']:
                            return response_data['response'].strip()
        except Exception as e:
            logging.error(f"Error in LLM query: {e}")
            return f"Error processing message: {str(e)}"
        
    def getDefaultResponse(self) -> any:
        # Generate the response and send it to the UI
        model = self.model  # local model
        message = "hi there i enjoyed our time"
        prompt = f"Take this message and make it more {self.discOne} and {self.discTwo} {message} create only one message DO NOT RESPOND TO THE MESSAGE ONLY MAKE IT MORE {self.discOne} and {self.discTwo} dont add an explanation only send back the modified message"
        url = self.url

        response = self.llmQuery(model, prompt, url)

        # data = {'message': response}
        # return jsonify(data)


        return response

    def gostNewQuery(self) -> json:

        # Parse the incoming JSON data
        request_data = request.get_json()
        if not request_data or 'prompt' not in request_data:
            return jsonify({'error': 'Invalid request, "prompt" is required'}), 400

        # Extract the prompt from the request
        prompt = request_data['prompt']

        model = self.model  # local model
        url = 'http://localhost:11434/api/generate'

        response = self.llmQuery(model, prompt, url)

        # Return the response as JSON
        return jsonify({'response': response})

    def setTonality(self, discOne: str, disctwo: str):
        self.discOne = discOne
        self.discTwo = disctwo

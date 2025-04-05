from flask import Flask, jsonify, request
import requests
import json
import logging

app = Flask(__name__)

serverip: str = "192.168.8.137"

logging.basicConfig(level=logging.DEBUG)

MODEL = 'llama2:7b-q4'
URL = 'http://192.168.8.137:11434/api/generate'


class LLmanager:
    def __init__(self, model= MODEL, url= URL):
        self.model = model
        self.url = url
        self.discOne = "MAD"
        self.discTwo = "MEAN"

    def llmQuery(self, message: str,) -> any:
        # Use the generate function for a one-off prompt
        prompt = (
            f"You are an AI that takes a message and rewrites it to sound extremely \"{self.discTwo}\" and \"{self.discOne}\".\n\n"
            f"The original message is:\n"
            f"\"{message}\"\n\n"
            f"Only respond in this exact JSON format:\n"
            f"```\n"
            f"{{\n"
            f"  \"response\": \"<your transformed {self.discTwo} and {self.discOne} version of the message>\"\n"
            f"}}\n"
            f"```"
        )

        # stream is used to define wether items should be streamd one at at time (True) or all in one message (False)
        data = {'model': self.model, 'prompt': prompt, 'stream': False}

        with requests.post(self.url, json=data, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    json_line = line.decode('utf-8')
                    response_data = json.loads(json_line)
                    if response_data['response']:
                        # print(response_data['response'], end='', flush=True)
                        return response_data['response']

    def getDefaultResponse(self) -> any:
        # Generate the response and send it to the UI
        model = self.model  # local model
        message = "hi there i enjoyed our time"
        prompt = f"Take this message and make it more {self.discOne} and {self.discTwo} {message} create only one message and respond only in json"
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

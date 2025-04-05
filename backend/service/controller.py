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
        self.message = "i hate this llm so bad becuase of how stupid it is it makes me supper misrable"
        # make this message sound more {self.discOne} and {self.discTwo} message:{self.message} only provide the modified message 
        self.prompt = f"""
          You are an AI that transforms customer messages for internal use.

          Your job is to take the original message below and rewrite it in a way that is more **{self.discOne.upper()}** and **{self.discTwo.upper()}** — while keeping the original meaning of the message the same.

        ⚠️ DO NOT respond to the message. DO NOT comment on it. DO NOT change the meaning.

        Only rephrase the message in a new tone and return the modified version **only**.

        Original Message:
        "{message}"

        Output:
        <transformed message only – no explanation, no intro, no formatting>
        """
        def llmQuery(self, message: str,) -> any:

        # Use the generate function for a one-off prompt
            self.message = message


           self.prompt = f"""
              You are an AI that transforms customer messages for internal use.

              Your job is to take the original message below and rewrite it in a way that is more **{self.discOne.upper()}** and **{self.discTwo.upper()}** — while keeping the original meaning of the message the same.

            ⚠️ DO NOT respond to the message. DO NOT comment on it. DO NOT change the meaning.

            Only rephrase the message in a new tone and return the modified version **only**.

            Original Message:
            "{message}"

            Output:
            <transformed message only – no explanation, no intro, no formatting>
            """
        # stream is used to define wether items should be streamd one at at time (True) or all in one message (False)
        data = {'model': self.model, 'prompt': self.prompt, 'stream': False}
        logging.debug(self.prompt)
        with requests.post(self.url, json=data, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    json_line = line.decode('utf-8')
                    response_data = json.loads(json_line)
                    if response_data['response']:
                        # print(response_data['response'], end='', flush=True)
                        logging.debug(response_data)
                        return response_data['response']

    def getDefaultResponse(self) -> any:
        # Generate the response and send it to the UI
        model = self.model  # local model
        message = "hi there i enjoyed our time"
        prompt = f"""
          You are an AI that transforms customer messages for internal use.

          Your job is to take the original message below and rewrite it in a way that is more **{self.discOne.upper()}** and **{self.discTwo.upper()}** — while keeping the original meaning of the message the same.

        ⚠️ DO NOT respond to the message. DO NOT comment on it. DO NOT change the meaning.

        Only rephrase the message in a new tone and return the modified version **only**.

        Original Message:
        "{message}"

        Output:
        <transformed message only – no explanation, no intro, no formatting>
        """ 
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

from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)


def llmQuery(model, prompt, url='http://localhost:11434/api/generate'):
    # Use the generate function for a one-off prompt

    # stream is used to define wether items should be streamd one at at time (True) or all in one message (False)
    data = {'model': model, 'prompt': prompt, 'stream': False}

    with requests.post(url, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                json_line = line.decode('utf-8')
                response_data = json.loads(json_line)
                if response_data['response']:
                    # print(response_data['response'], end='', flush=True)
                    return response_data['response']


@app.route('/api/data', methods=['GET'])
def GetDefaultResponse():
    # Generate the response and send it to the UI
    model = 'smollm2:135m'  # local model
    prompt = 'Why is the sky blue? keep your response under one paragraph'
    url = 'http://localhost:11434/api/generate'

    response = llmQuery(model, prompt, url)

    # data = {'message': response}
    # return jsonify(data)

    return response


@app.route('/api/data', methods=['POST'])
def PostNewQuery():

    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'prompt' not in request_data:
        return jsonify({'error': 'Invalid request, "prompt" is required'}), 400

    # Extract the prompt from the request
    prompt = request_data['prompt']

    model = 'smollm2:135m'  # local model
    url = 'http://localhost:11434/api/generate'

    response = llmQuery(model, prompt, url)

    # Return the response as JSON
    return jsonify({'response': response})

    # return response


def main():
    print("Starting the Flask app...")
    app.run(debug=True)


if __name__ == "__main__":
    main()


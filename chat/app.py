import os
import openai
from flask import Flask, request, jsonify
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.logging import Logger
from aws_lambda_wsgi import response as awslambda_wsgi_response

app = Flask(__name__)

OPENAI_ORGANIZATION_ID = os.getenv('OPENAI_ORGANIZATION_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORGANIZATION_ID

logger = Logger()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('user_input')
    if not user_input:
        return jsonify({'error': 'User input is required'}), 400

    messages = [
        {"role": "system", "content": "You are a customer support chat from Imediato Náutica, an online e-commerce store for marine products. You only answer product-related questions."},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        assistant_response = response.choices[0].message['content']
        return jsonify({'response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@lambda_handler_decorator(logger=logger.inject_lambda_context(correlation_paths.API_GATEWAY_REST))
def lambda_handler(event, context):
    return awslambda_wsgi_response(app, event, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


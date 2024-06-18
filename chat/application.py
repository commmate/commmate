import os
from flask import Flask, request, jsonify
import openai
import awsgi

application = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@application.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "user_input is required"}), 400

    messages = [
        {"role": "system", "content": "You are a customer support chat from Imetiato Nautica, an online e-commerce store for marine products. You only answer product-related questions."},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        assistant_response = response['choices'][0]['message']['content']
        return jsonify({"response": assistant_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def lambda_handler(event, context):
    return awsgi.response(application, event, context)

if __name__ == "__main__":
    application.run(debug=True)


import os
from flask import Flask, request, jsonify
from openai import OpenAI
import awsgi

application = Flask(__name__)

# Configuração da API OpenAI
client = OpenAI(
    organization=os.getenv('OPENAI_ORGANIZATION_ID'),
    project=os.getenv('OPENAI_PROJECT_ID')
)

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
        # Chamada para a API OpenAI usando o modelo gpt-3.5-turbo
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Constrói a resposta do assistente
        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
        
        messages.append({"role": "assistant", "content": response})

        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def lambda_handler(event, context):
    return awsgi.response(application, event, context)

if __name__ == "__main__":
    application.run(debug=True)


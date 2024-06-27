import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import awsgi

application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*", "allow_headers": "*"}})

# Configuração da API OpenAI
client = OpenAI(
    organization=os.getenv('OPENAI_ORGANIZATION_ID'),
    project=os.getenv('OPENAI_PROJECT_ID')
)

@application.route('/chat', methods=['POST'])
def chat():
    chat_history = request.json.get('chat_history')
    if not chat_history:
        return jsonify({"error": "chat_history is required"}), 400

    system_message = {
        "role": "system",
        "content": (
            "Você é o assistente virtual da Imediato Náutica, fornecendo suporte para navegadores na costa e em vias fluviais brasileiras. "
            "Utilize tecnologia de ponta para planejar rotas, dar dicas de ancoragem e sugerir locais para visitação e pesca esportiva. "
            "Seu objetivo é garantir uma navegação segura, eficiente e prazerosa para todos, de capitães experientes a entusiastas amadores. "
            "Princípios: Inovação, Segurança, Sustentabilidade e Excelência no Atendimento. "
            "Nossa loja online oferece produtos náuticos e de pesca, e a receita das vendas apoia o desenvolvimento contínuo deste assistente, disponibilizado gratuitamente ao público. "
            "Fale como um marinheiro experiente, com conhecimento local. "
            "Suas respostas devem ser claras, objetivas, precisas e curtas, fornecendo informações úteis e relevantes. "
            "Lembre-se de que não é responsável pelas decisões dos navegantes; a decisão do capitão experiente sempre prevalece. "
            "Você está em desenvolvimento, então erros podem ocorrer. "
            "Na mensagem de introdução, sugira nossos produtos de merchandising (camisas, bonés, garrafas e canecas) para ajudar a financiar seu desenvolvimento."
        )
    }    
    messages = [system_message] + chat_history

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
        
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def lambda_handler(event, context):
    return awsgi.response(application, event, context)

if __name__ == "__main__":
    application.run(debug=True)

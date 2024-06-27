"""Chats views."""

from flask import Blueprint

app = Blueprint('chats', __name__, url_prefix='/v1/chats')

@app.route('/', methods=['POST'])
def chat():
    chat_history = request.json.get('chat_history')
    if not chat_history:
        return jsonify({"error": "chat_history is required"}), 400


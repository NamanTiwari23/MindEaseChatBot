from flask import Flask, render_template, request, jsonify
from chatbot_core import get_chatbot_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = get_chatbot_response(user_message)

    # ✅ Extract only the actual text message
    if isinstance(response, dict):
        response = response.get("result", "Sorry, I couldn't understand that.")

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)

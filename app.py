import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load all JSON phone spec files from templates/data
def load_all_phone_data():
    data_folder = os.path.join('templates', 'data')
    phone_db = {}
    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                phone = json.load(f)
                phone_name = phone.get("phone_name", "").lower()
                if phone_name:
                    phone_db[phone_name] = phone
    return phone_db

# Load all phones once
all_phone_data = load_all_phone_data()

# Try to extract phone name from user input
def extract_phone_name(user_input):
    user_input = user_input.lower()
    for phone_name in all_phone_data.keys():
        if phone_name in user_input:
            return phone_name
    return None

# Chatbot response
def get_response(user_input):
    user_input_lower = user_input.lower()
    phone_name = extract_phone_name(user_input_lower)

    if not phone_name:
        return "Please specify the phone name you want specs for."

    phone_data = all_phone_data.get(phone_name)
    if not phone_data:
        return "Sorry, phone not found."

    specs = phone_data.get("specifications", {})
    response_lines = [f"<strong>Specifications for {phone_data.get('phone_name', 'Unknown')}:</strong><br><br>"]

    for section, items in specs.items():
        response_lines.append(f"<strong>{section}:</strong>")
        if isinstance(items, dict):
            for k, v in items.items():
                response_lines.append(f"{k}: {v}")
        elif isinstance(items, str):
            response_lines.append(items)
        response_lines.append("<br>")

    return "<br>".join(response_lines)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def chat():
    user_input = request.form.get('user_input', '')
    reply = get_response(user_input)
    return jsonify(response=reply)

if __name__ == '__main__':
    app.run(debug=True)

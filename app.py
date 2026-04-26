from flask import Flask, render_template, request, jsonify
import json
import re

app = Flask(__name__)

# Load chatbot data from JSON file
def load_chatbot_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("data.json not found!")
        return None

# Process user message and find matching intent
def get_bot_response(user_message):
    data = load_chatbot_data()
    if not data:
        return "Sorry, chatbot data not loaded properly."
    
    user_message = user_message.lower().strip()
    
    # Loop through all intents
    for intent in data['intents']:
        patterns = intent['patterns']
        
        # Check if any pattern matches the user message
        for pattern in patterns:
            # Simple keyword matching (case insensitive)
            if re.search(pattern.lower(), user_message):
                # Return random response from responses list
                responses = intent['responses']
                return responses[0] if len(responses) > 0 else "No response available."
    
    # If no match found, return fallback response
    fallback_intent = next((intent for intent in data['intents'] if intent['tag'] == 'fallback'), None)
    if fallback_intent:
        return fallback_intent['responses'][0]
    
    return "I don't understand. Please ask about admissions, courses, fees, hostel, placements, or contact info."

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from frontend"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        # Handle empty message
        if not user_message:
            return jsonify({'response': 'Please type something!'})
        
        # Get bot response
        bot_response = get_bot_response(user_message)
        
        return jsonify({'response': bot_response})
    
    except Exception as e:
        return jsonify({'response': 'Sorry, something went wrong!'})

if __name__ == '__main__':
    print("🚀 Starting MITAOE Chatbot on http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000, host='0.0.0.0')
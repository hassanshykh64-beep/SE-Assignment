from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

API_KEYS = {
    "consumer_1": secrets.token_hex(16),
    "consumer_2": secrets.token_hex(16),
    "consumer_3": secrets.token_hex(16)
}

print("--- YOUR GENERATED KEYS (FOR TESTING) ---")
for user, key in API_KEYS.items():
    print(f"{user}: {key}")
print("-----------------------------------------")

@app.route('/process', methods=['POST'])
def process_text():

    req_key = request.headers.get('X-API-Key')
    if req_key not in API_KEYS.values():
        return jsonify({"error": "Invalid or missing API key"}), 401
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Text missing in JSON"}), 400
        
    processed = data['text'].upper()
    return jsonify({"processed_text": processed})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
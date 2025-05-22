# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the key is available
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found in environment.")

# Set OpenAI API key
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allows requests from your desktop app

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        model = data.get("model", "gpt-3.5-turbo")

        if not prompt:
            return jsonify({"success": False, "error": "Missing prompt."}), 400

        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for resume writing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        content = response.choices[0].message.content.strip()
        return jsonify({"success": True, "response": content})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
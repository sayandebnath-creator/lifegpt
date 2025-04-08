from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI  # ⬅️ NEW IMPORT

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ⬅️ NEW STYLE

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/life-advice', methods=['POST'])
def life_advice():
    data = request.json
    name = data.get('name', 'User')
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "Question required"}), 400

    prompt = f"""
You are LifeGPT, a wise life strategist.
Name: {name}
Question: {question}
Give thoughtful and human advice.
"""

    try:
        response = client.chat.completions.create(  # ⬅️ NEW SYNTAX
            model="gpt-3.5-turbo",  # or "gpt-4o" if you have access
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

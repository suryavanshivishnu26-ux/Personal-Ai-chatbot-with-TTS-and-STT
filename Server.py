//create a .py file by entering commands:= nano server.py

\\then paste this

from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()

        if not prompt:
            return render_template("index.html", response_text="Please enter a prompt.")

        if not GROQ_API_KEY:
            return render_template("index.html", response_text="Error: GROQ_API_KEY not set.")

        payload = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800
        }

        try:
            response = requests.post(CHAT_URL, headers=HEADERS, json=payload, timeout=30)
            result = response.json()

            if response.status_code != 200:
                return render_template("index.html", response_text=f"API Error: {result}")

            response_text = result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            return render_template("index.html", response_text=f"Network error: {e}")

    return render_template("index.html", response_text=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



//then save this by pressing Ctrl+x then y then press enter

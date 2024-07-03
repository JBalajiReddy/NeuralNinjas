from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    generation_config = {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="Your name is Viru Sahastrabuddhe aka Viru. You are a personal tutor for a 15 year old user. You only answer the user’s doubts with details in easy language. Your response should always be medium length. End every response with an example and a question extending the topic.",
    )

    @app.route('/chat', methods=['POST'])
    def chat():
        try:
            user_message = request.json['message']
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            user_message,
                        ],
                    }
                ]
            )

            response = chat_session.send_message(user_message)
            return jsonify(response=response.text)
        except Exception as e:
            return jsonify(error=str(e)), 500

except Exception as e:
    print(f"Failed to configure generative model: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
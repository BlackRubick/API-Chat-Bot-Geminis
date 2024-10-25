from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import time

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = "AIzaSyBF4SR86JOiOpU44NBZw7jKRGYuCPjsKkk"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question", "")
    history = data.get("history", "")  # Obtener el historial

    if not question:
        return jsonify({"error": "No question provided."}), 400

    # Aquí se genera el contenido
    model = genai.GenerativeModel('gemini-1.5-flash')
    start_time = time.time()

    # Concatenar el historial y la nueva pregunta
    full_prompt = f"{history}\nUsuario: {question}\nBot: "  # Formato de conversación

    # Generar la respuesta
    response = model.generate_content(full_prompt)

    elapsed_time = time.time() - start_time
    answer = response.text

    # Verificar si hubo algún error con la respuesta
    feedback = response.prompt_feedback if response.prompt_feedback else None

    return jsonify({
        "answer": answer,
        "elapsed_time": elapsed_time,
        "feedback": feedback
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

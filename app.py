from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from config import BASE_URL, API_KEY, LLM_MODEL, SYSTEM_INSTRUCTION
from rag_pipeline import RAGPipeline

app = Flask(__name__)

# --- SYSTEM INITIALIZATION ---
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
rag = RAGPipeline()

# Define the global conversation history
conversation_history = [
    {"role": "system", "content": SYSTEM_INSTRUCTION}
]

@app.route('/')
def home():
    """Renders the primary web interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles conversational interactions with dynamic context retrieval."""
    user_input = request.json.get('message', '').strip()
    if not user_input:
        return jsonify({"response": "I didn't catch that. Could you please repeat?"})

    # Step 1: Optimize query and retrieve relevant DB context
    optimized_query = rag.optimize_query(user_input, conversation_history, client, LLM_MODEL)
    context_text = rag.retrieve_context(optimized_query)

    # Step 2: Append user input to history, but securely inject document context 
    # directly into the immediate payload so it doesn't pollute ongoing memory.
    conversation_history.append({"role": "user", "content": user_input})
    messages_to_send = conversation_history.copy()
    
    if context_text:
        messages_to_send[-1] = {
            "role": "user",
            "content": f"{user_input}\n\n{context_text}"
        }

    # Step 3: Send to LLM
    try:
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages_to_send,
            temperature=0.4,
        )
        bot_response = completion.choices[0].message.content

        # Save clean assistant response back to history
        conversation_history.append({"role": "assistant", "content": bot_response})
        return jsonify({"response": bot_response})

    except Exception as e:
        conversation_history.pop()  # Safe rollback on failed generation
        print(f"❌ Generation error: {e}")
        return jsonify({"response": f"I encountered an error. Please try again. ({str(e)})"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
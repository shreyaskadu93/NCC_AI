import time
from flask import Flask, request, jsonify
import main
from llama_index.core import QueryBundle


app = Flask(__name__)
chat_engine = None


@app.route('/ask', methods=['POST'])
def ask_question():
    global chat_engine
    if chat_engine is None:
        chat_engine=main.main() 
    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = request.json
    if 'question' not in data:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    query = data['question']
    # Get the answer from the chain
    start = time.time()
    response = chat_engine.chat(query)
    ref_nodes=response.source_nodes
    ref_docs=[]
    for i in ref_nodes:
        ref_docs.append(i.metadata.get('file_name'))
    answer = str(response)
    end = time.time()
    time_taken=end-start
    

    return jsonify({"answer": answer,"time_taken":round(time_taken,2),"ref_docs": ref_docs})


if __name__ == "__main__":
    chat_engine=main.main() 
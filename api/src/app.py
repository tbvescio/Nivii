from flask import Flask, request, jsonify
from flask_cors import CORS
from infrastructure.llm.openai_llm import OpenaiLLMModel
from infrastructure.db.postgres_repository import PostgresRepository
from utils.utils import error_handling
from services.analyze_service import AnalyzeService
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
CORS(app)


analyze_service = AnalyzeService(
    db=PostgresRepository(),
    llm_model=OpenaiLLMModel(api_key=os.environ["OPENAI_KEY"])
)


@app.route('/analyze', methods=['GET'])
@error_handling
def analyze():
    if 'text' not in request.args or not request.args['text'].strip():
        logging.warning("Missing or empty 'text' parameter in /analyze request")
        return jsonify({"error": "Text parameter is required and cannot be empty"}), 400
    text = request.args['text']

    result = analyze_service.analyze(text)
    return jsonify(result), 200


@app.route('/info', methods=['GET'])
@error_handling
def info():
    return jsonify({
        "status": "OK"
    }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)

from infrastructure.llm.llm import LLMModel
from infrastructure.db.repository import DatabaseRepository
import logging


class AnalyzeService:
    def __init__(self, db: DatabaseRepository, llm_model: LLMModel):
        self.db = db
        self.llm_model = llm_model

    def analyze(self, text: str):
        logging.info(f"Received analyze request with text: {text}")
        query = self.llm_model.natural_language_to_sql(self.db.get_schema(), text)
        logging.info(f"Generated SQL query: {query}")
        result = self.db.execute(query)
        logging.info(f"Query result: {result}")
        if not result or (isinstance(result, list) and len(result) == 0):
            logging.warning(f"Empty result for query: {query}")
            return {
                "result": [],
                "query": query,
                "chart_type": "none",
                "analysis": "No data found for your request. Please try a different question."
            }
        chart_type, analysis = self.llm_model.suggest_chart_and_analysis(text, query, result)
        return {
            "result": result,
            "query": query,
            "chart_type": chart_type,
            "analysis": analysis
        } 
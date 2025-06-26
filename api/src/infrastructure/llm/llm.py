from abc import ABC 

class LLMModel(ABC):
    def natural_language_to_sql(self, schema: dict, text: str) -> str:
        """Convert a string of text to a SQL query string."""
        pass 

    def suggest_chart_and_analysis(self, user_input: str, query: str, result: any) -> tuple[str, str]:
        """Analyzes a SQL query and result."""
        pass
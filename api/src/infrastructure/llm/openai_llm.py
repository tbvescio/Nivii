import openai
import json
from infrastructure.llm.llm import LLMModel
from utils.exception import APIException

class OpenaiLLMModel(LLMModel):
    def __init__(self, model: str = 'gpt-4o-mini', api_key: str = None):
        self.model = model
        self.api_key = api_key
        openai.api_key = self.api_key

    def natural_language_to_sql(self, schema: dict, user_input: str) -> str:
        prompt = f"""
        You are an expert SQL generator. Your task is to generate a PostgreSQL query from a database schema and a text string
        representing a request made by a user in natural language.
        
        <schema>
        {schema}
        </schema>
        
        <user_input>
        {user_input}
        </user_input>

        Make sure that the user input makes sense and is possible to fulfill, if it doesn't or is not possible to fulfill then your output should 
        be exactly \"ERROR\" and nothing more.

        The data generate by your query will ideally be use to generate a chart (line, bar or pie) so adjust your query accordingly. Because of this,
        avoid making queries that return too many rows as this will not make it possible to generate the chart. Avoid queries that return more
        than 10 rows. If it's not possible to make a query from the user input that results in chartable information then return all available data.
        
        The user's request may be vague and non-specific, in that case generate a query that made sense given the schema
        and request.
        
        Your response should be a string that is a SQL query.
        
        If your response is other than a SQL query or \"ERROR\" you have failed your task. Do not include any markdown or text other than the query.
        """
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        output = response.choices[0].message.content.strip().replace("```json", "").replace("```", "")
        if output == "ERROR":
            raise APIException("Invalid request. Make sure the prompt is valid.", 400)
        return output

    def suggest_chart_and_analysis(self, user_input: str, query: str, result: any) -> tuple[str, str]:
        prompt = f"""
        You will be given a database SQL query, a user input request and the result of executing the query.
        Based on the that, you should determine which type of chart would be most appropriate to be genreated from the result 
        (line, bar or pie) and also analyze and provide a summary of the result. 
        If the results are not able to be charted then chart_type should be equal to \"table\".
        
        <user_input>
        {user_input}
        </user_input>
        
        <query>
        {query}
        </query>

        <result>
        {result}
        </result>

        Your response should be a JSON object with the following format:
        <format>
        {{
            "chart_type": <CHART_TYPE>,
            "analysis": <ANALYSIS>
        }}
        </format>
        
        The analysis should be tailored to the user request and not be related or mention anything about the SQL query or which chart
        is more effective. It should mention what does the result imply and what insights can be gathered from it.
        
        Your response should only include the JSON object.
        
        If your response is other than a JSON object you have failed your task. Do not include any markdown or text other than the JSON.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            output = response.choices[0].message.content.strip().replace("```json", "").replace("```", "")
            parsed_output = json.loads(output)
            return parsed_output["chart_type"], parsed_output["analysis"]
        except Exception as e:
            raise APIException(f"OpenAI API error: {str(e)}", 500) 
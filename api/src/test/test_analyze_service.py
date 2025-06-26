import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock
from services.analyze_service import AnalyzeService
from utils.exception import APIException

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.get_schema.return_value = {'sales_data': [{'name': 'total', 'type': 'numeric'}]}
    return db

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    return llm

# Test: normal result
def test_analyze_normal_result(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.return_value = [(100,)]
    mock_llm.suggest_chart_and_analysis.return_value = ("bar", "Total sales is 100.")
    service = AnalyzeService(mock_db, mock_llm)
    result = service.analyze("total sales by week")
    assert result["result"] == [(100,)]
    assert result["query"] == 'SELECT total FROM sales_data'
    assert result["chart_type"] == "bar"
    assert result["analysis"] == "Total sales is 100."

def test_analyze_empty_result(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.return_value = []
    service = AnalyzeService(mock_db, mock_llm)
    result = service.analyze("total sales by week")
    assert result["result"] == []
    assert result["chart_type"] == "none"
    assert "No data found" in result["analysis"]

def test_analyze_llm_error(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.side_effect = APIException("LLM error", 500)
    service = AnalyzeService(mock_db, mock_llm)
    with pytest.raises(APIException) as excinfo:
        service.analyze("total sales by week")
    assert "LLM error" in str(excinfo.value)

def test_analyze_db_error(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.side_effect = APIException("DB error", 500)
    service = AnalyzeService(mock_db, mock_llm)
    with pytest.raises(APIException) as excinfo:
        service.analyze("total sales by week")
    assert "DB error" in str(excinfo.value)

def test_analyze_suggest_chart_error(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.return_value = [(100,)]
    mock_llm.suggest_chart_and_analysis.side_effect = APIException("Suggest error", 500)
    service = AnalyzeService(mock_db, mock_llm)
    with pytest.raises(APIException) as excinfo:
        service.analyze("total sales by week")
    assert "Suggest error" in str(excinfo.value)

def test_analyze_none_text(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.return_value = [(100,)]
    mock_llm.suggest_chart_and_analysis.return_value = ("bar", "Total sales is 100.")
    service = AnalyzeService(mock_db, mock_llm)
    result = service.analyze(None)
    assert result["result"] == [(100,)]
    assert result["query"] == 'SELECT total FROM sales_data'
    assert result["chart_type"] == "bar"
    assert result["analysis"] == "Total sales is 100."

def test_analyze_empty_string_text(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.return_value = [(100,)]
    mock_llm.suggest_chart_and_analysis.return_value = ("bar", "Total sales is 100.")
    service = AnalyzeService(mock_db, mock_llm)
    result = service.analyze("")
    assert result["result"] == [(100,)]
    assert result["query"] == 'SELECT total FROM sales_data'
    assert result["chart_type"] == "bar"
    assert result["analysis"] == "Total sales is 100."

def test_analyze_non_list_result(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.return_value = 100
    mock_llm.suggest_chart_and_analysis.return_value = ("bar", "Total sales is 100.")
    service = AnalyzeService(mock_db, mock_llm)
    result = service.analyze("total sales by week")
    assert result["result"] == 100
    assert result["query"] == 'SELECT total FROM sales_data'
    assert result["chart_type"] == "bar"
    assert result["analysis"] == "Total sales is 100."

def test_analyze_result_list_of_none(mock_db, mock_llm):
    mock_llm.natural_language_to_sql.return_value = 'SELECT total FROM sales_data'
    mock_db.execute.return_value = [None, None]
    mock_llm.suggest_chart_and_analysis.return_value = ("bar", "All values are None.")
    service = AnalyzeService(mock_db, mock_llm)
    result = service.analyze("total sales by week")
    assert result["result"] == [None, None]
    assert result["query"] == 'SELECT total FROM sales_data'
    assert result["chart_type"] == "bar"
    assert result["analysis"] == "All values are None." 
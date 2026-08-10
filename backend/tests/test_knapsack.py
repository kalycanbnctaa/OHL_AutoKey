import json
from pathlib import Path
import math
import pytest

from app.core.knapsack import solve_knapsack
from app.services.dictionary_service import DictionaryService
from app.services.smart_trim_service import SmartTrimService


@pytest.fixture
def dictionary_service(tmp_path: Path):
    path = tmp_path / "kamus.json"
    path.write_text(
        json.dumps({
            "program": 1000,
            "dinamis": 500,
            "ini": 2000,
            "cukup": 300,
            "sulit": 150,
            "a": 10,
            "b": 20,
            "c": 30,
        }),
        encoding="utf-8"
    )
    service = DictionaryService(path)
    service.load()
    return service


def test_solve_knapsack_basic():
    items = [("a", 2, 10.0), ("b", 3, 15.0), ("c", 5, 20.0)]
    result = solve_knapsack(items, 5)
    assert result is not None
    assert result.total_value == 25.0
    assert result.total_weight == 5
    assert len(result.items) == 2
    item_names = {item[0] for item in result.items}
    assert item_names == {"a", "b"}


def test_solve_knapsack_exact_capacity():
    items = [("a", 3, 10.0), ("b", 3, 15.0), ("c", 4, 20.0)]
    result = solve_knapsack(items, 6)
    assert result is not None
    assert result.total_value == 25.0
    assert result.total_weight == 6
    item_names = {item[0] for item in result.items}
    assert item_names == {"a", "b"}


def test_solve_knapsack_capacity_zero():
    items = [("a", 2, 10.0)]
    result = solve_knapsack(items, 0)
    assert result is not None
    assert result.total_value == 0.0
    assert result.total_weight == 0
    assert len(result.items) == 0


def test_solve_knapsack_empty_items():
    result = solve_knapsack([], 10)
    assert result is None


def test_solve_knapsack_one_item_fits():
    items = [("a", 3, 10.0)]
    result = solve_knapsack(items, 5)
    assert result is not None
    assert result.total_value == 10.0
    assert result.total_weight == 3


def test_solve_knapsack_one_item_too_heavy():
    items = [("a", 6, 10.0)]
    result = solve_knapsack(items, 5)
    assert result is not None
    assert result.total_value == 0.0
    assert result.total_weight == 0


def test_solve_knapsack_all_items_fit():
    items = [("a", 2, 10.0), ("b", 2, 15.0), ("c", 2, 20.0)]
    result = solve_knapsack(items, 6)
    assert result is not None
    assert result.total_value == 45.0
    assert result.total_weight == 6
    assert len(result.items) == 3


def test_solve_knapsack_no_items_fit_due_to_weight():
    items = [("a", 6, 10.0), ("b", 7, 15.0)]
    result = solve_knapsack(items, 5)
    assert result is not None
    assert result.total_value == 0.0
    assert result.total_weight == 0
    assert len(result.items) == 0


def test_solve_knapsack_items_with_zero_weight():
    items = [("a", 0, 10.0), ("b", 2, 15.0)]
    result = solve_knapsack(items, 2)
    assert result is not None
    assert result.total_value == 25.0
    assert result.total_weight == 2
    item_names = {item[0] for item in result.items}
    assert item_names == {"a", "b"}


def test_smart_trim_service_success(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("program dinamis ini cukup sulit", 15)
    assert result is not None
    assert result.total_weight <= 15
    assert len(result.items) > 0
    assert result.total_value > 0


def test_smart_trim_service_empty_text(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("", 10)
    assert result is None


def test_smart_trim_service_invalid_words(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("xyz abc def", 10)
    assert result is None


def test_smart_trim_service_limit_zero(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("program dinamis", 0)
    assert result is None


def test_smart_trim_service_keeps_high_value_words(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("ini program dinamis", 15)
    assert result is not None
    assert result.total_weight <= 15
    item_names = {item[0] for item in result.items}
    assert "program" in item_names
    assert "dinamis" in item_names


def test_smart_trim_service_limit_less_than_all_words(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("program dinamis", 10)
    assert result is not None
    assert result.total_weight <= 10
    assert len(result.items) == 1


def test_smart_trim_service_limit_greater_than_all_words(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("program dinamis", 20)
    assert result is not None
    assert result.total_weight == 14
    item_names = {item[0] for item in result.items}
    assert item_names == {"program", "dinamis"}


def test_smart_trim_service_prefers_high_value_words(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("ini program", 10)
    assert result is not None
    item_names = {item[0] for item in result.items}
    assert "program" in item_names
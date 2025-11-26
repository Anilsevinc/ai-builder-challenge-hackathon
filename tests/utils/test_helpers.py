"""Tests for helper functions"""

import pytest
from src.utils.helpers import (
    parse_matrix_string,
    extract_expression_from_command,
    validate_numeric_result,
    format_result_for_display,
)


def test_parse_matrix_string_valid():
    """parse_matrix_string - geçerli matris"""
    result = parse_matrix_string("[[1,2],[3,4]]")
    assert result == [[1, 2], [3, 4]]


def test_parse_matrix_string_single_row():
    """parse_matrix_string - tek satır"""
    result = parse_matrix_string("[[1,2,3]]")
    assert result == [[1, 2, 3]]


def test_parse_matrix_string_invalid_format():
    """parse_matrix_string - geçersiz format"""
    with pytest.raises(ValueError, match="Matris format hatasi"):
        parse_matrix_string("1,2,3")


def test_parse_matrix_string_not_list():
    """parse_matrix_string - liste değil"""
    with pytest.raises(ValueError, match="Matris parse hatasi"):
        parse_matrix_string('"not a list"')


def test_parse_matrix_string_invalid_syntax():
    """parse_matrix_string - geçersiz syntax"""
    with pytest.raises(ValueError, match="Matris parse hatasi"):
        parse_matrix_string("[[1,2,invalid]]")


def test_extract_expression_from_command_calculus():
    """extract_expression_from_command - calculus prefix"""
    result = extract_expression_from_command("!calculus x^2")
    assert result == "x^2"


def test_extract_expression_from_command_linalg():
    """extract_expression_from_command - linalg prefix"""
    result = extract_expression_from_command("!linalg [[1,2],[3,4]]")
    assert result == "[[1,2],[3,4]]"


def test_extract_expression_from_command_solve():
    """extract_expression_from_command - solve prefix"""
    result = extract_expression_from_command("!solve 2x + 4 = 0")
    assert result == "2x + 4 = 0"


def test_extract_expression_from_command_plot():
    """extract_expression_from_command - plot prefix"""
    result = extract_expression_from_command("!plot x^2")
    assert result == "x^2"


def test_extract_expression_from_command_finance():
    """extract_expression_from_command - finance prefix"""
    result = extract_expression_from_command("!finance NPV 1000 0.1 5")
    assert result == "NPV 1000 0.1 5"


def test_extract_expression_from_command_no_prefix():
    """extract_expression_from_command - prefix yok"""
    result = extract_expression_from_command("2 + 2")
    assert result == "2 + 2"


def test_extract_expression_from_command_case_insensitive():
    """extract_expression_from_command - büyük/küçük harf duyarsız"""
    result = extract_expression_from_command("!CALCULUS x^2")
    assert result == "x^2"


def test_validate_numeric_result_float():
    """validate_numeric_result - float"""
    assert validate_numeric_result(42.5) is True


def test_validate_numeric_result_int():
    """validate_numeric_result - int"""
    assert validate_numeric_result(42) is True


def test_validate_numeric_result_list_of_floats():
    """validate_numeric_result - float listesi"""
    assert validate_numeric_result([1.0, 2.0, 3.0]) is True


def test_validate_numeric_result_list_of_ints():
    """validate_numeric_result - int listesi"""
    assert validate_numeric_result([1, 2, 3]) is True


def test_validate_numeric_result_string():
    """validate_numeric_result - string"""
    assert validate_numeric_result("42") is False


def test_validate_numeric_result_mixed_list():
    """validate_numeric_result - karışık liste"""
    assert validate_numeric_result([1, "2", 3.0]) is False


def test_format_result_for_display_float():
    """format_result_for_display - float"""
    result = format_result_for_display(42.5)
    assert result == "42.5"


def test_format_result_for_display_float_integer():
    """format_result_for_display - float ama integer değer"""
    result = format_result_for_display(42.0)
    assert result == "42"


def test_format_result_for_display_float_trailing_zeros():
    """format_result_for_display - sıfırları temizleme"""
    result = format_result_for_display(42.500000)
    assert result == "42.5"


def test_format_result_for_display_int():
    """format_result_for_display - int"""
    result = format_result_for_display(42)
    assert result == "42"


def test_format_result_for_display_list():
    """format_result_for_display - liste"""
    result = format_result_for_display([1, 2, 3])
    assert result == "[1, 2, 3]"


def test_format_result_for_display_dict():
    """format_result_for_display - dict"""
    result = format_result_for_display({"x": 1, "y": 2})
    assert '"x": 1' in result
    assert '"y": 2' in result


def test_format_result_for_display_string():
    """format_result_for_display - string"""
    result = format_result_for_display("test")
    assert result == "test"

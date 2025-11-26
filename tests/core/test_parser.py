"""Tests for command parser"""

from src.core.parser import CommandParser


def test_parser_prefix_calculus():
    """Parser - calculus prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!calculus x^2")
    assert module == "calculus"
    assert expression == "x^2"


def test_parser_prefix_calc():
    """Parser - calc prefix (kısa form)"""
    parser = CommandParser()
    module, expression = parser.parse("!calc derivative x^2")
    assert module == "calculus"
    assert expression == "derivative x^2"


def test_parser_prefix_basic():
    """Parser - basic prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!basic 2 + 2")
    assert module == "basic_math"
    assert expression == "2 + 2"


def test_parser_prefix_linalg():
    """Parser - linalg prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!linalg [[1,2],[3,4]]")
    assert module == "linear_algebra"
    assert expression == "[[1,2],[3,4]]"


def test_parser_prefix_linear():
    """Parser - linear prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!linear matrix multiply")
    assert module == "linear_algebra"
    assert expression == "matrix multiply"


def test_parser_prefix_matrix():
    """Parser - matrix prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!matrix [[1,2],[3,4]]")
    assert module == "linear_algebra"
    assert expression == "[[1,2],[3,4]]"


def test_parser_prefix_solve():
    """Parser - solve prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!solve 2x + 4 = 0")
    assert module == "equation_solver"
    assert expression == "2x + 4 = 0"


def test_parser_prefix_equation():
    """Parser - equation prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!equation x^2 - 1 = 0")
    assert module == "equation_solver"
    assert expression == "x^2 - 1 = 0"


def test_parser_prefix_plot():
    """Parser - plot prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!plot x^2")
    assert module == "graph_plotter"
    assert expression == "x^2"


def test_parser_prefix_graph():
    """Parser - graph prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!graph sin(x)")
    assert module == "graph_plotter"
    assert expression == "sin(x)"


def test_parser_prefix_finance():
    """Parser - finance prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!finance NPV 1000 0.1 5")
    assert module == "financial"
    assert expression == "NPV 1000 0.1 5"


def test_parser_prefix_financial():
    """Parser - financial prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!financial loan payment")
    assert module == "financial"
    assert expression == "loan payment"


def test_parser_prefix_stats():
    """Parser - stats prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!stats mean [1,2,3]")
    assert module == "statistics"
    assert expression == "mean [1,2,3]"


def test_parser_prefix_statistics():
    """Parser - statistics prefix"""
    parser = CommandParser()
    module, expression = parser.parse("!statistics std dev [1,2,3]")
    assert module == "statistics"
    assert expression == "std dev [1,2,3]"


def test_parser_prefix_stat():
    """Parser - stat prefix (kısa form)"""
    parser = CommandParser()
    module, expression = parser.parse("!stat median [1,2,3]")
    assert module == "statistics"
    assert expression == "median [1,2,3]"


def test_parser_natural_language_derivative():
    """Parser - doğal dil: derivative"""
    parser = CommandParser()
    module, expression = parser.parse("derivative of x^2")
    assert module == "calculus"
    assert expression == "derivative of x^2"


def test_parser_natural_language_integral():
    """Parser - doğal dil: integral"""
    parser = CommandParser()
    module, expression = parser.parse("integral of x")
    assert module == "calculus"
    assert expression == "integral of x"


def test_parser_natural_language_matrix():
    """Parser - doğal dil: matrix"""
    parser = CommandParser()
    module, expression = parser.parse("matrix multiplication")
    assert module == "linear_algebra"
    assert expression == "matrix multiplication"


def test_parser_natural_language_determinant():
    """Parser - doğal dil: determinant"""
    parser = CommandParser()
    module, expression = parser.parse("determinant of matrix")
    assert module == "linear_algebra"
    assert expression == "determinant of matrix"


def test_parser_natural_language_solve():
    """Parser - doğal dil: solve"""
    parser = CommandParser()
    module, expression = parser.parse("solve equation 2x = 4")
    assert module == "equation_solver"
    assert expression == "solve equation 2x = 4"


def test_parser_natural_language_plot():
    """Parser - doğal dil: plot"""
    parser = CommandParser()
    module, expression = parser.parse("plot function x^2")
    assert module == "graph_plotter"
    assert expression == "plot function x^2"


def test_parser_natural_language_npv():
    """Parser - doğal dil: NPV"""
    parser = CommandParser()
    module, expression = parser.parse("calculate NPV")
    assert module == "financial"
    assert expression == "calculate NPV"


def test_parser_natural_language_interest():
    """Parser - doğal dil: interest"""
    parser = CommandParser()
    module, expression = parser.parse("calculate interest rate")
    assert module == "financial"
    assert expression == "calculate interest rate"


def test_parser_natural_language_mean():
    """Parser - doğal dil: mean"""
    parser = CommandParser()
    module, expression = parser.parse("mean of [1,2,3]")
    assert module == "statistics"
    assert expression == "mean of [1,2,3]"


def test_parser_natural_language_std_dev():
    """Parser - doğal dil: standard deviation"""
    parser = CommandParser()
    module, expression = parser.parse("standard deviation of data")
    assert module == "statistics"
    assert expression == "standard deviation of data"


def test_parser_natural_language_correlation():
    """Parser - doğal dil: correlation"""
    parser = CommandParser()
    module, expression = parser.parse("correlation between x and y")
    assert module == "statistics"
    assert expression == "correlation between x and y"


def test_parser_default_basic_math():
    """Parser - default: basic math"""
    parser = CommandParser()
    module, expression = parser.parse("2 + 2")
    assert module == "basic_math"
    assert expression == "2 + 2"


def test_parser_whitespace_stripping():
    """Parser - whitespace temizleme"""
    parser = CommandParser()
    module, expression = parser.parse("  !calculus   x^2  ")
    assert module == "calculus"
    assert expression == "x^2"


def test_parser_turkish_keywords():
    """Parser - Türkçe keyword'ler"""
    parser = CommandParser()
    module, expression = parser.parse("turev x^2")
    assert module == "calculus"

    module, expression = parser.parse("matris carpimi")
    assert module == "linear_algebra"

    module, expression = parser.parse("denklem coz")
    assert module == "equation_solver"

    module, expression = parser.parse("grafik ciz")
    assert module == "graph_plotter"

    module, expression = parser.parse("faiz hesapla")
    assert module == "financial"

    module, expression = parser.parse("ortalama hesapla")
    assert module == "statistics"

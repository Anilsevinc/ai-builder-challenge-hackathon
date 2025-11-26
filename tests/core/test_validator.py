"""Tests for input validator"""

import pytest
from src.core.validator import InputValidator
from src.utils.exceptions import SecurityViolationError, InvalidInputError


def test_validator_sanitize_valid_expression():
    """Validator - geçerli ifade"""
    validator = InputValidator()
    result = validator.sanitize_expression("2 + 2")
    assert result == "2 + 2"


def test_validator_sanitize_whitespace():
    """Validator - whitespace temizleme"""
    validator = InputValidator()
    result = validator.sanitize_expression("  2 + 2  ")
    assert result == "2 + 2"


def test_validator_sanitize_empty_string():
    """Validator - boş string"""
    validator = InputValidator()
    with pytest.raises(
        InvalidInputError, match="Gecersiz giris: ifade string olmali"
    ):
        validator.sanitize_expression("")


def test_validator_sanitize_none():
    """Validator - None"""
    validator = InputValidator()
    with pytest.raises(InvalidInputError, match="ifade string olmali"):
        validator.sanitize_expression(None)


def test_validator_sanitize_not_string():
    """Validator - string değil"""
    validator = InputValidator()
    with pytest.raises(InvalidInputError, match="ifade string olmali"):
        validator.sanitize_expression(123)


def test_validator_sanitize_forbidden_eval():
    """Validator - yasaklı pattern: eval"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: eval"):
        validator.sanitize_expression("eval('malicious')")


def test_validator_sanitize_forbidden_exec():
    """Validator - yasaklı pattern: exec"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: exec"):
        validator.sanitize_expression("exec('code')")


def test_validator_sanitize_forbidden_import():
    """Validator - yasaklı pattern: __import__"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: __import__"):
        validator.sanitize_expression("__import__('os')")


def test_validator_sanitize_forbidden_os():
    """Validator - yasaklı pattern: os."""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: os."):
        validator.sanitize_expression("os.system('rm -rf /')")


def test_validator_sanitize_forbidden_subprocess():
    """Validator - yasaklı pattern: subprocess"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: subprocess"):
        validator.sanitize_expression("subprocess.call('ls')")


def test_validator_sanitize_forbidden_open():
    """Validator - yasaklı pattern: open"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: open"):
        validator.sanitize_expression("open('/etc/passwd')")


def test_validator_sanitize_forbidden_builtins():
    """Validator - yasaklı pattern: __builtins__"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: __builtins__"):
        validator.sanitize_expression("__builtins__['eval']")


def test_validator_sanitize_forbidden_globals():
    """Validator - yasaklı pattern: globals"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: globals"):
        validator.sanitize_expression("globals()['x']")


def test_validator_sanitize_forbidden_locals():
    """Validator - yasaklı pattern: locals"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: locals"):
        validator.sanitize_expression("locals()['x']")


def test_validator_sanitize_forbidden_compile():
    """Validator - yasaklı pattern: compile"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: compile"):
        validator.sanitize_expression("compile('code', 'file', 'exec')")


def test_validator_sanitize_forbidden_file():
    """Validator - yasaklı pattern: __file__"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: __file__"):
        validator.sanitize_expression("__file__")


def test_validator_sanitize_forbidden_name():
    """Validator - yasaklı pattern: __name__"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError, match="Yasakli ifade tespit edildi: __name__"):
        validator.sanitize_expression("__name__")


def test_validator_sanitize_case_insensitive():
    """Validator - büyük/küçük harf duyarsız kontrol"""
    validator = InputValidator()
    with pytest.raises(SecurityViolationError):
        validator.sanitize_expression("EVAL('test')")


def test_validator_validate_length_valid():
    """Validator - geçerli uzunluk"""
    validator = InputValidator()
    result = validator.validate_length("2 + 2")
    assert result is True


def test_validator_validate_length_too_long():
    """Validator - çok uzun ifade"""
    validator = InputValidator()
    long_expression = "x" * 1001
    with pytest.raises(InvalidInputError, match="Ifade cok uzun"):
        validator.validate_length(long_expression)


def test_validator_validate_length_custom_max():
    """Validator - özel maksimum uzunluk"""
    validator = InputValidator()
    long_expression = "x" * 101
    with pytest.raises(InvalidInputError):
        validator.validate_length(long_expression, max_length=100)


def test_validator_validate_numeric_expression_valid():
    """Validator - geçerli numerik ifade"""
    validator = InputValidator()
    result = validator.validate_numeric_expression("2 + 2 * 3")
    assert result is True


def test_validator_validate_numeric_expression_with_letters():
    """Validator - harfler içeren ifade"""
    validator = InputValidator()
    result = validator.validate_numeric_expression("x^2 + 2x + 1")
    assert result is True  # Harfler izin verilir


def test_validator_validate_numeric_expression_with_special_chars():
    """Validator - özel karakterler"""
    validator = InputValidator()
    result = validator.validate_numeric_expression("sin(x) + cos(y)")
    assert result is True


def test_validator_validate_numeric_expression_invalid_chars():
    """Validator - geçersiz karakterler"""
    validator = InputValidator()
    with pytest.raises(InvalidInputError, match="Gecersiz karakterler"):
        validator.validate_numeric_expression("test@#$%")


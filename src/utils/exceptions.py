"""Custom exceptions for Calculator Agent"""


class CalculationError(Exception):
    """Genel hesaplama hatası"""
    pass


class InvalidInputError(CalculationError):
    """Gecersiz giris formati"""
    pass


class GeminiAPIError(Exception):
    """Gemini API'den donen hata"""
    pass


class SecurityViolationError(Exception):
    """Guvenlik ihlali tespit edildi"""
    pass


class CalculatorModuleNotFoundError(Exception):
    """Modul bulunamadi"""
    pass

"""Natural language to semantic command parser"""

from typing import Dict, Optional, Tuple
from src.utils.logger import setup_logger

logger = setup_logger()


class CommandParser:
    """Dogal dil komutlarini semantik komutlara cevirir"""

    MODULE_PREFIXES: Dict[str, str] = {
        "basic": "basic_math",
        "calculus": "calculus",
        "calc": "calculus",
        "linalg": "linear_algebra",
        "linear": "linear_algebra",
        "matrix": "linear_algebra",
        "solve": "equation_solver",
        "equation": "equation_solver",
        "plot": "graph_plotter",
        "graph": "graph_plotter",
        "finance": "financial",
        "financial": "financial",
        "stats": "statistics",
        "statistics": "statistics",
        "stat": "statistics",
    }

    def parse(self, user_input: str) -> Tuple[Optional[str], str]:
        """Kullanici girdisini parse eder

        Args:
            user_input: Kullanici girdisi

        Returns:
            (modul_adi, ifade) tuple'i
        """
        user_input = user_input.strip()

        # Prefix kontrolü
        for prefix, module in self.MODULE_PREFIXES.items():
            if user_input.lower().startswith(f"!{prefix}"):
                expression = user_input[len(f"!{prefix}"):].strip()
                return module, expression

        # Doğal dil tespiti
        detected_module = self._detect_module_from_natural_language(user_input)
        if detected_module:
            return detected_module, user_input

        # Default: basic math
        return "basic_math", user_input

    def _detect_module_from_natural_language(self, text: str) -> Optional[str]:
        """Dogal dil ifadesinden modul tespit eder

        Args:
            text: Kullanici metni

        Returns:
            Modul adi veya None
        """
        text_lower = text.lower()

        # Calculus keywords
        calculus_keywords = [
            "derivative", "integral", "limit", "taylor", "gradient",
            "turev", "integral", "limit", "seri"
        ]
        if any(keyword in text_lower for keyword in calculus_keywords):
            return "calculus"

        # Linear algebra keywords
        linalg_keywords = [
            "matrix", "determinant", "eigenvalue", "vector", "matris",
            "determinant", "ozdeger", "vektor"
        ]
        if any(keyword in text_lower for keyword in linalg_keywords):
            return "linear_algebra"

        # Equation solver keywords
        equation_keywords = [
            "solve", "equation", "coz", "denklem", "kok"
        ]
        if any(keyword in text_lower for keyword in equation_keywords):
            return "equation_solver"

        # Graph plotter keywords
        plot_keywords = [
            "plot", "graph", "draw", "ciz", "grafik"
        ]
        if any(keyword in text_lower for keyword in plot_keywords):
            return "graph_plotter"

        # Financial keywords
        financial_keywords = [
            "npv", "irr", "loan", "interest", "faiz", "kredi", "yatirim"
        ]
        if any(keyword in text_lower for keyword in financial_keywords):
            return "financial"

        # Statistics keywords
        statistics_keywords = [
            "mean", "median", "mode", "average", "ortalama", "medyan", "mod",
            "std dev", "standard deviation", "standart sapma",
            "variance", "varyans",
            "correlation", "korelasyon",
            "z-score", "z score", "z skor",
            "percentile", "yuzdelik",
            "regression", "regresyon",
            "statistics", "istatistik"
        ]
        if any(keyword in text_lower for keyword in statistics_keywords):
            return "statistics"

        return None

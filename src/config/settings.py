"""Settings and configuration for Calculator Agent"""

import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Uygulama ayarlari"""

    def __init__(self) -> None:
        self.GEMINI_API_KEY: str = (
            os.getenv("GEMINI_API_KEY", "") or ""
        ).strip()
        self.GEMINI_MODEL: str = (
            os.getenv("GEMINI_MODEL", "gemini-2.5-flash") or
            "gemini-2.5-flash"
        ).strip()

        self.RATE_LIMIT_CALLS_PER_MINUTE: int = int(
            os.getenv("RATE_LIMIT_CALLS_PER_MINUTE", "60")
        )
        self.TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
        self.TOP_P: float = float(os.getenv("TOP_P", "0.95"))
        self.MAX_OUTPUT_TOKENS: int = int(
            os.getenv("MAX_OUTPUT_TOKENS", "2048")
        )
        self.MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
        self.RETRY_BACKOFF_BASE: int = int(
            os.getenv("RETRY_BACKOFF_BASE", "2")
        )

        self.SAFETY_SETTINGS: Dict[str, str] = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }
        self.DEFAULT_CURRENCY: str = os.getenv("DEFAULT_CURRENCY", "TRY")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def validate(self) -> bool:
        """Ayarlarin gecerli olup olmadigini kontrol eder"""
        if not self.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable gerekli. "
                "Lutfen .env dosyasina GEMINI_API_KEY ekleyin."
            )
        if self.GEMINI_API_KEY == "your_gemini_api_key":
            raise ValueError(
                "GECERSIZ API KEY: Placeholder deger kullanilamaz. "
                "Lutfen gecerli bir GEMINI_API_KEY ayarlayin."
            )
        return True


settings = Settings()

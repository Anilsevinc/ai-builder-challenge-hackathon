"""Gemini API communication layer"""

import asyncio
import json
import re
from typing import Any, Dict, Optional, Sequence

import google.generativeai as genai
import time
from src.config.settings import settings
from src.utils.exceptions import GeminiAPIError
from src.utils.logger import setup_logger

logger = setup_logger()


class RateLimiter:
    """Basit rate limiter"""

    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call_time = 0.0
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Rate limit kontrolu yapar"""
        async with self.lock:
            current_time = time.time()
            time_since_last_call = current_time - self.last_call_time

            if time_since_last_call < self.min_interval:
                wait_time = self.min_interval - time_since_last_call
                # Minimum 1 saniye bekle (Gemini API gereksinimi)
                actual_wait_time = max(wait_time, 1.0)
                await asyncio.sleep(actual_wait_time)

            self.last_call_time = time.time()


class GeminiAgent:
    """Gemini API ile iletisim sinifi"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """Gemini agent'i baslatir

        Args:
            api_key: Gemini API anahtari
            model_name: Model adi
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY gerekli")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            self.model_name,
            safety_settings=self._get_safety_settings()
        )
        self.rate_limiter = RateLimiter(settings.RATE_LIMIT_CALLS_PER_MINUTE)

    def _get_safety_settings(self) -> list:
        """Gemini guvenlik ayarlarini dondurur"""
        import google.generativeai.types as genai_types

        return [
            {
                "category": genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": genai_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                "threshold": genai_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": (
                    genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT
                ),
                "threshold": genai_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": (
                    genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT
                ),
                "threshold": genai_types.HarmBlockThreshold.BLOCK_NONE,
            },
        ]

    def _extract_response_text(self, response: Any) -> str:
        """Extract textual content from Gemini response safely."""
        if not response:
            return ""

        TEXT_ATTRS = ("text", "output_text")
        for attr in TEXT_ATTRS:
            text_value = getattr(response, attr, None)
            if isinstance(text_value, str) and text_value.strip():
                return text_value

        candidates: Sequence[Any] = getattr(response, "candidates", []) or []
        collected_parts: list[str] = []
        for candidate in candidates:
            finish_reason = getattr(candidate, "finish_reason", None)
            if finish_reason == 2:  # SAFETY or STOP reason without content
                continue
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) if content else None
            if not parts and isinstance(candidate, dict):
                parts = candidate.get("content", {}).get("parts")
            if not parts:
                continue
            for part in parts:
                part_text = getattr(part, "text", None)
                if isinstance(part_text, str) and part_text.strip():
                    collected_parts.append(part_text)
                elif isinstance(part, dict):
                    dict_text = part.get("text")
                    if isinstance(dict_text, str) and dict_text.strip():
                        collected_parts.append(dict_text)
        return "\n".join(collected_parts).strip()

    async def generate_with_retry(
        self,
        prompt: str,
        max_retries: Optional[int] = None
    ) -> str:
        """Rate limiting ve retry mekanizmasi ile Gemini cagrisi

        Args:
            prompt: Gonderilecek prompt
            max_retries: Maksimum deneme sayisi

        Returns:
            Gemini'den donen metin

        Raises:
            GeminiAPIError: API hatasi
        """
        max_retries = max_retries or settings.MAX_RETRIES
        await self.rate_limiter.acquire()

        for attempt in range(max_retries):
            try:
                generation_config = {
                    "temperature": settings.TEMPERATURE,
                    "top_p": settings.TOP_P,
                    "max_output_tokens": settings.MAX_OUTPUT_TOKENS,
                }

                response = await self.model.generate_content_async(
                    prompt,
                    generation_config=generation_config
                )

                response_text = self._extract_response_text(response)
                if not response_text:
                    finish_reason = getattr(
                        response.candidates[0], "finish_reason", None
                    ) if getattr(response, "candidates", None) else None
                    raise GeminiAPIError(
                        f"Bos yanit alindi (finish_reason={finish_reason})"
                    )
                return response_text

            except Exception as e:
                logger.error(
                    f"Gemini API hatasi "
                    f"(deneme {attempt + 1}/{max_retries}): {e}"
                )

                if attempt == max_retries - 1:
                    raise GeminiAPIError(f"API hatasi: {e}")

                await asyncio.sleep(2 ** attempt)

    async def generate_json_response(
        self,
        prompt: str,
        max_retries: Optional[int] = None
    ) -> Dict[str, Any]:
        """JSON formatinda yanit alir

        Args:
            prompt: Gonderilecek prompt
            max_retries: Maksimum deneme sayisi

        Returns:
            Parse edilmis JSON dict
        """
        response_text = await self.generate_with_retry(prompt, max_retries)

        # JSON extract
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                parsed_json = json.loads(json_str)

                # Sonuç manipülasyonu kaldırıldı
                # Sonuçlar olduğu gibi kullanılmalı
                if ("result" in parsed_json and
                        isinstance(parsed_json["result"], (int, float))):
                    parsed_json["result"] = float(parsed_json["result"])

                return parsed_json
            except json.JSONDecodeError:
                logger.warning("JSON parse hatasi, raw text donduruluyor")

        # Fallback: structured response
        fallback_text = (
            response_text or "Gemini yaniti alinmadan islem sonlandi"
        )
        return {
            "result": fallback_text,
            "steps": [fallback_text],
            "confidence_score": 0.95,
        }

"""Structured logging for Calculator Agent"""

import json
import logging
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """JSON formatinda log formatter"""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logger(name: str = "calculator_agent", level: int = logging.INFO) -> logging.Logger:
    """Yapilandirilmis logger olusturur"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Mevcut handler'ları temizle (duplicate handler'ları önlemek için)
    logger.handlers.clear()
    
    handler = logging.StreamHandler()
    handler.setLevel(level)  # Handler level'ı logger level'ı ile aynı olmalı
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    # Root logger'ı etkilememek için propagate'i kapat
    logger.propagate = False
    
    return logger


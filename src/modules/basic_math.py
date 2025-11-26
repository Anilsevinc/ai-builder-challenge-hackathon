"""Basic math module for Calculator Agent"""

import re

from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import BASIC_MATH_PROMPT
from src.utils.logger import setup_logger

logger = setup_logger()


class BasicMathModule(BaseModule):
    """Temel matematik modulu"""
    
    INVALID_EXPRESSION_MESSAGE = "Geçersiz veya yasaklı ifade girdiniz."
    MISSING_OPERAND_MESSAGE = "Hatalı işlem: Eksik operand. Örnek kullanım: !basic 5 + 3"
    ALLOWED_PATTERN = re.compile(r'^[0-9+\-*/\.\s]+$')
    NUMBER_PATTERN = re.compile(r'(?:\d+(?:\.\d+)?|\.\d+)')
    
    def _get_domain_prompt(self) -> str:
        """Basic math prompt'unu dondurur"""
        return BASIC_MATH_PROMPT
    
    async def calculate(
        self,
        expression: str,
        **kwargs
    ) -> CalculationResult:
        """Temel matematik islemi yapar"""
        self.validate_input(expression)
        expression = expression.strip()
        
        validation_error = self._validate_expression(expression)
        if validation_error:
            logger.warning(f"Basic math validation failed: {validation_error}")
            return self._create_result({"error": validation_error}, "basic_math")
        
        logger.info(f"Basic math calculation: {expression}")
        
        try:
            response = await self._call_gemini(expression)
            result = self._create_result(response, "basic_math")
            
            logger.info(f"Calculation successful: {result.result}")
            return result
            
        except Exception as e:
            logger.error(f"Basic math calculation error: {e}")
            raise
    
    def _validate_expression(self, expression: str):
        """Expression-level validation for basic arithmetic."""
        if not expression:
            return self.MISSING_OPERAND_MESSAGE
        
        if not self.ALLOWED_PATTERN.match(expression):
            return self.INVALID_EXPRESSION_MESSAGE
        
        if not self.NUMBER_PATTERN.search(expression):
            return self.MISSING_OPERAND_MESSAGE
        
        compact_expression = "".join(expression.split())
        if self._has_operator_without_operand(compact_expression):
            return self.MISSING_OPERAND_MESSAGE
        
        return None
    
    def _has_operator_without_operand(self, compact_expression: str) -> bool:
        """Checks if an operator lacks a numeric operand on the right side."""
        operators = "+-*/"
        length = len(compact_expression)
        
        for index, char in enumerate(compact_expression):
            if char not in operators:
                continue
            
            # Allow unary minus at the start
            if char == '-' and index == 0 and length > 1:
                continue
            
            remaining = compact_expression[index + 1 :]
            if not remaining:
                return True
            
            if not any(ch.isdigit() for ch in remaining):
                return True
        
        return False

"""Statistics module for Calculator Agent"""

from typing import List, Optional
from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import STATISTICS_PROMPT
from src.utils.logger import setup_logger

logger = setup_logger()


class StatisticsModule(BaseModule):
    """Istatistik modulu (ortalama, medyan, standart sapma, korelasyon, vb.)"""
    
    def _get_domain_prompt(self) -> str:
        """Statistics prompt'unu dondurur"""
        return STATISTICS_PROMPT
    
    async def calculate(
        self,
        expression: str,
        **kwargs
    ) -> CalculationResult:
        """Istatistiksel hesaplama yapar
        
        Args:
            expression: Istatistiksel islem (ornek: "mean [1,2,3,4,5]", 
                       "std dev [10,20,30,40,50]", "correlation [1,2,3] [4,5,6]")
            **kwargs: Ek parametreler
            
        Returns:
            CalculationResult objesi
            
        Ornekler:
            - "mean [1,2,3,4,5]" -> Ortalama hesaplama
            - "median [10,20,30,40,50]" -> Medyan hesaplama
            - "std dev [5,10,15,20,25]" -> Standart sapma
            - "variance [2,4,6,8,10]" -> Varyans
            - "correlation [1,2,3,4,5] [2,4,6,8,10]" -> Korelasyon
            - "z-score 75 mean=70 std=5" -> Z-score
            - "percentile 85 [10,20,30,40,50,60,70,80,90,100]" -> Percentile
        """
        self.validate_input(expression)
        
        logger.info(f"Statistics calculation: {expression}")
        
        try:
            response = await self._call_gemini(expression)
            result = self._create_result(response, "statistics")
            
            logger.info(f"Statistics calculation successful: {result.result}")
            return result
            
        except Exception as e:
            logger.error(f"Statistics calculation error: {e}")
            raise


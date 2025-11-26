"""Main orchestrator and UI entry point for Calculator Agent"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Proje root'unu Python path'ine ekle (src klasöründen çalıştırılabilmesi için)
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from pydantic import ValidationError
from src.core.agent import GeminiAgent
from src.core.parser import CommandParser
from src.core.validator import InputValidator
from src.modules.basic_math import BasicMathModule
from src.modules.calculus import CalculusModule
from src.modules.linear_algebra import LinearAlgebraModule
from src.modules.financial import FinancialModule
from src.modules.equation_solver import EquationSolverModule
from src.modules.graph_plotter import GraphPlotterModule
from src.modules.statistics import StatisticsModule
from src.config.settings import settings
from src.utils.exceptions import (
    CalculationError,
    InvalidInputError,
    SecurityViolationError,
    CalculatorModuleNotFoundError,
)
from src.utils.logger import setup_logger
from src.utils.helpers import format_result_for_display

logger = setup_logger()
APP_NAME = "Calculator Agent"
APP_VERSION = "1.0.0"


class CalculatorAgent:
    """Ana calculator agent orchestrator"""
    
    def __init__(self):
        """Agent'i baslatir"""
        try:
            settings.validate()
        except ValueError as e:
            logger.error(f"Settings validation error: {e}")
            raise
        
        self.gemini_agent = GeminiAgent()
        self.parser = CommandParser()
        self.validator = InputValidator()
        
       
        self.modules = {
            "basic_math": BasicMathModule(self.gemini_agent),
            "calculus": CalculusModule(self.gemini_agent),
            "linear_algebra": LinearAlgebraModule(self.gemini_agent),
            "financial": FinancialModule(self.gemini_agent),
            "equation_solver": EquationSolverModule(self.gemini_agent),
            "graph_plotter": GraphPlotterModule(self.gemini_agent),
            "statistics": StatisticsModule(self.gemini_agent),
        }
        
        logger.info("Calculator Agent baslatildi")  
    
    async def process_command(self, user_input: str) -> Optional[str]:
        """Kullanici komutunu isler
        
        Args:
            user_input: Kullanici girdisi
            
        Returns:
            Sonuc string'i veya None
        """
        if not user_input or not user_input.strip():
            return "Boş komut girdiniz."
        
        try:
        
            module_name, expression = self.parser.parse(user_input)
            self.validator.sanitize_expression(expression)
            
   
            if module_name not in self.modules:
                raise CalculatorModuleNotFoundError(f"Modul bulunamadi: {module_name}")
            
            module = self.modules[module_name]
            

            logger.info(f"Processing: {module_name} - {expression}")
            result = await module.calculate(expression)
            

            return self._format_output(result)
            
        except SecurityViolationError as e:
            logger.warning(f"Security violation: {e}")
            return f"❌ Guvenlik hatasi: {e}"
            
        except InvalidInputError as e:
            logger.warning(f"Invalid input: {e}")
            return f"❌ Gecersiz giris: {e}"
        
        except ValidationError as e:
            logger.warning(f"Pydantic validation error: {e}")
            return "Girdi işlenemedi. Lütfen formatı kontrol edin."
            
        except CalculatorModuleNotFoundError as e:
            logger.warning(f"Module not found: {e}")
            return f"❌ Modul bulunamadi: {e}"
            
        except CalculationError as e:
            logger.error(f"Calculation error: {e}")
            return f"❌ Hesaplama hatasi: {e}"
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return f"❌ Beklenmeyen hata: {e}"
    
    def _format_output(self, result) -> str:
        """Sonucu kullanici dostu formatta gosterir
        
        Args:
            result: CalculationResult objesi
            
        Returns:
            Formatlanmis string
        """
        if getattr(result, "error", None):
            return str(result.error)
        
        output_lines = []
        
        # Sonuc
        output_lines.append(f"✅ Sonuc: {format_result_for_display(result.result)}")
        
        if result.steps:
            output_lines.append("\n📝 Adimlar:")
            for i, step in enumerate(result.steps, 1):
                output_lines.append(f"  {i}. {step}")


        if result.confidence_score < 1.0:
            output_lines.append(
                f"\n⚠️  Guven Skoru: {result.confidence_score:.2f}"
            )
        
        # Gorsellestirme
        if result.visual_data and "plot_paths" in result.visual_data:
            plot_paths = result.visual_data["plot_paths"]
            if "png" in plot_paths:
                output_lines.append(f"\n📊 Grafik: {plot_paths['png']}")
        
        return "\n".join(output_lines)


async def interactive_mode():
    """Interaktif mod"""
    agent = CalculatorAgent()
    
    print("=" * 60)
    print(f"🧮 Calculator Agent - AI Builder Challenge")
    print("=" * 60)
    print(f"Version: {APP_VERSION}")
    print("\nKullanilabilir komutlar:")
    print("  - !calculus <ifade>  : Kalkulus islemleri")
    print("  - !linalg <ifade>    : Lineer cebir")
    print("  - !solve <ifade>     : Denklem cozme")
    print("  - !plot <ifade>      : Grafik cizme")
    print("  - !finance <ifade>   : Finansal hesaplamalar")
    print("  - <ifade>            : Temel matematik")
    print("  - !statistics <ifade> : Istatistik islemleri")
    print("\nCikis icin 'quit' veya 'exit' yazin\n")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Gule gule!")
                break
            
            if not user_input:
                continue
            
            result = await agent.process_command(user_input)
            if result:
                print(result)
                print()  
            
        except KeyboardInterrupt:
            print("\n\nGule gule!")
            break
        except EOFError:
            print("\n\nGule gule!")
            break


async def single_command_mode(expression: str):
    """Tek komut modu"""
    agent = CalculatorAgent()
    result = await agent.process_command(expression)
    if result:
        print(result)


def main():
    """Ana entry point"""
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        asyncio.run(single_command_mode(expression))
    else:
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()


"""Pydantic models for input/output validation"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


Matrix = List[List[float]]


class CalculationResult(BaseModel):
    """Hesaplama sonucu modeli"""

    result: Union[float, List[float], Matrix, Dict[str, Any], str] = Field(
        ..., description="Hesaplama sonucu"
    )
    steps: List[str] = Field(
        default_factory=list, description="Adim adim cozum adimlari"
    )
    visual_data: Optional[Dict[str, Any]] = Field(
        None, description="Gorsellestirme icin veri"
    )
    confidence_score: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Sonuc guven skoru"
    )
    domain: str = Field(
        ..., description="Hesaplama domain'i (calculus, linalg, vb.)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Ek metadata bilgileri"
    )
    error: Optional[str] = Field(
        None, description="Hata mesaji"
    )
    module: Optional[str] = Field(
        None, description="Sonucu ureten modul"
    )


class CalculationRequest(BaseModel):
    """Hesaplama istegi modeli"""

    expression: str = Field(..., description="Hesaplanacak ifade")
    module: Optional[str] = Field(None, description="Kullanilacak modul")
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Ek parametreler"
    )

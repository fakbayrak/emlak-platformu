"""Ortak enum ve yardımcı tipler."""
from enum import Enum


class ListingType(str, Enum):
    SALE = "sale"
    RENT = "rent"


class DealLabel(str, Enum):
    BARGAIN = "firsat"       # Fırsat (gerçek < tahmin * 0.9)
    FAIR = "uygun"           # Uygun (tahmin ± %10)
    EXPENSIVE = "pahali"     # Pahalı (gerçek > tahmin * 1.1)

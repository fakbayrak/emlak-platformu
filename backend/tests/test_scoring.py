"""Yatırım skoru mantığı testleri (ML tarafındaki fonksiyonları ileride import eder)."""


def test_deal_threshold_bargain():
    """Tahmin 1.000.000, istenen 850.000 → fırsat."""
    from app.schemas.common import DealLabel
    predicted, asking = 1_000_000, 850_000
    deviation = (asking - predicted) / predicted
    label = DealLabel.BARGAIN if deviation <= -0.10 else DealLabel.FAIR
    assert label == DealLabel.BARGAIN


def test_deal_threshold_fair():
    predicted, asking = 1_000_000, 970_000
    deviation = (asking - predicted) / predicted
    assert -0.10 < deviation < 0.10

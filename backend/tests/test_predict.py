"""Tahmin uç noktası testleri."""


def _sample_features():
    return {
        "city": "İstanbul",
        "district": "Kadıköy",
        "neighborhood": "Caddebostan",
        "m2": 120,
        "room_count": "3+1",
        "building_age": 10,
        "floor": 3,
        "heating_type": "kombi",
        "furnished": False,
        "has_elevator": True,
        "has_parking": False,
    }


def test_predict_sale_schema(client):
    r = client.post("/predict/sale", json=_sample_features())
    # Model dosyası yoksa bile dummy yanıt 200 döner
    assert r.status_code == 200
    body = r.json()
    assert "predicted_price_nominal" in body
    assert "predicted_price_real" in body
    assert "top_shap_features" in body
    assert body["predicted_price_nominal"] > 0


def test_predict_sale_validates_m2(client):
    payload = _sample_features()
    payload["m2"] = -10
    r = client.post("/predict/sale", json=payload)
    assert r.status_code == 422

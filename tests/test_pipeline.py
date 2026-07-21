import pandas as pd

from src.pipeline import clean_customers, normalize_name, normalize_phone, parse_currency


def test_normalizers() -> None:
    assert normalize_name("  ANA  LIMA ") == "Ana Lima"
    assert normalize_phone("+55 (98) 98888-7777") == "98988887777"
    assert parse_currency("R$ 1.234,56") == 1234.56


def test_clean_customers_keeps_latest_duplicate() -> None:
    data = pd.DataFrame([
        {"cliente_id": "CLI-1", "nome": "ana lima", "email": "ana@gmail.com", "telefone": "98988887777", "estado": "ma", "data_cadastro": "01/01/2025", "valor_acumulado": "100,00", "atualizado_em": "2025-01-02"},
        {"cliente_id": "CLI-1", "nome": "Ana Lima", "email": "novo@gmail.com", "telefone": "+55 98988887777", "estado": "Maranhao", "data_cadastro": "2025-01-01", "valor_acumulado": "R$ 200,00", "atualizado_em": "2025-02-02"},
    ])
    result = clean_customers(data)
    assert len(result) == 1
    assert result.loc[0, "email"] == "novo@gmail.com"
    assert result.loc[0, "estado"] == "MA"
    assert result.loc[0, "valor_acumulado"] == 200.0


def test_invalid_email_is_flagged() -> None:
    data = pd.DataFrame([{ "cliente_id": "CLI-1", "nome": "Ana", "email": "sem-arroba", "telefone": "98988887777", "estado": "MA", "data_cadastro": "2025-01-01", "valor_acumulado": "10.00", "atualizado_em": "2025-01-02" }])
    assert pd.isna(clean_customers(data).loc[0, "email"])


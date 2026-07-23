"""Pipeline ETL para padronizar e validar cadastros de clientes."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
STATE_MAP = {"MARANHAO": "MA", "MA": "MA", "SP": "SP", "RJ": "RJ", "PA": "PA"}
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_ascii(value: object) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    return "".join(char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char))


def normalize_name(value: object) -> str:
    return " ".join(normalize_ascii(value).split()).title()


def normalize_phone(value: object) -> str | None:
    digits = re.sub(r"\D", "", "" if pd.isna(value) else str(value))
    if digits.startswith("55") and len(digits) == 13:
        digits = digits[2:]
    return digits if len(digits) == 11 else None


def parse_currency(value: object) -> float | None:
    text = "" if pd.isna(value) else str(value).strip().replace("R$", "").replace(" ", "")
    if not text:
        return None
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    try:
        return round(float(text), 2)
    except ValueError:
        return None


def profile_quality(df: pd.DataFrame) -> dict[str, int]:
    emails = df["email"].fillna("").astype(str).str.strip().str.lower()
    phones = df["telefone"].apply(normalize_phone)
    states = df["estado"].fillna("").astype(str).str.strip().str.upper().map(STATE_MAP)
    values = df["valor_acumulado"].apply(parse_currency)
    return {
        "linhas": int(len(df)),
        "ids_duplicados": int(df["cliente_id"].duplicated(keep=False).sum()),
        "emails_invalidos": int((~emails.str.match(EMAIL_PATTERN)).sum()),
        "telefones_invalidos": int(phones.isna().sum()),
        "estados_invalidos": int(states.isna().sum()),
        "valores_invalidos": int(values.isna().sum()),
    }


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["nome"] = cleaned["nome"].apply(normalize_name)
    cleaned["email"] = cleaned["email"].fillna("").astype(str).str.strip().str.lower()
    cleaned.loc[~cleaned["email"].str.match(EMAIL_PATTERN), "email"] = pd.NA
    cleaned["telefone"] = cleaned["telefone"].apply(normalize_phone)
    cleaned["estado"] = (
        cleaned["estado"].fillna("").astype(str).str.strip().str.upper().apply(normalize_ascii).map(STATE_MAP)
    )
    cleaned["data_cadastro"] = pd.to_datetime(cleaned["data_cadastro"], format="mixed", dayfirst=True, errors="coerce")
    cleaned["valor_acumulado"] = cleaned["valor_acumulado"].apply(parse_currency)
    cleaned["atualizado_em"] = pd.to_datetime(cleaned["atualizado_em"], errors="coerce")
    cleaned = cleaned.sort_values("atualizado_em").drop_duplicates("cliente_id", keep="last")
    cleaned["cadastro_valido"] = cleaned[["nome", "email", "telefone", "estado", "data_cadastro", "valor_acumulado"]].notna().all(axis=1)
    return cleaned.sort_values("cliente_id").reset_index(drop=True)


def run_pipeline() -> dict[str, dict[str, int]]:
    raw_path = ROOT / "data" / "raw" / "clientes_sujos.csv"
    output_dir = ROOT / "outputs"
    processed_dir = ROOT / "data" / "processed"
    output_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(raw_path, dtype=str)
    before = profile_quality(raw)
    clean = clean_customers(raw)
    after = {
        "linhas": int(len(clean)),
        "ids_duplicados": int(clean["cliente_id"].duplicated(keep=False).sum()),
        "emails_invalidos": int(clean["email"].isna().sum()),
        "telefones_invalidos": int(clean["telefone"].isna().sum()),
        "estados_invalidos": int(clean["estado"].isna().sum()),
        "valores_invalidos": int(clean["valor_acumulado"].isna().sum()),
    }
    report = {"antes": before, "depois": after, "linhas_removidas_por_duplicidade": before["linhas"] - after["linhas"]}
    clean.to_csv(processed_dir / "clientes_tratados.csv", index=False, date_format="%Y-%m-%d")
    (output_dir / "relatorio_qualidade.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    indicators = ["ids_duplicados", "emails_invalidos", "telefones_invalidos", "estados_invalidos", "valores_invalidos"]
    labels = ["IDs duplicados", "E-mails", "Telefones", "Estados", "Valores"]
    x = range(len(indicators))
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar([i - 0.2 for i in x], [before[key] for key in indicators], width=0.4, label="Antes", color="#ef4444")
    ax.bar([i + 0.2 for i in x], [after[key] for key in indicators], width=0.4, label="Depois", color="#10b981")
    ax.set_title("Qualidade dos cadastros antes e depois do ETL", fontsize=15, fontweight="bold")
    ax.set_xticks(list(x), labels, rotation=12)
    ax.set_ylabel("Quantidade de registros")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "qualidade_antes_depois.svg", bbox_inches="tight")
    plt.close(fig)
    return report


if __name__ == "__main__":
    print(json.dumps(run_pipeline(), indent=2, ensure_ascii=False))

"""Gera dados de clientes com problemas intencionais de qualidade."""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "data" / "raw" / "clientes_sujos.csv"
NAMES = ["Ana Lima", "Bruno Costa", "Carla Souza", "Diego Alves", "Elisa Rocha", "Fabio Santos", "Gabi Melo"]
STATES = ["MA", "ma", "Maranhao", "SP", "sp", "RJ", "rj", "PA", "pa", ""]
DOMAINS = ["gmail.com", "outlook.com", "empresa.com.br"]


def generate_customers(rows: int = 900, seed: int = 17) -> None:
    random.seed(seed)
    records = []
    for index in range(1, rows + 1):
        customer_id = random.randint(1, 720)
        name = random.choice(NAMES)
        if random.random() < 0.18:
            name = f"  {name.upper()}  "
        email = f"{name.lower().replace(' ', '.').strip()}{customer_id}@{random.choice(DOMAINS)}"
        if random.random() < 0.09:
            email = email.replace("@", "")
        phone_digits = f"98{random.randint(900000000, 999999999)}"
        phone = random.choice([phone_digits, f"({phone_digits[:2]}) {phone_digits[2:7]}-{phone_digits[7:]}", f"+55 {phone_digits}"])
        if random.random() < 0.05:
            phone = ""
        registration = date(2023, 1, 1) + timedelta(days=random.randint(0, 1095))
        value = random.uniform(45, 2600)
        formatted_value = random.choice([f"{value:.2f}", f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")])
        records.append({
            "cliente_id": f"CLI-{customer_id:04d}",
            "nome": name,
            "email": email,
            "telefone": phone,
            "estado": random.choice(STATES),
            "data_cadastro": registration.strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y"])),
            "valor_acumulado": formatted_value,
            "atualizado_em": (registration + timedelta(days=random.randint(0, 180))).isoformat(),
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Base criada: {OUTPUT} ({len(records)} linhas)")


if __name__ == "__main__":
    generate_customers()


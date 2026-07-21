# Pipeline ETL de Qualidade de Dados

Projeto de engenharia de dados que identifica e corrige problemas comuns em cadastros de clientes: duplicidades, textos inconsistentes, e-mails invalidos, telefones fora do padrao, datas em formatos diferentes e valores monetarios brasileiros.

![Comparacao da qualidade](outputs/qualidade_antes_depois.svg)

## Fluxo

```text
CSV bruto -> perfil de qualidade -> padronizacao -> validacao -> deduplicacao -> CSV tratado + relatorio
```

## Tecnologias

`Python` · `Pandas` · `Regex` · `ETL` · `SQL` · `Matplotlib` · `Pytest`

## Resultado da execucao

- 900 linhas brutas analisadas;
- 669 ocorrencias em IDs duplicados identificadas;
- 400 versoes antigas removidas pela regra de deduplicacao;
- IDs duplicados reduzidos a zero;
- registros invalidos preservados como nulos e sinalizados para revisao.

## Entregaveis

- base suja, ficticia e reproduzivel;
- pipeline modular em `src/pipeline.py`;
- base limpa em `data/processed/clientes_tratados.csv`;
- relatorio antes/depois em JSON;
- grafico de qualidade para comunicacao do resultado;
- consultas SQL para auditoria;
- testes automatizados das regras principais.

## Como executar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python generate_data.py
python src/pipeline.py
pytest -q
```

As regras de tratamento estao documentadas em [`docs/regras_de_qualidade.md`](docs/regras_de_qualidade.md).

> Os dados sao inteiramente ficticios. Valores invalidos nao sao inventados: eles sao sinalizados para revisao, preservando a rastreabilidade do processo.

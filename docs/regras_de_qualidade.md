# Regras de qualidade

| Campo | Regra aplicada |
|---|---|
| `cliente_id` | Mantem apenas a versao mais recente de cada identificador |
| `nome` | Remove espacos extras, acentos e padroniza maiusculas/minusculas |
| `email` | Converte para minusculas e valida o formato basico |
| `telefone` | Mantem 11 digitos, removendo `+55` e pontuacao |
| `estado` | Converte variacoes conhecidas para a sigla da UF |
| `data_cadastro` | Aceita formatos ISO e brasileiro e converte para data |
| `valor_acumulado` | Converte formatos brasileiro e decimal para numero |

Registros com campos essenciais invalidos nao sao inventados nem apagados: recebem valor nulo e `cadastro_valido = False`, permitindo revisao posterior.


-- Duplicidades por identificador
SELECT cliente_id, COUNT(*) AS ocorrencias
FROM clientes_raw
GROUP BY cliente_id
HAVING COUNT(*) > 1;

-- Campos obrigatorios ausentes apos o tratamento
SELECT
    SUM(email IS NULL) AS emails_ausentes,
    SUM(telefone IS NULL) AS telefones_ausentes,
    SUM(estado IS NULL) AS estados_ausentes,
    SUM(valor_acumulado IS NULL) AS valores_ausentes
FROM clientes_tratados;

-- Taxa de cadastros validos
SELECT
    ROUND(100 * SUM(cadastro_valido = 1) / COUNT(*), 2) AS taxa_validade_pct
FROM clientes_tratados;


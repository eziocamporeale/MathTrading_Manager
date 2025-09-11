-- Script per risolvere errore foreign key constraint
-- Prima crea un broker di default, poi inserisce i dati gruppi PAMM
-- Creato da Ezio Camporeale

-- 1. Verifica se esistono broker
SELECT COUNT(*) as broker_count FROM brokers;

-- 2. Se non ci sono broker, crea un broker di default
INSERT INTO brokers (
    nome_broker, tipo_broker, regolamentazione, paese, sito_web,
    spread_minimo, commissioni, leverage_massimo, deposito_minimo,
    valute_supportate, piattaforme, stato, note,
    creato_da, aggiornato_da
) VALUES (
    'Broker Default', 'ECN', 'FCA', 'UK', 'https://default-broker.com',
    0.5, 0.0, 500, 100.0,
    'EUR,USD,GBP', 'MT4,MT5', 'Attivo', 'Broker di default per test',
    'admin', 'admin'
) ON CONFLICT (nome_broker) DO NOTHING;

-- 3. Ottieni l'ID del broker di default (o il primo disponibile)
WITH broker_id AS (
    SELECT id FROM brokers ORDER BY id LIMIT 1
)
-- 4. Inserisci dati gruppi PAMM usando l'ID broker esistente
INSERT INTO gruppi_pamm (
    nome_gruppo, manager, broker_id, account_pamm, capitale_totale, numero_partecipanti,
    nome_cliente, importo_cliente, stato_prop, deposito_pamm, quota_prop, ciclo_numero,
    responsabili_gruppo, numero_membri_gruppo, commissioni_percentuale,
    creato_da, aggiornato_da
) 
SELECT 
    'Gruppo 1', 'frank andre', broker_id.id, 'PAMM001', 12000.0, 1, 
    'MANUEL CARINI [4000]', 4000.0, 'mancanza saldo', '', 1, 1, 
    'frank andre', 12000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 1', 'frank andre', broker_id.id, 'PAMM001', 12000.0, 1, 
    'MIRKO CARINI [8000]', 8000.0, 'mancanza saldo', '', 1, 1, 
    'frank andre', 12000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 2', 'mario', broker_id.id, 'PAMM002', 10000.0, 4, 
    'LUIGI GUGLIELMELLI (2404)', 2404.0, 'Svolto', 'Depositata', 1, 1, 
    'mario', 10000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 2', 'mario', broker_id.id, 'PAMM002', 10000.0, 4, 
    'VITO ZONNO [801]', 801.0, 'Svolto', 'Depositata', 1, 1, 
    'mario', 10000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 2', 'mario', broker_id.id, 'PAMM002', 10000.0, 4, 
    'VINCENZO VOZZA [972]', 972.0, 'Svolto', 'Depositata', 1, 1, 
    'mario', 10000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 2', 'mario', broker_id.id, 'PAMM002', 10000.0, 4, 
    'MARIO MAZZA 2 [2000]', 2000.0, 'Svolto', '', 1, 1, 
    'mario', 10000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 3', 'fede trott|mario', broker_id.id, 'PAMM003', 7000.0, 5, 
    'MIRKO MINATI RIZZI [1876]', 1876.0, 'Svolto', 'Depositata', 1, 1, 
    'fede trott|mario', 7000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 3', 'fede trott|mario', broker_id.id, 'PAMM003', 7000.0, 5, 
    'SILVIA SAMMARTANO [1887]', 1887.0, 'Svolto', 'Depositata', 1, 1, 
    'fede trott|mario', 7000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 3', 'fede trott|mario', broker_id.id, 'PAMM003', 7000.0, 5, 
    'PIERA ANDRANI [1000]', 1000.0, 'Non svolto', '', 1, 1, 
    'fede trott|mario', 7000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 3', 'fede trott|mario', broker_id.id, 'PAMM003', 7000.0, 5, 
    'PAOLA PIRAS [1000]', 1000.0, 'Non svolto', '', 1, 1, 
    'fede trott|mario', 7000, 25.0, 'admin', 'admin'
FROM broker_id
UNION ALL
SELECT 
    'Gruppo 3', 'fede trott|mario', broker_id.id, 'PAMM003', 7000.0, 5, 
    'MAURIZIO PETRACHI [1000]', 1000.0, 'Non svolto', '', 1, 1, 
    'fede trott|mario', 7000, 25.0, 'admin', 'admin'
FROM broker_id
ON CONFLICT (id) DO NOTHING;

-- 5. Verifica i risultati
SELECT 
    'Brokers' as tabella, COUNT(*) as count FROM brokers
UNION ALL
SELECT 
    'Gruppi PAMM' as tabella, COUNT(*) as count FROM gruppi_pamm;

-- 6. Mostra i dati inseriti
SELECT 
    nome_gruppo,
    nome_cliente,
    stato_prop,
    deposito_pamm,
    broker_id
FROM gruppi_pamm 
ORDER BY nome_gruppo, nome_cliente;

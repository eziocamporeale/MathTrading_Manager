-- Script semplice per risolvere errore foreign key
-- Creato da Ezio Camporeale

-- 1. Controlla se esistono broker
DO $$
DECLARE
    broker_count INTEGER;
    broker_id INTEGER;
BEGIN
    -- Conta broker esistenti
    SELECT COUNT(*) INTO broker_count FROM brokers;
    
    IF broker_count = 0 THEN
        -- Crea broker di default se non esistono
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
        );
        
        RAISE NOTICE 'Broker di default creato';
    END IF;
    
    -- Ottieni l'ID del primo broker disponibile
    SELECT id INTO broker_id FROM brokers ORDER BY id LIMIT 1;
    
    RAISE NOTICE 'Usando broker_id: %', broker_id;
    
    -- Inserisci dati gruppi PAMM usando l'ID broker esistente
    INSERT INTO gruppi_pamm (
        nome_gruppo, manager, broker_id, account_pamm, capitale_totale, numero_partecipanti,
        nome_cliente, importo_cliente, stato_prop, deposito_pamm, quota_prop, ciclo_numero,
        responsabili_gruppo, numero_membri_gruppo, commissioni_percentuale,
        creato_da, aggiornato_da
    ) VALUES 
    -- Gruppo 1: 12k membri (frank andre)
    ('Gruppo 1', 'frank andre', broker_id, 'PAMM001', 12000.0, 1, 'MANUEL CARINI [4000]', 4000.0, 'mancanza saldo', '', 1, 1, 'frank andre', 12000, 25.0, 'admin', 'admin'),
    ('Gruppo 1', 'frank andre', broker_id, 'PAMM001', 12000.0, 1, 'MIRKO CARINI [8000]', 8000.0, 'mancanza saldo', '', 1, 1, 'frank andre', 12000, 25.0, 'admin', 'admin'),
    
    -- Gruppo 2: 10k membri (mario)
    ('Gruppo 2', 'mario', broker_id, 'PAMM002', 10000.0, 4, 'LUIGI GUGLIELMELLI (2404)', 2404.0, 'Svolto', 'Depositata', 1, 1, 'mario', 10000, 25.0, 'admin', 'admin'),
    ('Gruppo 2', 'mario', broker_id, 'PAMM002', 10000.0, 4, 'VITO ZONNO [801]', 801.0, 'Svolto', 'Depositata', 1, 1, 'mario', 10000, 25.0, 'admin', 'admin'),
    ('Gruppo 2', 'mario', broker_id, 'PAMM002', 10000.0, 4, 'VINCENZO VOZZA [972]', 972.0, 'Svolto', 'Depositata', 1, 1, 'mario', 10000, 25.0, 'admin', 'admin'),
    ('Gruppo 2', 'mario', broker_id, 'PAMM002', 10000.0, 4, 'MARIO MAZZA 2 [2000]', 2000.0, 'Svolto', '', 1, 1, 'mario', 10000, 25.0, 'admin', 'admin'),
    
    -- Gruppo 3: 7k membri (fede trott|mario)
    ('Gruppo 3', 'fede trott|mario', broker_id, 'PAMM003', 7000.0, 5, 'MIRKO MINATI RIZZI [1876]', 1876.0, 'Svolto', 'Depositata', 1, 1, 'fede trott|mario', 7000, 25.0, 'admin', 'admin'),
    ('Gruppo 3', 'fede trott|mario', broker_id, 'PAMM003', 7000.0, 5, 'SILVIA SAMMARTANO [1887]', 1887.0, 'Svolto', 'Depositata', 1, 1, 'fede trott|mario', 7000, 25.0, 'admin', 'admin'),
    ('Gruppo 3', 'fede trott|mario', broker_id, 'PAMM003', 7000.0, 5, 'PIERA ANDRANI [1000]', 1000.0, 'Non svolto', '', 1, 1, 'fede trott|mario', 7000, 25.0, 'admin', 'admin'),
    ('Gruppo 3', 'fede trott|mario', broker_id, 'PAMM003', 7000.0, 5, 'PAOLA PIRAS [1000]', 1000.0, 'Non svolto', '', 1, 1, 'fede trott|mario', 7000, 25.0, 'admin', 'admin'),
    ('Gruppo 3', 'fede trott|mario', broker_id, 'PAMM003', 7000.0, 5, 'MAURIZIO PETRACHI [1000]', 1000.0, 'Non svolto', '', 1, 1, 'fede trott|mario', 7000, 25.0, 'admin', 'admin')
    
    ON CONFLICT (id) DO NOTHING;
    
    RAISE NOTICE 'Dati gruppi PAMM inseriti con successo';
END $$;

-- Verifica i risultati
SELECT 
    'Brokers' as tabella, COUNT(*) as count FROM brokers
UNION ALL
SELECT 
    'Gruppi PAMM' as tabella, COUNT(*) as count FROM gruppi_pamm;

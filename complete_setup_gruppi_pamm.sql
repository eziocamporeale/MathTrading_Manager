-- Script completo per setup Gruppi PAMM estesi
-- Esegue prima l'estensione della tabella, poi inserisce i dati
-- Creato da Ezio Camporeale

-- ========================================
-- STEP 1: ESTENDI TABELLA GRUPPI_PAMM
-- ========================================

-- Aggiungere nuove colonne alla tabella gruppi_pamm
ALTER TABLE gruppi_pamm 
ADD COLUMN IF NOT EXISTS nome_cliente TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS importo_cliente DECIMAL(15,2) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS stato_prop TEXT DEFAULT 'Non svolto' CHECK (stato_prop IN ('Svolto', 'Non svolto', 'mancanza saldo')),
ADD COLUMN IF NOT EXISTS deposito_pamm TEXT DEFAULT '' CHECK (deposito_pamm IN ('Depositata', '')),
ADD COLUMN IF NOT EXISTS quota_prop INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS ciclo_numero INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS fase_prop TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS operazione_numero INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS esito_broker TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS esito_prop TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS prelievo_prop DECIMAL(15,2) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS prelievo_profit DECIMAL(15,2) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS commissioni_percentuale DECIMAL(5,2) DEFAULT 25.0,
ADD COLUMN IF NOT EXISTS credenziali_broker TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS credenziali_prop TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS responsabili_gruppo TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS numero_membri_gruppo INTEGER DEFAULT 0;

-- Creare indici per migliorare le performance delle query
CREATE INDEX IF NOT EXISTS idx_gruppi_pamm_stato_prop ON gruppi_pamm(stato_prop);
CREATE INDEX IF NOT EXISTS idx_gruppi_pamm_deposito_pamm ON gruppi_pamm(deposito_pamm);
CREATE INDEX IF NOT EXISTS idx_gruppi_pamm_ciclo_numero ON gruppi_pamm(ciclo_numero);
CREATE INDEX IF NOT EXISTS idx_gruppi_pamm_nome_cliente ON gruppi_pamm(nome_cliente);
CREATE INDEX IF NOT EXISTS idx_gruppi_pamm_responsabili_gruppo ON gruppi_pamm(responsabili_gruppo);

-- Aggiornare commenti per documentare le nuove colonne
COMMENT ON COLUMN gruppi_pamm.nome_cliente IS 'Nome completo cliente (es. "MANUEL CARINI [4000]")';
COMMENT ON COLUMN gruppi_pamm.importo_cliente IS 'Importo cliente tra parentesi quadre';
COMMENT ON COLUMN gruppi_pamm.stato_prop IS 'Stato prop firm: Svolto, Non svolto, mancanza saldo';
COMMENT ON COLUMN gruppi_pamm.deposito_pamm IS 'Stato deposito PAMM: Depositata o vuoto';
COMMENT ON COLUMN gruppi_pamm.quota_prop IS 'Quota prop firm (sempre 1 nell''Excel)';
COMMENT ON COLUMN gruppi_pamm.ciclo_numero IS 'Numero ciclo progressivo';
COMMENT ON COLUMN gruppi_pamm.fase_prop IS 'Fase prop firm';
COMMENT ON COLUMN gruppi_pamm.operazione_numero IS 'Numero operazione';
COMMENT ON COLUMN gruppi_pamm.esito_broker IS 'Esito broker';
COMMENT ON COLUMN gruppi_pamm.esito_prop IS 'Esito prop firm';
COMMENT ON COLUMN gruppi_pamm.prelievo_prop IS 'Importo prelievo prop';
COMMENT ON COLUMN gruppi_pamm.prelievo_profit IS 'Importo prelievo profit';
COMMENT ON COLUMN gruppi_pamm.commissioni_percentuale IS 'Commissioni percentuale (default 25%)';
COMMENT ON COLUMN gruppi_pamm.credenziali_broker IS 'Credenziali broker (da crittografare)';
COMMENT ON COLUMN gruppi_pamm.credenziali_prop IS 'Credenziali prop firm (da crittografare)';
COMMENT ON COLUMN gruppi_pamm.responsabili_gruppo IS 'Responsabili gruppo identificati';
COMMENT ON COLUMN gruppi_pamm.numero_membri_gruppo IS 'Numero membri gruppo';

-- Verifica struttura tabella aggiornata
SELECT 'STEP 1 COMPLETATO: Colonne aggiunte alla tabella gruppi_pamm' as status;

-- ========================================
-- STEP 2: INSERISCI DATI CON BROKER
-- ========================================

-- Controlla se esistono broker e inserisci dati
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

-- ========================================
-- STEP 3: VERIFICA RISULTATI
-- ========================================

-- Verifica i risultati finali
SELECT 
    'Brokers' as tabella, COUNT(*) as count FROM brokers
UNION ALL
SELECT 
    'Gruppi PAMM' as tabella, COUNT(*) as count FROM gruppi_pamm;

-- Mostra struttura tabella aggiornata
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'gruppi_pamm' 
ORDER BY ordinal_position;

-- Mostra alcuni dati di esempio
SELECT 
    nome_gruppo,
    nome_cliente,
    stato_prop,
    deposito_pamm,
    broker_id
FROM gruppi_pamm 
ORDER BY nome_gruppo, nome_cliente
LIMIT 5;

SELECT 'SETUP COMPLETATO CON SUCCESSO!' as status;

-- Script per creare le tabelle per la gestione completa dei gruppi PAMM
-- Creato da Ezio Camporeale

-- 1. Tabella per i gruppi PAMM (entità principali)
CREATE TABLE IF NOT EXISTS gruppi_pamm_gruppi (
    id SERIAL PRIMARY KEY,
    nome_gruppo VARCHAR(255) NOT NULL,
    manager VARCHAR(255) NOT NULL,
    broker_id INTEGER NOT NULL REFERENCES brokers(id),
    account_pamm VARCHAR(100) NOT NULL,
    capitale_totale DECIMAL(15,2) DEFAULT 0.0,
    numero_membri_gruppo INTEGER DEFAULT 0,
    responsabili_gruppo TEXT,
    stato VARCHAR(50) DEFAULT 'ATTIVO',
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(100),
    aggiornato_da VARCHAR(100),
    
    -- Vincoli per performance
    UNIQUE(nome_gruppo, broker_id)
);

-- 2. Tabella per i clienti dei gruppi PAMM
CREATE TABLE IF NOT EXISTS clienti_gruppi_pamm (
    id SERIAL PRIMARY KEY,
    gruppo_pamm_id INTEGER NOT NULL REFERENCES gruppi_pamm_gruppi(id) ON DELETE CASCADE,
    nome_cliente VARCHAR(255) NOT NULL,
    importo_cliente DECIMAL(15,2) DEFAULT 0.0,
    stato_prop VARCHAR(50) DEFAULT 'Non svolto',
    deposito_pamm VARCHAR(50) DEFAULT '',
    quota_prop INTEGER DEFAULT 1,
    ciclo_numero INTEGER DEFAULT 0,
    fase_prop VARCHAR(100),
    operazione_numero VARCHAR(100),
    esito_broker VARCHAR(255),
    esito_prop VARCHAR(255),
    prelievo_prop DECIMAL(15,2) DEFAULT 0.0,
    prelievo_profit DECIMAL(15,2) DEFAULT 0.0,
    commissioni_percentuale DECIMAL(5,2) DEFAULT 25.0,
    credenziali_broker TEXT,
    credenziali_prop TEXT,
    chi_ha_comprato_prop VARCHAR(255),
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(100),
    aggiornato_da VARCHAR(100),
    
    -- Vincoli per performance
    UNIQUE(gruppo_pamm_id, nome_cliente)
);

-- 3. Crea indici per performance
CREATE INDEX IF NOT EXISTS idx_gruppi_manager ON gruppi_pamm_gruppi(manager);
CREATE INDEX IF NOT EXISTS idx_gruppi_stato ON gruppi_pamm_gruppi(stato);
CREATE INDEX IF NOT EXISTS idx_clienti_gruppo ON clienti_gruppi_pamm(gruppo_pamm_id);
CREATE INDEX IF NOT EXISTS idx_clienti_stato_prop ON clienti_gruppi_pamm(stato_prop);
CREATE INDEX IF NOT EXISTS idx_clienti_deposito ON clienti_gruppi_pamm(deposito_pamm);
CREATE INDEX IF NOT EXISTS idx_clienti_nome ON clienti_gruppi_pamm(nome_cliente);

-- 4. Crea broker di default se non esiste
INSERT INTO brokers (id, nome, url, api_key, note, creato_da, aggiornato_da)
VALUES (1, 'Broker Default', 'https://default-broker.com', 'default-api-key', 'Broker di default per i test', 'admin', 'admin')
ON CONFLICT (id) DO NOTHING;

-- 5. Inserisci alcuni gruppi di esempio
INSERT INTO gruppi_pamm_gruppi (
    nome_gruppo, manager, broker_id, account_pamm, 
    capitale_totale, numero_membri_gruppo, responsabili_gruppo, 
    creato_da, aggiornato_da
) VALUES 
('Gruppo 1', 'frank andre', 1, 'PAMM001', 12000.0, 12000, 'frank andre', 'admin', 'admin'),
('Gruppo 2', 'mario', 1, 'PAMM002', 10000.0, 10000, 'mario', 'admin', 'admin'),
('Gruppo 3', 'fede trott|mario', 1, 'PAMM003', 7000.0, 7000, 'fede trott|mario', 'admin', 'admin')
ON CONFLICT (nome_gruppo, broker_id) DO NOTHING;

-- 6. Inserisci alcuni clienti di esempio
INSERT INTO clienti_gruppi_pamm (
    gruppo_pamm_id, nome_cliente, importo_cliente, stato_prop, deposito_pamm,
    quota_prop, ciclo_numero, fase_prop, operazione_numero,
    esito_broker, esito_prop, prelievo_prop, prelievo_profit,
    commissioni_percentuale, credenziali_broker, credenziali_prop, chi_ha_comprato_prop,
    creato_da, aggiornato_da
) VALUES 
-- Gruppo 1 clienti
(1, 'MANUEL CARINI [4000]', 4000.0, 'mancanza saldo', '', 1, 1, '', '', '', '', 0.0, 0.0, 25.0, '', '', 'FRANK', 'admin', 'admin'),
(1, 'MIRKO CARINI [8000]', 8000.0, 'mancanza saldo', '', 1, 1, '', '', '', '', 0.0, 0.0, 25.0, '', '', 'FRANK', 'admin', 'admin'),

-- Gruppo 2 clienti
(2, 'LUIGI GUGLIELMELLI (2404)', 2404.0, 'Svolto', 'Depositata', 1, 1, '1 fase', 'Prima operazione', 'OK', 'OK', 1000.0, 500.0, 25.0, '6001855', '1125804', 'MARIO', 'admin', 'admin'),
(2, 'VITO ZONNO [801]', 801.0, 'Svolto', 'Depositata', 1, 1, '1 fase', 'Prima operazione', 'OK', 'OK', 200.0, 100.0, 25.0, '6001856', '1125805', 'MARIO', 'admin', 'admin'),
(2, 'VINCENZO VOZZA [972]', 972.0, 'Svolto', 'Depositata', 1, 1, '1 fase', 'Prima operazione', 'OK', 'OK', 300.0, 150.0, 25.0, '6001857', '1125806', 'MARIO', 'admin', 'admin'),
(2, 'MARIO MAZZA 2 [2000]', 2000.0, 'Svolto', '', 1, 1, '1 fase', 'Prima operazione', 'OK', 'OK', 500.0, 250.0, 25.0, '6001858', '1125807', 'MARIO', 'admin', 'admin'),

-- Gruppo 3 clienti
(3, 'MIRKO MINATI RIZZI [1876]', 1876.0, 'Svolto', 'Depositata', 1, 1, '1 fase', 'Prima operazione', 'OK', 'OK', 400.0, 200.0, 25.0, '6001859', '1125808', 'FEDE', 'admin', 'admin'),
(3, 'SILVIA SAMMARTANO [1887]', 1887.0, 'Svolto', 'Depositata', 1, 1, '1 fase', 'Prima operazione', 'OK', 'OK', 450.0, 225.0, 25.0, '6001860', '1125809', 'FEDE', 'admin', 'admin'),
(3, 'PIERA ANDRANI [1000]', 1000.0, 'Non svolto', '', 1, 1, '', '', '', '', 0.0, 0.0, 25.0, '', '', 'FEDE', 'admin', 'admin'),
(3, 'PAOLA PIRAS [1000]', 1000.0, 'Non svolto', '', 1, 1, '', '', '', '', 0.0, 0.0, 25.0, '', '', 'FEDE', 'admin', 'admin'),
(3, 'MAURIZIO PETRACHI [1000]', 1000.0, 'Non svolto', '', 1, 1, '', '', '', '', 0.0, 0.0, 25.0, '', '', 'FEDE', 'admin', 'admin')
ON CONFLICT DO NOTHING;

-- 7. Crea viste per calcoli automatici
CREATE OR REPLACE VIEW gruppi_pamm_statistics AS
SELECT 
    g.id,
    g.nome_gruppo,
    g.manager,
    g.capitale_totale,
    g.numero_membri_gruppo,
    COUNT(c.id) as numero_clienti_attivi,
    COUNT(CASE WHEN c.stato_prop = 'Svolto' THEN 1 END) as numero_clienti_svolti,
    COUNT(CASE WHEN c.deposito_pamm = 'Depositata' THEN 1 END) as numero_clienti_depositati,
    COALESCE(SUM(c.importo_cliente), 0) as totale_importi,
    COALESCE(SUM(c.prelievo_prop), 0) as totale_prelievi_prop,
    COALESCE(SUM(c.prelievo_profit), 0) as totale_prelievi_profit,
    COALESCE(AVG(c.commissioni_percentuale), 0) as commissioni_medie
FROM gruppi_pamm_gruppi g
LEFT JOIN clienti_gruppi_pamm c ON g.id = c.gruppo_pamm_id
GROUP BY g.id, g.nome_gruppo, g.manager, g.capitale_totale, g.numero_membri_gruppo;

-- 8. Funzione per aggiornare statistiche gruppo
CREATE OR REPLACE FUNCTION update_gruppo_statistics(gruppo_id INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE gruppi_pamm_gruppi 
    SET 
        capitale_totale = (
            SELECT COALESCE(SUM(importo_cliente), 0) 
            FROM clienti_gruppi_pamm 
            WHERE gruppo_pamm_id = gruppo_id
        ),
        data_aggiornamento = NOW()
    WHERE id = gruppo_id;
END;
$$ LANGUAGE plpgsql;

-- 9. Trigger per aggiornare statistiche automaticamente
CREATE OR REPLACE FUNCTION trigger_update_gruppo_stats()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM update_gruppo_statistics(COALESCE(NEW.gruppo_pamm_id, OLD.gruppo_pamm_id));
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_gruppo_stats_on_clienti_change
    AFTER INSERT OR UPDATE OR DELETE ON clienti_gruppi_pamm
    FOR EACH ROW
    EXECUTE FUNCTION trigger_update_gruppo_stats();

-- 10. Verifica creazione tabelle
SELECT 'Tabelle create con successo!' as status;

-- 11. Mostra dati di esempio
SELECT 
    g.nome_gruppo,
    g.manager,
    COUNT(c.id) as numero_clienti,
    COALESCE(SUM(c.importo_cliente), 0) as totale_importi
FROM gruppi_pamm_gruppi g
LEFT JOIN clienti_gruppi_pamm c ON g.id = c.gruppo_pamm_id
GROUP BY g.id, g.nome_gruppo, g.manager
ORDER BY g.nome_gruppo;

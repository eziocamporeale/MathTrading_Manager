-- Schema Supabase per Dashboard Matematico Prop/Broker
-- Creato da Ezio Camporeale

-- ==================== TABELLE AUTENTICAZIONE ====================

-- Tabella ruoli utenti
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    permissions JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabella utenti
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    role_id INTEGER REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    notes TEXT,
    last_login TIMESTAMP WITH TIME ZONE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==================== TABELLE BUSINESS ====================

-- Tabella Broker
CREATE TABLE IF NOT EXISTS brokers (
    id SERIAL PRIMARY KEY,
    nome_broker VARCHAR(255) NOT NULL,
    tipo_broker VARCHAR(100),
    regolamentazione VARCHAR(100),
    paese VARCHAR(100),
    sito_web VARCHAR(255),
    spread_minimo DECIMAL(10,5),
    commissioni DECIMAL(10,5),
    leverage_massimo INTEGER,
    deposito_minimo DECIMAL(15,2),
    valute_supportate TEXT,
    piattaforme TEXT,
    stato VARCHAR(50) DEFAULT 'Attivo',
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255),
    aggiornato_da VARCHAR(255)
);

-- Tabella Prop Firms
CREATE TABLE IF NOT EXISTS prop_firms (
    id SERIAL PRIMARY KEY,
    nome_prop VARCHAR(255) NOT NULL,
    tipo_prop VARCHAR(100),
    capitale_iniziale DECIMAL(15,2),
    drawdown_massimo DECIMAL(10,2),
    profit_target DECIMAL(10,2),
    regole_trading TEXT,
    restrizioni_orarie TEXT,
    strumenti_permessi TEXT,
    broker_associati TEXT,
    commissioni DECIMAL(10,5),
    fee_mensile DECIMAL(10,2),
    stato VARCHAR(50) DEFAULT 'Attiva',
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255),
    aggiornato_da VARCHAR(255)
);

-- Tabella Wallets
CREATE TABLE IF NOT EXISTS wallets (
    id SERIAL PRIMARY KEY,
    indirizzo_wallet VARCHAR(255) NOT NULL,
    tipo_wallet VARCHAR(100),
    nome_wallet VARCHAR(255),
    saldo_attuale DECIMAL(20,8),
    valuta VARCHAR(10),
    exchange VARCHAR(100),
    chiave_privata TEXT, -- Crittografata
    frase_seed TEXT, -- Crittografata
    stato VARCHAR(50) DEFAULT 'Attivo',
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255),
    aggiornato_da VARCHAR(255)
);

-- Tabella Pack Copiatori
CREATE TABLE IF NOT EXISTS pack_copiatori (
    id SERIAL PRIMARY KEY,
    numero_pack VARCHAR(100) NOT NULL,
    broker_id INTEGER REFERENCES brokers(id),
    account_number VARCHAR(100),
    password_account TEXT, -- Crittografata
    server_broker VARCHAR(100),
    tipo_account VARCHAR(50),
    capitale_iniziale DECIMAL(15,2),
    saldo_attuale DECIMAL(15,2),
    profit_loss DECIMAL(15,2),
    drawdown_massimo DECIMAL(10,2),
    stato VARCHAR(50) DEFAULT 'Attivo',
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255),
    aggiornato_da VARCHAR(255)
);

-- Tabella Gruppi PAMM
CREATE TABLE IF NOT EXISTS gruppi_pamm (
    id SERIAL PRIMARY KEY,
    nome_gruppo VARCHAR(255) NOT NULL,
    manager VARCHAR(255),
    broker_id INTEGER REFERENCES brokers(id),
    account_pamm VARCHAR(100),
    capitale_totale DECIMAL(15,2),
    numero_partecipanti INTEGER DEFAULT 0,
    performance_totale DECIMAL(10,2),
    performance_mensile DECIMAL(10,2),
    drawdown_massimo DECIMAL(10,2),
    commissioni_manager DECIMAL(10,2),
    commissioni_broker DECIMAL(10,2),
    stato VARCHAR(50) DEFAULT 'Attivo',
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255),
    aggiornato_da VARCHAR(255)
);

-- Tabella Incroci
CREATE TABLE IF NOT EXISTS incroci (
    id SERIAL PRIMARY KEY,
    nome_incrocio VARCHAR(255) NOT NULL,
    broker_id INTEGER REFERENCES brokers(id),
    prop_id INTEGER REFERENCES prop_firms(id),
    wallet_id INTEGER REFERENCES wallets(id),
    gruppo_pamm_id INTEGER REFERENCES gruppi_pamm(id),
    pack_copiatore_id INTEGER REFERENCES pack_copiatori(id),
    tipo_incrocio VARCHAR(100),
    descrizione TEXT,
    performance_totale DECIMAL(10,2),
    rischio_totale DECIMAL(10,2),
    stato VARCHAR(50) DEFAULT 'Attivo',
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255),
    aggiornato_da VARCHAR(255)
);

-- Tabella Utenti
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    ruolo VARCHAR(50) DEFAULT 'Viewer',
    attivo BOOLEAN DEFAULT TRUE,
    ultimo_accesso TIMESTAMP WITH TIME ZONE,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255),
    aggiornato_da VARCHAR(255)
);

-- Tabella Transazioni Wallet
CREATE TABLE IF NOT EXISTS transazioni_wallet (
    id SERIAL PRIMARY KEY,
    wallet_id INTEGER REFERENCES wallets(id),
    tipo_transazione VARCHAR(100),
    importo DECIMAL(20,8),
    valuta VARCHAR(10),
    indirizzo_destinazione VARCHAR(255),
    hash_transazione VARCHAR(255),
    fee_transazione DECIMAL(20,8),
    stato VARCHAR(50) DEFAULT 'Pending',
    note TEXT,
    data_transazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255)
);

-- Tabella Performance History
CREATE TABLE IF NOT EXISTS performance_history (
    id SERIAL PRIMARY KEY,
    entita_tipo VARCHAR(100), -- broker, prop, wallet, pack_copiatore, gruppo_pamm
    entita_id INTEGER,
    data_performance TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    valore_iniziale DECIMAL(20,8),
    valore_finale DECIMAL(20,8),
    profit_loss DECIMAL(20,8),
    percentuale_variazione DECIMAL(10,2),
    drawdown DECIMAL(10,2),
    note TEXT,
    data_creazione TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creato_da VARCHAR(255)
);

-- Indici per migliorare le performance
CREATE INDEX IF NOT EXISTS idx_brokers_stato ON brokers(stato);
CREATE INDEX IF NOT EXISTS idx_prop_firms_stato ON prop_firms(stato);
CREATE INDEX IF NOT EXISTS idx_wallets_stato ON wallets(stato);
CREATE INDEX IF NOT EXISTS idx_pack_copiatori_stato ON pack_copiatori(stato);
CREATE INDEX IF NOT EXISTS idx_gruppi_pamm_stato ON gruppi_pamm(stato);
CREATE INDEX IF NOT EXISTS idx_incroci_stato ON incroci(stato);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_transazioni_wallet_wallet_id ON transazioni_wallet(wallet_id);
CREATE INDEX IF NOT EXISTS idx_performance_history_entita ON performance_history(entita_tipo, entita_id);

-- Trigger per aggiornare automaticamente data_aggiornamento
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_aggiornamento = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Applica il trigger a tutte le tabelle con data_aggiornamento
CREATE TRIGGER update_brokers_updated_at BEFORE UPDATE ON brokers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_prop_firms_updated_at BEFORE UPDATE ON prop_firms FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_wallets_updated_at BEFORE UPDATE ON wallets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pack_copiatori_updated_at BEFORE UPDATE ON pack_copiatori FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gruppi_pamm_updated_at BEFORE UPDATE ON gruppi_pamm FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_incroci_updated_at BEFORE UPDATE ON incroci FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Inserimento dati di esempio
INSERT INTO brokers (nome_broker, tipo_broker, regolamentazione, paese, spread_minimo, commissioni, leverage_massimo, deposito_minimo, stato, creato_da) VALUES
('IC Markets', 'ECN', 'ASIC', 'Australia', 0.0, 3.5, 500, 200.00, 'Attivo', 'admin'),
('Pepperstone', 'ECN', 'FCA', 'Regno Unito', 0.0, 3.5, 500, 200.00, 'Attivo', 'admin'),
('XM', 'Market Maker', 'CySEC', 'Cipro', 1.0, 0.0, 888, 5.00, 'Attivo', 'admin'),
('FXCM', 'Market Maker', 'FCA', 'Regno Unito', 1.2, 0.0, 400, 50.00, 'Attivo', 'admin'),
('OANDA', 'Market Maker', 'FCA', 'Regno Unito', 1.0, 0.0, 50, 0.00, 'Attivo', 'admin');

INSERT INTO prop_firms (nome_prop, tipo_prop, capitale_iniziale, drawdown_massimo, profit_target, commissioni, fee_mensile, stato, creato_da) VALUES
('FTMO', 'Evaluation', 10000.00, 10.00, 10.00, 0.0, 0.0, 'Attiva', 'admin'),
('MyForexFunds', 'Evaluation', 10000.00, 12.00, 8.00, 0.0, 0.0, 'Attiva', 'admin'),
('The5ers', 'Evaluation', 10000.00, 8.00, 8.00, 0.0, 0.0, 'Attiva', 'admin'),
('TopStep', 'Evaluation', 10000.00, 10.00, 10.00, 0.0, 0.0, 'Attiva', 'admin'),
('Apex Trader Funding', 'Evaluation', 10000.00, 10.00, 10.00, 0.0, 0.0, 'Attiva', 'admin');

INSERT INTO wallets (indirizzo_wallet, tipo_wallet, nome_wallet, saldo_attuale, valuta, exchange, stato, creato_da) VALUES
('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'Bitcoin', 'Wallet Bitcoin Principale', 0.5, 'BTC', 'Binance', 'Attivo', 'admin'),
('0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6', 'Ethereum', 'Wallet Ethereum Principale', 2.5, 'ETH', 'Coinbase', 'Attivo', 'admin'),
('TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE', 'Tron', 'Wallet Tron Principale', 1000.0, 'TRX', 'Binance', 'Attivo', 'admin'),
('D7Y55P7VQJ5VQJ5VQJ5VQJ5VQJ5VQJ5VQJ5', 'Dogecoin', 'Wallet Dogecoin Principale', 5000.0, 'DOGE', 'Binance', 'Attivo', 'admin'),
('LTC1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'Litecoin', 'Wallet Litecoin Principale', 10.0, 'LTC', 'Binance', 'Attivo', 'admin');

INSERT INTO pack_copiatori (numero_pack, broker_id, account_number, server_broker, tipo_account, capitale_iniziale, saldo_attuale, stato, creato_da) VALUES
('PACK001', 1, '12345678', 'ICMarketsSC-Demo', 'Demo', 10000.00, 10500.00, 'Attivo', 'admin'),
('PACK002', 2, '87654321', 'Pepperstone-Demo', 'Demo', 10000.00, 9800.00, 'Attivo', 'admin'),
('PACK003', 3, '11223344', 'XM-Demo', 'Demo', 10000.00, 11200.00, 'Attivo', 'admin'),
('PACK004', 4, '44332211', 'FXCM-Demo', 'Demo', 10000.00, 9500.00, 'Attivo', 'admin'),
('PACK005', 5, '55667788', 'OANDA-Demo', 'Demo', 10000.00, 10800.00, 'Attivo', 'admin');

INSERT INTO gruppi_pamm (nome_gruppo, manager, broker_id, account_pamm, capitale_totale, numero_partecipanti, performance_totale, performance_mensile, stato, creato_da) VALUES
('Gruppo Alpha', 'Manager Alpha', 1, 'PAMM001', 100000.00, 5, 15.5, 2.3, 'Attivo', 'admin'),
('Gruppo Beta', 'Manager Beta', 2, 'PAMM002', 75000.00, 3, 12.8, 1.8, 'Attivo', 'admin'),
('Gruppo Gamma', 'Manager Gamma', 3, 'PAMM003', 50000.00, 2, 8.2, 1.2, 'Attivo', 'admin'),
('Gruppo Delta', 'Manager Delta', 4, 'PAMM004', 25000.00, 1, 5.5, 0.8, 'Attivo', 'admin'),
('Gruppo Epsilon', 'Manager Epsilon', 5, 'PAMM005', 15000.00, 1, 3.2, 0.5, 'Attivo', 'admin');

INSERT INTO incroci (nome_incrocio, broker_id, prop_id, wallet_id, gruppo_pamm_id, pack_copiatore_id, tipo_incrocio, descrizione, performance_totale, stato, creato_da) VALUES
('Incrocio Alpha', 1, 1, 1, 1, 1, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 18.5, 'Attivo', 'admin'),
('Incrocio Beta', 2, 2, 2, 2, 2, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 15.2, 'Attivo', 'admin'),
('Incrocio Gamma', 3, 3, 3, 3, 3, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 12.8, 'Attivo', 'admin'),
('Incrocio Delta', 4, 4, 4, 4, 4, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 9.5, 'Attivo', 'admin'),
('Incrocio Epsilon', 5, 5, 5, 5, 5, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 7.2, 'Attivo', 'admin');

-- ==================== DATI DI DEFAULT ====================

-- Inserimento ruoli di default
INSERT INTO roles (name, description, permissions) VALUES
('Admin', 'Amministratore completo del sistema', '["all"]'),
('Manager', 'Manager con permessi di gestione completa', '["manage_brokers", "manage_props", "manage_wallets", "manage_packs", "manage_pamm", "manage_incroci", "view_reports"]'),
('Trader', 'Trader con permessi di trading', '["view_brokers", "view_props", "manage_wallets", "view_packs", "view_pamm", "view_incroci"]'),
('Copiatore', 'Copiatore con permessi limitati', '["view_brokers", "view_props", "manage_packs", "view_wallets"]'),
('PAMM Manager', 'Manager PAMM con permessi specifici', '["view_brokers", "manage_pamm", "view_wallets", "view_incroci"]'),
('Viewer', 'Visualizzatore con permessi limitati', '["view_brokers", "view_props", "view_wallets", "view_packs", "view_pamm", "view_incroci"]')
ON CONFLICT (name) DO NOTHING;

-- Inserimento utenti di default
INSERT INTO users (username, email, password_hash, first_name, last_name, role_id, is_active, is_admin, created_by) VALUES
('admin', 'admin@matematico.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K', 'Admin', 'Sistema', 1, true, true, 1),
('demo', 'demo@matematico.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K', 'Demo', 'User', 2, true, false, 1)
ON CONFLICT (username) DO NOTHING;

-- Abilita Row Level Security (RLS) per tutte le tabelle
ALTER TABLE roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE brokers ENABLE ROW LEVEL SECURITY;
ALTER TABLE prop_firms ENABLE ROW LEVEL SECURITY;
ALTER TABLE wallets ENABLE ROW LEVEL SECURITY;
ALTER TABLE pack_copiatori ENABLE ROW LEVEL SECURITY;
ALTER TABLE gruppi_pamm ENABLE ROW LEVEL SECURITY;
ALTER TABLE incroci ENABLE ROW LEVEL SECURITY;
ALTER TABLE transazioni_wallet ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_history ENABLE ROW LEVEL SECURITY;

-- Politiche RLS per permettere accesso completo agli admin
CREATE POLICY "Admin access all" ON roles FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON users FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON brokers FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON prop_firms FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON wallets FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON pack_copiatori FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON gruppi_pamm FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON incroci FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON transazioni_wallet FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON performance_history FOR ALL TO authenticated USING (true);

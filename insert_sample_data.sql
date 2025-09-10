-- Inserimento Dati di Esempio per DASH_PROP_BROKER
-- Creato da Ezio Camporeale

-- Inserimento Broker
INSERT INTO brokers (nome_broker, tipo_broker, regolamentazione, paese, spread_minimo, commissioni, leverage_massimo, deposito_minimo, stato, creato_da) VALUES
('IC Markets', 'ECN', 'ASIC', 'Australia', 0.0, 3.5, 500, 200.00, 'Attivo', 'admin'),
('Pepperstone', 'ECN', 'FCA', 'Regno Unito', 0.0, 3.5, 500, 200.00, 'Attivo', 'admin'),
('XM', 'Market Maker', 'CySEC', 'Cipro', 1.0, 0.0, 888, 5.00, 'Attivo', 'admin'),
('FXCM', 'Market Maker', 'FCA', 'Regno Unito', 1.2, 0.0, 400, 50.00, 'Attivo', 'admin'),
('OANDA', 'Market Maker', 'FCA', 'Regno Unito', 1.0, 0.0, 50, 0.00, 'Attivo', 'admin');

-- Inserimento Prop Firms
INSERT INTO prop_firms (nome_prop, tipo_prop, capitale_iniziale, drawdown_massimo, profit_target, commissioni, fee_mensile, stato, creato_da) VALUES
('FTMO', 'Evaluation', 10000.00, 10.00, 10.00, 0.0, 0.0, 'Attiva', 'admin'),
('MyForexFunds', 'Evaluation', 10000.00, 12.00, 8.00, 0.0, 0.0, 'Attiva', 'admin'),
('The5ers', 'Evaluation', 10000.00, 8.00, 8.00, 0.0, 0.0, 'Attiva', 'admin'),
('TopStep', 'Evaluation', 10000.00, 10.00, 10.00, 0.0, 0.0, 'Attiva', 'admin'),
('Apex Trader Funding', 'Evaluation', 10000.00, 10.00, 10.00, 0.0, 0.0, 'Attiva', 'admin');

-- Inserimento Wallet
INSERT INTO wallets (indirizzo_wallet, tipo_wallet, nome_wallet, saldo_attuale, valuta, exchange, stato, creato_da) VALUES
('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'Bitcoin', 'Wallet Bitcoin Principale', 0.5, 'BTC', 'Binance', 'Attivo', 'admin'),
('0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6', 'Ethereum', 'Wallet Ethereum Principale', 2.5, 'ETH', 'Coinbase', 'Attivo', 'admin'),
('TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE', 'Tron', 'Wallet Tron Principale', 1000.0, 'TRX', 'Binance', 'Attivo', 'admin'),
('D7Y55P7VQJ5VQJ5VQJ5VQJ5VQJ5VQJ5VQJ5', 'Dogecoin', 'Wallet Dogecoin Principale', 5000.0, 'DOGE', 'Binance', 'Attivo', 'admin'),
('LTC1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'Litecoin', 'Wallet Litecoin Principale', 10.0, 'LTC', 'Binance', 'Attivo', 'admin');

-- Inserimento Pack Copiatori
INSERT INTO pack_copiatori (numero_pack, broker_id, account_number, server_broker, tipo_account, capitale_iniziale, saldo_attuale, stato, creato_da) VALUES
('PACK001', 1, '12345678', 'ICMarketsSC-Demo', 'Demo', 10000.00, 10500.00, 'Attivo', 'admin'),
('PACK002', 2, '87654321', 'Pepperstone-Demo', 'Demo', 10000.00, 9800.00, 'Attivo', 'admin'),
('PACK003', 3, '11223344', 'XM-Demo', 'Demo', 10000.00, 11200.00, 'Attivo', 'admin'),
('PACK004', 4, '44332211', 'FXCM-Demo', 'Demo', 10000.00, 9500.00, 'Attivo', 'admin'),
('PACK005', 5, '55667788', 'OANDA-Demo', 'Demo', 10000.00, 10800.00, 'Attivo', 'admin');

-- Inserimento Gruppi PAMM
INSERT INTO gruppi_pamm (nome_gruppo, manager, broker_id, account_pamm, capitale_totale, numero_partecipanti, performance_totale, performance_mensile, stato, creato_da) VALUES
('Gruppo Alpha', 'Manager Alpha', 1, 'PAMM001', 100000.00, 5, 15.5, 2.3, 'Attivo', 'admin'),
('Gruppo Beta', 'Manager Beta', 2, 'PAMM002', 75000.00, 3, 12.8, 1.8, 'Attivo', 'admin'),
('Gruppo Gamma', 'Manager Gamma', 3, 'PAMM003', 50000.00, 2, 8.2, 1.2, 'Attivo', 'admin'),
('Gruppo Delta', 'Manager Delta', 4, 'PAMM004', 25000.00, 1, 5.5, 0.8, 'Attivo', 'admin'),
('Gruppo Epsilon', 'Manager Epsilon', 5, 'PAMM005', 15000.00, 1, 3.2, 0.5, 'Attivo', 'admin');

-- Inserimento Incroci
INSERT INTO incroci (nome_incrocio, broker_id, prop_id, wallet_id, gruppo_pamm_id, pack_copiatore_id, tipo_incrocio, descrizione, performance_totale, stato, creato_da) VALUES
('Incrocio Alpha', 1, 1, 1, 1, 1, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 18.5, 'Attivo', 'admin'),
('Incrocio Beta', 2, 2, 2, 2, 2, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 15.2, 'Attivo', 'admin'),
('Incrocio Gamma', 3, 3, 3, 3, 3, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 12.8, 'Attivo', 'admin'),
('Incrocio Delta', 4, 4, 4, 4, 4, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 9.5, 'Attivo', 'admin'),
('Incrocio Epsilon', 5, 5, 5, 5, 5, 'Broker-Prop-Wallet-PAMM-Pack', 'Incrocio completo con tutti i componenti', 7.2, 'Attivo', 'admin');

-- Inserimento Utente Admin
INSERT INTO users (username, email, password_hash, nome, cognome, ruolo, creato_da) VALUES
('admin', 'admin@matematico.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K', 'Admin', 'Sistema', 'Admin', 'system');

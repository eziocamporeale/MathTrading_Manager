-- Script per aggiornare il database con le tabelle di autenticazione
-- Eseguire questo script nel Supabase SQL Editor

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

-- Abilita Row Level Security (RLS) per le nuove tabelle
ALTER TABLE roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Politiche RLS per permettere accesso completo agli admin
CREATE POLICY "Admin access all" ON roles FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON users FOR ALL TO authenticated USING (true);

-- Aggiorna le politiche esistenti per includere le nuove tabelle
DROP POLICY IF EXISTS "Admin access all" ON brokers;
DROP POLICY IF EXISTS "Admin access all" ON prop_firms;
DROP POLICY IF EXISTS "Admin access all" ON wallets;
DROP POLICY IF EXISTS "Admin access all" ON pack_copiatori;
DROP POLICY IF EXISTS "Admin access all" ON gruppi_pamm;
DROP POLICY IF EXISTS "Admin access all" ON incroci;
DROP POLICY IF EXISTS "Admin access all" ON transazioni_wallet;
DROP POLICY IF EXISTS "Admin access all" ON performance_history;

CREATE POLICY "Admin access all" ON brokers FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON prop_firms FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON wallets FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON pack_copiatori FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON gruppi_pamm FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON incroci FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON transazioni_wallet FOR ALL TO authenticated USING (true);
CREATE POLICY "Admin access all" ON performance_history FOR ALL TO authenticated USING (true);

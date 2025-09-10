-- Script per creare le tabelle di autenticazione
-- Eseguire questo script nel Supabase SQL Editor PRIMA di tutto

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

-- ==================== RLS POLICIES ====================

-- Abilita Row Level Security
ALTER TABLE roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Politiche RLS permissive (per ora)
CREATE POLICY "Allow all operations" ON roles FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON users FOR ALL USING (true);

-- ==================== VERIFICA ====================

-- Verifica che le tabelle siano state create
SELECT 'roles' as table_name, count(*) as row_count FROM roles
UNION ALL
SELECT 'users' as table_name, count(*) as row_count FROM users;

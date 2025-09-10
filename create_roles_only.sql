-- Script per creare solo la tabella roles
-- Eseguire questo script nel Supabase SQL Editor

-- Crea la tabella roles se non esiste
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    permissions JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inserisci ruoli di default
INSERT INTO roles (name, description, permissions) VALUES
('Admin', 'Amministratore completo del sistema', '["all"]'::jsonb),
('Manager', 'Manager con permessi di gestione completa', '["manage_brokers", "manage_props", "manage_wallets", "manage_packs", "manage_pamm", "manage_incroci", "view_reports"]'::jsonb),
('Trader', 'Trader con permessi di trading', '["view_brokers", "view_props", "manage_wallets", "view_packs", "view_pamm", "view_incroci"]'::jsonb),
('Copiatore', 'Copiatore con permessi limitati', '["view_brokers", "view_props", "manage_packs", "view_wallets"]'::jsonb),
('PAMM Manager', 'Manager PAMM con permessi specifici', '["view_brokers", "manage_pamm", "view_wallets", "view_incroci"]'::jsonb),
('Viewer', 'Visualizzatore con permessi limitati', '["view_brokers", "view_props", "view_wallets", "view_packs", "view_pamm", "view_incroci"]'::jsonb)
ON CONFLICT (name) DO NOTHING;

-- Verifica creazione
SELECT 'RUOLI CREATI:' as info;
SELECT id, name, description FROM roles ORDER BY id;

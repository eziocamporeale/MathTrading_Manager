-- Script completo per configurare il sistema di autenticazione
-- Eseguire questo script nel Supabase SQL Editor

-- ==================== STEP 1: CONTROLLA STRUTTURA ESISTENTE ====================

-- Mostra struttura tabella users esistente
SELECT 'STRUTTURA TABELLA USERS ESISTENTE:' as info;
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

-- Controlla se esiste la tabella roles
SELECT 'TABELLA ROLES ESISTENTE:' as info;
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_name = 'roles'
) as roles_exists;

-- ==================== STEP 2: CREA TABELLA ROLES SE NON ESISTE ====================

CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    permissions JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==================== STEP 3: ADATTA TABELLA USERS ====================

-- Aggiungi colonne mancanti alla tabella users esistente
DO $$ 
BEGIN
    -- Aggiungi first_name se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'first_name') THEN
        ALTER TABLE users ADD COLUMN first_name VARCHAR(50);
        RAISE NOTICE 'Aggiunta colonna first_name';
    END IF;
    
    -- Aggiungi last_name se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'last_name') THEN
        ALTER TABLE users ADD COLUMN last_name VARCHAR(50);
        RAISE NOTICE 'Aggiunta colonna last_name';
    END IF;
    
    -- Aggiungi phone se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'phone') THEN
        ALTER TABLE users ADD COLUMN phone VARCHAR(20);
        RAISE NOTICE 'Aggiunta colonna phone';
    END IF;
    
    -- Aggiungi role_id se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'role_id') THEN
        ALTER TABLE users ADD COLUMN role_id INTEGER;
        RAISE NOTICE 'Aggiunta colonna role_id';
    END IF;
    
    -- Aggiungi is_active se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'is_active') THEN
        ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
        RAISE NOTICE 'Aggiunta colonna is_active';
    END IF;
    
    -- Aggiungi is_admin se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'is_admin') THEN
        ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Aggiunta colonna is_admin';
    END IF;
    
    -- Aggiungi notes se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'notes') THEN
        ALTER TABLE users ADD COLUMN notes TEXT;
        RAISE NOTICE 'Aggiunta colonna notes';
    END IF;
    
    -- Aggiungi last_login se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'last_login') THEN
        ALTER TABLE users ADD COLUMN last_login TIMESTAMP WITH TIME ZONE;
        RAISE NOTICE 'Aggiunta colonna last_login';
    END IF;
    
    -- Aggiungi created_by se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'created_by') THEN
        ALTER TABLE users ADD COLUMN created_by INTEGER;
        RAISE NOTICE 'Aggiunta colonna created_by';
    END IF;
    
    -- Aggiungi updated_at se non esiste
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'updated_at') THEN
        ALTER TABLE users ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
        RAISE NOTICE 'Aggiunta colonna updated_at';
    END IF;
END $$;

-- ==================== STEP 4: INSERISCI DATI DI DEFAULT ====================

-- Inserisci ruoli di default
INSERT INTO roles (name, description, permissions) VALUES
('Admin', 'Amministratore completo del sistema', '["all"]'),
('Manager', 'Manager con permessi di gestione completa', '["manage_brokers", "manage_props", "manage_wallets", "manage_packs", "manage_pamm", "manage_incroci", "view_reports"]'),
('Trader', 'Trader con permessi di trading', '["view_brokers", "view_props", "manage_wallets", "view_packs", "view_pamm", "view_incroci"]'),
('Copiatore', 'Copiatore con permessi limitati', '["view_brokers", "view_props", "manage_packs", "view_wallets"]'),
('PAMM Manager', 'Manager PAMM con permessi specifici', '["view_brokers", "manage_pamm", "view_wallets", "view_incroci"]'),
('Viewer', 'Visualizzatore con permessi limitati', '["view_brokers", "view_props", "view_wallets", "view_packs", "view_pamm", "view_incroci"]')
ON CONFLICT (name) DO NOTHING;

-- Inserisci utenti di default (solo se non esistono già)
INSERT INTO users (username, email, password_hash, first_name, last_name, role_id, is_active, is_admin, created_by) VALUES
('admin', 'admin@matematico.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K', 'Admin', 'Sistema', 1, true, true, 1),
('demo', 'demo@matematico.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K', 'Demo', 'User', 2, true, false, 1)
ON CONFLICT (username) DO UPDATE SET
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    role_id = EXCLUDED.role_id,
    is_active = EXCLUDED.is_active,
    is_admin = EXCLUDED.is_admin;

-- Assicurati che l'admin sia configurato correttamente
UPDATE users 
SET 
    first_name = 'Admin',
    last_name = 'Sistema',
    role_id = 1,
    is_admin = true,
    is_active = true
WHERE username = 'admin';

-- ==================== STEP 5: CONFIGURA RLS ====================

-- Abilita RLS
ALTER TABLE roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Elimina politiche esistenti
DROP POLICY IF EXISTS "Allow all operations" ON roles;
DROP POLICY IF EXISTS "Allow all operations" ON users;

-- Crea politiche RLS permissive
CREATE POLICY "Allow all operations" ON roles FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON users FOR ALL USING (true);

-- ==================== STEP 6: VERIFICA FINALE ====================

-- Mostra struttura finale
SELECT 'STRUTTURA FINALE TABELLA USERS:' as info;
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

-- Conta record
SELECT 'CONTEGGIO RECORD:' as info;
SELECT 'roles' as table_name, count(*) as row_count FROM roles
UNION ALL
SELECT 'users' as table_name, count(*) as row_count FROM users;

-- Mostra utenti creati
SELECT 'UTENTI CREATI:' as info;
SELECT username, first_name, last_name, role_id, is_active, is_admin FROM users;

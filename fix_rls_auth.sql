-- Script per risolvere problemi RLS con sistema di autenticazione
-- Eseguire questo script nel Supabase SQL Editor

-- Disabilita temporaneamente RLS per permettere inserimenti
ALTER TABLE roles DISABLE ROW LEVEL SECURITY;
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE brokers DISABLE ROW LEVEL SECURITY;
ALTER TABLE prop_firms DISABLE ROW LEVEL SECURITY;
ALTER TABLE wallets DISABLE ROW LEVEL SECURITY;
ALTER TABLE pack_copiatori DISABLE ROW LEVEL SECURITY;
ALTER TABLE gruppi_pamm DISABLE ROW LEVEL SECURITY;
ALTER TABLE incroci DISABLE ROW LEVEL SECURITY;
ALTER TABLE transazioni_wallet DISABLE ROW LEVEL SECURITY;
ALTER TABLE performance_history DISABLE ROW LEVEL SECURITY;

-- Elimina politiche esistenti
DROP POLICY IF EXISTS "Admin access all" ON roles;
DROP POLICY IF EXISTS "Admin access all" ON users;
DROP POLICY IF EXISTS "Admin access all" ON brokers;
DROP POLICY IF EXISTS "Admin access all" ON prop_firms;
DROP POLICY IF EXISTS "Admin access all" ON wallets;
DROP POLICY IF EXISTS "Admin access all" ON pack_copiatori;
DROP POLICY IF EXISTS "Admin access all" ON gruppi_pamm;
DROP POLICY IF EXISTS "Admin access all" ON incroci;
DROP POLICY IF EXISTS "Admin access all" ON transazioni_wallet;
DROP POLICY IF EXISTS "Admin access all" ON performance_history;

-- Crea nuove politiche RLS più permissive
CREATE POLICY "Allow all operations" ON roles FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON users FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON brokers FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON prop_firms FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON wallets FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON pack_copiatori FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON gruppi_pamm FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON incroci FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON transazioni_wallet FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON performance_history FOR ALL USING (true);

-- Riabilita RLS
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

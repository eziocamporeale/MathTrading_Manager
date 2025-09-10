-- Fix RLS Policies per DASH_PROP_BROKER
-- Risolve il problema di inserimento dati
-- Creato da Ezio Camporeale

-- Disabilita temporaneamente RLS per permettere inserimenti
ALTER TABLE brokers DISABLE ROW LEVEL SECURITY;
ALTER TABLE prop_firms DISABLE ROW LEVEL SECURITY;
ALTER TABLE wallets DISABLE ROW LEVEL SECURITY;
ALTER TABLE pack_copiatori DISABLE ROW LEVEL SECURITY;
ALTER TABLE gruppi_pamm DISABLE ROW LEVEL SECURITY;
ALTER TABLE incroci DISABLE ROW LEVEL SECURITY;
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE transazioni_wallet DISABLE ROW LEVEL SECURITY;
ALTER TABLE performance_history DISABLE ROW LEVEL SECURITY;

-- Oppure crea politiche RLS più permissive per inserimento
-- (Commenta le righe sopra e decommenta quelle sotto se preferisci mantenere RLS)

/*
-- Elimina politiche esistenti
DROP POLICY IF EXISTS "Admin access all" ON brokers;
DROP POLICY IF EXISTS "Admin access all" ON prop_firms;
DROP POLICY IF EXISTS "Admin access all" ON wallets;
DROP POLICY IF EXISTS "Admin access all" ON pack_copiatori;
DROP POLICY IF EXISTS "Admin access all" ON gruppi_pamm;
DROP POLICY IF EXISTS "Admin access all" ON incroci;
DROP POLICY IF EXISTS "Admin access all" ON users;
DROP POLICY IF EXISTS "Admin access all" ON transazioni_wallet;
DROP POLICY IF EXISTS "Admin access all" ON performance_history;

-- Crea politiche RLS permissive per tutti gli utenti autenticati
CREATE POLICY "Allow all for authenticated users" ON brokers FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON prop_firms FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON wallets FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON pack_copiatori FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON gruppi_pamm FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON incroci FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON users FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON transazioni_wallet FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for authenticated users" ON performance_history FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Crea politiche RLS per utenti anonimi (per sviluppo)
CREATE POLICY "Allow all for anon users" ON brokers FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON prop_firms FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON wallets FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON pack_copiatori FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON gruppi_pamm FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON incroci FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON users FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON transazioni_wallet FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon users" ON performance_history FOR ALL TO anon USING (true) WITH CHECK (true);
*/

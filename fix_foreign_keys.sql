-- Fix foreign key constraints per eliminazione broker
-- Esegui questo script nel SQL Editor di Supabase

-- Modifica foreign key per pack_copiatori per permettere eliminazione a cascata
ALTER TABLE pack_copiatori 
DROP CONSTRAINT IF EXISTS pack_copiatori_broker_id_fkey;

ALTER TABLE pack_copiatori 
ADD CONSTRAINT pack_copiatori_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;

-- Modifica foreign key per wallets per permettere eliminazione a cascata
ALTER TABLE wallets 
DROP CONSTRAINT IF EXISTS wallets_broker_id_fkey;

ALTER TABLE wallets 
ADD CONSTRAINT wallets_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;

-- Modifica foreign key per gruppi_pamm per permettere eliminazione a cascata
ALTER TABLE gruppi_pamm 
DROP CONSTRAINT IF EXISTS gruppi_pamm_broker_id_fkey;

ALTER TABLE gruppi_pamm 
ADD CONSTRAINT gruppi_pamm_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;

-- Modifica foreign key per incroci per permettere eliminazione a cascata
ALTER TABLE incroci 
DROP CONSTRAINT IF EXISTS incroci_broker_id_fkey;

ALTER TABLE incroci 
ADD CONSTRAINT incroci_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;

-- Verifica le foreign key esistenti
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    tc.constraint_name
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' 
  AND tc.table_schema = 'public'
  AND ccu.table_name = 'brokers';

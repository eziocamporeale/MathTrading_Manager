-- Fix foreign key constraints per eliminazione broker (VERSIONE SICURA)
-- Esegui questo script nel SQL Editor di Supabase

-- Prima verifica la struttura delle tabelle
-- Poi esegui solo le modifiche necessarie

-- 1. Aggiungi colonna phone se non esiste
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS phone VARCHAR(20);

-- 2. Verifica e modifica foreign key per pack_copiatori
-- Prima controlla se la colonna broker_id esiste
DO $$
BEGIN
    -- Se la colonna broker_id esiste, modifica la foreign key
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'pack_copiatori' 
        AND column_name = 'broker_id'
    ) THEN
        -- Rimuovi constraint esistente
        ALTER TABLE pack_copiatori 
        DROP CONSTRAINT IF EXISTS pack_copiatori_broker_id_fkey;
        
        -- Aggiungi nuovo constraint con CASCADE
        ALTER TABLE pack_copiatori 
        ADD CONSTRAINT pack_copiatori_broker_id_fkey 
        FOREIGN KEY (broker_id) REFERENCES brokers(id) 
        ON DELETE CASCADE;
        
        RAISE NOTICE 'Foreign key per pack_copiatori.broker_id modificata con successo';
    ELSE
        RAISE NOTICE 'Colonna broker_id non trovata in pack_copiatori';
    END IF;
END $$;

-- 3. Verifica e modifica foreign key per wallets
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'wallets' 
        AND column_name = 'broker_id'
    ) THEN
        ALTER TABLE wallets 
        DROP CONSTRAINT IF EXISTS wallets_broker_id_fkey;
        
        ALTER TABLE wallets 
        ADD CONSTRAINT wallets_broker_id_fkey 
        FOREIGN KEY (broker_id) REFERENCES brokers(id) 
        ON DELETE CASCADE;
        
        RAISE NOTICE 'Foreign key per wallets.broker_id modificata con successo';
    ELSE
        RAISE NOTICE 'Colonna broker_id non trovata in wallets';
    END IF;
END $$;

-- 4. Verifica e modifica foreign key per gruppi_pamm
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'gruppi_pamm' 
        AND column_name = 'broker_id'
    ) THEN
        ALTER TABLE gruppi_pamm 
        DROP CONSTRAINT IF EXISTS gruppi_pamm_broker_id_fkey;
        
        ALTER TABLE gruppi_pamm 
        ADD CONSTRAINT gruppi_pamm_broker_id_fkey 
        FOREIGN KEY (broker_id) REFERENCES brokers(id) 
        ON DELETE CASCADE;
        
        RAISE NOTICE 'Foreign key per gruppi_pamm.broker_id modificata con successo';
    ELSE
        RAISE NOTICE 'Colonna broker_id non trovata in gruppi_pamm';
    END IF;
END $$;

-- 5. Verifica e modifica foreign key per incroci
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'incroci' 
        AND column_name = 'broker_id'
    ) THEN
        ALTER TABLE incroci 
        DROP CONSTRAINT IF EXISTS incroci_broker_id_fkey;
        
        ALTER TABLE incroci 
        ADD CONSTRAINT incroci_broker_id_fkey 
        FOREIGN KEY (broker_id) REFERENCES brokers(id) 
        ON DELETE CASCADE;
        
        RAISE NOTICE 'Foreign key per incroci.broker_id modificata con successo';
    ELSE
        RAISE NOTICE 'Colonna broker_id non trovata in incroci';
    END IF;
END $$;

-- 6. Verifica finale delle foreign key
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
  AND ccu.table_name = 'brokers'
ORDER BY tc.table_name, kcu.column_name;

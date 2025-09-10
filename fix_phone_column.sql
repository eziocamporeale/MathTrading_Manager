-- Fix colonna phone mancante nella tabella users
-- Esegui questo script nel SQL Editor di Supabase

-- Aggiungi colonna phone se non esiste
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS phone VARCHAR(20);

-- Verifica la struttura della tabella
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

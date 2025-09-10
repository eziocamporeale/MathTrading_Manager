-- Script per controllare la struttura della tabella users esistente
-- Eseguire questo script nel Supabase SQL Editor

-- Controlla la struttura della tabella users
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

-- Controlla se esistono dati nella tabella users
SELECT COUNT(*) as user_count FROM users;

-- Mostra i primi 5 utenti esistenti
SELECT * FROM users LIMIT 5;

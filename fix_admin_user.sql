-- Script per correggere l'utente admin
-- Eseguire questo script nel Supabase SQL Editor

-- Aggiorna l'utente admin per renderlo effettivamente admin
UPDATE users 
SET 
    first_name = 'Admin',
    last_name = 'Sistema',
    role_id = 1,
    is_admin = true,
    is_active = true
WHERE username = 'admin';

-- Verifica la correzione
SELECT 'UTENTE ADMIN CORRETTO:' as info;
SELECT username, first_name, last_name, role_id, is_active, is_admin 
FROM users 
WHERE username = 'admin';

-- Mostra tutti gli utenti per verifica
SELECT 'TUTTI GLI UTENTI:' as info;
SELECT username, first_name, last_name, role_id, is_active, is_admin 
FROM users;

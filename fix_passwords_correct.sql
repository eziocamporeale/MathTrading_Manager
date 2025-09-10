-- Script per correggere le password degli utenti con hash corretti
-- Eseguire questo script nel Supabase SQL Editor

-- Aggiorna password admin (admin123)
UPDATE users 
SET password_hash = '$2b$12$kSmvy4fmCB2Im5F0mJWsVOPShQihlcq4F6mCJK.rlQZQoySAvbAeq'
WHERE username = 'admin';

-- Aggiorna password demo (demo123)
UPDATE users 
SET password_hash = '$2b$12$j8gc7ZGwSONDVZdyHACe6eIK1r./8TmViiXsGjfsqex.g3uTdRM4S'
WHERE username = 'demo';

-- Verifica aggiornamento
SELECT username, 
       CASE 
           WHEN password_hash = '$2b$12$kSmvy4fmCB2Im5F0mJWsVOPShQihlcq4F6mCJK.rlQZQoySAvbAeq' 
           THEN 'Password admin corretta' 
           ELSE 'Password admin errata' 
       END as admin_status,
       CASE 
           WHEN password_hash = '$2b$12$j8gc7ZGwSONDVZdyHACe6eIK1r./8TmViiXsGjfsqex.g3uTdRM4S' 
           THEN 'Password demo corretta' 
           ELSE 'Password demo errata' 
       END as demo_status
FROM users;
